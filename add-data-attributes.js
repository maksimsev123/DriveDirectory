// Скрипт для добавления data-атрибутов ко всем карточкам автомобилей

// Данные об автомобилях
const carData = {
    'bmw-m5-competition': { brand: 'BMW', model: 'M5 Competition', price: 12900000 },
    'bmw-x5-competition': { brand: 'BMW', model: 'X5 M Competition', price: 10200000 },
    'bmw-i7-xdrive60': { brand: 'BMW', model: 'i7 xDrive60', price: 9800000 },
    'mercedes-amg-g63': { brand: 'Mercedes', model: 'AMG G 63', price: 18500000 },
    'mercedes-s580': { brand: 'Mercedes', model: 'S 580', price: 11900000 },
    'mercedes-eqs580': { brand: 'Mercedes', model: 'EQS 580', price: 8900000 },
    'audi-rs6-avant': { brand: 'Audi', model: 'RS6 Avant', price: 11200000 },
    'audi-r8-v10-plus': { brand: 'Audi', model: 'R8 V10 Plus', price: 14500000 },
    'audi-etron-gt': { brand: 'Audi', model: 'e-tron GT', price: 9500000 },
    'porsche-911-turbo-s': { brand: 'Porsche', model: '911 Turbo S', price: 16500000 },
    'porsche-taycan-turbo': { brand: 'Porsche', model: 'Taycan Turbo', price: 12300000 },
    'porsche-cayenne-turbo-gt': { brand: 'Porsche', model: 'Cayenne Turbo GT', price: 13800000 },
    'dodge-challenger-hellcat': { brand: 'Dodge', model: 'Challenger SRT Hellcat', price: 8900000 },
    'dodge-charger-hellcat': { brand: 'Dodge', model: 'Charger SRT Hellcat', price: 9200000 },
    'dodge-viper-acr': { brand: 'Dodge', model: 'Viper ACR', price: 15000000 },
    'chevrolet-camaro-zl1': { brand: 'Chevrolet', model: 'Camaro ZL1', price: 7500000 },
    'chevrolet-corvette-stingray': { brand: 'Chevrolet', model: 'Corvette Stingray', price: 8200000 },
    'chevrolet-tahoe-high-country': { brand: 'Chevrolet', model: 'Tahoe High Country', price: 6800000 },
    'ford-mustang-gt': { brand: 'Ford', model: 'Mustang GT', price: 5900000 },
    'ford-f150-raptor': { brand: 'Ford', model: 'F-150 Raptor', price: 7200000 },
    'ford-explorer-st': { brand: 'Ford', model: 'Explorer ST', price: 6500000 },
    'cadillac-escalade-v': { brand: 'Cadillac', model: 'Escalade-V', price: 12500000 },
    'cadillac-xt5-sport': { brand: 'Cadillac', model: 'XT5 Sport', price: 5200000 },
    'cadillac-lyriq': { brand: 'Cadillac', model: 'Lyriq', price: 6800000 },
    'lamborghini-urus': { brand: 'Lamborghini', model: 'Urus', price: 22000000 },
    'lamborghini-revuelto': { brand: 'Lamborghini', model: 'Revuelto', price: 45000000 },
    'lamborghini-huracan-sto': { brand: 'Lamborghini', model: 'Huracán STO', price: 28500000 },
    'ram-1500-tungsten': { brand: 'RAM', model: '1500 Tungsten', price: 6200000 },
    'ram-1500-trx': { brand: 'RAM', model: '1500 TRX', price: 12500000 },
    'ram-1500-rho': { brand: 'RAM', model: '1500 RHO', price: 8900000 }
};

// Функция для добавления атрибутов
function addDataAttributes() {
    const carCards = document.querySelectorAll('.car-card');
    
    carCards.forEach(card => {
        // Ищем кнопку избранного для получения ID автомобиля
        const favoriteBtn = card.querySelector('.btn-favorite');
        if (favoriteBtn) {
            const onclick = favoriteBtn.getAttribute('onclick');
            const carId = onclick.match(/'([^']+)'/)[1];
            
            if (carData[carId]) {
                const data = carData[carId];
                card.setAttribute('data-brand', data.brand);
                card.setAttribute('data-model', data.model);
                card.setAttribute('data-price', data.price);
            }
        }
    });
    
    // Добавляем атрибуты к секциям брендов
    const brandSections = document.querySelectorAll('.brand-section');
    brandSections.forEach(section => {
        const title = section.querySelector('.brand-title').textContent.trim();
        section.setAttribute('data-brand', title);
    });
}

// Запускаем после загрузки DOM
document.addEventListener('DOMContentLoaded', addDataAttributes);