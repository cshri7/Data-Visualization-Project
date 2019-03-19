Steps to run:


"--------------Data Processing--------------"

1. combine_data.py : requires all the WebMd dataset files in the same folder.

	* command to run: python combine_data.py
	* outcome : combines all the the data files into a single csv 'combined.csv'

2. create_data_json.py

	* command to run: python create_data_json.py
	* outcome : creates different text files, functions required for visualization.


"--------------Application--------------"

* Installing requirements: requires python == 3.6, pip3 
	pip install -r requirements.txt
	
* running the project:
	python manage.py runserver
	
	The website will be hosted on 127.0.0.1:8000

