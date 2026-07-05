#!/usr/bin/env python3
"""
Scrape Yuque docs through a real Chrome session.

The important part for Yuque's new doc list is link collection:
- doc rows are virtual/lazy rendered;
- visible doc links have a CSS-modules class like
  DocListItem-module_itemContent_Z01iZ;
- the script scrolls the virtual list container and accumulates hrefs until no
  new links appear.

Usage:
  python3 scrape_yuque.py https://www.yuque.com/xiumubai/doc --out yuque-docs
  python3 scrape_yuque.py https://www.yuque.com/xiumubai/doc --out yuque-docs --collect-only
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import time
from pathlib import Path
from urllib.parse import urldefrag, urljoin, urlparse


def slugify(text: str, fallback: str) -> str:
    text = re.sub(r"[\\/:*?\"<>|#]+", "-", text.strip())
    text = re.sub(r"\s+", "-", text)
    text = text.strip(".-")
    return text[:90] or fallback


def normalize_url(url: str, base_url: str) -> str:
    absolute = urljoin(base_url, url)
    clean, _ = urldefrag(absolute)
    return clean.rstrip("/")


def same_yuque_book(url: str, base_url: str) -> bool:
    parsed = urlparse(url)
    base = urlparse(base_url)
    if parsed.netloc != base.netloc:
        return False
    base_parts = [part for part in base.path.split("/") if part]
    parts = [part for part in parsed.path.split("/") if part]
    return len(parts) >= 2 and len(base_parts) >= 2 and parts[:2] == base_parts[:2]


COLLECT_LINKS_SCRIPT = r"""
async ({ maxRounds, idleRounds, scrollDelay }) => {
  const sleep = (ms) => new Promise(resolve => setTimeout(resolve, ms))
  const normalizeText = (text) => (text || '').replace(/\s+/g, ' ').trim()
  const linkSelector = [
    'a[class*="DocListItem-module_itemContent_"][href]',
    '[class*="DocListItem-module_itemContent_"] a[href]'
  ].join(',')

  const isVisible = (el) => {
    const rect = el.getBoundingClientRect()
    const style = window.getComputedStyle(el)
    return rect.width > 0 &&
      rect.height > 0 &&
      style.display !== 'none' &&
      style.visibility !== 'hidden'
  }

  const findScrollContainer = () => {
    const firstLink = document.querySelector(linkSelector)
    let node = firstLink
    while (node && node !== document.body) {
      const parent = node.parentElement
      if (!parent) break
      const style = window.getComputedStyle(parent)
      if (/(auto|scroll)/.test(style.overflowY) && parent.scrollHeight > parent.clientHeight) {
        return parent
      }
      node = parent
    }

    const candidates = [
      ...document.querySelectorAll('[class*="DocList" i], [class*="docList" i], [class*="catalog" i], [class*="sidebar" i], aside, nav, div')
    ].filter(el => {
      const style = window.getComputedStyle(el)
      return isVisible(el) &&
        /(auto|scroll)/.test(style.overflowY) &&
        el.scrollHeight > el.clientHeight &&
        el.querySelector(linkSelector)
    })

    return candidates.sort((a, b) => b.scrollHeight - a.scrollHeight)[0] ||
      document.scrollingElement ||
      document.documentElement
  }

  const collectVisible = (store) => {
    for (const a of document.querySelectorAll(linkSelector)) {
      if (!isVisible(a)) continue
      const href = a.href || a.getAttribute('href') || ''
      const title =
        a.querySelector('[title]')?.getAttribute('title') ||
        normalizeText(a.querySelector('[class*="title" i]')?.innerText) ||
        normalizeText(a.innerText).split('\n')[0] ||
        href
      if (!href || !title) continue
      const key = href.split('#')[0].replace(/\/$/, '')
      if (!store.has(key)) {
        store.set(key, { title, url: href })
      }
    }
  }

  const store = new Map()
  const scroller = findScrollContainer()
  let stable = 0
  let lastSize = 0

  if (scroller) scroller.scrollTop = 0
  await sleep(scrollDelay)

  for (let round = 0; round < maxRounds && stable < idleRounds; round += 1) {
    collectVisible(store)
    stable = store.size === lastSize ? stable + 1 : 0
    lastSize = store.size

    if (!scroller) break
    const before = scroller.scrollTop
    const step = Math.max(320, Math.floor(scroller.clientHeight * 0.85))
    scroller.scrollTop = Math.min(scroller.scrollHeight, scroller.scrollTop + step)
    await sleep(scrollDelay)

    const atBottom = scroller.scrollTop === before ||
      scroller.scrollTop + scroller.clientHeight >= scroller.scrollHeight - 2
    if (atBottom) {
      collectVisible(store)
      stable += 1
    }
  }

  return {
    items: [...store.values()],
    count: store.size,
    scrollTop: scroller?.scrollTop || 0,
    scrollHeight: scroller?.scrollHeight || 0,
    clientHeight: scroller?.clientHeight || 0
  }
}
"""


EXTRACT_PAGE_SCRIPT = r"""
() => {
  const pick = (selectors) => {
    for (const selector of selectors) {
      const node = document.querySelector(selector)
      if (node && node.innerText && node.innerText.trim().length > 80) return node
    }
    return document.querySelector('article') || document.querySelector('main') || document.body
  }

  const title =
    document.querySelector('h1')?.innerText?.trim() ||
    document.title.replace(/语雀|Yuque/g, '').trim() ||
    location.pathname.split('/').filter(Boolean).pop() ||
    'untitled'

  const content = pick([
    '.lake-content',
    '.ne-viewer-body',
    '.yuque-doc-content',
    '.doc-reader',
    '[data-testid="doc-reader"]',
    '[data-testid="reader"]',
    'article',
    'main'
  ])

  const escape = (text) => text.replace(/\u00a0/g, ' ').replace(/[ \t]+\n/g, '\n').trim()
  const codeText = (node) => node.innerText.replace(/\n+$/g, '')

  const walk = (node, depth = 0) => {
    if (!node) return ''
    if (node.nodeType === Node.TEXT_NODE) return node.textContent || ''
    if (node.nodeType !== Node.ELEMENT_NODE) return ''

    const tag = node.tagName.toLowerCase()
    if (tag === 'script' || tag === 'style' || tag === 'svg') return ''
    if (tag === 'br') return '\n'
    if (tag === 'hr') return '\n\n---\n\n'
    if (tag === 'img') {
      const src = node.getAttribute('src') || node.getAttribute('data-src') || ''
      const alt = node.getAttribute('alt') || ''
      return src ? `![${alt}](${src})` : ''
    }
    if (tag === 'a') {
      const text = escape([...node.childNodes].map(child => walk(child, depth)).join(''))
      const href = node.href || node.getAttribute('href') || ''
      return href && text ? `[${text}](${href})` : text
    }
    if (tag === 'code' && node.parentElement?.tagName?.toLowerCase() !== 'pre') {
      return '`' + codeText(node).trim() + '`'
    }
    if (tag === 'pre') {
      return '\n\n```text\n' + codeText(node) + '\n```\n\n'
    }
    if (/^h[1-6]$/.test(tag)) {
      const level = Number(tag.slice(1))
      const text = escape([...node.childNodes].map(child => walk(child, depth)).join(''))
      return text ? `\n\n${'#'.repeat(level)} ${text}\n\n` : ''
    }
    if (tag === 'li') {
      const text = escape([...node.childNodes].map(child => walk(child, depth + 1)).join(''))
      return text ? `${'  '.repeat(Math.max(0, depth - 1))}- ${text}\n` : ''
    }
    if (tag === 'p') {
      const text = escape([...node.childNodes].map(child => walk(child, depth)).join(''))
      return text ? `\n\n${text}\n\n` : ''
    }
    if (tag === 'table') return '\n\n' + node.innerText.trim() + '\n\n'
    if (['div', 'section', 'article', 'main', 'body', 'ul', 'ol'].includes(tag)) {
      return [...node.childNodes].map(child => walk(child, depth)).join('')
    }
    return [...node.childNodes].map(child => walk(child, depth)).join('')
  }

  const markdown = escape(walk(content)).replace(/\n{3,}/g, '\n\n')
  return {
    title,
    markdown,
    html: content?.outerHTML || document.body.outerHTML,
    url: location.href
  }
}
"""


def write_link_index(out_dir: Path, links: list[dict[str, str]]) -> None:
    (out_dir / "links.json").write_text(
        json.dumps(links, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    lines = [f"- [{item['title']}]({item['url']})" for item in links]
    (out_dir / "links.md").write_text("# 语雀目录链接\n\n" + "\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Scrape Yuque docs with a real browser session.")
    parser.add_argument("url", help="Yuque doc/book URL, e.g. https://www.yuque.com/xiumubai/doc")
    parser.add_argument("--out", default="yuque-docs", help="Output directory")
    parser.add_argument("--max-pages", type=int, default=80, help="Max pages to save after collecting links")
    parser.add_argument("--collect-only", action="store_true", help="Only collect virtual-list links, do not save pages")
    parser.add_argument("--user-data-dir", default=".yuque-browser-profile", help="Browser profile dir for cookies")
    parser.add_argument("--headless", action="store_true", help="Run browser headless after login profile is ready")
    parser.add_argument("--max-scroll-rounds", type=int, default=900, help="Max virtual-list scroll rounds while collecting links")
    parser.add_argument("--idle-rounds", type=int, default=8, help="Stop after this many scroll rounds without new links")
    parser.add_argument("--scroll-delay", type=int, default=160, help="Delay after each virtual-list scroll in ms")
    args = parser.parse_args()

    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("Missing dependency: playwright", file=sys.stderr)
        print("Install with: python3 -m pip install playwright", file=sys.stderr)
        print("If Chromium is missing, run: python3 -m playwright install chromium", file=sys.stderr)
        return 2

    start_url = normalize_url(args.url, args.url)
    out_dir = Path(args.out).resolve()
    html_dir = out_dir / "html"
    md_dir = out_dir / "markdown"
    out_dir.mkdir(parents=True, exist_ok=True)
    html_dir.mkdir(parents=True, exist_ok=True)
    md_dir.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as p:
        context = p.chromium.launch_persistent_context(
            user_data_dir=args.user_data_dir,
            headless=args.headless,
            channel="chrome",
            viewport={"width": 1440, "height": 1000},
        )
        page = context.new_page()
        page.goto(start_url, wait_until="domcontentloaded", timeout=60000)

        if not args.headless:
            input("Browser opened. Log in / open the doc list if needed, then press Enter to collect links...")
            page.wait_for_load_state("domcontentloaded", timeout=60000)
            page.wait_for_timeout(1000)
            start_url = normalize_url(page.url, page.url)

        result = page.evaluate(
            COLLECT_LINKS_SCRIPT,
            {
                "maxRounds": args.max_scroll_rounds,
                "idleRounds": args.idle_rounds,
                "scrollDelay": args.scroll_delay,
            },
        )
        raw_links = result.get("items", [])
        links: list[dict[str, str]] = []
        seen: set[str] = set()
        for item in raw_links:
            clean = normalize_url(item.get("url") or "", start_url)
            if clean in seen or not same_yuque_book(clean, start_url):
                continue
            seen.add(clean)
            links.append({"title": item.get("title") or clean, "url": clean})

        write_link_index(out_dir, links)
        print(
            f"Collected {len(links)} links "
            f"(scrollTop={result.get('scrollTop')}, scrollHeight={result.get('scrollHeight')})."
        )

        if args.collect_only:
            context.close()
            print(f"Saved links to {out_dir / 'links.json'}")
            return 0

        saved: list[tuple[str, str]] = []
        for item in links[: args.max_pages]:
            url = item["url"]
            print(f"[{len(saved) + 1}] {url}")
            page.goto(url, wait_until="domcontentloaded", timeout=60000)
            page.wait_for_timeout(1200)
            page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            page.wait_for_timeout(600)
            page.evaluate("window.scrollTo(0, 0)")

            data = page.evaluate(EXTRACT_PAGE_SCRIPT)
            title = data.get("title") or item["title"] or "untitled"
            real_url = normalize_url(data.get("url") or url, start_url)
            prefix = f"{len(saved) + 1:03d}-{slugify(title, f'page-{len(saved) + 1:03d}')}"

            (md_dir / f"{prefix}.md").write_text(
                f"# {title}\n\n> 来源：{real_url}\n\n{data.get('markdown') or ''}\n",
                encoding="utf-8",
            )
            (html_dir / f"{prefix}.html").write_text(data.get("html") or "", encoding="utf-8")
            saved.append((title, real_url))
            time.sleep(0.25)

        index = "\n".join(f"- [{title}]({url})" for title, url in saved)
        (out_dir / "index.md").write_text(f"# Yuque 抓取索引\n\n{index}\n", encoding="utf-8")
        context.close()

    print(f"Saved {len(saved)} pages to {out_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
