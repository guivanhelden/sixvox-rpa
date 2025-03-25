"""
DADOS DE EXEMPLO PARA PREENCHIMENTO DE PROPOSTA

Este arquivo contém dados de exemplo para preencher o formulário de nova proposta
no sistema SixVox. Estes dados podem ser usados para testes de automação RPA.
"""

# Dados de exemplo para preenchimento
dados_proposta = {
    # Informações Principais
    "informacoes_principais": {
        "cod_administradora": "QUALICORP (61)",
        "cod_plano": "Linha Amil",
        "numero_proposta": "123456789",
        "cnpj": "12.345.678/0001-90",
        "razao_social": "Empresa Exemplo LTDA",
        "cod_empresa_principal": "54321",
        "cod_status": "Novo"
    },
    
    # Venda
    "venda": {
        "name_corretor": "Monica Mattos Takazaki (4049)",
        "tipo_corretor": "PLATINUM",
        "distribuidora": "Direto",
        "carencia_compra": "Nao",
        "operadora_carencia": "AMIL (167)"
    },
    
    # Datas
    "datas": {
        "data_venda": "15/03/2025",
        "data_cadastro": "15/03/2025",
        "data_vigencia": "01/04/2025",
        "mes_aniversario": "Abril",
        "data_entrega": "30/04/2025"
    },
    
    # Valores
    "valores": {
        "vidas_saude": 5,
        "mensalidade_normal_saude": 1500.00,
        "taxa_saude": 0,
        "iof_saude": 0,
        "vidas_dental": 5,
        "mensalidade_normal_dental": 150.00,
        "taxa_dental": 0,
        "iof_dental": 0,
        "aditivo": 0,
        "comissao_primeira": "Boleto pago pelo Corretor/cliente"
    },
    
    # Dados da Empresa
    "dados_empresa": {
        "nome_fantasia": "Empresa Exemplo",
        "porte": "Pequeno",
        "inscricao_estadual": "123456789",
        "site": "www.empresaexemplo.com.br",
        "data_fundacao": "01/01/2010",  # Data fictícia adicionada
        "telefone": "11 98765-4321",    # Usando o telefone do contato
        "email": "joao.silva@empresaexemplo.com.br"  # Usando o email do contato
    },
    
    # Contato
    "contato": {
        "nome": "João Silva",
        "ddd": "11",
        "telefone": "98765-4321",
        "email": "joao.silva@empresaexemplo.com.br"
    },
    
    # Endereço
    "endereco": {
        "cep": "01234-567",
        "logradouro": "Rua Exemplo",
        "numero": "123",
        "complemento": "Sala 45",
        "bairro": "Centro",
        "cod_cidade": "São Paulo",
        "cod_estado": "SP"
    },
    
    # Responsável/Titular
    "responsavel": {
        "nome_responsavel": "João da Silva",
        "email_responsavel": "joao@exemplo.com",
        "cod_estado_civil": "Casado(a)",
        "sexo": "Masculino",
        "data_nascimento_responsavel": "01/01/1980",
        "cpf_responsavel": "123.456.789-00",
        "nome_mae": "Maria da Silva",
        "rg_responsavel": "12.345.678-9",  # RG fictício adicionado
        "telefone_responsavel": "11 98765-4321"  # Telefone fictício adicionado
    },
    
    # Plano e Pagamento
    "plano_pagamento": {
        "cod_operadora": "AMIL (167)",
        "cod_tipo_plano": "Linha Amil",
        "cod_forma_pagamento": "Boleto",
        "cod_dia_vencimento": "10",
        "data_vigencia": "01/04/2025",
        "valor_total": 1650.00,  # Soma de saúde e dental
        "quantidade_vidas": 5
    },
    
    # Dependentes
    "dependentes": [
        {
            "nome": "Ana da Silva",
            "email": "ana@exemplo.com",
            "estado_civil": "Casado(a)",
            "sexo": "Feminino",
            "data_nascimento": "01/01/1985",
            "cpf": "987.654.321-00",
            "nome_mae": "Joana da Silva"
        },
        {
            "nome": "Pedro da Silva",
            "email": "pedro@exemplo.com",
            "estado_civil": "Solteiro(a)",
            "sexo": "Masculino",
            "data_nascimento": "15/05/2010",
            "cpf": "111.222.333-44",
            "nome_mae": "Maria da Silva"
        }
    ],
    
    # Observações
    "observacoes": {
        "observacoes_gerais": "Proposta de teste para automação RPA."
    }
}

# Função para obter todos os dados de uma seção
def get_dados_secao(secao):
    """
    Retorna todos os dados de uma seção específica
    
    Args:
        secao (str): Nome da seção
        
    Returns:
        dict: Dicionário com todos os dados da seção ou None se a seção não existir
    """
    return dados_proposta.get(secao)

# Função para obter um valor específico
def get_valor(secao, campo):
    """
    Retorna o valor de um campo específico em uma seção
    
    Args:
        secao (str): Nome da seção
        campo (str): Nome do campo
        
    Returns:
        any: Valor do campo ou None se não encontrado
    """
    secao_dados = dados_proposta.get(secao)
    if secao_dados:
        return secao_dados.get(campo)
    return None

# Exemplo de uso:
if __name__ == "__main__":
    # Imprimir informações principais da proposta
    info = get_dados_secao("informacoes_principais")
    print("=== INFORMAÇÕES DA PROPOSTA ===")
    print(f"Administradora: {info.get('cod_administradora')}")
    print(f"Plano: {info.get('cod_plano')}")
    print(f"Número da Proposta: {info.get('numero_proposta')}")
    print(f"CNPJ: {info.get('cnpj')}")
    print(f"Razão Social: {info.get('razao_social')}")
    
    # Imprimir informações do responsável
    resp = get_dados_secao("responsavel")
    print("\n=== DADOS DO RESPONSÁVEL ===")
    print(f"Nome: {resp.get('nome_responsavel')}")
    print(f"CPF: {resp.get('cpf_responsavel')}")
    print(f"Data de Nascimento: {resp.get('data_nascimento_responsavel')}")
    
    # Imprimir dependentes
    deps = get_dados_secao("dependentes")
    print("\n=== DEPENDENTES ===")
    for i, dep in enumerate(deps, 1):
        print(f"\nDependente {i}:")
        print(f"Nome: {dep.get('nome')}")
        print(f"CPF: {dep.get('cpf')}")
        print(f"Data de Nascimento: {dep.get('data_nascimento')}")
