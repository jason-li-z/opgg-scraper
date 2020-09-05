from bs4 import BeautifulSoup
import requests
import csv
import time

champ_counter = {}
listOfRefs = []


def getHighest():
    listOfURL = getURL()
    parse = listOfURL[0]
    req = requests.get(parse)
    soup = BeautifulSoup(req.text, 'html.parser')
    highest = soup.find('ul', class_='ranking-highest__list')
    for player in highest:
        curr = player.find("a")
        listOfRefs.append("https:" + curr['href'])


def getPlayers():
    listOfURL = getURL()
    for url in listOfURL:
        req = requests.get(url)
        soup = BeautifulSoup(req.text, 'html.parser')
        playersTable = soup.find('table', class_='ranking-table')
        for player in playersTable.find_all('tbody'):
            rows = player.find_all('tr')
            for row in rows:
                alink = row.find(
                    'td', class_='select_summoner ranking-table__cell ranking-table__cell--summoner').find('a')
                listOfRefs.append("https:" + alink['href'])


def scrapePlayers():
    getHighest()
    getPlayers()
    players = listOfRefs
    for player in players:
        req = requests.get(player)
        soup = BeautifulSoup(req.text, 'html.parser')
        champs = soup.find_all('div', class_='ChampionBox Ranked')
        for champ in champs:
            name = champ.find("div", class_="ChampionName")
            champ_name = name.text.strip()
            if champ_name in champ_counter:
                champ_counter[champ_name] += 1
            else:
                champ_counter[champ_name] = 1


def getURL():
    listOfUrl = []
    for i in range(1, 28):
        listOfUrl.append('https://jp.op.gg/ranking/ladder/page=' + str(i))
    return listOfUrl


start = time.time()


scrapePlayers()


# Sort descending
sort_champs = sorted(champ_counter.items(), key=lambda x: x[1], reverse=True)

with open('jp-sample.csv', 'w') as f:
    for k in sort_champs:
        f.write("%s, %s\n" % (k[0], k[1]))

end = time.time()


print("Total elapsed time: " + str(end - start) + " seconds")
