// import { infoModalfunc } from './modal-window.js';

var toastEl = document.querySelector('.toast');

var toastMessage = document.getElementById("toastNotificationMessageLite");
var closeButton = document.createElement('button');
closeButton.classList.add('btn-close', 'btn-close-white', 'me-2', 'm-auto');
closeButton.setAttribute('type', 'button');
closeButton.setAttribute('data-bs-dismiss', 'toast');
closeButton.setAttribute('aria-label', 'Close');

function copyText() {
    var text = document.getElementById("textToCopy").innerText;
    navigator.clipboard.writeText(text)
        .then(function() {
            toastMessage.textContent = "Скопійовано в буфер";
            toastMessage.appendChild(closeButton);
            var toast = new bootstrap.Toast(toastEl);
            toast.show();
        })
        .catch(function(err) {
            console.error('Помилка копіювання тексту: ', err);
            toastMessage.textContent = "Помилка копіювання тексту";
            toastMessage.appendChild(closeButton);
            var toast = new bootstrap.Toast(toastEl);
            toast.show();
        });
}