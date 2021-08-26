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
    'num_followersError': 'header ul li:nth-child(2) span span',
    'num_following': 'header ul li:nth-child(3) span',
    'verificado': '//*[@id="react-root"]/section/main/div/header/section/div[1]/div[1]/span',
    'following': 'header ul li:nth-child(3) a',

}


class instagramInfo:

    def __init__(self):
        # chrome_options = webdriver.ChromeOptions()
        # chrome_options.add_argument("--headless")
        # self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
        self.limit = int(input("Digite a Quantidade Mínima que deseja de Seguidores: "))
        self.driver = webdriver.Chrome(ChromeDriverManager().install())
        self.driver.set_window_position(-10000, 0)
        self.driver.delete_all_cookies()
        with open('nomes.txt', 'r') as contas:
            self.usernames = contas.readlines()
            # print(self.usernames)

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
            self.driver.refresh()

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

    def buscarDados(self):

        time.sleep(5)
        self.driver.get(f'https://instagram.com/{self.user}')
        print(f'Capturando dados do perfil - {self.user}')

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
            self.num_posts = 0
        # print(self.num_posts)

        #     PEGAR NÚMERO DE SEGUIDORES
        try:
            self.num_followers = int(
                self.driver.find_element_by_css_selector(selectors['num_followers']).get_attribute('title').replace('.',
                                                                                                                    ''))
        except:
            try:
                self.num_followers = int(self.driver.find_element_by_css_selector(selectors['num_followersError']).get_attribute('title').replace('.', ''))
            except:
                self.driver.refresh()
        # print(self.num_followers)

        #     PEGAR NÚMERO DE SEGUIDOS
        try:
            self.num_following = self.driver.find_element_by_css_selector(selectors['num_following']).text.replace(
                ',', '')
        except:
            self.num_following = 0

        # PROCURAR NÚMERO DE TELEFONE
        try:
            insta = self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section').text
        except:
            self.driver.refresh()

        try:
            self.phones = re.findall(r'\(?\d{2}\)?-? *\d{4}-? *-?\d{4}\b', insta)
        except:
            self.phones = 0

        # PROCURAR E-MAIL
        try:
            self.email = re.findall(r'[\w\.-]+@[\w\.-]+', insta)
        except:
            self.email = 0

    def capturarSeguidos(self):
        time.sleep(2)
        try:
            self.driver.find_element_by_css_selector(selectors['following']).click()
        except:
            print('...Não foi possivel capturar os Seguidores dessa conta...')
            self.names = []
            return
        time.sleep(2)

        scroll_box = self.driver.find_element_by_xpath("/html/body/div[6]/div/div/div[3]")

        while len(scroll_box.find_elements_by_tag_name('a')) < 1:
            print("...Aguardando carregar a Lista de Seguidos...")
            time.sleep(1)

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
        print(f'Pegando os Seguidos...')
        # self.infoSeguidos()
        self.gerarDataFrameSeguindos()

    def infoSeguidos(self):
        for self.user in self.names:
            self.buscarDados()
            # print(self.num_followers)

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

        dat1 = pd.DataFrame.from_dict(informacoesPerfil, orient='index').transpose()
        # columns = ['Nome', 'Qnt Posts', 'Qnt Seguidores', 'Qnt Seguindo', 'Situacao', 'Telefone','Email']
        print(f'DADOS {dat1}')
        # CRIAÇÃO DE DATAFRAME DOS SEGUINDOS

        d = {'Seguidos': self.names}
        if self.dat2.empty:
            dat = dat1
            loc = 'minimo/'
        else:
            # JUNÇÃO DE INFORMAÇÕES DE DATAFRAMES
            dat = pd.concat([pd.DataFrame({})] + [self.dat2, dat1], axis=1)
            self.dat2 = self.dat2.iloc[0:0]
            loc = 'maximo/'

        return dat.to_csv(f'{loc}{self.user}.csv')

    def gerarDataFrameSeguindos(self):
        # CRIAÇÃO DE DATAFRAME DOS SEGUINDOS
        d = {'Seguidos': self.names}
        self.dat2 = pd.DataFrame(d)
        return self.dat2

    # CAPTURA DADOS DO ARQUIVO DE ENTRADA TXT
    def capturarDados(self):
        for self.user in self.usernames:
            self.user = self.user.replace('\n', '')
            self.buscarDados()
            print('Capturando Seguidores...')
            self.capturarSeguidos()
            self.geraInfoPerfil()
            self.infoSeguidos()

            # driver.delete_all_cookies()
        self.driver.quit()


ini = instagramInfo()
ini.login()
