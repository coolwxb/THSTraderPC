@echo off
:restart
echo Starting Python program...
python E:\THSTraderPC\thread.py
if %ERRORLEVEL% neq 0 (
    echo Error detected, restarting...
    timeout /t 1
    goto restart
)