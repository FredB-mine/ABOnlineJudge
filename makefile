python3 = /Library/Frameworks/Python.framework/Versions/3.7/bin/python3

default:
	@$(python3) makeProject.py

push: default
	@$(python3) Git_Uploader.py
