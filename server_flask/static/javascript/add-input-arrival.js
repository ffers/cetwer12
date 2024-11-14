
$('#addButton').on('click', function() {
    var container = $('#product-container');
    var newField = $(`
     <div class="row">
                        <!-- Товар та кількість -->
                        <div class="col-sm" >
                            <input 
                                style="text-align: center;" 
                                class="form-control" 
                                id="description" 
                                name="description" 
                                min="1" 
                                placeholder="Опис" 
                                value="Товар"
                                required>
                        </div>
                					
                        <div class="col-sm">
                            <select  
                                class="form-control select-source" 
                                name="article" 
                                required>
                            </select> 
                        </div>
                        <div class="col-sm col-lg-2">
                            <input 
                            style="text-align: center;" 
                            class=" quantity form-control" 
                            id="quantity" name="quantity"  
                            min="1" max="10000" 
                            placeholder="* Кількість" 
                            required>
                        </div>
                        <div class="col-sm col-lg-2"><button type="button" class="removeButton text-button">Видалити</button></div>
                    </div>       
`);


    // Добавление нового поля в контейнер
    container.append(newField);

    


    // Инициализация Select2 для нового поля
    newField.find('.select-source').select2({
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

    $('#product-container').on('click', '.removeButton', function() {
        $(this).closest('.row').remove();
        });