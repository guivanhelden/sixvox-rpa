# RPA para Cadastro de Propostas no SixVox

Este projeto contém ferramentas para automatizar o cadastro de propostas no sistema SixVox através de um RPA (Robotic Process Automation) baseado em Selenium.

## Estrutura do Projeto

- `element_tracker.py` - Ferramenta para rastrear elementos da interface enquanto você navega
- `rpa_cadastro_propostas.py` - RPA para automatizar o cadastro de propostas
- `requirements.txt` - Dependências do projeto

## Pré-requisitos

- Python 3.6+
- Google Chrome instalado
- Acesso ao sistema SixVox

## Instalação

1. Clone ou baixe este repositório
2. Crie um ambiente virtual Python:
   ```
   python -m venv venv
   ```
3. Ative o ambiente virtual:
   - Windows: `venv\Scripts\activate`
   - Mac/Linux: `source venv/bin/activate`
4. Instale as dependências:
   ```
   pip install -r requirements.txt
   ```

## Como Usar

### 1. Rastreamento de Elementos

Primeiro, execute o rastreador de elementos para mapear a interface do sistema enquanto você navega:

```
python element_tracker.py
```

Este script irá:
- Abrir um navegador Chrome
- Fazer login no sistema SixVox
- Rastrear elementos enquanto você navega pelo sistema
- Salvar os elementos rastreados na pasta `elementos_rastreados`

Navegue pelo sistema normalmente, especialmente pelo fluxo de cadastro de propostas. Pressione Ctrl+C quando terminar.

### 2. Criação do Template de Dados

Crie um template Excel para preencher com os dados das propostas:

```
python rpa_cadastro_propostas.py --template
```

Isso criará um arquivo `template_propostas.xlsx` que você pode preencher com os dados das propostas a serem cadastradas.

### 3. Execução do RPA

Depois de preencher o template com os dados, execute o RPA no modo automático:

```
python rpa_cadastro_propostas.py --arquivo template_propostas.xlsx --modo automatico
```

Ou execute no modo interativo para navegar manualmente:

```
python rpa_cadastro_propostas.py --modo interativo
```

## Personalização

O RPA foi desenvolvido para ser adaptável, mas pode ser necessário personalizá-lo de acordo com as especificidades do seu fluxo de cadastro de propostas:

1. Modifique a função `navegar_para_cadastro_proposta()` para ajustar a navegação
2. Adapte a função `preencher_formulario_proposta()` para mapear corretamente os campos do formulário
3. Ajuste o template de dados conforme necessário

## Segurança

As credenciais de acesso estão codificadas diretamente nos scripts para facilitar o desenvolvimento. Para um ambiente de produção, recomenda-se:

1. Criar um arquivo `.env` com as credenciais
2. Modificar os scripts para usar `os.getenv()` para obter as credenciais do ambiente

## Suporte

Para problemas ou dúvidas, entre em contato com o desenvolvedor.
