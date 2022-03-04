tippy('#button', {
  content(reference) {
    const id = reference.getAttribute('data-template');
    return document.getElementById(id);
  },
  trigger: 'click',
  allowHTML: true,
});