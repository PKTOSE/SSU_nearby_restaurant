# SSU_nearby_restaurant
숭실대 근처 식당 랜덤 제안 프로젝트


#python exe build
use pyinstaller 

참고 : https://github.com/TomSchimansky/CustomTkinter/wiki/Packaging#windows-pyinstaller-auto-py-to-exe
```
pyinstaller --noconfirm --onedir --windowed --add-data "c:\users\arkitio\.conda\envs\rnd_menu\lib\site-packages/customtkinter;customtkinter/" index.py
```
