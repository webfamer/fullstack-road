# Python 全栈后端入门：FastAPI + MySQL

这是一个写给前端工程师的 Python 后端教程站，重点补齐 FastAPI、MySQL 建模、SQL、事务与并发一致性。

## 本地预览

```bash
npm install
npm run docs:dev
```

## 构建

```bash
npm run docs:build
npm run docs:preview
```

## 发布到 GitHub Pages

1. 把本目录提交到 GitHub 仓库。
2. 在仓库 Settings → Pages 中，把 Source 设置为 GitHub Actions。
3. 推送到 `main` 分支后，`.github/workflows/deploy.yml` 会自动构建并发布。

站点配置会在 GitHub Actions 中自动识别仓库名：

- 如果仓库是普通项目仓库，发布路径会自动使用 `/仓库名/`。
- 如果仓库是 `用户名.github.io`，发布路径会自动使用 `/`。
- 本地开发默认使用 `/`。

如需手动覆盖，可以在构建时设置环境变量：

```bash
VITEPRESS_BASE=/your-base/ npm run docs:build
```
