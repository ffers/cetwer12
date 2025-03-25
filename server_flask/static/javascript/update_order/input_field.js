document.querySelectorAll('.editable').forEach(function(div) {
    div.addEventListener('click', function () {
      const input = this.nextElementSibling;
      this.classList.add('d-none');
      input.classList.remove('d-none');
      input.focus();
    });
  });

  document.querySelectorAll('.form-control').forEach(function(input) {
    input.addEventListener('blur', function () {
      const div = this.previousElementSibling;
      const name = this.name;
      const hidden = document.querySelector('input[type="hidden"][name="' + name + '"]');

      div.textContent = this.value;
      this.classList.add('d-none');
      div.classList.remove('d-none');

      if (hidden) {
        hidden.value = this.value;
      }
    });
  });