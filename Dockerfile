FROM python:3.10.9

WORKDIR /DCSStatsDataProvider

COPY ./DCSStatsDataProvider/requirements.txt /DCSStatsDataProvider/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /DCSStatsDataProvider/requirements.txt

COPY ./DCSStatsDataProvider /DCSStatsDataProvider/

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]