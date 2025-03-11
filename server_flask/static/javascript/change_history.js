const form = document.querySelector("#changehistory");

async function changeHistory() {
    const formData = new FormData(form);
    // Відправка даних на сервер за допомогою AJAX-запиту
    try {
        const responce = await fetch('/cabinet/orders/change_history', {
            method: 'POST',
            body: formData,
        });
        console.log('Відповідь від сервера:', responce);
        $('#historyModal').modal('hide');
        var toastLite = document.getElementById('toastLite');
        var textToastLite = document.getElementById("textToastLite");
        textToastLite.textContent = "Історію змінено";
        var toast = new bootstrap.Toast(toastLite);
        toast.show();
    } catch(e) {
        console.error('Помилка:', e);
        var toastLite = document.getElementById('toastLite');
        var textToastLite = document.getElementById("textToastLite");
        textToastLite.textContent = "Помилка";
        new bootstrap.Toast(toastLite).show();
    }
}

// Take over form submission
form.addEventListener("submitHistory", (event) => {
    event.preventDefault();
    sendData();
  });