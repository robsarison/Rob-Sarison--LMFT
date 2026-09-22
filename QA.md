# First-version verification

- All 15 routes checked in the browser at 320 × 740, 390 × 844 and 1440 × 1000: shared stylesheet applied and no horizontal overflow.
- Home, About, Aging and Contact visually inspected. Interior pages share a responsive two-column editorial layout that becomes a single reading column on mobile.
- Mobile Menu opens, exposes navigation, and navigates to About. Escape closes the menu and restores focus, verified in the browser.
- FAQ disclosure opens and displays insurance information.
- All generated local links and fragment destinations, image alt attributes, one H1 per page, title/description metadata and secure booking URL format passed `check.py`.
- No fake booking actions: unavailable consultation/inquiry/portal options are explicitly labeled.
- Video activation creates the correct privacy-enhanced iframe with start=0 and autoplay=0, verified in the browser; original YouTube destination provided. Full playback, caption quality and timestamp selection remain unverified; Rob will provide timestamps later.
- Responsive WebP image variants are local; no font CDN, trackers, analytics, or clinical forms.
- Keyboard focus, semantic regions, skip link, native FAQ disclosure, reduced-motion styling included. This is not a formal WCAG certification or a measured Core Web Vitals report.
- Launch still requires real practice contact links, final fee/policy details and current credential verification. A portrait can replace the atmospheric image once supplied with permission.
- GitHub publication must explicitly preserve the latest request for a private preview. The local preview is bound to 127.0.0.1; no public GitHub Pages deployment should be started until Rob authorizes public launch. Repository source is public as requested.
