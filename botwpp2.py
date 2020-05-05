from selenium import webdriver
import os
from time import sleep


class zapbot:
    dir_path = os.getcwd()
    chromedriver = os.path.join(dir_path, "chromedriver.exe")
    profile = os.path.join(dir_path, "profile", "wpp")

    def __init__(self):
        self.options = webdriver.ChromeOptions()
        self.options.add_argument(
            r"user-data-dir={}".format(self.profile))
        self.driver = webdriver.Chrome(
            self.chromedriver, chrome_options=self.options)
        self.driver.get("https://web.whatsapp.com/")
        self.driver.implicitly_wait(15)

    def lerUltimaMsg(self):
        """ Ler ultima mensagem da conversa aberta """
        try:
            post = self.driver.find_elements_by_class_name("_3_7SH")
            ultimo = len(post) - 1
            # O texto da ultima mensagem
            texto = post[ultimo].find_element_by_css_selector(
                "span.selectable-text").text
            return texto
        except Exception as e:
            print("Erro ao ler msg, tentando novamente!", e)

    def enviarMsg(self, msg):
        """ Envia uma mensagem para conversa aberta """
        try:
            sleep(2)
            self.caixa_de_mensagem = self.driver.find_element_by_class_name("_1Plpp")
            self.caixa_de_mensagem.send_keys(msg)
            sleep(1)
            self.botao_enviar = self.driver.find_element_by_xpath("//span[@data-icon='send']")
            self.botao_enviar.click()
            sleep(2)
        except Exception as e:
            print("Erro ao enviar msg", e)

    def enviarMedia(self, fileToSend):
        """ Enviar media """
        try:
            self.driver.find_element_by_css_selector("span[data-icon='clip']").click()
            attach = self.driver.find_element_by_css_selector("input[type='file']")
            attach.send_keys(fileToSend)
            sleep(3)
            send = self.driver.find_element_by_xpath("//div[contains(@class, 'yavlE')]")
            send.click()
        except Exception as e:
            print("Erro ao enviar media", e)

    def abrirConversa(self, contato):
        """ Abre a conversa com um contato especifico """
        try:
            #self.caixa_de_pesquisa = self.driver.find_element_by_class_name("_2S1VP ")
            #self.caixa_de_pesquisa.send_keys(contato)
            sleep(5)
            self.contato = self.driver.find_element_by_xpath(f"//span[@title='{contato}']")
            #self.contato = self.driver.find_element_by_xpath("//span[@title = '{}']".format(contato))
            self.contato.click()
        except Exception as e:
            raise e


bot = zapbot()
bot.abrirConversa("Conversa 1")
bot.enviarMsg("Olá!")

msg = ""
while msg != "sair":
    sleep(1)
    msg = bot.lerUltimaMsg()
    if msg == "Oi":
        bot.enviarMsg("Oi")
    elif msg == "Tudo bem?":
        bot.enviarMsg("""Sim
        E você?""")
    elif msg == "sair":
        bot.enviarMsg("Tchau")