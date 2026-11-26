# Coding Studio v2 source

Source of the page served at `/code` (`web/coding/public/index.html`). The page talks to the unchanged Express API in `web/coding/server.js`.

```sh
npm install
npm run typecheck
npm run build   # writes ../coding/public/index.html (one self-contained file)
```

Commit the rebuilt `web/coding/public/index.html` together with source changes. Vercel serves that file; it does not build this folder.

Without the API (for example inside a claude.ai artifact) the page runs on placeholder demo posts that are not part of the study sample. Add `?demo` to the URL to force demo mode.
