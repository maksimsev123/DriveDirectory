// Система аутентификации
class AuthSystem {
    constructor() {
        this.users = JSON.parse(localStorage.getItem('driveDirectoryUsers')) || {
            'admin': { password: 'admin123', favorites: [] }
        };
        this.currentUser = localStorage.getItem('currentUser') || null;
        this.init();
    }

    init() {
        this.updateUI();
        this.setupEventListeners();
    }

    setupEventListeners() {
        // Обработчики для форм
        document.getElementById('loginForm')?.addEventListener('submit', (e) => {
            e.preventDefault();
            this.login();
        });

        document.getElementById('registerForm')?.addEventListener('submit', (e) => {
            e.preventDefault();
            this.register();
        });

        // Кнопка выхода
        document.getElementById('logoutBtn')?.addEventListener('click', () => {
            this.logout();
        });
    }

    login() {
        const username = document.getElementById('loginUsername').value;
        const password = document.getElementById('loginPassword').value;

        if (this.users[username] && this.users[username].password === password) {
            this.currentUser = username;
            localStorage.setItem('currentUser', username);
            this.updateUI();
            this.closeModal('loginModal');
            this.showNotification('Вход выполнен успешно!', 'success');
            this.loadUserFavorites();
        } else {
            this.showNotification('Неверный логин или пароль', 'danger');
        }
    }

    register() {
        const username = document.getElementById('registerUsername').value;
        const password = document.getElementById('registerPassword').value;
        const confirmPassword = document.getElementById('confirmPassword').value;

        if (password !== confirmPassword) {
            this.showNotification('Пароли не совпадают', 'danger');
            return;
        }

        if (this.users[username]) {
            this.showNotification('Пользователь уже существует', 'danger');
            return;
        }

        this.users[username] = { password, favorites: [] };
        localStorage.setItem('driveDirectoryUsers', JSON.stringify(this.users));
        
        this.currentUser = username;
        localStorage.setItem('currentUser', username);
        
        this.updateUI();
        this.closeModal('registerModal');
        this.showNotification('Регистрация прошла успешно!', 'success');
        this.loadUserFavorites();
    }

    logout() {
        this.currentUser = null;
        localStorage.removeItem('currentUser');
        this.updateUI();
        this.showNotification('Вы вышли из системы', 'info');
        // Очищаем избранное при выходе
        favorites = [];
        updateFavoritesBadge();
    }

    updateUI() {
        const authButtons = document.getElementById('authButtons');
        const userInfo = document.getElementById('userInfo');

        if (this.currentUser) {
            authButtons.style.display = 'none';
            userInfo.style.display = 'block';
            document.getElementById('currentUsername').textContent = this.currentUser;
        } else {
            authButtons.style.display = 'block';
            userInfo.style.display = 'none';
        }
    }

    loadUserFavorites() {
        if (this.currentUser && this.users[this.currentUser]) {
            favorites = this.users[this.currentUser].favorites || [];
            updateFavoritesBadge();
            
            // Обновляем кнопки избранного
            document.querySelectorAll('.btn-favorite').forEach(btn => {
                const onclick = btn.getAttribute('onclick');
                if (onclick) {
                    const carId = onclick.match(/'([^']+)'/)[1];
                    if (favorites.includes(carId)) {
                        btn.classList.add('active');
                        btn.innerHTML = '<i class="fas fa-heart"></i>';
                    } else {
                        btn.classList.remove('active');
                        btn.innerHTML = '<i class="far fa-heart"></i>';
                    }
                }
            });
        }
    }

    saveFavorites() {
        if (this.currentUser && this.users[this.currentUser]) {
            this.users[this.currentUser].favorites = favorites;
            localStorage.setItem('driveDirectoryUsers', JSON.stringify(this.users));
        }
    }

    closeModal(modalId) {
        const modal = bootstrap.Modal.getInstance(document.getElementById(modalId));
        if (modal) modal.hide();
    }

    showNotification(message, type) {
        const alertDiv = document.createElement('div');
        alertDiv.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
        alertDiv.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
        alertDiv.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        document.body.appendChild(alertDiv);
        
        setTimeout(() => {
            if (alertDiv.parentNode) {
                alertDiv.remove();
            }
        }, 3000);
    }
}

// Инициализация системы аутентификации
let authSystem;
document.addEventListener('DOMContentLoaded', () => {
    authSystem = new AuthSystem();
});