const checkboxes = document.querySelectorAll('.item_check');
// Посилання на головний чекбокс
const selectAllCheckbox = document.getElementById('flexCheckDefault');

const add_reg = document.getElementById('add_reg');
const del_reg = document.getElementById('del_reg');
const changeStatus = document.getElementById('changeStatusSee');
 
// Додаємо обробник подій для головного чекбоксу
selectAllCheckbox.addEventListener('change', function() {
    checkboxes.forEach(checkbox => {
        // Встановлюємо стан усім чекбоксам згідно зі станом головного чекбокса
        checkbox.checked = selectAllCheckbox.checked;
    });
});

// Додаємо обробник подій для кожного з індивідуальних чекбоксів
checkboxes.forEach(checkbox => {
    checkbox.addEventListener('change', function() {
        // Перевіряємо, чи всі чекбокси вибрані
        const allChecked = [...checkboxes].every(cb => cb.checked);
        selectAllCheckbox.checked = allChecked;
        // add_reg.style.display = allChecked ? 'block' : 'none';
        // del_reg.style.display = allChecked ? 'block' : 'none';
        // changeStatus.style.display = allChecked ? 'block' : 'none';
        // перевіряємо чи якісь чекбокси обрані
        const anyChecked = [...checkboxes].some(cb => cb.checked);
        add_reg.style.display = anyChecked ? 'block' : 'none';
        del_reg.style.display = anyChecked ? 'block' : 'none';
        changeStatus.style.display = anyChecked ? 'block' : 'none';


    });
});
  
// checkboxes.forEach(checkbox => {
//     checkbox.addEventListener('change', function() {
//         // Перевіряємо, чи обрано хоча б один чекбокс
        
//     });
// });