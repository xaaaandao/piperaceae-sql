run:
	rm -rf main.py
	jupyter nbconvert --to script main.ipynb   
	nohup python main.py &
