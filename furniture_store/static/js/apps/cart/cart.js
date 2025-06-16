document.addEventListener('DOMContentLoaded', function () {
    // Обновление количества товара
    document.querySelectorAll('.quantity-btn').forEach(button => {
        button.addEventListener('click', function () {
            const action = this.dataset.action;
            const input = this.closest('.quantity-control').querySelector('.quantity-input');
            let value = parseInt(input.value);

            if (action === 'increase') {
                value += 1;
            } else if (action === 'decrease' && value > 1) {
                value -= 1;
            }

            input.value = value;

            // Отправка запроса на обновление количества
            const itemId = this.closest('.cart-item').dataset.itemId;
            updateCartItem(itemId, value);
        });
    });

    // Ручное изменение количества
    document.querySelectorAll('.quantity-input').forEach(input => {
        input.addEventListener('change', function () {
            const maxStock = parseInt(this.dataset.maxStock) || 99;
            let value = parseInt(this.value);

            if (isNaN(value) || value < 1) value = 1;
            if (value > maxStock) {
                value = maxStock;
                this.value = maxStock;
                alert(`Максимальное количество: ${maxStock}`);
            }

            const itemId = this.closest('.cart-item').dataset.itemId;
            updateCartItem(itemId, value);
        });
    });

    // Удаление товара из корзины
    document.querySelectorAll('.btn-remove').forEach(button => {
        button.addEventListener('click', function () {
            const itemId = this.closest('.cart-item').dataset.itemId;
            removeCartItem(itemId);
        });
    });

    // Функция обновления количества товара
    function updateCartItem(itemId, quantity) {
        fetch(`/cart/update/${itemId}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: `quantity=${quantity}`
        })
            .then(response => {
                if (response.ok) {
                    location.reload();
                } else {
                    alert('Ошибка при обновлении корзины');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Произошла ошибка при обновлении корзины');
            });
    }

    // Функция удаления товара из корзины
    function removeCartItem(itemId) {
        fetch(`/cart/remove/${itemId}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': getCookie('csrftoken')
            }
        })
            .then(response => {
                if (response.ok) {
                    location.reload();
                } else {
                    alert('Ошибка при удалении товара');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Произошла ошибка при удалении товара');
            });
    }

    // Функция получения CSRF токена
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});