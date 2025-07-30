function confirmDelete(id) {
      if (confirm(`Удалить запчасть с ID ${id}?`)) {
        alert(`Запчасть #${id} удалена`);
      }
    }