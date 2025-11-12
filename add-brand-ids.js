// Скрипт для добавления ID ко всем секциям брендов

const brandNames = ['BMW', 'Mercedes', 'Audi', 'Porsche', 'Dodge', 'Chevrolet', 'Ford', 'Cadillac', 'Lamborghini', 'RAM'];

function addBrandIds() {
    brandNames.forEach(brand => {
        const section = document.querySelector(`[data-brand="${brand}"]`);
        if (section) {
            section.id = `brand-${brand}`;
        }
    });
}

document.addEventListener('DOMContentLoaded', addBrandIds);