document.addEventListener('DOMContentLoaded', function() {
    // Находим поле промпта в админке
    const promptField = document.querySelector('.field-ai_prompt');

    if (promptField) {
        // Создаем кнопку
        const btn = document.createElement('button');
        btn.type = 'button';
        btn.innerText = '✨ Обработать фото через AI';
        btn.style = 'margin-top: 10px; padding: 10px; background: #417690; color: white; border: none; border-radius: 4px; cursor: pointer;';

        promptField.appendChild(btn);

        btn.onclick = function() {
            const productId = window.location.pathname.split('/')[4]; // Получаем ID товара из URL
            if (!confirm('Отправить фото на обработку? Это может занять время.')) return;

            btn.innerText = '⏳ Обработка...';
            btn.disabled = true;

            fetch(`/process-ai/${productId}/`, { method: 'POST' })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        alert('Готово! Страница будет перезагружена.');
                        location.reload();
                    } else {
                        alert('Ошибка: ' + data.error);
                    }
                })
                .finally(() => {
                    btn.innerText = '✨ Обработать фото через AI';
                    btn.disabled = false;
                });
        };
    }
});