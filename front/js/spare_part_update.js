function confirmDeletePhoto(filename){
    return confirm(`Удалить фото ${filename}?`);
}
function confirmDelete(){
    if (confirm("Вы уверены, что хотите удалить эту запчасть?")) {
        window.location.href = "spare_part_delete.html";
   }
}