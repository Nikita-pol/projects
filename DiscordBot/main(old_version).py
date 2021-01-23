import datetime
import time
import os
import shutil
from random import randint
from math import sqrt
import json
from discord.utils import get

# import requests
import discord
from discord.ext import commands

from config import settings
from statLogger import statLogger, formatTime
prefix = settings['prefix']

bot = commands.Bot(command_prefix=settings['prefix'])
bot.remove_command('help')

playWords = False
playKMN = False
end = False
math_answer, riddle_answer, gifts_answer = 0, 0, 0
math, riddle, gift = False, False, False
user, right = '', ''
debug = 0
words = None
a, sl, rp = None, None, None
playerKmn = None
gifs4, gifs5 = None, None
new_day = True
activity_levels = []


@bot.event
async def on_ready():
    print("Ready")
    channel = bot.get_channel(793390527328419843)
    hiEmbed1 = discord.Embed(title="Готов к работе.",
                             colour=discord.Colour.from_rgb(80, 125, 229))
    hiEmbed1.set_author(name="Akkumuru Sekkai",
                        url="",
                        icon_url="http://memes1.unaux.com/icon.png")
    hiEmbed2 = discord.Embed(title="Я вылез из гроба!",
                             colour=discord.Colour.from_rgb(80, 125, 229))
    hiEmbed2.set_author(name="Akkumuru Sekkai",
                        url="",
                        icon_url="http://memes1.unaux.com/icon.png")
    logs = [hiEmbed1, hiEmbed2]
    # hiEmbed2.set_thumbnail(url="http://memes1.unaux.com/icon.png")
    await channel.send(embed=logs[randint(0, len(logs)-1)])
    channel = bot.get_channel(799731037998678096)
    await channel.send("Пуск!")


@bot.event
async def on_message(message):
    if message.channel.id != 799731037998678096:
        print(message)
        print(message.author.name)
        print(message.content)
    global playWords, playKMN, qsl, playerKmn, user, right, math_answer, debug, prefix, riddle_answer,\
        math, riddle, a, sl, gifts_answer, gifs4, gifs5, gift, new_day, activity_levels
    mc = message.content
    msgAuthor = message.author.name
    word = message.content

    def reload_level():
        a11 = {}
        with open("users.json") as info_file:
            info = json.loads(info_file.read)
            for username in info:
                points = info[username]["points"]
                lvl = info[username]["level"]
                for i in range(lvl):
                    points += i ** 2 * 100
                info[username]["points"] = points
            json.dump(info_file, info)
        levels = []
        for i in a11:
            levels.append(a11[i][0])
        levels.sort()
        levels.reverse()
        for j in levels:
            for i in a11:
                if a11[i][0] == j:
                    activity_levels.append(a11[i][2])

    def write_id():
        with open("users.json") as info_file:
            info = json.loads(info_file)
            info[message.author.name]["id"] = message.author.id
            json.dump(info_file, info)

    reload_level()
    write_id()
    if message.channel.id == 799731037998678096:
        time.sleep(1)
        embed = discord.Embed(title="Debug",
                              description="Время " + datetime.datetime.today().strftime("%H:%M:%S"),
                              colour=discord.Colour.from_rgb(80, 125, 229))
        await message.channel.send(embed=embed)
        if datetime.datetime.today().strftime("%H:%M") == "00:00" and new_day:
            channel = bot.get_channel(793390527328419843)
            await channel.send("Новый день настал, сегодня " + datetime.datetime.today().strftime("%d.%m.%Y"))
            new_day = False
            for root, dirs, files in os.walk("Users"):
                if root != "Users":
                    with open("users.json") as info_file:
                        date = json.loads(info_file.read())
                    if file.read() == datetime.datetime.today().strftime("%d.%m"):
                        embed = discord.Embed(title="С Днем Рождения!",
                                              description=f"Сегодня день рождения у {root[6:]}, поздравим его!",
                                              colour=discord.Colour.from_rgb(80, 125, 229))
                        embed.set_thumbnail(url="http://memes1.unaux.com/bday.jpg")
                        await message.channel.send(embed=embed)
        if datetime.datetime.today().strftime("%H:%M") == "00:01" and not new_day:
            new_day = True

    if message.channel.id == 793390527328419843:
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

    if playKMN and message.author.name == playerKmn:
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
    # ---------------------------------------------------------------

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
    # ---------------------------------------------------------------

    if riddle_answer != 1 and message.author.name == user and riddle:
        riddle_answer += 1
    if riddle_answer == 1 and message.author.name == user and riddle:
        user_a = mc.lower()
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
    # ---------------------------------------------------------------

    if math_answer != 1 and message.author.name == user and math:
        math_answer += 1
    if math_answer == 1 and message.author.name == user and math:
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

    if gifts_answer != 1 and message.author.name == user and gift:
        gifts_answer += 1
    if gifts_answer == 1 and message.author.name == user and gift:
        gifs6 = mc
        gift = False
        user = ""
        gifts_answer = 0
        if gifs6 == gifs4 + gifs5:
            embed = discord.Embed(
                title="Вы победили!",
                colour=discord.Colour.from_rgb(80, 125, 229)
            )
            await message.channel.send(embed=embed)
        else:
            embed = discord.Embed(
                title="Вы проиграли!",
                description='Приз был в ' + gifs4 + gifs5,
                colour=discord.Colour.from_rgb(80, 125, 229)
            )
            await message.channel.send(embed=embed)

    await bot.process_commands(message)

"""Liver commands ---------------------------------------------------------------------------------------------------"""
@bot.command()
async def show_liver(ctx):
    pass

""" admin commands --------------------------------------------------------------------------------------------------"""
@bot.command()
async def ban(ctx, *, arg):
    admin = False
    for i in ctx.message.author.roles:
        if str(i) == "Админ":
            admin = True
            username, time, points = arg.split(" ")
            if int(time) > 10080:
                embed = discord.Embed(title="Внимание!",
                                      description="Время бана слишком большое, введите в минутах не больше 10080.",
                                      colour=discord.Colour.from_rgb(80, 125, 229))
                ctx.send(embed=embed)
            try:
                file = open("files\\UserId\\"+username+".txt", "r")
                id = int(file.read())
                file.close()
                user = get(bot.get_all_members(), id=id)
                await user.remove_roles
                role = discord.utils.get(ctx.message.guild.roles, id=800059082471505970)
                await user.add_roles(role)
                nowday = datetime.datetime.today().strftime("%d")
                nowmin = datetime.datetime.today().strftime("%M")
                nowhour = datetime.datetime.today().strftime("%H")
                m = time % 60
                h = time % 1440
                d = h // 1440
                banmin = int(nowmin) + m
                if banmin >= 60:
                    banmin -= 60
                    h += 1
                banhour = int(nowhour) + h
                if banhour >= 24:
                    banhour -= 24
                    d += 1
                banday = nowday + d
                with open("files\\ban_list.json", "w") as ban_file:
                    ban_list = json.loads(ban_file)
                    ban_list[username][ban_status] = 1
                    ban_list[username][ban_time] = f'{banday}.{banhour}.{banmin}'
                    json.dump(ban_list, ban_file)
            except FileNotFoundError:
                embed = discord.Embed(
                    title='Ошибка!',
                    description="Пользователя с таким именем не существует.",
                    colour=discord.Colour.from_rgb(80, 125, 229))
                await ctx.send(embed=embed)

    if not admin:
        embed = discord.Embed(
            title='Бан!',
            description="Недостаточно прав.\nСначала получите роль админа.",
            colour=discord.Colour.from_rgb(80, 125, 229))
        await ctx.send(embed=embed)
        await ctx.message.author.remove_roles
        role = discord.utils.get(ctx.message.guild.roles, id=800059082471505970)
        await ctx.message.author.add_roles(role)
        banday = 2
        banhour = 0
        banmin = 0
        with open("files\\ban_list.json", "w") as ban_file:
            ban_list = json.loads(ban_file)
            ban_list[ctx.message.author.name][ban_status] = 1
            ban_list[ctx.message.author.name][ban_time] = f'{banday}.{banhour}.{banmin}'
            json.dump(ban_list, ban_file)


@bot.command()
async def reload_levels(ctx):
    admin = False
    for i in ctx.message.author.roles:
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
            await ctx.send(embed=embed)
        if not admin:
            embed = discord.Embed(
                title='Ошибка!',
                description="Недостаточно прав.\nСначала получите роль админа.",
                colour=discord.Colour.from_rgb(80, 125, 229))
            await ctx.send(embed=embed)


@bot.command()
async def reload_for(ctx, *, username):
    admin = False
    for i in ctx.message.author.roles:
        if str(i) == "Админ":
            admin = True
            try:
                root = "Users\\" + username
                path = os.path.join(os.path.abspath(os.path.dirname(__file__)), root)
                shutil.rmtree(path)
                embed = discord.Embed(
                    title='Успешно!',
                    description="Уровень активности для " + username + " сброшен.",
                    colour=discord.Colour.from_rgb(80, 125, 229))
                await ctx.send(embed=embed)
            except FileNotFoundError:
                embed = discord.Embed(
                    title='Ошибка!',
                    description="Пользователя с таким именем не существует или его уровень активности равен 0.",
                    colour=discord.Colour.from_rgb(80, 125, 229))
                await ctx.send(embed=embed)
    if not admin:
        embed = discord.Embed(
            title='Ошибка!',
            description="Недостаточно прав.\nСначала получите роль админа.",
            colour=discord.Colour.from_rgb(80, 125, 229))
        await ctx.send(embed=embed)


@bot.command()
async def change_prefix(ctx, *, pref):
    global prefix
    admin = False
    for i in ctx.message.author.roles:
        if str(i) == "Админ":
            admin = True
            file = open("files\\prefix.txt", "w")
            file.write(pref)
            file.close()
            prefix = pref
            bot.command_prefix = prefix
            embed = discord.Embed(
                title='Успешно!',
                description="Префикс сменен на " + pref,
                colour=discord.Colour.from_rgb(80, 125, 229))
            await ctx.send(embed=embed)
    if not admin:
        embed = discord.Embed(
            title='Ошибка!',
            description="Недостаточно прав.\nСначала получите роль админа.",
            colour=discord.Colour.from_rgb(80, 125, 229))
        await ctx.send(embed=embed)


"""book control commands---------------------------------------------------------------------------------------------"""
@bot.command()
async def book_in(ctx, *, idea):
    file = open("files\\id.txt", "r")
    id = file.read()
    id = str(int(id) + 1)
    file.close()
    file = open("files\\id.txt", "w")
    file.write(id)
    file.close()
    file = open("files\\ideas.txt", "a+")
    file.write("<id: " + id + "> " + idea+"\n")
    file.close()
    embed = discord.Embed(title="Успешно!",
                          description="Добавлена новая заметка с id " + id,
                          colour=discord.Colour.from_rgb(80, 125, 229))
    await ctx.send(embed=embed)


@bot.command()
async def book_out(ctx):
    file = open("files\\ideas.txt", "r")
    embed = discord.Embed(title="Актуальные идеи",
                          description=file.read(),
                          colour=discord.Colour.from_rgb(80, 125, 229))
    await ctx.send(embed=embed)


@bot.command()
async def delete_idea(ctx, *, id):
    dev = False
    for i in ctx.message.author.roles:
        if str(i) == "Разработчик":
            dev = True
            delete = False
            file = open("files\\ideas.txt", "r")
            contx = file.read()
            contx = contx.split("\n")
            for i in contx:
                if "<id: " + id + ">" in i:
                    contx.pop(contx.index(i))
                    delete = True
                    embed = discord.Embed(title="Успешно!",
                                          description="Идея с id " + id + " успешно удалена.\n"
                                                      "Содержание: " + i,
                                          colour=discord.Colour.from_rgb(80, 125, 229))
                    await ctx.send(embed=embed)
                    break
            file.close()
            file = open("files\\ideas.txt", "w")
            file.write("\n".join(contx))
            file.close()
            if not delete:
                embed = discord.Embed(title="Ошибка!",
                                      description="Идеи с таким id не существует.",
                                      colour=discord.Colour.from_rgb(80, 125, 229))
                await ctx.send(embed=embed)
    if not dev:
        embed = discord.Embed(
            title='Ошибка!',
            description="Недостаточно прав.\nСначала получите роль создателя ботов.",
            colour=discord.Colour.from_rgb(80, 125, 229))
        await ctx.send(embed=embed)

""" other commands---------------------------------------------------------------------------------------------------"""
@bot.command()
async def show_levels(ctx):
    content = ""
    a11 = {}
    for root, dirs, files in os.walk("Users"):
        if root != "Users":
            global words
            file = open(root + "\\level.txt", "r")
            lvl = file.read()
            file.close()
            file = open(root + "\\words.txt", "r")
            words = file.read()
            points = int(words)
            for i in range(int(lvl)):
                points += i ** 2 * 100
            a11[root] = [points, int(lvl)-1, root[6:], words]
            file.close()
    print(a11)
    levels = []
    for i in a11:
        levels.append(a11[i][0])
    levels.sort()
    levels.reverse()
    print(levels)
    for j in levels:
        for i in a11:
            print(a11[i][0], j)
            if a11[i][0] == j:
                content += a11[i][2] + " -- " + str(a11[i][1] + 1) + " уровень; " + a11[i][3] + " очков.\n"
    embed = discord.Embed(
        title='Уровни активности на сервере',
        description=content,
        colour=discord.Colour.from_rgb(80, 125, 229))
    await ctx.send(embed=embed)


@bot.command()
async def level(ctx):
    file = open("Users\\"+ctx.message.author.name+"\\level.txt", "r")
    lvl = file.read()
    file.close()
    file = open("Users\\"+ctx.message.author.name+"\\words.txt", "r")
    embed = discord.Embed(title="Уровень активности для " + ctx.message.author.name,
                          description=
                          "Место в рейтинге: " + str(int(activity_levels.index(ctx.message.author.name)) + 1) +
                          "\nУровень: " + lvl +
                          "\nОчки: " + file.read(),
                          colour=discord.Colour.from_rgb(80, 125, 229))
    await ctx.send(embed=embed)


@bot.command()
async def show_time(ctx):
    if ctx.message.author.id == 688789301202387088:
        today = str(int(datetime.datetime.today().strftime("%H")) - 1)
        today += datetime.datetime.today().strftime(":%M:%S")
        embed = discord.Embed(
            title='Киевское время',
            description="Сегодня " + datetime.datetime.today().strftime("%d.%m.%Y") +
                        "\nВремя " + today,
            colour=discord.Colour.from_rgb(80, 125, 229))
    else:
        embed = discord.Embed(
            title='Московское время',
            description="Сегодня " + datetime.datetime.today().strftime("%d.%m.%Y") +
                        "\nВремя " + datetime.datetime.today().strftime("%H:%M:%S"),
            colour=discord.Colour.from_rgb(80, 125, 229))
    await ctx.send(embed=embed)


@bot.command()
async def toast(ctx):
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
    await ctx.send(embed=embed)


@bot.command()
async def joke(ctx):
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
    await ctx.send(embed=embed)


@bot.command()
async def game_list(ctx):
    embed = discord.Embed(
        title='Список всех игр',
        description='Камень-ножницы-бумага\n' +
                    'Подарки 3x3\n' +
                    'Кости(демо)',
        colour=discord.Colour.from_rgb(80, 125, 229))
    await ctx.send(embed=embed)


@bot.command()
async def puzzle(ctx):
    global rp, user, riddle
    user = ctx.message.author.name
    riddle = True
    riddles = ['Сто одёжек и все без застёжек', 'C помощью чего можно смотрет сквозь стену?',
               'У какой операции низкий процент провалов, но почти никто из пациентов не выживает',
               'Два конца, два кольца, по середине гвоздик']
    ro = ['бомж', 'окно', 'эвтаназия', 'ножницы']
    rg = randint(0, len(riddles) - 1)
    rs = riddles[rg]
    rp = ro[rg]
    embed = discord.Embed(
        title=rs,
        colour=discord.Colour.from_rgb(80, 125, 229))
    await ctx.send(embed=embed)


@bot.command()
async def math_task(ctx):
    global math_answer, right, user, math
    user = ctx.message.author.name
    math = True
    task = ['Корень из 225', 'Квадрат 28', '3 в степени n = 2 во второй степени кмножить на 3 в третей степени',
            '5 в степени 0', '|(2 * √5)²|']
    answer = ["15", "784", "5", "1", "20"]
    g = randint(0, len(task) - 1)
    embed = discord.Embed(
        title=task[g],
        colour=discord.Colour.from_rgb(80, 125, 229))
    await ctx.send(embed=embed)
    right = answer[g]


@bot.command()
async def go_play(ctx, *, g):
    # if mc[9:] == "Виселица":
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

    game, second = g.split(" ")

    if game == "Камень-ножницы-бумага":
        global a, playKMN, debug, playerKmn
        debug = 0
        playerKmn = ctx.message.author.name
        playKMN = True
        a = randint(1, 3)
        embed = discord.Embed(
            title="Началась игра \"Камень-ножницы-бумага\" c пользователем " + playerKmn,
            description='Введите "камень", "ножницы" или "бумага", чтоб сделать выбор',
            colour=discord.Colour.from_rgb(80, 125, 229))
        await ctx.send(embed=embed)

    if game == "Подарки":
        global gifs4, gifs5, user, gift
        gift = True
        if second == "3x3":
            user = ctx.message.author.name
            embed = discord.Embed(
                title="Началась игра \"Подарки\" c пользователем " + user,
                description='[] А   Б   В\n' +
                            '1  🎁 🎁 🎁\n' +
                            '2 🎁 🎁 🎁\n' +
                            '3 🎁 🎁 🎁\n\n' +
                            'Введи свой выбор по типу 1А(кириллица)',
                colour=discord.Colour.from_rgb(80, 125, 229)
            )
            await ctx.send(embed=embed)
            gifs4 = randint(1, 3)
            gifs5 = randint(1, 3)
            if gifs5 == 1:
                gifs5 = 'А'
            elif gifs5 == 2:
                gifs5 = 'Б'
            else:
                gifs5 = 'В'
            gifs4 = str(gifs4)
        """
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

    if game == "Кости":
        if second == "Akkumuru Sekkai":
            first, second = str(randint(1, 6)), str(randint(1, 6))
            plrF, plrS = str(randint(1, 6)), str(randint(1, 6))
            embed = discord.Embed(
                title='Бросок костей',
                description="У меня выпало " + first + " и " + second + "\n"
                                                                        "У вас " + plrF + " и " + plrS,
                colour=discord.Colour.from_rgb(80, 125, 229))
            await ctx.send(embed=embed)
            if int(first) + int(second) > int(plrF) + int(plrS):
                embed = discord.Embed(
                    title='Я победил!',
                    colour=discord.Colour.from_rgb(80, 125, 229))
                await ctx.send(embed=embed)
            elif int(first) + int(second) < int(plrF) + int(plrS):
                embed = discord.Embed(
                    title='Вы победили!',
                    colour=discord.Colour.from_rgb(80, 125, 229))
                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(
                    title='Ничья!',
                    colour=discord.Colour.from_rgb(80, 125, 229))
                await ctx.send(embed=embed)
        else:
            print(message.channel.members)
            # await message.channel.send()
            embed = discord.Embed(
                title='Внимание!',
                description='Доступна только демо-версия игры со мной.\n'
                            'Для игры введите $go_play Кости с Akkumuru Sekkai',
                colour=discord.Colour.from_rgb(80, 125, 229))
            await ctx.send(embed=embed)


@bot.command()
async def roulette(ctx, *, mode=None):
    """ mode: None - сыграть в русскую рулетку; stats - статистика
        Всё, что написано КАПСОМ - пустышки, замени их на нужные функции из библиотеки discord"""
    file = open("Users\\"+ctx.message.author.name+"\\total.txt")
    total = int(file.read())
    file.close()
    file = open("Users\\" + ctx.message.author.name + "\\bans.txt")
    bans = int(file.read())
    file.close()
    file = open("Users\\" + ctx.message.author.name + "\\totalBanTime.txt")
    totalBanLength = int(file.read())
    file.close()
    author = ctx.message.author.name

    # 1 неделя - 604800 секунд, 1 день - 86400.
    if mode is None:
        banLength = randint(86400, 604800)
        ch = randint(1, 6)
        if ch <= 1:
            fbl = formatTime(int(banLength))  # Formatted Ban Length
            embed = discord.Embed(title="Вы были забанены.",
                                  description=f"Срок бана: {fbl[0]} дней {fbl[1]} часов {fbl[2]} минут {fbl[3]} секунд.",
                                  color=discord.Colour.from_rgb(80, 125, 229))
            await ctx.send(embed=embed)
            bans += 1
            time.sleep(5)
            role = discord.utils.get(ctx.message.guild.roles, id=800059082471505970)
            await ctx.message.author.add_roles(role)
        else:
            embed = discord.Embed(title="Вы не проиграли:)",
                                  color=discord.Colour.from_rgb(80, 125, 229))
            await ctx.send(embed=embed)
        total += 1
        totalBanLength += banLength
        file = open("Users\\" + ctx.message.author.name + "\\total.txt", "w")
        file.write(str(total))
        file.close()
        file = open("Users\\" + ctx.message.author.name + "\\bans.txt", "w")
        file.write(str(bans))
        file.close()
        file = open("Users\\" + ctx.message.author.name + "\\totalBanTime.txt", "w")
        file.write(str(totalBanLength))
        file.close()
        statLogger(1, author)

    elif mode == "stats":
        statLogger(2, author)
        try:
            fab = formatTime(int(totalBanLength / bans))
        except ZeroDivisionError:
            fab = formatTime(0)
        try:
            embed = discord.Embed(title="Ваша статистика",
                                  description=f"Всего сыграно: {total}\n" +
                                              f"Всего банов: {bans}\n" +
                                              f"Процент банов: {bans / total * 100}\n" +
                                              f"Среднее время бана: {fab[0]} дней {fab[1]} часов {fab[2]} минут {fab[3]} секунд.",
                                  color=discord.Colour.from_rgb(80, 125, 229))
            embed.set_thumbnail(url="http://memes1.unaux.com/rullete.jpg")
        except ZeroDivisionError:
            embed = discord.Embed(title="Ваша статистика",
                                  description=f"Всего сыграно: {total}\n" +
                                              f"Всего банов: {bans}\n" +
                                              f"Процент банов: {bans}\n" +
                                              f"Среднее время бана: {fab[0]} дней {fab[1]} часов {fab[2]} минут {fab[3]} секунд.",
                                  color=discord.Colour.from_rgb(80, 125, 229))
            embed.set_thumbnail(url="http://memes1.unaux.com/rullete.jpg")
        await ctx.send(embed=embed)


@bot.command()
async def add_birthday(ctx, *, date):
    try:
        d, m = date.split(".")
        to = [1, 3, 5, 7, 8, 10, 12]
        t = [4, 6, 9, 11]
        if int(m) in to and 1 <= int(d) <= 31:
            file = open("Users\\" + ctx.message.author.name + "\\birthday.txt", "w")
            file.write(date)
            file.close()
            embed = discord.Embed(title="Успешно!",
                                  description="День рождения для " + ctx.message.author.name + " записан на " + date,
                                  colour=discord.Colour.from_rgb(80, 125, 229))
            await ctx.send(embed=embed)
        elif int(m) in t and 1 <= int(d) <= 30:
            file = open("Users\\" + ctx.message.author.name + "\\birthday.txt", "w")
            file.write(date)
            file.close()
            embed = discord.Embed(title="Успешно!",
                                  description="День рождения для " + ctx.message.author.name + " записан на " + date,
                                  colour=discord.Colour.from_rgb(80, 125, 229))
            await ctx.send(embed=embed)
        elif int(m) == 2 and 1 <= int(d) <= 29:
            file = open("Users\\" + ctx.message.author.name + "\\birthday.txt", "w")
            file.write(date)
            file.close()
            embed = discord.Embed(title="Успешно!",
                                  description="День рождения для " + ctx.message.author.name + " записан на " + date,
                                  colour=discord.Colour.from_rgb(80, 125, 229))
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title="Ошибка!",
                                  description="Неверный формат даты.",
                                  colour=discord.Colour.from_rgb(80, 125, 229))
            await ctx.send(embed=embed)
    except ValueError:
        embed = discord.Embed(title="Ошибка!",
                              description="Неверный формат даты.",
                              colour=discord.Colour.from_rgb(80, 125, 229))
        await ctx.send(embed=embed)


@bot.command()
async def show_birthdays(ctx, *, arg=""):
    context = ""
    if arg == "":
        for root, dirs, files in os.walk("Users"):
            if root != "Users":
                try:
                    file = open(root + "\\birthday.txt", "r")
                    context += root[6:] + " -- " + file.read() + '\n'
                    file.close()
                except FileNotFoundError:
                    pass
        embed = discord.Embed(title="Дни рождения пользователей",
                              description=context,
                              colour=discord.Colour.from_rgb(80, 125, 229))
    else:
        try:
            file = open("Users\\" + arg + "\\birthday.txt", "r")
            context = arg + " -- " + file.read()
            file.close()
            embed = discord.Embed(title="День рождения для " + arg,
                                  description=context,
                                  colour=discord.Colour.from_rgb(80, 125, 229))
        except FileNotFoundError:
            embed = discord.Embed(title="Ошибка!",
                                  description="Пользователя с таким именем не существует"
                                              " или его день рождения не указан.",
                                  colour=discord.Colour.from_rgb(80, 125, 229))
    await ctx.send(embed=embed)


@bot.command()
async def help(ctx):
    embed = discord.Embed(
        title='Список команд',
        colour=discord.Colour.from_rgb(80, 125, 229))
    embed.set_author(name="Akkumuru Sekkai",
                     url="",
                     icon_url="http://memes1.unaux.com/icon.png")
    embed.set_thumbnail(url="http://memes1.unaux.com/icon.png")
    embed.add_field(name="Команды Админа",
                    value=
"""`change_prefix <префикс>` - меняет префикс на `<префикс>`
`reload_for <имя пользователя>` - Сбрасывает уровень активности для `<имя пользователя>`.
`reload_levels` - Сбрасывает уровни активности всех пользователей""",
                    inline=False)
    embed.add_field(name="Операции с заметками",
                    value=
"""`book_out` - выводит все идеи
`book_in <текст>` - добавляет идею `<текст>`
`delete_idea <id>` - удаляет идею с id `<id>`""",
                    inline=False)
    embed.add_field(name="Информация о ползователях",
                    value=
"""`level` - покзываю информацию активности о запросившем пользователе
`show_birthdays <имя пользователя>` - При заданом `<имя пользователя>` выдаю его день рождения. Иначе вывожу дни рождения всех пользователей.
`show_levels` - Показывает уровни активности всех пользователей кроме неактивных.""",
                    inline=False)
    embed.add_field(name="Развлечения",
                    value=
"""`game_list` - список всех игр
`go_play <игра>` - начинаю играть в `<игра>`
`joke` - выкидываю тупую шутку
`puzzle` - задаю загадку
`math_task` - даю математическую задачку
`show_time` - Показывает текущие дату и время
`toast` - рандомный повод выпить""",
                    inline=False)
    await ctx.send(embed=embed)

bot.run(settings['token'])
