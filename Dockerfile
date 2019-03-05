#Pulling the image from my docker hub
FROM indamutsa/ussd-image:latest

#Add the local files in the image
ADD . /home/app/

#Our working directory
WORKDIR /home/app/

#We expose this port to be used to access our docker image
EXPOSE 6200

#The executable, together python3 app.py will run the file
ENTRYPOINT ["python3", "run.py"]
