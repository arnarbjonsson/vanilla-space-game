@echo off
echo Starting Vanilla Space Game...
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not available. Please make sure Python 3.11 is installed and in PATH.
    echo You may need to restart your terminal after setting up pyenv.
    pause
    exit /b 1
)

echo Python found: 
python --version

REM Check if pipenv is available
python -m pipenv --version >nul 2>&1
if errorlevel 1 (
    echo Pipenv not found. Installing pipenv...
    python -m pip install pipenv
    if errorlevel 1 (
        echo ERROR: Failed to install pipenv
        pause
        exit /b 1
    )
    echo Pipenv installed successfully!
) else (
    echo Pipenv is already installed
)

REM Check if virtual environment exists, if not create it
if not exist "Pipfile" (
    echo Creating new Pipfile...
    python -m pipenv --python python
)

REM Install dependencies
echo Installing/updating dependencies...
python -m pipenv install

REM Run the game
echo.
echo Starting the game...
echo Use WASD or Arrow keys to move, Space to shoot, ESC to pause
echo Close the game window to exit
echo.

python -m pipenv run python main.py

echo.
echo Game ended. Press any key to close...
pause >nul 