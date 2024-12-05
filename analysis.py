import matplotlib.pyplot as plt
import pandas as pd
import json
import os
import base64
import io
import webbrowser

def load_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def generate_pie_chart_base64(df):
    pass_count = df['Pass/Fail'].value_counts().get('Pass', 0)
    fail_count = df['Pass/Fail'].value_counts().get('Fail', 0)
    total_images = len(df) - 1

    labels = ['Pass', 'Fail']
    sizes = [pass_count, fail_count]
    colors = ['#4CAF50', '#FF5252']
    explode = (0.1, 0)

    fig, ax = plt.subplots()
    ax.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140, textprops={'color': 'w'})
    ax.set_title(f"Pass/Fail Analysis\nTotal Test Cases: {total_images}, Passed: {pass_count}, Failed: {fail_count}", fontsize=12)

    chart_stream = io.BytesIO()
    plt.savefig(chart_stream, format='png', bbox_inches='tight')
    plt.close(fig)
    chart_stream.seek(0)
    return base64.b64encode(chart_stream.read()).decode('utf-8')

def generate_html(house_df, car_df, person_df):
    html = "<html><head><style>table {border-collapse: collapse;} th, td {border: 1px solid black; padding: 5px;}</style></head><body>"
    for df, title in zip([house_df, car_df, person_df], ['Houses', 'Cars', 'Persons']):
        chart_base64 = generate_pie_chart_base64(df)
        html += f"<h1>{title}</h1><img src='data:image/png;base64,{chart_base64}' alt='Pie Chart'><br>"
        html += df.to_html(index=False)
    html += "</body></html>"
    return html

def analyze_data(data):
    houses = []
    cars = []
    persons = []

    for item in data:
        image = item.get('image', '')
        category = item.get('category', '').lower()
        analysis = item.get('analysis', '')

        if category == 'people':
            activity, count = extract_activity_and_count(analysis)
            correct_activity = 'Correct' if activity else 'Incorrect'
            correct_count = 'Correct' if count is not None and count > 0 else 'Incorrect'
            detection = "Yes" if activity and count is not None else "No"
            accuracy = calculate_accuracy(correct_activity, correct_count)
            pass_fail = "Pass" if accuracy >= 75 else "Fail"
            persons.append([image, category, activity, count, correct_activity, correct_count, detection, accuracy, pass_fail])

        elif category == 'cars':
            car_type, car_side = extract_car_details(analysis)
            correct_type = 'Correct' if car_type else 'Incorrect'
            correct_side = 'Correct' if car_side else 'Incorrect'
            detection = "Yes" if car_type and car_side else "No"
            accuracy = calculate_accuracy(correct_type, correct_side)
            pass_fail = "Pass" if accuracy >= 75 else "Fail"
            cars.append([image, category, car_type, car_side, correct_type, correct_side, detection, accuracy, pass_fail])

        elif category == 'houses':
            house_type, weather_condition = extract_house_details(analysis)
            correct_type = 'Correct' if house_type else 'Incorrect'
            correct_weather = 'Correct' if weather_condition else 'Incorrect'
            detection = "Yes" if house_type and weather_condition else "No"
            accuracy = calculate_accuracy(correct_type, correct_weather)
            pass_fail = "Pass" if accuracy >= 75 else "Fail"
            houses.append([image, category, house_type, weather_condition, correct_type, correct_weather, detection, accuracy, pass_fail])

    house_df = pd.DataFrame(houses, columns=['Image', 'Partition', 'House Type', 'Weather Condition', 'Type Correct', 'Weather Correct', 'Detection', 'Accuracy', 'Pass/Fail'])
    car_df = pd.DataFrame(cars, columns=['Image', 'Partition', 'Car Type', 'Car Side', 'Type Correct', 'Side Correct', 'Detection', 'Accuracy', 'Pass/Fail'])
    person_df = pd.DataFrame(persons, columns=['Image', 'Partition', 'Activity', 'Number of People', 'Activity Correct', 'Count Correct', 'Detection', 'Accuracy', 'Pass/Fail'])

    house_df = add_summary_row(house_df, ["Type Correct", "Weather Correct"])
    car_df = add_summary_row(car_df, ["Type Correct", "Side Correct"])
    person_df = add_summary_row(person_df, ["Activity Correct", "Count Correct"])

    return house_df, car_df, person_df

def calculate_accuracy(correct_column1, correct_column2):
    correct_count = 0
    total_count = 0

    if correct_column1 == 'Correct':
        correct_count += 1
    total_count += 1

    if correct_column2 == 'Correct':
        correct_count += 1
    total_count += 1

    accuracy = (correct_count / total_count) * 100 if total_count > 0 else 0
    return round(accuracy, 2)

def extract_activity_and_count(analysis):
    activity = None
    count = None

    word_to_number = {
        "one": 1,
        "two": 2,
        "three": 3,
        "four": 4,
        "five": 5,
        "six": 6,
        "seven": 7,
        "eight": 8,
        "nine": 9,
        "ten": 10
    }

    if "activity" in analysis.lower():
        try:
            activity = analysis.split("Activity:")[1].split("Number of People:")[0].strip()
        except IndexError:
            activity = None

    if "number of people" in analysis.lower():
        try:
            count_segment = analysis.split("Number of People:")[1].strip()
            count_word = count_segment.split()[0].lower()  # Get the first word

            count = word_to_number.get(count_word, int(count_word) if count_word.isdigit() else None)
        except (IndexError, ValueError):
            count = None

    if count is None and "object: " in analysis.lower():
        try:
            object_segment = analysis.split("Object:")[1].strip()
            object_word = object_segment.split()[0].lower()
            count = word_to_number.get(object_word, int(object_word) if object_word.isdigit() else None)
        except (IndexError, ValueError):
            count = None

    return activity, count

def extract_car_details(analysis):
    car_type = None
    car_side = None
    if "type" in analysis.lower():
        car_type = analysis.split("Type:")[-1].split("Side Facing:")[0].strip()
    if "side facing" in analysis.lower():
        car_side = analysis.split("Side Facing:")[-1].strip()
    return car_type, car_side

def extract_house_details(analysis):
    house_keywords = ['farmhouse', 'residential', 'modern', 'colonial']
    weather_keywords = ['sunny', 'raining', 'snowing', 'night']

    house_type = next((word for word in house_keywords if word in analysis.lower()), None)
    weather_condition = next((word for word in weather_keywords if word in analysis.lower()), None)

    return house_type, weather_condition

def add_summary_row(df, correct_cols):
    total_rows = len(df)

    correct_counts = {col: df[col].value_counts().get("Correct", 0) for col in correct_cols}

    summary_row = {
        "Image": "Summary",
    }

    for col in correct_cols:
        correct_count = correct_counts.get(col, 0)
        correct_fraction = f"{correct_count}/{total_rows}" if total_rows > 0 else "0/0"
        correct_percentage = f"{(correct_count / total_rows) * 100:.2f}%" if total_rows > 0 else "0.00%"
        summary_row[col] = f"{correct_fraction} ({correct_percentage})"

    pass_count = df['Pass/Fail'].value_counts().get('Pass', 0)
    pass_fail_rate = f"Pass: {pass_count}/{total_rows} ({(pass_count / total_rows) * 100:.2f}%)" if total_rows > 0 else "Pass: 0/0 (0%)"
    summary_row["Pass/Fail"] = pass_fail_rate

    for col in df.columns:
        if col not in summary_row:
            summary_row[col] = ""

    df = pd.concat([df, pd.DataFrame([summary_row])], ignore_index=True)
    return df

def save_and_open_html(html_content, file_name='analysis.html'):
    with open(file_name, 'w') as file:
        file.write(html_content)
    chrome_path = "C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s"
    webbrowser.get(chrome_path).open(f"file://{os.path.abspath(file_name)}")

def main():
    file_path = 'analysis_results.json'
    data = load_json(file_path)
    house_df, car_df, person_df = analyze_data(data)
    html_content = generate_html(house_df, car_df, person_df)
    save_and_open_html(html_content)

if __name__ == "__main__":
    main()