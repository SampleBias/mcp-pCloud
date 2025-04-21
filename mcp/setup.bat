@echo off
REM Script to set up and run the pCloud MCP server on Windows

REM Check for Python 3
python --version 2>NUL
if %ERRORLEVEL% NEQ 0 (
    echo Python is required but not found. Please install Python and try again.
    exit /b 1
)

REM Create virtual environment if it doesn't exist
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Install required packages
echo Installing required packages...
pip install mcp "mcp[cli]" requests

REM Check if PCLOUD_ACCESS_TOKEN is set
if "%PCLOUD_ACCESS_TOKEN%"=="" (
    echo Warning: PCLOUD_ACCESS_TOKEN environment variable is not set.
    echo You will need to set this to use the MCP server.
    echo You can get a token by running: python src\get_pcloud_token.py

    REM Prompt to run the token script
    set /p GET_TOKEN="Do you want to get a pCloud access token now? (y/n): "
    if /i "%GET_TOKEN%"=="y" (
        REM Edit get_pcloud_token.py to set client ID and secret
        echo Please edit src\get_pcloud_token.py to set your CLIENT_ID and CLIENT_SECRET before continuing.
        pause
        
        REM Run the token script
        python src\get_pcloud_token.py
        
        REM If token file exists, offer to set it
        if exist src\pcloud_token.txt (
            for /f "tokens=3" %%a in ('findstr "Access Token:" src\pcloud_token.txt') do set TOKEN=%%a
            if not "%TOKEN%"=="" (
                set PCLOUD_ACCESS_TOKEN=%TOKEN%
                echo Access token set for this session.
                echo To set it permanently, run:
                echo setx PCLOUD_ACCESS_TOKEN "%TOKEN%"
            )
        )
    )
)

REM Offer to run the server
set /p START_SERVER="Do you want to start the MCP server now? (y/n): "
if /i "%START_SERVER%"=="y" (
    echo Starting the MCP server...
    cd src
    python -m mcp dev pcloud_mcp_server.py
) else (
    echo To start the server later, run:
    echo   venv\Scripts\activate.bat
    echo   cd src
    echo   python -m mcp dev pcloud_mcp_server.py
)

pause 