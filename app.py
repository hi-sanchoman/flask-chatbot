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
        bmr = (10 * weight) + (6.25 * height) - (5 * age) + 5
    else:
        bmr = (10 * weight) + (6.25 * height) - (5 * age) - 161

    # Расчет сухой массы
    lean_mass = weight * (1 - percent_fat)

    # Расчет термического эффекта пищи (TEF)
    tef = bmr * 0.1

    # Расчет общего калорийного потребления
    calories = bmr * (1 + activity) + tef

    # Расчет КБЖУ
    protein = lean_mass * (1.2 - percent_fat)
    fat = lean_mass * (0.8 - percent_fat)
    carbs = (calories - (protein * 4 + fat * 9)) / 4

    # Расчет ИМТ
    bmi = weight / ((height / 100) ** 2)

    # Расчет потребности в воде
    water = weight * 0.035

    # Расчет потребности в клетчатке
    fiber = 38 if gender == 'Мужской' else 25

    # Адаптация калорий в зависимости от цели
    if goal == 'Дефицит':
        calories *= 0.8  # уменьшение калорий на 20%
    elif goal == 'Профицит':
        calories *= 1.1  # увеличение калорий на 10%
    
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
        'caffeine': 400,  # максимальное рекомендуемое потребление кофеина
        'fiber': fiber,
        'salt': 5  # рекомендуемое потребление соли
    }

    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
