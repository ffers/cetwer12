document.addEventListener('keydown', function(e) {
    if (e.key === 'Enter' && e.target.tagName === 'INPUT') {
      e.preventDefault();
      const input = e.target;
      const display = input.previousElementSibling;
  
      if (display && display.classList.contains('editable')) {
        display.textContent = input.value;
        input.classList.add('d-none');
        display.classList.remove('d-none');
      }
    }
  });
  