
function processOrders(action) {
    var checkboxes = document.getElementsByName('selectedItems');
    var selectedOrders = [];

    var toastEl = document.querySelector('.toast');
    var toastMessage = document.getElementById('textToCopy');

    var toastLite = document.getElementById('toastLite');
    var textToastLite = document.getElementById("textToastLite");

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
            toastMessage.textContent = data.number_registr; // data.number_registr;
            var button = document.getElementById("buttonTextToast");
            button.textContent = "Скопіювати";
            [toastMessage, button].forEach(function(element) {
                element.addEventListener("click", function() {
                    copyText(data.number_registr);
                });
            });
            new bootstrap.Toast(toastEl).show();
        })
        // .then(data => {
        //     window.location.reload();
        //    });
        .catch(function(err) {
            console.error('Помилка додавання в реєєстр: ', err);
            textToastLite.textContent = "Помилка додавання в реєєстр";
            var toast = new bootstrap.Toast(toastLite);
            toast.show();
        });
    } else if (action === 'del_reg') {
        // Логіка для видалення з реєстру
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
            textToastLite.textContent = "Видаленно з реєстру";
            var toast = new bootstrap.Toast(toastLite);
            toast.show();
            });
    } else if (action === 'vcvc') {
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
