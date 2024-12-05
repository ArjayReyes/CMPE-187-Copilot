@echo off
call venv\Scripts\activate
python copilot.py
python analysis.py
call deactivate