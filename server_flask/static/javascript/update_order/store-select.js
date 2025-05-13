$(document).ready(function () {
    $('.select2').select2({ 
      width: '30%', 
      theme: 'bootstrap-5', 
      language: { 
        noResults: function () { 
          return 'Ничего не знайдено';}, 
        searching: function () { return 'Пошук...'; }},
      ajax: {
          url: '/cabinet/store/list_select',
          dataType: 'json',
          delay: 250,
          processResults: function (data) {
              return {
                  results: data.results.map(function (item) {
                      return {
                          id: item.id,
                          text: item.name
                      };
                  })
              };
          },
          cache: true
      },
      placeholder: 'Store',
      templateResult: function (result) {
          return result.text || result.City; // Виведення тексту міста
      }

});
const $container = $('.select2-container');
    $container.addClass('d-none');

  
document.querySelectorAll('.editable').forEach(function (div) {
  div.addEventListener('click', function () {
    const id = div.dataset.id;
    const $select = $(`select.select2[data-id="${id}"]`);

    div.classList.add('d-none');

    const $container = $select.next('.select2-container');
    $container.removeClass('d-none');

    // open select2 dropdown
    setTimeout(() => $select.select2('open'), 100);
  });
});

$('.select2').on('select2:close', function () {
  const id = this.dataset.id;
  const div = document.querySelector(`.editable[data-id="${id}"]`);
  const $container = $(this).next('.select2-container');

  // оновити текст
  const selectedText = this.options[this.selectedIndex].text;
  div.textContent = selectedText;

  div.classList.remove('d-none');
  $container.addClass('d-none');
});


});
  