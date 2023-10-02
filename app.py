from flask import Flask, request, jsonify

app = Flask(__name__)

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
        carbs = calories - protein - fat
    elif goal == 'Поддержка':
        protein = lean_mass * 2
        fat = lean_mass * 1
        carbs = calories - protein - fat
        
    
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
