// import { infoModalfunc } from './modal-window.js';

var toastEl = document.getElementById('toastLite');

var toastMessage = document.getElementById("textToastLite");

function copyText(text) {
    // var text = document.getElementById("textToCopy").innerText;
    navigator.clipboard.writeText(text)
        .then(function() {
            toastMessage.textContent = "Скопійовано в буфер";
            var toast = new bootstrap.Toast(toastEl);
            toast.show();
        })
        .catch(function(err) {
            console.error('Помилка копіювання тексту: ', err);
            toastMessage.textContent = "Помилка копіювання тексту";
            var toast = new bootstrap.Toast(toastEl);
            toast.show();
        });
}