$(document).ready(function() {
    // Ініціалізація #citySelect
$('#citySelect').select2({ width: '100%', theme: 'bootstrap-5', language: { noResults: function () { return 'Ничего не знайдено';}, searching: function () { return 'Пошук...'; },
    inputTooShort: function (args) {
        var remainingChars = args.minimum - args.input.length; 
        return 'Введіть хочаб ' + remainingChars + ' символ' + (remainingChars > 1 ? 'а' : '');}},
ajax: {
    url: '/cabinet/orders/get_cities',
    dataType: 'json',
    delay: 250,
    processResults: function (data) {
        return {
            results: data.results.map(function (city) {
                return {
                    id: city.CityRef,
                    text: city.City
                };
            })
        };
    },
    cache: true
},
placeholder: 'Місто',
minimumInputLength: 1,
templateResult: function (result) {
    return result.text || result.text; // Виведення тексту міста
}
}).on('change', function (e) {
// Отримати обране місто
var selectedCity = $(this).select2('data')[0];

// Перевірити, чи обрано місто
if (selectedCity) {
    // Зробити новий запит для отримання відділень для обраного міста

    $('#warhousSelect').select2({
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
        // Налаштування для отримання відділень обраного міста
        ajax: {
            url: '/cabinet/orders/get_warehouse',
            dataType: 'json',
            delay: 250,
            data: function (params) {
                return {
                    q: params.term, // Пошуковий термін
                    cityRef: selectedCity.id // ID обраного міста
                };
            },
            processResults: function (data) {
                return {
                    results: data.results.map(function (warehouse) {
                        return {
                            id: warehouse.Ref,
                            text: warehouse.Description

                        };
                    })
                };
            },
            cache: true
        },
        placeholder: 'Віділення',

        templateResult: function (result) {
                return result.text || result.text; // Виведення тексту міста
            }
    });
}
// Якщо місто не обрано, скидаємо вміст відділень
else {
    $('#postSelect').val(null).trigger('change');
}
}).on('change', function (e) {
// Отримати обране місто
var selectedCity = $(this).select2('data')[0];

// Перевірити, чи обрано місто
if (selectedCity) {
    // Зробити новий запит для отримання відділень для обраного міста

    $('#postSelect').select2({
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
        // Налаштування для отримання відділень обраного міста
        ajax: {
            url: '/cabinet/orders/get_post',
            dataType: 'json',
            delay: 250,
            data: function (params) {
                return {
                    q: params.term, // Пошуковий термін
                    cityRef: selectedCity.id // ID обраного міста
                };
            },
            
            processResults: function (data) {
                return {
                    results: data.results.map(function (warehouse) {                        
                        return {
                            id: warehouse.Ref,
                            text: warehouse.Description
                        };
                    })
                };
            },
            cache: true
        },
        placeholder: 'Поштомат',

        templateResult: function (result) {
                return result.text || result.text; // Виведення тексту міста
            }
    });
}
// Якщо місто не обрано, скидаємо вміст відділень
else {
    $('#postSelect').val(null).trigger('change');
}
});
// Ініціалізація #productSelect
$('.product-select').select2({
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


});