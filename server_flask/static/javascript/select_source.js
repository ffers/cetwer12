$(document).ready(function () {
$('.select-source').select2({ 
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
        url: '/cabinet/source/get_source',
        dataType: 'json',
        delay: 250,
        processResults: function (data) {
            return {
                results: data.results.map(function (item) {
                    return {
                        id: item.id,
                        text: item.article
                    };
                })
            };
        },
        cache: true
    },
    placeholder: 'Ісходнік',
    templateResult: function (result) {
        return result.text || result.text; // Виведення тексту міста
    }
    });   
});

