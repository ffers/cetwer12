document.getElementById("changeStatus").addEventListener("change", function() {
    var selectedOption = this.value;
    
    var checkboxes = document.getElementsByName('selectedItems');
    var selectedOrders = [];
    // Проходимося по всіх чекбоксах і зберігаємо вибрані замовлення у масив
    for (var i = 0; i < checkboxes.length; i++) {
        if (checkboxes[i].checked) {
            selectedOrders.push(checkboxes[i].value);
            var selectedOption = this.value;
        }
    }
    
    var dataToSend = {
      status: selectedOption,
      id: selectedOrders
    };
  
    // Отриманий об'єкт dataToSend тепер можна використовувати для передачі на сервер або виконання інших дій
    console.log(dataToSend);
    changeStatusFunc(dataToSend)
  });


 function changeStatusFunc(data) {
    fetch('/cabinet/orders/changeStatus', {
        method: 'POST',
        credentials: "same-origin",
        redirect: "follow",
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    })
    .then(response => response.json())
    .then(data => {
        console.log('Дані успішно відправлено на сервер:', data);
        window.location.reload();
    })
    .catch((error) => {
        console.error('Сталася помилка:', error);
    });
} 

window.onload = function() {
    var select = document.getElementById("changeStatus");
    var checkboxes = document.querySelectorAll('input[type="checkbox"]');
    select.selectedIndex = 0;
    checkboxes.forEach(function(checkbox) {
        if (checkbox.id !== 'themeSwitch') {
        checkbox.checked = false; }
    });
    
};



