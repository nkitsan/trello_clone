(function () {
  const content = document.querySelector('.content');

  const addCardBtnClass = 'add-card-btn';
  const addListBtnClass = 'add-list-btn';
  const closeFormBtn = 'close-form';
  const showForm = 'show-form';

  content.addEventListener('click', (e) => {
    const targetEl = e.target;

    if (
      targetEl.classList.contains(addCardBtnClass) ||
      targetEl.classList.contains(addListBtnClass)
    ) {
      e.preventDefault();

      const actionsEl = targetEl.parentNode;
      actionsEl.classList.add(showForm);
    } else if (targetEl.classList.contains(closeFormBtn)) {
      e.preventDefault();

      const actionsEl = targetEl.parentNode.parentNode.parentNode;
      actionsEl.classList.remove(showForm);
    }
  });
})();