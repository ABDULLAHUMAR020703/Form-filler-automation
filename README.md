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
- Playwright (`pip install playwright`)
- PyYAML (for YAML support, if using customer_details.yml)

## Setup
1. Clone this repository:
   ```sh
   git clone https://github.com/yourusername/form-filler-automation.git
   cd form-filler-automation
   ```
2. (Optional) Create a virtual environment:
   ```sh
   python -m venv venv
   .\venv\Scripts\activate
   ```
3. Install dependencies:
   ```sh
   pip install playwright pyyaml
   playwright install
   ```

## Usage
- To run the fixed form filling script:
  ```sh
  python form_filling.py
  ```
- To use the more advanced or batch automation, see `automated_form_filler.py`.

## Customization
- Edit `form_filling.py` to change the form URL or the data being filled.
- Use `customer_details.yml` to provide batch data (see `automated_form_filler.py`).

## License
MIT License 