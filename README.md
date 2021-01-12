# Final Project Sistem Deteksi Intrusi
## Muhammad Sulthon Nashir
## 05311840000011
## Teknologi Informasi

### Remote Server Integrity
Tool untuk mengecek integritas files pada server.

### Requirement
- Pyhthon 3.6.0+
- Windows
- Linux / OSX

### Instalasi
Clone ke direktori, lalu jalankan :

### Linux / OSX
```
 $ pip install virtualenv --user
 $ virtualenv venv      
 $ source venv/bin/activate   
 $ pip install .
```
### Windows
```
  C:\path\ke\program> pip install virtualenv --user
  C:\Users\You\Integrity> virtualenv venv
  C:\Users\You\Integrity> .\venv\Scripts\activate.bat
  C:\Users\You\Integrity> pip install .
```
### Penggunaan
Untuk menggunakan, jalankan:
```
$ remote-integrity --config {path_ke_file_config}.cfg
```
### Contoh File Config
 ```
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
    

   NB: Kosongkan api / chat_id jika tidak ingin ada push notification
```
