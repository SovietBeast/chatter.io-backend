FROM python:3.10.7
EXPOSE 8080
WORKDIR /app
COPY "./src/requirements.txt" /app
RUN pip install -r requirements.txt
COPY "./src/" /app
RUN ls /app
RUN echo AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
CMD ["uvicorn", "main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "8080"]

