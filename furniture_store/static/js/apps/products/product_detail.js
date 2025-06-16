document.addEventListener('DOMContentLoaded', function () {
    // Общие функции
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

    function updateCartCount(count) {
        const cartCountElement = document.getElementById('cart-count');
        if (cartCountElement) {
            cartCountElement.textContent = count;
        }
    }

    // Кнопка добавления в корзину
    const addToCartBtn = document.getElementById('add-to-cart-btn');
    if (addToCartBtn) {
        addToCartBtn.addEventListener('click', function () {
            const variantId = this.getAttribute('data-variant-id');

            if (!variantId) {
                alert('Выберите вариант товара');
                return;
            }

            fetch(`/cart/add/${variantId}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({})
            })
                .then(response => {
                    const contentType = response.headers.get('content-type');
                    if (contentType && contentType.includes('application/json')) {
                        return response.json();
                    } else if (response.redirected) {
                        window.location.href = response.url;
                        return Promise.reject('redirected');
                    } else {
                        return response.text().then(text => {
                            throw new Error(`Invalid response: ${text}`);
                        });
                    }
                })
                .then(data => {
                    if (data && data.success) {
                        updateCartCount(data.cart_item_count);

                        const notification = document.createElement('div');
                        notification.className = 'notification success';
                        notification.textContent = data.message;
                        document.body.appendChild(notification);

                        setTimeout(() => {
                            notification.remove();
                        }, 3000);
                    }
                })
                .catch(error => {
                    if (error !== 'redirected') {
                        console.error('Error:', error);
                        alert('Произошла ошибка. Пожалуйста, войдите в систему.');
                    }
                });
        });
    }


    // Кнопка избранного
    // Кнопка избранного - обновленная версия
    const addToFavoritesBtn = document.getElementById('add-to-favorites-btn');
    if (addToFavoritesBtn) {
        addToFavoritesBtn.addEventListener('click', function () {
            const productId = this.getAttribute('data-product-id');

            fetch(`/users/favorite/${productId}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({})
            })
                .then(response => {
                    const contentType = response.headers.get('content-type');
                    if (contentType && contentType.includes('application/json')) {
                        return response.json();
                    } else if (response.redirected) {
                        window.location.href = response.url;
                        return Promise.reject('redirected');
                    } else {
                        return response.text().then(text => {
                            throw new Error(`Invalid response: ${text}`);
                        });
                    }
                })
                .then(data => {
                    if (data && data.success) {
                        this.classList.toggle('active', data.is_favorite);
                        updateWishlistCount(data.favorites_count);

                        const notification = document.createElement('div');
                        notification.className = 'notification success';
                        notification.textContent = data.message;
                        document.body.appendChild(notification);

                        setTimeout(() => {
                            notification.remove();
                        }, 3000);
                    }
                })
                .catch(error => {
                    if (error !== 'redirected') {
                        console.error('Error:', error);
                        alert('Произошла ошибка. Пожалуйста, войдите в систему.');
                    }
                });
        });
    }
});
