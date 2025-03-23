"""
RPA para Cadastro de Propostas no Sistema SixVox
Este script automatiza o processo de cadastro de novas propostas no sistema SixVox,
utilizando os elementos rastreados durante a navegação manual.
"""
import os
import json
import time
import pandas as pd
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Configurações
URL = "https://vhseguro.sixvox.com.br"
EMAIL = "marketing@vhseguros.com.br"  # Idealmente, usar os.getenv("EMAIL")
PASSWORD = "M@aite2017"  # Idealmente, usar os.getenv("PASSWORD")

# Diretório com os elementos rastreados
ELEMENTS_DIR = "elementos_rastreados"

class PropostaCadastroRPA:
    def __init__(self, data_file=None):
        """
        Inicializa o RPA para cadastro de propostas
        
        Args:
            data_file: Caminho para o arquivo CSV/Excel com os dados das propostas a cadastrar
        """
        self.driver = None
        self.element_maps = {}
        self.data_file = data_file
        self.propostas_data = None
        
        # Carregar dados de propostas se o arquivo for fornecido
        if data_file and os.path.exists(data_file):
            self.load_propostas_data()
    
    def load_propostas_data(self):
        """Carrega os dados das propostas a partir do arquivo CSV/Excel"""
        try:
            if self.data_file.endswith('.csv'):
                self.propostas_data = pd.read_csv(self.data_file)
            elif self.data_file.endswith(('.xlsx', '.xls')):
                self.propostas_data = pd.read_excel(self.data_file)
            
            print(f"Dados carregados: {len(self.propostas_data)} propostas encontradas")
        except Exception as e:
            print(f"Erro ao carregar dados das propostas: {str(e)}")
    
    def load_element_maps(self):
        """Carrega os mapeamentos de elementos a partir dos arquivos de rastreamento"""
        if not os.path.exists(ELEMENTS_DIR):
            print(f"Diretório {ELEMENTS_DIR} não encontrado. Execute o rastreador de elementos primeiro.")
            return False
        
        # Listar arquivos de elementos
        element_files = [f for f in os.listdir(ELEMENTS_DIR) if f.endswith('.json')]
        if not element_files:
            print("Nenhum arquivo de elementos encontrado. Execute o rastreador de elementos primeiro.")
            return False
        
        # Carregar todos os arquivos de elementos
        for file_name in element_files:
            file_path = os.path.join(ELEMENTS_DIR, file_name)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # Organizar elementos por URL
                for page_data in data:
                    url = page_data.get('url')
                    if url not in self.element_maps:
                        self.element_maps[url] = []
                    
                    self.element_maps[url].extend(page_data.get('elements', []))
            except Exception as e:
                print(f"Erro ao carregar arquivo {file_name}: {str(e)}")
        
        print(f"Mapeamentos de elementos carregados para {len(self.element_maps)} páginas")
        return True
    
    def setup_driver(self):
        """Configura o driver do Selenium"""
        chrome_options = Options()
        chrome_options.add_argument("--start-maximized")
        # Desabilitar o modo headless para visualizar a automação
        # chrome_options.add_argument("--headless")
        
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
    
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
    
    def find_element_by_properties(self, properties, wait_time=10):
        """
        Encontra um elemento com base em suas propriedades
        
        Args:
            properties: Dicionário com propriedades do elemento
            wait_time: Tempo de espera em segundos
        
        Returns:
            Elemento encontrado ou None
        """
        try:
            # Tentar encontrar por ID
            if properties.get('id'):
                return WebDriverWait(self.driver, wait_time).until(
                    EC.presence_of_element_located((By.ID, properties['id']))
                )
            
            # Tentar encontrar por nome
            if properties.get('name'):
                return WebDriverWait(self.driver, wait_time).until(
                    EC.presence_of_element_located((By.NAME, properties['name']))
                )
            
            # Tentar encontrar por XPath
            if properties.get('xpath'):
                return WebDriverWait(self.driver, wait_time).until(
                    EC.presence_of_element_located((By.XPATH, properties['xpath']))
                )
            
            # Tentar encontrar por texto (para links e botões)
            if properties.get('text') and properties.get('text').strip():
                xpath = f"//*[contains(text(), '{properties['text']}')]"
                return WebDriverWait(self.driver, wait_time).until(
                    EC.presence_of_element_located((By.XPATH, xpath))
                )
            
            return None
        except Exception:
            return None
    
    def navegar_para_cadastro_proposta(self):
        """Navega até a página de cadastro de propostas"""
        try:
            # Procurar por link ou botão que leve à página de propostas
            # Esta parte depende da estrutura do sistema e dos elementos rastreados
            # Exemplo genérico:
            menu_propostas = self.find_element_by_properties({
                'text': 'Propostas'
            })
            
            if menu_propostas:
                menu_propostas.click()
                time.sleep(1)
            
            # Procurar botão/link para nova proposta
            nova_proposta = self.find_element_by_properties({
                'text': 'Nova Proposta'
            })
            
            if nova_proposta:
                nova_proposta.click()
                time.sleep(2)
                return True
            
            print("Não foi possível navegar até a página de cadastro de propostas")
            return False
        except Exception as e:
            print(f"Erro ao navegar para cadastro de proposta: {str(e)}")
            return False
    
    def preencher_formulario_proposta(self, dados_proposta):
        """
        Preenche o formulário de cadastro de proposta
        
        Args:
            dados_proposta: Dicionário com os dados da proposta
        
        Returns:
            True se o preenchimento foi bem-sucedido, False caso contrário
        """
        try:
            # Esta função deve ser personalizada de acordo com os campos do formulário
            # e a estrutura dos dados das propostas
            
            # Exemplo genérico de preenchimento de campos
            for campo, valor in dados_proposta.items():
                # Pular campos vazios
                if pd.isna(valor) or valor == '':
                    continue
                
                # Procurar campo pelo nome ou label
                elemento = self.find_element_by_properties({
                    'name': campo
                })
                
                if not elemento:
                    # Tentar encontrar por ID
                    elemento = self.find_element_by_properties({
                        'id': campo
                    })
                
                if not elemento:
                    # Tentar encontrar por placeholder
                    elemento = self.find_element_by_properties({
                        'placeholder': campo
                    })
                
                # Se encontrou o elemento, preencher com o valor
                if elemento:
                    # Verificar o tipo de elemento
                    tag_name = elemento.tag_name.lower()
                    
                    if tag_name == 'select':
                        # Para campos de seleção
                        select = Select(elemento)
                        select.select_by_visible_text(str(valor))
                    elif tag_name == 'input':
                        # Para campos de entrada
                        input_type = elemento.get_attribute('type')
                        if input_type == 'checkbox':
                            if valor:
                                if not elemento.is_selected():
                                    elemento.click()
                        else:
                            elemento.clear()
                            elemento.send_keys(str(valor))
                    else:
                        # Para outros tipos de elementos
                        elemento.clear()
                        elemento.send_keys(str(valor))
                else:
                    print(f"Campo '{campo}' não encontrado no formulário")
            
            # Procurar e clicar no botão de salvar/enviar
            botao_salvar = self.find_element_by_properties({
                'text': 'Salvar'
            })
            
            if not botao_salvar:
                botao_salvar = self.find_element_by_properties({
                    'text': 'Enviar'
                })
            
            if not botao_salvar:
                botao_salvar = self.find_element_by_properties({
                    'text': 'Cadastrar'
                })
            
            if botao_salvar:
                botao_salvar.click()
                time.sleep(2)
                return True
            else:
                print("Botão de salvar não encontrado")
                return False
        
        except Exception as e:
            print(f"Erro ao preencher formulário: {str(e)}")
            return False
    
    def processar_propostas(self):
        """Processa todas as propostas do arquivo de dados"""
        if self.propostas_data is None or len(self.propostas_data) == 0:
            print("Nenhuma proposta para processar")
            return
        
        sucessos = 0
        falhas = 0
        
        for index, proposta in self.propostas_data.iterrows():
            print(f"\nProcessando proposta {index+1}/{len(self.propostas_data)}")
            
            # Navegar para a página de cadastro
            if not self.navegar_para_cadastro_proposta():
                falhas += 1
                continue
            
            # Preencher o formulário
            if self.preencher_formulario_proposta(proposta):
                print(f"Proposta {index+1} cadastrada com sucesso")
                sucessos += 1
            else:
                print(f"Falha ao cadastrar proposta {index+1}")
                falhas += 1
            
            # Aguardar um pouco entre cada proposta
            time.sleep(2)
        
        print(f"\nProcessamento concluído: {sucessos} propostas cadastradas com sucesso, {falhas} falhas")
    
    def criar_template_dados(self, output_file="template_propostas.xlsx"):
        """
        Cria um arquivo de template para preenchimento dos dados das propostas
        
        Args:
            output_file: Nome do arquivo de saída
        """
        try:
            # Esta função deve ser personalizada de acordo com os campos necessários
            # para o cadastro de propostas no sistema
            
            # Exemplo de colunas para o template
            colunas = [
                "nome_cliente", 
                "cpf", 
                "data_nascimento",
                "telefone", 
                "email", 
                "endereco",
                "cidade", 
                "estado", 
                "cep",
                "tipo_seguro", 
                "valor_proposta",
                "data_inicio_vigencia",
                "observacoes"
            ]
            
            # Criar DataFrame vazio com as colunas
            df = pd.DataFrame(columns=colunas)
            
            # Salvar como Excel
            df.to_excel(output_file, index=False)
            
            print(f"Template criado com sucesso: {output_file}")
            print("Preencha o arquivo com os dados das propostas e execute novamente o RPA")
        except Exception as e:
            print(f"Erro ao criar template: {str(e)}")
    
    def run(self, modo="interativo"):
        """
        Executa o RPA para cadastro de propostas
        
        Args:
            modo: Modo de execução ('interativo' ou 'automatico')
        """
        try:
            # Carregar mapeamentos de elementos
            if not self.load_element_maps():
                return
            
            # Configurar driver
            self.setup_driver()
            
            # Fazer login
            if not self.login():
                return
            
            if modo == "interativo":
                # Modo interativo: o usuário navega e o RPA apenas assiste
                print("\nModo interativo ativado.")
                print("Navegue pelo sistema normalmente para identificar o fluxo de cadastro de propostas.")
                print("Pressione Ctrl+C para encerrar.\n")
                
                while True:
                    time.sleep(1)
            
            elif modo == "automatico":
                # Modo automático: o RPA processa as propostas automaticamente
                if self.propostas_data is not None:
                    self.processar_propostas()
                else:
                    print("Nenhum dado de proposta carregado. Criando template...")
                    self.criar_template_dados()
            
        except KeyboardInterrupt:
            print("\nOperação interrompida pelo usuário.")
        except Exception as e:
            print(f"\nErro durante a execução: {str(e)}")
        finally:
            if self.driver:
                self.driver.quit()
            print("\nRPA finalizado.")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='RPA para cadastro de propostas no SixVox')
    parser.add_argument('--arquivo', type=str, help='Arquivo CSV/Excel com dados das propostas')
    parser.add_argument('--modo', type=str, choices=['interativo', 'automatico'], 
                        default='interativo', help='Modo de execução')
    parser.add_argument('--template', action='store_true', 
                        help='Criar template para preenchimento de dados')
    
    args = parser.parse_args()
    
    if args.template:
        rpa = PropostaCadastroRPA()
        rpa.criar_template_dados()
    else:
        rpa = PropostaCadastroRPA(args.arquivo)
        rpa.run(args.modo)
