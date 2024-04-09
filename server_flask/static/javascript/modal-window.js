// function openModal() {
//     document.getElementById('myModal').style.display = 'block';
//     document.getElementById('modalOverlay').style.display = 'block'
// };

// function closeModal() {
//     document.getElementById('myModal').style.display = 'none';
//     document.getElementById('modalOverlay').style.display = 'none'
// };

// let modalOverlay = document.getElementById('modalOverlay');
// let modal = document.getElementById('myModal');

// window.addEventListener('click', function (event) {
//     if (event.target === modal) {
//         closeModal();
//     }
// });
function infoModalfunc() { 
    let modal = document.getElementById('notificationContainer');
    modal.classList.add('show');
    // Опціонально: приховати уведомлення через 3 секунди
    setTimeout(function() {
        modal.classList.remove('show');
    }, 3000);}

export { infoModalfunc };

// document.addEventListener('DOMContentLoaded', function () {
//     let openModalBtn = document.getElementById('openModalBtn');
    
//     function alignModal() {
//         var windowTop = $(window).scrollTop();
//         var windowHeight = $(window).height();
//         var modalHeight = modal.height();

//         // Визначте нове положення для модального вікна
//         var newTop = windowTop + (windowHeight - modalHeight) / 2;

//         // Змініть стиль верхнього положення модального вікна
//         modal.css('top', newTop + 'px');
//     }

//     openModalBtn.addEventListener('click', function () {
//         infoModalfunc();       


// });
// });


// function sendDataToServer() {
//     var product_name = document.getElementById('product_name').value;
//     var description = document.getElementById('description_prod').value;
//     var price = document.getElementById('price_prod').value;
//     var quantity = document.getElementById('quantity_prod').value;
//     var article = document.getElementById('article').value;
    

//     var formData = new FormData();
//     formData.append('product_name', product_name);
//     formData.append('description', description);
//     formData.append('price', price);
//     formData.append('quantity', quantity);
//     formData.append('article', article);
//     formData.append('modal', 'modal');

//     // Відправка даних на сервер за допомогою AJAX-запиту
//     fetch('/cabinet/products/add_product', {
//         method: 'POST',
//         body: formData,
//     })
//     .then(response => response.json())
//     .then(data => {
//         console.log('Відповідь від сервера:', data);
//         $('#myModal').modal('hide');
//         infoModalfunc();
//     })
//     .catch(error => console.error('Помилка:', error));
// }

// const exampleEl = document.getElementById('example')
// const popover = new bootstrap.Popover(exampleEl, options)