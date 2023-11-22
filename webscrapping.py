from selenium import webdriver
# from webdriver_manager.chrome import ChromeDriverManager
# from webdriver_manager import WebDriverManager
from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from unidecode import unidecode
import pandas as pd
import re



    

listaprod = ['SUCO DEL VALLE NÉCTAR SABOR UVA SEM AÇÚCAR TP 1L', 'ARROZ PARBOILIZADO CAMIL INTEGRAL 1KG', 'FEIJAO CAMIL 1KG', 'OLEO LISA', 'ACUCAR UNIAO', 'SAL LEBRE']
df = pd.DataFrame()
i = 0

service = Service(executable_path=f'C:\\path\\msedgedriver.exe')
driver = webdriver.Edge(service=service)

while i < len(listaprod):

    driver.get("https://www.sondadelivery.com.br/delivery")
    time.sleep(5)
    find = driver.find_element("xpath",'//*[@id="ctl00_txtBusca"]')
    find.send_keys(listaprod[i])
    time.sleep(5)
    findbutton = driver.find_element("xpath",'//*[@id="ctl00_lbtnBuscar"]')
    findbutton.click()
    time.sleep(5)
    url = driver.current_url
    time.sleep(5)


    headers = {'user-agent' : 'Mozilla/5.0'}
    resposta = requests.get('https://www.sondadelivery.com.br/delivery/busca/SUCO%20DEL%20VALLE%20NÉCTAR%20SABOR%20UVA%20SEM%20AÇÚCAR%20TP%201L',
    headers = headers)
    resposta = requests.get(url,headers = headers)
    sopa = resposta.text
    btfsoup = BeautifulSoup(sopa, 'html.parser')


    lista = btfsoup.find_all('div',{'class':'product--info'})
    # print(btfsoup)
    print(lista[0].contents[3].text)


    dfsonda = pd.DataFrame()
    dfsonda['nome'] = [lista[0].contents[1].text]
    dfsonda['preco']= [lista[0].contents[3].text]
    dfsonda['idMercado']= 1
    dfsonda['idProduto']= i
    dfsonda =dfsonda.replace(r'\n','',regex=True)
    dfsonda['preco'] = dfsonda['preco'].str.replace(r'[a-zA-Z]', '', regex=True)
    dfsonda['preco'] = dfsonda['preco'].str.replace('$', '')
    dfsonda['preco'] = dfsonda['preco'].str.replace(' ', '')
    dfsonda['nome'] = dfsonda['nome'].apply(unidecode)
    df = pd.concat([df,dfsonda])

    print(df)
    print('-----')
    print('mercado2')



    driver.get("https://www.superpaguemenos.com.br")
    time.sleep(5)
    find = driver.find_element("xpath",'//*[@id="main-wrapper"]/header/div[2]/div/div/div[3]/div/form/input')
    find.send_keys(listaprod[i])
    find.send_keys(Keys.ENTER)
    time.sleep(5)
    url = driver.current_url
    time.sleep(5)

    headers = {'user-agent' : 'Mozilla/5.0'}
    resposta = requests.get('https://www.superpaguemenos.com.br/néctar%20del%20valle%20zero%20açúcar%20uva%201l/',
    headers = headers)
    resposta = requests.get(url,headers = headers)
    sopa = resposta.text
    btfsoup = BeautifulSoup(sopa, 'html.parser')
    lista = btfsoup.find_all('div',{'class':'desc position-relative'})
    textoimagem = sopa.split('data-src="')[1]
    textoimagem = textoimagem.split('" src')[0]


    texto = lista[0].contents[0].text

    t1 = texto.split('R$')[0]
    t1 = re.sub(' +', ' ', t1)
    t2 = texto.split('R$')[1]
    dfpb = pd.DataFrame()
    dfpb['nome'] = [t1]
    dfpb['preco']= [t2]
    dfpb['idMercado']= [2]
    dfpb['idProduto']= [i]
    dfpb['imagem']= [textoimagem]
    df['imagem']= [textoimagem]
    dfpb =dfpb.replace(r'\n','',regex=True)
    dfpb['preco'] = dfpb['preco'].str.replace(r'[a-zA-Z]', '', regex=True)
    dfpb['preco'] = dfpb['preco'].str.replace('$', '')
    dfpb['preco'] = dfpb['preco'].str.replace(' ', '')
    dfpb['nome'] = dfpb['nome'].apply(unidecode)
    df = pd.concat([df,dfpb])


    driver.get('https://www.nagumo.com.br/guarulhos-lj42-guarulhos-aruja-cumbica-caminho-do-campo-do-rincao')

    time.sleep(5)
    driver.maximize_window()
    time.sleep(5)
    find = driver.find_element("xpath",'/html/body/app-root/app-sm-master-page/app-header-desk-main/div[1]/div/div/div/div[2]/div[2]/div[1]/app-search-bar/div/div/input')
    find.send_keys(listaprod[i])
    find.send_keys(Keys.ENTER)
    time.sleep(5)
    url = driver.current_url
    print(url)
    print(url)
    print(url)
    time.sleep(5)


    headers = {'user-agent' : 'Mozilla/5.0'}
    resposta = requests.get('https://www.nagumo.com.br/guarulhos-lj42-guarulhos-aruja-cumbica-caminho-do-campo-do-rincao/busca/suco%2520del%252Bvalle%252Buva%252Bsem%252Bacucar',
    headers = headers)
    resposta = requests.get(url,headers = headers)
    #print (resposta.text)
    sopa = resposta.text
    btfsoup = BeautifulSoup(sopa, 'html.parser')
    lista = btfsoup.find_all('div',{'class':'list-product-item'})

    print('mercado3')


    texto = lista[0].contents[0].text
    preco = texto.split(' ')[1]
    valor = 'R$ '
    nome = texto.split(preco)[1]
    nome = nome.strip()
    dfnagumo = pd.DataFrame()
    dfnagumo['nome'] = [nome]
    dfnagumo['preco']= [preco]
    dfnagumo['idMercado']= [3]
    dfnagumo['idProduto']= [i]
    dfnagumo['imagem']= [textoimagem]
    df = pd.concat([df,dfnagumo])

    i=i+1


#jsondict = df.to_json('tests/test1.json', orient='records')
df.to_json(r'C:\\Users\\Guilherme\\Downloads\\test2222.json', orient='records')


import json
with open(r'C:\\path\\test2222.json') as f:
    dfjson = json.load(f)

print(dfjson)


import requests

headers = {
    'Content-Type': 'application/json',
    'authorization': 'UGVjdW5pYTpxdm1jc3JiZHVhbXN4eWVl',
}

json_data = dfjson

response = requests.post('https://pecunia-api.onrender.com/createUpdateProducts', headers=headers, json=json_data)

