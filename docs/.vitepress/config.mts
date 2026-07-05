import { defineConfig } from 'vitepress'

const repoName = process.env.GITHUB_REPOSITORY?.split('/')[1]
const isUserOrOrgPage = repoName?.endsWith('.github.io')
const githubPagesBase =
  process.env.GITHUB_ACTIONS && repoName && !isUserOrOrgPage ? `/${repoName}/` : '/'

export default defineConfig({
  title: 'Python 全栈后端入门',
  description: '写给前端工程师的 FastAPI + MySQL 实战教程',
  lang: 'zh-CN',
  base: process.env.VITEPRESS_BASE ?? githubPagesBase,
  cleanUrls: true,
  lastUpdated: true,
  ignoreDeadLinks: true,
  themeConfig: {
    logo: '/logo.svg',
    siteTitle: 'Python 全栈后端入门',
    nav: [
      { text: '学习路线', link: '/guide/learning-path' },
      { text: 'MySQL', link: '/guide/mysql-table-design' },
      { text: 'FastAPI', link: '/guide/fastapi-basics' },
      { text: '练习', link: '/guide/exercises' }
    ],
    sidebar: [
      {
        text: '开始之前',
        items: [
          { text: '这套教程怎么学', link: '/guide/learning-path' },
          { text: '后端思维补齐', link: '/guide/backend-thinking' }
        ]
      },
      {
        text: 'MySQL 与建模',
        items: [
          { text: '表结构设计', link: '/guide/mysql-table-design' },
          { text: 'SQL 基础与查询', link: '/guide/sql-basics' }
        ]
      },
      {
        text: 'FastAPI 开发',
        items: [
          { text: 'FastAPI 基础', link: '/guide/fastapi-basics' },
          { text: 'FastAPI + MySQL 项目结构', link: '/guide/fastapi-mysql-project' }
        ]
      },
      {
        text: '真实后端问题',
        items: [
          { text: '并发、事务与一致性', link: '/guide/concurrency-transaction' },
          { text: '综合练习', link: '/guide/exercises' }
        ]
      }
    ],
    socialLinks: [
      { icon: 'github', link: 'https://github.com/' }
    ],
    search: {
      provider: 'local'
    },
    outline: {
      level: [2, 3],
      label: '本页目录'
    },
    docFooter: {
      prev: '上一章',
      next: '下一章'
    },
    lastUpdated: {
      text: '最后更新'
    }
  }
})
