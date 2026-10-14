const CACHE_NAME = "pdfcraft-pwa-__BUILD_VERSION__";
const ASSETS = __PRECACHE_ASSETS__;
self.addEventListener("install", event => {
  event.waitUntil(caches.open(CACHE_NAME).then(cache => cache.addAll(ASSETS)).then(() => self.skipWaiting()));
});
self.addEventListener("activate", event => {
  event.waitUntil(caches.keys().then(names => Promise.all(names.filter(n => n.startsWith("pdfcraft-pwa-") && n !== CACHE_NAME).map(n => caches.delete(n)))).then(() => self.clients.claim()));
});
self.addEventListener("fetch", event => {
  if (event.request.method !== "GET" || new URL(event.request.url).origin !== self.location.origin) return;
  const url = new URL(event.request.url);
  // Never cache user-requested PDF files or personalized URL query responses.
  if (url.searchParams.has("file") || /\.pdf$/i.test(url.pathname)) return;
  event.respondWith(caches.match(event.request, {ignoreSearch: url.pathname.endsWith("/") || url.pathname.endsWith("/index.html")}).then(cached => cached || fetch(event.request)));
});
