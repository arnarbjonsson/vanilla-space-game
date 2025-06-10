@echo off
echo Starting Vanilla Space Game...
echo.

echo Installing dependencies...
call python -m pipenv install
if errorlevel 1 (
    echo Failed to install dependencies!
    goto :end
)

echo Starting game...
call python -m pipenv run python main.py
if errorlevel 1 (
    echo Game failed to start!
    goto :end
)

:end
echo.
echo Game ended. Press any key to close...
pause >nul 