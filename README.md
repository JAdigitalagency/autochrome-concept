# Autochrome concept

Speculative website concept preview for Autochrome (mobile alloy wheel refurbishment, Plymouth). Unofficial: created independently by JA Digital, not commissioned or endorsed by Autochrome. The site is static files only, served by a Cloudflare Worker. There is no Worker script.

The published address is a public `workers.dev` URL with no Cloudflare Access login (JA Digital concept previews are public by policy). Privacy comes from noindex and robots rules, no analytics and no data collection, not from a login.

Pages are marked `noindex, nofollow` in HTML, `public/_headers` sends `X-Robots-Tag: noindex, nofollow, noarchive`, and `public/robots.txt` disallows all crawlers. `public/sitemap.xml` is for future use only and must not be submitted while this is a concept.

Do not attach any Autochrome domain. `wrangler.jsonc` has no routes and no custom domains, and none should be added. The only host for this preview is `workers.dev`.

## Site files

Everything served lives in `public/`: `index.html`, `credits.html`, `404.html`, `styles.css`, `app.js`, self-hosted fonts in `fonts/`, images in `img/`, plus `robots.txt`, `_headers` and `sitemap.xml`. No frameworks, analytics or third-party requests.

The quote form is a demonstration only: no `action`, submit is prevented, no fetch/XHR/storage, selected photos are previewed locally with object URLs and never uploaded.

## Photos and before/after sliders

All photos and the logo come from the public Autochrome Alloys UK Facebook page (originals kept outside the repo in `/workspace/autochrome-fb/`). They are for this concept preview only and need the owner's permission before any launch.

Each slider uses two halves cropped from one of Autochrome's own combined before/after images, split at the exact white gutter with borders trimmed, so both halves share one framing and aspect ratio:

All sliders are cropped to 4:5 (the `.compare` box sets `aspect-ratio:4/5`) so every card is the same size:

- Hero: `citroen-before/after-45-{480,720,987}.webp` (987x1234), Citroën silver to gloss black.
- Gallery: `bmw-m-spoke-*-45-{480,720,987}.webp`; `nissan-*-45-536.webp` (from a 268px-wide source, Lanczos 2x plus mild sharpening, no AI upscaling); `kerb-*-45-630.webp` (the large before/after pair in the "kerbed your alloy" graphic, starts at 65% so the damage shows).
- "More recent work": `recent-{gloss-black,bmw-wheel,bmw-estate}-{600,900}.webp`, 4:3 crops with collage borders and white strips removed; the BMW shots come from the 2048px original.
- Logo: `logo-{96,192,480}.webp`, the supplied logo resized only, shown in a rounded square frame. `favicon.png` is the same logo at 64px.

To add a pair: crop both halves to the same size from the same job, export WebP at responsive widths, then copy a `figure.card` in `index.html`, crop to 4:5, set `width`/`height` to the crop size, and update `srcset`, `alt`, the slider `aria-label` and the caption. Skip pairs that are misaligned or too low-res (the BMW silver-to-black pair in the "custom colours" graphic was skipped for that reason).

See `PROVISIONAL.md` for content still waiting on owner confirmation.

## Deploy

When this repository is connected to [Workers Builds](https://developers.cloudflare.com/workers/ci-cd/builds/), merging to `main` deploys to the `workers.dev` preview. The production-branch deploy command is `npx wrangler deploy` (the `deploy` script). `workers_dev` and `preview_urls` are both enabled. Preview URLs are public too and carry the same noindex headers.

Local commands, from a machine that is already logged in to the right Cloudflare account:

```sh
npm install
npm run dev
```

`npm run deploy` publishes the Worker. Do not deploy from a workstation unless that publish is intended. This repository contains no account id and no secrets.
