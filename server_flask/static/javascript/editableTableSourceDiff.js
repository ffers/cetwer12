
$(document).ready(function () {
    const table = $('#editableTable').DataTable({
        pageLength: 50,
        hover: true,
        autoWidth: false
        // columnDefs: [{ width: '100%' }]
    });

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
