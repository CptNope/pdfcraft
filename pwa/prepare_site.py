#!/usr/bin/env python3
"""Wrap the Rust/WASM PdfCraft output as an installable GitHub Pages PWA."""
from pathlib import Path
import os
import json
import shutil
import struct
import zlib
import sys

ROOT = Path(__file__).resolve().parents[1]

def icon(path, size):
    pixels = bytearray()
    for y in range(size):
        pixels.append(0)
        for x in range(size):
            u = (x + .5) / size
            v = (y + .5) / size
            r, g, b = (28, 36, 49)
            if .08 < u < .92 and .08 < v < .92:
                r, g, b = (46, 62, 83)
            if .28 < u < .72 and .17 < v < .83:
                r, g, b = (237, 242, 246)
            if .61 < u < .72 and .17 < v < .30:
                r, g, b = (167, 199, 214)
            if .36 < u < .64 and .42 < v < .46 or .36 < u < .64 and .54 < v < .58 or .36 < u < .55 and .66 < v < .70:
                r, g, b = (66, 115, 148)
            pixels.extend((r, g, b, 255))
    def chunk(tag, data):
        return struct.pack(">I", len(data)) + tag + data + struct.pack(">I", zlib.crc32(tag + data) & 0xffffffff)
    path.write_bytes(b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", size, size, 8, 6, 0, 0, 0)) + chunk(b"IDAT", zlib.compress(bytes(pixels), 9)) + chunk(b"IEND", b""))

def main(site):
    index = site / "index.html"
    if not index.exists():
        raise SystemExit("Built PdfCraft index.html missing")
    icons = site / "icons"
    icons.mkdir(parents=True, exist_ok=True)
    for name, size in (("icon-192.png", 192), ("icon-512.png", 512), ("apple-touch-icon.png", 180)):
        icon(icons / name, size)
    for name in ("LICENSE-MIT", "LICENSE-APACHE", "NOTICE", "ATTRIBUTION.md", "ATTRIBUTION.toml"):
        source = ROOT / name
        if source.exists():
            shutil.copy2(source, site / name)
    shutil.copy2(ROOT / "pwa" / "manifest.webmanifest", site / "manifest.webmanifest")
    shutil.copy2(ROOT / "pwa" / "install-ui.js", site / "install-ui.js")
    (site / ".nojekyll").touch()
    html = index.read_text(encoding="utf-8")
    if "</head>" not in html or "</body>" not in html:
        raise SystemExit("HTML missing </head> or </body>")
    html = html.replace("</head>", '<link rel="manifest" href="./manifest.webmanifest">\n<meta name="theme-color" content="#19191c">\n<link rel="apple-touch-icon" href="./icons/apple-touch-icon.png">\n</head>', 1)
    html = html.replace("</body>", """<script src="./install-ui.js" defer></script>
<script>
if ("serviceWorker" in navigator) {
  window.addEventListener("load", () => navigator.serviceWorker.register("./sw.js").catch(err => console.warn("PdfCraft PWA service worker:", err)));
}
</script>
</body>""", 1)
    index.write_text(html, encoding="utf-8")
    built = ["./" + p.name for p in site.iterdir() if p.is_file() and p.suffix.lower() in (".wasm", ".js", ".css")]
    if not any(x.endswith(".wasm") for x in built):
        raise SystemExit("No compiled .wasm found")
    precache = ["./", "./index.html", "./manifest.webmanifest", "./install-ui.js",
                "./icons/icon-192.png", "./icons/icon-512.png", "./icons/apple-touch-icon.png"]
    sw = (ROOT / "pwa" / "sw.js").read_text(encoding="utf-8")
    sw = sw.replace("__BUILD_VERSION__", (os.environ.get("GITHUB_SHA") or "local")[:12])
    sw = sw.replace("__PRECACHE_ASSETS__", json.dumps(sorted(set(precache + built))))
    (site / "sw.js").write_text(sw, encoding="utf-8")
    print("Prepared PdfCraft PWA with", len(built), "compiled assets")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("Usage: prepare_site.py dist/web")
    main(Path(sys.argv[1]).resolve())
