# streaming-05-smart-smoker

## Description 
This repo is for the use of sending data from smoker-temps.csv to a consumer that will take this data and use it in order to detect changes in tempatures in order to stimulate a "smart smoker". This repo only contains the producer and the data. 

## Important Variables 
I will list below important vaiables as using this code without these vairables set correctly on the consumerside will fail. 

QUEUE1 = "SmokerTemps"
QUEUE2 = "FoodATemps"
QUEUE3 = "FoddBTemps"

## How to Use 
1. We need to install a python virtual enviroment 
    a. python -m venv .venv
    b. I used this command 
2. Run the script 
    a. .venv\Scripts\activate
3. Insall Pika using Pip
4. Run the python emitter.py 
5. (Optinal) After the consumer is made run step 4 after running the consumers.  

## How the Code works
I used the same tempalte as the HW 4 Emitter. The main changes made was to the how data was read in and a bit was changed to where messages were sent out. I tried to keep everthing modular as this would make it so I would have less to change. To read in the data I just split the data up by commas and append each data point to their resctive list. I then looped through the list to send the data and check if there is anyhting to send then send it. 

## Image of code running 
![alt text](image.png)
