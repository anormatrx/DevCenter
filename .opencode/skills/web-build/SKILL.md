---
name: web-build
description: بناء ويب: npm, vite, webpack, env vars, deploy
---

# مهارة بناء الويب

سير عمل كامل لبناء مشاريع الويب.

---

## 1. إدارة الحزم

```bash
# npm
npm init -y
npm install react react-dom
npm install -D vite @vitejs/plugin-react
npm run dev

# yarn
yarn init -y
yarn add react react-dom
yarn dev

# pnpm (أسرع)
pnpm init
pnpm add react react-dom
pnpm dev
```

---

## 2. ملفات الإعدادات

### package.json:
```json
{
  "name": "myapp",
  "version": "1.0.0",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview",
    "lint": "eslint src/",
    "test": "vitest run",
    "deploy": "gh-pages -d dist"
  }
}
```

### vite.config.js:
```js
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  build: {
    outDir: 'dist',
    sourcemap: true,
    minify: 'terser',
  },
  server: {
    port: 3000,
    proxy: {
      '/api': 'http://localhost:5000'
    }
  }
})
```

---

## 3. متغيرات البيئة

### .env:
```env
VITE_API_URL=http://localhost:5000
VITE_APP_TITLE=MyApp
```

### .env.production:
```env
VITE_API_URL=https://api.myapp.com
```

### الاستخدام في الكود:
```js
const apiUrl = import.meta.env.VITE_API_URL
console.log(import.meta.env.MODE)  // development | production
```

---

## 4. أوامر البناء

```bash
npm run dev          # تطوير (hot reload)
npm run build        # بناء للإنتاج
npm run preview      # معاينة الإنتاج محلياً
npm run lint         # فحص الكود
npm test             # اختبارات
npm run deploy       # نشر (إذا مكون)
```

### تحسينات البناء:
```bash
# تحليل الحجم
npm install -D vite-bundle-analyzer

# بناء مع تحليل
NODE_ENV=production npm run build

# تصغير متقدم
# أضف terser في vite.config.js
```

---

## 5. الفحص (Linting)

### ESLint + Prettier:
```bash
npm install -D eslint prettier eslint-plugin-react
```

### .eslintrc.js:
```js
module.exports = {
  env: { browser: true, es2021: true },
  extends: ['eslint:recommended', 'plugin:react/recommended'],
  rules: {
    'react/react-in-jsx-scope': 'off',
    'no-unused-vars': 'warn',
  },
}
```

---

## 6. CI/CD للويب

### .github/workflows/web.yml:
```yaml
name: Web CI/CD
on: [push]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
      - run: npm ci
      - run: npm run lint
      - run: npm test
      - run: npm run build
      - if: github.ref == 'refs/heads/main'
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./dist
```

---

## 7. النشر (Deploy)

### GitHub Pages:
```bash
npm install -D gh-pages
# أضف: "deploy": "gh-pages -d dist"
npm run deploy
```

### Vercel:
```bash
npm i -g vercel
vercel --prod
```

### Netlify:
```bash
npm i -g netlify-cli
netlify deploy --prod --dir=dist
```
