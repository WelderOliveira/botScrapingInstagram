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
        self.driver.set_window_position(-10000, 0)
        self.driver.delete_all_cookies()
        self.usernames = ['pecararaplanaltina', 'virginia', 'anitta']

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

    def infoSeguidos(self):
        for nome in self.names:
            print(nome)

    def geraInfoPerfil(self):

        # GERA O CSV COM AS INFORMAÇÕES
        informacoesPerfil = {'Nome': self.name_el, 'Quantidade Posts': self.num_posts,
                             'Quantidade Seguidores': self.num_followers,
                             'Quantidade Seguindo': self.num_following,
                             'Verificado': self.status}
        dat1 = pd.DataFrame(informacoesPerfil, [0])

        # CRIAÇÃO DE DATAFRAME DOS SEGUINDOS
        d = {'Seguidos': self.names}
        dat2 = pd.DataFrame(d)

        # JUNÇÃO DE INFORMAÇÕES DE DATAFRAMES
        dat = pd.concat([pd.DataFrame({})] + [dat1, dat2], axis=1)

        return dat.to_csv(f'{self.username}.csv')

    def capturarDados(self):
        for self.username in self.usernames:

            time.sleep(6)
            self.driver.get(f'https://instagram.com/{self.username}')
            print(f'Capturando dados do perfil - {self.username}')

            # PEGAR SE O PERFIL É VERIFICADO OU NÃO
            try:
                self.status = self.driver.find_element_by_xpath(selectors['verificado']).text
            except:
                self.status = 'NAO VERIFICADO'
            # print(status)

            #     PEGAR NOME
            self.name_el = self.driver.find_element_by_css_selector(selectors['name']).text
            # print(name_el)

            #     PEGAR NÚMERO DE POSTS
            self.num_posts = self.driver.find_element_by_css_selector(selectors['num_posts']).text.replace(',', '')
            # print(self.num_posts)

            #     PEGAR NÚMERO DE SEGUIDORES
            self.num_followers = self.driver.find_element_by_css_selector(selectors['num_followers']).get_attribute(
                'title')
            # print(num_followers)

            #     PEGAR NÚMERO DE SEGUIDOS
            self.num_following = self.driver.find_element_by_css_selector(selectors['num_following']).text.replace(',',
                                                                                                                   '')
            # print(num_following)
            print('Capturando Seguidores...')
            self.capturarSeguidos()
            self.geraInfoPerfil()

            # driver.delete_all_cookies()
        self.driver.quit()


ini = instagramInfo()
ini.login()
