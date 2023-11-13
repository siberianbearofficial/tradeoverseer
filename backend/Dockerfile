FROM python:3.10-slim

WORKDIR /backend

COPY ./torch ./torch

COPY ./requirements.txt .

RUN python3 -m pip download --cache-dir ./tmp/pipcache -r requirements.txt

RUN python3 -m pip install --cache-dir ./tmp/pipcache -r requirements.txt

COPY . .

EXPOSE 8001

CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8001", "--root-path", "/api"]
