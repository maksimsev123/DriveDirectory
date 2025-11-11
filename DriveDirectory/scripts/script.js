// scripts/script.js

// Функция для переключения фото в галерее
function initCarGallery() {
    const thumbs = document.querySelectorAll('.thumb');

    thumbs.forEach(thumb => {
        thumb.addEventListener('click', function() {
            // Убираем активный класс у всех миниатюр
            thumbs.forEach(t => t.classList.remove('active'));

            // Добавляем активный класс текущей миниатюре
            this.classList.add('active');

            // Меняем главное фото
            const mainPhoto = this.closest('.car-gallery').querySelector('.main-photo');
            const fullSizeImage = this.getAttribute('data-full');
            mainPhoto.src = fullSizeImage;
            mainPhoto.alt = this.alt;
        });
    });
}

// Плавная прокрутка для навигации
function initSmoothScroll() {
    const navLinks = document.querySelectorAll('a[href^="#"]');

    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();

            const targetId = this.getAttribute('href');
            if (targetId === '#') return;

            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                const offsetTop = targetElement.offsetTop - 80;

                window.scrollTo({
                    top: offsetTop,
                    behavior: 'smooth'
                });
            }
        });
    });
}

// Анимация появления элементов при скролле
function initScrollAnimations() {
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, { threshold: 0.1 });

    // Наблюдаем за карточками автомобилей
    const carCards = document.querySelectorAll('.car-card');
    carCards.forEach(card => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(30px)';
        card.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(card);
    });

    // Наблюдаем за элементами статистики
    const statItems = document.querySelectorAll('.stat-item');
    statItems.forEach(item => {
        item.style.opacity = '0';
        item.style.transform = 'translateY(30px)';
        item.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(item);
    });
}

// Загрузка автомобилей из базы данных
async function loadCars() {
    try {
        const response = await fetch('/api/cars');
        const cars = await response.json();
        displayCars(cars);
    } catch (error) {
        console.error('Error loading cars:', error);
        // Fallback: показываем статические данные если API недоступно
        displayStaticCars();
    }
}

// Отображение автомобилей на странице
function displayCars(cars) {
    const container = document.getElementById('cars-container');
    if (!container) return;

    container.innerHTML = cars.map(car => `
        <div class="col-md-6 col-lg-4 mb-4">
            <div class="car-card card h-100">
<img src="${car.images && car.images.length > 0 ? car.images[0] : 'images/placeholder.jpg'}"
                     class="card-img-top"
                     alt="${car.brand} ${car.model}"
                     onerror="this.src='images/placeholder.jpg'">
                <div class="card-body">
                    <h5 class="card-title">${car.brand} ${car.model}</h5>
                    <p class="card-text">
                        <strong>Год:</strong> ${car.year}<br>
                        <strong>Цена:</strong> $${car.price ? car.price.toLocaleString() : 'По запросу'}
                    </p>
                    <p class="card-text">${car.description}</p>
                </div>
                <div class="card-footer">
                    <button class="btn btn-primary w-100" onclick="showContactForm(${car.id})">
                        Запросить информацию
                    </button>
                </div>
            </div>
        </div>
    `).join('');

    // Переинициализируем анимации для новых элементов
    initScrollAnimations();
}

// Fallback статические данные
function displayStaticCars() {
    const container = document.getElementById('cars-container');
    if (!container) return;

    container.innerHTML = `
        <div class="col-md-6 col-lg-4 mb-4">
            <div class="car-card card h-100">
                <img src="images/cars/camry.jpg" class="card-img-top" alt="Toyota Camry">
                <div class="card-body">
                    <h5 class="card-title">Toyota Camry</h5>
                    <p class="card-text">
                        <strong>Год:</strong> 2023<br>
                        <strong>Цена:</strong> $25,000
                    </p>
                    <p class="card-text">Комфортный седан бизнес-класса</p>
                </div>
                <div class="card-footer">
                    <button class="btn btn-primary w-100" onclick="showContactForm(1)">
                        Запросить информацию
                    </button>
                </div>
            </div>
        </div>
        <div class="col-md-6 col-lg-4 mb-4">
            <div class="car-card card h-100">
                <img src="images/cars/x5.jpg" class="card-img-top" alt="BMW X5">
                <div class="card-body">
                    <h5 class="card-title">BMW X5</h5>
                    <p class="card-text">
                        <strong>Год:</strong> 2024<br>
                        <strong>Цена:</strong> $65,000
                    </p>
                    <p class="card-text">Премиальный внедорожник</p>
                </div>
                <div class="card-footer">
                    <button class="btn btn-primary w-100" onclick="showContactForm(2)">
                        Запросить информацию
                    </button>
                </div>
            </div>
        </div>
    `;
}

// Поиск автомобилей
async function searchCars(query) {
    if (!query.trim()) {
        loadCars();
        return;
    }

    try {
        const response = await fetch(`/api/search?q=${encodeURIComponent(query)}`);
        const cars = await response.json();
        displayCars(cars);
    } catch (error) {
        console.error('Error searching cars:', error);
    }
}

// Показать форму контакта
function showContactForm(carId = null) {
    const carModel = carId ? ` для автомобиля #${carId}` : '';

    // Создаем модальное окно формы
    const modalHTML = `
        <div class="modal fade" id="contactModal" tabindex="-1">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">Запрос информации${carModel}</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body">
                        <form id="contactForm">
                            <input type="hidden" id="carId" value="${carId || ''}">
                            <div class="mb-3">
                                <label for="name" class="form-label">Имя</label>
                                <input type="text" class="form-control" id="name" required>
                            </div>
                            <div class="mb-3">
                                <label for="email" class="form-label">Email</label>
                                <input type="email" class="form-control" id="email" required>
                            </div>
                            <div class="mb-3">
                                <label for="phone" class="form-label">Телефон</label>
                                <input type="tel" class="form-control" id="phone">
                            </div>
                            <div class="mb-3">
                                <label for="message" class="form-label">Сообщение</label>
                                <textarea class="form-control" id="message" rows="4" required></textarea>
                            </div>
                        </form>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Отмена</button>
                        <button type="button" class="btn btn-primary" onclick="submitContactForm()">Отправить</button>
                    </div>
                </div>
            </div>
        </div>
    `;

    // Добавляем модальное окно в body если его нет
    if (!document.getElementById('contactModal')) {
        document.body.insertAdjacentHTML('beforeend', modalHTML);
    }

    // Показываем модальное окно
    const modal = new bootstrap.Modal(document.getElementById('contactModal'));
    modal.show();
}

// Отправка формы контакта
async function submitContactForm() {
    const formData = {
        name: document.getElementById('name').value,
        email: document.getElementById('email').value,
        phone: document.getElementById('phone').value,
        message: document.getElementById('message').value,
        car_id: document.getElementById('carId').value || null
    };

    // Валидация
    if (!formData.name || !formData.email || !formData.message) {
        alert('Пожалуйста, заполните все обязательные поля');
        return;
    }

    try {
        const response = await fetch('/api/contact', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData)
        });

        if (response.ok) {
            alert('Ваше сообщение отправлено! Мы свяжемся с вами в ближайшее время.');
            const modal = bootstrap.Modal.getInstance(document.getElementById('contactModal'));
            modal.hide();
        } else {
            throw new Error('Ошибка отправки');
        }
    } catch (error) {
        console.error('Error submitting form:', error);
        alert('Произошла ошибка при отправке формы. Пожалуйста, попробуйте еще раз.');
    }
}

// Анимация счетчиков статистики
function animateCounters() {
    const counters = document.querySelectorAll('.stat-item h3');
    const speed = 200;

    counters.forEach(counter => {
        const target = +counter.getAttribute('data-target');
        const count = +counter.innerText;
        const increment = target / speed;

        if (count < target) {
            counter.innerText = Math.ceil(count + increment);
            setTimeout(() => animateCounters(), 1);
        } else {
            counter.innerText = target;
        }
    });
}

// 1. Функция для фильтрации автомобилей по брендам
function initBrandFilter() {
    const brandButtons = document.querySelectorAll('.brand-logo');
    
    brandButtons.forEach(button => {
        button.addEventListener('click', async function() {
            const brandName = this.querySelector('span').textContent;
            
            // Убираем активный класс у всех кнопок
            brandButtons.forEach(btn => btn.classList.remove('active'));
            // Добавляем активный класс текущей кнопке
            this.classList.add('active');
            
            try {
                const response = await fetch(`/api/cars/brand/${encodeURIComponent(brandName)}`);
                const cars = await response.json();
                updateCarsDisplay(cars, brandName);
            } catch (error) {
                console.error('Error filtering by brand:', error);
            }
        });
    });
}

// 2. Функция для обновления отображения автомобилей с анимацией
function updateCarsDisplay(cars, brandName = null) {
    const catalogSection = document.getElementById('catalog');
    const existingBrandSections = catalogSection.querySelectorAll('.brand-section');
    
    // Удаляем существующие секции брендов
    existingBrandSections.forEach(section => section.remove());
    
    if (cars.length === 0) {
        catalogSection.innerHTML += `
            <div class="text-center py-5">
                <h4>Автомобили не найдены</h4>
                <p>Попробуйте выбрать другой бренд</p>
            </div>
        `;
        return;
    }
    
    // Группируем автомобили по брендам
    const carsByBrand = {};
    cars.forEach(car => {
        if (!carsByBrand[car.brand]) {
            carsByBrand[car.brand] = [];
        }
        carsByBrand[car.brand].push(car);
    });
    
    // Создаем секции для каждого бренда
    Object.keys(carsByBrand).forEach(brand => {
        const brandCars = carsByBrand[brand];
        const brandSection = document.createElement('div');
        brandSection.className = 'brand-section mb-5';
        brandSection.innerHTML = `
            <h3 class="brand-title mb-4">${brand}</h3>
            <div class="row g-4" id="cars-${brand.toLowerCase()}">
                ${brandCars.map(car => `
                    <div class="col-md-6 col-lg-4">
                        <div class="card h-100 car-card" data-bs-toggle="modal" data-bs-target="#carModal${car.id}">
                            <div class="card-image">
                                <img src="${car.images && car.images.length > 0 ? car.images[0] : 'images/placeholder.jpg'}" 
                                     class="card-img-top" 
                                     alt="${car.brand} ${car.model}"
                                     onerror="this.src='images/placeholder.jpg'">
                                <div class="card-overlay">
                                    <span class="price">${formatPrice(car.price)}</span>
                                </div>
                            </div>
                            <div class="card-body">
                                <h5 class="card-title">${car.brand} ${car.model}</h5>
                                <div class="car-specs">
                                    <div class="spec-item">
                                        <i class="fas fa-tachometer-alt"></i>
                                        <span>${car.horsepower || 'N/A'} л.с.</span>
                                    </div>
                                    <div class="spec-item">
                                        <i class="fas fa-rocket"></i>
                                        <span>${car.acceleration || 'N/A'} с</span>
                                    </div>
                                    <div class="spec-item">
                                        <i class="fas fa-calendar-alt"></i>
                                        <span>${car.year}</span>
                                    </div>
                                </div>
                                <p class="card-text">${car.description || 'Описание временно недоступно'}</p>
                            </div>
                        </div>
                    </div>
                `).join('')}
            </div>
        `;
        catalogSection.appendChild(brandSection);
    });
    
    // Переинициализируем анимации
    initScrollAnimations();
    
    // Прокручиваем к каталогу если фильтровали
    if (brandName) {
        setTimeout(() => {
            catalogSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }, 300);
    }
}

// 3. Функция для управления избранными автомобилями
function initFavorites() {
    let favorites = JSON.parse(localStorage.getItem('favoriteCars')) || [];
    
    // Функция добавления/удаления из избранного
    window.toggleFavorite = function(carId, carData = null) {
        const index = favorites.findIndex(fav => fav.id === carId);
        
        if (index > -1) {
            // Удаляем из избранного
            favorites.splice(index, 1);
            updateFavoriteButton(carId, false);
        } else {
            // Добавляем в избранное
            if (carData) {
                favorites.push({
                    id: carId,
                    brand: carData.brand,
                    model: carData.model,
                    price: carData.price,
                    image: carData.images ? carData.images[0] : 'images/placeholder.jpg',
                    addedAt: new Date().toISOString()
                });
            } else {
                favorites.push({ id: carId, addedAt: new Date().toISOString() });
            }
            updateFavoriteButton(carId, true);
        }
        
        // Сохраняем в localStorage
        localStorage.setItem('favoriteCars', JSON.stringify(favorites));
        updateFavoritesBadge();
        
        // Показываем уведомление
        showNotification(
            index > -1 ? 'Удалено из избранного' : 'Добавлено в избранное',
            index > -1 ? 'warning' : 'success'
        );
    };
    
    // Функция обновления кнопки избранного
    function updateFavoriteButton(carId, isFavorite) {
        const buttons = document.querySelectorAll(`[onclick="toggleFavorite(${carId})"]`);
        buttons.forEach(button => {
            if (isFavorite) {
                button.innerHTML = '<i class="fas fa-heart"></i> В избранном';
                button.classList.remove('btn-outline-danger');
                button.classList.add('btn-danger');
            } else {
                button.innerHTML = '<i class="far fa-heart"></i> В избранное';
                button.classList.remove('btn-danger');
                button.classList.add('btn-outline-danger');
            }
        });
    }
    
    // Функция обновления бейджа с количеством избранных
    function updateFavoritesBadge() {
        const badge = document.getElementById('favoritesBadge');
        if (badge) {
            badge.textContent = favorites.length;
            badge.style.display = favorites.length > 0 ? 'inline-block' : 'none';
        }
    }
    
    // Функция показа избранных автомобилей
    window.showFavorites = function() {
        if (favorites.length === 0) {
            showNotification('У вас пока нет избранных автомобилей', 'info');
            return;
        }
        
        const favoriteCarsList = favorites.map(fav => `
            <div class="col-md-6 col-lg-4 mb-3">
                <div class="card">
                    <img src="${fav.image}" class="card-img-top" alt="${fav.brand} ${fav.model}">
                    <div class="card-body">
                        <h6>${fav.brand} ${fav.model}</h6>
                        <p class="mb-1">${formatPrice(fav.price)}</p>
                        <button class="btn btn-sm btn-outline-danger" onclick="toggleFavorite(${fav.id})">
                            <i class="fas fa-trash"></i> Удалить
                        </button>
                    </div>
                </div>
            </div>
        `).join('');
        
        // Создаем модальное окно избранного
        const modalHTML = `
            <div class="modal fade" id="favoritesModal" tabindex="-1">
                <div class="modal-dialog modal-lg">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title">Избранные автомобили (${favorites.length})</h5>
                            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                        </div>
                        <div class="modal-body">
                            <div class="row">
                                ${favoriteCarsList}
                            </div>
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Закрыть</button>
                            <button type="button" class="btn btn-danger" onclick="clearAllFavorites()">
                                Очистить все
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        // Добавляем модальное окно если его нет
        if (!document.getElementById('favoritesModal')) {
            document.body.insertAdjacentHTML('beforeend', modalHTML);
        } else {
            document.getElementById('favoritesModal').innerHTML = modalHTML;
        }
        
        // Показываем модальное окно
        const modal = new bootstrap.Modal(document.getElementById('favoritesModal'));
        modal.show();
    };
    
    // Функция очистки всех избранных
    window.clearAllFavorites = function() {
        if (confirm('Вы уверены, что хотите очистить все избранные автомобили?')) {
            favorites = [];
            localStorage.setItem('favoriteCars', JSON.stringify(favorites));
            updateFavoritesBadge();
            
            const modal = bootstrap.Modal.getInstance(document.getElementById('favoritesModal'));
            if (modal) modal.hide();
            
            showNotification('Все автомобили удалены из избранного', 'info');
        }
    };
    
    // Инициализация бейджа при загрузке
    updateFavoritesBadge();
}

// Вспомогательная функция для показа уведомлений
function showNotification(message, type = 'info') {
    const alertClass = {
        'success': 'alert-success',
        'warning': 'alert-warning',
        'error': 'alert-danger',
        'info': 'alert-info'
    }[type] || 'alert-info';
    
    const notification = document.createElement('div');
    notification.className = `alert ${alertClass} alert-dismissible fade show position-fixed`;
    notification.style.cssText = `
        top: 20px;
        right: 20px;
        z-index: 9999;
        min-width: 300px;
    `;
    notification.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(notification);
    
    // Автоматическое скрытие через 3 секунды
    setTimeout(() => {
        if (notification.parentNode) {
            notification.remove();
        }
    }, 3000);
}

// Функция для форматирования цены
function formatPrice(price) {
    if (!price) return 'Цена по запросу';
    return new Intl.NumberFormat('ru-RU', {
        minimumFractionDigits: 0
    }).format(price) + ' ₽';
}

// Инициализация при загрузке страницы
document.addEventListener('DOMContentLoaded', function() {
    initCarGallery();
    initSmoothScroll();
    initScrollAnimations();
    initBrandFilter();
    initFavorites();
    loadCars();

    // Добавляем кнопку избранного в навигацию
    const navbar = document.querySelector('.navbar .navbar-nav');
    if (navbar) {
        const favoritesItem = document.createElement('li');
        favoritesItem.className = 'nav-item';
        favoritesItem.innerHTML = `
            <a class="nav-link" href="#" onclick="showFavorites(); return false;">
                <i class="fas fa-heart"></i> Избранное
                <span id="favoritesBadge" class="badge bg-danger ms-1" style="display: none;">0</span>
            </a>
        `;
        navbar.appendChild(favoritesItem);
    }

    // Инициализация поиска
    const searchInput = document.getElementById('searchInput');
    if (searchInput) {
        searchInput.addEventListener('input', function() {
            searchCars(this.value);
        });
    }

    // Переинициализация галереи при открытии модального окна
    const modals = document.querySelectorAll('.modal');
    modals.forEach(modal => {
        modal.addEventListener('show.bs.modal', function() {
            setTimeout(initCarGallery, 100);
        });
    });

    // Изменение стиля навигации при скролле
    window.addEventListener('scroll', function() {
        const navbar = document.querySelector('.navbar');
        if (window.scrollY > 100) {
            navbar.style.background = 'rgba(44, 62, 80, 0.98)';
            navbar.style.boxShadow = '0 2px 10px rgba(0,0,0,0.1)';
        } else {
            navbar.style.background = 'rgba(44, 62, 80, 0.95)';
            navbar.style.boxShadow = 'none';
        }
    });

    // Обработка ошибок загрузки изображений
    const images = document.querySelectorAll('img');
    images.forEach(img => {
        img.addEventListener('error', function() {
            this.src = 'images/placeholder.jpg';
            this.alt = 'Изображение временно недоступно';
        });
    });
});

// Инициализация анимации счетчиков при появлении в viewport
const statsSection = document.querySelector('.hero-stats');
if (statsSection) {
    const statsObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                animateCounters();
                statsObserver.unobserve(entry.target);
            }
        });
    }, { threshold: 0.5 });

    statsObserver.observe(statsSection);
}