
document.addEventListener('DOMContentLoaded', function() {
    // Инициализация функционала блога
    initBlog();
});

function initBlog() {
    // Плавное раскрытие изображений в постах
    initImageExpansion();

    // Подсветка тегов при наведении
    initTagHover();

    // Инициализация кнопки "Наверх" для длинных постов
    initScrollToTop();
}

// Плавное раскрытие/скрытие изображений при клике
function initImageExpansion() {
    document.querySelectorAll('.post-image').forEach(image => {
        image.addEventListener('click', function() {
            this.classList.toggle('expanded');

            if (this.classList.contains('expanded')) {
                // Прокрутка к изображению при раскрытии
                this.scrollIntoView({behavior: 'smooth', block: 'center'});
            }
        });
    });
}

// Подсветка тегов при наведении
function initTagHover() {
    document.querySelectorAll('.tag').forEach(tag => {
        tag.addEventListener('mouseenter', function() {
            const relatedTags = document.querySelectorAll(`.tag[data-tag="${this.dataset.tag}"]`);
            relatedTags.forEach(t => t.classList.add('highlighted'));
        });

        tag.addEventListener('mouseleave', function() {
            const relatedTags = document.querySelectorAll(`.tag[data-tag="${this.dataset.tag}"]`);
            relatedTags.forEach(t => t.classList.remove('highlighted'));
        });
    });
}

// Кнопка "Наверх" для длинных постов
function initScrollToTop() {
    const scrollBtn = document.createElement('button');
    scrollBtn.className = 'scroll-to-top';
    scrollBtn.innerHTML = '↑ Наверх';
    scrollBtn.style.display = 'none';
    document.body.appendChild(scrollBtn);

    window.addEventListener('scroll', function() {
        scrollBtn.style.display = window.scrollY > 500 ? 'block' : 'none';
    });

    scrollBtn.addEventListener('click', function() {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });
}

// Инициализация поиска по блогу (если будет реализован)
function initBlogSearch() {
    const searchForm = document.querySelector('.blog-search-form');
    if (!searchForm) return;

    searchForm.addEventListener('submit', function(e) {
        e.preventDefault();
        const query = this.querySelector('input').value.trim();

        if (query.length > 2) {
            // Здесь будет логика поиска (AJAX или перенаправление)
            console.log('Поиск по блогу:', query);
        }
    });
}