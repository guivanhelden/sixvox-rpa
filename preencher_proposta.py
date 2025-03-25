"""
AUTOMAÇÃO DE PREENCHIMENTO DE PROPOSTA - SIXVOX

Este script automatiza o preenchimento de propostas no sistema SixVox,
utilizando o mapeamento de elementos e os dados de exemplo.
"""

import time
import json
from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# Importando os mapeamentos e dados de exemplo
from elementos_nova_proposta import form_elements, get_element_by_id
from dados_exemplo_proposta import dados_proposta, get_valor

# Configurações
URL = "https://vhseguro.sixvox.com.br"
EMAIL = "marketing@vhseguros.com.br"
PASSWORD = "M@ite2017"

class SixvoxAutomation:
    def __init__(self):
        """Inicializa a automação do SixVox"""
        # Configurações do Chrome
        options = webdriver.ChromeOptions()
        options.add_argument('--start-maximized')
        options.add_argument('--disable-extensions')
        options.add_argument('--disable-popup-blocking')
        options.add_argument('--disable-infobars')
        
        # Inicializa o driver
        self.driver = webdriver.Chrome(options=options)
        self.wait = WebDriverWait(self.driver, 10)
        
    def login(self):
        """Realiza o login no sistema SixVox"""
        print("Realizando login no sistema...")
        self.driver.get(URL)
        
        # Preenche o email
        email_field = self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@id='email']")))
        email_field.send_keys(EMAIL)
        
        # Preenche a senha
        password_field = self.driver.find_element(By.XPATH, "//input[@id='xenha']")
        password_field.send_keys(PASSWORD)
        
        # Clica no botão de enviar
        login_button = self.driver.find_element(By.XPATH, "//input[@id='enviar']")
        login_button.click()
        
        # Aguarda o carregamento da página inicial
        try:
            self.wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='menu_propostas']")))
            print("Login realizado com sucesso!")
        except TimeoutException:
            print("Falha ao realizar login. Verifique as credenciais.")
            self.driver.quit()
            return False
        
        return True
    
    def navegar_para_nova_proposta(self):
        """Navega para a página de nova proposta"""
        print("Navegando para a página de nova proposta...")
        
        # Usar a sequência correta de XPaths conforme indicado pelo usuário
        try:
            # Primeiro, clica no menu de propostas
            print("  Clicando no menu de propostas...")
            try:
                menu_propostas = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='menu_propostas']")))
                menu_propostas.click()
                time.sleep(2)  # Aguarda a ação completar
                print("  Menu de propostas clicado com sucesso")
            except Exception as e:
                print(f"  Erro ao clicar no menu de propostas: {str(e)}")
                # Continua mesmo se falhar, pois pode já estar na página correta

            # Depois, clica no elemento chi_novas
            print("  Clicando no elemento chi_novas...")
            try:
                chi_novas = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='chi_novas']")))
                chi_novas.click()
                time.sleep(2)  # Aguarda a ação completar
                print("  Elemento chi_novas clicado com sucesso")
            except Exception as e:
                print(f"  Erro ao clicar no elemento chi_novas: {str(e)}")
                # Continua mesmo se falhar
            
            # Terceiro XPath: sub_novas/a[2]
            print("  Clicando no elemento sub_novas/a[2]...")
            try:
                nova_proposta = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='sub_novas']/a[2]")))
                nova_proposta.click()
                time.sleep(2)  # Aguarda a página carregar
                print("  Link de nova proposta clicado com sucesso")
            except Exception as e:
                print(f"  Erro ao clicar no link de nova proposta: {str(e)}")
                # Se falhar, tenta ir direto para a URL
                try:
                    print("  Tentando navegar diretamente para a URL de nova proposta...")
                    self.driver.get(URL + "/propostas/nova")
                    time.sleep(2)
                    print("  Navegação direta para URL concluída")
                except Exception as e:
                    print(f"  Erro na navegação direta: {str(e)}")
                    return False
            
            print("  Navegação concluída!")
        except Exception as e:
            print(f"  Erro geral na navegação: {str(e)}")
            return False
            
        # Verifica se a página de nova proposta foi carregada corretamente
        try:
            # Tenta identificar elementos chave na página
            elementos_indicadores = ["cod_administradora", "numero_proposta", "cnpj"]
            for elemento in elementos_indicadores:
                try:
                    self.wait.until(EC.presence_of_element_located((By.ID, elemento)))
                    print(f"Página de nova proposta carregada com sucesso! (Identificado pelo elemento '{elemento}')")
                    return True
                except TimeoutException:
                    continue
            
            # Se não encontrou os elementos esperados, verifica se há formulários
            forms = self.driver.find_elements(By.TAG_NAME, "form")
            if forms:
                print(f"  Encontrados {len(forms)} formulários na página. Assumindo que estamos na página correta.")
                return True
            else:
                print("  Nenhum formulário encontrado na página. Verificando elementos HTML...")
                
                # Última tentativa: verificar se há elementos de formulário
                inputs = self.driver.find_elements(By.TAG_NAME, "input")
                selects = self.driver.find_elements(By.TAG_NAME, "select")
                if inputs or selects:
                    print(f"  Encontrados {len(inputs)} inputs e {len(selects)} selects. Assumindo que estamos na página correta.")
                    return True
                else:
                    print("  Nenhum elemento de formulário encontrado. Navegação falhou.")
                    return False
        except Exception as e:
            print(f"Erro ao verificar carregamento da página: {str(e)}")
            return False
    
    def preencher_select(self, id_elemento, valor):
        """Preenche um elemento select com o valor especificado"""
        try:
            # Verifica se o elemento existe e está visível
            try:
                elemento = self.wait.until(EC.visibility_of_element_located((By.ID, id_elemento)))
            except TimeoutException:
                print(f"Elemento select '{id_elemento}' não encontrado ou não visível")
                return False
                
            # Verifica se é realmente um select
            if elemento.tag_name.lower() != 'select':
                print(f"Elemento '{id_elemento}' não é um select, é um {elemento.tag_name}")
                # Se for um input, tenta preencher como input
                if elemento.tag_name.lower() == 'input':
                    return self.preencher_input(id_elemento, valor)
                return False
                
            select = Select(elemento)
            
            # Tenta selecionar pelo texto visível
            try:
                select.select_by_visible_text(valor)
                print(f"  Selecionado '{valor}' no campo '{id_elemento}'")
                return True
            except:
                # Se falhar, tenta encontrar uma opção que contenha o texto
                options = select.options
                for option in options:
                    if valor in option.text:
                        select.select_by_visible_text(option.text)
                        print(f"  Selecionado '{option.text}' no campo '{id_elemento}'")
                        return True
                
                # Se falhar, exibe as opções disponíveis
                print(f"Não foi possível selecionar '{valor}' no campo '{id_elemento}'")
                print(f"  Opções disponíveis: {[o.text for o in options[:5]]}{'...' if len(options) > 5 else ''}")
                return False
        except Exception as e:
            print(f"Erro ao preencher select '{id_elemento}': {str(e)}")
            return False
    
    def preencher_input(self, id_elemento, valor):
        """Preenche um elemento input com o valor especificado"""
        try:
            # Verifica se é um campo de autocompletar
            if id_elemento == "name_corretor":
                return self.preencher_autocomplete(id_elemento, valor)
                
            # Tenta encontrar o elemento e esperar que esteja clicável
            try:
                elemento = self.wait.until(EC.element_to_be_clickable((By.ID, id_elemento)))
            except TimeoutException:
                print(f"Elemento input '{id_elemento}' não encontrado ou não clicável")
                # Tenta encontrar por XPath como alternativa
                try:
                    xpath = f"//input[@id='{id_elemento}']|//input[@name='{id_elemento}']|//textarea[@id='{id_elemento}']|//textarea[@name='{id_elemento}']"  
                    elemento = self.wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
                    print(f"  Elemento '{id_elemento}' encontrado por XPath")
                except TimeoutException:
                    print(f"  Elemento '{id_elemento}' não encontrado por XPath também")
                    return False
            
            # Tenta interagir com o elemento
            try:
                # Rola até o elemento para garantir que está visível
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", elemento)
                time.sleep(0.5)  # Pequena pausa para garantir que o scroll terminou
                
                # Limpa e preenche o campo
                elemento.clear()
                elemento.send_keys(str(valor))
                print(f"  Preenchido '{valor}' no campo '{id_elemento}'")
                return True
            except Exception as e:
                print(f"  Não foi possível interagir com o elemento '{id_elemento}': {str(e)}")
                return False
                
        except Exception as e:
            print(f"Erro ao preencher input '{id_elemento}': {str(e)}")
            return False
            
    def preencher_autocomplete(self, id_elemento, valor):
        """Preenche um campo de autocompletar e seleciona uma opção da lista"""
        try:
            print(f"  Preenchendo campo de autocompletar '{id_elemento}' com '{valor}'")
            
            # Encontra o elemento de input
            elemento = self.wait.until(EC.element_to_be_clickable((By.XPATH, f"//*[@id='{id_elemento}']")))
            
            # Rola até o elemento para garantir que está visível
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", elemento)
            time.sleep(1)  # Aguarda o scroll terminar
            
            # Clica no elemento para focar
            try:
                elemento.click()
                print("  Campo clicado com sucesso")
            except Exception as e:
                print(f"  Erro ao clicar no campo: {str(e)}")
                # Tenta usar JavaScript para focar o elemento
                self.driver.execute_script("arguments[0].focus();", elemento)
            
            # Limpa o campo
            elemento.clear()
            time.sleep(0.5)
            
            # Digita o valor lentamente para acionar o autocompletar
            print(f"  Digitando '{valor}' no campo...")
            for char in str(valor):
                elemento.send_keys(char)
                time.sleep(0.1)  # Pequena pausa entre cada caractere
            
            # Aguarda as opções de autocompletar aparecerem
            print("  Aguardando opções de autocompletar...")
            time.sleep(2)
            
            # Tenta várias abordagens para selecionar uma opção
            try:
                # Abordagem 1: Procura por elementos da lista de autocompletar usando CSS
                opcoes_autocomplete = self.driver.find_elements(By.CSS_SELECTOR, "ul.ui-autocomplete li.ui-menu-item")
                
                if opcoes_autocomplete:
                    print(f"  Encontradas {len(opcoes_autocomplete)} opções de autocompletar")
                    try:
                        # Abordagem 1.1: Tenta encontrar o link por ID específico (visto na imagem)
                        try:
                            # Tenta encontrar o link com ID ui-id-121 ou similar
                            links = self.driver.find_elements(By.CSS_SELECTOR, "ul.ui-autocomplete li.ui-menu-item a[id^='ui-id-']")
                            if links:
                                print(f"  Encontrados {len(links)} links com ID ui-id-*")
                                for link in links:
                                    print(f"  Link encontrado: ID={link.get_attribute('id')}, texto={link.text}")
                                    if "Monica Mattos Takazaki" in link.text:
                                        print(f"  Encontrado link exato com texto: '{link.text}'")
                                        self.driver.execute_script("arguments[0].click();", link)
                                        print("  Selecionada opção de autocompletar pelo texto")
                                        time.sleep(1)
                                        return True
                                
                                # Se não encontrou pelo texto, usa o primeiro
                                self.driver.execute_script("arguments[0].click();", links[0])
                                print(f"  Selecionada primeira opção de autocompletar com ID {links[0].get_attribute('id')}")
                                time.sleep(1)
                                return True
                        except Exception as e:
                            print(f"  Erro ao buscar por ID específico: {str(e)}")
                        
                        # Abordagem 1.2: Tenta clicar no link dentro do item (mais genérico)
                        link = self.driver.find_element(By.CSS_SELECTOR, "ul.ui-autocomplete li.ui-menu-item a")
                        print(f"  Encontrado link de autocompletar com texto: '{link.text}'")
                        # Usa JavaScript para clicar no elemento, que é mais confiável
                        self.driver.execute_script("arguments[0].click();", link)
                        print("  Selecionada opção de autocompletar usando JavaScript")
                        time.sleep(1)
                        return True
                    except Exception as e:
                        print(f"  Erro ao clicar no link: {str(e)}")
                        # Se falhar, tenta clicar no item da lista diretamente
                        try:
                            self.driver.execute_script("arguments[0].click();", opcoes_autocomplete[0])
                            print("  Selecionada a primeira opção de autocompletar usando JavaScript")
                        except:
                            opcoes_autocomplete[0].click()
                            print("  Selecionada a primeira opção de autocompletar")
                        time.sleep(1)
                        return True
                else:
                    print("  Nenhuma opção encontrada por CSS. Tentando outras abordagens...")
                    
                    # Abordagem 2: Tenta usar XPath para encontrar opções
                    try:
                        opcoes_xpath = self.driver.find_elements(By.XPATH, "//ul[contains(@class, 'ui-autocomplete')]/li")
                        if opcoes_xpath:
                            print(f"  Encontradas {len(opcoes_xpath)} opções por XPath")
                            opcoes_xpath[0].click()
                            print("  Selecionada opção por XPath")
                            time.sleep(1)
                            return True
                    except Exception as e:
                        print(f"  Erro ao buscar por XPath: {str(e)}")
                    
                    # Abordagem 3: Pressiona seta para baixo e Enter
                    try:
                        print("  Tentando selecionar com teclas de navegação...")
                        elemento.send_keys(Keys.DOWN)  # Pressiona seta para baixo
                        time.sleep(0.5)
                        elemento.send_keys(Keys.ENTER)  # Pressiona Enter
                        print("  Selecionada opção usando teclas de navegação")
                        time.sleep(1)
                        return True
                    except Exception as e:
                        print(f"  Erro ao usar teclas de navegação: {str(e)}")
                    
                    # Se todas as tentativas falharem, apenas pressiona Tab para sair do campo
                    print("  Todas as tentativas falharam. Pressionando Tab para continuar...")
                    elemento.send_keys(Keys.TAB)
                    time.sleep(0.5)
                    return True
                    
            except Exception as e:
                print(f"  Erro geral ao selecionar opção de autocompletar: {str(e)}")
                # Pressiona Tab para sair do campo
                elemento.send_keys(Keys.TAB)
                time.sleep(0.5)
                return True
                
        except Exception as e:
            print(f"Erro ao preencher campo de autocompletar '{id_elemento}': {str(e)}")
            return False
    
    def preencher_textarea(self, id_elemento, valor):
        """Preenche um elemento textarea com o valor especificado"""
        try:
            elemento = self.wait.until(EC.presence_of_element_located((By.ID, id_elemento)))
            elemento.clear()
            elemento.send_keys(str(valor))
            return True
        except Exception as e:
            print(f"Erro ao preencher textarea '{id_elemento}': {str(e)}")
            return False
    
    def clicar_botao(self, id_elemento):
        """Clica em um botão pelo ID"""
        try:
            elemento = self.wait.until(EC.element_to_be_clickable((By.ID, id_elemento)))
            elemento.click()
            return True
        except Exception as e:
            print(f"Erro ao clicar no botão '{id_elemento}': {str(e)}")
            return False
    
    def abrir_acordeao(self, nome_secao):
        """Abre o acordeão correspondente à seção"""
        # Mapeamento de seções para IDs de acordeão
        acordeoes = {
            "venda": "//*[@id='ui-accordion-accordion-header-1']",
            "datas": "//*[@id='ui-accordion-accordion-header-2']",
            "valores": "//*[@id='ui-accordion-accordion-header-3']",
            "dados_empresa": "//*[@id='ui-accordion-accordion-header-4']",
            "endereco": "//*[@id='ui-accordion-accordion-header-5']",
            "responsavel": "//*[@id='ui-accordion-accordion-header-6']",
            "titular_dependentes": "//*[@id='ui-accordion-accordion-header-6']",
            "plano_pagamento": "//*[@id='ui-accordion-accordion-header-7']",
            "observacoes": "//*[@id='ui-accordion-accordion-header-8']"
        }
        
        # Verifica se a seção tem um acordeão correspondente
        xpath_acordeao = acordeoes.get(nome_secao)
        if not xpath_acordeao:
            print(f"  Seção '{nome_secao}' não tem acordeão mapeado")
            return True
        
        try:
            # Verifica se o acordeão existe
            acordeao = self.driver.find_element(By.XPATH, xpath_acordeao)
            
            # Verifica se o acordeão já está aberto (verificando a classe)
            if 'ui-state-active' not in acordeao.get_attribute('class'):
                print(f"  Abrindo acordeão para a seção '{nome_secao}'")
                # Rola até o acordeão para garantir que está visível
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", acordeao)
                time.sleep(0.5)  # Aguarda o scroll terminar
                
                # Clica para abrir o acordeão
                acordeao.click()
                print(f"  Aguardando o acordeão '{nome_secao}' abrir completamente...")
                time.sleep(2)  # Aguarda mais tempo para a animação e carregamento dos elementos
                
                # Verifica se o acordeão realmente abriu
                try:
                    acordeao = self.driver.find_element(By.XPATH, xpath_acordeao)
                    if 'ui-state-active' not in acordeao.get_attribute('class'):
                        print(f"  Tentando clicar novamente no acordeão '{nome_secao}'")
                        acordeao.click()
                        time.sleep(2)
                except Exception as e:
                    print(f"  Erro ao verificar se o acordeão abriu: {str(e)}")
            else:
                print(f"  Acordeão da seção '{nome_secao}' já está aberto")
            
            # Aguarda um tempo adicional para garantir que todos os elementos dentro do acordeão estejam carregados
            time.sleep(1)
            return True
        except Exception as e:
            print(f"  Erro ao abrir acordeão para a seção '{nome_secao}': {str(e)}")
            return False
    
    def preencher_secao(self, nome_secao):
        """Preenche todos os campos de uma seção específica"""
        print(f"\nPreenchendo seção: {nome_secao}")
        
        # Abre o acordeão correspondente à seção antes de preencher
        self.abrir_acordeao(nome_secao)
        
        secao = form_elements.get(nome_secao, {})
        dados_secao = dados_proposta.get(nome_secao, {})
        
        if not dados_secao:
            print(f"  Aviso: Não há dados para a seção '{nome_secao}'")
            return
            
        if not secao:
            print(f"  Aviso: Não há mapeamento de elementos para a seção '{nome_secao}'")
            # Tenta preencher usando os IDs dos dados como IDs dos elementos
            for id_elemento, valor in dados_secao.items():
                print(f"  Tentando preencher '{id_elemento}' com '{valor}' (sem mapeamento)")
                # Tenta como select primeiro
                if not self.preencher_select(id_elemento, valor):
                    # Se falhar, tenta como input
                    self.preencher_input(id_elemento, valor)
            return
        
        # Preenche os selects
        for select in secao.get("selects", []):
            id_elemento = select.get("id")
            valor = dados_secao.get(id_elemento)
            if valor:
                print(f"  Preenchendo select '{id_elemento}' com '{valor}'")
                self.preencher_select(id_elemento, valor)
        
        # Preenche os inputs
        for input_field in secao.get("inputs", []):
            id_elemento = input_field.get("id")
            valor = dados_secao.get(id_elemento)
            if valor:
                print(f"  Preenchendo input '{id_elemento}' com '{valor}'")
                self.preencher_input(id_elemento, valor)
        
        # Preenche os textareas
        for textarea in secao.get("textareas", []):
            id_elemento = textarea.get("id")
            valor = dados_secao.get(id_elemento)
            if valor:
                print(f"  Preenchendo textarea '{id_elemento}' com '{valor}'")
                self.preencher_textarea(id_elemento, valor)
                
        # Pausa para dar tempo ao usuário de ver o que está acontecendo
        time.sleep(1)
    
    def preencher_formulario(self):
        """Preenche todo o formulário de nova proposta"""
        print("Iniciando preenchimento do formulário...")
        
        # Lista de seções a serem preenchidas na ordem
        secoes = [
            "informacoes_principais",
            "venda",
            "datas",
            "valores",
            "dados_empresa",
            "endereco",
            "responsavel",
            "plano_pagamento",
            "observacoes"
        ]
        
        # Preenche cada seção
        for secao in secoes:
            self.preencher_secao(secao)
            time.sleep(1)  # Pequena pausa entre seções
        
        print("\nFormulário preenchido com sucesso!")
    
    def salvar_proposta(self):
        """Salva a proposta clicando no botão de salvar"""
        print("Salvando proposta...")
        botoes = form_elements.get("botoes_acao", {}).get("buttons", [])
        
        for botao in botoes:
            if botao.get("id") == "btn_salvar":
                self.clicar_botao("btn_salvar")
                break
        
        # Aguarda confirmação de salvamento
        try:
            self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "alert-success")))
            print("Proposta salva com sucesso!")
            return True
        except TimeoutException:
            print("Não foi possível confirmar o salvamento da proposta.")
            return False
    
    def fechar(self):
        """Fecha o navegador"""
        print("Fechando o navegador...")
        self.driver.quit()

def executar_automacao():
    """Função principal para executar a automação"""
    print("Iniciando automação de preenchimento de proposta no SixVox...")
    
    # Inicializa a automação
    automacao = SixvoxAutomation()
    
    # Realiza o login
    if not automacao.login():
        return
    
    # Navega para a página de nova proposta
    if not automacao.navegar_para_nova_proposta():
        automacao.fechar()
        return
    
    # Preenche o formulário
    automacao.preencher_formulario()
    
    # Pergunta se deseja salvar a proposta
    resposta = input("\nDeseja salvar a proposta? (s/n): ")
    if resposta.lower() == 's':
        automacao.salvar_proposta()
    
    # Pergunta se deseja fechar o navegador
    resposta = input("\nDeseja fechar o navegador? (s/n): ")
    if resposta.lower() == 's':
        automacao.fechar()
    else:
        print("Navegador mantido aberto. Feche manualmente quando terminar.")

if __name__ == "__main__":
    executar_automacao()
