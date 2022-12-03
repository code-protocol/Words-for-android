import time

from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
import pickle
import random
import datetime
import os

Window.size = (480, 853)

from kivy.config import Config

Config.set('kivy', 'keyboard_mode', 'systemanddock')

count = 0
words = []
word = []
Files = ['1000', 'All', 'Learn', 'Repeat']


def getConfig():
    """getConfig(masFiles)

    Returns the configuration and checks it for correctness
    """

    if not os.path.isfile('config.pickle'):
        file = open('config.pickle', 'wb')
        deafult = {
            "file": 'Learn',
            "repetition": False,
            "numbering": True,
            "translation": 'EN',
            "writing": False,
            'date': datetime.date(2001, 1, 1),
            'num': 0
        }
        pickle.dump(deafult, file)
        file.close()

    file = open('config.pickle', 'rb')
    config = pickle.load(file)
    file.close()
    print(config)
    return config


def saveConfig(config):
    """saveConfig(config)

    Saves the configuration
    """

    file = open('config.pickle', 'wb')
    pickle.dump(config, file)
    file.close()


# datetime.datetime.date(datetime.datetime.today())
def getMas(fileName, num):
    """Returns an array [word / translation] from the specified file"""
    f = open(f'words\\{fileName}.txt', 'r', encoding="utf-8")
    temp = f.readlines()
    f.close()

    txt = []
    for i in temp:
        txt += [[str(i[0:i.find('|')]).strip(), str(i[i.find('|') + 1:].replace('\n', '')).strip()]]

    # finalTxt = []
    # for i in range(num, num + 10):
    #     finalTxt += [txt[i]]
    return txt


def separateWords(mas):
    txt = []
    for item in mas:
        word = item[0]
        translate = item[1]
        txt += [{'EN': word, 'UA': translate}]
    return txt


def next_(obj):
    num = random.randint(0, len(words) - 1)
    word.clear()
    if config['repetition']:
        word.append(words[num])
    else:
        word.append(words.pop(num))
    obj.label_widget.text = word[0][config['translation']]
    obj.label_count.text = str(int(obj.label_count.text) + 1)


config = getConfig()
words = separateWords(getMas(config['file'], config['num']))

# config['date'] = datetime.date(2022, 12, 2)
# saveConfig(config)


# config = getConfig()
# print(words)
today = datetime.datetime.date(datetime.datetime.today() + datetime.timedelta(days=3))


def check_date():
    if today != config['date']:
        if config['date'] != datetime.date(2001, 1, 1):
            config['num'] += 10
        config['date'] = today
        saveConfig(config)
        f = open(f'words\\1000.txt', 'r', encoding="utf-8")
        temp = f.readlines()
        f.close()

        txt = ''
        for i in range(config['num'], config['num'] + 10):
            txt += temp[i]

        file = open('words\\Learn.txt', 'w', encoding="utf-8")
        file.write(txt)
        file.close()
        REFile()
        initialRe()


def REFile():
    """REFile()

    Creates a Re file from "[ LEARN ]" and adds it to the ReList
    """

    if not os.path.isfile('REList.pickle'):
        file = open('REList.pickle', 'wb')

        REList = {
            "updateDate": today,
            "list": []
        }

        pickle.dump(REList, file)
        file.close()

    file = open('words\\Learn.txt', 'r', encoding="utf-8")
    text = file.readlines()
    file.close()

    fileName = getLastFileName() + 1
    file = open(f'RE\\{fileName}.txt', 'w', encoding="utf-8")
    for i in text:
        file.write(i)
    file.close()

    saveInfoReFile()
    initialALL()


def saveInfoReFile():
    """saveInfoReFile(fileName)
    fileName - file name

    Adds a file to the ReList
    """

    file = open('REList.pickle', 'rb')
    REList = pickle.load(file)
    file.close()

    REList['list'] = REList['list'] + [[today, 1, getLastFileName()]]

    file = open('REList.pickle', 'wb')
    pickle.dump(REList, file)
    file.close()


def getLastFileName():
    """getLastFileName()

    Returns the number of the last file
    """

    myList = os.listdir(os.getcwd() + '\RE')
    if myList == []:
        return 0

    for i in range(0, len(myList)):
        myList[i] = int(myList[i].replace('.txt', ''))

    return max(myList)


def initialALL():
    """initialALL(text)

    Adds text to the "[ ALL ]" file
    """

    allText = ''
    for i in range(1, getLastFileName() + 1):
        try:
            file = open(f'RE\\{i}.txt', 'r', encoding="utf-8")
            txt = file.readlines()
            for word in txt:
                allText += word
            file.close()
        except:
            continue

    file = open('words\\All.txt', 'w', encoding="utf-8")
    file.write(allText)
    file.close()


def initialRe():
    """initialRe()

    Initializes the file "[ RE ]" according to the dates of the file "ReList"
    """
    updateReList()

    filesToRe = getReFilesForToday()

    text = getTextFromFiles(filesToRe)

    file = open('words\\Repeat.txt', 'w')
    file.write(text)
    file.close()


def updateReList():
    """updateReList()

    Updates data in REList
    """

    file = open('REList.pickle', 'rb')
    REList = pickle.load(file)
    file.close()

    if today != REList['updateDate']:
        for item in REList['list']:
            plusDay = datetime.timedelta(days=int(item[1]))
            dateToRe = item[0]
            newDateToRe = item[0] + plusDay

            if dateToRe < today:
                item[0] = newDateToRe
                item[1] *= 2
        REList['updateDate'] = today

    file = open('REList.pickle', 'wb')
    pickle.dump(REList, file)
    file.close()


def getReFilesForToday():
    """getReFilesNameForToday(mas)
    mas - list of ReList objects

    Returns a list of filenames to repeat
    """

    file = open('REList.pickle', 'rb')
    REList = pickle.load(file)
    file.close()

    sort = []
    for item in REList['list']:
        if item[0] <= today:
            sort += [item[2]]
    return sort


def getTextFromFiles(files):
    """getTextFromFiles(files)

    Returns text from files
    """

    text = ''
    for file in files:
        file = open(f'RE\\{file}.txt', 'r')
        for txt in file.readlines():
            text += str(txt)
        file.close()
    return text


check_date()
time.sleep(2)

class Container(GridLayout):

    def check_word(self):
        if config['writing'] and self.label_widget.text != 'Press for reset':
            if config['translation'] == 'EN':
                if self.enterworld.text == word[0]['UA']:
                    self.label_widget.background_color = (0, 0, 0)
                    self.enterworld.text = ''
                    self.next()
                else:
                    self.label_widget.background_color = (1, 0, 0, 1)
            else:
                if self.enterworld.text == word[0]['EN']:
                    self.label_widget.background_color = (0, 0, 0)
                    self.enterworld.text = ''
                    self.next()
                else:
                    self.label_widget.background_color = (1, 0, 0, 1)
        else:
            self.label_widget.background_color = (0, 0, 0)
            self.next()

    def next(self):
        print(words)
        if len(words) == 0:
            if self.label_widget.text == 'Press for reset':
                words.clear()
                f = separateWords(getMas(config['file'], config['num']))
                for i in range(0, len(f)):
                    words.append(f[i])
                self.label_count.text = '0'

                if len(words):
                    next_(self)
            else:
                self.label_widget.text = 'Press for reset'
                self.label_count.text = '0'
        else:
            next_(self)

    def translate(self):
        if config['translation'] == 'EN':
            config['translation'] = 'UA'
        else:
            config['translation'] = 'EN'
        self.label_translate.text = 'Translate: ' + config['translation']
        if len(word):
            self.label_widget.text = word[0][config['translation']]

    def check_repetition(self):
        if config['repetition']:
            config['repetition'] = False
            self.label_repetition.text = 'Repetition: OFF'
        else:
            config['repetition'] = True
            self.label_repetition.text = 'Repetition: ON'
        words.clear()
        f = separateWords(getMas(config['file'], config['num']))
        for i in range(0, len(f)):
            words.append(f[i])

    def check_writing(self):
        if config['writing']:
            self.label_enterworld_size.size_hint = 1, 0
            self.label_writing.text = 'Writing: OFF'
            config['writing'] = False
        else:
            self.label_enterworld_size.size_hint = 1, 0.1
            self.label_writing.text = 'Writing: ON'
            config['writing'] = True

    def check_file(self):
        if Files.index(config['file']) + 1 == len(Files):
            self.label_file.text = 'File: ' + Files[0]
            config['file'] = Files[0]
        else:
            self.label_file.text = 'File: ' + Files[Files.index(config['file']) + 1]
            config['file'] = Files[Files.index(config['file']) + 1]
        word.clear()
        words.clear()
        self.next()


class MyApp(App):
    def build(self):
        return Container()


if __name__ == '__main__':
    MyApp().run()

# background_color: (0,1,0,1) - green
