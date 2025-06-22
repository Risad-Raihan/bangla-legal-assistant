@echo off
echo Creating virtual environment...
python -m venv legal_env --without-pip

echo Downloading get-pip.py...
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py

echo Installing pip in virtual environment...
legal_env\Scripts\python.exe get-pip.py

echo Installing requirements...
legal_env\Scripts\python.exe -m pip install -r requirements.txt

echo Activating environment and starting app...
call legal_env\Scripts\activate.bat
streamlit run app.py

pause 