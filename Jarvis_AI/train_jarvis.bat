@echo off
echo ==================================================
echo       J.A.R.V.I.S. AI MODEL CUSTOMIZATION
echo ==================================================
echo.
echo Phase 1: Pulling base model (phi3:mini)...
ollama pull phi3:mini

echo.
echo Phase 2: Creating custom JARVIS personality...
ollama create jarvis -f Modelfile

echo.
echo ==================================================
echo       SUCCESS! JARVIS MODEL IS READY.
echo ==================================================
echo.
pause
