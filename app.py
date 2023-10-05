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
    
    best_match_percentage = 0
    best_match_fat = 0

    for template_url, fat_percentage in templates.items():
        template = fetch_image_from_url(template_url)
        res = cv2.matchTemplate(source_image, template, cv2.TM_CCOEFF_NORMED)
        max_similarity = np.max(res)

        if max_similarity > best_match_percentage:
            best_match_percentage = max_similarity
            best_match_fat = fat_percentage

    estimated_fat = best_match_fat * (best_match_percentage)
    return estimated_fat


templates = {
    "https://cdn.discordapp.com/attachments/1053759410297634906/1159574302459441152/Screenshot_2023-10-06_at_01.02.27.png?ex=653184b9&is=651f0fb9&hm=1ace1623419634ff78769c5347c1d93d2fd4b1aca4e6665620a4d7fb2d83e1cc&": 35, 
    "https://cdn.discordapp.com/attachments/1053759410297634906/1159574650024640742/Screenshot_2023-10-06_at_01.02.36.png?ex=6531850c&is=651f100c&hm=6afc8664f57fe27cda288511a4800c6e77cf890ad42477314524d7e6e4e1eaec&": 25,
    "https://cdn.discordapp.com/attachments/1053759410297634906/1159576164717826089/Screenshot_2023-10-06_at_01.02.51.png?ex=65318675&is=651f1175&hm=76916c91f6ca621a62f963e61af414b9a1631db821408145685a573afc3b1954&": 20
    # ... Add more templates as needed
}

@app.route('/fat', methods=['GET'])
def calculate_fat():
    source_image_url = request.args.get('source_image')
    #template_image_urls = ['https://cdn.discordapp.com/attachments/1053759410297634906/1159574302459441152/Screenshot_2023-10-06_at_01.02.27.png?ex=653184b9&is=651f0fb9&hm=1ace1623419634ff78769c5347c1d93d2fd4b1aca4e6665620a4d7fb2d83e1cc&', 'https://cdn.discordapp.com/attachments/1053759410297634906/1159574650024640742/Screenshot_2023-10-06_at_01.02.36.png?ex=6531850c&is=651f100c&hm=6afc8664f57fe27cda288511a4800c6e77cf890ad42477314524d7e6e4e1eaec&', 'https://cdn.discordapp.com/attachments/1053759410297634906/1159576164717826089/Screenshot_2023-10-06_at_01.02.51.png?ex=65318675&is=651f1175&hm=76916c91f6ca621a62f963e61af414b9a1631db821408145685a573afc3b1954&']  # Add as many URLs as needed
    #best_match, similarity = template_matching(source_image_url, template_image_urls)

    estimated_fat = estimate_fat_percentage(source_image_url, templates)

    result = {
        'fat': estimated_fat
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

    # Расчет базального метаболизма
    if gender == 'Мужской':
        bmr = 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
    else:
        bmr = 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)

    # Расчет сухой массы
    lean_mass = weight * (1 - percent_fat)

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
    fiber = calories / 1000 * 10
    salt = lean_mass / 10 * 1
    caffeine = weight * 2.5

    # Адаптация калорий в зависимости от цели
    if goal == 'Дефицит':
        calories *= 0.8  # уменьшение калорий на 20%
        protein = lean_mass * 2.2
        fat = lean_mass * 1
        carbs = (calories - (protein * 4 + fat * 9)) / 4
    elif goal == 'Профицит':
        calories *= 1.2  # увеличение калорий на 20%
        protein = lean_mass * 2
        fat = lean_mass * 1
        #carbs = (calories - (protein * 4 + fat * 9)) / 4
        carbs = (calories - (protein * 4 + fat * 9)) / 4
    elif goal == 'Поддержка':
        protein = lean_mass * 2
        fat = lean_mass * 1
        carbs = (calories - (protein * 4 + fat * 9)) / 4
        
    
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
        'caffeine': caffeine,  # максимальное рекомендуемое потребление кофеина
        'fiber': fiber,
        'salt': salt  # рекомендуемое потребление соли
    }

    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
