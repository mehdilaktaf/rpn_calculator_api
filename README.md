# Getting started with RPN Calculator API

This project was created using [python](https://www.python.org/), [fastapi](https://github.com/tiangolo/fastapi) and [mongodb](https://www.mongodb.com/fr-fr).
<br>

## What is RPN ?

**RPN** stands for **"Reverse Polish Notation"** which is a notation for equation that does not use parenthesis, it is also known as ***postfix notation***. 

This is an example of an equation using the **Reverse Polish Notation** : 
### **`1 2 + 3 /`**

What we normally use to write this equation is called the ***infix notation***, it looks like this :
### **`((1 + 2) / 3)`**

<br>

## What can you use this calculator for?

The goal of this API is to take in a RPN equation and compute it to give a result.
You will also see the current time when calling the API, infix notation and of course the result.

<br>

## Requirements
<br>
Now that I explained the RPN and goal of this application, here are the steps to follow to use this API:
<br>

* First, you will need to install all the requirements by lauching the following command:

    ### **`pip install -r requirements.txt`**
<br>

* Then you need to replace **`<database>`** and **`<uri>`** inside **`docker-compose.yml`**.
<br><br>

* /!\ You also need to add a  **`settings.py`** file in the project root and add the following variables: /!\ 

    ###  `MONGODB_URI = "your mongo db uri"`
    ###  `MONGODB_DB =  "your database"`
    ###  `MONGODB_COLLECTION = "your collection"`
<br>

* Once this is done, you should be able to launch the server using either:

    ### `uvicorn main:app --reload`

    ## or

    ### `docker-compose up`
 <br>

## Usage

Finally, you can access the launched API documentation to see all the routes you can use:

### `http://127.0.0.1/docs`