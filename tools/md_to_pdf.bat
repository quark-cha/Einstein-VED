@echo off
set G_MESSAGES_DEBUG=
set GIO_USE_VFS=local

python "%~dp0md_to_pdf.py" %* > nul 
pause

