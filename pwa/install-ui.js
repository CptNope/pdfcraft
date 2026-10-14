(() => {
  const standalone = matchMedia('(display-mode: standalone)').matches || navigator.standalone === true;
  if (standalone) return;
  const style = document.createElement('style');
  style.textContent = '#pc-install{position:fixed;right:8px;bottom:calc(env(safe-area-inset-bottom,0px) + 8px);z-index:1000;font:12px system-ui;background:#222735;color:#fff;border:1px solid #61758b;border-radius:9px;padding:9px 12px;box-shadow:0 2px 8px #0008}#pc-install-help{position:fixed;right:8px;bottom:calc(env(safe-area-inset-bottom,0px) + 54px);max-width:min(270px,85vw);z-index:1000;font:13px/1.45 system-ui;background:#222735;color:#fff;padding:12px;border:1px solid #61758b;border-radius:9px;box-shadow:0 4px 12px #0008}#pc-install-help[hidden]{display:none}';
  document.head.append(style);
  const btn = document.createElement('button');
  btn.type = 'button'; btn.id = 'pc-install'; btn.textContent = 'Install PdfCraft'; btn.setAttribute('aria-label','Install PdfCraft app');
  const help = document.createElement('div');
  help.id = 'pc-install-help'; help.hidden = true; help.setAttribute('role','status');
  help.textContent = /iPad|iPhone|iPod/.test(navigator.userAgent)
    ? 'In Safari, tap Share, then Add to Home Screen.'
    : 'Open the browser menu and choose Install app or Add to Home screen. The browser may not offer installation on every device.';
  document.body.append(btn,help);
  let installEvent = null;
  window.addEventListener('beforeinstallprompt', e => {e.preventDefault();installEvent=e;});
  btn.addEventListener('click', () => {
    if (installEvent) { const e=installEvent; installEvent=null; e.prompt(); }
    else help.hidden = !help.hidden;
  });
  window.addEventListener('appinstalled',()=>{btn.remove();help.remove();});
})();
