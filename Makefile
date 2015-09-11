install:
	pip install -r requirements/dev.txt
	bower install

setup:
	make install
	python manage.py db upgrade
	python manage.py make_normal_user

serve:
	python manage.py db upgrade
