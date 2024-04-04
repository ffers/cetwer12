$(document).ready(function() {
$('#search-select2').select2({
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
        url: '/cabinet/orders/search_for_phone',
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
    placeholder: 'Пошук по телефону',
    templateResult: function (result) {
        return result.text || result.text; // Виведення тексту міста
    }
    
    
    });
    $('#search-select2').on('select2:select', function (item) {
    
        // Перевірка, щоб упевнитися, що обраний варіант не пустий
        
          // Перехід на сторінку редагування з обраним ID
          window.location.href = '/cabinet/orders/update/' + item.params.data.id;
        
    });

    
    });