from database import db

def populate_cars():
    """Заполнение базы данных всеми автомобилями из каталога DriveDirectory"""
    print("🔄 Заполнение базы данных автомобилями...")
    
    # Проверяем существующие автомобили
    existing_cars = db.get_all_cars()
    existing_models = {(car['brand'], car['model']) for car in existing_cars}
    
    # ПОЛНЫЕ данные автомобилей для каталога DriveDirectory
    cars_data = [
        # ========== BMW ==========
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
            'fuel_consumption': 0,
            'transmission': 'Автоматическая',
            'drive_type': 'Полный (xDrive)',
            'description': 'Флагманский электромобиль с инновационными технологиями',
            'images': ['bmw-i7-1.jpg', 'bmw-i7-2.jpg', 'bmw-i7-3.jpg']
        }),

        # ========== Mercedes-Benz ==========
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
        ('Mercedes-Benz', 'EQS 580', 2024, 8900000, {
            'engine_type': 'Два электромотора',
            'horsepower': 524,
            'acceleration': 4.3,
            'top_speed': 210,
            'fuel_consumption': 0,
            'transmission': 'Автоматическая',
            'drive_type': 'Полный (4MATIC)',
            'description': 'Электрический флагман с рекордным запасом хода',
            'images': ['mercedes-eqs-1.jpg', 'mercedes-eqs-2.jpg', 'mercedes-eqs-3.jpg']
        }),

        # ========== Audi ==========
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
        ('Audi', 'R8 V10 Plus', 2024, 14500000, {
            'engine_type': '5.2 л V10 атмосферный',
            'horsepower': 610,
            'acceleration': 3.2,
            'top_speed': 330,
            'fuel_consumption': 12.3,
            'transmission': '7-ст. РКПП S tronic',
            'drive_type': 'Полный (quattro)',
            'description': 'Суперкар с атмосферным двигателем',
            'images': ['audi-r8-1.jpg', 'audi-r8-2.jpg', 'audi-r8-3.jpg']
        }),
        ('Audi', 'e-tron GT', 2024, 9500000, {
            'engine_type': 'Два электромотора',
            'horsepower': 530,
            'acceleration': 4.1,
            'top_speed': 245,
            'fuel_consumption': 0,
            'transmission': '2-ст. АКПП',
            'drive_type': 'Полный (quattro)',
            'description': 'Электрический гран туризмо',
            'images': ['audi-etron-1.jpg', 'audi-etron-2.jpg', 'audi-etron-3.jpg']
        }),

        # ========== Porsche ==========
        ('Porsche', '911 Turbo S', 2024, 16500000, {
            'engine_type': '3.7 л B6 Twin-Turbo',
            'horsepower': 650,
            'acceleration': 2.7,
            'top_speed': 330,
            'fuel_consumption': 11.1,
            'transmission': '8-ст. АКПП PDK',
            'drive_type': 'Полный (PTM)',
            'description': 'Икона спортивных автомобилей с невероятной динамикой',
            'images': ['porsche-911-1.jpg', 'porsche-911-2.jpg', 'porsche-911-3.jpg']
        }),
        ('Porsche', 'Taycan Turbo', 2024, 12300000, {
            'engine_type': 'Два электромотора',
            'horsepower': 680,
            'acceleration': 3.2,
            'top_speed': 260,
            'fuel_consumption': 0,
            'transmission': '2-ст. АКПП',
            'drive_type': 'Полный',
            'description': 'Электрический спорткар с ДНК Porsche',
            'images': ['porsche-taycan-1.jpg', 'porsche-taycan-2.jpg', 'porsche-taycan-3.jpg']
        }),
        ('Porsche', 'Cayenne Turbo GT', 2024, 13800000, {
            'engine_type': '4.0 л V8 Twin-Turbo',
            'horsepower': 640,
            'acceleration': 3.3,
            'top_speed': 300,
            'fuel_consumption': 12.9,
            'transmission': '8-ст. АКПП Tiptronic S',
            'drive_type': 'Полный (PTM)',
            'description': 'Самый быстрый SUV на Нюрбургринге',
            'images': ['porsche-cayenne-1.jpg', 'porsche-cayenne-2.jpg', 'porsche-cayenne-3.jpg']
        }),

        # ========== Dodge ==========
        ('Dodge', 'Challenger SRT Hellcat', 2024, 8900000, {
            'engine_type': '6.2 л V8 HEMI Supercharged',
            'horsepower': 717,
            'acceleration': 3.6,
            'top_speed': 328,
            'fuel_consumption': 15.9,
            'transmission': '8-ст. АКПП TorqueFlite',
            'drive_type': 'Задний',
            'description': 'Американский мускул-кар с адским характером',
            'images': ['dodge-challenger-1.jpg', 'dodge-challenger-2.jpg', 'dodge-challenger-3.jpg']
        }),
        ('Dodge', 'Charger SRT Hellcat', 2024, 9200000, {
            'engine_type': '6.2 л V8 HEMI Supercharged',
            'horsepower': 717,
            'acceleration': 3.7,
            'top_speed': 315,
            'fuel_consumption': 16.2,
            'transmission': '8-ст. АКПП TorqueFlite',
            'drive_type': 'Задний',
            'description': 'Четырехдверный мускул-кар с невероятной мощностью',
            'images': ['dodge-charger-1.jpg', 'dodge-charger-2.jpg', 'dodge-charger-3.jpg']
        }),
        ('Dodge', 'Viper ACR', 2024, 15000000, {
            'engine_type': '8.4 л V10 атмосферный',
            'horsepower': 645,
            'acceleration': 3.0,
            'top_speed': 285,
            'fuel_consumption': 14.7,
            'transmission': '6-ст. МКПП Tremec',
            'drive_type': 'Задний',
            'description': 'Легендарный американский суперкар',
            'images': ['dodge-viper-1.jpg', 'dodge-viper-2.jpg', 'dodge-viper-3.jpg']
        }),

        # ========== Chevrolet ==========
        ('Chevrolet', 'Camaro ZL1', 2024, 7500000, {
            'engine_type': '6.2 л V8 Supercharged',
            'horsepower': 650,
            'acceleration': 3.5,
            'top_speed': 320,
            'fuel_consumption': 14.2,
            'transmission': '10-ст. АКПП',
            'drive_type': 'Задний',
            'description': 'Икона американского автомобилестроения',
            'images': ['chevrolet-camaro-1.jpg', 'chevrolet-camaro-2.jpg', 'chevrolet-camaro-3.jpg']
        }),
        ('Chevrolet', 'Corvette Stingray', 2024, 8200000, {
            'engine_type': '6.2 л V8 LT2',
            'horsepower': 495,
            'acceleration': 2.9,
            'top_speed': 312,
            'fuel_consumption': 12.1,
            'transmission': '8-ст. АКПП',
            'drive_type': 'Задний',
            'description': 'Американский суперкар с заднемоторной компоновкой',
            'images': ['chevrolet-corvette-1.jpg', 'chevrolet-corvette-2.jpg', 'chevrolet-corvette-3.jpg']
        }),
        ('Chevrolet', 'Tahoe High Country', 2024, 6800000, {
            'engine_type': '6.2 л V8 EcoTec3',
            'horsepower': 420,
            'acceleration': 6.1,
            'top_speed': 180,
            'fuel_consumption': 13.8,
            'transmission': '10-ст. АКПП',
            'drive_type': 'Полный (4WD)',
            'description': 'Флагманский полноразмерный SUV',
            'images': ['chevrolet-tahoe-1.jpg', 'chevrolet-tahoe-2.jpg', 'chevrolet-tahoe-3.jpg']
        }),

        # ========== Ford ==========
        ('Ford', 'Mustang GT', 2024, 5900000, {
            'engine_type': '5.0 л V8 Coyote',
            'horsepower': 450,
            'acceleration': 4.3,
            'top_speed': 250,
            'fuel_consumption': 12.4,
            'transmission': '10-ст. АКПП',
            'drive_type': 'Задний',
            'description': 'Легендарный пони-кар',
            'images': ['ford-mustang-1.jpg', 'ford-mustang-2.jpg', 'ford-mustang-3.jpg']
        }),
        ('Ford', 'F-150 Raptor', 2024, 7200000, {
            'engine_type': '3.5 л V6 EcoBoost',
            'horsepower': 450,
            'acceleration': 5.7,
            'top_speed': 180,
            'fuel_consumption': 13.8,
            'transmission': '10-ст. АКПП',
            'drive_type': 'Полный (4WD)',
            'description': 'Внедорожный пикап для экстремальных условий',
            'images': ['ford-f150-1.jpg', 'ford-f150-2.jpg', 'ford-f150-3.jpg']
        }),
        ('Ford', 'Explorer ST', 2024, 6500000, {
            'engine_type': '3.0 л V6 EcoBoost',
            'horsepower': 400,
            'acceleration': 5.5,
            'top_speed': 230,
            'fuel_consumption': 11.9,
            'transmission': '10-ст. АКПП',
            'drive_type': 'Полный (4WD)',
            'description': 'Спортивный SUV для всей семьи',
            'images': ['ford-explorer-1.jpg', 'ford-explorer-2.jpg', 'ford-explorer-3.jpg']
        }),

        # ========== Cadillac ==========
        ('Cadillac', 'Escalade-V', 2024, 12500000, {
            'engine_type': '6.2 л V8 Supercharged',
            'horsepower': 682,
            'acceleration': 4.4,
            'top_speed': 198,
            'fuel_consumption': 16.3,
            'transmission': '10-ст. АКПП',
            'drive_type': 'Полный (4WD)',
            'description': 'Самый мощный полноразмерный SUV в мире',
            'images': ['cadillac-escalade-1.jpg', 'cadillac-escalade-2.jpg', 'cadillac-escalade-3.jpg']
        }),
        ('Cadillac', 'XT5 Sport', 2024, 5200000, {
            'engine_type': '3.6 л V6',
            'horsepower': 310,
            'acceleration': 7.5,
            'top_speed': 210,
            'fuel_consumption': 10.2,
            'transmission': '9-ст. АКПП',
            'drive_type': 'Полный (AWD)',
            'description': 'Премиальный кроссовер с американским характером',
            'images': ['cadillac-xt5-1.jpg', 'cadillac-xt5-2.jpg', 'cadillac-xt5-3.jpg']
        }),
        ('Cadillac', 'Lyriq', 2024, 6800000, {
            'engine_type': 'Электромотор',
            'horsepower': 340,
            'acceleration': 6.0,
            'top_speed': 210,
            'fuel_consumption': 0,
            'transmission': '1-ст. АКПП',
            'drive_type': 'Задний',
            'description': 'Электрический флагман нового поколения',
            'images': ['cadillac-lyriq-1.jpg', 'cadillac-lyriq-2.jpg', 'cadillac-lyriq-3.jpg']
        }),

        # ========== Lamborghini ==========
        ('Lamborghini', 'Urus', 2024, 22000000, {
            'engine_type': '4.0 л V8 Twin-Turbo',
            'horsepower': 650,
            'acceleration': 3.6,
            'top_speed': 305,
            'fuel_consumption': 12.7,
            'transmission': '8-ст. АКПП',
            'drive_type': 'Полный',
            'description': 'Самый быстрый SUV в мире',
            'images': ['lamborghini-urus-1.jpg', 'lamborghini-urus-2.jpg', 'lamborghini-urus-3.jpg']
        }),
        ('Lamborghini', 'Revuelto', 2024, 45000000, {
            'engine_type': '6.5 л V12 + 3 электромотора',
            'horsepower': 1015,
            'acceleration': 2.5,
            'top_speed': 350,
            'fuel_consumption': 0,
            'transmission': '8-ст. АКПП',
            'drive_type': 'Полный',
            'description': 'Гиперкар нового поколения с гибридной силовой установкой',
            'images': ['lamborghini-revuelto-1.jpg', 'lamborghini-revuelto-2.jpg', 'lamborghini-revuelto-3.jpg']
        }),
        ('Lamborghini', 'Huracán STO', 2024, 28500000, {
            'engine_type': '5.2 л V10 атмосферный',
            'horsepower': 640,
            'acceleration': 3.0,
            'top_speed': 310,
            'fuel_consumption': 13.9,
            'transmission': '7-ст. РКПП',
            'drive_type': 'Задний',
            'description': 'Трековый монстр для дорог общего пользования',
            'images': ['lamborghini-huracan-1.jpg', 'lamborghini-huracan-2.jpg', 'lamborghini-huracan-3.jpg']
        }),

        # ========== RAM ==========
        ('RAM', '1500 Tungsten', 2024, 6200000, {
            'engine_type': '5.7 л V8 HEMI',
            'horsepower': 395,
            'acceleration': 6.8,
            'top_speed': 180,
            'fuel_consumption': 13.1,
            'transmission': '8-ст. АКПП',
            'drive_type': 'Полный (4WD)',
            'description': 'Роскошный пикап премиум-класса',
            'images': ['ram-1500-tungsten-1.jpg', 'ram-1500-tungsten-2.jpg', 'ram-1500-tungsten-3.jpg']
        }),
        ('RAM', '1500 TRX', 2024, 12500000, {
            'engine_type': '6.2 л V8 Supercharged',
            'horsepower': 702,
            'acceleration': 4.5,
            'top_speed': 190,
            'fuel_consumption': 17.0,
            'transmission': '8-ст. АКПП',
            'drive_type': 'Полный (4WD)',
            'description': 'Самый мощный серийный пикап в мире',
            'images': ['ram-1500-trx-1.jpg', 'ram-1500-trx-2.jpg', 'ram-1500-trx-3.jpg']
        }),
        ('RAM', '1500 RHO', 2024, 8900000, {
            'engine_type': '3.0 л I6 Twin-Turbo Hurricane',
            'horsepower': 540,
            'acceleration': 5.6,
            'top_speed': 185,
            'fuel_consumption': 12.5,
            'transmission': '8-ст. АКПП',
            'drive_type': 'Полный (4WD)',
            'description': 'Высокопроизводительный пикап для бездорожья',
            'images': ['ram-1500-rho-1.jpg', 'ram-1500-rho-2.jpg', 'ram-1500-rho-3.jpg']
        })
    ]
    
    # Добавляем только новые автомобили
    added_count = 0
    for car_data in cars_data:
        brand_name, model, year, price, kwargs = car_data
        
        # Проверяем, существует ли уже такой автомобиль
        if (brand_name, model) not in existing_models:
            car_id = db.add_car(brand_name, model, year, price, **kwargs)
            if car_id:
                added_count += 1
                print(f"✅ Добавлен: {brand_name} {model}")
        else:
            print(f"⏭️  Пропущен (уже существует): {brand_name} {model}")
    
    print(f"\n🎉 Заполнение завершено! Добавлено {added_count} новых автомобилей")
    return added_count

if __name__ == "__main__":
    populate_cars()