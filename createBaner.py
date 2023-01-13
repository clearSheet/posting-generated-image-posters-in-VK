from PIL import Image, ImageFilter, ImageFont, ImageDraw
import dates
import os.path


def create_banner(titleFilm, genres, duration, yearRelease, dateRussiaRelease, ageLimit, description, golivudStr, charleyStr, cinemaCenterStr):
    # Исходник разрешение 1030x580
    # Нужно получать банер размером 1000x700
    # Нужно получить афишу размером 299x443

    # Создание размытого бэкграунда
    # if Image.open(f'backgrounds/{titleFilm}.jpg'):
    #     img = Image.open(f'backgrounds/{titleFilm}.jpg')
    # else:
    #     img = Image.open('static/zag.jpg')

    if os.path.isfile(f'backgrounds/{titleFilm}.jpg'):
        img = Image.open(f'backgrounds/{titleFilm}.jpg')
    else:
        img = Image.open('static/zag.jpg')

    img = img.filter(ImageFilter.BLUR)
    img = img.filter(ImageFilter.BLUR)
    img = img.filter(ImageFilter.BLUR)
    img = img.filter(ImageFilter.BLUR)

    pixels = img.getdata()
    brightness_multiplier = 0.5  # Переменная затемнения
    new_image_list = []

    for pixel in pixels:
        new_pixel = (int(pixel[0] * brightness_multiplier),
                     int(pixel[1] * brightness_multiplier),
                     int(pixel[2] * brightness_multiplier))

        # check the new pixel values are within rgb range
        for pixel in new_pixel:
            if pixel > 255:
                pixel = 255
            elif pixel < 0:
                pixel = 0
        new_image_list.append(new_pixel)

    img.putdata(new_image_list)
    img = img.crop((0, 0, 828, 579))
    img = img.resize((1000, 700))


    # ______________________________
    # Добавление афиши в изрбражение

    watermark = Image.open(f'afisha/{titleFilm}.jpg').convert("RGBA")
    watermark = watermark.resize((299, 443))

    img.paste(watermark, (21, 109), watermark)

    # __________________________________________________________________________
    # Создание шрифтов (размеры, функции добавления черного и ораньжевого цвета)
    font13 = ImageFont.truetype('days_[allfont.ru].ttf', size=13, layout_engine=ImageFont.LAYOUT_BASIC)
    font22 = ImageFont.truetype('days_[allfont.ru].ttf', size=22, layout_engine=ImageFont.LAYOUT_BASIC)
    font30 = ImageFont.truetype('days_[allfont.ru].ttf', size=30, layout_engine=ImageFont.LAYOUT_BASIC)
    font40 = ImageFont.truetype('days_[allfont.ru].ttf', size=40, layout_engine=ImageFont.LAYOUT_BASIC)

    def add_text_white(text, x, y, fnt):
        draw_text = ImageDraw.Draw(img)
        draw_text.text(
            (y, x),
            f'{text}',
            font=fnt,
            fill=(255, 255, 255)
        )

    def add_text_red(text, x, y, fnt):
        draw_text = ImageDraw.Draw(img)
        draw_text.text(
            (y, x),
            f'{text}',
            font=fnt,
            fill=(255, 69, 0)
        )

    # ____________________________________________
    # Наложение текста, который относится непосредсвенно к фильму

    add_text_white(titleFilm, 75, 21, font22)

    add_text_red('Жанр:', 115, 335, font22)
    add_text_white(genres, 115, 415, font22)

    add_text_red('Продолжительность:', 142, 335, font22)
    add_text_white(duration, 142, 600, font22)

    add_text_red('Год выпуска:', 169, 335, font22)
    add_text_white(yearRelease, 169, 503, font22)

    add_text_red('Премьера в России:', 196, 335, font22)
    add_text_white(dateRussiaRelease, 196, 585, font22)

    add_text_red('Возраст:', 223, 335, font22)
    add_text_white(ageLimit, 223, 452, font22)

    add_text_red('Расписание сеансов:', 550, 21, font22)

    if golivudStr != '-':
        add_text_white(golivudStr, 575, 150, font22)
        add_text_white('Голливуд:', 575, 21, font22)

    if charleyStr != '-':
        add_text_white('Чарли:', 600, 21, font22)
        add_text_white(charleyStr, 600, 120, font22)

    if cinemaCenterStr != '-':
        add_text_white('Центр Кино:', 625, 21, font22)
        add_text_white(cinemaCenterStr, 625, 180, font22)



    # Нужно ограничение в 50 символов для строки описания
    
    def descriptionView(description):
        if len(description) == 400:
            description = description + '...Подробнее на bratsk.com'

        lst = description.split(' ')
        countLit = 0
        str = ''
        x = 250
        jump = 28

        for item in lst:  # Проходимся по элементам массива
            if len(str) < 35 and countLit < 35:
                countLit = + len(item) + 1
                str = str + item + ' '
            else:
                add_text_white(str, x, 335, font22)
                x = x + jump
                str = item + ' '
                countLit = 0
        if len(description) < 450:
            add_text_white(str, x, 335, font22)
        else:
            add_text_white(str, x, 335, font22)

    descriptionView(description.replace(' ', ' '))

    # with open(f"{titleFilm}.txt", 'w') as file:
    #     file.writelines(description)
    # ____________________________________________
    # Наложение дополнительного текста

    # Левый верхний угол
    add_text_white('АФИША', 15, 20, font30)
    add_text_white('КИНО', 40, 50, font22)

    # Правый верхний угол

    add_text_red(dates.date, 15, dates.day_positon[dates.date], font30)

    add_text_white(dates.month.upper(), 15, 800, font30)

    add_text_white('Повседневный Братск', 50, 780, font13)
    add_text_white('vk.com/everydaybratsk', 65, 780, font13)

    img.save(f'baner/{titleFilm}.png')

