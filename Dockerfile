FROM python:3.10.9

WORKDIR /DCSStats

COPY ./requirements.txt /DCSStats/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /DCSStats/requirements.txt

COPY ./ /DCSStats/

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]