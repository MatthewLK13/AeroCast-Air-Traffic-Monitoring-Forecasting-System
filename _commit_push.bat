@echo off
chcp 65001 >nul
TITLE Commit and push AeroCast

echo ========================================================
echo   COMMIT + PUSH - AeroCast-VAA-System
echo ========================================================
echo.

REM Check we're in repo root
IF NOT EXIST ".git" (
    echo [LOI] Khong tim thay .git — hay chay tu thu muc goc repo!
    echo Vi du: cd "C:\Users\khoilm\Downloads\project\AeroCast-VAA-System"
    pause
    exit /b 1
)

echo [1/6] Trang thai hien tai...
git status --short
echo.

echo [2/6] Cac remote da cau hinh...
git remote -v
echo.

echo [3/6] Branch hien tai...
git branch --show-current
echo.

echo [4/6] Them tat ca file moi + thay doi (bo qua file trong .gitignore)...
git add -A
echo.

echo [5/6] Commit...
git commit -m "docs: rewrite chuong3+4 with A-Z explanations, fix packaging, add DB fallback

- Rewrite chuong3.docx + chuong4.docx with A-Z explanations for 28+ technical terms
  (vector, sin/cos, knots, naive forecast, ADS-B, FIR, etc.)
- Apply teacher feedback: workload/intensity definition, training log, waypoints
- Add get_db_live_state() helper in app.py for offline fallback
- Render_radar() now reads DB when FlightRadarAPI is empty/throws
- Render_ai_panel() uses DB latest row when session_state is 0
- Fix run.bat cmd syntax corruption (BOM, >nul, backslash)
- Pin all 13 packages in requirements.txt with == versions
- Add .streamlit/config.toml dark theme
- Cleanup: remove 17 temp scripts, ckpt files, duplicate docx, log files
- Add document/README.md describing folder structure"

IF %ERRORLEVEL% NEQ 0 (
    echo.
    echo [LOI] Commit that bai! Co the chua co gi de commit.
    pause
    exit /b 1
)
echo.

echo [6/6] Push len remote...
git push origin HEAD

IF %ERRORLEVEL% NEQ 0 (
    echo.
    echo [LOI] Push that bai!
    echo Neu loi 'no upstream branch', chay:
    echo     git push -u origin HEAD
    echo Neu loi authentication, dam bao da dang nhap GitHub.
    pause
    exit /b 1
)

echo.
echo ========================================================
echo   THANH CONG!
echo ========================================================
pause
