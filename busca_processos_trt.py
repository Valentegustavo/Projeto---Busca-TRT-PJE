from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

# === CONFIGURAÇÕES GERAIS ===
URL_TRIBUNAL = "https://www.trt1.jus.br"
PJE_LINK = "https://pje.trt1.jus.br/primeirograu/"

# Termos de busca
ADVOGADO_NOME = "Fulano de Tal"
ASSUNTO_PROCESSO = "dano moral por transporte de valores"

def iniciar_driver():
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=chrome_options)
    return driver

def acessar_pje(driver):
    print("Acessando site do TRT1...")
    driver.get(URL_TRIBUNAL)
    time.sleep(2)
    print("Redirecionando para o PJE...")
    driver.get(PJE_LINK)
    time.sleep(5)

def buscar_processos(driver, advogado=None, assunto=None):
    print("Iniciando busca de processos...")
    try:
        consulta_link = driver.find_element(By.LINK_TEXT, "Consulta Pública")
        consulta_link.click()
        time.sleep(4)
    except Exception as e:
        print("Erro ao encontrar a Consulta Pública:", e)
        return

    if advogado:
        try:
            campo_advogado = driver.find_element(By.ID, "fAdvogado")
            campo_advogado.send_keys(advogado)
        except:
            print("Campo de advogado não encontrado.")

    if assunto:
        try:
            campo_assunto = driver.find_element(By.ID, "fAssunto")
            campo_assunto.send_keys(assunto)
        except:
            print("Campo de assunto não encontrado.")

    try:
        botao_buscar = driver.find_element(By.XPATH, '//button[contains(text(), "Pesquisar")]')
        botao_buscar.click()
        time.sleep(5)
    except:
        print("Botão de busca não encontrado.")

    extrair_resultados(driver)

def extrair_resultados(driver):
    print("Extraindo resultados...")
    try:
        resultados = driver.find_elements(By.CSS_SELECTOR, ".some-result-class")
        for resultado in resultados:
            print(resultado.text)
    except:
        print("Não foi possível extrair os resultados. Verifique os seletores.")

if __name__ == "__main__":
    driver = iniciar_driver()
    try:
        acessar_pje(driver)
        buscar_processos(driver, advogado=ADVOGADO_NOME, assunto=ASSUNTO_PROCESSO)
    finally:
        print("Fechando navegador.")
        time.sleep(5)
        driver.quit()
