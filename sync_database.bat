@echo off
echo ========================================
echo   ENSPD LearnAI - Database Sync
echo ========================================
echo.

cd backend

echo [1/2] Exporting local database...
echo.
python export_data.py
echo.

if not exist database_export.json (
    echo ERROR: Export failed!
    pause
    exit /b 1
)

echo [2/2] Importing to production server...
echo.
python import_data.py
echo.

echo ========================================
echo   Synchronization Complete!
echo ========================================
echo.
pause
