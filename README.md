# Web Scraping Projects

This repository contains two projects for web scraping:

1. **SALENIUM_SCRAPPING**: A tool to scrape content from Google Maps using a GUI built with Tkinter.
2. **PRODUCT_SCRAPING FROM WEBSITE**: A tool to scrape content from websites entered by the user using a GUI, with LLM integration for filtering and processing the scraped content.

## Table of Contents

- [1. SALENIUM_SCRAPPING](#1-salenium_scrapping)
  - [Requirements](#requirements)
  - [Setup and Installation](#setup-and-installation)
  - [How to Run](#how-to-run)
- [2. PRODUCT_SCRAPING FROM WEBSITE](#2-product_scraping-from-website)
  - [Requirements](#requirements-1)
  - [Setup and Installation](#setup-and-installation-1)
  - [How to Run](#how-to-run-1)
- [Contributing](#contributing)
- [License](#license)

## 1. SALENIUM_SCRAPPING

This project provides a GUI-based tool for scraping content from Google Maps.

### Requirements

- Python 3.7+
- `tkinter` for GUI
- `selenium` for web automation
- `chromedriver` or another driver compatible with your browser
- Other dependencies listed in `requirements.txt`

### Setup and Installation

1.1 **Clone the repository**:
   ```bash
   git clone https://github.com/Apiljungthapa/salenium_scrapping_googleMaps.git
   ```

1.2 **Navigate to folder path**:
   ```bash
   cd SALENIUM_SCRAPPING
   ```

1.3 **Install the required Python packages Make sure you have Python and pip installed, then run**:
   ```bash
   pip install -r requirements.txt
   ```
    

1.4 **Download ChromeDriver:**:
   Download the appropriate version of ChromeDriver for your browser from [ChromeDriver Downloads](https://googlechromelabs.github.io/chrome-for-testing/).
   Place the `chromedriver.exe` file in the same directory as your script or add it to your system PATH.
   
   
1.5 **Run Gui Application**:
    
    
    python main_gui.py

## 2. PRODUCT_SCRAPING FROM WEBSITE

This project provides a GUI-based tool for scraping product content from websites using LLM (Large Language Model) integration for filtering results.

### Requirements

- Python 3.7+
- `Streamlit` for GUI
- `selenium` for web automation
- `chromedriver` or another driver compatible with your browser
- LLM integration (ChatGroq)
- Other dependencies listed in `requirements.txt`


### Setup and Installation

2.1 **Clone the repository**:
   ```bash
   git clone https://github.com/Apiljungthapa/salenium_scrapping_googleMaps.git
   ```

2.2 **Navigate to folder path**:
   ```bash
   cd SALENIUM_SCRAPPING
   ```

2.3 **Install the required Python packages Make sure you have Python and pip installed, then run**:
   ```bash
   pip install -r requirements.txt
   ```
    

2.4 **Download ChromeDriver:**:
   Download the appropriate version of ChromeDriver for your browser from [ChromeDriver Downloads](https://googlechromelabs.github.io/chrome-for-testing/).
   Place the `chromedriver.exe` file in the same directory as your script or add it to your system PATH.
   
   
2.5 **Run Gui Application**:
    
    
    streamlit run gui.py

### Contributing

If you want to contribute to this project, feel free to open a pull request or issue on GitHub. We welcome all contributions that improve functionality or add new features!

### License
This project is licensed under the [MIT License]().

   

   
