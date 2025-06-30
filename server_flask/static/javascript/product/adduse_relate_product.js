// import { infoModalfunc } from './modal-window.js';

function adduse_relate() {
    const new_product_id = document.getElementById('new_product_id').value;
    const old_product_id =  document.getElementById('old_product_id').value;
 
    



    // товар айди под которий подвязать весь список компонентов
    // в продакт релейт добавить записи с етими компонетами с айди вибраного товара
    

    const formData = new FormData();
    formData.append('new_product_id', new_product_id);
    formData.append('old_product_id', old_product_id);
    formData.append('modal', 'modal');


    // Відправка даних на сервер за допомогою AJAX-запиту
    fetch('/cabinet/products/adduse_product_relate', {
        method: 'POST',
        body: formData,
    })
    .then(response => response.json())
    .then(data => {
        console.log('Відповідь від сервера:', data);
        // const resp = JSON.parse(data);
        const result = data.result;
        console.log('Резалт:', result);
        var toastLite = document.getElementById('toastLite');
        var textToastLite = document.getElementById("textToastLite");
        if (result === 'ok'){
            $('#adduseComponent').modal('hide');
            textToastLite.textContent = "Компоненти додано";
            var toast = new bootstrap.Toast(toastLite);
            toast.show();
            location.reload();
        } else if (result === 'product_empty') {
            textToastLite.textContent = "У цього товару нема компонентів";
            var toast = new bootstrap.Toast(toastLite);
            toast.show();
        } else {
            textToastLite.textContent = "Невийшло";
            var toast = new bootstrap.Toast(toastLite);
            toast.show();
        }
        

    })
    .catch(error => {
        console.error('Помилка:', error);
        $('#adduseComponent').modal('hide');
        var toastLite = document.getElementById('toastLite');
        var textToastLite = document.getElementById("textToastLite");
        textToastLite.textContent = "Помилка, можливо товар вже було создано";
        new bootstrap.Toast(toastLite).show();

    });
}



