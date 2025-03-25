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
PASSWORD = "M@ite2017"  # Corrigido para corresponder ao arquivo playwright

# Diretório para salvar os dados rastreados
ELEMENTS_DIR = "elementos_rastreados"
os.makedirs(ELEMENTS_DIR, exist_ok=True)

class ElementTracker:
    def __init__(self):
        self.driver = None
        self.tracked_elements = []
        self.current_page = ""
        self.interacted_elements = set()  # Conjunto para armazenar elementos com interação
        
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
        
        # Adicionar scripts para monitorar interações do usuário
        self.add_interaction_monitoring()
        
    def add_interaction_monitoring(self):
        """Adiciona scripts para monitorar interações do usuário com elementos"""
        # Script para monitorar cliques e interações
        interaction_script = """
        (function() {
            // Armazenar elementos com os quais o usuário interagiu
            window.interactedElements = new Set();
            
            // Função para adicionar elemento à lista de interações
            function addInteraction(element) {
                window.interactedElements.add(element);
            }
            
            // Monitorar cliques
            document.addEventListener('click', function(e) {
                addInteraction(e.target);
            }, true);
            
            // Monitorar inputs
            document.addEventListener('input', function(e) {
                addInteraction(e.target);
            }, true);
            
            // Monitorar mudanças em selects
            document.addEventListener('change', function(e) {
                addInteraction(e.target);
            }, true);
            
            // Monitorar foco em elementos
            document.addEventListener('focus', function(e) {
                addInteraction(e.target);
            }, true);
            
            // Monitorar submissões de formulários
            document.addEventListener('submit', function(e) {
                addInteraction(e.target);
                // Também adicionar os elementos do formulário
                if (e.target.tagName === 'FORM') {
                    Array.from(e.target.elements).forEach(addInteraction);
                }
            }, true);
        })();
        """
        
        # Executar o script após carregar cada página
        self.driver.execute_script(interaction_script)

    def login(self):
        """Realiza login no sistema"""
        try:
            self.driver.get(URL)
            print(f"Acessando {URL}...")
            
            # Aguardar página de login carregar com os mesmos seletores do playwright
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//input[@id='email']"))
            )
            
            # Preencher credenciais usando os mesmos seletores do playwright
            self.driver.find_element(By.XPATH, "//input[@id='email']").send_keys(EMAIL)
            self.driver.find_element(By.XPATH, "//input[@id='xenha']").send_keys(PASSWORD)
            
            # Clicar no botão de login
            self.driver.find_element(By.XPATH, "//input[@id='enviar']").click()
            
            # Aguardar login ser concluído
            try:
                # Esperar que a página termine de carregar
                WebDriverWait(self.driver, 10).until(
                    lambda driver: driver.current_url != URL
                )
                print("Login realizado com sucesso!")
                return True
            except Exception as e:
                print(f"Aviso: {str(e)}")
                # Mesmo com erro, continuar se a página mudou
                if self.driver.current_url != URL:
                    print("Página mudou após tentativa de login, continuando...")
                    return True
                return False
        except Exception as e:
            print(f"Erro ao fazer login: {str(e)}")
            return False
    
    def track_elements(self):
        """Rastreia elementos com os quais o usuário interagiu na página atual"""
        try:
            # Obter URL atual
            current_url = self.driver.current_url
            page_title = self.driver.title
            
            # Se mudou de página, atualizar e reiniciar o monitoramento
            if current_url != self.current_page:
                self.current_page = current_url
                print(f"\nRastreando elementos da página: {page_title} ({current_url})")
                # Reiniciar o script de monitoramento na nova página
                self.add_interaction_monitoring()
            
            # Obter elementos com os quais o usuário interagiu
            interacted_elements_js = """
            return Array.from(window.interactedElements || new Set());
            """
            
            try:
                # Tentar obter os elementos interagidos
                interacted_elements = self.driver.execute_script(interacted_elements_js)
            except:
                # Se falhar, pode ser porque a página foi recarregada
                self.add_interaction_monitoring()
                interacted_elements = []
            
            if not interacted_elements:
                # Se não houver elementos interagidos, não fazer nada
                return
            
            # Rastrear elementos interativos
            elements_data = {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "url": current_url,
                "title": page_title,
                "elements": []
            }
            
            # Processar cada elemento interagido
            for i, element in enumerate(interacted_elements):
                try:
                    # Obter informações do elemento
                    element_type = self.driver.execute_script("return arguments[0].tagName.toLowerCase();", element)
                    element_id = self.driver.execute_script("return arguments[0].id;", element)
                    element_name = self.driver.execute_script("return arguments[0].name;", element)
                    element_class = self.driver.execute_script("return arguments[0].className;", element)
                    element_text = self.driver.execute_script("return arguments[0].textContent;", element)
                    
                    # Criar dados do elemento
                    element_data = {
                        "type": element_type,
                        "text": element_text.strip() if element_text else "",
                        "id": element_id,
                        "name": element_name,
                        "class": element_class,
                        "xpath": self.get_xpath(element)
                    }
                    
                    # Adicionar atributos específicos com base no tipo
                    if element_type == "input":
                        element_data["input_type"] = self.driver.execute_script("return arguments[0].type;", element)
                        element_data["placeholder"] = self.driver.execute_script("return arguments[0].placeholder;", element)
                    elif element_type == "a":
                        element_data["href"] = self.driver.execute_script("return arguments[0].href;", element)
                    elif element_type == "label":
                        element_data["for"] = self.driver.execute_script("return arguments[0].htmlFor;", element)
                    
                    # Adicionar à lista de elementos rastreados
                    elements_data["elements"].append(element_data)
                except Exception as e:
                    print(f"Erro ao processar elemento {i}: {str(e)}")
            
            # Limpar os elementos interagidos no JavaScript
            self.driver.execute_script("window.interactedElements = new Set();")
            
            # Adicionar à lista de elementos rastreados
            if elements_data["elements"]:
                self.tracked_elements.append(elements_data)
                
                # Salvar elementos rastreados
                self.save_tracked_elements()
                
                print(f"Rastreados {len(elements_data['elements'])} elementos interagidos")
            
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
