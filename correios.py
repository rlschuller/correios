#!python3
#coding: utf-8

from bs4 import BeautifulSoup
import requests
import re
import subprocess as s
from time import sleep
import os
import sys

notify_installed=True
try:
    from notify_run import Notify
    phone_notify = Notify()
except:
    if os.name != 'posix':
        print("Erro: Voce nao esta usando linux, e sem notify_run")
        ui = input("Deseja rodar mesmo sem notificacoes? (s/N) ")
        if ui != 's' and ui != 'S' and ui != 'y' and ui != 'Y':
            sys.exit()
    else:
        print("Rodando sem notificacoes para celular.")
    notify_installed=False


def notify(str_data):
    # local notification
    msg = 'Correios\n'+str_data
    print(msg)
    if os.name == 'posix':
        s.call(['notify-send', '-u', 'critical', msg])

    # public notification (hides code)
    if notify_installed: 
        phone_notify.send('Correio\nRastreamento atualizado')


FILENAME="correios.html"
f = open("codigo.txt", "r")
TRACK_CODE = f.read().strip() 
f.close()
url = 'https://www2.correios.com.br/sistemas/rastreamento/ctrl/ctrlRastreamento.cfm'
post_params = {'acao':'track', 'objetos':TRACK_CODE, 'btnPesq':'Buscar'}

# local init msg
msg = "Código\n"+TRACK_CODE
print(msg)
if os.name == 'posix':
    s.call(['notify-send', '-u', 'critical', msg])

# public init msg
if notify_installed:
    phone_notify.send('Correio\nPrograma iniciou')

while True:
    response = requests.post(url, data=post_params)
    soup = BeautifulSoup(response.text, 'html.parser')
    list_events = soup.findAll("table", {"class":"listEvent sro"})
    events = str(list_events).replace('\r','')
    old_events = ""
    try:
        f = open(FILENAME, "r")
        old_events = str(f.read())
        f.close()
    except IOError:
        print("arquivo "+FILENAME+" nao encontrado")

    # events changed
    if re.sub(r"\s+","",events) != re.sub(r"\s+","",old_events):
        try:
            row = re.split('<|>',str(list_events[0]).split('td')[1] )
            e_date = row[1].strip()
            e_time = row[3].strip()
            e_place = row[5].strip()
            data = e_date+"\n"+e_time+"\n"+e_place
        except:
            print("Excecao na leitura dos dados")
        else:
            f = open(FILENAME, "w")
            print("atualizando "+FILENAME+"...")
            f.write(events)
            f.close()
            notify(data)


    sleep(120)
