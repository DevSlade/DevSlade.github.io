# Capybara Cartel: studio website

Plain HTML, CSS and a little JavaScript. No build step, no framework, nothing to install.
It's served by GitHub Pages at **https://capybaracartel.com** (the `CNAME` file sets the domain).

| Path | What it is |
|---|---|
| `index.html` | Home: hero, games (Holler Pop and Whiskeyville), house rules, about, contact |
| `holler-pop/index.html` | The Holler Pop page, in the game's own look (`assets/css/holler-pop.css`) |
| `holler-pop/privacy.html` | Holler Pop privacy policy. **This URL is in Play Console. Don't move it.** |
| `holler-pop/terms.html` | Holler Pop terms of service |
| `support/index.html` | Support: email, bug-report checklist, FAQ |
| `about/index.html` | About the studio |
| `404.html` | "Lost in the holler" page (GitHub Pages serves it for missing pages) |
| `app-ads.txt` | AdMob verification. It has to sit at the site root |
| `robots.txt`, `sitemap.xml` | For search engines |
| `assets/css/site.css` | Studio styles, shared by every page |
| `assets/js/site.js` | Menu, copy button, screenshot carousel, scroll reveals, bottle parallax |
| `assets/fonts/` | Lilita One and Fredoka (the game's fonts, SIL OFL; licences alongside) |
| `assets/img/holler-pop/` | Game art, icons and screenshots, exported from the game project |

The logo files and the old press-kit page now live outside this repo, in
`MY PROGRAMS & Repositories/Capybara Cartel brand kit/`.

## Try it locally

```
python -m http.server 8810 --bind 127.0.0.1
```

Then open http://127.0.0.1:8810. Links are root-relative (`/support/`), so open it through a server,
not by double-clicking the file.

## When Holler Pop goes live on Google Play

Swap "coming soon" for the real thing. Use Google's official "Get it on Google Play" badge,
linking to the store page:

- `index.html`: the status pill in the game card, the "Tell me when it's out" button, the marquee band
- `holler-pop/index.html`: the `.soon` chip and the "Tell me when it's out" buttons in the hero and
  the closing section, the closing heading, and the "When does it come out?" FAQ
- `about/index.html`: the facts box and the first item under "What's coming"
- `assets/img/holler-pop/shots/`: re-export if the game's look changes

## Legal pages

- Change the "Effective" date at the top whenever you edit the privacy policy or terms.
- If the game starts collecting anything new (analytics, accounts, cloud saves, another ad network),
  the privacy policy and Play Console's Data safety form both have to change first.
- `app-ads.txt`: once the AdMob account exists, paste your real line and remove the `# `.

## Notes

- The studio fonts (Rye, Bitter, Source Serif 4) load from Google Fonts, and the privacy policy says so.
  To keep visitors' IPs away from Google, download the three families (all SIL OFL) into `assets/fonts/`
  and swap the `<link>` for `@font-face` rules, then update section 9 of the privacy policy.
- In Play Console, set **Website** to `https://capybaracartel.com`, with no path, or AdMob won't find
  `app-ads.txt`.
