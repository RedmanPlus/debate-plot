import pandas as pd

def file_unpack_csv(f):
	with open('filename.csv', 'w') as destination:
		for chunk in f.chunks():
			destination.write(chunk)