"""
Element Tracker para o Sistema SixVox usando Playwright
Este script abre um navegador automatizado, faz login no sistema SixVox
e rastreia elementos enquanto o usuário navega pelo sistema.
"""
import os
import time
import json
import asyncio
from datetime import datetime
from playwright.async_api import async_playwright

# Configurações
URL = "https://vhseguro.sixvox.com.br"
EMAIL = "marketing@vhseguros.com.br"
PASSWORD = "M@ite2017"

# Diretório para salvar os dados rastreados
ELEMENTS_DIR = "elementos_rastreados"
os.makedirs(ELEMENTS_DIR, exist_ok=True)

class ElementTracker:
    def __init__(self):
        self.browser = None
        self.page = None
        self.tracked_elements = []
        self.current_url = ""
        
    async def setup_browser(self):
        """Configura o navegador Playwright"""
        playwright = await async_playwright().start()
        self.browser = await playwright.chromium.launch(headless=False)
        self.page = await self.browser.new_page()
        
    async def login(self):
        """Realiza login no sistema"""
        try:
            await self.page.goto(URL)
            print(f"Acessando {URL}...")
            
            # Aguardar página de login carregar e usar os seletores XPath fornecidos
            await self.page.wait_for_selector("//input[@id='email']")
            
            # Preencher credenciais
            await self.page.fill("//input[@id='email']", EMAIL)
            await self.page.fill("//input[@id='xenha']", PASSWORD)  # Usando o id 'xenha' conforme informado
            
            # Clicar no botão de login
            await self.page.click("//input[@id='enviar']")
            
            # Aguardar login ser concluído (ajustando para ser mais genérico)
            try:
                # Tentar aguardar redirecionamento para dashboard ou outra página após login
                await self.page.wait_for_load_state('networkidle', timeout=10000)
                print("Login realizado com sucesso!")
                return True
            except Exception as e:
                print(f"Aviso: {str(e)}")
                # Mesmo com erro, continuar se a página mudou
                if self.page.url != URL:
                    print("Página mudou após tentativa de login, continuando...")
                    return True
                return False
        except Exception as e:
            print(f"Erro ao fazer login: {str(e)}")
            return False
    
    async def track_elements(self):
        """Rastreia elementos da página atual"""
        try:
            # Obter URL atual
            current_url = self.page.url
            page_title = await self.page.title()
            
            # Se mudou de página, atualizar
            if current_url != self.current_url:
                self.current_url = current_url
                print(f"\nRastreando elementos da página: {page_title} ({current_url})")
            
            # Rastrear elementos interativos
            elements_data = {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "url": current_url,
                "title": page_title,
                "elements": []
            }
            
            # Rastrear botões
            buttons = await self.page.query_selector_all('button')
            for button in buttons:
                try:
                    text = await button.text_content()
                    id_attr = await button.get_attribute('id')
                    name_attr = await button.get_attribute('name')
                    class_attr = await button.get_attribute('class')
                    
                    element_data = {
                        "type": "button",
                        "text": text.strip() if text else "",
                        "id": id_attr,
                        "name": name_attr,
                        "class": class_attr,
                        "selector": await self.get_selector(button)
                    }
                    elements_data["elements"].append(element_data)
                except:
                    pass
            
            # Rastrear inputs
            inputs = await self.page.query_selector_all('input')
            for input_elem in inputs:
                try:
                    id_attr = await input_elem.get_attribute('id')
                    name_attr = await input_elem.get_attribute('name')
                    type_attr = await input_elem.get_attribute('type')
                    placeholder_attr = await input_elem.get_attribute('placeholder')
                    class_attr = await input_elem.get_attribute('class')
                    
                    element_data = {
                        "type": "input",
                        "input_type": type_attr,
                        "id": id_attr,
                        "name": name_attr,
                        "placeholder": placeholder_attr,
                        "class": class_attr,
                        "selector": await self.get_selector(input_elem)
                    }
                    elements_data["elements"].append(element_data)
                except:
                    pass
            
            # Rastrear selects
            selects = await self.page.query_selector_all('select')
            for select in selects:
                try:
                    id_attr = await select.get_attribute('id')
                    name_attr = await select.get_attribute('name')
                    class_attr = await select.get_attribute('class')
                    
                    element_data = {
                        "type": "select",
                        "id": id_attr,
                        "name": name_attr,
                        "class": class_attr,
                        "selector": await self.get_selector(select)
                    }
                    elements_data["elements"].append(element_data)
                except:
                    pass
            
            # Rastrear links
            links = await self.page.query_selector_all('a')
            for link in links:
                try:
                    text = await link.text_content()
                    href_attr = await link.get_attribute('href')
                    id_attr = await link.get_attribute('id')
                    class_attr = await link.get_attribute('class')
                    
                    element_data = {
                        "type": "link",
                        "text": text.strip() if text else "",
                        "href": href_attr,
                        "id": id_attr,
                        "class": class_attr,
                        "selector": await self.get_selector(link)
                    }
                    elements_data["elements"].append(element_data)
                except:
                    pass
            
            # Rastrear labels
            labels = await self.page.query_selector_all('label')
            for label in labels:
                try:
                    text = await label.text_content()
                    for_attr = await label.get_attribute('for')
                    id_attr = await label.get_attribute('id')
                    class_attr = await label.get_attribute('class')
                    
                    element_data = {
                        "type": "label",
                        "text": text.strip() if text else "",
                        "for": for_attr,
                        "id": id_attr,
                        "class": class_attr,
                        "selector": await self.get_selector(label)
                    }
                    elements_data["elements"].append(element_data)
                except:
                    pass
            
            # Rastrear menus suspensos (dropdown)
            # Procurar elementos que geralmente são menus suspensos
            dropdown_selectors = [
                '.dropdown',          # Bootstrap
                '[role="menu"]',      # ARIA
                '.menu-dropdown',     # Comum
                'ul.menu',            # Comum
                'nav ul',             # Navegação
                'select',             # HTML nativo
                'details',            # HTML5
                '[aria-haspopup="true"]'  # ARIA
            ]
            
            for selector in dropdown_selectors:
                try:
                    dropdowns = await self.page.query_selector_all(selector)
                    for dropdown in dropdowns:
                        try:
                            # Informações básicas do menu
                            id_attr = await dropdown.get_attribute('id')
                            class_attr = await dropdown.get_attribute('class')
                            text = await dropdown.text_content()
                            
                            # Criar entrada para o menu
                            dropdown_data = {
                                "type": "dropdown_menu",
                                "text": text.strip() if text else "",
                                "id": id_attr,
                                "class": class_attr,
                                "selector": await self.get_selector(dropdown),
                                "items": []
                            }
                            
                            # Tentar encontrar itens do menu
                            menu_items = await dropdown.query_selector_all('li, option, a')
                            for item in menu_items:
                                try:
                                    item_text = await item.text_content()
                                    item_id = await item.get_attribute('id')
                                    item_class = await item.get_attribute('class')
                                    item_href = await item.get_attribute('href')
                                    item_value = await item.get_attribute('value')
                                    
                                    item_data = {
                                        "text": item_text.strip() if item_text else "",
                                        "id": item_id,
                                        "class": item_class,
                                        "href": item_href,
                                        "value": item_value,
                                        "selector": await self.get_selector(item)
                                    }
                                    dropdown_data["items"].append(item_data)
                                except:
                                    pass
                            
                            # Adicionar menu à lista de elementos
                            elements_data["elements"].append(dropdown_data)
                        except:
                            pass
                except:
                    pass
            
            # Adicionar à lista de elementos rastreados
            self.tracked_elements.append(elements_data)
            
            # Salvar elementos rastreados
            await self.save_tracked_elements()
            
            print(f"Rastreados {len(elements_data['elements'])} elementos")
            
        except Exception as e:
            print(f"Erro ao rastrear elementos: {str(e)}")
    
    async def get_selector(self, element):
        """Obtém um seletor CSS para o elemento"""
        try:
            # Tenta obter um seletor CSS único para o elemento
            return await self.page.evaluate("""(element) => {
                function getSelector(el) {
                    if (el.id) {
                        return '#' + el.id;
                    }
                    
                    if (el.name) {
                        return el.tagName.toLowerCase() + '[name="' + el.name + '"]';
                    }
                    
                    var path = [];
                    while (el && el.nodeType === Node.ELEMENT_NODE) {
                        var selector = el.nodeName.toLowerCase();
                        if (el.id) {
                            selector += '#' + el.id;
                            path.unshift(selector);
                            break;
                        } else {
                            var sib = el, nth = 1;
                            while (sib.previousElementSibling) {
                                sib = sib.previousElementSibling;
                                if (sib.nodeName.toLowerCase() === selector) nth++;
                            }
                            if (nth !== 1) selector += ":nth-of-type("+nth+")";
                        }
                        path.unshift(selector);
                        el = el.parentNode;
                    }
                    return path.join(' > ');
                }
                return getSelector(element);
            }""", element)
        except:
            return ""
    
    async def save_tracked_elements(self):
        """Salva os elementos rastreados em um arquivo JSON"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{ELEMENTS_DIR}/elements_{timestamp}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.tracked_elements, f, ensure_ascii=False, indent=2)
    
    async def run(self):
        """Executa o rastreador de elementos"""
        try:
            await self.setup_browser()
            if not await self.login():
                return
            
            print("\nNavegue pelo sistema normalmente. O rastreador está ativo.")
            print("Pressione Ctrl+C para encerrar o rastreamento.\n")
            
            # Loop principal para rastrear elementos enquanto o usuário navega
            while True:
                await self.track_elements()
                await asyncio.sleep(2)  # Intervalo entre rastreamentos
                
        except KeyboardInterrupt:
            print("\nRastreamento interrompido pelo usuário.")
        except Exception as e:
            print(f"\nErro durante o rastreamento: {str(e)}")
        finally:
            if self.browser:
                await self.browser.close()
            print("\nRastreamento finalizado. Elementos salvos em:", ELEMENTS_DIR)

async def main():
    tracker = ElementTracker()
    await tracker.run()

if __name__ == "__main__":
    asyncio.run(main())
