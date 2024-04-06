fetch('/your-endpoint')
  .then(response => {
    if (!response.ok) {
      throw new Error('Запит заборонено (403)');
    }
    return response.json();
  })
  .then(data => {
    // Обробка отриманих даних
  })
  .catch(error => {
    // Обробка помилки 403
    console.error(error);

    // Виведення фото для помилки 403
    const imageElement = document.createElement('img');
    imageElement.src = 'path/to/403-image.jpg'; // Шлях до вашого зображення для помилки 403
    document.body.appendChild(imageElement);
  });
