"""
MAPEAMENTO DE ELEMENTOS POR SEÇÃO PARA AUTOMAÇÃO RPA

Este arquivo contém o mapeamento estruturado dos elementos do formulário,
organizados por seção para facilitar a automação RPA de preenchimento de propostas.
"""

# Estrutura principal do formulário
form_elements = {
    # Seção: Informações Principais
    "informacoes_principais": {
        "selects": [
            {"id": "cod_administradora", "name": "cod_administradora", "label": "Administradora"},
            {"id": "cod_plano", "name": "cod_plano", "label": "Plano"},
            {"id": "cod_status", "name": "cod_status", "label": "Status"}
        ],
        "inputs": [
            {"id": "numero_proposta", "name": "numero_proposta", "type": "text", "required": True, "label": "Número da Proposta"},
            {"id": "cnpj", "name": "cnpj", "type": "text", "required": True, "label": "CNPJ"},
            {"id": "razao_social", "name": "razao_social", "type": "text", "required": True, "label": "Razão Social"},
            {"id": "cod_empresa_principal", "name": "cod_empresa_principal", "type": "text", "required": False, "label": "Código Empresa Principal"}
        ]
    },
    
    # Seção: Venda
    "venda": {
        "selects": [
            {"id": "cod_corretor_tipo", "name": "cod_corretor_tipo", "label": "Tipo de Corretor"},
            {"id": "cod_distribuidora", "name": "cod_distribuidora", "label": "Distribuidora"},
            {"id": "carencia_compra", "name": "carencia_compra", "label": "Carência Compra"},
            {"id": "carencia_cod_operadora", "name": "carencia_cod_operadora", "label": "Operadora Carência"}
        ],
        "inputs": [
            {"id": "name_corretor", "name": "name_corretor", "type": "text", "required": True, "label": "Nome do Corretor", "isAutocomplete": True}
        ]
    },
    
    # Seção: Dados da Empresa
    "dados_empresa": {
        "inputs": [
            {"id": "nome_fantasia", "name": "nome_fantasia", "type": "text", "required": False, "label": "Nome Fantasia"},
            {"id": "inscricao_estadual", "name": "inscricao_estadual", "type": "text", "required": False, "label": "Inscrição Estadual"},
            {"id": "data_fundacao", "name": "data_fundacao", "type": "date", "required": True, "label": "Data de Fundação"},
            {"id": "telefone", "name": "telefone", "type": "tel", "required": True, "label": "Telefone"},
            {"id": "email", "name": "email", "type": "email", "required": True, "label": "E-mail"}
        ],
        "selects": [
            {"id": "cod_ramo_atividade", "name": "cod_ramo_atividade", "label": "Ramo de Atividade"},
            {"id": "cod_natureza_juridica", "name": "cod_natureza_juridica", "label": "Natureza Jurídica"}
        ]
    },
    
    # Seção: Valores
    "valores": {
        "inputs": [
            # Saúde
            {"id": "vidas_saude", "name": "vidas_saude", "type": "text", "required": True, "label": "Qtd. Vidas Saúde", "isNumberOnly": True},
            {"id": "mensalidade_normal_saude", "name": "mensalidade_normal_saude", "type": "text", "required": True, "label": "Mensalidade Saúde", "isNumberOnly": True},
            {"id": "taxa_saude", "name": "taxa_saude", "type": "text", "required": False, "label": "Taxa Saúde", "isNumberOnly": True},
            {"id": "iof_saude", "name": "iof_saude", "type": "text", "required": False, "label": "IOF Saúde", "isNumberOnly": True},
            
            # Dental
            {"id": "vidas_dental", "name": "vidas_dental", "type": "text", "required": True, "label": "Qtd. Vidas Dental", "isNumberOnly": True},
            {"id": "mensalidade_normal_dental", "name": "mensalidade_normal_dental", "type": "text", "required": True, "label": "Mensalidade Dental", "isNumberOnly": True},
            {"id": "taxa_dental", "name": "taxa_dental", "type": "text", "required": False, "label": "Taxa Dental", "isNumberOnly": True},
            {"id": "iof_dental", "name": "iof_dental", "type": "text", "required": False, "label": "IOF Dental", "isNumberOnly": True}
        ]
    },
    
    # Seção: Endereço
    "endereco": {
        "inputs": [
            {"id": "cep", "name": "cep", "type": "text", "required": True, "label": "CEP"},
            {"id": "logradouro", "name": "logradouro", "type": "text", "required": True, "label": "Logradouro"},
            {"id": "numero", "name": "numero", "type": "text", "required": True, "label": "Número"},
            {"id": "complemento", "name": "complemento", "type": "text", "required": False, "label": "Complemento"},
            {"id": "bairro", "name": "bairro", "type": "text", "required": True, "label": "Bairro"}
        ],
        "selects": [
            {"id": "cod_estado", "name": "cod_estado", "label": "Estado"},
            {"id": "cod_cidade", "name": "cod_cidade", "label": "Cidade"}
        ]
    },
    
    # Seção: Responsável
    "responsavel": {
        "inputs": [
            {"id": "nome_responsavel", "name": "nome_responsavel", "type": "text", "required": True, "label": "Nome do Responsável"},
            {"id": "cpf_responsavel", "name": "cpf_responsavel", "type": "text", "required": True, "label": "CPF do Responsável"},
            {"id": "rg_responsavel", "name": "rg_responsavel", "type": "text", "required": False, "label": "RG do Responsável"},
            {"id": "data_nascimento_responsavel", "name": "data_nascimento_responsavel", "type": "date", "required": True, "label": "Data de Nascimento"},
            {"id": "telefone_responsavel", "name": "telefone_responsavel", "type": "tel", "required": True, "label": "Telefone do Responsável"},
            {"id": "email_responsavel", "name": "email_responsavel", "type": "email", "required": True, "label": "E-mail do Responsável"}
        ],
        "selects": [
            {"id": "cod_cargo_responsavel", "name": "cod_cargo_responsavel", "label": "Cargo do Responsável"},
            {"id": "cod_estado_civil", "name": "cod_estado_civil", "label": "Estado Civil"}
        ]
    },
    
    # Seção: Plano e Pagamento
    "plano_pagamento": {
        "selects": [
            {"id": "cod_operadora", "name": "cod_operadora", "label": "Operadora"},
            {"id": "cod_tipo_plano", "name": "cod_tipo_plano", "label": "Tipo de Plano"},
            {"id": "cod_forma_pagamento", "name": "cod_forma_pagamento", "label": "Forma de Pagamento"},
            {"id": "cod_dia_vencimento", "name": "cod_dia_vencimento", "label": "Dia de Vencimento"}
        ],
        "inputs": [
            {"id": "data_vigencia", "name": "data_vigencia", "type": "date", "required": True, "label": "Data de Vigência"},
            {"id": "valor_total", "name": "valor_total", "type": "number", "required": True, "label": "Valor Total (R$)"},
            {"id": "quantidade_vidas", "name": "quantidade_vidas", "type": "number", "required": True, "label": "Quantidade de Vidas"}
        ]
    },
    
    # Seção: Observações
    "observacoes": {
        "textareas": [
            {"id": "observacoes_gerais", "name": "observacoes_gerais", "required": False, "label": "Observações Gerais"}
        ]
    },
    
    # Botões de Ação
    "botoes_acao": {
        "buttons": [
            {"id": "btn_salvar", "name": "btn_salvar", "text": "Salvar", "type": "submit"},
            {"id": "btn_cancelar", "name": "btn_cancelar", "text": "Cancelar", "type": "button"},
            {"id": "btn_adicionar_beneficiario", "name": "btn_adicionar_beneficiario", "text": "Adicionar Beneficiário", "type": "button"}
        ]
    }
}

# Função para obter um elemento específico pelo ID
def get_element_by_id(element_id):
    """
    Busca um elemento pelo ID em todas as seções do formulário
    
    Args:
        element_id (str): ID do elemento a ser buscado
        
    Returns:
        dict: Informações do elemento encontrado ou None se não encontrado
    """
    for section_name, section_data in form_elements.items():
        for element_type, elements in section_data.items():
            for element in elements:
                if element.get("id") == element_id:
                    return {
                        "section": section_name,
                        "type": element_type,
                        "element": element
                    }
    return None

# Função para obter todos os elementos de uma seção
def get_elements_by_section(section_name):
    """
    Retorna todos os elementos de uma seção específica
    
    Args:
        section_name (str): Nome da seção
        
    Returns:
        dict: Dicionário com todos os elementos da seção ou None se a seção não existir
    """
    return form_elements.get(section_name)

# Função para obter elementos por tipo em uma seção específica
def get_elements_by_type(section_name, element_type):
    """
    Retorna elementos de um tipo específico em uma seção
    
    Args:
        section_name (str): Nome da seção
        element_type (str): Tipo de elemento (inputs, selects, buttons, textareas)
        
    Returns:
        list: Lista de elementos do tipo especificado ou lista vazia se não encontrado
    """
    section = form_elements.get(section_name, {})
    return section.get(element_type, [])

# Exemplo de uso:
if __name__ == "__main__":
    # Exemplo: Obter todos os campos obrigatórios
    required_fields = []
    
    for section_name, section_data in form_elements.items():
        for element_type, elements in section_data.items():
            for element in elements:
                if element.get("required") == True:
                    required_fields.append({
                        "id": element.get("id"),
                        "label": element.get("label"),
                        "section": section_name
                    })
    
    print(f"Total de campos obrigatórios: {len(required_fields)}")
    for field in required_fields:
        print(f"Campo: {field['label']} (ID: {field['id']}) - Seção: {field['section']}")
