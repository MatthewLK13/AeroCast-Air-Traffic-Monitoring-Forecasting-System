@echo off
chcp 65001 >nul
TITLE He Thong Giam Sat Khong Luu - Trinh Khoi Dong

echo ========================================================
echo   AEROCAST: HE THONG GIAM SAT VA DU BAO KHONG LUU (VAA)
echo   [ Created by Luong Minh Khoi (c) 2026 ]
echo ========================================================
echo.

:: 1. Kiem tra xem Python da duoc cai dat chua
python --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo [CANH BAO] May tinh cua ban chua co Python!
    echo Dang tu dong tai trinh cai dat Python ve may...
    powershell -Command "Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.11.8/python-3.11.8-amd64.exe' -OutFile 'python-installer.exe'"
    
    echo Dang cai dat Python - Vui long cho khoang 1-2 phut, khong tat cua so nay...
    start /wait python-installer.exe /quiet InstallAllUsers=0 PrependPath=1 Include_test=0
    del python-installer.exe
    
    echo.
    echo =========================================================================
    echo [QUAN TRONG] Cai dat Python thanh cong! 
    echo Ban vui long TAT CUA SO NAY va NHAP DUP vao run.bat 1 lan nua nhe!
    echo =========================================================================
    pause
    exit
)

echo [OK] Python da san sang.
echo.
echo Dang kiem tra va tai cac thanh phan AI (Neu ban chay lan dau se mat vai phut)...

IF NOT EXIST "venv\Scripts\python.exe" (
    echo [INFO] Dang tao moi truong ao Virtual Environment de tranh loi xung dot tren may nay...
    python -m venv venv
)
call venv\Scripts\activate.bat

python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip install typing-extensions

echo.
echo ========================================================
echo   BAT DAU KHOI DONG HE THONG!
echo ========================================================
echo.
echo [1/2] Dang khoi dong cong cu quet Radar ngam...
start cmd /k "TITLE Radar Collector & call venv\Scripts\activate.bat & python collector2.py"

echo [2/2] Dang bat Giao dien dieu khien (Dashboard)...
python -m streamlit run app.py

pause
