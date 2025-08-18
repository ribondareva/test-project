(function () {
  function bindConfirm(selector, message) {
    document.addEventListener('click', function (e) {
      const btn = e.target.closest(selector);
      if (!btn) return;
      if (!confirm(message)) {
        e.preventDefault();
        e.stopPropagation();
      }
    });
  }

  function onReady(fn) {
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', fn);
    } else {
      fn();
    }
  }

  onReady(function () {
    bindConfirm('.btn-spareparttype-delete', 'Удалить этот тип запчасти?');
    bindConfirm('.btn-sparepart-delete', 'Удалить эту запчасть?');
    bindConfirm('.btn-sparepart-photo-delete', 'Удалить фото?');
    bindConfirm('.btn-attribute-delete', 'Удалить атрибут?');
  });
})();
