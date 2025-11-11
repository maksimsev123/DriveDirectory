import sqlite3
import json
from datetime import datetime

class CarDatabase:
    def __init__(self, db_name='cars.db'):
        self.db_name = db_name
        self.init_database()
    
    def get_connection(self):
        return sqlite3.connect(self.db_name)
    
    def init_database(self):
        """Инициализация базы данных и создание таблиц"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Таблица брендов
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS brands (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name VARCHAR(50) NOT NULL UNIQUE,
                country VARCHAR(50),
                description TEXT,
                logo_url VARCHAR(255),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Таблица автомобилей
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS cars (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                brand_id INTEGER,
                model VARCHAR(100) NOT NULL,
                year INTEGER NOT NULL,
                price DECIMAL(12,2),
                engine_type VARCHAR(50),
                horsepower INTEGER,
                acceleration DECIMAL(4,1),
                top_speed INTEGER,
                fuel_consumption DECIMAL(4,1),
                transmission VARCHAR(50),
                drive_type VARCHAR(50),
                images TEXT,
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (brand_id) REFERENCES brands (id)
            )
        ''')
        
        # Таблица контактов
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS contacts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name VARCHAR(100) NOT NULL,
                email VARCHAR(100) NOT NULL,
                phone VARCHAR(20),
                message TEXT NOT NULL,
                car_id INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
        print("✅ База данных инициализирована")
    
    def add_brand(self, name, country=None, description=None, logo_url=None):
        """Добавление бренда"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO brands (name, country, description, logo_url)
                VALUES (?, ?, ?, ?)
            ''', (name, country, description, logo_url))
            conn.commit()
            print(f"✅ Добавлен бренд: {name}")
            return cursor.lastrowid
        except sqlite3.IntegrityError:
            # Бренд уже существует
            cursor.execute('SELECT id FROM brands WHERE name = ?', (name,))
            result = cursor.fetchone()
            return result[0] if result else None
        finally:
            conn.close()
    
    def add_car(self, brand_name, model, year, price=None, **kwargs):
        """Добавление автомобиля"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Получаем или создаем бренд
        brand_id = self.add_brand(brand_name)
        if not brand_id:
            conn.close()
            return None
        
        # Подготавливаем изображения как JSON
        images = json.dumps(kwargs.get('images', []))
        
        cursor.execute('''
            INSERT INTO cars (
                brand_id, model, year, price, engine_type, horsepower,
                acceleration, top_speed, fuel_consumption, transmission,
                drive_type, images, description
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            brand_id, model, year, price,
            kwargs.get('engine_type'),
            kwargs.get('horsepower'),
            kwargs.get('acceleration'),
            kwargs.get('top_speed'),
            kwargs.get('fuel_consumption'),
            kwargs.get('transmission'),
            kwargs.get('drive_type'),
            images,
            kwargs.get('description')
        ))
        
        conn.commit()
        car_id = cursor.lastrowid
        conn.close()
        print(f"✅ Добавлен автомобиль: {brand_name} {model}")
        return car_id
    
    def get_all_cars(self):
        """Получение всех автомобилей с информацией о брендах"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT 
                c.id, b.name as brand, c.model, c.year, c.price,
                c.engine_type, c.horsepower, c.acceleration, c.top_speed,
                c.fuel_consumption, c.transmission, c.drive_type,
                c.images, c.description
            FROM cars c
            JOIN brands b ON c.brand_id = b.id
            ORDER BY b.name, c.model
        ''')
        
        cars = []
        for row in cursor.fetchall():
            car = {
                'id': row[0],
                'brand': row[1],
                'model': row[2],
                'year': row[3],
                'price': float(row[4]) if row[4] else None,
                'engine_type': row[5],
                'horsepower': row[6],
                'acceleration': row[7],
                'top_speed': row[8],
                'fuel_consumption': row[9],
                'transmission': row[10],
                'drive_type': row[11],
                'images': json.loads(row[12]) if row[12] else [],
                'description': row[13]
            }
            cars.append(car)
        
        conn.close()
        return cars
    
    def get_cars_by_brand(self, brand_name):
        """Получение автомобилей по бренду"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT 
                c.id, b.name as brand, c.model, c.year, c.price,
                c.engine_type, c.horsepower, c.acceleration,
                c.images, c.description
            FROM cars c
            JOIN brands b ON c.brand_id = b.id
            WHERE b.name = ?
            ORDER BY c.price DESC
        ''', (brand_name,))
        
        cars = []
        for row in cursor.fetchall():
            car = {
                'id': row[0],
                'brand': row[1],
                'model': row[2],
                'year': row[3],
                'price': float(row[4]) if row[4] else None,
                'engine_type': row[5],
                'horsepower': row[6],
                'acceleration': row[7],
                'images': json.loads(row[8]) if row[8] else [],
                'description': row[9]
            }
            cars.append(car)
        
        conn.close()
        return cars
    
    def search_cars(self, query):
        """Поиск автомобилей"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT 
                c.id, b.name as brand, c.model, c.year, c.price,
                c.engine_type, c.horsepower, c.acceleration,
                c.images, c.description
            FROM cars c
            JOIN brands b ON c.brand_id = b.id
            WHERE b.name LIKE ? OR c.model LIKE ? OR c.description LIKE ?
            ORDER BY c.price DESC
        ''', (f'%{query}%', f'%{query}%', f'%{query}%'))
        
        cars = []
        for row in cursor.fetchall():
            car = {
                'id': row[0],
                'brand': row[1],
                'model': row[2],
                'year': row[3],
                'price': float(row[4]) if row[4] else None,
                'engine_type': row[5],
                'horsepower': row[6],
                'acceleration': row[7],
                'images': json.loads(row[8]) if row[8] else [],
                'description': row[9]
            }
            cars.append(car)
        
        conn.close()
        return cars
    
    def add_contact(self, name, email, message, phone=None, car_id=None):
        """Добавление контакта"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO contacts (name, email, phone, message, car_id)
            VALUES (?, ?, ?, ?, ?)
        ''', (name, email, phone, message, car_id))
        
        conn.commit()
        contact_id = cursor.lastrowid
        conn.close()
        return contact_id

# Создаем глобальный экземпляр базы данных
db = CarDatabase()