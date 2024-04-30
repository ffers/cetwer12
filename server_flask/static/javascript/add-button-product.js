
$('#addButton').on('click', function() {
    var container = $('#product-container');
    var newField = $(`
        <div class="row" >
        <div class="col-sm"><select class="form-control product-select" name="product"></select></div><br>
        <div class="col-sm col-lg-2"><input type="number" style="text-align: center;" class="quantity form-control" id="quantity" name="quantity"  min="1" max="10000" placeholder="* Кількість" required><br></div>
        <div class="col-sm col-lg-2"><input type="number" style="text-align: center;" class="price form-control" id="price" name="price" min="1" placeholder="Ціна" required><br></div>
        <div class="col-sm col-lg-2"><input type="number" style="text-align: center; display: none;" class="total form-control" id="sum_price" name="sum_price" min="1" placeholder="Сумма" required><br></div>
        <div class="col-sm col-lg-2"><button type="button" class="removeButton text-button">Видалити</button></div>
        </div>`
    );

    // Добавление нового поля в контейнер
    container.append(newField);
    // Викликаєм калькулятор
    


    // Инициализация Select2 для нового поля
    newField.find('.product-select').select2({
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
        // var scriptElement = document.createElement('script');
        //         scriptElement.type = 'module';
        //         scriptElement.src = "/static/javascript/add-button-product.js";
        //         document.body.appendChild(scriptElement);
        });

$('#product-container').on('click', '.removeButton', function() {
$(this).closest('.row').remove();
});

import { calculateTotal, calculateSum } from './calculate.js';
document.addEventListener('DOMContentLoaded', function () {
    // Отримуємо всі поля total
    var totalInputs = document.querySelectorAll('.total');

    // Додаємо обробник подій для кожного поля total
    totalInputs.forEach(function (totalInput) {
        totalInput.addEventListener('input', calculateSum);
    });

    // Функція для розрахунку суми всіх total
    function calculateSum() {
        // Отримуємо всі значення total і сумуємо їх
        var sum = Array.from(totalInputs).reduce(function (acc, totalInput) {
            var value = parseFloat(totalInput.value) || 0;
            return acc + value;
        }, 0);

        // Виводимо суму
        console.log('Загальна сума: ' + sum.toFixed(2));
        // Тут ви можете вивести суму куди завгодно на ваш вибір
    }
});

calculateTotal();
calculateSum();

// Відслідковування змін у кожному полі ціни та кількості
$('#product-container').on('input', '.price, .quantity', calculateTotal);
$('#product-container').on('input', '.price, .quantity, .total', calculateSum);

// Відслідковування події кліку на кнопці видалення
$('#product-container').on('click', '.removeButton', function() {
    $(this).closest('.row').remove();
    calculateTotal(); // Виклик функції для розрахунку суми при видаленні товару
});