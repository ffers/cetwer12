$(document).ready(function () {
    let modal = document.getElementById('modal-div')
    let select2Options = { 
    width: '100%',
    theme: 'bootstrap-5',
    if (modal) {

    },
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
    }
if (modal) {
  select2Options.dropdownParent = $('#modal-div');
}
$('.select-source').select2(select2Options);   
});

