import os
from tinytag import *
import sqlite3



def parser():
    global temp_track
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()

    print("Подключен к SQLite")


    cur.execute("""CREATE TABLE IF NOT EXISTS songs(
       ID INTEGER PRIMARY KEY ,
       
       artist TEXT,
       title TEXT,
       album TEXT,
       year INTEGER,
       size REAL,
       time REAL,
       UNIQUE (title) ON CONFLICT IGNORE
       );
       
    """)
    print("Таблица создана")
    conn.commit()
    cur.execute("""DELETE FROM songs""")

    print("Start")
    tracks = []
    counter = 0
    for roots, dirs, files in os.walk("D:\Music\music"):
        for name in files:

            if name.endswith((".mp3", ".m4a", ".flac", ".alac")):

                try:
                    temp_track = TinyTag.get(roots + "\\" + name)

                    tracks.append((  temp_track.artist ,temp_track.title, temp_track.album , temp_track.year, temp_track.filesize/1000/1024, os.path.getctime(f"D:\Music\music\{name}" )))

                except:
                    print("Error")

        tracks.sort(key=lambda x: (x[5]), reverse= True)

        for i in tracks:
            counter += 1
            cur.execute("""INSERT OR REPLACE INTO  songs( artist, title, album, year, size, time) 
                                               VALUES( ?, ?, ?, ?, ?,?);""", i )
            conn.commit()
            print(f"Запись успешно вставлена ")
        cur.close()
        print(f"БД успешно закрыта")



parser()
conn = sqlite3.connect('database.db')
cur = conn.cursor()
print("Получить информацию по последним 10 композициям? Y/N ")
b = input()

if b == "Y":
    a = cur.execute("""SELECT * FROM songs WHERE ID BETWEEN 1 AND 10""").fetchall()
    for i in a:
        print(f"Artist: {i[1]}, Title: {i[2]}, Album: {i[3]}, Year: {i[4]}")
else:
    print("Завершение программы")

cur.close()