import requests
from requests.exceptions import HTTPError

import time
import datetime

import numpy

import pylab
import matplotlib.pyplot as plt


# Импортируем класс кнопки
from matplotlib.widgets import Button


def LoadData():

    x = []
    y = []
    y1 = []

    response = requests.get('http://192.168.100.239/power')
    response.encoding = 'utf-8'
    if response.status_code == 200:
        title = 'Данные с контроллера ESP8266'
        lp = response.text.split('},{')
    else:
        nameFile = '/home/aou/anaconda3/envs/pythonProject/1.txt'
        title = 'Данные из файла' + nameFile
        fp = open(nameFile, 'r')
        rf = fp.read()

        lp = rf.split("},{")
    for counter, prom in enumerate(lp):

        power_ = prom.split("\"P\":\t")
        power = power_[1].split(".")

        volt_ = prom.split("\"U\":\t")
        volt = volt_[1].split(".")

        time_ = prom.split("\"T\":\t")
        timeUnix = int(time_[1].split(",")[0])
        t = time.localtime(timeUnix)
        d = datetime.datetime(t.tm_year, t.tm_mon, t.tm_mday,
                            t.tm_hour, t.tm_min, t.tm_sec)

        if timeUnix != 0:
            x.append(d)
            y.append(int(power[0]))
            y1.append(int(volt[0]))

    return x,y,y1,title


def addPlot(graph_axes):

    textBusy = pylab.text(-1.6, 6.5, u"Загрузка данных...", family="verdana", fontsize=14, color='g')

    while len(graph_axes.lines) > 0:
        for line in graph_axes.lines:
            line.remove()

    graph_axes.grid(False)

    pylab.draw()
    plt.pause(0.01)



    x, y, y1, title = LoadData()

    textBusy.remove()

    graph_axes.grid(True)


    graph_axes.plot(x, y, x, y1, linestyle='solid', linewidth=2)
    graph_axes.set_title(title, loc='center', pad=2)

    pylab.draw()
    plt.pause(0.1)


if __name__ == '__main__':
    def onButtonAddClicked(event):
        ''' !!! Обработчик события для кнопки "Добавить"'''
        addPlot(graph_axes)

    # Начальные параметры графиков
    current_sigma = 0.2
    current_mu = 0.0

    # Создадим окно с графиком
    fig, graph_axes = pylab.subplots()
    graph_axes.grid()

    graph_axes.set_ylabel('Вольты, Ватты')

    # graph_axes.yaxis.set_label_text('Вольты, Ватты')
    fig.autofmt_xdate()


    # Оставим снизу от графика место для виджетов
    fig.subplots_adjust(left=0.1, right=0.95, top=0.95, bottom=0.2)

    # Создадим ось для кнопки
    axes_button_add = pylab.axes([0.7, 0.05, 0.25, 0.075])

    # Создание кнопки
    button_add = Button(axes_button_add, 'Обновить')

    # !!! Подпишемся на событие обработки нажатия кнопки
    button_add.on_clicked(onButtonAddClicked)

    # plt.ylabel("Ватты, Вольты", fontsize=10, labelpad=20)  # ось ординат

    pylab.rcParams.update({'font.size': 16})
    pylab.tick_params(axis='both', which='major', labelsize=26)

    addPlot(graph_axes)

    pylab.show()
