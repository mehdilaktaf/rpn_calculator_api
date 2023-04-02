import csv
import settings
from io import StringIO
from datetime import datetime
from pymongo import MongoClient
from fastapi import FastAPI, Response
from modules.rpn_calculator_console.rpn_calculator import *



app = FastAPI()


# Use the URI in your code to connect to the MongoDB database
client = MongoClient(settings.MONGODB_URI)

# Get the collection from mongo connection
db =  client[settings.MONGODB_DB]
rpn_collection = db[settings.MONGODB_COLLECTION]

@app.get("/")
def welcome():
    return {"message": "Hello, please use curl or Postman to go to http://127.0.0.1:8000/rpn/ and enter a valid RPN equation that you want to compute. The request body should look like this : {'tokens' : 'equation'}"}

# This is changed from a get to a post request to avoid division bug in url
@app.post("/rpn/")
def compute_rpn(tokens: dict):
    '''
    Returns the reverse polish notation equation in infix notation.

    Parameters:
        tokens (dict): A dictionnary with "tokens" has the key and the equation as the value
    Returns:
        result (dict): Dictionnary representing the json response expected
    '''
    # Get result and infix equation equivalent
    result = rpn_compute(tokens["tokens"])
    infix = rpn_to_infix(tokens["tokens"])
    # Get current date_time
    now = datetime.now()
    date_time = now.strftime("%m/%d/%Y %H:%M:%S")

    # Inserting data into MongoDB
    rpn_collection.insert_one({"date_time": date_time, "rpn": tokens["tokens"], "infix": infix, "result": result})

    return {"date_time": date_time, "rpn": tokens["tokens"], "infix": infix, "result": result}


@app.get("/operations")
def get_operations():
    '''
    Returns all operations in the database as CSV format.

    Returns:
        response (Response): Response object with csv data and headers
    '''
    # Get all operations from mongo
    operations = rpn_collection.find()
    # Create a StringIO object to write the CSV data to
    csv_output = StringIO()
    # Create a csv writer object
    writer = csv.writer(csv_output)
    # Write the headers
    writer.writerow(['date_time', 'rpn', 'infix', 'result'])
    # Loop through the operations and write each row to the csv
    for op in operations:
        writer.writerow([op['date_time'], op['rpn'], op['infix'], op['result']])
    # Get the csv data as a string
    csv_data = csv_output.getvalue()
    # Set the content type header
    headers = {
        'Content-Type': 'text/csv',
        'Content-Disposition': 'attachment; filename="operations.csv"'
    }
    # Return the response object with the csv data and headers
    return Response(content=csv_data, headers=headers)