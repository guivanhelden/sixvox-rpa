/**
 * MAPEAMENTO DE ELEMENTOS POR SEÇÃO PARA AUTOMAÇÃO RPA
 * 
 * Este arquivo contém o mapeamento estruturado dos elementos do formulário,
 * organizados por seção para facilitar a automação RPA de preenchimento de propostas.
 */

// Estrutura principal do formulário
const formElements = {
    // Seção: Informações Principais
    informacoesPrincipais: {
      selects: [
        { id: "cod_administradora", name: "cod_administradora", label: "Administradora" },
        { id: "cod_plano", name: "cod_plano", label: "Plano" },
        { id: "cod_status", name: "cod_status", label: "Status" }
      ],
      inputs: [
        { id: "numero_proposta", name: "numero_proposta", type: "text", required: true, label: "Número da Proposta" },
        { id: "cnpj", name: "cnpj", type: "text", required: true, label: "CNPJ" },
        { id: "razao_social", name: "razao_social", type: "text", required: true, label: "Razão Social" },
        { id: "cod_empresa_principal", name: "cod_empresa_principal", type: "text", required: false, label: "Código Empresa Principal" }
      ]
    },
    
    // Seção: Venda
    venda: {
      selects: [
        { id: "cod_corretor_tipo", name: "cod_corretor_tipo", label: "Tipo de Corretor" },
        { id: "cod_distribuidora", name: "cod_distribuidora", label: "Distribuidora" },
        { id: "carencia_compra", name: "carencia_compra", label: "Carência Compra" },
        { id: "carencia_cod_operadora", name: "carencia_cod_operadora", label: "Operadora Carência" }
      ],
      inputs: [
        { id: "name_corretor", name: "name_corretor", type: "text", required: false, label: "Nome do Corretor", isAutocomplete: true }
      ],
      autocompleteOptions: [
        { id: "ui-id-7", text: "4049 - Monica Mattos Takazaki (4049)" }
      ]
    },
    
    // Seção: Datas
    datas: {
      selects: [
        { id: "mes_aniversario", name: "mes_aniversario", label: "Mês de Aniversário" }
      ],
      inputs: [
        { id: "data_venda", name: "data_venda", type: "text", required: true, label: "Data da Venda", isDatepicker: true },
        { id: "data_cadastro", name: "data_cadastro", type: "text", required: true, label: "Data de Cadastro", isDatepicker: true },
        { id: "data_vigencia", name: "data_vigencia", type: "text", required: true, label: "Data de Vigência", isDatepicker: true },
        { id: "data_entrega", name: "data_entrega", type: "text", required: false, label: "Data de Entrega", isDatepicker: true }
      ]
    },
    
    // Seção: Valores
    valores: {
      inputs: [
        // Saúde
        { id: "vidas_saude", name: "vidas_saude", type: "text", required: true, label: "Qtd. Vidas Saúde", isNumberOnly: true },
        { id: "mensalidade_normal_saude", name: "mensalidade_normal_saude", type: "text", required: true, label: "Mensalidade Saúde", isNumberOnly: true },
        { id: "taxa_saude", name: "taxa_saude", type: "text", required: false, label: "Taxa Saúde", isNumberOnly: true },
        { id: "iof_saude", name: "iof_saude", type: "text", required: false, label: "IOF Saúde", isNumberOnly: true },
        
        // Dental
        { id: "vidas_dental", name: "vidas_dental", type: "text", required: true, label: "Qtd. Vidas Dental", isNumberOnly: true },
        { id: "mensalidade_normal_dental", name: "mensalidade_normal_dental", type: "text", required: true, label: "Mensalidade Dental", isNumberOnly: true },
        { id: "taxa_dental", name: "taxa_dental", type: "text", required: false, label: "Taxa Dental", isNumberOnly: true },
        { id: "iof_dental", name: "iof_dental", type: "text", required: false, label: "IOF Dental", isNumberOnly: true },
        
        // Aditivo
        { id: "aditivo[16]", name: "aditivo[16]", type: "text", required: false, label: "Aditivo", isNumberOnly: true }
      ],
      selects: [
        { id: "comissao_primeira", name: "comissao_primeira", label: "Comissão Primeira" }
      ]
    },
    
    // Seção: Empresa
    empresa: {
      inputs: [
        { id: "nome_fantasia", name: "nome_fantasia", type: "text", required: false, label: "Nome Fantasia" },
        { id: "porte", name: "porte", type: "text", required: false, label: "Porte" },
        { id: "inscricao_estadual", name: "inscricao_estadual", type: "text", required: false, label: "Inscrição Estadual" },
        { id: "site", name: "site", type: "text", required: false, label: "Site" },
        
        // Contato
        { id: "contato_nome", name: "contato_nome", type: "text", required: false, label: "Nome do Contato" },
        { id: "contato_ddd", name: "contato_ddd", type: "text", required: false, label: "DDD" },
        { id: "contato_tel", name: "contato_tel", type: "text", required: false, label: "Telefone" },
        { id: "contato_email", name: "contato_email", type: "text", required: false, label: "E-mail do Contato" },
        
        // Endereço
        { id: "cep", name: "cep", type: "text", required: false, label: "CEP" },
        { id: "endereco_empresa", name: "endereco_empresa", type: "text", required: false, label: "Endereço" },
        { id: "endereco_numero", name: "endereco_numero", type: "text", required: false, label: "Número" },
        { id: "endereco_complemento", name: "endereco_complemento", type: "text", required: false, label: "Complemento" },
        { id: "endereco_bairro", name: "endereco_bairro", type: "text", required: false, label: "Bairro" },
        { id: "endereco_cidade", name: "endereco_cidade", type: "text", required: false, label: "Cidade" },
        { id: "endereco_uf", name: "endereco_uf", type: "text", required: false, label: "UF" },
        { id: "endereco_cep", name: "endereco_cep", type: "text", required: false, label: "CEP (Endereço)" }
      ]
    },
    
    // Seção: Titular/Dependentes
    titularDependentes: {
      buttons: [
        { id: "incluir_titular", label: "Incluir Titular" },
        { xpath: "/html/body/div/form/div/div[2]/div[7]/div/div/div/div[9]/button", label: "Incluir Dependente" }
      ],
      titularInputs: [
        { id: "person_nome[]", name: "person_nome[]", type: "text", required: false, label: "Nome" },
        { id: "person_email[]", name: "person_email[]", type: "text", required: false, label: "E-mail" },
        { id: "person_nascimento[]", name: "person_nascimento[]", type: "text", required: false, label: "Data de Nascimento" },
        { id: "person_cpf[]", name: "person_cpf[]", type: "text", required: false, label: "CPF" },
        { id: "person_nome_mae[]", name: "person_nome_mae[]", type: "text", required: false, label: "Nome da Mãe" }
      ],
      titularSelects: [
        { id: "person_cod_estado_civil[]", name: "person_cod_estado_civil[]", label: "Estado Civil" },
        { id: "person_sexo[]", name: "person_sexo[]", label: "Sexo" }
      ]
    }
  };
  
  // Exporta a estrutura para uso em scripts de automação
  module.exports = formElements;