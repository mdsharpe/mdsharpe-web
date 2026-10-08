Source of https://www.mdsharpe.com/

Built with [Eleventy](https://www.11ty.dev/) from `src/` into `_site/`.

```sh
npm install
npm start      # dev server with live reload
npm run build  # output to _site/
```

Album data for `/music` lives in `src/_data/albums.json`.

Deployed to Cloudflare Workers as static assets (see `wrangler.jsonc`). Workers Builds runs `npm run build` then `npx wrangler deploy`.
