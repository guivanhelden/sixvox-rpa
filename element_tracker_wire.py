"""
Element Tracker para o Sistema SixVox usando Selenium Wire
Este script abre um navegador automatizado, faz login no sistema SixVox
e rastreia elementos enquanto o usuário navega pelo sistema.
"""
import os
import time
import json
from datetime import datetime
from seleniumwire import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Configurações
URL = "https://vhseguro.sixvox.com.br"
EMAIL = "marketing@vhseguros.com.br"
PASSWORD = "M@aite2017"

# Diretório para salvar os dados rastreados
ELEMENTS_DIR = "elementos_rastreados"
os.makedirs(ELEMENTS_DIR, exist_ok=True)

class ElementTracker:
    def __init__(self):
        self.driver = None
        self.tracked_elements = []
        self.current_page = ""
        
    def setup_driver(self):
        """Configura o driver do Selenium Wire"""
        chrome_options = Options()
        chrome_options.add_argument("--start-maximized")
        # Desabilitar o modo headless para permitir navegação manual
        # chrome_options.add_argument("--headless")
        
        # Configuração específica para o Selenium Wire
        seleniumwire_options = {
            'disable_encoding': True,  # Desabilitar codificação para melhor performance
        }
        
        self.driver = webdriver.Chrome(
            options=chrome_options,
            seleniumwire_options=seleniumwire_options
        )
        
    def login(self):
        """Realiza login no sistema"""
        try:
            self.driver.get(URL)
            print(f"Acessando {URL}...")
            
            # Aguardar página de login carregar
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "email"))
            )
            
            # Preencher credenciais
            self.driver.find_element(By.ID, "email").send_keys(EMAIL)
            self.driver.find_element(By.ID, "password").send_keys(PASSWORD)
            
            # Clicar no botão de login
            self.driver.find_element(By.XPATH, "//button[@type='submit']").click()
            
            # Aguardar login ser concluído
            WebDriverWait(self.driver, 10).until(
                EC.url_contains("dashboard")
            )
            
            print("Login realizado com sucesso!")
            return True
        except Exception as e:
            print(f"Erro ao fazer login: {str(e)}")
            return False
    
    def track_elements(self):
        """Rastreia elementos da página atual"""
        try:
            # Obter URL atual
            current_url = self.driver.current_url
            page_title = self.driver.title
            
            # Se mudou de página, atualizar
            if current_url != self.current_page:
                self.current_page = current_url
                print(f"\nRastreando elementos da página: {page_title} ({current_url})")
            
            # Rastrear elementos interativos
            elements_data = {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "url": current_url,
                "title": page_title,
                "elements": []
            }
            
            # Rastrear botões
            buttons = self.driver.find_elements(By.TAG_NAME, "button")
            for button in buttons:
                try:
                    element_data = {
                        "type": "button",
                        "text": button.text.strip(),
                        "id": button.get_attribute("id"),
                        "name": button.get_attribute("name"),
                        "class": button.get_attribute("class"),
                        "xpath": self.get_xpath(button)
                    }
                    elements_data["elements"].append(element_data)
                except:
                    pass
            
            # Rastrear inputs
            inputs = self.driver.find_elements(By.TAG_NAME, "input")
            for input_elem in inputs:
                try:
                    element_data = {
                        "type": "input",
                        "input_type": input_elem.get_attribute("type"),
                        "id": input_elem.get_attribute("id"),
                        "name": input_elem.get_attribute("name"),
                        "placeholder": input_elem.get_attribute("placeholder"),
                        "class": input_elem.get_attribute("class"),
                        "xpath": self.get_xpath(input_elem)
                    }
                    elements_data["elements"].append(element_data)
                except:
                    pass
            
            # Rastrear selects
            selects = self.driver.find_elements(By.TAG_NAME, "select")
            for select in selects:
                try:
                    element_data = {
                        "type": "select",
                        "id": select.get_attribute("id"),
                        "name": select.get_attribute("name"),
                        "class": select.get_attribute("class"),
                        "xpath": self.get_xpath(select)
                    }
                    elements_data["elements"].append(element_data)
                except:
                    pass
            
            # Rastrear links
            links = self.driver.find_elements(By.TAG_NAME, "a")
            for link in links:
                try:
                    element_data = {
                        "type": "link",
                        "text": link.text.strip(),
                        "href": link.get_attribute("href"),
                        "id": link.get_attribute("id"),
                        "class": link.get_attribute("class"),
                        "xpath": self.get_xpath(link)
                    }
                    elements_data["elements"].append(element_data)
                except:
                    pass
            
            # Rastrear labels (podem ser úteis para identificar campos)
            labels = self.driver.find_elements(By.TAG_NAME, "label")
            for label in labels:
                try:
                    element_data = {
                        "type": "label",
                        "text": label.text.strip(),
                        "for": label.get_attribute("for"),
                        "id": label.get_attribute("id"),
                        "class": label.get_attribute("class"),
                        "xpath": self.get_xpath(label)
                    }
                    elements_data["elements"].append(element_data)
                except:
                    pass
            
            # Adicionar à lista de elementos rastreados
            self.tracked_elements.append(elements_data)
            
            # Salvar elementos rastreados
            self.save_tracked_elements()
            
            print(f"Rastreados {len(elements_data['elements'])} elementos")
            
        except Exception as e:
            print(f"Erro ao rastrear elementos: {str(e)}")
    
    def get_xpath(self, element):
        """Tenta obter o XPath do elemento"""
        try:
            return self.driver.execute_script("""
                function getElementXPath(element) {
                    if (element && element.id) {
                        return '//*[@id="' + element.id + '"]';
                    }
                    
                    var paths = [];
                    for (; element && element.nodeType == 1; element = element.parentNode) {
                        var index = 0;
                        for (var sibling = element.previousSibling; sibling; sibling = sibling.previousSibling) {
                            if (sibling.nodeType == 1 && sibling.tagName == element.tagName) {
                                index++;
                            }
                        }
                        var tagName = element.tagName.toLowerCase();
                        var pathIndex = (index ? "[" + (index+1) + "]" : "");
                        paths.unshift(tagName + pathIndex);
                    }
                    return "/" + paths.join("/");
                }
                return getElementXPath(arguments[0]);
            """, element)
        except:
            return ""
    
    def save_tracked_elements(self):
        """Salva os elementos rastreados em um arquivo JSON"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{ELEMENTS_DIR}/elements_{timestamp}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.tracked_elements, f, ensure_ascii=False, indent=2)
    
    def run(self):
        """Executa o rastreador de elementos"""
        try:
            self.setup_driver()
            if not self.login():
                return
            
            print("\nNavegue pelo sistema normalmente. O rastreador está ativo.")
            print("Pressione Ctrl+C para encerrar o rastreamento.\n")
            
            # Loop principal para rastrear elementos enquanto o usuário navega
            while True:
                self.track_elements()
                time.sleep(2)  # Intervalo entre rastreamentos
                
        except KeyboardInterrupt:
            print("\nRastreamento interrompido pelo usuário.")
        except Exception as e:
            print(f"\nErro durante o rastreamento: {str(e)}")
        finally:
            if self.driver:
                self.driver.quit()
            print("\nRastreamento finalizado. Elementos salvos em:", ELEMENTS_DIR)

if __name__ == "__main__":
    tracker = ElementTracker()
    tracker.run()
