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
        
        try:
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
                cursor.execute('SELECT * FROM brands ORDER BY name')
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
            
            elif self.path.startswith('/api/car/'):
                car_id = self.path.split('/')[-1]
                if car_id.isdigit():
                    cars = db.get_all_cars()
                    car = next((c for c in cars if c['id'] == int(car_id)), None)
                    if car:
                        self._send_json(car)
                    else:
                        self._send_json({'error': 'Car not found'}, 404)
                else:
                    self._send_json({'error': 'Invalid car ID'}, 400)
            
            else:
                self.send_error(404, 'API endpoint not found')
                
        except Exception as e:
            self._send_json({'error': str(e)}, 500)
    
    def do_POST(self):
        if self.path == '/api/contact':
            try:
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                contact_data = json.loads(post_data.decode('utf-8'))
                
                # Валидация обязательных полей
                required_fields = ['name', 'email', 'message']
                for field in required_fields:
                    if not contact_data.get(field):
                        self._send_json({'success': False, 'error': f'Missing required field: {field}'}, 400)
                        return
                
                contact_id = db.add_contact(
                    name=contact_data['name'],
                    email=contact_data['email'],
                    phone=contact_data.get('phone'),
                    message=contact_data['message'],
                    car_id=contact_data.get('car_id')
                )
                
                self._send_json({'success': True, 'contact_id': contact_id})
                
            except json.JSONDecodeError:
                self._send_json({'success': False, 'error': 'Invalid JSON'}, 400)
            except Exception as e:
                self._send_json({'success': False, 'error': str(e)}, 500)
        else:
            self.send_error(404, 'Endpoint not found')
    
    def _send_json(self, data, status=200):
        self.send_response(status)
        self.send_header('Content-type', 'application/json; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode('utf-8'))
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

def populate_initial_data():
    """Заполнение базы начальными данными для каталога DriveDirectory"""
    print("🔄 Заполнение базы данных начальными данными...")
    
    # Данные автомобилей для вашего каталога
    cars_data = [
        # BMW
        ('BMW', 'M5 Competition', 2024, 12900000, {
            'engine_type': '4.4 л V8 Twin-Turbo',
            'horsepower': 625,
            'acceleration': 3.1,
            'top_speed': 305,
            'fuel_consumption': 10.8,
            'transmission': '8-ст. АКПП M Steptronic',
            'drive_type': 'Полный (M xDrive)',
            'description': 'Легендарный спортивный седан с технологиями Formula 1',
            'images': ['bmw-m5-1.jpg', 'bmw-m5-2.jpg', 'bmw-m5-3.jpg']
        }),
        ('BMW', 'X5 M Competition', 2024, 10200000, {
            'engine_type': '4.4 л V8 Twin-Turbo',
            'horsepower': 625,
            'acceleration': 3.8,
            'top_speed': 290,
            'fuel_consumption': 12.5,
            'transmission': '8-ст. АКПП M Steptronic',
            'drive_type': 'Полный (M xDrive)',
            'description': 'Мощный SUV с характером спортивного автомобиля',
            'images': ['bmw-x5-1.jpg', 'bmw-x5-2.jpg', 'bmw-x5-3.jpg']
        }),
        ('BMW', 'i7 xDrive60', 2024, 9800000, {
            'engine_type': 'Два электромотора',
            'horsepower': 544,
            'acceleration': 4.7,
            'top_speed': 240,
            'fuel_consumption': None,
            'transmission': 'Автоматическая',
            'drive_type': 'Полный (xDrive)',
            'description': 'Флагманский электромобиль с инновационными технологиями',
            'images': ['bmw-i7-1.jpg', 'bmw-i7-2.jpg', 'bmw-i7-3.jpg']
        }),
        
        # Mercedes-Benz
        ('Mercedes-Benz', 'AMG G 63', 2024, 18500000, {
            'engine_type': '4.0 л V8 Biturbo',
            'horsepower': 585,
            'acceleration': 4.5,
            'top_speed': 220,
            'fuel_consumption': 13.1,
            'transmission': '9-ст. АКПП AMG Speedshift',
            'drive_type': 'Полный (4MATIC)',
            'description': 'Легендарный внедорожник с характером AMG',
            'images': ['mercedes-g63-1.jpg', 'mercedes-g63-2.jpg', 'mercedes-g63-3.jpg']
        }),
        ('Mercedes-Benz', 'S 580', 2024, 11900000, {
            'engine_type': '4.0 л V8 Biturbo + EQ Boost',
            'horsepower': 503,
            'acceleration': 4.7,
            'top_speed': 250,
            'fuel_consumption': 9.1,
            'transmission': '9-ст. АКПП 9G-Tronic',
            'drive_type': 'Полный (4MATIC)',
            'description': 'Идеальное сочетание роскоши и технологий',
            'images': ['mercedes-sclass-1.jpg', 'mercedes-sclass-2.jpg', 'mercedes-sclass-3.jpg']
        }),
        
        # Audi
        ('Audi', 'RS6 Avant', 2024, 11200000, {
            'engine_type': '4.0 л V8 Twin-Turbo',
            'horsepower': 600,
            'acceleration': 3.6,
            'top_speed': 305,
            'fuel_consumption': 11.6,
            'transmission': '8-ст. АКПП Tiptronic',
            'drive_type': 'Полный (quattro)',
            'description': 'Самый быстрый универсал в мире',
            'images': ['audi-rs6-1.jpg', 'audi-rs6-2.jpg', 'audi-rs6-3.jpg']
        }),
        
        # Добавьте остальные автомобили из вашего HTML...
        # Porsche, Dodge, Chevrolet, Ford, Cadillac, Lamborghini, RAM
    ]
    
    # Добавляем автомобили в базу
    for car_data in cars_data:
        brand_name, model, year, price, kwargs = car_data
        db.add_car(brand_name, model, year, price, **kwargs)
    
    print("✅ База данных заполнена!")

def check_database():
    """Проверка состояния базы данных"""
    try:
        conn = db.get_connection()
        cursor = conn.cursor()
        
        # Проверяем количество автомобилей
        cursor.execute('SELECT COUNT(*) FROM cars')
        car_count = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM brands')
        brand_count = cursor.fetchone()[0]
        
        conn.close()
        
        print(f"📊 Статистика базы данных:")
        print(f"   🚗 Автомобилей: {car_count}")
        print(f"   🏷️ Брендов: {brand_count}")
        
        return car_count > 0
        
    except Exception as e:
        print(f"❌ Ошибка проверки базы данных: {e}")
        return False

if __name__ == '__main__':
    # Проверяем и заполняем базу данных
    if not check_database():
        populate_initial_data()
    else:
        print("✅ База данных уже заполнена")
    
    # Настройка порта
    PORT = 8000
    
    # Запуск сервера
    with socketserver.TCPServer(("", PORT), CarHandler) as httpd:
        print(f"\n🚀 Сервер DriveDirectory запущен!")
        print(f"📍 Адрес: http://localhost:{PORT}")
        print(f"🗄️ База данных: cars.db")
        print(f"\n📡 Доступные API эндпоинты:")
        print("   GET  /api/cars - все автомобили")
        print("   GET  /api/cars/brand/{name} - автомобили по бренду") 
        print("   GET  /api/search?q=query - поиск автомобилей")
        print("   GET  /api/brands - все бренды")
        print("   GET  /api/car/{id} - информация об автомобиле")
        print("   POST /api/contact - отправить заявку")
        print("\n⚡ Статические файлы обслуживаются из текущей директории")
        print("\n⏹️  Для остановки сервера нажмите Ctrl+C")
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n🛑 Сервер остановлен")