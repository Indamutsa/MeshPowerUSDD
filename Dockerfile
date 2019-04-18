#Pulling the image from my docker hub
FROM python:3

# Copy the requirements file in order to install
# Python dependencies
COPY requirements.txt .

# Install Python dependencies
RUN pip install -r requirements.txt

#Add the local files in the image
ADD . /home/app/

#Our working directory
WORKDIR /home/app/

#We expose this port to be used to access our docker image
EXPOSE 6200

#The executable, together python3 app.py will run the file
ENTRYPOINT ["python3", "run.py"]
