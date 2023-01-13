import sys

import requests as requests
from bs4 import BeautifulSoup
import time
import createBaner

url = 'https://bratsk.kinoafisha.info/movies/'

    request = requests.get(url)
    bs = BeautifulSoup(request.text, 'html.parser')

# Находим все ссылки на фильмы в городе помещаем их в массив cinmeHrefs
hrefs = bs.find_all('a', class_='movieItem_ref')
cinemaHrefs = []
for href in hrefs:
    cinemaHrefs.append(href['href'])

# Создаем новое подключение к каждому фильму

def parsFilm(url, time=time):
    request = requests.get(url)
    bs = BeautifulSoup(request.text, 'html.parser')
    
    # Получем название фильма и преобразовываем его
    title = bs.find('h1', class_='trailer_title')
    title = title.text.replace(', 2021', '')  # До 22 года
    
    # Получем категории фильма и заносим в массив
    genresBlocks = bs.find_all('a', class_='filmInfo_genreItem button-main')
    genres = []
    for gen in genresBlocks:
        genres.append(gen.text) # Размер массива уникальный
    
    # Создаем строку из массива
    genresStr = ''
    genres = genres[:3]
    for item in genres:
        genresStr = genresStr + item + ', '
    genresStr = genresStr[:-2]
    
    information = bs.find_all('div', class_='filmInfo_infoItem')
    duration = information[0].find('span', class_='filmInfo_infoData').text  # Продолжительность фильма
    yearRelease = information[1].find('span', class_='filmInfo_infoData').text  # Год выпуска
    dateRussiaRelease = information[2].find('span', class_='filmInfo_infoData').text  # Дата релиза в России
    ageLimit = information[3].find('span', class_='filmInfo_infoData').text  # Возрастное ограничение
    
    description = bs.find('div', class_='visualEditorInsertion more_content').find('p').text[:400] # Описание фильма
    
    # Получение ссылки на фон банера
    backgrounds = bs.find('picture', class_='trailer_altImage picture as-desktop')
    if backgrounds:
        backgrounds = bs.find('picture', class_='trailer_altImage picture as-desktop').find_all('source')[1]['srcset']
        backgroundsData = requests.get(backgrounds)
        with open(f'backgrounds/{title}.jpg', 'wb') as imgfile:
            imgfile.write(backgroundsData.content)


    
    time.sleep(2)
    
    # Получение ссылки на афишу
    afisha = bs.find('a', class_='filmInfo_posterLink')['href']
    afishaData = requests.get(afisha)
    with open(f'afisha/{title}.jpg', 'wb') as imgfile:
        imgfile.write(afishaData.content)
    
    time.sleep(2)
    
    subMenu = bs.find_all('a', class_='subMenu_item')# Поиск элементов саб-меню
    
    timetable = subMenu[1]['href'].replace('msk', 'bratsk')# Ссылка эелмента расписания
    
    
    # Подключение к расписанию фильмов Братска
    url = timetable.replace('kr', 'bratsk')
    request = requests.get(url)
    bs = BeautifulSoup(request.text, 'html.parser')
    
    
    # Сбор данных о времени сеана в кинотеатре Голивуд
    timeGolivud = bs.find(attrs={'data-schedulesearch-item': "Голливуд пщддшмгв ujkkbdel ujkkbdel голливуд gollivud"})
    
    if timeGolivud:
        timeGolivud = timeGolivud.find_all('span', class_='session_time')
    
        golivud = []
        for time in timeGolivud:
            golivud.append(time.text)
    
        golivudStr = ''
        for item in golivud:
            golivudStr = golivudStr + item + ', '
        golivudStr = golivudStr[:-2]
    else:
        golivudStr = "-"
    
    # Сбор данных о времени сеана в кинотеатре Чарли
    timeCharley = bs.find(attrs={'data-schedulesearch-item': "Чарли срфкдш xfhkb xfhkb чарли charli"})
    
    if timeCharley:
        timeCharley = timeCharley.find_all('span', class_='session_time')
    
        charley = []
        for time in timeCharley:
            charley.append(time.text)
        charleyStr = ''
        for item in charley:
            charleyStr = charleyStr + item + ', '
        charleyStr = charleyStr[:-2]
    else:
        charleyStr = "-"


    timeCenterCinema = bs.find(attrs={'data-schedulesearch-item': 'Центр Кино сутек лштщ wtynh rbyj wtynh rbyj центр кино centr kino'})

    if timeCenterCinema:
        timeCenterCinema = timeCenterCinema.find_all('span', class_='session_time')
        centerCinema = []

        for time in timeCenterCinema:
            centerCinema.append(time.text)

        cinemaCenterStr = ''

        for item in centerCinema:
            cinemaCenterStr = cinemaCenterStr + item + ', '

        cinemaCenterStr = cinemaCenterStr[:-2]
    else:
        cinemaCenterStr = '-'


    createBaner.create_banner(title, genresStr, duration, yearRelease, dateRussiaRelease, ageLimit, description, golivudStr, charleyStr, cinemaCenterStr)

    print('[GET FILM]')

def started():
    for href in hrefs:
        parsFilm(href['href'])
