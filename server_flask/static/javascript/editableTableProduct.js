
$(document).ready(function () {
    let table = $('#editableTable').DataTable({
      pageLength: 50,
      hover: true,
      autoWidth: false
    //   columnDefs: [{ width: '10%' }]

    });

    // var value = $(this).val();
    // $('#myInput').off('keyup').on('keyup', function () {
    //     table.search(this.value).draw();
    // });
    

//     $('#myInput').on('keyup', function () {
//         table.search(this.value).draw();
//     });

// $('#example_filter input').off('keyup').on('keyup', function() {
//         // Отримуємо введене значення
//         var value = $(this).val();
//         if (value) {
//             // Використовуємо точний пошук
//             table.search('^' + value + '$', true, false).draw();
//         } else {
//             // Порожній пошук, якщо поле очищене
//             table.search('').draw();
//         }
//     });

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
                console.log(newData)

                // Очищуємо старі дані в DataTable
                table.clear();
                
                // Додаємо нові дані
                table.rows.add(newData);              
                
            
  const tableData = [];

  table.rows().every(function (rowIdx, tableLoop, rowLoop) {
      const data = this.data();
      tableData.push({
          id: data[0], 
          article: data[1], 
          name: data[2]        
        });
        console.log(tableData, "datta")
  });


  // Відправка даних
  $.ajax({
      url: '/cabinet/product/update_bulk',
      type: 'POST',
      contentType: 'application/json',
      data: JSON.stringify(tableData),
      success: function (response) {
          location.reload()
          
      }
  });
});
});
