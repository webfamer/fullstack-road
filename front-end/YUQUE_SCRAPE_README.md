# 语雀文章抓取脚本

脚本位置：

```text
/Users/xsz/project/front-ai/interview/front-end/scrape_yuque.py
```

## 安装依赖

```bash
python3 -m pip install playwright
python3 -m playwright install chromium
```

如果你本机已经有 Chrome，脚本会优先通过 Playwright 调用 Chrome。

## 抓取

先只测试目录虚拟列表链接收集：

```bash
cd /Users/xsz/project/front-ai/interview/front-end
python3 scrape_yuque.py "https://www.yuque.com/xiumubai/doc" --out yuque-docs-test --collect-only
```

输出：

```text
yuque-docs-test/
  links.json
  links.md
```

确认 `Collected xxx links` 数量符合预期后，再抓页面内容：

```bash
cd /Users/xsz/project/front-ai/interview/front-end
python3 scrape_yuque.py "https://www.yuque.com/xiumubai/doc" --out yuque-docs
```

流程：

1. 脚本会打开浏览器。
2. 如果需要登录，在浏览器里登录语雀。
3. 确认能看到文档后，回到终端按 Enter。
4. 脚本会滚动语雀虚拟目录列表，收集 `DocListItem-module_itemContent_*` 对应的文档链接。
5. 脚本按收集到的链接逐页保存 HTML 和 Markdown。

输出：

```text
yuque-docs/
  links.json
  links.md
  index.md
  markdown/
  html/
```

## 常用参数

```bash
python3 scrape_yuque.py "https://www.yuque.com/xiumubai/doc" --out yuque-docs --max-pages 120
```

限制抓取页数：

```bash
python3 scrape_yuque.py "https://www.yuque.com/xiumubai/doc" --out yuque-docs --max-pages 120
```

调整虚拟列表滚动收集参数：

```bash
python3 scrape_yuque.py "https://www.yuque.com/xiumubai/doc" --out yuque-docs-test --collect-only --max-scroll-rounds 1200 --idle-rounds 12
```

说明：

- 语雀目录是虚拟/懒加载列表，DOM 中通常只保留可见的几条。
- 脚本会不断滚动目录容器，累计 `a[class*="DocListItem-module_itemContent_"][href]` 链接并去重。
- `--collect-only` 只收集链接，不抓正文，适合先测试链接数量。

如果登录态已经保存在 `.yuque-browser-profile`，可以无头运行：

```bash
python3 scrape_yuque.py "https://www.yuque.com/xiumubai/doc" --out yuque-docs --headless
```

## 注意

- 只抓你有权限访问的内容。
- 不建议高频反复抓，避免触发站点风控。
- 抓完后我可以读取 `yuque-docs/markdown`，帮你整理成“前端面试快速回顾版”。
