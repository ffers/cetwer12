
function processOrders(action) {
    var checkboxes = document.getElementsByName('selectedItems');
    var selectedOrders = [];
    var toastEl = document.querySelector('.toast');
    var toast = new bootstrap.Toast(toastEl);
    var toastMessage = document.getElementById('textToCopy');
    var toastMessageLite = document.getElementById("toastNotificationMessageLite");

    // Проходимося по всіх чекбоксах і зберігаємо вибрані замовлення у масив
    for (var i = 0; i < checkboxes.length; i++) {
        if (checkboxes[i].checked) {
            selectedOrders.push(checkboxes[i].value);
            var selectedOption = this.value;
        }
    }

    // Виконуємо певні дії з вибраними замовленнями в залежності від дії
    if (action === 'add_reg') {
        // Логіка для схвалення замовлень
        fetch('/cabinet/order_draft', {
            method: 'POST',
            credentials: "same-origin",
            redirect: "follow",
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ id: selectedOrders})
        })
        .then(response => response.json())
        .then(data => {
            console.log(data)
            toastMessage.textContent = data.number_registr;
            var button = document.getElementById("buttonTextToast");
            if (button) {
                // Додайте атрибут onclick до кнопки
                button.setAttribute("onclick", "copyText()");
                button.textContent = "Скопіювати";
            } else {
                console.error("Кнопку з заданим ідентифікатором не знайдено.");
            }
             
            toast.show();
           })
        // .then(data => {
        //     window.location.reload();
        //    });
        .catch(function(err) {
            console.error('Помилка додавання в реєєстр: ', err);
            toastMessageLite.textContent = "Помилка додавання в реєєстр";
            toastMessageLite.appendChild(closeButton);
            var toast = new bootstrap.Toast(toastEl);
            toast.show();
        });
    } else if (action === 'del_reg') {
        // Логіка для відхилення замовлень
        fetch('/cabinet/orders/del_reg', {
            method: 'POST',
            credentials: "same-origin",
            redirect: "follow",
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ id: selectedOrders})
            })
        .then(data => {
             window.location.reload();
            });
    } else if (action === 'changeStatus1') {
        // Логіка для відхилення замовлень
        fetch('/cabinet/orders/changeStatus', {
            method: 'POST',
            credentials: "same-origin",
            redirect: "follow",
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ id: selectedOrders, status: selectedOption})
            })
        .then(data => {
             window.location.reload();
            });
    };
}
