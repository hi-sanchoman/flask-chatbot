from flask import Flask, request, jsonify
import cv2
import numpy as np
import requests

app = Flask(__name__)

# Detect fat %

def fetch_image_from_url(url):
    response = requests.get(url)
    image_arr = np.asarray(bytearray(response.content), dtype=np.uint8)
    image = cv2.imdecode(image_arr, -1)  # Loads image as it is, including alpha channel if present
    
    #if 'image' not in response.headers.get('content-type'):
    #    raise ValueError("URL did not return an image " + response.headers.get('content-type'))
    
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # Convert to grayscale

def template_matching(source_image_url, template_image_urls):
    # Fetch the source image from the URL
    source_image = fetch_image_from_url(source_image_url)

    max_similarity = -np.inf  # Initialize with a very low value
    best_match_url = None

    # Loop through each template and compute similarity
    for template_url in template_image_urls:
        template = fetch_image_from_url(template_url)
        res = cv2.matchTemplate(source_image, template, cv2.TM_CCOEFF_NORMED)

        if np.max(res) > max_similarity:
            max_similarity = np.max(res)
            best_match_url = template_url

    # Convert the max similarity to a percentage
    similarity_percentage = max_similarity * 100

    return best_match_url, similarity_percentage

def estimate_fat_percentage(source_image_url, templates):
    source_image = fetch_image_from_url(source_image_url)
    
    # best_match_percentage = 0
    # best_match_fat = 0

    # for template_url, fat_percentage in templates.items():
    #     template = fetch_image_from_url(template_url)
    #     res = cv2.matchTemplate(source_image, template, cv2.TM_CCOEFF_NORMED)
    #     max_similarity = np.max(res)

    #     if max_similarity > best_match_percentage:
    #         best_match_percentage = max_similarity
    #         best_match_fat = fat_percentage

    # bfp = best_match_fat * (best_match_percentage)
    return bfp


templates = {
    #"https://cdn.discordapp.com/attachments/1053759410297634906/1159574302459441152/Screenshot_2023-10-06_at_01.02.27.png?ex=653184b9&is=651f0fb9&hm=1ace1623419634ff78769c5347c1d93d2fd4b1aca4e6665620a4d7fb2d83e1cc&": 35, 
    #"https://cdn.discordapp.com/attachments/1053759410297634906/1159574650024640742/Screenshot_2023-10-06_at_01.02.36.png?ex=6531850c&is=651f100c&hm=6afc8664f57fe27cda288511a4800c6e77cf890ad42477314524d7e6e4e1eaec&": 25,
    #"https://cdn.discordapp.com/attachments/1053759410297634906/1159576164717826089/Screenshot_2023-10-06_at_01.02.51.png?ex=65318675&is=651f1175&hm=76916c91f6ca621a62f963e61af414b9a1631db821408145685a573afc3b1954&": 20
    # ... Add more templates as needed
    "https://media.discordapp.net/attachments/1053759410297634906/1160992674543829153/fat_08_2.png?ex=6536adaf&is=652438af&hm=29f7a56f359c243d46b5a3109132ae2a79caf22d1a916f6590dcc6dd614d947d&=&width=850&height=934": 8,
    "https://media.discordapp.net/attachments/1053759410297634906/1160992674216689785/fat_08.png?ex=6536adaf&is=652438af&hm=c34b96b792ed3f55adaf48c044edd8d369c7c6aea729bc81abe6a8f89144543a&=&width=854&height=934": 8,
    "https://media.discordapp.net/attachments/1053759410297634906/1160992611293737133/fat_10.png?ex=6536ada0&is=652438a0&hm=5b1393e0f2e75e0bda1748d9b446f1af8e16f88f506993e86a88037fa3e36c78&=&width=864&height=934": 10,
    "https://media.discordapp.net/attachments/1053759410297634906/1160992611616686270/fat_10_2.png?ex=6536ada0&is=652438a0&hm=d28021bfdbfc9a313508c778fa255a3c828b66f5a439626df49b1446521edf60&=&width=834&height=934": 10,
    "https://media.discordapp.net/attachments/1053759410297634906/1160992611901919342/fat_15.png?ex=6536ada0&is=652438a0&hm=29ef5fb110532e0c9893a592f66e6a6a173c11ca3af3e23f85085120a376683e&=&width=852&height=934": 15,
    "https://media.discordapp.net/attachments/1053759410297634906/1160992612174540921/fat_15_2.png?ex=6536ada0&is=652438a0&hm=44745f68c68f76d684a7974765340391fa6e7468f023682e83c268493b16cd26&=&width=854&height=934": 15,
    "https://media.discordapp.net/attachments/1053759410297634906/1160992612421996544/fat_20.png?ex=6536ada1&is=652438a1&hm=d7dcbdd7fc12bdb548a3656ee42eb2749ee641f2af1eaa55783bdd79bb6de774&=&width=854&height=934": 20,
    "https://media.discordapp.net/attachments/1053759410297634906/1160992612669476945/fat_20_2.png?ex=6536ada1&is=652438a1&hm=58fe63ce8a2f2f865e48dc76fb2fabfe81a3bfa0cdf3483d305f4cccbafcb89c&=&width=850&height=934": 20,
    "https://media.discordapp.net/attachments/1053759410297634906/1160992612916932618/fat_25.png?ex=6536ada1&is=652438a1&hm=3d5606ede7f2cbe8494bbad37286b879da40e90df302c5c9cbc9a54a6bf7056b&=&width=852&height=934": 25,
    "https://media.discordapp.net/attachments/1053759410297634906/1160992613260857364/fat_25_2.png?ex=6536ada1&is=652438a1&hm=7e262576c81817569dd6f68eb1f998d952c3b4ea10512a31bcc9ca27a1024142&=&width=846&height=934": 25,
    "https://media.discordapp.net/attachments/1053759410297634906/1160992613642555417/fat_30.png?ex=6536ada1&is=652438a1&hm=417bd5ed9cca91f9ad9320ee503f355efa82d8437195eeb079e10aa66a652a60&=&width=848&height=934": 30,
    "https://media.discordapp.net/attachments/1053759410297634906/1160992613969702974/fat_35_2.png?ex=6536ada1&is=652438a1&hm=0a1840a0525d238af9f4fbc36700fabb97ed06fffb7309500c97c91ac067f197&=&width=844&height=934": 35,
    
}

@app.route('/fat', methods=['GET'])
def calculate_fat():
    source_image_url = request.args.get('source_image')
    #template_image_urls = ['https://cdn.discordapp.com/attachments/1053759410297634906/1159574302459441152/Screenshot_2023-10-06_at_01.02.27.png?ex=653184b9&is=651f0fb9&hm=1ace1623419634ff78769c5347c1d93d2fd4b1aca4e6665620a4d7fb2d83e1cc&', 'https://cdn.discordapp.com/attachments/1053759410297634906/1159574650024640742/Screenshot_2023-10-06_at_01.02.36.png?ex=6531850c&is=651f100c&hm=6afc8664f57fe27cda288511a4800c6e77cf890ad42477314524d7e6e4e1eaec&', 'https://cdn.discordapp.com/attachments/1053759410297634906/1159576164717826089/Screenshot_2023-10-06_at_01.02.51.png?ex=65318675&is=651f1175&hm=76916c91f6ca621a62f963e61af414b9a1631db821408145685a573afc3b1954&']  # Add as many URLs as needed
    #best_match, similarity = template_matching(source_image_url, template_image_urls)

    age = float(request.args.get('bju_age'))
    weight = float(request.args.get('bju_weight'))
    height = float(request.args.get('bju_height'))
    gender = request.args.get('bju_gender')

    bmi = weight / ((height / 100) ** 2)
    
    bfp = 0
    
    if gender == 'Мужской':
        bfp = 1.20 * bmi + 0.23 * age - 16.2
    else:
        bfp = 1.20 * bmi + 0.23 * age - 5.4

    # estimated_fat = estimate_fat_percentage(source_image_url, templates)

    result = {
        'fat': bfp
    }

    return jsonify(result)





@app.route('/cbju', methods=['GET'])
def calculate_bju():
    goal = request.args.get('bju_goal')
    weight = float(request.args.get('bju_weight'))
    height = float(request.args.get('bju_height'))
    age = float(request.args.get('bju_age'))
    gender = request.args.get('bju_gender')
    percent_fat = float(request.args.get('bju_percent')) / 100
    activity = float(request.args.get('bju_activity'))

    l_protein = 0
    l_fat = 0
    l_carbs = 0

    # Расчет сухой массы
    lean_mass = weight * (1 - percent_fat)

    # Расчет базального метаболизма
    if gender == 'Мужской':
        bmr = 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
    else:
        bmr = 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)


    # Расчет термического эффекта пищи (TEF)
    tef = bmr * 0.1

    # Расчет общего калорийного потребления
    if activity == 1.2:
        calories = bmr * 1.2
    elif activity == 1.375:
        calories = bmr * 1.3 - 1.375
    elif activity == 1.55:
        calories = bmr * 1.5 - 1.55
    elif activity == 1.7:
        calories = bmr * 1.7
    elif activity == 1.9:
        calories = bmr * 1.9

    # Расчет ИМТ
    bmi = weight / ((height / 100) ** 2)

    # Вода, клетчатка, соль и кофеин
    water = lean_mass / 20
    salt = lean_mass / 10 * 1
    caffeine_from = weight * 2.5
    caffeine_to = weight * 5

    # Адаптация калорий в зависимости от цели
    if goal == 'Дефицит':
        calories *= 0.8  # уменьшение калорий на 20%
        if gender == 'Мужской':
            protein = lean_mass * 2.2
        else:
            protein = lean_mass * 2
        fat = lean_mass * 1
        carbs = (calories - (protein * 4 + fat * 9)) / 4
        fiber = calories / 1000 * 10
    elif goal == 'Профицит':
        calories *= 1.2  # увеличение калорий на 20%
        protein = lean_mass * 2
        fat = lean_mass * 1
        #carbs = (calories - (protein * 4 + fat * 9)) / 4
        carbs = (calories - (protein * 4 + fat * 9)) / 4
        fiber = calories / 1000 * 10
    elif goal == 'Поддержка':
        protein = lean_mass * 2
        fat = lean_mass * 1
        carbs = (calories - (protein * 4 + fat * 9)) / 4
        fiber = calories / 1000 * 10

    # Расчет базального метаболизма
    if gender == 'Женский':
        l_protein = lean_mass * 2
        l_fat = lean_mass * 1.4
        calories = calories + 200
        l_carbs = (calories - (l_protein * 4 + l_fat * 9)) / 4
    
    
    result = {
        'bmr': round(bmr),
        'lean_mass': round(lean_mass, 2),
        'tef': round(tef),
        'calories': round(calories),
        'protein': round(protein),
        'fat': round(fat),
        'carbs': round(carbs),
        'bmi': round(bmi, 2),
        'water': round(water, 2),
        'caffeine_from': round(caffeine_from, 2), 
        'caffeine_to': round(caffeine_to, 2), 
        'fiber': round(fiber, 2),
        'salt': round(salt, 2),
        'l_protein': round(l_protein),
        'l_fat': round(l_fat),
        'l_carbs': round(l_carbs)
    }

    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
