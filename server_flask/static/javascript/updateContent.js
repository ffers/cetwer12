document.getElementById("searchFormContent").addEventListener("submit", function(event) {
    event.preventDefault(); // Зупиняємо стандартну поведінку форми
    
    var formData = new FormData(this); // Створюємо об'єкт FormData для передачі даних форми
    
    fetch("/your-server-endpoint", {
      method: "POST", // або "GET", в залежності від вашого серверного обробника
      body: formData
    })
    .then(response => response.text())
    .then(data => {
      document.getElementById("responseDiv").textContent = data; // Виводимо відповідь сервера у спеціальний div
    })
    .catch(error => {
      console.error("Error:", error);
    });
  });
  