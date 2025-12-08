# Praktični dio

Svugdje gdje piše "python" kod mene npr ide "python3" tako da imajte na umu mozda i kod vas.
Ja imam Python 3.12.3, ako netko ima noviju mozda da se prebacimo na tu? Ili instalirajte ovu pa ju koristite

## Stvaranje virtualnog okuženja
Linux: python -m venv venv
Windows: py -m venv venv_windows

## Aktiviranje venv
Linux: source venv/bin/activate
Windows: .\venv_windows\Scripts\Activate.ps1 

## Izlazak iz venv
deactivate

## Instaliranje biblioteka u requirements.txt
Linux: pip install -r requirements.txt
Windows: py -m pip install -r .\requirements.txt

## Pokretanje aplikacije
Linux: python main.py
Windows: py main.py

## Preporuke
Na vsc-u instalirajte extention "SQLite Viewer" za pregledavanje baze

## Packaganje aplikacije

### Linux

pyinstaller --noconfirm --onefile --windowed --name "SecureFileVault" \
    --icon "src/pic/app_icon.png" \
    --add-data "data/schema.sql:data" \
    --add-data "security_policy.json:." \
    --add-data "src/views/themes/dark_theme.qss:src/views/themes" \
    --add-data "src/pic:src/pic" \
    main.py

### Windows

pyinstaller --noconfirm --onefile --windowed --name "SecureFileVault" `
    --icon "src/pic/app_icon.ico" `
    --add-data "data/schema.sql;data" `
    --add-data "security_policy.json;." `
    --add-data "src/views/themes/dark_theme.qss;src/views/themes" `
    --add-data "src/pic;src/pic" `
    main.py