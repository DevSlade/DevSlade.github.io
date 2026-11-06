# Capybara Cartel — studio website

Plain HTML and CSS: no build step, no framework, nothing to install. It runs on any static host.
GitHub Pages is free, and it's what Holler Pop's release plan uses.

| Path | What it is |
|---|---|
| `index.html` | Home page: hero, games (Holler Pop and Whiskeyville), about, contact |
| `holler-pop/privacy.html` | Holler Pop privacy policy. **This is the URL for Play Console** |
| `app-ads.txt` | AdMob verification. It has to sit at the site root |
| `brand/` | Press kit page plus every logo variant (see below) |
| `assets/` | CSS and the small images the site uses |
| `tools/make_logos.py` | Rebuilds every logo variant from `brand/source/` |
| `404.html` | "Lost in the holler" page |

## Before it goes live: fill these in

1. **`SUPPORT_EMAIL`**: in `index.html` (contact button) and `holler-pop/privacy.html` (contact section).
   Use a studio address, not a personal one: it will be public.
2. **`app-ads.txt`**: once the AdMob account exists, paste your real line and remove the `# `.
3. **Site address**: `index.html` assumes `https://devslade.github.io/` in its sharing tags (`og:url`,
   `og:image`). Change both if you use another address or a domain.

## Put it online (GitHub Pages, about 10 minutes)

1. On GitHub, create a **public** repo named exactly `DevSlade.github.io`.
2. Push this folder to it:
   ```
   git init -b main
   git add -A
   git commit -m "Capybara Cartel site"
   git remote add origin https://github.com/DevSlade/DevSlade.github.io.git
   git push -u origin main
   ```
3. On the repo, go to Settings → Pages → Deploy from branch → `main` / root.
4. After a minute:
   - Site: `https://devslade.github.io/`
   - Privacy policy for Play Console: `https://devslade.github.io/holler-pop/privacy.html`
   - AdMob reads: `https://devslade.github.io/app-ads.txt`
5. In Play Console, set **Website** to `https://devslade.github.io`, with no path, or AdMob won't find `app-ads.txt`.

## Logo variants (`brand/`)

Every piece comes in six treatments: `-rust` (original), `-cream` (light badge), `-cream-transparent`,
`-ink-transparent`, `-black-transparent`, `-white-transparent`.

- `lockup/`: capybara and name together (the full logo), plus a square version on rust
- `mark/`: the capybara alone, plus a square version on rust
- `wordmark/`: the name plate alone
- `social/`: 800×800 avatar (circle-safe), 1500×500 banner, 1200×630 link-preview card
- `icons/`: 512/192/180/48/32/16 PNGs, a maskable 512 for Android, and `favicon.ico`

To rebuild after changing the source image: `python tools/make_logos.py` (needs Pillow and numpy).

**Limits of the current files:** they come from a 1024×1024 image, so the full logo is about 870 px wide.
That's fine for screens. Merch and large print need a vector redraw (SVG) or a higher-resolution source.
The favicon at 16 px is mostly a silhouette; a simplified mark would read better that small.

## Notes

- Fonts (Rye, Bitter, Source Serif 4) load from Google Fonts. To keep visitors' IPs away from Google,
  download the three families (all SIL OFL), put them in `assets/fonts/` and swap the `<link>` for
  `@font-face` rules. The privacy page already uses system fonts only.
- The site copy says Holler Pop is "Coming soon · Google Play". When it's live, swap that pill for the
  official Google Play badge linking to the store page.
