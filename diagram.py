import json
import os
import matplotlib.pyplot as plt
from time import sleep

users_path = 'users'
png_path = 'png'
test_json = {"1": {"Каким транспортом вы пользуетесь?": {"Автомобиль с ДВС": 0, "Электромобиль": 0, "Элктросамокат": 0, "Велосипед": 0, "Общественный транспорт": 0}},
             "2": {"Сортируете ли мусор?": {"нет": 0, "да": 0, "иногда": 0}},
             "3": {"Вы едите мясо/ молочные продукты": {"нет": 0, "да": 0, "я на пути к вегетарианству": 0}},
             "4": {"Как часто вы совершаете перелёты": {"1 раз в год": 0, "2-3 раза в год": 0, "более 3х раз в год": 0}},
             "5": {"У вас есть дома пакет с пакетами? Только честно конечно": {"да": 0, "нет": 0, "только бумажный пакет с пакетами": 0, "я давно хожу с эко-пакетом по магазинам": 0}},
             "6": {"В кофейне вы берете стакан с собой?": {"да": 0, "нет": 0, "я всегда со своей термокружкой": 0}},
             "7": {"Вы когда-нибудь были в секонд-хенд?": {"да, даже покупал": 0, "нет": 0, "заходил для интереса": 0}},
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
                    result_dict[count][question][answer] += value
    result_dict.pop('Счетчик')

    for count, value in result_dict.items():
        file_path = os.path.join(png_path, f"{count}.png")
        question = list(value.keys())[0]
        labels = list(value.get(question).keys())
        values = list(value.get(question).values())

        fig1, ax1 = plt.subplots()
        plt.title(question)
        ax1.pie(values, labels=labels)
        wedges, texts, autotexts = ax1.pie(values, labels=labels, autopct='%1.2f%%')
        ax1.axis('equal')
        # ax1.legend(loc='upper left', bbox_to_anchor=(1.0, 1.0))
        plt.savefig(file_path)
        sleep(2)
        print(file_path)


if __name__ == "__main__":
    main()