import json
import os
import matplotlib.pyplot as plt
from time import sleep

users_path = 'users'
png_path = 'png'
test_json = {"1": {"Каким транспортом вы пользуетесь?": {"Автомобиль с ДВС": {"val": 0, "color": "#ff9999"}, "Электромобиль": {"val": 0, "color": "#99ff99"}, "Элктросамокат": {"val": 0, "color": "#ffcc99"}, "Велосипед": {"val": 0, "color": "#66b3ff"}, "Общественный транспорт": {"val": 0, "color": "#999999"}}},
             "2": {"Сортируете ли мусор?": {"нет": {"val": 0, "color": "#ff9999"}, "да": {"val": 0, "color": "#99ff99"}, "иногда": {"val": 0, "color": "#ffcc99"}}},
             "3": {"Вы едите мясо/ молочные продукты": {"нет": {"val": 0, "color": "#99ff99"}, "да": {"val": 0, "color": "#ff9999"}, "я на пути к вегетарианству": {"val": 0, "color": "#ffcc99"}}},
             "4": {"Как часто вы совершаете перелёты": {"1 раз в год": {"val": 0, "color": "#99ff99"}, "2-3 раза в год": {"val": 0, "color": "#ffcc99"}, "более 3х раз в год": {"val": 0, "color": "#ff9999"}}},
             "5": {"У вас есть дома пакет с пакетами? Только честно конечно": {"да": {"val": 0, "color": "#ff9999"}, "нет": {"val": 0, "color": "#66b3ff"}, "только бумажный пакет с пакетами": {"val": 0, "color": "#ffcc99"}, "я давно хожу с эко-пакетом по магазинам": {"val": 0, "color": "#99ff99"}}},
             "6": {"В кофейне вы берете стакан с собой?": {"да": {"val": 0, "color": "#ff9999"}, "нет": {"val": 0, "color": "#ffcc99"}, "я всегда со своей термокружкой": {"val": 0, "color": "#99ff99"}}},
             "7": {"Вы когда-нибудь были в секонд-хенд?": {"да, даже покупал": {"val": 0, "color": "#99ff99"}, "нет": {"val": 0, "color": "#ff9999"}, "заходил для интереса": {"val": 0, "color": "#ffcc99"}}},
             "Счетчик": 0}


def read_json_from_file(file_name, path=users_path):
    """Считывание данных из файла
    """

    file_path = os.path.join(path, file_name)
    with open(file_path, encoding='utf-8') as json_file:
        data = json.load(json_file)

    return json.loads(json.dumps(data, ensure_ascii=False))


def main():
    result_dict = test_json
    for elem in os.listdir(users_path):
        read_file = read_json_from_file(elem, users_path)
        read_file.pop('Счетчик')
        for count, questions in read_file.items():
            for question, answers in questions.items():
                for answer, value in answers.items():
                    result_dict[count][question][answer]['val'] += value
    result_dict.pop('Счетчик')

    for count, value in result_dict.items():
        file_path = os.path.join(png_path, f"{count}.png")
        question = list(value.keys())[0]
        labels = list(value.get(question).keys())
        values = [elem.get("val") for elem in list(value.get(question).values())]
        colors = [elem.get("color") for elem in list(value.get(question).values())]

        fig1, ax1 = plt.subplots()
        plt.title(question)
        ax1.pie(values, labels=labels)
        wedges, texts, autotexts = ax1.pie(values, labels=labels, autopct='%1.2f%%', colors=colors)
        ax1.axis('equal')
        # ax1.legend(loc='upper left', bbox_to_anchor=(1.0, 1.0))
        plt.savefig(file_path)
        sleep(2)
        print(file_path)


if __name__ == "__main__":
    main()