/* Progressive enhancements only; page text and the status remain static HTML. */
(() => {
  const decorateChapters = () => {
    document.querySelectorAll('.chapter a').forEach(link => {
      const text = link.firstChild;
      if (!text || text.nodeType !== Node.TEXT_NODE) return;
      const match = text.textContent.match(/^(\d+\s*·\s*)/);
      if (!match) return;
      const number = document.createElement('span');
      number.className = 'chapter-number';
      number.textContent = match[0];
      text.textContent = text.textContent.slice(match[0].length);
      link.prepend(number);
    });
  };
  decorateChapters();
  const sidebar = document.querySelector('.sidebar-scrollbox');
  if (sidebar) new MutationObserver(decorateChapters).observe(sidebar, { childList: true, subtree: true });

  document.querySelectorAll('main figure').forEach(figure => {
    const image = figure.querySelector('img, svg');
    if (!image) return;
    if (figure.classList.contains('protocol-diagram')) {
      const viewport = document.createElement('div');
      viewport.className = 'diagram-viewport';
      viewport.tabIndex = 0;
      viewport.setAttribute('role', 'region');
      viewport.setAttribute('aria-label', 'Diagram — scroll horizontally to explore');
      image.before(viewport);
      viewport.append(image);
      figure.removeAttribute('tabindex');
    }
    // Use the existing description verbatim, never invent editorial content.
    const description = image.getAttribute('alt') || figure.getAttribute('aria-label');
    if (description && !figure.querySelector('figcaption')) {
      const caption = document.createElement('figcaption');
      caption.textContent = description;
      figure.append(caption);
    }
  });
  document.querySelectorAll('.table-wrapper, pre').forEach(region => {
    region.tabIndex = 0;
    region.setAttribute('role', 'region');
    region.setAttribute('aria-label', region.matches('pre') ? 'Code example' : 'Table');
  });
})();
