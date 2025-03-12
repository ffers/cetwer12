




    
function changeBlock(id) {
    console.log(id.closest(".row"))
    // Видаляємо блок AdsressOld
    let oldBlock = id.closest(".row");
    oldBlock.parentNode.removeChild(oldBlock);
  
    // Додаємо інший блок або виконайте інші дії, які вам потрібні
    var container = $('#ProductOldItem');
    var newField = $('<div class="row" id="product-container"> style="width: 100%"')
        .html(`
                <div class="col-sm-3 col-lg-4 button-pult">
                    <select  class="  form-control product-select1" 
                        name="product" required></select>
                </div>
                <div class="col-sm col-lg-2 button-pult">
                    <input type="number" style="text-align: center;" 
                        class=" quantity form-control" id="quantity" 
                        name="quantity"  min="1" max="10000" 
                        placeholder="* Кількість" required>
                   
                </div>
                <div class="col-sm col-lg-2 button-pult" >
                    <input type="number" 
                        style="text-align: center;" 
                        class=" price form-control" 
                        id="price" name="price" 
                        min="1" placeholder="Ціна" required>
                        
                </div>					
                
                    <input type="number" 
                        style="text-align: center; display: none;" 
                        class="total form-control" id="total	" 
                        name="total" min="1" placeholder="Сумма" 
                        required>
                        
           
                <div class="col-sm col-lg-2 button-pult">
                    <button 
                        class="removeButton btn btn-outline-info my-2 my-sm-0"   
                        onclick="deleteBlock(this)">
                        Видалити
                    </button>
                </div>
            `);

// Добавление нового поля в контейнер
container.append(newField);

newField.find('.product-select1').select2({
    width: '100%',
    theme: 'bootstrap-5',
    language: {
    noResults: function () {
    return 'Ничего не знайдено';
    },
    searching: function () {
    return 'Пошук...';
    },
    inputTooShort: function (args) {
    var remainingChars = args.minimum - args.input.length;
    return 'Введіть хочаб ' + remainingChars + ' символ' + (remainingChars > 1 ? 'а' : '');
    }
    },
    ajax: {
    url: '/cabinet/orders/get_product',
    dataType: 'json',
    delay: 250,
    processResults: function (data) {
    return {
        results: data.results.map(function (city) {
            return {
                id: city.id,
                text: city.article
            };
        })
    };
    },
    cache: true
    },
    placeholder: 'Товар',
    templateResult: function (result) {
    return result.text || result.text; // Виведення тексту міста
    }
    });
    var scriptElement = document.createElement('script');
    scriptElement.type = 'module';
    scriptElement.src = "/static/javascript/add-button-product.js";
    document.body.appendChild(scriptElement);
    };
    function deleteBlock(id){
        let oldBlock = id.closest(".row");
        oldBlock.remove();
}
    
    
    // document.addEventListener('DOMContentLoaded', function () {
    //     // Отримуємо всі поля total
    //     var totalInputs = document.querySelectorAll('.total');
    
    //     // Додаємо обробник подій для кожного поля total
    //     totalInputs.forEach(function (totalInput) {
    //         totalInput.addEventListener('input', calculateSum);
    //     });
    
    //     // Функція для розрахунку суми всіх total
    //     function calculateSum() {
    //         // Отримуємо всі значення total і сумуємо їх
    //         var sum = Array.from(totalInputs).reduce(function (acc, totalInput) {
    //             var value = parseFloat(totalInput.value) || 0;
    //             return acc + value;
    //         }, 0);
    
    //         // Виводимо суму
    //         console.log('Загальна сума: ' + sum.toFixed(2));
    //         // Тут ви можете вивести суму куди завгодно на ваш вибір
    //     }
    // });
    
    // calculateTotal();
    // calculateSum();
    
    // // Відслідковування змін у кожному полі ціни та кількості
    // $('#product-container').on('input', '.price, .quantity', calculateTotal);
    // $('#product-container').on('input', '.price, .quantity, .total', calculateSum);
    
    // // Відслідковування події кліку на кнопці видалення
    // $('#product-container').on('click', '.removeButton', function() {
    //     $(this).closest('.row').remove();
    //     calculateTotal(); // Виклик функції для розрахунку суми при видаленні товару



        
    // });