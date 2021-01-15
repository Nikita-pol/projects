import datetime
import os
import shutil
from random import randint
from math import sqrt

# import requests
import discord
from discord.ext import commands

from config import settings
prefix = settings['prefix']

bot = commands.Bot(command_prefix=settings['prefix'])
playWords = False
playKMN = False
end = False
math_answer = 0
riddle_answer = 0
math, riddle = False, False
user, right = '', ''
debug = 0


@bot.event
async def on_ready():
    print("Ready")
    channel = bot.get_channel(793390527328419843)
    # await channel.send("Готов к работе.")


@bot.event
async def on_message(message):
    print(message)
    print(message.author.name)
    print(message.content)
    global playWords, playKMN, qsl, playerKmn, user, right, math_answer, debug, prefix, riddle_answer, math, riddle
    mc = message.content
    msgAuthor = message.author.name
    word = message.content
    try:
        file = open("Users\\" + msgAuthor + "\\words.txt", "r")
        w = file.read()
        file = open("Users\\" + msgAuthor + "\\words.txt", "w")
        file.write(str(int(w) + len(word)))
        file = open("Users\\" + msgAuthor + "\\level.txt", "r")
        lvl = file.read()
        if int(w) + len(word) >= (int(lvl) ** 2) * 100:
            file = open("Users\\" + msgAuthor + "\\level.txt", "w")
            file.write(str(int(lvl) + 1))
            file = open("Users\\" + msgAuthor + "\\words.txt", "w")
            file.write(str((int(w) + len(word)) - ((int(lvl) ** 2) * 100)))
            file.close()
            embed = discord.Embed(
                title='Поздравляем!',
                description=msgAuthor + " достиг " + str(int(lvl) + 1) + " уровня.",
                colour=discord.Colour.from_rgb(80, 125, 229))
            await message.channel.send(embed=embed)
    except FileNotFoundError:
        os.mkdir("Users\\" + msgAuthor)
        file = open("Users\\" + msgAuthor + "\\words.txt", "a+")
        file.write(str(len(word)))
        file.close()
        file = open("Users\\" + msgAuthor + "\\level.txt", "a+")
        file.write("1")
        file.close()

    if mc[0] == prefix:
        if mc[1:] == "reload_levels":
            admin = False
            for i in message.author.roles:
                if str(i) == "Админ":
                    admin = True
                    for root, dirs, files in os.walk("Users"):
                        if root != "Users":
                            path = os.path.join(os.path.abspath(os.path.dirname(__file__)), root)
                            shutil.rmtree(path)
                    embed = discord.Embed(
                        title='Успешно!',
                        description="Все уровни активности сброшены до 0.",
                        colour=discord.Colour.from_rgb(80, 125, 229))
                    await message.channel.send(embed=embed)
                if not admin:
                    embed = discord.Embed(
                        title='Ошибка!',
                        description="Недостаточно прав.\nСначала получите роль админа.",
                        colour=discord.Colour.from_rgb(80, 125, 229))
                    await message.channel.send(embed=embed)

        if "reload_for " == mc[:12]:
            admin = False
            for i in message.author.roles:
                if str(i) == "Админ":
                    admin = True
                    try:
                        root = "Users\\" + mc[12:]
                        path = os.path.join(os.path.abspath(os.path.dirname(__file__)), root)
                        shutil.rmtree(path)
                        embed = discord.Embed(
                            title='Успешно!',
                            description="Уровень активности для " + mc[12:] + " сброшен.",
                            colour=discord.Colour.from_rgb(80, 125, 229))
                        await message.channel.send(embed=embed)
                    except FileNotFoundError:
                        embed = discord.Embed(
                            title='Ошибка!',
                            description="Пользователя с таким именем не существует или его уровень активности равен 0.",
                            colour=discord.Colour.from_rgb(80, 125, 229))
                        await message.channel.send(embed=embed)
            if not admin:
                embed = discord.Embed(
                    title='Ошибка!',
                    description="Недостаточно прав.\nСначала получите роль админа.",
                    colour=discord.Colour.from_rgb(80, 125, 229))
                await message.channel.send(embed=embed)

        if mc[1:14] == "change_prefix":
            admin = False
            for i in message.author.roles:
                if str(i) == "Админ":
                    admin = True
                    file = open("files\\prefix.txt", "w")
                    file.write(mc[15:])
                    file.close()
                    prefix = mc[15:]
                    print(prefix)
                    embed = discord.Embed(
                        title='Успешно!',
                        description="Префикс сменен на " + mc[15:],
                        colour=discord.Colour.from_rgb(80, 125, 229))
                    await message.channel.send(embed=embed)
            if not admin:
                embed = discord.Embed(
                    title='Ошибка!',
                    description="Недостаточно прав.\nСначала получите роль админа.",
                    colour=discord.Colour.from_rgb(80, 125, 229))
                await message.channel.send(embed=embed)

        if mc[1:] == "restart":
            admin = False
            for i in message.author.roles:
                if str(i) == "Админ":
                    admin = True
                    await message.channel.send("Перезагрузка...")
                    os.system("reset.py")
                    exit(0)
            if not admin:
                embed = discord.Embed(
                    title='Ошибка!',
                    description="Недостаточно прав.\nСначала получите роль админа.",
                    colour=discord.Colour.from_rgb(80, 125, 229))
                await message.channel.send(embed=embed)

        if mc[1:] == "show_levels":
            content = ""
            for root, dirs, files in os.walk("Users"):
                if root != "Users":
                    file = open(root + "\\level.txt", "r")
                    lvl = file.read()
                    file = open(root + "\\words.txt", "r")
                    content += root[6:] + " -- " + lvl + " уровень; " + file.read() + " очков.\n"
                    file.close()
            embed = discord.Embed(
                title='Уровни активности на сервере',
                description=content,
                colour=discord.Colour.from_rgb(80, 125, 229))
            await message.channel.send(embed=embed)

        if mc[1:] == "show_time":
            embed = discord.Embed(
                title='Московское время',
                description="Сегодня " + datetime.datetime.today().strftime("%d.%m.%Y") +
                                       "\nВремя " + datetime.datetime.today().strftime("%H:%M:%S"),
                colour=discord.Colour.from_rgb(80, 125, 229))
            await message.channel.send(embed=embed)

        elif "go_play " == mc[:9]:
            #if mc[9:] == "Виселица":
            #    global sl, s, debug
            #    debug = 0
            #    await message.channel.send("Началась игра \"Виселица\" c пользователем " + msgAuthor)
            #    playWords = True
            #    qsl = msgAuthor
            #    word = ['макака', 'мухобойка', 'собака', 'экспедиция', 'революция', 'авиатор', 'сентенция',
            #            'сенокосилка', 'пиццерия', 'репродукция', 'энергоблок', 'квалификация']
            #    g = randint(0, len(word) - 1)
            #    s = word[g]
            #    sl = len(s) * '.'

            if mc[9:] == "Камень-ножницы-бумага":
                global a
                debug = 0
                playerKmn = msgAuthor
                print("player" + playerKmn)
                await message.channel.send("Началась игра \"Камень-ножницы-бумага\" c пользователем " + msgAuthor)
                playKMN = True
                a = randint(1, 3)
                embed = discord.Embed(
                    title="Началась игра \"Камень-ножницы-бумага\" c пользователем " + msgAuthor,
                    description='Введите "камень", "ножницы" или "бумага", чтоб сделать выбор',
                    colour=discord.Colour.from_rgb(80, 125, 229))
                await message.channel.send(embed=embed)

            """
            if "Подарки" in mc:
                if mc[17:] == "3x3":
                    embed = discord.Embed(
                        title="Началась игра \"Подарки\" c пользователем " + msgAuthor,
                        description='  1 2 3\n' +
                                    'А 🎁 🎁 🎁\n' +
                                    'Б 🎁 🎁 🎁\n' +
                                    'В 🎁 🎁 🎁\n\n' +
                                    'Введи свой выбор по типу 1А(кириллица)',
                        colour=discord.Colour.from_rgb(80, 125, 229)
                    )
                    await message.channel.send(embed=embed)
                    gifs4 = randint(1, 3)
                    gifs5 = randint(1, 3)
                    if gifs5 == 1:
                        gifs5 = 'А'
                    elif gifs5 == 2:
                        gifs5 = 'Б'
                    else:
                        gifs5 = 'В'
                    gifs4 = str(gifs4)
                    if gifs6 == gifs4 + gifs5:
                        embed = discord.Embed(
                            title="Вы победили!",
                            colour=discord.Colour.from_rgb(80, 125, 229)
                        )
                        await message.channel.send(embed=embed)
                    else:
                        embed = discord.Embed(
                            title="Вы проиграли!",
                            description='приз был в ' + gifs4 + gifs5,
                            colour=discord.Colour.from_rgb(80, 125, 229)
                        )
                        await message.channel.send(embed=embed)
                elif mc[17:] == "5x5":
                    embed = discord.Embed(
                        title="Началась игра \"Подарки\" c пользователем " + msgAuthor,
                        description='  1 2 3 4 5\n' +
                                    'А 🎁 🎁 🎁 🎁 🎁\n' +
                                    'Б 🎁 🎁 🎁 🎁 🎁\n' +
                                    'В 🎁 🎁 🎁 🎁 🎁\n' +
                                    'Г 🎁 🎁 🎁 🎁 🎁\n' +
                                    'Д 🎁 🎁 🎁 🎁 🎁\n\n' +
                                    'Введи свой выбор по типу 1А(кириллица)',
                        colour=discord.Colour.from_rgb(80, 125, 229)
                    )
                    await message.channel.send(embed=embed)
                    gifs1 = randint(1, 5)
                    gifs2 = randint(1, 5)
                    if gifs2 == 1:
                        gifs2 = 'А'
                    elif gifs2 == 2:
                        gifs2 = 'Б'
                    elif gifs2 == 3:
                        gifs2 = 'В'
                    elif gifs2 == 4:
                        gifs2 = 'Г'
                    else:
                        gifs2 = 'Д'
                    gifs1 = str(gifs1)
                    if gifs3 == gifs1 + gifs2:
                        print('Ты победил')
                    else:
                        print('Ты проиграл, приз был в', gifs1 + gifs2)
            """

            if mc[9:17] == "Кости с ":
                if mc[17:] == "Akkumuru Sekkai":
                    first, second = str(randint(1, 6)), str(randint(1, 6))
                    plrF, plrS = str(randint(1, 6)), str(randint(1, 6))
                    embed = discord.Embed(
                        title='Бросок костей',
                        description="У меня выпало " + first + " и " + second + "\n"
                                    "У вас " + plrF + " и " + plrS,
                        colour=discord.Colour.from_rgb(80, 125, 229))
                    await message.channel.send(embed=embed)
                    if int(first) + int(second) > int(plrF) + int(plrS):
                        embed = discord.Embed(
                            title='Я победил!',
                            colour=discord.Colour.from_rgb(80, 125, 229))
                        await message.channel.send(embed=embed)
                    elif int(first) + int(second) < int(plrF) + int(plrS):
                        embed = discord.Embed(
                            title='Вы победили!',
                            colour=discord.Colour.from_rgb(80, 125, 229))
                        await message.channel.send(embed=embed)
                    else:
                        embed = discord.Embed(
                            title='Ничья!',
                            colour=discord.Colour.from_rgb(80, 125, 229))
                        await message.channel.send(embed=embed)
                else:
                    print(message.channel.members)
                    #await message.channel.send()
                    embed = discord.Embed(
                        title='Внимание!',
                        description='Доступна только демо-версия игры со мной.\n'
                                    'Для игры введите $go_play Кости с Akkumuru Sekkai',
                        colour=discord.Colour.from_rgb(80, 125, 229))
                    await message.channel.send(embed=embed)
        if playKMN and message.author.name == playerKmn:
            if debug == 0:
                debug = 1
            else:
                print("hi")
                b = mc.lower()
                if (a == 1 and b == 'камень') or (a == 2 and b == 'ножницы') or (a == 3 and b == 'бумага'):
                    embed = discord.Embed(
                        title='Совпадение!',
                        description=b + ' vs ' + b,
                        colour=discord.Colour.from_rgb(80, 125, 229))
                    await message.channel.send(embed=embed)
                if a == 2 and b == 'бумага':
                    embed = discord.Embed(
                        title='Вы проиграли!',
                        description='ножницы vs бумага',
                        colour=discord.Colour.from_rgb(80, 125, 229))
                    await message.channel.send(embed=embed)
                elif a == 2 and b == 'камень':
                    embed = discord.Embed(
                        title='Вы выиграли!',
                        description='ножницы vs камень',
                        colour=discord.Colour.from_rgb(80, 125, 229))
                    await message.channel.send(embed=embed)
                elif a == 1 and b == 'ножницы':
                    embed = discord.Embed(
                        title='Вы проиграли!',
                        description='камень vs ножницы',
                        colour=discord.Colour.from_rgb(80, 125, 229))
                    await message.channel.send(embed=embed)
                elif a == 1 and b == 'бумага':
                    embed = discord.Embed(
                        title='Вы выиграли!',
                        description='камень vs бумага',
                        colour=discord.Colour.from_rgb(80, 125, 229))
                    await message.channel.send(embed=embed)
                elif a == 3 and b == 'ножницы':
                    embed = discord.Embed(
                        title='Вы выиграли!',
                        description='бумага vs ножницы',
                        colour=discord.Colour.from_rgb(80, 125, 229))
                    await message.channel.send(embed=embed)
                elif a == 3 and b == 'камень':
                    embed = discord.Embed(
                        title='Вы проиграли!',
                        description='бумага vs камень',
                        colour=discord.Colour.from_rgb(80, 125, 229))
                    await message.channel.send(embed=embed)
                playKMN = False

        if playWords and message.author.name == qsl:
            print(msgAuthor, qsl)
            if debug == 0:
                debug = 1
            else:
                await message.channel.send(sl)
                while sl != s:
                    k = ''
                    if mc != 'Буква либо была, либо это не буква' or mc != sl:
                        a = mc.lower()
                        while a in k or len(a) != 1:
                            await message.channel.send('Буква либо была, либо это не буква')
                            await message.channel.send(sl)
                            a = mc.lower()
                        k += a
                        for i in range(len(s)):
                            if s[i] == a:
                                sl = sl[:i] + a + sl[i + 1:]
                        await message.channel.send(sl)
                await message.channel.send('Вы победили!')

        if mc[1:] == "toast":
            toast = ['Когда ты просыпешься здоровым и янсым, ты выигрывешь неольшую лотерею - ещё один день жизни подарен '
                     'для тебя.\n*открывает баночку пива*\nВыигрышь всегда нужно праздновать.🍻',
                     'О, ты тут! Выпьем же за это!🍻',
                     'Хорошая команда, выпьем за неё!🍻',
                     'О! Сейчас ' + datetime.datetime.today().strftime("%H:%M") + ', пора выпить!',
                     'Слава СССР!',
                     'Звучит как тост, выпьем!',
                     f'В нашей компании есть хорошие люди.\nВыпьем же за это!']
            g = randint(0, len(toast) - 1)
            s = toast[g]
            embed = discord.Embed(
                title=s,
                colour=discord.Colour.from_rgb(80, 125, 229))
            await message.channel.send(embed=embed)

        if mc[1:] == "joke":
            joke = ['Я тоже могу достать языком до носа. Главное, застать человека врасплох',
                    'Жил-был царь, и было у него косоглазие. Пошёл он куда глаза глядят и порвался',
                    'Толстые стриптизёрши иногда перегибают палку',
                    'Из-за коронавируса отменили концерты Ольги Бузовой... '
                    'Уже в который раз Природа встает на защиту людей!',
                    'Любую неизвестную кнопку нужно нажимать четное количество раз',
                    'Мальчик так и не смог решить задачу со звездочкой, потому что запах этой дряни реально мешает',
                    'Чтобы в будущем дочь не стала путаной, родители назвали ее Авдотья',
                    'Объявление на дверях отдела кадров Газпрома: "Приема на работу нет. Работа передается по наследству"']
            g = randint(0, len(joke) - 1)
            s = joke[g]
            embed = discord.Embed(
                title=s,
                description='',
                colour=discord.Colour.from_rgb(80, 125, 229))
            await message.channel.send(embed=embed)

        if mc[1:] == "riddle":
            global rp
            user = msgAuthor
            riddle = True
            riddles = ['Сто одёжек и все без застёжек', 'с помощью чего можно смотрет сквозь стену?',
                      'У какой операции низкий процент провалов, но почти никто из пациэнтов не выживает',
                      'Два конца, два кольца, по середине гвоздик']
            ro = ['Бомж', 'Окно', 'Эвтаназия', 'Ножницы']
            rg = randint(0, len(riddles) - 1)
            rs = riddles[rg]
            rp = ro[rg]
            embed = discord.Embed(
                title=rs,
                colour=discord.Colour.from_rgb(80, 125, 229))
            await message.channel.send(embed=embed)

        if mc[1:] == "game_list":
            embed = discord.Embed(
                title='Список всех игр',
                description='Камень-ножницы-бумага\n'+
                            'Кости(демо)',
                colour=discord.Colour.from_rgb(80, 125, 229))
            await message.channel.send(embed=embed)

        if mc[1:] == "math_task":
            user = playerKmn = msgAuthor
            global math_answer, right
            math = True
            task = ['Корень из 225', 'Квадрат 28', '3 в степени n = 2 во второй степени кмножить на 3 в третей степени',
                    '5 в степени 0', '|(2 * √5)²|']
            answer = ["15", "784", "5", "1", "20"]
            g = randint(0, len(task) - 1)
            embed = discord.Embed(
                title=task[g],
                colour=discord.Colour.from_rgb(80, 125, 229))
            await message.channel.send(embed=embed)
            right = answer[g]

        if mc[1:9] == "eqManager":
            arg = mc.split(" ")
            workMode = int(arg[1])
            answer = bool(arg[2])
            a = int(arg[3])
            b = int(arg[4])
            c = int(srg[5])

            """ workMode: 1 - создаёт уравнение и ответ (кол-во знаков после запятой - до 16),
            2 - решает уравнение с коэффициентами a, b и c. answer: False - ответ не генерируется и не выводится,
            True - *угадай*."""

            def solverLegacy(a1, b1, c1):

                """ Дискриминант. Возвращает ужасные десятичные дроби, поэтому и заброшен. """

                d = (b1 ** 2) - (4 * a1 * c1)
                if d < 0:
                    return []
                try:
                    x1 = (-b1 + sqrt(d)) / (2 * a1)
                    x2 = (-b1 - sqrt(d)) / (2 * a1)
                except Exception:
                    return "Ошибка: деление на ноль. Взгляните еще раз на входные данные."

                if x1 == x2:
                    return [x1]

                return [x1, x2]

            def solver(a1, b1, c1):
                """ Дискриминант. Эта функция возвращает (пытается) значения, понятные для людей,
                 по типу 4 - 3*кор(2) вместо -0.24264068711928566 """
                try:
                    d = (b1 ** 2) - (4 * a1 * c1)
                except ValueError:
                    return "Ошибка: входные данные не являются числами."
                if d < 0:
                    return []
                squares = [x ** 2 for x in range(1, 16)]
                squares.reverse()
                root = ""
                for i in squares:
                    if d % i == 0:
                        root = f'{int(sqrt(i))}*кор({d // i})'
                        break
                if b1 >= 0:
                    x1 = f'(-{b1} + {root}) / {2 * a1}'
                    x2 = f'(-{b1} - {root}) / {2 * a1}'
                    neutr = f'-{b1} / {2 * a1}'
                else:
                    x1 = f'({b1} + {root}) / {2 * a1}'
                    x2 = f'({b1} - {root}) / {2 * a1}'
                    neutr = f'{b1} / {2 * a1}'
                if d == 0:
                    return neutr
                return [x1, x2]
            if workMode == 1:  # Создать новое кв. уравнение и его ответ
                coeffs = [randint(-10, 15) for x in
                          range(3)]  # Генерация коэффициентов. Возможных уравнений около 15 тысяч.
                eq = ""
                # Для каждого коэффициента было нужно уникальное поведение. Клянусь Богом, это необходимо.
                for i in range(3):
                    coeff = coeffs[i]
                    if i == 0:
                        if coeff == 0:
                            coeff = 1
                        if coeff == 1:
                            eq += "x^2"
                            continue
                        elif coeff == -1:
                            eq += "-x^2"
                            continue
                        elif coeff >= 0:
                            eq += str(abs(coeff)) + "x^2"
                            continue
                        else:
                            eq += "-" + str(abs(coeff)) + "x^2"
                            continue
                    elif i == 1:
                        if coeff == 0:
                            continue
                        if coeff == 1:
                            eq += " + x"
                            continue
                        elif coeff == -1:
                            eq += " - x"
                            continue
                        elif coeff >= 0:
                            eq += " + " + str(abs(coeff)) + "x"
                            continue
                        else:
                            eq += " - " + str(abs(coeff)) + "x"
                    else:
                        if coeff == 0:
                            continue
                        if coeff >= 0:
                            eq += " + " + str(abs(coeff))
                            continue
                        else:
                            eq += " - " + str(abs(coeff))

                eq += " = 0"

                if answer:
                    await message.channel.send([eq, solver(coeffs[0], coeffs[1], coeffs[2])])
                    # Возвращаются само уравнение и список ответов. Да, список в списке
                else:
                    await message.channel.send(eq)  # Только уравнение.

            elif workMode == 2:
                await message.channel.send(solver(a, b, c))  # wM 2: возможность решения готового уравнения

            else:

                await message.channel.send("Неправильное значение параметра workmode. Проверьте входные данные.")

        if mc[1:] == "help":
            embed = discord.Embed(
                title='Список команд',
                description='change_prefix <префикс> - меняет префикс на <префикс>\n' +
                            'game_list - список всех игр\n' +
                            'go_play <игра> - начинаю играть в <игра>\n' +
                            'joke - выкидываю тупую шутку\n' +
                            'math_task - даю математическую задачку\n' +
                            'reload_for <имя пользователя> - Сбрасывает уровень активности для'
                            ' <имя пользователя>.\n' +
                            'reload_levels - Сбрасывает уровни активности всех пользователей\n' +
                            'show_levels - Показывает уровни активности всех пользователей '
                            'кроме неактивных.\n' +
                            'show_time - Показывает текущие дату и время\n' +
                            'toast - рандомный повод выпить',
                colour=discord.Colour.from_rgb(80, 125, 229)
            )
            await message.channel.send(embed=embed)

    if riddle_answer != 2 and message.author.name == user and riddle:
        riddle_answer += 1
    if riddle_answer == 2 and message.author.name == user and riddle:
        user_a = mc
        user = ''
        riddle_answer = 0
        riddle = False
        if user_a != rp:
            embed = discord.Embed(
                title='Не правильно, верный ответ: ' + rp,
                colour=discord.Colour.from_rgb(80, 125, 229))
            await message.channel.send(embed=embed)
        else:
            embed = discord.Embed(
                title='Верно!',
                colour=discord.Colour.from_rgb(80, 125, 229))
            await message.channel.send(embed=embed)

    if math_answer != 2 and message.author.name == user and math:
        math_answer += 1
    if math_answer == 2 and message.author.name == user and math:
        user_a = mc
        user = ''
        math_answer = 0
        math = False
        if user_a != right:
            embed = discord.Embed(
                title='Не правильно, в следующий раз повезёт',
                colour=discord.Colour.from_rgb(80, 125, 229))
            await message.channel.send(embed=embed)
        else:
            embed = discord.Embed(
                title='Верно!',
                colour=discord.Colour.from_rgb(80, 125, 229))
            await message.channel.send(embed=embed)

bot.run(settings['token'])
