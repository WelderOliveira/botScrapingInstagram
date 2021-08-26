import re
import time

import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

selectors = {
    'username': '//input[@name="username"]',
    'passwd': '//input[@name="password"]',
    'name': 'header h1',
    'num_posts': 'header ul li:nth-child(1) span span',
    'num_followers': 'header ul li:nth-child(2) span',
    'num_following': 'header ul li:nth-child(3) span',
    'verificado': '//*[@id="react-root"]/section/main/div/header/section/div[1]/div[1]/span',
    'following': 'header ul li:nth-child(3) a',

}


# # chrome_options = webdriver.ChromeOptions()
# # chrome_options.add_argument('headless')
# # driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
# driver = webdriver.Chrome(ChromeDriverManager().install())
# driver.delete_all_cookies()
# usernames = ['pecararaplanaltina', 'virginia', 'anitta']


class instagramInfo:

    def __init__(self):
        # chrome_options = webdriver.ChromeOptions()
        # chrome_options.add_argument("--headless")
        # self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
        self.driver = webdriver.Chrome(ChromeDriverManager().install())
        # self.driver.set_window_position(-10000, 0)
        self.driver.delete_all_cookies()
        self.limit = int(input("Digite a Quantidade Mínima que deseja de Seguidores: "))
        self.usernames = ['hobbydasorte', 'pecararaplanaltina', 'virginia', 'anitta']

    def login(self):

        # CAPTURAR DADOS DE LOGIN EM ARQUIVO TXT
        with open('login.txt', 'r') as arquivoLogin:
            linhas = arquivoLogin.readlines()
            usuario = linhas[0].split(':')[1]
            senha = linhas[1].split(':')[1]

        #     INICIA O INSTAGRAM
        self.driver.get('https://instagram.com/')

        # AGUARDA ENQUANTO A PAGINA DO INSTAGRAM CARREGA
        while len(self.driver.find_elements_by_name('username')) < 1:
            time.sleep(1)

        #     EFETUA LOGIN
        user = self.driver.find_element_by_xpath(selectors['username'])
        user.clear()
        user.send_keys(usuario)

        password = self.driver.find_element_by_xpath(selectors['passwd'])
        password.clear()
        password.send_keys(senha)

        password.send_keys(Keys.RETURN)
        time.sleep(3)
        self.capturarDados()

    def buscarDados(self, user):

        time.sleep(5)
        self.driver.get(f'https://instagram.com/{user}')
        print(f'Capturando dados do perfil - {user}')

        # PEGAR SE O PERFIL É VERIFICADO OU NÃO
        try:
            self.status = self.driver.find_element_by_xpath(selectors['verificado']).text
        except:
            self.status = 'NAO VERIFICADO'
        # print(status)

        #     PEGAR NOME
        try:
            self.name_el = self.driver.find_element_by_css_selector(selectors['name']).text
        except:
            self.name_el = 'NOT FOUND'
        # print(name_el)

        #     PEGAR NÚMERO DE POSTS
        try:
            self.num_posts = self.driver.find_element_by_css_selector(selectors['num_posts']).text.replace(',', '')
        except:
            self.num_posts = 'NOT FOUND'
        # print(self.num_posts)

        #     PEGAR NÚMERO DE SEGUIDORES
        try:
            self.num_followers = self.driver.find_element_by_css_selector(selectors['num_followers']).get_attribute(
                'title').replace('.', '')
        except:
            self.num_followers = 'NOT FOUND'
        # print(num_followers)

        #     PEGAR NÚMERO DE SEGUIDOS
        try:

            self.num_following = self.driver.find_element_by_css_selector(selectors['num_following']).text.replace(
                ',', '')
        except:
            self.num_following = 'NOT FOUND'

        # PROCURAR NÚMERO DE TELEFONE
        insta = self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section').text
        try:
            self.phones = re.findall(r'\(?\d{2}\)?-? *\d{4}-? *-?\d{4}\b', insta)
        except:
            self.phones = ''

        # PROCURAR E-MAIL
        try:
            self.email = re.findall(r'[\w\.-]+@[\w\.-]+', insta)
        except:
            self.email = ''

    def capturarSeguidos(self):
        time.sleep(5)
        self.driver.find_element_by_css_selector(selectors['following']).click()

        time.sleep(2)

        scroll_box = self.driver.find_element_by_xpath("/html/body/div[6]/div/div/div[3]")
        prev_height, height = 0, 1

        while prev_height != height:
            prev_height = height
            time.sleep(3)
            height = self.driver.execute_script("""
                        arguments[0].scrollTo(0, arguments[0].scrollHeight); 
                        return arguments[0].scrollHeight;
                        """, scroll_box)
        links = scroll_box.find_elements_by_tag_name('a')
        self.names = [name.text for name in links if name.text != '']
        print(f'TO TENTANDO {self.names}')
        # self.infoSeguidos()
        self.gerarDataFrameSeguindos()

    def infoSeguidos(self):
        for nome in self.names:
            self.buscarDados(nome)

            if int(self.num_followers) > self.limit:
                self.capturarSeguidos()

            self.geraInfoPerfil()

    def geraInfoPerfil(self):

        # GERA O CSV COM AS INFORMAÇÕES
        informacoesPerfil = {'Nome': self.name_el, 'Quantidade Posts': self.num_posts,
                             'Quantidade Seguidores': self.num_followers,
                             'Quantidade Seguindo': self.num_following,
                             'Verificado': self.status,
                             'Telefone': self.phones,
                             'Email': self.email}
        # print(informacoesPerfil)
        dat1 = pd.DataFrame.from_dict(informacoesPerfil, orient='index').transpose()
        # columns = ['Nome', 'Qnt Posts', 'Qnt Seguidores', 'Qnt Seguindo', 'Situacao', 'Telefone','Email']
        print(f'DICIONARIO {dat1}')
        # CRIAÇÃO DE DATAFRAME DOS SEGUINDOS
        d = {'Seguidos': self.names}
        # print(f'TOO TEEENTADDOOO2 {d}')
        # dat2 = pd.DataFrame(d)
        # print(f'FODA SE {dat2}')
        if self.dat2.empty:
            # print("Entrei no IF")
            # JUNÇÃO DE INFORMAÇÕES DE DATAFRAMES
            dat = dat1
        else:
            print(len(self.dat2.columns))
            dat = pd.concat([pd.DataFrame({})] + [self.dat2, dat1], axis=1)
            self.dat2 = self.dat2.iloc[0:0]

        return dat.to_csv(f'{self.name_el}.csv')

    def gerarDataFrameSeguindos(self):
        # CRIAÇÃO DE DATAFRAME DOS SEGUINDOS
        d = {'Seguidos': self.names}
        self.dat2 = pd.DataFrame(d)
        return self.dat2

    # CAPTURA DADOS DO ARQUIVO DE ENTRADA TXT
    def capturarDados(self):
        for self.username in self.usernames:
            self.buscarDados(self.username)
            print('Capturando Seguidores...')
            self.capturarSeguidos()
            self.geraInfoPerfil()
            self.infoSeguidos()

            # driver.delete_all_cookies()
        self.driver.quit()


ini = instagramInfo()
ini.login()
