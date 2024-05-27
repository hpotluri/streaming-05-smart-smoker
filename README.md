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


