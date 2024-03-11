FROM python:3.10
EXPOSE 5000
WORKDIR /app
RUN pip install pipenv
COPY Pipfile /app
RUN pipenv install
COPY . /app
CMD ["pipenv", "run", "flask", "run", "--host", "0.0.0.0"]
