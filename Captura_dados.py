import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime

# Função para capturar o preço de um produto
def capturar_preco(link, selector):
    headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0",
    "Accept-Language": "en-US,en;q=0.5",
    "Referer": "https://www.google.com/"
    }
    response = requests.get(link, headers=headers)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        try:
            preco = soup.select_one(selector).text.strip()  # Usar o seletor CSS
        except AttributeError:
            preco = 'N/A'
    else:
        preco = 'N/A'
    
    return preco

# Lista de links dos produtos e seus respectivos seletores CSS para os preços
produtos = {
    "iPhone 14": {
        "link": 'https://www.amazon.com.br/Apple-iPhone-14-256-GB/dp/B0C8ZK46JW/ref=sr_1_5?__mk_pt_BR=%C3%85M%C3%85%C5%BD%C3%95%C3%91&crid=2G4V4T00JD7GV&dib=eyJ2IjoiMSJ9.WhA_MhcQJQAVXpwJL91lbJ6eIgc6KA53Ble7NF7uCTyOimSdID1GNrpeQS87vRJR8S_qM50USyPiWsTzR4eHwe37yZpeY6amQHbeOnXaTdn-UVUuhq_T7_D1H5LJ-y32pjaSoaFKh_ZBHFDqIsA8ihUYw_h_ZlNB_RspeInHuyzN7eENDoR5WbNa0Nl0krAYZdtY9iJHigc5TF_9hinSSWoDT8r-2AKwE-5sneGXHsCK2zaWVd-Y0QIh3hR9qJoIbZZJGAPJxDCf-WXmG7-_WjDpP8ShuFrkTyVBe-0Mn1k.TTXjA0twIgCzVXdXfpOnifbl3JIurNe4-XWkQwJ0d5o&dib_tag=se&keywords=Apple+iPhone+14+%28256+GB%29+%E2%80%93+Amarelo&qid=1729451382&sprefix=apple+iphone+14+256+gb+amarelo%2Caps%2C424&sr=8-5&ufe=app_do%3Aamzn1.fos.95de73c3-5dda-43a7-bd1f-63af03b14751',
        "selector": ".a-price-whole"  # Ajuste o seletor CSS conforme necessário
    },
    "Smart TV LG 65\"": {
        "link": 'https://www.amazon.com.br/LG-55QNED80T-Processador-Chromecast-integrado/dp/B0D4VKD19F/ref=sr_1_1_sspa?__mk_pt_BR=%C3%85M%C3%85%C5%BD%C3%95%C3%91&crid=123E8YUV2R36S&dib=eyJ2IjoiMSJ9.v-3A_Kr-OPmL-kLw9fZNwWNNw2eWIkoGnIMuKJXy5lPtD1bTZEYcpNlqyh2EVsYbANj1czhbbwfMzTA_QlRHI5Uf2Jof8_t-8_rFMJMdSetCfLt8PSdjfA3XYIuvoI62ma_1pPTYtCMuasp-kYOaLUc1sXru0GmA037rxrW3Dp9A0XWNG-0I0b5RGuxVWr-7CQXYdLdoCaMOfW4QArdszimsABfLckNvZvdRT3iaA2sg_G5qkFAtWK7ZY2AUUeAAIN2Hqhg33pzUdW5dVUBTWVpp_c2DPH7lb_LOHwkimGg.X-dNOIQZAzqeuvip_YAPPUuuNwbEfB4qm8IC-s1Uqlw',
        "selector": ".a-price-whole"  # Ajuste o seletor CSS conforme necessário
    },
    "PlayStation 5 Slim": {
        "link": 'https://www.amazon.com.br/PlayStation%C2%AE5-Slim-Edi%C3%A7%C3%A3o-Digital-Jogos/dp/B0CYJBWGH5',
        "selector": ".a-price-whole"  # Ajuste o seletor CSS conforme necessário
    },
    "Notebook Dell": {
        "link": 'https://www.amazon.com.br/Notebook-Dell-Inspiron-I15-I120K-A25P-Gera%C3%A7%C3%A3o/dp/B0DCKWYRQ6/ref=sr_1_5?dib=eyJ2IjoiMSJ9.YMItyqzctAvLDWmmaYdAYWnksYgwUS5iaw4fz9tNHBKmtiqmGbLHxmcO_LftNaiXP9CFzXel6DYSHhjFnrAkXJNoqprL1q8KZ5SimlFgW95-B8o7El49fk00EgUN8E5FzUA0ORd1i8c2ZQsfjUUk241hhjeuLANJLTT_S6tByHy72MDU3aTxu96R7wP4TAO_MH_X0C4ULuQOESpAdTnT6kePHcO_tnQ4B7axbOw27lZS019Cqwh9gqMgNIGbjx2zvL1yB2TXLwjO1pknWOkcGd_n0mWv5NDqnYxGyTOnwsY',
        "selector": ".a-price-whole"  # Ajuste o seletor CSS conforme necessário
    }
}

# Criar ou abrir o arquivo CSV
csv_file = 'precos_produtos.csv'

# Capturar a data de hoje
data_atual = datetime.now().strftime("%Y-%m-%d")

# Abrir o arquivo CSV para escrita (modo append)
with open(csv_file, mode='a', newline='', encoding='utf-8') as file:
    writer = csv.writer(file, delimiter=';')
    
    # Verificar se o arquivo está vazio, se sim, adicionar o cabeçalho
    if file.tell() == 0:
        # Cabeçalho com os nomes dos produtos
        header = ['DATA'] + list(produtos.keys())
        writer.writerow(header)
    
    # Capturar os preços de cada produto
    linha = [data_atual]  # Iniciar com a data
    for produto, info in produtos.items():
        preco = capturar_preco(info["link"], info["selector"])
        linha.append(preco)
    
    # Escrever a linha com os preços
    writer.writerow(linha)

print("Dados salvos no arquivo CSV com sucesso!")
