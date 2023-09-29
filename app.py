from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/cbju', methods=['GET'])
def calculate_bju():
    weight = float(request.args.get('bju_weight'))
    height = float(request.args.get('bju_height'))
    age = float(request.args.get('bju_age'))
    gender = request.args.get('bju_gender')
    percent_fat = float(request.args.get('bju_percent')) / 100
    activity = float(request.args.get('bju_activity'))

    # Расчет калорий
    if gender == 'male':
        calories = (10 * weight) + (6.25 * height) - (5 * age) + 5
    else:
        calories = (10 * weight) + (6.25 * height) - (5 * age) - 161

    calories *= (1 + activity)  # учитываем активность

    # Расчет КБЖУ
    protein = weight * (1.2 - percent_fat)
    fat = weight * (0.8 - percent_fat)
    carbs = (calories - (protein * 4 + fat * 9)) / 4

    result = {
        'calories': round(calories),
        'protein': round(protein),
        'fat': round(fat),
        'carbs': round(carbs)
    }

    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
