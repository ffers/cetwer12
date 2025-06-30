$(document).ready(function() {
    document.querySelectorAll('.select-product').forEach(function(selectEl) {
        const modal = selectEl.closest('.modal-div');
        const select2Options = {
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
                return result.text || result.text;
            }
        }

    if (modal) {
    select2Options.dropdownParent = $(modal);
    }
// Ініціалізація #productSelect
    $(selectEl).select2(select2Options);


});
});