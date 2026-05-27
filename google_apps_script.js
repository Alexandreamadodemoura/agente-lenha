// ─────────────────────────────────────────────────────────────────────────────
// Agente Lenha — Google Apps Script
// Cole este código em: script.google.com → Novo projeto
// Depois: Implantar → App da Web → Qualquer pessoa → Implantar
// ─────────────────────────────────────────────────────────────────────────────

var SPREADSHEET_ID = "https://script.google.com/macros/s/AKfycbyd3aqtSw-O09eOs2rFaCM_ZRs1yI3NG_Hfp6bfMTyq3li9SbOc5qlD91CL8aNiFIni/exec";  // ← alterar
var SHEET_NAME     = "Registros";

function doPost(e) {
  try {
    var dados = JSON.parse(e.postData.contents);

    var planilha = SpreadsheetApp.openById(SPREADSHEET_ID);
    var aba      = planilha.getSheetByName(SHEET_NAME);

    // Criar cabeçalho se a aba estiver vazia
    if (aba.getLastRow() === 0) {
      aba.appendRow([
        "Data/Hora Registro",
        "Nº Ticket",
        "Data Ticket",
        "Hora Ticket",
        "Motorista",
        "Placa",
        "Produto",
        "Fornecedor",
        "Peso Bruto (kg)",
        "Peso Tara (kg)",
        "Peso Líquido (kg)",
        "WhatsApp"
      ]);

      // Formatar cabeçalho
      var cabecalho = aba.getRange(1, 1, 1, 12);
      cabecalho.setBackground("#2d6a2d");
      cabecalho.setFontColor("#ffffff");
      cabecalho.setFontWeight("bold");
    }

    // Gravar linha de dados
    aba.appendRow([
      new Date(),
      dados.numero_ticket  || "",
      dados.data_ticket    || "",
      dados.hora_ticket    || "",
      dados.motorista      || "",
      dados.placa          || "",
      dados.produto        || "Lenha",
      dados.fornecedor     || "",
      Number(dados.peso_bruto)   || 0,
      Number(dados.peso_tara)    || 0,
      Number(dados.peso_liquido) || 0,
      dados.numero_whatsapp || ""
    ]);

    return ContentService
      .createTextOutput(JSON.stringify({ status: "ok" }))
      .setMimeType(ContentService.MimeType.JSON);

  } catch (erro) {
    console.error("Erro no doPost:", erro);
    return ContentService
      .createTextOutput(JSON.stringify({ status: "erro", mensagem: erro.toString() }))
      .setMimeType(ContentService.MimeType.JSON);
  }
}

// Teste manual: execute esta função no editor para verificar a conexão
function testeManual() {
  var dadosTeste = {
    numero_ticket:  "1234",
    data_ticket:    "27/05/2026",
    hora_ticket:    "08:30",
    motorista:      "João Silva",
    placa:          "ABC-1234",
    produto:        "Lenha Eucalipto",
    fornecedor:     "Fazenda Boa Vista",
    peso_bruto:     12500,
    peso_tara:      4200,
    peso_liquido:   8300,
    numero_whatsapp: "5511999999999"
  };

  var planilha = SpreadsheetApp.openById(SPREADSHEET_ID);
  var aba      = planilha.getSheetByName(SHEET_NAME);
  aba.appendRow([
    new Date(),
    dadosTeste.numero_ticket,
    dadosTeste.data_ticket,
    dadosTeste.hora_ticket,
    dadosTeste.motorista,
    dadosTeste.placa,
    dadosTeste.produto,
    dadosTeste.fornecedor,
    dadosTeste.peso_bruto,
    dadosTeste.peso_tara,
    dadosTeste.peso_liquido,
    dadosTeste.numero_whatsapp
  ]);

  Logger.log("✅ Linha de teste gravada com sucesso!");
}
