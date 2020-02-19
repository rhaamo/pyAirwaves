run:
	. ./venv/bin/activate; \
	./manage.py runserver

revision:
	alembic revision --autogenerate;

upgrade:
	alembic upgrade head

downgrade:
	alembic downgrade head
