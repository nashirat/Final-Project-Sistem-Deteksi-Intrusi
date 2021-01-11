# Remote Integrity Tool
Tool untuk mengecek integritas files pada server.

## Dependencies
* **Python version**: 3.6.0+ (3.6.7 digunakan untuk pembuatan)

## Installation
Clone ke direktori, lalu jalankan :

### Linux / OSX

    $ pip install virtualenv --user     # Install virtualenv
    $ virtualenv venv                   # Set up virtual environment 
    $ source venv/bin/activate          # Aktivasi virtual environment (Harus dilakukan setiap ingin menjalankan tool)
    $ pip install .                     # Install (use -e for development)

### Windows

    C:\Users\You\Integrity> pip install virtualenv --user
    C:\Users\You\Integrity> virtualenv venv
    C:\Users\You\Integrity> .\venv\Scripts\activate.bat
    C:\Users\You\Integrity> pip install .
    
## Usage (Remote Integrity tool)
Untuk menggunakan, jalankan:

    $ remote-integrity --config {path to config file}.cfg

## Configuration file format

    [server]
    server_name=Nama server
    server_port=22
    server_address=127.0.0.1
    
    [auth]
    auth_username=usrname
    auth_private_key=~/.ssh/id_rsa

    [filter]
    scan_php_modules = yes
    start_directory=~/Documents/
    ignore_files=.gitignore
    ignore_directories=.git,fonts
    
    [telegram]
    telegram_api_token={your api token}
    telegram_api_chat_id={your chat id}
    
## Skipping notifications

    Kosongkan api atau chat id.
