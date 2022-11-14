import psycopg2
import psycopg2.extras
import csv
import sys

csv.field_size_limit(sys.maxsize)


conn = psycopg2.connect(host="localhost", 
    database="cc3201", user="cc3201", 
    password="viudo.sable.avaro.rutar", 
    port="5432")

cur = conn.cursor()


def findOrInsert(table, name):
    cur.execute("select id from "+table+" where name=%s limit 1", [name])
    r = cur.fetchone()
    if(r):
        return r[0]
    else:
        cur.execute("insert into "+table+" (name) values (%s) returning id", [name])
        return cur.fetchone()[0]



with open("steam.csv", encoding="utf8") as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    j = 0

    for row in reader:

        j += 1
        if j == 1:
            continue
        
        type = row[1]

        if type == "dlc":
            continue

        #Juego
        appid = row[0]
        name = row[2]
        price = row[17] if (row[17]) else None
        release_date = row[14] if (row[14]) else None
        required_age = row[3] if (row[3]) else None
        achievements = int(float(row[13])) if (row[13]) else None

        #Stadistics
        review_score = int(float(row[18])) if (row[18]) else None
        total_positive = int(float(row[19])) if (row[19]) else None
        total_negative = int(float(row[20])) if (row[20]) else None
        rating = row[21] if (row[21]) else None
        owners = (row[22].split("-"))[1] if (row[22]) else None
        average_forever = row[23] if (row[23]) else None
        median_forever = row[24] if (row[24]) else None
        
        #Developers
        developers_unclean = row[7].split(",")
        developers = []
        for i in developers_unclean:
            developers.append(i.strip(" '").strip("['").strip("']"))

        #Publishers
        publishers = []
        publishers_unclean = row[8].split(",")
        for i in publishers_unclean:
            publishers.append(i.strip(" '").strip("['").strip("']"))

        #Platforms
        platforms = []
        platforms_unclean = row[10].split(",")  #maybe
        for i in platforms_unclean:
            platforms.append(i.strip(" '").strip("['").strip("']"))
        
        #Categories
        categories = []
        categories_unclean = row[11].split(",")
        for i in categories_unclean:
            categories.append(i.strip(" '").strip("['").strip("']"))

        #Tags
        tags_unclean = row[25].split(",")
        tags = []
        for i in tags_unclean:
            tags.append(i.strip(" '").strip("['").strip("']"))

        #Languages
        supported_languages_unclean = row[6].split(",") #lista
        supported_languages = []
        for i in supported_languages_unclean:
            supported_languages.append(i.strip(" '").strip("['").strip("']"))


        cur.execute("select appid from Juego where appid=%s", [appid])
        r = cur.fetchone()
        
        if(r):
            continue
        else:
            cur.execute("insert into Juego (appid, name, price, release_date, required_age, achievements) values (%s, %s, %s, %s, %s, %s)", [appid, name, price, release_date, required_age, achievements])
            cur.execute("insert into Stadistics (appid, review_score, total_positive, total_negative, rating, owners, average_forever, median_forever) values (%s, %s, %s, %s, %s, %s, %s, %s)", [appid, review_score, total_positive, total_negative, rating, owners, average_forever, median_forever])
            
            for x in developers:
                cur.execute("select appid from Desarrolla where appid=%s and dev = %s", [appid, x])
                r = cur.fetchone()
                if(r):
                    pass
                else:
                    cur.execute("insert into Desarrolla (appid, dev) values (%s, %s)", [appid, x])

            for x in publishers:
                cur.execute("select appid from Publica where appid=%s and pub = %s", [appid, x])
                r = cur.fetchone()
                if(r):
                    pass
                else:
                    cur.execute("insert into Publica (appid, pub) values (%s, %s)", [appid, x])

            for x in categories:
                cur.execute("select appid from Categoriza where appid=%s and cat = %s", [appid, x])
                r = cur.fetchone()
                if(r):
                    pass
                else:
                    cur.execute("insert into Categoriza (appid, cat) values (%s, %s)", [appid, x])

            for x in tags:
                cur.execute("select appid from Representa where appid=%s and tag = %s", [appid, x])
                r = cur.fetchone()
                if(r):
                    pass
                else:
                    cur.execute("insert into Representa (appid, tag) values (%s, %s)", [appid, x])

            for x in supported_languages:
                cur.execute("select appid from Soporta where appid=%s and len = %s", [appid, x])
                r = cur.fetchone()
                if(r):
                    pass
                else:
                    cur.execute("insert into Soporta (appid, len) values (%s, %s)", [appid, x])
            

    conn.commit()
    csvfile.close()

with open('steam_optional.csv', encoding="utf8") as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    i = 0
    for row in reader:
        i+=1
        if i == 1:
            continue

        #Score
        appid = row[0]
        metacritic_score = int(float(row[5])) if (row[5]) else None

        cur.execute("select appid from Juego where appid=%s", [appid])
        r = cur.fetchone()
        
        if(r):
            cur.execute("select appid from Score where appid=%s", [appid])
            r = cur.fetchone()
            if(r):
                continue
            else:
                cur.execute("insert into Score (appid, metacritic_score) values (%s, %s)", [appid, metacritic_score])
        else:
            continue

    conn.commit()
    csvfile.close()


with open('steam_requirements_data.csv', encoding="utf8") as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    i = 0
    for row in reader:
        i+=1
        if i == 1:
            continue
        
        #OS - Limita
        appid = row[0]

        pc_requirements = row[1]
        mac_requirements = row[2]
        linux_requirements = row[3]

        pc_minimum = row[4]
        pc_recommended = row[5]
        mac_minimum = row[6]
        mac_recommended = row[7]


        ##si no tiene datos de un sistema, aparece []
        cur.execute("select appid from Juego where appid=%s", [appid])
        r = cur.fetchone()
        
        if(r):
            if pc_requirements != '[]':
                cur.execute("select appid from Limita where appid=%s and os = 'Windows'", [appid])
                r = cur.fetchone()
                if (r):
                    pass
                else:
                    cur.execute("insert into Limita (appid, os, minimum, recommended) values (%s, 'Windows', %s, %s) returning appid", [appid, pc_minimum, pc_recommended])

            if mac_requirements != '[]':
                cur.execute("select appid from Limita where appid=%s and os = 'Mac'", [appid])
                r = cur.fetchone()
                if (r):
                    pass
                else:
                    cur.execute("insert into Limita (appid, os, minimum, recommended) values (%s, 'Mac', %s, %s) returning appid", [appid, mac_minimum, mac_recommended])
        else:
            continue    


    conn.commit()
    csvfile.close()

with open('steam_description_data.csv', encoding="utf8") as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    i = 0
    for row in reader:
        i+=1
        if i == 1:
            continue
  
        #Description_data
        appid = row[0]
        short_description = row[3]

        cur.execute("select appid from Juego where appid=%s", [appid])
        r = cur.fetchone()
        
        if(r):
            cur.execute("select appid from Description_data where appid=%s", [appid])
            r = cur.fetchone()
            if(r):
                continue
            else:
                cur.execute("insert into Description_data (appid, short_description) values (%s, %s)", [appid, short_description])
        else:
            continue


    conn.commit()
    csvfile.close()

conn.close() 