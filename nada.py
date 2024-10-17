#Blibliotecas usadas, Selenium para criar , datetime e csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import csv
from datetime import datetime
import time
import os

# Função para inicializar o navegador com Selenium
def initialize_driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Executar o navegador em modo headless (sem abrir a janela)
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver

# Função para capturar o preço de uma página
def get_price(driver, url):
    driver.get(url)
    time.sleep(3)  # Esperar a página carregar completamente (ajuste o tempo se necessário)

    if "fastshop" in url:
        try:
            product = driver.find_element(By.TAG_NAME, 'h1').text.strip()
            price = driver.find_element(By.CLASS_NAME, 'sales-price').text.strip()
        except:
            product, price = "Produto não encontrado", "Preço não disponível"

    elif "casasbahia" in url:
        try:
            product = driver.find_element(By.CLASS_NAME, 'product-name-default').text.strip()
            price = driver.find_element(By.CLASS_NAME, 'sales-price').text.strip()
        except:
            product, price = "Produto não encontrado", "Preço não disponível"

    elif "amazon" in url:
        try:
            product = driver.find_element(By.ID, 'productTitle').text.strip()
            price = driver.find_element(By.CLASS_NAME, 'a-price-whole').text.strip()
        except:
            product, price = "Produto não encontrado", "Preço não disponível"

    elif "americanas" in url:
        try:
            product = driver.find_element(By.TAG_NAME, 'h1').text.strip()
            price = driver.find_element(By.CLASS_NAME, 'price__SalesPrice-ej7lo7-2').text.strip()
        except:
            product, price = "Produto não encontrado", "Preço não disponível"

    else:
        product, price = "URL não reconhecida", "N/A"

    return product, price

# Função para salvar os dados em um arquivo CSV
def save_to_csv(data, filename='precos_produtos.csv'):
    file_exists = os.path.isfile(filename)

    with open(filename, mode='a', newline='', encoding='utf-8') as file: #abre o arquivo e salva
        writer = csv.writer(file, delimiter=";") #separa por ; para cada elemento ficar em uma coluna

        # Escrever o cabeçalho se o arquivo estiver sendo criado pela primeira vez
        if not file_exists:
            writer.writerow(['DATA', 'PRODUTO', 'PREÇO'])

        # Escrever os dados
        writer.writerow(data)

# Links dos produtos
urls = [
    'https://www.amazon.com.br/Apple-iPhone-14-256-GB/dp/B0C8ZK46JW/ref=sr_1_10?dib=eyJ2IjoiMSJ9.dXqv5B_lgx4NpYYgysPWwK-MDv2X47JQIsKgI5bX0AZpfzGt8Cm_7UUJKWQ9KlnC9rXRFqvAUFOewQjzOk5VAUWsnnDAvwrvvso1bBu2qV70wzOG4ufhHTOLXNTaNL9z-zW1WI9MdQv8ng0QDbqx4bE9aH_0-0WGMAsPw_Hy-TCEEhQdioU9a7sOsvjEeOHP9GGLXrx8D3K2yCBq2OP7h1D1JbjOYLUfv29Sx9PYCJsE1kcSJhrYU8SROy4su17tLDokxLAHo7Mb07lyQ5cEqjNyXkAzXYSO9WizFU0PEeU.LVG1X7GbwzyTTsp4Y1tVYWifSN9Gl4dDYdXAuXTMLZ8&dib_tag=se&keywords=iPhone+14+Pro&qid=1729180111&sr=8-10&ufe=app_do%3Aamzn1.fos.95de73c3-5dda-43a7-bd1f-63af03b14751',
    'https://www.amazon.com.br/LG-55QNED80T-Processador-Chromecast-integrado/dp/B0D4VKD19F/ref=sr_1_1_sspa?__mk_pt_BR=%C3%85M%C3%85%C5%BD%C3%95%C3%91&crid=123E8YUV2R36S&dib=eyJ2IjoiMSJ9.v-3A_Kr-OPmL-kLw9fZNwWNNw2eWIkoGnIMuKJXy5lPtD1bTZEYcpNlqyh2EVsYbANj1czhbbwfMzTA_QlRHI5Uf2Jof8_t-8_rFMJMdSetCfLt8PSdjfA3XYIuvoI62ma_1pPTYtCMuasp-kYOaLUc1sXru0GmA037rxrW3Dp9A0XWNG-0I0b5RGuxVWr-7CQXYdLdoCaMOfW4QArdszimsABfLckNvZvdRT3iaA2sg_G5qkFAtWK7ZY2AUUeAAIN2Hqhg33pzUdW5dVUBTWVpp_c2DPH7lb_LOHwkimGg.X-dNOIQZAzqeuvip_YAPPUuuNwbEfB4qm8IC-s1Uqlw&dib_tag=se&keywords=Smart+TV+LG+65%27%27+4K&qid=1729180142&sprefix=smart+tv+lg+65%27%27+4k+%2Caps%2C211&sr=8-1-spons&ufe=app_do%3Aamzn1.fos.95de73c3-5dda-43a7-bd1f-63af03b14751&sp_csd=d2lkZ2V0TmFtZT1zcF9hdGY&psc=1',
    'https://www.amazon.com.br/PlayStation%C2%AE5-Slim-Edi%C3%A7%C3%A3o-Digital-Jogos/dp/B0CYJBWGH5',
    'hhttps://www.amazon.com.br/Notebook-Dell-Inspiron-I15-I120K-A25P-Gera%C3%A7%C3%A3o/dp/B0DCKWYRQ6/ref=sr_1_5?__mk_pt_BR=%C3%85M%C3%85%C5%BD%C3%95%C3%91&crid=32R3O7WNXIL9I&dib=eyJ2IjoiMSJ9.YMItyqzctAvLDWmmaYdAYWnksYgwUS5iaw4fz9tNHBKmtiqmGbLHxmcO_LftNaiXP9CFzXel6DYSHhjFnrAkXJNoqprL1q8KZ5SimlFgW95-B8o7El49fk00EgUN8E5FzUA0ORd1i8c2ZQsfjUUk26_Tr04AIFOxmSZW4wNtOazJ4CTZFcFIqrKm-4TIGm7FMH_X0C4ULuQOESpAdTnT6kePHcO_tnQ4B7axbOw27lasK9xyfJcNOMbRMp80EZ8rMh6GMJlMa6mPBWN7_M4vQN_n0mWv5NDqnYxGyTOnwsY.APQ5hzEv4tap0l2r44IwaKwMpeQBrgzgy6XgjVO8b4A&dib_tag=se&keywords=Notebook+Dell+Inspiron+15&qid=1729180166&sprefix=notebook+dell+inspiron+15%2Caps%2C204&sr=8-5&ufe=app_do%3Aamzn1.fos.25548f35-0de7-44b3-b28e-0f56f3f96147'
]

# Inicializa o driver do Selenium
driver = initialize_driver()

# Captura dos dados
for url in urls:
    product, price = get_price(driver, url)
    if product and price:
        current_date = datetime.now().strftime('%Y-%m-%d')
        save_to_csv([current_date, product, price])

driver.quit()

print("Dados capturados e salvos com sucesso!")
