// import { infoModalfunc } from './modal-window.js';

function copyText() {
    var text = document.querySelectorAll(".textToCopy").innerText;
    navigator.clipboard.writeText(text)
        .then(function() {
            alert("Номер скопійовано до буферу обміну!");
        })
        .catch(function(err) {
            console.error('Помилка копіювання тексту: ', err);
            alert("Помилка копіювання тексту!");
        });
}