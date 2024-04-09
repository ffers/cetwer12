// import { infoModalfunc } from './modal-window.js';

function sendDataToServerW() {
    var product_name = document.getElementById('product_name').value;
    var description = document.getElementById('description_prod').value;
    var price = document.getElementById('price_prod').value;
    var quantity = document.getElementById('quantity_prod').value;
    var article = document.getElementById('article').value;
    

    var formData = new FormData();
    formData.append('product_name', product_name);
    formData.append('description', description);
    formData.append('price', price);
    formData.append('quantity', quantity);
    formData.append('article', article);
    formData.append('modal', 'modal');

    var toastEl = document.querySelector('.toast');
    var toast = new bootstrap.Toast(toastEl);
    // Відправка даних на сервер за допомогою AJAX-запиту
    fetch('/cabinet/products/add_product', {
        method: 'POST',
        body: formData,
    })
    .then(response => response.json())
    .then(data => {
        console.log('Відповідь від сервера:', data);
        $('#myModal').modal('hide');
        
        toast.show();
        infoModalfunc();
    })
    .catch(error => {
        console.error('Помилка:', error);
        $('#myModal').modal('hide');
        var toastMessage = document.getElementById("toastNotificationMessageLite");
        toastMessage.textContent = "Помилка, можливо товар вже було создано";
        var closeButton = document.createElement('button');
        closeButton.classList.add('btn-close', 'btn-close-white', 'me-2', 'm-auto');
        closeButton.setAttribute('type', 'button');
        closeButton.setAttribute('data-bs-dismiss', 'toast');
        closeButton.setAttribute('aria-label', 'Close');
        toastMessage.appendChild(closeButton);
        toast.show();

    });
}



