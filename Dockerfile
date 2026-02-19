FROM python:3.11-slim

# set workdir
WORKDIR /app

# install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# copy project
COPY . /app

# expose port
EXPOSE 8000

# run
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
