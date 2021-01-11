@echo on

:loop
	remote-integrity --config sample.cfg
	timeout /t 60 /nobreak
goto loop