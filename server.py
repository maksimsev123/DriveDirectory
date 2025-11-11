import http.server
import socketserver
import json
import sqlite3
import os
from urllib.parse import urlparse, parse_qs
from database import db

class CarHandler(http.server.SimpleHTTPRequestHandler):
    
    def do_GET(self):
        # Обработка API запросов
        if self.path.startswith('/api/'):
            self.handle_api_request()
        else:
            # Статические файлы
            super().do_GET()
    
    def handle_api_request(self):
        parsed_path = urlparse(self.path)
        
        if self.path == '/api/cars':
            cars = db.get_all_cars()
            self._send_json(cars)
        
        elif self.path.startswith('/api/cars/brand/'):
            brand_name = self.path.split('/')[-1]
            cars = db.get_cars_by_brand(brand_name)
            self._send_json(cars)
        
        elif self.path.startswith('/api/search'):
            query_params = parse_qs(parsed_path.query)
            query = query_params.get('q', [''])[0]
            if query:
                cars = db.search_cars(query)
            else:
                cars = db.get_all_cars()
            self._send_json(cars)
        
        elif self.path == '/api/brands':
            conn = db.get_connection()
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM brands')
            brands = []
            for row in cursor.fetchall():
                brand = {
                    'id': row[0],
                    'name': row[1],
                    'country': row[2],
                    'description': row[3],
                    'logo_url': row[4]
                }
                brands.append(brand)
            conn.close()
            self._send_json(brands)
        
        else:
            self.send_error(404, 'API endpoint not found')
    
    def do_POST(self):
        if self.path == '/api/contact':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            contact_data = json.loads(post_data.decode('utf-8'))
            
            try:
                contact_id = db.add_contact(
                    name=contact_data['name'],
                    email=contact_data['email'],
                    phone=contact_data.get('phone'),
                    message=contact_data['message'],
                    car_id=contact_data.get('car_id')
                )
                
                self._send_json({'success': True, 'contact_id': contact_id})
            except Exception as e:
                self._send_json({'success': False, 'error': str(e)}, status=500)
        else:
            self.send_error(404, 'Endpoint not found')
    
    def _send_json(self, data, status=200):
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode('utf-8'))

def populate_initial_data():
    """Заполнение базы начальными данными"""
    print("🔄 Заполнение базы данных начальными данными...")
    
    # Данные автомобилей
    cars_data = [
        # BMW
        ('BMW', 'M5 Competition', 2024, 12900000, {
            'engine_type': '4.4 л V8 Twin-Turbo',
            'horsepower': 625,
            'acceleration': 3.1,
            'top_speed': 305,
            'fuel_consumption': 10.8,
            'transmission': '8-ст. АКПП',
            'drive_type': 'Полный (M xDrive)',
            'description': 'Легендарный спортивный седан с технологиями Formula 1',
            'images': ['images/bmw-m5-1.jpg', 'images/bmw-m5-2.jpg']
        }),
        ('BMW', 'X5 M Competition', 2024, 10200000, {
            'engine_type': '4.4 л V8 Twin-Turbo',
            'horsepower': 625,
            'acceleration': 3.8,
            'top_speed': 290,
            'fuel_consumption': 12.5,
            'transmission': '8-ст. АКПП',
            'drive_type': 'Полный (M xDrive)',
            'description': 'Мощный SUV с характером спортивного автомобиля',
            'images': ['images/bmw-x5-1.jpg', 'images/bmw-x5-2.jpg']
        }),
        # Mercedes
        ('Mercedes', 'AMG G 63', 2024, 18500000, {
            'engine_type': '4.0 л V8 Biturbo',
            'horsepower': 585,
            'acceleration': 4.5,
            'top_speed': 220,
            'fuel_consumption': 13.1,
            'transmission': '9-ст. АКПП',
            'drive_type': 'Полный (4MATIC)',
            'description': 'Легендарный внедорожник с характером AMG',
            'images': ['images/mercedes-g63-1.jpg', 'images/mercedes-g63-2.jpg']
        }),
        ('Mercedes', 'S-Class', 2024, 9500000, {
            'engine_type': '3.0 л I6',
            'horsepower': 435,
            'acceleration': 4.7,
            'top_speed': 250,
            'fuel_consumption': 8.5,
            'transmission': '9-ст. АКПП',
            'drive_type': 'Полный (4MATIC)',
            'description': 'Флагманский седан класса люкс',
            'images': ['images/mercedes-s-class-1.jpg']
        }),
        # Audi
        ('Audi', 'RS6 Avant', 2024, 11200000, {
            'engine_type': '4.0 л V8 Twin-Turbo',
            'horsepower': 600,
            'acceleration': 3.6,
            'top_speed': 305,
            'fuel_consumption': 11.6,
            'transmission': '8-ст. АКПП',
            'drive_type': 'Полный (quattro)',
            'description': 'Самый быстрый универсал в мире',
            'images': ['images/audi-rs6-1.jpg', 'images/audi-rs6-2.jpg']
        }),
        # Toyota
        ('Toyota', 'Camry', 2024, 2800000, {
            'engine_type': '2.5 л I4',
            'horsepower': 203,
            'acceleration': 8.1,
            'top_speed': 210,
            'fuel_consumption': 6.8,
            'transmission': '8-ст. АКПП',
            'drive_type': 'Передний',
            'description': 'Надежный седан бизнес-класса',
            'images': ['images/toyota-camry-1.jpg']
        })
    ]
    
    # Добавляем автомобили в базу
    for car_data in cars_data:
        brand_name, model, year, price, kwargs = car_data
        db.add_car(brand_name, model, year, price, **kwargs)
    
    print("✅ База данных заполнена!")

if __name__ == '__main__':
    # Заполняем базу начальными данными
    populate_initial_data()
    
    PORT = 8001
    with socketserver.TCPServer(("", PORT), CarHandler) as httpd:
        print(f"🚀 Сервер запущен на http://localhost:{PORT}")
        print(f"🗄️ База данных: cars.db")
        print("📊 Доступные эндпоинты:")
        print("   GET /api/cars - все автомобили")
        print("   GET /api/cars/brand/{name} - автомобили по бренду") 
        print("   GET /api/search?q=query - поиск автомобилей")
        print("   GET /api/brands - все бренды")
        print("   POST /api/contact - отправить заявку")
        print("\n⏹️  Для остановки сервера нажмите Ctrl+C")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n🛑 Сервер остановлен")