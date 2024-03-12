FROM python:3.10
# EXPOSE 5000
WORKDIR /app
RUN pip install --no-cache-dir --upgrade pipenv
COPY Pipfile /app
RUN pipenv install
COPY . /app
#CMD ["pipenv", "run", "flask", "run", "--host", "0.0.0.0"]
CMD ["gunicorn", "--bind", "0.0.0.0:80", "app:create_app()"]