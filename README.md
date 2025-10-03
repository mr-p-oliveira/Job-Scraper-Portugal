
<h1 align="center"> Job Scraper - Sistema de Recolha de Dados de Emprego</h1>

<div align="center">
  
  <a href="">[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://python.org/) </a>
  <a href="">[![Selenium 4.x](https://img.shields.io/badge/selenium-4.x-green.svg)](https://selenium.dev/) </a>
  <a href="">[![Licença MIT](https://img.shields.io/badge/license-MIT-lightgrey.svg)](LICENSE)</a>
  
</div>


### 🌍 Idiomas: [:uk: English](README.en.md) | [🇵🇹 Português](README.md)

## 📌 Scraper de Empregos 

Este **scraper de empregos** é um projeto em Python para a recolha automatizada de anúncios de emprego.
Foi criado apenas para fins educativos de forma a criar um sistema modular para automação de recolha de dados.

> [!WARNING]
> Este projeto destina-se apenas a fins de aprendizagem e investigação.  <br />
> Consulte sempre os **Termos de Serviço** de um site antes de automatizar ou recolher dados.   <br />
> Utilize de forma responsável.

## Funcionalidades

| Funcionalidade                | Descrição                                                                 |
|-------------------------------|---------------------------------------------------------------------------|
| ⚙️ Configuração via YAML       | Gestão unificada de parâmetros através do ficheiro  `settings.yaml`      |
| 📄  Exportação de Dados        | Suporte para múltiplos formatos: **CSV e JSON**                          |
| 🕵️‍♂️ Modo headless               | Operação sem interface gráfica para maior eficiência e discrição         |
| ⏱️ Controlo de Taxa de Pedidos   | Intervalos automáticos entre requisições para prevenção de bloqueios   |
| 🔧 Arquitetura Modular           | Código separado em **utilitários** + **scrapers específicos por site** |
| 🌍  Suporte Multiplataforma      | Compatibilidade com **Net Empregos** e **Sapo Emprego**|

## Estrutura 

```text
├── scraper_utils.py        # Utilitários comuns 
├── net_empregos.py         # Implementação do scraper para Net-Empregos  
├── sapo.py                 # Implementação do scraper para Sapo Emprego
├── run_scraper.py          # Script principal de execução
├── settings.yaml           # Configurações e parâmetros da aplicação
├── requirements.txt        # Dependências e pacotes necessários
└── README.md               # Documentação em PT 
```

## Instalação

1. Clonar este repositório:

```bash
git clone https://github.com/mr-p-oliveira/job_search_portugal.git
cd job-scraper
```
2. Instalar dependências:

```bash
pip install -r requirements.txt
```

## Configuração  

```yaml
query:
  #-------- Sapo Empregos ------------
    local: "porto"
    pesquisa: "rececionista"  # Termo de pesquisa (para múltiplos termos usar "+", ex: "Engenharia+Mecânica")
    hora: "full-time"
    ordem: "mais-recentes"    # Opções: relevancia, mais-recentes, nome-a-z

  #-------- Net-Empregos ------------
    zona: 2                   # Códigos de zona: 1-Lisboa, 2-Porto
    categoria: 0              # Categoria (não alterar)
    tipo: 1                   # Tipo de contrato: 1-Full-Time, 2-Part-Time, 3-Estágio
  output_formats: ["json"]    # Formatos suportados: json, csv
```
---
## Ficheiro de keywords 🔑

Para agilizar operações de monitorização em escala, o sistema admite a definição de termos de pesquisa em ficheiros `.txt`, assegurando processamento automatizado e contornando modificações manuais no `settings.yaml`.
📁  O sistema aceita qualquer nome de ficheiro .txt (exemplo `trabalhos.txt`)

1. Ficheiro
   
 Crie um ficheiro de texto (ex: keywords.txt) com os keyword alvo:
   ```text
   Engenheiro+biomédico
   Dispositivos+médicos
   Biossensores
   Nanotecnologia
   ```

> [!WARNING]
> Extensão obrigatória: `.txt`.   <br />
> Ficheiro não pode estar vazio.  <br />
> Cada linha representa um termo de pesquisa distinto.

## ▶️ Executar

Utilizando configuração padrão (settings.yaml):

```bash
python run_scraper.py netempregos
python run_scraper.py sapo
```
Com ficheiro personalizado de keywords: 

```bash
# Com ficheiro personalizado (qualquer nome)
python run_scraper.py netempregos meus_trabalhos.txt

# Com outro ficheiro
python run_scraper.py sapo termos_tecnicos.txt

```



### Exemplo de output

- administrativo_sapo_jobs_28-09-2025.json

```json
[
  {
    "Title": "Assistente Administrativo (m/f).",
    "Link": "https://emprego.sapo.pt/offers/assistente-administrativo-mf?id=e81b61da-b7eb-4988-aef2-4e9549125ec8",
    "Company": "Grupo Egor",
    "Location": "Povoa de Varzim, Portugal , Portugal",
    "Type": "Full-Time",
    "Date Posted": "Últimas 24 horas",
    "Description": "A Synchro, Outsourcing by Egor, está a recrutar Assistente Administrativo para empresa de referência no setor da distribuição e retalho de combustíveis e energias, com mais de 30 anos de atividade, situada na Póvoa de Varzim. FUNÇÃO Assegurar o aten"
  }
]
```


