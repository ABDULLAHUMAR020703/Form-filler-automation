# form-filler-automation

A Python automation tool that fills out web forms automatically using Playwright. This project demonstrates how to automate form filling for testing or productivity purposes, with robust element waiting and error handling.

## Features
- Automates filling out web forms using Playwright (sync API)
- Handles element waiting and selectors robustly
- Supports file upload, dropdowns, checkboxes, and radio buttons
- Error handling with screenshot capture on failure
- Customizable for different forms and data sources

## Requirements
- Python 3.8+
- All dependencies listed in `requirements.txt`

## Setup
1. Clone this repository:
   ```sh
   git clone https://github.com/ABDULLAHUMAR020703/Form-filler-automation.git
   cd Form-filler-automation
   ```
2. (Optional) Create a virtual environment:
   ```sh
   python -m venv venv
   .\venv\Scripts\activate
   ```
3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   playwright install
   ```

## Usage
- To run the fixed form filling script (if you have it locally):
  ```sh
  python automated_form_filling.py
  ```

## Customization
- Edit `automated_form_filler.py` to change the form URL or the data being filled.
- Use `customer_details.yml` to provide batch data.


## License
MIT License 