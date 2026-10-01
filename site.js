(() => {
  const yearEl = document.getElementById('year');
  if (yearEl) yearEl.textContent = new Date().getFullYear();

  // Naver Analytics events count contact-link clicks, not completed enquiries.
  // Keep the existing page-view call in each HTML page unchanged.
  document.addEventListener('click', (event) => {
    if (event.defaultPrevented || !(event.target instanceof Element)) return;
    const link = event.target.closest('a[href]');
    if (!link) return;
    const href = link.getAttribute('href') || '';
    let channel;
    if (/^tel:010-?8168-?0205$/i.test(href)) channel = 'Phone';
    else if (/^sms:010-?8168-?0205$/i.test(href)) channel = 'Sms';
    else if (href === 'https://open.kakao.com/o/sXKkFpRh') channel = 'Kakao';
    else return;

    let placement = 'Page';
    if (link.closest('.mobile-contact')) placement = 'Mobile';
    else if (link.closest('.hero')) placement = 'Hero';
    else if (link.closest('.contact-card')) placement = 'Main';
    else if (link.closest('.detail-summary')) placement = 'CaseSummary';
    else if (link.closest('.story-contact')) placement = 'CaseBody';

    // Analytics must never delay or interrupt the telephone/chat navigation.
    try {
      if (window.wcs && typeof window.wcs.event === 'function') {
        window.wcs.event('Contact', channel + placement);
      }
    } catch (_) {
      // Contact links still work when analytics is blocked or unavailable.
    }
  });
})();
