# Autochrome concept

Private speculative website concept preview for Autochrome (mobile alloy wheel refurbishment, Plymouth). Unofficial: created independently by JA Digital, not commissioned or endorsed by Autochrome. The site is static files only, served by a Cloudflare Worker. There is no Worker script.

The published address is a `workers.dev` URL. Keep that URL behind [Cloudflare Access](https://developers.cloudflare.com/workers/configuration/cloudflare-access/). Access is turned on for the Worker in the Cloudflare dashboard. It is not configured in this repository. `workers.dev` and preview URLs are reachable on the internet until Access is enabled, so enable it before sharing the address.

Pages are marked `noindex, nofollow` in HTML, `public/_headers` sends `X-Robots-Tag: noindex, nofollow, noarchive`, and `public/robots.txt` disallows all crawlers. `public/sitemap.xml` is for future use only and must not be submitted while this is a concept.

Do not attach any Autochrome domain. `wrangler.jsonc` has no routes and no custom domains, and none should be added. The only host for this preview is `workers.dev`.

## Site files

Everything served lives in `public/`: `index.html`, `credits.html`, `404.html`, `styles.css`, `app.js`, self-hosted fonts in `fonts/`, images in `img/`, plus `robots.txt`, `_headers` and `sitemap.xml`. No frameworks, analytics or third-party requests.

The quote form is a demonstration only: no `action`, submit is prevented, no fetch/XHR/storage, selected photos are previewed locally with object URLs and never uploaded.

## Photos and before/after sliders

All photos and the logo come from the public Autochrome Alloys UK Facebook page (originals kept outside the repo in `/workspace/autochrome-fb/`). They are for this private concept only and need the owner's permission before any launch.

Each slider uses two halves cropped from one of Autochrome's own combined before/after images, split at the exact white gutter with borders trimmed, so both halves share one framing and aspect ratio:

- Hero: `bmw-m-spoke-before/after-{480,720,987}.webp` (987x1645, 3:5), from the BMW M-spoke post.
- Gallery: `citroen-before/after-{480,720,987}.webp` (3:5), and `nissan-before/after-268.webp` (268x447, low-res source, so shown smaller).
- "More recent work": `recent-*.webp`, single finished shots.
- Logo: `logo-{96,192,480}.webp`, the supplied logo resized only, shown in a rounded square frame. `favicon.png` is the same logo at 64px.

To add a pair: crop both halves to the same size from the same job, export WebP at responsive widths, then copy a `figure.card` in `index.html`, set `aspect-ratio` and `width`/`height` to the crop size, and update `srcset`, `alt`, the slider `aria-label` and the caption. Skip pairs that are misaligned or too low-res (the BMW silver-to-black pair in the "custom colours" graphic was skipped for that reason).

See `PROVISIONAL.md` for content still waiting on owner confirmation.

## Deploy

When this repository is connected to [Workers Builds](https://developers.cloudflare.com/workers/ci-cd/builds/), merging to `main` deploys to the `workers.dev` preview. The production-branch deploy command is `npx wrangler deploy` (the `deploy` script). `workers_dev` and `preview_urls` are both enabled. Preview URLs should stay behind the same Access policy.

Local commands, from a machine that is already logged in to the right Cloudflare account:

```sh
npm install
npm run dev
```

`npm run deploy` publishes the Worker. Do not deploy from a workstation unless that publish is intended. This repository contains no account id and no secrets.
