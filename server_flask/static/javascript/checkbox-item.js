const checkboxes = document.querySelectorAll('.item_check');
const add_reg = document.getElementById('add_reg');
const del_reg = document.getElementById('del_reg');
const changeStatus = document.getElementById('changeStatusSee');

checkboxes.forEach(checkbox => {
    checkbox.addEventListener('change', function() {
        // Перевіряємо, чи обрано хоча б один чекбокс
        const anyChecked = [...checkboxes].some(cb => cb.checked);
        add_reg.style.display = anyChecked ? 'block' : 'none';
        del_reg.style.display = anyChecked ? 'block' : 'none';
        changeStatus.style.display = anyChecked ? 'block' : 'none';
        
    });
});