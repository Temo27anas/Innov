FROM python:3.9.17-slim-bullseye

RUN pip install --upgrade pip

COPY ./requirements.txt .

RUN pip install torch==2.0.1+cpu -f https://download.pytorch.org/whl/torch_stable.html

RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /api

COPY ./api /api

RUN python -m nltk.downloader punkt

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5607"]