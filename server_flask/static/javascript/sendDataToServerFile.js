// import { infoModalfunc } from './modal-window.js';

function sendDataToServerW() {
    var product_name = document.getElementById('product_name').value;
    var description = "None"
    var price = document.getElementById('price_prod').value;
    var quantity = 0
    var article = document.getElementById('article').value;
    

    var formData = new FormData();
    formData.append('product_name', product_name);
    formData.append('description', description);
    formData.append('price', price);
    formData.append('quantity', quantity);
    formData.append('article', article);
    formData.append('modal', 'modal');


    // Відправка даних на сервер за допомогою AJAX-запиту
    fetch('/cabinet/products/add_product', {
        method: 'POST',
        body: formData,
    })
    .then(response => response.json())
    .then(data => {
        console.log('Відповідь від сервера:', data);
        $('#myModal').modal('hide');
        var toastLite = document.getElementById('toastLite');
        var textToastLite = document.getElementById("textToastLite");
        textToastLite.textContent = "Продукт створено";
        var toast = new bootstrap.Toast(toastLite);
        toast.show();

    })
    .catch(error => {
        console.error('Помилка:', error);
        $('#myModal').modal('hide');
        var toastLite = document.getElementById('toastLite');
        var textToastLite = document.getElementById("textToastLite");
        textToastLite.textContent = "Помилка, можливо товар вже було создано";
        new bootstrap.Toast(toastLite).show();

    });
}



