@echo off
call .\.venv\Scripts\activate
:restart
echo Starting Python program...
python C:\Users\jiehuiliu\Desktop\THSTraderPC\main.py
if %ERRORLEVEL% neq 0 (
    echo Error detected, restarting...
    timeout /t 1
    goto restart
)