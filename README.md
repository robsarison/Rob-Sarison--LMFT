# Rob’s website

The homepage headline is “Meaningful change. Stronger connections.” Video timestamps will be supplied by Rob later.

Your first version has 15 working pages, including the full psychotherapy section, aging and caregiving, drama therapy, training, fees, contact, and client portal.

## Preview

Your private preview runs at http://127.0.0.1:4173/ on this Mac. GitHub source is stored in the public repository you selected. GitHub Pages deployment is prepared but intentionally not activated, honoring your request for a private preview. Noindex is not access control.

For a local preview, tell Codex: “Open the local preview of my Rob Sarison website.” Codex can rebuild and serve `dist` on port 4173. Rebuilds default to local preview paths, so interior-page styles stay intact. Opening an HTML file directly is not recommended because links start at the site root.

## Ask for edits in ordinary language

Examples:

- “Make the homepage opening a little warmer, keeping the practical focus.”
- “Replace the Bay photograph with this portrait. I have permission to use it.”
- “Set my individual fee to $___ and my couples fee to $___.”
- “Add this video to About Rob, starting at 1 minute 20 seconds.”

You do not need to edit code. Codex should update the source, rebuild, check the affected pages, and refresh the private website.

## Add SimplePractice

Give Codex the three actual public links from your SimplePractice account: appointment request, secure inquiry (if your account supports it), and client portal. Never provide your password or a clinical record.

Codex will place the links into `config.json`, under `simplePractice`, and rebuild. The three contact options automatically become working links. There is no form or clinical database on this website. Inquiry functionality depends on the feature actually available in your account; no endpoint has been invented.

## Information still needed for public launch

Your approved portrait and image permissions; verified license details; final fees and session lengths; actual contact/booking links; office arrangements if applicable; cancellation and clinical privacy policies; your review of the copy. The video still needs an audiovisual/caption review and excerpt selection. Source verification notes distinguish your statements from independently supported facts.

## Where things live

- `config.json`: editable practice settings; `null` means deliberately unspecified, not a real contact detail.
- `content.py`: interior-page copy.
- `build.py`: shared page templates, homepage and static generation.
- `style.css`: colors, typography, layout and responsive behavior.
- `app.js`: mobile navigation and click-to-load video.
- `IMAGE-ASSET-INVENTORY.md`: image sources, permissions and recommendations.
- `SOURCES-AND-CLAIMS.md`: claim review and unresolved items.
- `QA.md`: checks and limits.
- `dist`: complete deployable website output. Edit source first; rebuild regenerates this folder.

## GitHub Pages deployment

The requested eventual host is GitHub Pages. The repository is public; the site is not yet published. Enable Pages with GitHub Actions and run the deployment workflow only after authorizing public launch. When ready, ask Codex to connect your final domain, set `origin` to its HTTPS address, connect booking, and enable `publicLaunch`. That setting removes the preview strip and changes robots metadata to permit indexing. A sitemap, canonical URLs, Open Graph metadata and Person structured data are generated for every page. A custom domain can be connected later.

The local `export-github.py` helper prepares a flat copy in `github-source` for browser upload. Only the approved source files are included; the Sites registration and credentials are excluded.

No server-side application, database, paid framework, tracking service, or dependency updates are needed. The site uses static HTML/CSS with a small Python-standard-library build script and minimal JavaScript. Any static host can serve `dist`, and this project uses GitHub Pages.

## Technical commands (for Codex)

Run `python3 build.py`, then `python3 check.py`. For root-path local preview run `SITE_BASE_PATH="" python3 build.py`. Preview with `python3 -m http.server 4173 --bind 127.0.0.1 --directory dist`. On this Mac, the bundled Python path is `/Users/robertsarison/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3` because the system Python requires unavailable developer tools.

No secrets belong in `config.json`; settings there are public website information. New external links must be valid HTTPS URLs. Never store authentication tokens in the repository.

## Testimonials

The homepage supports genuine, approved testimonials. At Rob’s request, clearly labeled fictional examples are displayed only while `publicLaunch` is false. Entries with `sample: true` are excluded from a public-launch build, even if permission is later set. Replace them with genuine quotes and remove the sample flag before publishing. Give Codex the exact quote, approved attribution and relationship context. Each entry in `config.json` needs `quote`, `attribution`, `context`, and `permissionToPublish: true`. Do not repurpose senior-living testimonials as therapy-client endorsements. Quotes are escaped as plain text; entries without confirmed permission stay hidden.

## Public website

The public address is https://robsarison.github.io/Rob-Sarison--LMFT/. The full dementia-care presentation is on Aging, Memory Loss & Family Caregiving. Fictional samples are excluded from public builds. Booking and inquiries remain unavailable until real SimplePractice links are supplied.

To publish updates, save changes to the GitHub repository, open Actions, select “Deploy website to GitHub Pages”, and choose Run workflow on main. Codex can handle this for you. The one-time Pages setting is Settings → Pages → Source: GitHub Actions.
