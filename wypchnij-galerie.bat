@echo off
chcp 65001 >nul

echo [1] Tworzenie kopii zapasowej index.html...
copy /Y index.html index.html.bak >nul
echo OK - Kopia zapisana jako index.html.bak

echo.
echo [2] Generowanie galerii (zdjecia + wideo)...
python update-gallery.py
if errorlevel 1 (
  echo BLAD podczas generowania galerii!
  echo Przywracanie index.html z kopii...
  copy /Y index.html.bak index.html >nul
  pause
  exit /b 1
)

echo.
echo [3] Dodawanie wszystkich plikow do Git...
git add .

echo [4] Zapisywanie commita...
git commit -m "aktualizacja strony"

echo.
echo [5] Wypychanie na GitHub...
git push

echo.
echo GOTOWE! Wszystkie zmiany wypchniete na GitHub.
echo Kopia zapasowa: index.html.bak
pause
