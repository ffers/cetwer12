
document.addEventListener("DOMContentLoaded", function () {
  const radios = document.querySelectorAll('input[name="payment_option"]');
  const container = document.getElementById("add_sum_before_goods");
  const sumValue = container.dataset.sum || "";

  function toggleField() {
    const selected = document.querySelector('input[name="payment_option"]:checked');

    // видалити поле, якщо існує
    const oldField = document.getElementById("hiddenFieldPay");
    if (oldField) oldField.remove();

    // якщо обрано "Передплата", додати поле
    if (selected && selected.value === "3") {
      const row = document.createElement("div");
      row.className = "row mt-4";
      row.id = "hiddenFieldPay";

      row.innerHTML = `
        <input type="number" class="form-control text-center"
               id="sum_before_goods"
               name="sum_before_goods"
               min="1"
               placeholder="Сума"
               value="${sumValue}"
               required>
      `;
      container.appendChild(row);
    }
  }

  radios.forEach(radio => {
    radio.addEventListener("change", toggleField);
  });

  // Ініціалізація при завантаженні
  toggleField();
});

