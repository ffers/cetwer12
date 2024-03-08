function calculateTotal() {
    // Отримуємо колекції елементів ціни, кількості та суми
    var priceInputs = document.querySelectorAll('.price');
    var quantityInputs = document.querySelectorAll('.quantity');
    var totalInputs = document.querySelectorAll('.total');

    // Додаємо обробники подій для кожного товару
    for (var i = 0; i < priceInputs.length; i++) {
        priceInputs[i].addEventListener('input', calculateTotal);
        quantityInputs[i].addEventListener('input', calculateTotal);
    }

    // Функція для розрахунку суми для кожного товару
   
        // Проходимося по всіх товарах і розраховуємо суму для кожного
        for (var i = 0; i < priceInputs.length; i++) {
            // Отримуємо значення ціни та кількості для кожного товару
            var price = parseFloat(priceInputs[i].value) || 0;
            var quantity = parseFloat(quantityInputs[i].value) || 0;

            // Розраховуємо суму (ціна * кількість) для кожного товару
            var total = price * quantity;

            // Виводимо суму в поле "Сума" для кожного товару
            totalInputs[i].value = total.toFixed(2); // Виводимо суму з двома знаками після коми
        }
    
}
export { calculateTotal };


    // Отримуємо колекції елементів ціни, кількості та суми
    

// calculate.js

// Експортуємо функцію calculateSum
    export function calculateSum() {
        // Отримуємо всі поля total
        var totalInputs = document.querySelectorAll('.total');
        var totalInputsAll = document.querySelectorAll('.totalall');

        // Додаємо обробник подій для кожного поля total
        totalInputs.forEach(function (totalInput) {
            totalInput.addEventListener('input', function () {
                // Викликаємо функцію calculateSum
                calculateSum(totalInputs);
            });
        });

        // Отримуємо всі значення total і сумуємо їх
        var sum = Array.from(totalInputs).reduce(function (acc, totalInput) {
            var value = parseFloat(totalInput.value) || 0;
            return acc + value;
        }, 0);

        // Виводимо суму
        console.log('Загальна сума: ' + sum.toFixed(2));
        // Тут ви можете вивести суму куди завгодно на ваш вибір
        totalInputsAll.forEach(function (totalInputAll) {
            totalInputAll.value = sum.toFixed(2);
        });
    }

