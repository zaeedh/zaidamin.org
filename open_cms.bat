@echo off
title Academic CMS & Editorial Studio - Dr. Zaid Amin
cls
echo =====================================================================
echo    ACADEMIC CMS & EDITORIAL STUDIO - DR. ZAID AMIN
echo =====================================================================
echo.
echo Checking preview server status on port 8000...
netstat -ano | findstr :8000 >nul 2>&1
if %errorlevel% neq 0 (
    echo Starting background server via serve.py...
    start /b python serve.py
    timeout /t 2 /nobreak >nul
) else (
    echo Academic Preview Server is already active on port 8000.
)

echo.
echo Opening CMS Studio in your browser:
echo - Local URL:  http://localhost:8000/cms.html
echo - Online URL: https://zaidamin.org/cms.html
echo.
start http://localhost:8000/cms.html
echo CMS launched successfully. You can close this window.
timeout /t 5

