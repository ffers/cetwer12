// import { infoModalfunc } from './modal-window.js';

function add_relate() {
    const product_id = document.getElementById('new_product_id').value;
    const source_ids =  Array.from(
        document.querySelectorAll('#product [name="source_id_modal"]')
    ).map(el => el.value);
    const relate_quantity =  Array.from(
        document.querySelectorAll('#product [name="relate_quantity_modal"]')
    ).map(el => el.value);
    const product_ids = source_ids.map(function() {
        return product_id;
        });
    



    // товар айди под которий подвязать весь список компонентов
    // в продакт релейт добавить записи с етими компонетами с айди вибраного товара
    

    const formData = new FormData();
    source_ids.forEach(id => formData.append('article', id));
    product_ids.forEach(id => formData.append('product', id));
    relate_quantity.forEach(id => formData.append('quantity', id));
    formData.append('modal', 'modal');


    // Відправка даних на сервер за допомогою AJAX-запиту
    fetch('/cabinet/products/add_product_relate', {
        method: 'POST',
        body: formData,
    })
    .then(response => response.json())
    .then(data => {
        console.log('Відповідь від сервера:', data);
        // const resp = JSON.parse(data);
        const result = data.result;
        console.log('Резалт:', result);
        if (result === 'ok'){
            $('#addComponent').modal('hide');
            var toastLite = document.getElementById('toastLite');
            var textToastLite = document.getElementById("textToastLite");
            textToastLite.textContent = "Компоненти додано";
            var toast = new bootstrap.Toast(toastLite);
            toast.show();
            location.reload();
        } else {
            var toastLite = document.getElementById('toastLite');
            var textToastLite = document.getElementById("textToastLite");
            textToastLite.textContent = "Невийшло";
            var toast = new bootstrap.Toast(toastLite);
            toast.show();
        }
        

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



