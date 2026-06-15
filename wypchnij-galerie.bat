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
if errorlevel 1 (
  echo BLAD podczas commita! Mozliwe, ze nie ma zmian do zapisania.
  pause
  exit /b 1
)

echo.
echo [5] Wypychanie na GitHub...
git push
if errorlevel 1 (
  echo.
  echo ============================================
  echo BLAD! PUSH NA GITHUB NIE POWIODL SIE!
  echo ============================================
  echo Najczestsza przyczyna: plik wideo (.mp4)
  echo przekracza 100 MB limit GitHub.
  echo.
  echo ROZWIAZANIE:
  echo 1. Skompresuj wideo do ponizej 100 MB
  echo    (np. na www.freeconvert.com/compress-mp4)
  echo 2. Lub usun plik z assets/gallery/ i wstaw
  echo    wideo na YouTube, a tu tylko link/iframe.
  echo 3. Po naprawie uruchom skrypt ponownie.
  echo ============================================
  pause
  exit /b 1
)

echo.
echo ============================================
echo GOTOWE! Wszystkie zmiany wypchniete na GitHub.
echo ============================================
echo Kopia zapasowa: index.html.bak
pause
