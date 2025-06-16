document.addEventListener('DOMContentLoaded', function() {
    const variantOptions = document.querySelectorAll('.variant-option');
    const selectedVariantInfo = document.getElementById('selected-variant-info');
    const selectedVariantSku = document.getElementById('selected-variant-sku');
    const selectedVariantPrice = document.getElementById('selected-variant-price');
    const selectedVariantStock = document.getElementById('selected-variant-stock');
    const mainImage = document.getElementById('main-image');
    const thumbnails = document.querySelectorAll('.thumbnail');
    const addToCartBtn = document.getElementById('add-to-cart-btn');

    variantOptions.forEach(option => {
        option.addEventListener('click', function() {
            // Обновляем классы выбранного варианта
            variantOptions.forEach(opt => opt.classList.remove('selected'));
            this.classList.add('selected');

            // Получаем данные варианта
            const variantId = this.getAttribute('data-variant-id');
            const sku = this.getAttribute('data-variant-sku');
            const price = this.getAttribute('data-variant-price');
            const stock = this.getAttribute('data-variant-stock');
            const images = this.getAttribute('data-variant-images')?.split(',') || [];

            // Обновляем информацию о варианте
            if (selectedVariantInfo) {
                let infoText = 'Выбран: ';
                const labels = this.querySelectorAll('.variant-option-label');
                labels.forEach((label, index) => {
                    if (index > 0) infoText += ', ';
                    infoText += label.textContent;
                });
                selectedVariantInfo.textContent = infoText;
            }

            if (selectedVariantSku) selectedVariantSku.textContent = sku;
            if (selectedVariantPrice) selectedVariantPrice.textContent = `${price} ₽`;
            if (selectedVariantStock) {
                selectedVariantStock.textContent = stock > 0 ?
                    `В наличии (${stock} шт.)` : 'Нет в наличии';
            }

            // Обновляем главное изображение
            if (images.length > 0 && mainImage) {
                mainImage.src = images[0];
            }

            // Обновляем активные миниатюры
            thumbnails.forEach(thumb => {
                thumb.classList.remove('active');
                if (thumb.getAttribute('data-variant-id') === variantId) {
                    thumb.classList.add('active');
                }
            });

            // Обновляем кнопку корзины
            if (addToCartBtn) {
                addToCartBtn.setAttribute('data-variant-id', variantId);
                addToCartBtn.disabled = stock <= 0;
            }
        });
    });

    // Инициализация галереи
    thumbnails.forEach(thumb => {
        thumb.addEventListener('click', function() {
            const imageSrc = this.getAttribute('data-image-src');
            if (imageSrc && mainImage) {
                mainImage.src = imageSrc;
            }
        });
    });
});