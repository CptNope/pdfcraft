# PdfCraft — GitHub Pages PWA

This fork builds the original PdfCraft Rust web app and publishes an installable Progressive Web App via GitHub Actions.

## Setup
1. Repository **Settings → Pages → Build and deployment → Source: GitHub Actions**.
2. Under **Actions**, run **Deploy PdfCraft PWA** manually if the initial deployment has not started.
3. Visit https://cptnope.github.io/pdfcraft/ from Chrome, Samsung Internet, Edge, or Safari. Use **Install PdfCraft** or the browser menu; Safari on iOS uses **Share → Add to Home Screen**.

Changes to `main` trigger the deployment. Original upstream CI, packaging and release workflows are manual-only to avoid unnecessary runs.

This fork preserves the original project license and attribution files. The PWA icon is generic and distinct from ArtCraft branding.

The browser app supports URL imports using `?file=`, subject to CORS. It can also export/download PDFs. Test mobile controls before depending on this as a production PDF editor; the upstream interface is desktop oriented.

The service worker caches compiled app files for use offline, but **does not cache PDFs passed via URL**. Keep local copies of important documents; avoid relying on browser storage as your only backup.
