FROM python:3.6
RUN mkdir /code
COPY . /code/
WORKDIR /code
RUN pip install pipenv
RUN pipenv install --system --deploy
CMD nameko run --config nameko_config.yml services
