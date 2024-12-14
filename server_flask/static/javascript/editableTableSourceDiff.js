
$(document).ready(function () {
    const table = $('#editableTable').DataTable({
        pageLength: 50,
        hover: true,
        autoWidth: false,
        // columnDefs: [{ width: '100%' }]
        drawCallback: function() {
            $('.select-source').select2({ 
                width: '100%',
                theme: 'bootstrap-5',
                language: {
                    noResults: function () {
                        return 'Ничого не знайдено';
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
            }
            
         }
    );


$('#saveBtn').on('click', function () {
  const newData = [];
                
                // Проходимо всі рядки таблиці
                $('#editableTable tbody tr').each(function () {
                    const id = $(this).data('id');
                    const row = [id];
                    // Проходимо всі комірки в рядку
                    $(this).find('td').each(function () {
                        // Якщо комірка містить input
                        const input = $(this).find('input');
                        if (input.length) {
                            row.push(input.val()); // Зчитуємо значення з input
                        } else {
                            row.push($(this).text()); // Зчитуємо текст
                        }
                    });
                    newData.push(row); // Додаємо рядок у масив
                });

                // Очищуємо старі дані в DataTable
                table.clear();
                
                // Додаємо нові дані
                table.rows.add(newData);              
                
            
  const tableData = [];

  table.rows().every(function (rowIdx, tableLoop, rowLoop) {
      const data = this.data();
      tableData.push({
          id: data[0],  
          crm: data[5],  
          stock: data[6]           
        });
        console.log(tableData)
  });


  // Відправка даних
  $.ajax({
      url: '/cabinet/source_difference/update_bulk',
      type: 'POST',
      contentType: 'application/json',
      data: JSON.stringify(tableData),
      success: function (response) {
          location.reload()
          
      }
  });
});
});
