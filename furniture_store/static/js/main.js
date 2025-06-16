// Адаптивное меню
function initMobileMenu() {
    const toggle = document.querySelector('.mobile-menu-toggle');
    if (!toggle) return;

    toggle.addEventListener('click', function() {
        this.classList.toggle('active');
        document.querySelector('.header__nav').classList.toggle('open');
    });
}


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

// Функции для обновления счетчиков
function updateCartCount(count) {
    const cartCountElement = document.getElementById('cart-count');
    if (cartCountElement) {
        cartCountElement.textContent = count > 0 ? count : '';
        cartCountElement.style.display = count > 0 ? 'block' : 'none';
    }
}

function updateWishlistCount(count) {
    const wishlistCountElement = document.getElementById('wishlist-count');
    if (wishlistCountElement) {
        wishlistCountElement.textContent = count > 0 ? count : '';
        wishlistCountElement.style.display = count > 0 ? 'block' : 'none';
    }
}

// Инициализация всех компонентов
window.addEventListener('DOMContentLoaded', () => {
    initMobileMenu();

    // Показываем/скрываем счетчики при загрузке
    const cartCount = document.getElementById('cart-count');
    const wishlistCount = document.getElementById('wishlist-count');

    if (cartCount) {
        cartCount.style.display = cartCount.textContent.trim() !== '' ? 'block' : 'none';
    }

    if (wishlistCount) {
        wishlistCount.style.display = wishlistCount.textContent.trim() !== '' ? 'block' : 'none';
    }
});