from flask import Flask, request, jsonify, render_template_string, redirect

app = Flask(__name__)

correct_answers = {
    "stage_1": 1,
    "stage_2": 0,
    "stage_3": "Hello World",
    "stage_4": 2,
    "stage_5": 1
}

info_message = {
    "stage_1": """
    Етап 1: Загадковий портал
    На самому початку пригоди команда стикається з великим кам'яним порталом, 
    який блокував шлях у магічний ліс. 
    Щоб активувати портал, необхідно знайти "магічний код" 
    і виконати операцію XOR на послідовності чисел, які заховані в загадках.      
    """,
    "stage_2": """Етап 2: "Мости ельфів" Команда проходить через ліс і натрапляє на три мости, 
    кожен з яких веде до різного напрямку. Перший міст виглядає старим і вкритий мохом, другий — 
    зроблений із блискучого металу, а третій — дерев'яний і скрипучий. Один із мостів безпечний, 
    а два інших ведуть до орків, які не пропустять далі без бою.""",
    "stage_3": """Команда потрапляє до печери, де гноми заховали давній кристал мудрості, 
    який дає силу бачити приховане. Щоб отримати кристал, необхідно розшифрувати повідомлення, яке було закодоване.
    Напись на скелі: Khoor Zruog""",
    "stage_4": """Етап 4: "Магічний лабіринт орків" Орки заховали ключ від фортеці у магічному лабіринті, який можна 
    подолати, лише вирішивши загадку. Лабіринт заплутаний і наповнений ілюзіями, що збивають з пантелику навіть 
    найсміливіших героїв. Його стіни постійно змінюють своє розташування, а двері відкриваються лише за умови 
    правильного вирішення головоломок.""",
    "stage_5": """Етап 5: "🗝️ Три магічні скрині" У фортеці орків знаходяться три магічні скрині, 
    одна з яких містить 👑. Кожна скриня має напис, але лише один з написів говорить правду. Завдання команди — 
    знайти скриню з 👑, використовуючи логічний аналіз написів."""
}

info_message_task = {
    "stage_1": """Підказка:
    Гноми знайшли давній сувій, де описано, як працює XOR. Вводити потрібно лише одне число
    3, 5, 7""",
    "stage_2": """Підказка: Уважно прочитайте написи на старовинних табличках — 
    вони містять підказки, що допоможуть обрати правильний міст.
    bridge_signs = ["безпека", "небезпека", "небезпека"]""",
    "stage_3": """Підказка: Гай Юлій. offset=3, ASCII: 65 """,
    "stage_4": """doors = ["зачинено", "зачинено", "відчинено", "зачинено", "зачинено", "відчинено"]
    """,
    "stage_5": """Підказка: Лише один напис говорить правду, а решта — брехня.
     Використовуйте логічні оператори для вирішення.
     chests = ["👑 тут", "👑 не тут", "👑 не в першій скрині"]"""
}

final_scene = """Після того як всі перешкоди подолані, а двері відкриті, команда знаходить корону і повертає 
її до Старого Королівства. Люди зустрічають героїв з радістю, влаштовуючи велике святкування на 
честь їхнього повернення. Гноми, які допомагали в дорозі, відчувають гордість за свою мудрість і сміливість, 
а орки, усвідомивши цінність співпраці, обіцяють більше не заважати іншим народам. Усі мешканці Старого Королівства 
об'єднуються навколо корони, щоб разом будувати мирне майбутнє. Навіть колишні вороги тиснуть один одному руки, 
усвідомлюючи, що тільки разом вони можуть подолати будь-які труднощі. Люди, гноми та навіть орки вирішують більше 
не сваритися та жити в мирі, адже тепер вони знають, що співпраця — найкраща магія."""

losse_scene = """Нажаль ви втрачаєте одного з учасників. Оберіть хто це буде цього разу"""

start_message = """Давним-давно, коли люди, гноми та орки ще співіснували разом на території Старого Королівства, 
настала велика біда: корону магічного короля було вкрадено орками-злодіями. Корона давала людям і 
гномам можливість мирно співіснувати, даруючи добробут і магічну силу всім, хто її охороняє. 
І тепер три команди відважних героїв — гноми, орки та люди — повинні пройти через магічний ліс, 
подолати перешкоди й розв'язати складні загадки, щоб повернути корону і відновити мир
"""

HTML_TEMPLATE = """
<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <title>Крізь магічний ліс</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f0f8ff;
            color: #333;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
        }
        .container {
            background: #ffffff;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            text-align: center;
            max-width: 500px;
        }
        h1 {
            color: #007bff;
        }
        .message {
            font-size: 1.2em;
            margin-top: 20px;
        }
        .correct {
            color: #28a745;
        }
        .incorrect {
            color: #dc3545;
        }
        form {
            margin-top: 20px;
        }
        input[type="text"] {
            padding: 10px;
            font-size: 1em;
            width: 80%;
            margin-bottom: 10px;
        }
        input[type="submit"] {
            padding: 10px 20px;
            font-size: 1em;
            background-color: #007bff;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }
        input[type="submit"]:hover {
            background-color: #0056b3;
        }
        .info {
            margin-top: 10px;
            font-style: italic;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Крізь Магічний Ліс</h1>
        <div class="info">
            {{ info_message }} <br>
            <b>{{ info_message_task }}</b>
        </div>
        <img src="{{ image_path }}" alt="Stage Image" width="100%">
        <div class="message {{ message_class }}">
            {{ result_message }}
        </div>
        <form method="post">
            <input type="text" name="answer" placeholder="Enter your answer here" required>
            <input type="submit" value="Submit">
        </form>
    </div>
</body>
</html>
"""

HTML_TEMPLATE_START = """
<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <title>Крізь магічний ліс</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f0f8ff;
            color: #333;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
        }
        .container {
            background: #ffffff;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            text-align: center;
            max-width: 500px;
        }
        h1 {
            color: #007bff;
        }
        .message {
            font-size: 1.2em;
            margin-top: 20px;
        }
        .correct {
            color: #28a745;
        }
        .incorrect {
            color: #dc3545;
        }
        form {
            margin-top: 20px;
        }
        input[type="text"] {
            padding: 10px;
            font-size: 1em;
            width: 80%;
            margin-bottom: 10px;
        }
        input[type="submit"] {
            padding: 10px 20px;
            font-size: 1em;
            background-color: #007bff;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }
        input[type="submit"]:hover {
            background-color: #0056b3;
        }
        .info {
            margin-top: 10px;
            font-style: italic;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Крізь Магічний Ліс</h1>
        <div class="info">
            {{ info_message }} <br>
            <b>{{ info_message_task }}</b>
        </div>
        <img src="{{ image_path }}" alt="Stage Image" width="100%">
        <div class="message {{ message_class }}">
            {{ result_message }}
        </div>
       <form action="/stage_1" method="get">
            <input type="submit" value="Перейти на 1 етап">
        </form>
    </div>
</body>
</html>
"""

HTML_TEMPLATE_LOOSE = """
<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <title>Крізь магічний ліс</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f0f8ff;
            color: #333;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
        }
        .container {
            background: #ffffff;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            text-align: center;
            max-width: 500px;
        }
        h1 {
            color: #007bff;
        }
        .message {
            font-size: 1.2em;
            margin-top: 20px;
        }
        .correct {
            color: #28a745;
        }
        .incorrect {
            color: #dc3545;
        }
        form {
            margin-top: 20px;
        }
        input[type="text"] {
            padding: 10px;
            font-size: 1em;
            width: 80%;
            margin-bottom: 10px;
        }
        input[type="submit"] {
            padding: 10px 20px;
            font-size: 1em;
            background-color: #007bff;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }
        input[type="submit"]:hover {
            background-color: #0056b3;
        }
        .info {
            margin-top: 10px;
            font-style: italic;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Крізь Магічний Ліс</h1>
        <div class="info">
            {{ info_message }} <br>
            <b>{{ info_message_task }}</b>
        </div>
        <img src="{{ image_path }}" alt="Stage Image" width="100%">
        <div class="message {{ message_class }}">
            {{ result_message }}
        </div>
         <form action="{{ request.path }}" method="get">
            <input type="submit" value="Повернутися назад">
        </form>
    </div>
</body>
</html>
"""

@app.route("/")
def start():
    return render_template_string(HTML_TEMPLATE_START, result_message="", message_class="",
                                  info_message=start_message,
                                  info_message_task="",
                                  image_path="/static/images/start.webp")

@app.route('/stage_1', methods=['GET', 'POST'])
def stage_1():
    if request.method == 'GET':
        return render_template_string(HTML_TEMPLATE, result_message="", message_class="",
                                      info_message=info_message.get("stage_1"),
                                      info_message_task=info_message_task.get("stage_1"),
                                      image_path="/static/images/1stage.webp")
    user_answer = int(request.form.get('answer'))
    if user_answer == correct_answers['stage_1']:
        return redirect('/stage_2')
    return render_template_string(HTML_TEMPLATE_LOOSE, result_message="Incorrect. Try again. 😢", message_class="incorrect",
                                  info_message=losse_scene,
                                  info_message_task="",
                                  image_path="/static/images/losse.webp"), 400


@app.route('/stage_2', methods=['GET', 'POST'])
def stage_2():
    if request.method == 'GET':
        return render_template_string(HTML_TEMPLATE, result_message="", message_class="",
                                      info_message=info_message.get("stage_2"),
                                      info_message_task=info_message_task.get("stage_2"),
                                      image_path="/static/images/2stage.webp")
    user_answer = int(request.form.get('answer'))
    if user_answer == correct_answers['stage_2']:
        return redirect('/stage_3')
    return render_template_string(HTML_TEMPLATE_LOOSE, result_message="Incorrect. Try again. 😢", message_class="incorrect",
                                  info_message="Ви втратили одного члена команди. Спробуйте ще раз",
                                  info_message_task="",
                                  image_path="/static/images/losse.webp"), 400


@app.route('/stage_3', methods=['GET', 'POST'])
def stage_3():
    if request.method == 'GET':
        return render_template_string(HTML_TEMPLATE, result_message="", message_class="",
                                      info_message=info_message.get("stage_3"),
                                      info_message_task=info_message_task.get("stage_3"),
                                      image_path="/static/images/3stage.webp")
    user_answer = str(request.form.get('answer'))
    if user_answer == correct_answers['stage_3']:
        return redirect('/stage_4')
    return render_template_string(HTML_TEMPLATE_LOOSE, result_message="Incorrect. The guards block your way. 😢",
                                  message_class="incorrect",
                                  info_message="Ви втратили одного члена команди. Спробуйте ще раз",
                                  info_message_task="",
                                  image_path="/static/images/losse.webp"), 400


@app.route('/stage_4', methods=['GET', 'POST'])
def stage_4():
    if request.method == 'GET':
        return render_template_string(HTML_TEMPLATE, result_message="", message_class="",
                                      info_message=info_message.get("stage_4"),
                                      info_message_task=info_message_task.get("stage_4"),
                                      image_path="/static/images/4stage.webp")
    user_answer = int(request.form.get('answer'))
    if user_answer == correct_answers['stage_4']:
        return redirect('/stage_5')
    return render_template_string(HTML_TEMPLATE_LOOSE, result_message="Incorrect. You are sent back to the start of the labyrinth. 😢",
                                  message_class="incorrect",
                                  info_message="Ви втратили одного члена команди. Спробуйте ще раз",
                                  info_message_task="",
                                  image_path="/static/images/losse.webp"), 400

@app.route('/stage_5', methods=['GET', 'POST'])
def stage_5():
    if request.method == 'GET':
        return render_template_string(HTML_TEMPLATE, result_message="", message_class="",
                                      info_message=info_message.get("stage_5"),
                                      info_message_task=info_message_task.get("stage_5"),
                                      image_path="/static/images/5stage.webp")
    user_answer = int(request.form.get('answer'))
    if user_answer == correct_answers['stage_5']:
        return redirect('/final')
    return render_template_string(HTML_TEMPLATE_LOOSE,
                                  result_message="Incorrect. The chest is empty. 😢",
                                  message_class="incorrect",
                                  info_message="Ви втратили одного члена команди. Спробуйте ще раз",
                                  info_message_task="",
                                  image_path="/static/images/losse.webp"), 400

@app.route('/final')
def stage_6():
    return render_template_string(HTML_TEMPLATE, result_message="You win!",
                                  message_class="correct",
                                  info_message=final_scene,
                                  info_message_task="",
                                  image_path="/static/images/end.webp"), 200

if __name__ == '__main__':
    app.run(port=30000, debug=True)
