document.addEventListener('DOMContentLoaded', function () {
    document.documentElement.style.display = 'none';
    const themeSwitch = document.getElementById('themeSwitch');
    const savedTheme = localStorage.getItem('userTheme');
    themeSwitch.checked = savedTheme === 'dark';

    // Залиште решту вашого JavaScript-коду тут



    // const themeSwitch = document.getElementById('themeSwitch');

    // // Отримати попередній вибір теми з локального сховища
    // const savedTheme = localStorage.getItem('userTheme');

    // Встановити початковий стан чекбокса відповідно до локального сховища
    // themeSwitch.checked = savedTheme === 'dark';

    // Встановити тему при завантаженні сторінки
    document.documentElement.setAttribute('data-bs-theme', themeSwitch.checked ? 'dark' : 'light');

    // Зберегти стан чекбокса в локальному сховищі
    function saveTheme() {
        const selectedTheme = themeSwitch.checked ? 'dark' : 'light';
        localStorage.setItem('userTheme', selectedTheme);
    }

    // Функція для динамічного додавання або видалення CSS правил
    function updateStyles(theme) {
        // Знайдемо або створимо елемент стилів
        let styleElement = document.getElementById('customStyles');

        if (!styleElement) {
            styleElement = document.createElement('style');
            styleElement.id = 'customStyles';
            document.head.appendChild(styleElement);
        }

        // Очистимо старі CSS правила
        styleElement.innerHTML = '';

        // Додамо нові CSS правила в залежності від теми
        if (theme === 'dark') {
            const darkModeCSS = `
                
.select2-search {
    background-color: #020208 !important;
}
    /* Change the appearence of the search input field */
.select2-search input {
        color: #7b7f83 !important;
        background-color: #020208 !important;
    }

/* Change the appearence of the search results container */
.select2-results {
    background-color: #020208 !important;
    
}

/* Change the appearence of the dropdown select container */
.select2-container--bootstrap-5 .select2-selection {
    border-color: #6c757d !important;
    color: #6c757d !important;
    background-color: #020208 !important;
}

/* Change the caret down arrow symbol to white */
.select2-container--bootstrap-5 .select2-selection--single {
    background-image: url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16'%3e%3cpath fill='none' stroke='white' stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M2 5l6 6 6-6'/%3e%3c/svg%3e") !important;
}

/* Change the color of the default selected item i.e. the first option */
.select2-container--bootstrap-5 .select2-selection--single .select2-selection__rendered {
    color: #a0a4a8 !important;
}

.select2-container--bootstrap-5 .select2-dropdown .select2-results__options .select2-results__option.select2-results__option--highlighted {
    color: #6c757d;
    background-color: #020208;
  }
.select2-container--bootstrap-5 .select2-dropdown {
    color: #3F4347;
    border-color: #495057;
  }
body {
    font-family: Arial, sans-serif;
    margin: 0;
    padding: 0;
    background-image: radial-gradient(circle, #36333c 1px, transparent 1px);
    background-size: 18px 19px; /* розмір кожної точки */
    background-position: center;
    background-color: #000; /* колір фону */
}
#notificationContainer {
    background-color: #212529;
    box-shadow: 16px 16px 10px rgb(0, 0, 0);
    color: #818589;
}
.form-control {
    background-color: #020208;
}


            `;
            styleElement.innerHTML = darkModeCSS;
        }
    }

    // Викликати функцію для початкового встановлення стилів
    const initialTheme = themeSwitch.checked ? 'dark' : 'light';
    updateStyles(initialTheme);

    themeSwitch.addEventListener('change', function () {
        // Змінює значення атрибута data-bs-theme на основі стану чекбокса
        const selectedTheme = themeSwitch.checked ? 'dark' : 'light';

        // Зберігати вибір теми в локальному сховищі
        saveTheme();

        // Встановити тему
        document.documentElement.setAttribute('data-bs-theme', selectedTheme);

        // Додати або видалити CSS правила в залежності від теми
        updateStyles(selectedTheme);
    });
    document.documentElement.style.display = 'block';
});


