const option = { trigger: 'manual',}
let client_lastname_input = document.getElementById('client_lastname');
let client_firstname_input = document.getElementById('client_firstname');
let popoverTriggerEl_lastname = document.getElementById('client_lastname');
let popoverTriggerEl_firstname = document.getElementById('client_firstname');
let popover_lastname = new bootstrap.Popover(popoverTriggerEl_lastname, option);
let popover_firstname = new bootstrap.Popover(popoverTriggerEl_firstname, option);

client_lastname_input.addEventListener('input', function () {
    validateAndTogglePopover(client_lastname_input, popover_lastname);
});

client_firstname_input.addEventListener('input', function () {
    validateAndTogglePopover(client_firstname_input, popover_firstname);
});

let isPopoverVisible = false;

// Додаємо обробник подій для події input
function validateAndTogglePopover(inputElement, popoverInstance) {
    // Отримуємо введене значення з текстового поля
    
    let inputValue = inputElement.value;
    
    // Перевірка, чи містить рядок тільки кирилицю
    if (/^[а-яА-ЯЁёіїє\s]+$/.test(inputValue)) {
        // Якщо все вірно, ховаємо поповер

        
        if (isPopoverVisible) {
          popoverInstance.hide();
          isPopoverVisible = false;
      }
    } else {
        // Якщо є помилка, відображаємо поповер
        if (inputValue.length > 1) {
                if (!isPopoverVisible) {
                  popoverInstance.show();
                  isPopoverVisible = true;
                }
        }       
    }
};




    // Ваша власна функція для перевірки заповненості полів
 function isFormValid() {
      let selectedCity = $('#citySelect').length > 0 ? $('#citySelect') : null;
      if (selectedCity) {
          let selectedCity = $('#citySelect').select2('data')[0];
          if ( !selectedCity ) {
              alert('Будь ласка, заповніть "місто" обов\'язкове поле.');
              return false;
          } else {
            
            const selectedWarehouse = $('#warhousSelect').select2('data')[0];
            const selectedPost = $('#postSelect').select2('data')[0] || null;
            let warehouseData = selectedWarehouse || selectedPost || { id: 'null', text: document.getElementById('addressText').value };
            let encodedWarehouse = encodeURIComponent(warehouseData.text);
            $('#myForm').append('<input type="hidden" name="warehouse-id" value="' + warehouseData.id + '">');
            $('#myForm').append('<input type="hidden" name="warehouse-text" value="' + encodedWarehouse + '">');
            $('#myForm').append('<input type="hidden" name="CityREF" value="' + selectedCity.id + '">');
            $('#myForm').append('<input type="hidden" name="CityName" value="' + selectedCity.text + '">');
          }
      }
      let productSelect = $('#product-select').length > 0 ? $('#product-select') : null;
      if (productSelect) {
          const productSelect = document.querySelector('[name="product"]');
          const quantityInput = document.getElementById('quantity');
          const priceInput = document.getElementById('price');
          const selectedProduct = $('.product-select').select2('data');
          if ( 
            productSelect.value === '' ||
            quantityInput.value === '' ||
            priceInput.value === '' ||
            !selectedProduct
           ) {
            alert('Будь ласка, заповніть всі обов\'язкові поля товару замовлення.');
            return false;
        } 
      } else {
        return true
      }
    };

function paymentMethod(){
  const paymentOptions = document.getElementsByName("payment_option");
  console.log("dev_paymentOptions", paymentOptions)
  
      if (paymentOptions.length > 0) {
        const isChecked = Array.from(paymentOptions).some(option => option.checked);  
        if (!isChecked) {
        alert('Будь ласка, заповніть всі обов\'язкові поля.');
          return false;
        } else {
        return true
        }
      }
      return true
    };


function methodDeliveryValid(){
  const delivery_method_detail = document.getElementById('delivery_method_detail');
  if (delivery_method_detail){
    if(delivery_method_detail.value){
      return true
    } else {
      console.log("dev_paymentOptions", "False")
      alert('Будь ласка, заповніть поле спосіб доставки.');
      return false
    }
  }
  return true
};
  
function submitForm() { 
  event.preventDefault();
  if (isFormValid() && methodDeliveryValid() && paymentMethod()) { 
    // const form = document.getElementById('myForm');
    // const formData = new FormData(form);

    // for (const [key, value] of formData.entries()) {
    //   console.log(`${key}: ${value}`);
    // }
    // Відправка форми
    $('#myForm').submit(); 
  } 
}
