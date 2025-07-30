function confirmDelete(id) {
      if (confirm(`Удалить атрибут с ID ${id}?`)) {
        alert(`Атрибут #${id} удалён`);
      }
    }