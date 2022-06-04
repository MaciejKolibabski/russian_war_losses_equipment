from math import ceil
from tkinter import *
import pandas as pd
from kaggle.api.kaggle_api_extended import KaggleApi
import plotly.express as px

api = KaggleApi()
api.authenticate()

api.dataset_download_file('piterfm/2022-ukraine-russian-war',
                          file_name='russia_losses_equipment.csv')

api1 = KaggleApi()
api1.authenticate()

api1.dataset_download_file('piterfm/2022-ukraine-russian-war',
                           file_name='russia_losses_personnel.csv')

data = pd.read_csv('russia_losses_equipment.csv')

data1 = pd.read_csv('russia_losses_personnel.csv')

data["Ludzie"] = data1['personnel']
data.to_csv("russia_losses_equipment.csv", index=False)

df_aircraft = data['aircraft']
df_tanks = data['tank']
df_drone = data['drone']
df_date = data['date']
data["sum_eq"] = df_aircraft + df_tanks + df_drone
data.to_csv("russia_losses_equipment.csv", index=False)
df_suma = data['sum_eq']
df_ludzie = data['Ludzie']

aircrafts_pom = []
drones_pom = []
tanks_pom = []
suma_eq_pom = []
ludzie_pom = []

aircrafts = []
tanks = []
drones = []
suma_eq = []
ludzie = []

for i in df_aircraft:
    aircrafts_pom.append(i)
for i in df_drone:
    drones_pom.append(i)
for i in df_tanks:
    tanks_pom.append(i)
for i in df_suma:
    suma_eq_pom.append(i)
for i in df_ludzie:
    ludzie_pom.append(i)

for i in range(0, len(aircrafts_pom)):
    if i >= 1:
        aircrafts.append(aircrafts_pom[i] - aircrafts_pom[i - 1] + 1)
        drones.append(drones_pom[i] - drones_pom[i - 1] + 1)
        tanks.append(tanks_pom[i] - tanks_pom[i - 1] + 1)
        suma_eq.append(suma_eq_pom[i] - suma_eq_pom[i - 1] + 1)
        ludzie.append(ludzie_pom[i] - ludzie_pom[i - 1] + 1)
    elif i == 0:
        aircrafts.append(aircrafts_pom[i] + 1)
        drones.append(drones_pom[i] + 1)
        tanks.append(tanks_pom[i] + 1)
        suma_eq.append(suma_eq_pom[i] + 1)
        ludzie.append(ludzie_pom[i] + 1)

data["Ilość"] = suma_eq
data.to_csv("russia_losses_equipment.csv", index=False)
data["Samoloty"] = aircrafts
data.to_csv("russia_losses_equipment.csv", index=False)
data["Czołgi"] = tanks
data.to_csv("russia_losses_equipment.csv", index=False)
data["Drony"] = drones
data.to_csv("russia_losses_equipment.csv", index=False)
data["Tydzień"] = 0
data.to_csv("russia_losses_equipment.csv", index=False)
data["Żołnierze"] = ludzie
data.to_csv("russia_losses_equipment.csv", index=False)

d = {1: 'Pierwszy', 2: 'Drugi', 3: 'Trzeci', 4: 'Czwarty', 5: 'Piąty', 6: 'Szósty',
     7: 'Siódmy', 8: 'Ósmy', 9: 'Dziewiąty', 10: 'Dziesiąty', 11: 'Jedenasty', 12: 'Dwunasty',
     13: 'Trzynasty', 14: 'Czternasty', 15: 'Piętnasty', 16: 'Szesnasty', 17: 'Siedemnasty'}

data_list = data.values.tolist()

for i in range(0, len(data_list)):
    linia = data_list[i]
    data.loc[i, 'Tydzień'] = d[ceil(linia[1] / 7)]
data.to_csv("russia_losses_equipment.csv", index=False)


def wykres_ilosc():
    choice = value_inside.get()
    if choice == 'Wszystko':
        fig = px.scatter(data, x=data['date'], y=data['Ilość'], color='Tydzień',
                         marginal_y='box', marginal_x= 'histogram', size='Żołnierze')

        fig.show()
    if choice == 'Samoloty':
        fig = px.scatter(data, x=data['date'], y=data['Samoloty'], color='Tydzień',
                         marginal_y='box')

        fig.show()
    if choice == 'Drony':
        fig = px.scatter(data, x=data['date'], y=data['Drony'], color='Tydzień',
                         marginal_y='box')

        fig.show()
    if choice == 'Czołgi':
        fig = px.scatter(data, x=data['date'], y=data['Czołgi'], color='Tydzień',
                         marginal_y='box')

        fig.show()


app = Tk()

option_list = ['Wszystko', 'Samoloty', 'Czołgi', 'Drony']
value_inside = StringVar(app)
value_inside.set("Wybierz")

hello_text = Label(app, text='Straty poniesione przez rosję podczas konfliktu na Ukrainie ', font=('bold', 18),
                   bg='#612d2d', fg='#ffffff')
hello_text.grid(row=0, sticky=W, pady=20, padx=35)

label_filtry = Label(app, text='Filtry: ', font=('bold', 14), bg='#612d2d', fg='#ffffff')
label_filtry.grid(row=2, sticky=W, pady=45, padx=250)
filtry = OptionMenu(app, value_inside, *option_list)
filtry.grid(row=2, sticky=W, pady=5, padx=350)

draw_chart = Button(app, text='Pokaż wizualizację', width=62, bg='#406abd', fg='#000000', command=wykres_ilosc)
draw_chart.grid(row=4, sticky=W, pady=30, padx=130)

app.title('Wizualizacja Zadanie 4 ')
app.configure(background='#612d2d')
app.geometry('700x360')
app.minsize(700, 360)
app.maxsize(700, 360)
app.mainloop()
