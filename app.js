const toggle = document.querySelector('.menu-toggle');
const nav = document.querySelector('.navlinks');
const services = document.querySelector('.services-nav');
function closeNavigation(restoreFocus = false) {
  toggle?.setAttribute('aria-expanded', 'false');
  nav?.classList.remove('open');
  if (services) services.open = false;
  if (restoreFocus) toggle?.focus();
}
toggle?.addEventListener('click', () => {
  const open = toggle.getAttribute('aria-expanded') !== 'true';
  if (!open) return closeNavigation(true);
  toggle.setAttribute('aria-expanded', 'true');
  nav.classList.add('open');
});
nav?.addEventListener('click', event => {
  if (event.target.closest('a')) closeNavigation();
});
document.addEventListener('keydown', event => {
  if (event.key !== 'Escape') return;
  if (toggle?.getAttribute('aria-expanded') === 'true') closeNavigation(true);
  else if (services?.open) {
    services.open = false;
    services.querySelector('summary').focus();
  }
});
document.addEventListener('click', event => {
  if (services?.open && !services.contains(event.target)) services.open = false;
});
document.querySelectorAll('[data-video]').forEach(button => button.addEventListener('click', () => {
  const frame = document.createElement('iframe');
  frame.src = `https://www.youtube-nocookie.com/embed/${button.dataset.video}?start=${Number(button.dataset.start) || 0}&autoplay=0&rel=0`;
  frame.title = button.dataset.title || 'Rob Sarison — original YouTube video';
  frame.allow = 'encrypted-media; picture-in-picture; fullscreen';
  frame.allowFullscreen = true;
  frame.referrerPolicy = 'strict-origin-when-cross-origin';
  frame.tabIndex = 0;
  button.parentElement.replaceChildren(frame);
  frame.focus();
}));
