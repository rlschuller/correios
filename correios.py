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
notify_url=None
try:
    from notify_run import Notify
    phone_notify = Notify()
except:
    notify_installed=False
    if os.name != 'posix':
        print("Aviso: Voce nao esta usando linux, notificacoes para Desktop estao desativadas")
    try:
        print("lendo arquivo 'notify_run_url.txt'...")
        f = open("notify_url.txt", "r")
        notify_url = f.read().strip()
        f.close()
    except:
        notify_url = input("Erro de leitura, digite o url\n").strip()
        print("salvando arquivo 'notify_run_url.txt'...")
        f = open("notify_url.txt", "w")
        f.write(notify_url)
        f.close()

def notify(private_msg, public_msg):
    # local notification
    print(private_msg)
    if os.name == 'posix':
        s.call(['notify-send', '-u', 'critical', private_msg])

    # public notification (hides code)
    if notify_installed: 
        phone_notify.send(public_msg)
    else:
        if str(requests.post(notify_url, public_msg)) != "<Response [200]>":
            print("Erro mandando mensagem, url='"+notify_url+"', verifique o arquivo notify_url.txt")

FILENAME="correios.html"
f = open("codigo.txt", "r")
TRACK_CODE = f.read().strip() 
f.close()
url = 'https://www2.correios.com.br/sistemas/rastreamento/ctrl/ctrlRastreamento.cfm'
post_params = {'acao':'track', 'objetos':TRACK_CODE, 'btnPesq':'Buscar'}

# local init msg
private_msg = "Código\n"+TRACK_CODE
public_msg = 'Correios\nPrograma iniciou'
notify(private_msg, public_msg)

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
            print("Excecao na leitura dos dados, mostrados a seguir:")
            print(events)
        else:
            f = open(FILENAME, "w")
            print("atualizando "+FILENAME+"...")
            f.write(events)
            f.close()
            private_msg = 'Correios\n'+data
            public_msg = 'Correios\nEvento atualizado'
            notify(private_msg, public_msg)
    sleep(120)
