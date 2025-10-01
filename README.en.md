<h1 align="center"> Job Scraper - Automated Job Data Collection System </h1>

<div align="center">
  
  <a href="">[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://python.org/) </a>
  <a href="">[![Selenium 4.x](https://img.shields.io/badge/selenium-4.x-green.svg)](https://selenium.dev/) </a>
  <a href="">[![MIT Licence](https://img.shields.io/badge/license-MIT-lightgrey.svg)](LICENSE)</a>
  
</div>


### 🌍 Idiomas: [:uk: English](README.en.md) | [🇵🇹 Português](README.md)
## 📌 Job Scraper

This **job scraper** is a Python project for the automated collection of job listings.  
It was created purely for **educational purposes**, as an example of a modular system for automation and data collection.

> [!WARNING]
> This project is intended solely for learning and research purposes.  
> Always check a website’s **Terms of Service** before automating or collecting data.  
> Use responsibly.

---

##  Features

| Feature                       | Description                                                                 |
|-------------------------------|-----------------------------------------------------------------------------|
| ⚙️ YAML-based configuration   | Unified parameter management via the `settings.yaml` file                   |
| 📄 Data export                 | Supports multiple formats: **CSV and JSON**                                |
| 🕵️‍♂️ Headless mode             | Operates without a graphical interface for efficiency and discretion        |
| ⏱️ Request rate control        | Automatic intervals between requests to help avoid blocking                 |
| 🔧 Modular architecture        | Code separated into **utilities** + **site-specific scrapers**              |
| 🌍 Multi-platform support      | Compatible with **Net Empregos** and **Sapo Emprego**                       |

---

##  Project Structure

```text
├── scraper_utils.py        # Common utilities
├── net_empregos.py         # Implementation of the Net Empregos scraper  
├── sapo.py                 # Implementation of the Sapo Emprego scraper
├── run_scraper.py          # Main execution script
├── settings.yaml           # Application settings and parameters
├── requirements.txt        # Required dependencies
├── README.md               # Documentation (PT)
└── README.en.md            # Documentation (EN)
```
## Installation

1. Clone this repository:

```bash

 git clone https://github.com/mr-p-oliveira/job_search_portugal.git
 cd job-scraper

```

2. Install dependencies:

```bash

 pip install -r requirements.txt

```

## Configuration

```yaml

query:
  #-------- Sapo Emprego ------------
    local: "porto"
    pesquisa: "receptionist"  # For multiple terms use "+", e.g. "Engineering+Mechanical"
    hora: "full-time"
    ordem: "mais-recentes"    # Options: relevancia, mais-recentes, nome-a-z

  #-------- Net Empregos ------------
    zona: 2                   # Zone codes: 1-Lisbon, 2-Porto
    categoria: 0              # Category (do not change)
    tipo: 1                   # Contract type: 1-Full-Time, 2-Part-Time, 3-Internship

  output_formats: ["json"]    # Supported formats: json, csv

```


## ▶️ Run

```bash

 python run_scraper.py netempregos
 python run_scraper.py sapo

```

###  Example Output

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










