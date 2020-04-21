#!python3
from bs4 import BeautifulSoup
import requests
import re
import subprocess as s
from time import sleep
import os

FILENAME="correios.html"

f = open("codigo.txt", "r")
TRACK_CODE = f.read().strip() 
f.close()

url = 'https://www2.correios.com.br/sistemas/rastreamento/ctrl/ctrlRastreamento.cfm'
post_params = {'acao':'track', 'objetos':TRACK_CODE, 'btnPesq':'Buscar'}

def notify(str_data):
    if os.name == 'posix':
        s.call(['notify-send', '-u', 'critical','Correios', str_data])
    if os.name == 'nt':
        s.call(['msg', '*', '/W','Correios\n'+ str_data])

first=True
notify("Código: " + TRACK_CODE)

while True:
    response = requests.post(url, data=post_params)
    soup = BeautifulSoup(response.text, 'html.parser')
    list_events = soup.findAll("table", {"class":"listEvent sro"})
    events = str(list_events).replace('\r','')

    last_events = ""
    f = None
    try:
        f = open(FILENAME, "r")
        last_events = str(f.read())
        f.close()
    except IOError:
        print("can't read "+FILENAME)

    event_changed = re.sub(r"\s+","",events) != re.sub(r"\s+","",last_events)
    if event_changed:
        f = open(FILENAME, "w")
        print("updating "+FILENAME+"...")
        f.write(events)
        f.close()
    if event_changed or first:
        row = re.split('<|>',str(list_events[0]).split('td')[1] )
        e_date = row[1].strip()
        e_time = row[3].strip()
        e_place = row[5].strip()
        data = e_date+"\n"+e_time+"\n"+e_place
        notify(data)
        first = False
    sleep(120)
