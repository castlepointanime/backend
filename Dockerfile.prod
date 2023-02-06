FROM python:3.10-slim-bullseye

# copy the requirements file into the image
COPY requirements.txt .

# install the dependencies and packages in the requirements file
RUN pip install -r requirements.txt

# copy all content from the local file to the image
COPY . /app
 
# switch working directory
WORKDIR /app

# run the container with gunicorn (production ready) on port 3001 with hot reloading
CMD gunicorn app:app -w 2 --reload --threads 2 -b 0.0.0.0:3001