@echo off
chcp 65001 >nul
title Mini RAG - Akilli Dokuman Soru-Cevap Sistemi
cd /d "%~dp0"

set VENV_PY=%~dp0venv\Scripts\python.exe

echo ============================================
echo   Mini RAG baslatiliyor...
echo ============================================
echo.

REM --- 1) venv yoksa olustur ---
if not exist "%VENV_PY%" (
    echo [1/4] Sanal ortam bulunamadi, olusturuluyor...
    python -m venv venv
    if errorlevel 1 (
        echo.
        echo HATA: Python bulunamadi veya venv olusturulamadi.
        echo Once Python kurmalisin: https://www.python.org/downloads/
        echo Kurulum sirasinda "Add Python to PATH" kutucugunu isaretlemeyi unutma.
        pause
        exit /b 1
    )
) else (
    echo [1/4] Sanal ortam zaten mevcut, atlaniyor.
)

REM --- 2) venv icindeki python ile pip guncelle ---
echo [2/4] pip kontrol ediliyor...
"%VENV_PY%" -m pip install --upgrade pip >nul

REM --- 3) Kutuphaneler kurulu mu diye venv python'u ile kontrol et ---
"%VENV_PY%" -c "import fitz, streamlit, chromadb" 2>nul
if errorlevel 1 (
    echo [3/4] Gerekli kutuphaneler kuruluyor, bu ilk seferde birkac dakika surebilir...
    "%VENV_PY%" -m pip install -r requirements.txt
    if errorlevel 1 (
        echo.
        echo HATA: Kutuphaneler kurulamadi. Yukaridaki hata mesajini kontrol et.
        pause
        exit /b 1
    )
) else (
    echo [3/4] Kutuphaneler zaten kurulu, atlaniyor.
)

REM --- 4) .env yoksa olustur ---
if not exist ".env" (
    echo [4/4] .env dosyasi bulunamadi, .env.example kopyalaniyor...
    copy .env.example .env >nul
    echo.
    echo UYARI: .env dosyasini acip LLM_PROVIDER ve ilgili ayarlari kontrol et.
    echo Not Defteri ile simdi acmak icin: notepad .env
    echo.
    pause
) else (
    echo [4/4] .env dosyasi mevcut.
)

echo.
echo ============================================
echo   Uygulama baslatiliyor, tarayici acilacak...
echo   Kapatmak icin bu pencerede CTRL+C basip Y yaz.
echo ============================================
echo.

"%VENV_PY%" -m streamlit run app.py

pause
