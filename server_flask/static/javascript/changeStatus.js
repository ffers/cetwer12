document.getElementById("changeStatus").addEventListener("change", function() {
    var selectedOption = this.value;
    
    var checkboxes = document.getElementsByName('selectedItems');
    var selectedOrders = [];
    // Проходимося по всіх чекбоксах і зберігаємо вибрані замовлення у масив
    if (checkboxes && checkboxes.type === "checkbox" && checkboxes.checked) {
        for (var i = 0; i < checkboxes.length; i++) {
            if (checkboxes[i].checked) {
                selectedOrders.push(checkboxes[i].value);
                var selectedOption = this.value;
            }
        }
    } else {
        var selectedOption = this.value;
        selectedOrders.push(document.getElementById("selectedItems").value)
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
    var toastLite = document.getElementById('toastLite');
    var toast = new bootstrap.Toast(toastLite);
    var textToastLite = document.getElementById("textToastLite");
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
        console.error('Все ОК: ', data);
        localStorage.setItem("toastMessage", "Статус змінено");
        window.location.reload();
    })
    .catch((error) => {
        console.error('Сталася помилка: ', error);
        textToastLite.textContent = "Сталася помилка";
        toast.show();
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



