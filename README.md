# DriveDirectory - Каталог премиальных автомобилей

## Установка и запуск

### Требования
- Современный веб-браузер (Chrome, Firefox, Safari, Edge)
- Веб-сервер для локального запуска

### Способы запуска:

#### 1. Python (если установлен)
```bash
cd DriveDirectory
python -m http.server 8000
```
Откройте: http://localhost:8000

#### 2. Node.js
```bash
npm install -g http-server
cd DriveDirectory
http-server
```

#### 3. VS Code Live Server
1. Установите расширение "Live Server"
2. Откройте папку проекта в VS Code
3. Правый клик на index.html → "Open with Live Server"

#### 4. Простой запуск (может не работать со всеми функциями)
Откройте файл index.html напрямую в браузере

### Структура проекта
```
DriveDirectory/
├── index.html          # Главная страница
├── images/            # Изображения автомобилей
└── README.md          # Этот файл
```

### Внешние зависимости (загружаются автоматически)
- Bootstrap 5.3.0
- Font Awesome 6.0.0
- Google Fonts (Montserrat, Roboto)

Все стили и скрипты подключены через CDN, дополнительная установка не требуется.