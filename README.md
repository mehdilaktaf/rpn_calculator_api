# Getting started with RPN Calculator API

This project was created using python and fastapi.

## What is RPN ?

**RPN** stands for **"Reverse Polish Notation"** which is a notation for equation that does not use parenthesis, it is also known as ***postfix notation***. 

This is an example of an equation using the **Reverse Polish Notation** : 
### **`1 2 + 3 /`**

What we normally use to write this equation is called the ***infix notation***, it looks like this :
### **`((1 + 2) / 3)`**

## What can you use this calculator for?

The goal of this API is to take in a RPN equation and compute it to give a result.
You will also see the current time when calling the API, infix notation and of course the result.

## Usage

Now that I explained the RPN and goal of this application, here is how to use it:

*First you will need to install all the requirements by lauching the following command:*

### **`pip install requirements.txt`**

*Once this is done, you should be able to launche the uvicorn server using the next command line.*

### **`uvicorn main:app --reload`**

*Finally you can access the launched API to enter an equation and get the result by going on this address: *


### **`http://127.0.0.1:8000/rpn/{equation}`**

*Where {equation} is a valid RPN equation.*