document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll('.btn-delete-vehicle').forEach(function (btn) {
        btn.addEventListener('click', function (event) {
            if (!confirm('Вы уверены, что хотите удалить технику?')) {
                event.preventDefault();
            }
        });
    });

    document.querySelectorAll('.btn-delete-type').forEach(function (btn) {
        btn.addEventListener('click', function (event) {
            if (!confirm('Удалить этот тип техники?')) {
                event.preventDefault();
            }
        });
    });

    document.querySelectorAll('.btn-delete-photo').forEach(function (btn) {
        btn.addEventListener('click', function (event) {
            if (!confirm('Удалить фото?')) {
                event.preventDefault();
            }
        });
    });
});
