
function processOrders(action) {
    var checkboxes = document.getElementsByName('selectedItems');
    var selectedOrders = [];

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
        // fetch('/cabinet/order_draft', {
        //     method: 'POST',
        //     credentials: "same-origin",
        //     redirect: "follow",
        //     headers: {
        //         'Content-Type': 'application/json'
        //     },
        //     body: JSON.stringify({ id: selectedOrders})
        // })
        // .then(data => {
            var modal = document.getElementById("exampleModal");
            var modalMessage = document.getElementById("modalNotificationMessage");
            modalMessage.textContent = "dsad";
            $(modal).modal('show');
        //    });
        // .then(data => {
        //     window.location.reload();
        //    });
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
