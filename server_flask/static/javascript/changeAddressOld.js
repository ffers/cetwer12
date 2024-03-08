document.getElementById('ChangeAddress').addEventListener('click', function() {
    // Видаляємо блок AdsressOld
    let oldAddressBlock = document.getElementById('AdsressOld');
    oldAddressBlock.parentNode.removeChild(oldAddressBlock);
  
    // Додаємо інший блок або виконайте інші дії, які вам потрібні
    var container = $('#address_row');
    var newField = $('<div>')
        .html(
            `<div class="row">
            <legend></legend>
          <div class="col"><input class="form-check-input text-radio" type="radio" id="warehouse" name="warehouse_option" value="warehouse" onclick="toggleField()" ><label for="warehouse" class="form-check-label"> Відділення</label></div>
          <div class="col"><input type="radio" id="poshtomat " class="form-check-input text-radio" name="warehouse_option" value="poshtomat" onclick="toggleField()" /><label for="poshtomat" class="form-check-label"> Поштомат</label></div>
          <div class="col"><input type="radio" id="address" class="form-check-input text-radio" name="warehouse_option" value="address" onclick="toggleField()" /><label for="address" class="form-check-label"> Адреса</label></div>
      </div></br>
      
      <div class="row "> 
            <legend></legend>
          <div class="col"><select id="citySelect" class="js-data-example-ajax    form-control" name="city"  required></select><br></div>
          <div id="hiddenFieldWar" style="display:block;" class="col"><select id="warhousSelect" class="form-control   " name="warehouse" rows="1" cols="50" placeholder="Відділення"></select><br></div>
          <div id="hiddenFieldPost" style="display:none;" class="col"><select id="postSelect" class="form-control   " name="warehouse" rows="1" cols="50" placeholder="Поштомат"></select><br></div>
          <div id="hiddenFieldAdr" style="display:none;" class="col"><textarea id="addressText" class="form-control   " name="warehouse" rows="1" cols="50" placeholder="* Адреса"></textarea></div>
      </div></br>`
            );

    // Добавление нового поля в контейнер
    container.append(newField);
    newField.find('#citySelect').select2({ width: '100%', theme: 'bootstrap-5', language: { noResults: function () { return 'Ничего не знайдено';}, searching: function () { return 'Пошук...'; },
    inputTooShort: function (args) {var remainingChars = args.minimum - args.input.length; return 'Введіть хочаб ' + remainingChars + ' символ' + (remainingChars > 1 ? 'а' : '');}},
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
    return result.text || result.City; // Виведення тексту міста
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
  
  });});