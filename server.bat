@echo off
REM Check if Python is installed
python --version
if %errorlevel% neq 0 (
echo Python is not installed or not added to PATH. Please install Python from https://python.org
echo Make sure to add Python to your PATH during the installation.
pause
exit /b 1
)
 
REM Install required packages
pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org pyautogui
if %errorlevel% neq 0 (
echo Failed to install pyautogui. Please ensure you have pip installed and try again.
pause
exit /b 1
)
 
@REM REM Download the server script
@REM curl -O https://raw.githubusercontent.com/sumit91221/Server_Script_Auto_Typing/main/server.py --ssl-no-revoke
@REM if %errorlevel% neq 0 (
@REM echo Failed to download the server script. Please check your internet connection and try again.
@REM pause
@REM exit /b 1
@REM )
 
REM Run the server script
python server.py
if %errorlevel% neq 0 (
echo Failed to run the server script. Please ensure all dependencies are installed and try again.
pause
exit /b 1
)
 
echo Installation complete and server script is running.
pause