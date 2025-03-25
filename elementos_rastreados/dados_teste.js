/**
 * SCRIPT BASE PARA AUTOMAÇÃO RPA DE PREENCHIMENTO DE PROPOSTA
 * 
 * Este script exemplifica como implementar a automação para preencher o formulário
 * de propostas utilizando Puppeteer (uma biblioteca Node.js para automação de navegador).
 */

const puppeteer = require('puppeteer');
const formElements = require('./rpa-elements'); // Importa o mapeamento dos elementos

// Configuração da proposta (exemplo)
const propostaConfig = {
  // Informações Principais
  administradora: 'QUALICORP (61)',
  plano: 'Linha Amil',
  numeroProposta: '123456789',
  cnpj: '12.345.678/0001-90',
  razaoSocial: 'Empresa Exemplo LTDA',
  status: 'Novo',
  
  // Venda
  corretor: '4049 - Monica Mattos Takazaki (4049)',
  tipoCorretor: 'PLATINUM',
  distribuidora: 'Direto',
  carenciaCompra: 'Nao',
  operadoraCarencia: 'AMIL (167)',
  
  // Datas
  dataVenda: '15/03/2025',
  dataCadastro: '15/03/2025',
  dataVigencia: '01/04/2025',
  mesAniversario: 'Abril',
  
  // Valores
  vidasSaude: '5',
  mensalidadeSaude: '1500.00',
  taxaSaude: '0',
  iofSaude: '0',
  vidasDental: '5',
  mensalidadeDental: '150.00',
  taxaDental: '0',
  iofDental: '0',
  comissaoPrimeira: 'Boleto pago pelo Corretor/cliente',
  
  // Empresa
  nomeFantasia: 'Empresa Exemplo',
  porte: 'Pequeno',
  inscricaoEstadual: '123456789',
  site: 'www.empresaexemplo.com.br',
  
  // Contato
  contatoNome: 'João Silva',
  contatoDDD: '11',
  contatoTel: '98765-4321',
  contatoEmail: 'joao.silva@empresaexemplo.com.br',
  
  // Endereço
  cep: '01234-567',
  endereco: 'Rua Exemplo',
  numero: '123',
  complemento: 'Sala 45',
  bairro: 'Centro',
  cidade: 'São Paulo',
  uf: 'SP',
  
  // Titular
  titular: {
    nome: 'João da Silva',
    email: 'joao@exemplo.com',
    estadoCivil: 'Casado(a)',
    sexo: 'Masculino',
    nascimento: '01/01/1980',
    cpf: '123.456.789-00',
    nomeMae: 'Maria da Silva'
  },
  
  // Dependentes
  dependentes: [
    {
      nome: 'Ana da Silva',
      email: 'ana@exemplo.com',
      estadoCivil: 'Casado(a)',
      sexo: 'Feminino',
      nascimento: '01/01/1985',
      cpf: '987.654.321-00',
      nomeMae: 'Joana da Silva'
    }
  ]
};

// Função principal para automação
async function preencherProposta(config) {
  const browser = await puppeteer.launch({ 
    headless: false, // Visível para depuração
    defaultViewport: null, // Viewport automático
    args: ['--start-maximized'] // Iniciar maximizado
  });
  
  const page = await browser.newPage();
  
  try {
    // Acessar a página do formulário
    await page.goto('https://url-do-sistema-de-propostas.com.br/nova-proposta');
    
    // Aguardar carregamento da página
    await page.waitForSelector('#cod_administradora');

    console.log('Preenchendo Informações Principais...');
    // Preencher Informações Principais
    await selecionarOpcao(page, '#cod_administradora', config.administradora);
    await selecionarOpcao(page, '#cod_plano', config.plano);
    await preencherCampo(page, '#numero_proposta', config.numeroProposta);
    await preencherCampo(page, '#cnpj', config.cnpj);
    await preencherCampo(page, '#razao_social', config.razaoSocial);
    await selecionarOpcao(page, '#cod_status', config.status);
    
    console.log('Preenchendo Venda...');
    // Clicar na seção Venda
    await clicarSecao(page, 'Venda');
    
    // Preencher Venda
    await preencherCampo(page, '#name_corretor', config.corretor);
    await page.waitForTimeout(500);
    // Selecionar opção do autocomplete
    await page.click('#ui-id-7');
    
    await selecionarOpcao(page, '#cod_corretor_tipo', config.tipoCorretor);
    await selecionarOpcao(page, '#cod_distribuidora', config.distribuidora);
    await selecionarOpcao(page, '#carencia_compra', config.carenciaCompra);
    await selecionarOpcao(page, '#carencia_cod_operadora', config.operadoraCarencia);
    
    console.log('Preenchendo Datas...');
    // Clicar na seção Datas
    await clicarSecao(page, 'Datas');
    
    // Preencher Datas
    await preencherCampo(page, '#data_venda', config.dataVenda);
    await preencherCampo(page, '#data_cadastro', config.dataCadastro);
    await preencherCampo(page, '#data_vigencia', config.dataVigencia);
    await selecionarOpcao(page, '#mes_aniversario', config.mesAniversario);
    
    console.log('Preenchendo Valores...');
    // Clicar na seção Valores
    await clicarSecao(page, 'Valores');
    
    // Preencher Valores
    await preencherCampo(page, '#vidas_saude', config.vidasSaude);
    await preencherCampo(page, '#mensalidade_normal_saude', config.mensalidadeSaude);
    await preencherCampo(page, '#taxa_saude', config.taxaSaude);
    await preencherCampo(page, '#iof_saude', config.iofSaude);
    
    await preencherCampo(page, '#vidas_dental', config.vidasDental);
    await preencherCampo(page, '#mensalidade_normal_dental', config.mensalidadeDental);
    await preencherCampo(page, '#taxa_dental', config.taxaDental);
    await preencherCampo(page, '#iof_dental', config.iofDental);
    
    await selecionarOpcao(page, '#comissao_primeira', config.comissaoPrimeira);
    
    console.log('Preenchendo Empresa...');
    // Clicar na seção Empresa
    await clicarSecao(page, 'Empresa');
    
    // Preencher Empresa
    await preencherCampo(page, '#nome_fantasia', config.nomeFantasia);
    await preencherCampo(page, '#porte', config.porte);
    await preencherCampo(page, '#inscricao_estadual', config.inscricaoEstadual);
    await preencherCampo(page, '#site', config.site);
    
    // Preencher Contato
    await preencherCampo(page, '#contato_nome', config.contatoNome);
    await preencherCampo(page, '#contato_ddd', config.contatoDDD);
    await preencherCampo(page, '#contato_tel', config.contatoTel);
    await preencherCampo(page, '#contato_email', config.contatoEmail);
    
    // Preencher Endereço
    await preencherCampo(page, '#cep', config.cep);
    await page.waitForTimeout(1000); // Aguardar preenchimento automático do CEP
    
    await preencherCampo(page, '#endereco_empresa', config.endereco);
    await preencherCampo(page, '#endereco_numero', config.numero);
    await preencherCampo(page, '#endereco_complemento', config.complemento);
    await preencherCampo(page, '#endereco_bairro', config.bairro);
    await preencherCampo(page, '#endereco_cidade', config.cidade);
    await preencherCampo(page, '#endereco_uf', config.uf);
    
    console.log('Preenchendo Titular/Dependentes...');
    // Clicar na seção Titular/Dependentes
    await clicarSecao(page, 'Titular/Dependentes');
    
    // Incluir Titular
    await page.click('#incluir_titular');
    await page.waitForTimeout(500);
    
    // Preencher dados do Titular
    await preencherCampo(page, '#person_nome\\[\\]', config.titular.nome);
    await preencherCampo(page, '#person_email\\[\\]', config.titular.email);
    await selecionarOpcao(page, '#person_cod_estado_civil\\[\\]', config.titular.estadoCivil);
    await selecionarOpcao(page, '#person_sexo\\[\\]', config.titular.sexo);
    await preencherCampo(page, '#person_nascimento\\[\\]', config.titular.nascimento);
    await preencherCampo(page, '#person_cpf\\[\\]', config.titular.cpf);
    await preencherCampo(page, '#person_nome_mae\\[\\]', config.titular.nomeMae);
    
    // Incluir dependentes
    for (const dependente of config.dependentes) {
      // Clicar no botão incluir dependente
      await page.click('button:contains("Incluir dependente.")');
      await page.waitForTimeout(1000);
      
      // Esperar pelo carregamento dos novos campos
      // Nota: Os seletores dos dependentes podem variar, aqui precisamos ajustar conforme o sistema
      // Esta é uma implementação simplificada, em um cenário real precisaria ser adaptada
    }
    
    console.log('Preenchimento concluído!');
    
    // Aguardar algum tempo para visualização antes de encerrar
    await page.waitForTimeout(5000);
    
  } catch (error) {
    console.error('Erro durante o preenchimento:', error);
  } finally {
    await browser.close();
  }
}

// Funções auxiliares
async function preencherCampo(page, selector, valor) {
  await page.waitForSelector(selector);
  await page.click(selector, { clickCount: 3 }); // Selecionar todo o texto existente
  await page.type(selector, valor);
}

async function selecionarOpcao(page, selector, texto) {
  await page.waitForSelector(selector);
  await page.select(selector, await getOptionValue(page, selector, texto));
}

async function getOptionValue(page, selectSelector, optionText) {
  return await page.evaluate((selectSelector, optionText) => {
    const select = document.querySelector(selectSelector);
    for (const option of select.options) {
      if (option.text.includes(optionText)) {
        return option.value;
      }
    }
    return null;
  }, selectSelector, optionText);
}

async function clicarSecao(page, tituloSecao) {
  const xpath = `//h3[contains(text(), '${tituloSecao}')]`;
  await page.waitForXPath(xpath);
  const [secaoElement] = await page.$x(xpath);
  if (secaoElement) {
    await secaoElement.click();
    await page.waitForTimeout(500); // Aguardar abertura da seção
  }
}

// Executar o script
// preencherProposta(propostaConfig);

module.exports = { preencherProposta };