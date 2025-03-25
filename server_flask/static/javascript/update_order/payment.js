 // Показати редагування способу оплати
 paymentDisplay.addEventListener("click", function () {
    paymentDisplay.style.display = "none";
    paymentEdit.style.display = "block";
  });

  // Обрати спосіб оплати
  document.querySelectorAll('input[name="payment_option"]').forEach(function (radio) {
  radio.addEventListener("change", function () {
    const label = document.querySelector(`label[for="${this.id}"]`);
    paymentText.textContent = label.textContent.trim();

    // оновити hidden input
    document.getElementById("paymentMethodInput").value = this.value;

    paymentEdit.style.display = "none";
    paymentDisplay.style.display = "block";
  });
});

  // Клік по статусу → редагування
  statusDisplay.addEventListener("click", function () {
    statusDisplay.style.display = "none";
    statusEdit.style.display = "block";
    // синхронізуємо чекбокс з поточним статусом
    statusToggle.checked = paymentStatus.textContent.trim() === "Оплачено";
  });

  // Зміна статусу
  statusToggle.addEventListener("change", function () {
  const isPaid = this.checked;
  paymentStatus.textContent = isPaid ? "Оплачено" : "Не оплачено";
  document.getElementById("paymentStatusInput").value = isPaid ? "1" : "0";

  statusEdit.style.display = "none";
  statusDisplay.style.display = "block";
});