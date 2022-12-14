import os
from tinytag import *
import sqlite3
from tkinter import *

def cliclk1():
    finish = Label(window, text="Конец программы")
    finish.grid(column=0, row=3)


def cliclk2():

    counter = 2
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    a = cur.execute("""SELECT * FROM songs WHERE ID BETWEEN 1 AND 10""").fetchall()
    for i in a:
        counter+=1
        finish2 = Label(window, text=f"{counter- 2} - Artist: {i[1]}, Title: {i[2]}, Album: {i[3]}, Year: {i[4]}, Size: {i[5]}, Bitrate: {i[6]} kBits/s, Sample: {i[7]}", anchor= W)
        finish2.grid(column=0, row=counter)


    cur.close()
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
       bitrate TEXT,
       samples REAL,
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

                    tracks.append((  temp_track.artist ,temp_track.title, temp_track.album , temp_track.year, temp_track.filesize/1000/1024, os.path.getctime(f"D:\Music\music\{name}" ), f"{temp_track.bitrate} kBits/s", temp_track.samplerate))

                except:
                    print("Error")

        tracks.sort(key=lambda x: (x[5]), reverse= True)

        for i in tracks:
            counter += 1
            cur.execute("""INSERT OR REPLACE INTO  songs( artist, title, album, year, size, time, bitrate, samples) 
                                               VALUES( ?, ?, ?, ?, ?,?,?, ?);""", i )
            conn.commit()
            print(f"Запись успешно вставлена ")
        cur.close()
        print(f"БД успешно закрыта")




if os.listdir("D:\Music\music"):
    parser()

    window = Tk()
    window.title("Выгрузка из БД")
    request = Label(window, text="Получить информацию по последним 10 композициям? Y/N ", anchor= CENTER)
    request.grid(column=0, row=0)
    window.geometry('1000x280')

    btn = Button(window, text="Да", command=cliclk2)
    btn.grid(column=0, row=1)

    btn1 = Button(window, text="Нет", command=cliclk1)
    btn1.grid(column=1, row=1)

    window.mainloop()
else:
    print("ПАПКА ПУСТА.")