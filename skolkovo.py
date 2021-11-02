import telebot
import json
import os
from diagram import main

path = 'bot'
users_path = 'users'
png_path = 'png'


def read_json_from_file(file_name, path=path):
    """Считывание данных из файла
    """

    file_path = os.path.join(path, file_name)
    with open(file_path, encoding='utf-8') as json_file:
        data = json.load(json_file)

    return json.loads(json.dumps(data, ensure_ascii=False))


def write_json(file_name, data_json, path=path):
    """Запись данных в файл
    """

    file_path = os.path.join(path, file_name)
    with open(file_path, 'w', encoding='utf-8') as json_file:
        json.dump(data_json, json_file)


config_dict = read_json_from_file('config.json')
TOKEN_API = config_dict.get('token')
test_json = {"1": {"Каким транспортом вы пользуетесь?": {"Автомобиль с ДВС": 0, "Электромобиль": 0, "Элктросамокат": 0, "Велосипед": 0, "Общественный транспорт": 0}},
             "2": {"Сортируете ли мусор?": {"нет": 0, "да": 0, "иногда": 0}},
             "3": {"Вы едите мясо/ молочные продукты": {"нет": 0, "да": 0, "я на пути к вегетарианству": 0}},
             "4": {"Как часто вы совершаете перелёты": {"1 раз в год": 0, "2-3 раза в год": 0, "более 3х раз в год": 0}},
             "5": {"У вас есть дома пакет с пакетами? Только честно конечно": {"да": 0, "нет": 0, "только бумажный пакет с пакетами": 0, "я давно хожу с эко-пакетом по магазинам": 0}},
             "6": {"В кофейне вы берете стакан с собой?": {"да": 0, "нет": 0, "я всегда со своей термокружкой": 0}},
             "7": {"Вы когда-нибудь были в секонд-хенд?": {"да, даже покупал": 0, "нет": 0, "заходил для интереса": 0}},
             "Счетчик": 0}

bot = telebot.TeleBot(TOKEN_API)


@bot.message_handler(commands=['start'])
def handel_start(message):
    _id = message.from_user.id
    file_name = f"{str(_id)}.json"
    if not (file_name in os.listdir(users_path)):
        write_json(file_name, test_json, users_path)
    user_markup = telebot.types.ReplyKeyboardMarkup(True, True)
    user_markup.row('Начать')
    bot.send_message(_id, "Пройти опрос", reply_markup=user_markup)


@bot.message_handler(commands=['result'])
def handel_doc(message):
    # main()
    _id = str(message.from_user.id)
    save_diagram(_id=_id)


@bot.message_handler(commands=['show'])
def handel_text(message):
    _id = message.from_user.id

    file_name = f"{str(_id)}.json"
    item = read_json_from_file(file_name, users_path)
    bot.send_message(_id, "Ваши ответы")
    bot.send_message(_id, str(item))


@bot.message_handler(content_types=['text'])
def handel_text(message):
    _id = message.from_user.id

    file_name = f"{str(_id)}.json"
    if not (file_name in os.listdir(users_path)):
        write_json(file_name, test_json, users_path)
    item = read_json_from_file(file_name, users_path)
    msg = message.text

    if msg == "Начать":
        item['Счетчик'] = 1
        write_json(file_name, item, users_path)

    question_item = item.get(str(item['Счетчик']))
    question = list(question_item.keys())[0]
    user_markup = telebot.types.ReplyKeyboardMarkup(True, True)
    for elem in question_item.get(question):
        user_markup.row(elem)
    send = bot.send_message(_id, question, reply_markup=user_markup)
    bot.register_next_step_handler(send, add_answer, question=question, item=item, count=item['Счетчик'], file_name=file_name)


def add_answer(message, question=None, item=None, count=None, file_name=None):
    _id = message.from_user.id
    item[str(count)][question][message.text] += 1
    item['Счетчик'] += 1
    write_json(file_name, item, users_path)
    if item['Счетчик'] > 7:
        item['Счетчик'] = 1
        write_json(file_name, item, users_path)
        bot.send_message(_id, "Опрос завершен")
    else:
        user_markup = telebot.types.ReplyKeyboardMarkup(True, True)
        user_markup.row("Следующий вопрос")
        bot.send_message(_id, "Ваш ответ учтен", reply_markup=user_markup)


def save_diagram(_id):
    result_dict = test_json
    result_dict.pop('Счетчик')

    for count, value in result_dict.items():
        file_path = os.path.join(png_path, f"{count}.png")
        with open(file_path, 'rb') as f:
            bot.send_photo(_id, f)


if __name__ == "__main__":
    try:
        bot.polling(none_stop=True)
    except Exception as inst:
        print('Какая то ошибка: ', inst)
