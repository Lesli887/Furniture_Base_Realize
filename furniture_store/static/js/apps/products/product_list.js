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

    // Функция для обновления параметров URL
    function updateUrlParams(form) {
        const params = new URLSearchParams();
        const formData = new FormData(form);

        for (const [key, value] of formData.entries()) {
            if (value && value !== 'all') {
                params.set(key, value);
            }
        }

        return params.toString();
    }

    // Обработка изменения фильтров
    const filterForm = document.getElementById('filter-form');
    const filterSelects = filterForm.querySelectorAll('select');

    filterSelects.forEach(select => {
        select.addEventListener('change', function () {
            // Сохраняем текущую страницу
            const currentPage = new URLSearchParams(window.location.search).get('page');
            const params = updateUrlParams(filterForm);

            // Собираем новый URL
            let newUrl = `${window.location.pathname}?${params}`;
            if (currentPage && params) {
                newUrl += `&page=${currentPage}`;
            } else if (currentPage) {
                newUrl += `?page=${currentPage}`;
            }

            // Переходим по новому URL
            window.location.href = newUrl;
        });
    });

    // Функция для сохранения параметров фильтрации в URL пагинации
    document.querySelectorAll('.pagination a').forEach(link => {
        const url = new URL(link.href);
        const currentParams = new URLSearchParams(window.location.search);

        // Копируем текущие параметры фильтрации
        ['category', 'collection', 'sort', 'stock'].forEach(param => {
            const value = currentParams.get(param);
            if (value) {
                url.searchParams.set(param, value);
            }
        });

        link.href = url.toString();
    });

    // Обработка добавления в корзину
    document.querySelectorAll('.product-card .btn-add-to-cart').forEach(button => {
        button.addEventListener('click', function (e) {
            e.preventDefault();
            const variantId = this.getAttribute('data-variant-id');

            if (!variantId) {
                alert('Этот товар недоступен для заказа');
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
                    // Проверяем тип ответа
                    const contentType = response.headers.get('content-type');
                    if (contentType && contentType.includes('application/json')) {
                        return response.json();
                    } else if (response.redirected) {
                        window.location.href = response.url; // Перенаправляем если требуется авторизация
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
    });

    // Обработка избранного - обновленная версия
    document.querySelectorAll('.product-card .btn-wishlist').forEach(button => {
        button.addEventListener('click', function (e) {
            e.preventDefault();
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
    });
});