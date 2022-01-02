# vaxFinder

## Disclaimer
Research purpose only. Public APIs. Please use at your own risk. 

https://techcrunch.com/2021/10/15/f12-isnt-hacking-missouri-governor-threatens-to-prosecute-local-journalist-for-finding-exposed-state-data/ 

## Usage
1. Clone the project
2. Create a virtual environment and install the dependencies in `requirements.txt`
   ```bash
   # create a virtual environment
   python3 -m venv venv
   
   # enable the virtual environment
   source venv/bin/activate
   
   # install the dependencies from requirements.txt
   pip install -r requirements.txt
   ```
3. Uncomment one of the "DOSE" lines in `main.py`. e.g.
   ```python
   # FIXME: uncomment only one of below to select the wanted dose
   # DOSE = "Pfizer Dose 1"
   # DOSE = "Pfizer Dose 2"
   DOSE = "Pfizer Dose 3"
   # DOSE = "Moderna Dose 1"
   # DOSE = "Moderna Dose 2"
   # DOSE = "Moderna Dose 3"
   ```
4. Run the script
   ```bash
   python main.py
   ```
