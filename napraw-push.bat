@echo off
chcp 65001 >nul

echo ============================================
echo NAPRAWA - usuwanie duzego pliku z Gita
echo ============================================
echo.

REM Cofamy ostatni commit (zmiany zostaja w staging area)
echo [1] Cofanie ostatniego commita...
git reset --soft HEAD~1
if errorlevel 1 (
  echo BLAD przy git reset! Sprawdz czy jestes w folderze repozytorium.
  pause
  exit /b 1
)

REM Usuwamy duzy plik z indeksu Gita (staging area)
echo.
echo [2] Usuwanie duzego pliku z indeksu Gita...
git rm --cached "assets/karaoke Martyna Narcyz.mp4"
if errorlevel 1 (
  echo Plik nie byl w indeksie - to OK, lecimy dalej.
)

REM Dodajemy wszystko na nowo (bez usunietego wideo)
echo.
echo [3] Dodawanie zmian na nowo...
git add .

REM Nowy commit
echo.
echo [4] Zapisywanie nowego commita...
git commit -m "aktualizacja strony - bez duzego pliku wideo"

REM Push
echo.
echo [5] Wypychanie na GitHub...
git push
if errorlevel 1 (
  echo.
  echo ============================================
  echo BLAD! Push nadal nie dziala.
  echo ============================================
  echo Mozliwe przyczyny:
  echo - Plik wideo byl w jeszcze starszych commitach.
  echo - Inny plik przekracza 100 MB.
  echo.
  echo Wtedy rozwiazanie:
  echo 1. Otworz terminal (CMD) w tym folderze.
  echo 2. Wpisz: git log --stat
  echo 3. Znajdz commit z duzym plikiem.
  echo 4. Wpisz: git reset --soft HEAD~[liczba]
  echo    gdzie [liczba] = ile commitow wstecz.
  echo 5. Usun plik z dysku i zrob commit na nowo.
  echo ============================================
  pause
  exit /b 1
)

echo.
echo ============================================
echo GOTOWE! Plik wideo usuniety, reszta wypchnieta.
echo ============================================
pause
