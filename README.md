# 📊 Job Market Analysis

---

**Table of Contents**
1. [Project Overview](#-project-overview)
2. [Project Structure](#-project-structure)
3. [Key Findings](#-key-findings)
4. [How to Run the Project](#-how-to-run-the-project)
   - [Prerequisites](#1-prerequisites)
   - [Installation](#2-installation)
   - [Running the Analysis](#3-running-the-analysis)
5. [Technologies](#-technologies)

---

## 📝 Project Overview

This project provides a comprehensive analysis of the IT job market in Ukraine, focusing on **Python**, **Java**, and **JavaScript** developer roles. Based on data collected from Work.ua, the analysis explores salary trends, experience requirements, and the demand for specific technical skills.

The project automates the entire pipeline: from data cleaning and statistical analysis to clustering and generating a professional PDF report.

---

## 📂 Project Structure

```text
job-market-analysis/
├── .gitignore                      # Essentials: exclude venv, __pycache__, .DS_Store
├── requirements.txt
├── README.md
├── data/
│   ├── parsed_data/
│   ├── cleaned_data/
│   └── analyzed_data/
├── scraping_service/               # Acts as the Scrapy project root
│   ├── scrapy.cfg                  # Deploy configuration
│   └── scraping_service/           # Main python package for the scraper
│       ├── __init__.py
│       ├── items.py                # Definition of scraped data models
│       ├── middlewares.py          # Custom request/response processing
│       ├── pipelines.py            # Item processing (cleaning, saving to file/DB)
│       ├── settings.py             # Settings (User-Agent, download delay, etc.)
│       └── spiders/
│           ├── __init__.py
│           └── workua_spider.py    # The spider logic goes here
├── data_cleaning_service/
│   ├── data_cleaning_workua.ipynb  # Main cleaning logic
│   └── utils/
│       ├── __init__.py             # Makes 'utils' importable
│       └── utils_workua.py         # Helper functions for cleaning
└── data_analysis_service/
    ├── data_analysis_workua.ipynb  # Main analysis logic
    └── utils/
        ├── __init__.py             # Makes 'utils' importable
        └── saving_utils.py         # PDF export logic
```

---

## 💡 Key Findings

- Experience Threshold: A significant salary increase occurs after the 2-year experience mark.

- Skill Impact: Proficiency in DevOps tools (Docker, CI/CD) often correlates with higher compensation than tenure alone.

- Market Segmentation: Clustering reveals a "High-Paying Middle" segment driven by skill intensity rather than just years of service.

👉 [View the Full Analysis PDF](https://github.com/mishagitcode/job-market-analysis/blob/develop/data/analyzed_data/data_analysis_workua.pdf)

---

## 🚀 How to Run the Project

Follow these steps to set up the environment and run the analysis on your local machine.

### 1. Prerequisites
- Python 3.8+
- Git

### 2. Installation

2.1. Clone the repository:

```commandline
git clone https://github.com/mishagitcode/job-market-analysis.git
```

```commandline
cd job-market-analysis
```

2.2. Create virtual environment

```commandline
python -m venv venv
```

2.3. Activate virtual environment

2.3.1. Windows:

```commandline 
venv\Scripts\activate
```

2.3.2. macOS/Linux:

```commandline
source venv/bin/activate
```


2.4. Install the required dependencies:

```commandline
pip install -r requirements.txt
```

Important: This project uses playwright to render the PDF report. You must install the Chromium browser engine:

```commandline
playwright install chromium
```

---

### 3. Running the Analysis

Launch the Jupyter Notebook to execute the code and generate the report:

```Bash
jupyter notebook data_analysis_service/data_analysis_workua.ipynb
```

Execute all cells. The final cell will automatically trigger the export script and save the results to data/analyzed_data/.

---

## 🛠 Technologies

- **Python**: Core programming language.

- **Pandas & NumPy**: Data manipulation and analysis.

- **Matplotlib**: Data visualization.

- **Scikit-Learn**: K-Means clustering algorithm.

- **Jupyter & Playwright**: Interactive development and PDF report generation.

---

Developed by [mishagitcode](https://github.com/mishagitcode)
