from selenium import webdriver
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager

selectors = {
    'name': 'header h1',
    'num_posts': 'header ul li:nth-child(1) span',
    'num_followers': 'header ul li:nth-child(2) span',
    'num_following': 'header ul li:nth-child(3) span',
    'verificado': '//*[@id="react-root"]/section/main/div/header/section/div[1]/div[1]/span',

}

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('headless')
driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
# driver = webdriver.Chrome(ChromeDriverManager().install())
usernames = ['anitta', 'virginia', 'pecararaplanaltina']
for username in usernames:

    driver.get(f'https://www.instagram.com/{username}')
    print(f'Capturando dados do perfil - {username}')

    try:
        status = driver.find_element_by_xpath(selectors['verificado']).text
    except:
        status = 'NÃO VERIFICADO'
    # print(status)

    #     PEGAR NOME
    name_el = driver.find_element_by_css_selector(selectors['name']).text
    # print(name_el)

    #     PEGAR NÚMERO DE POSTS
    num_posts = driver.find_element_by_css_selector(selectors['num_posts']).text.replace(',', '')
    # print(num_posts)

    #     PEGAR NÚMERO DE SEGUIDORES
    num_followers = driver.find_element_by_css_selector(selectors['num_followers']).get_attribute('title')
    # print(num_followers)

    #     PEGAR NÚMERO DE SEGUIDOS
    num_following = driver.find_element_by_css_selector(selectors['num_following']).text.replace(',', '')
    # print(num_following)

    # CRIAÇÃO DE DATAFRAME
    d = {'Nome': name_el, 'Quantidade Posts': num_posts,
     'Quantidade Seguidores': num_followers,
     'Quantidade Seguindo': num_following,
     'Verificado': status}
    dat = pd.DataFrame(data=d, index=[0])
    dat.to_csv(f"{name_el}.csv")

driver.quit()
