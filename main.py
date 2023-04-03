from typing import Annotated, List, Dict
import csv

from pydantic import BaseModel, validator
import settings
from io import StringIO
from datetime import datetime
from pymongo import MongoClient
from fastapi import Body, FastAPI, HTTPException, Response
from fastapi.responses import RedirectResponse
from modules.rpn_calculator_console.rpn_calculator import *


# Initiate application
app = FastAPI()

# Create custom schema for operation objects
class Operation(BaseModel):
    date_time: datetime
    rpn: str
    infix: str
    result: int

    @validator('date_time', pre=True)
    def parse_date_time(cls, value):
        if isinstance(value, str):
            return datetime.strptime(value, '%m/%d/%Y %H:%M:%S')
        return value
    
    class Config:
        schema_extra = {
            "example": {
                "date_time": "01/01/2022 10:00:00",
                "rpn": "2 2 +",
                "infix": "2 + 2",
                "result": 4
            }
        }

# Use the URI in your code to connect to the MongoDB database
client = MongoClient(settings.MONGODB_URI)

# Get the collection from mongo connection
db =  client[settings.MONGODB_DB]
rpn_collection = db[settings.MONGODB_COLLECTION]


@app.get("/")
def root():
    '''
    Redirects user to "/docs" swagger documentation.
    '''
    return RedirectResponse(url="/docs")

# This is changed from a get to a post request to avoid division bug in url
@app.post("/rpn", description="Returns the reverse polish notation equation in infix notation.", response_model=Operation)
def compute_rpn(tokens: Annotated[Dict[str,str], Body(example={"tokens": "2 2 +"})]):
    '''
    Parameters:
        - tokens (Dict[str, str]): A dictionnary with "tokens" has the key and the equation as the value
    Returns:
        - (Operation): The operation object created and added to the database.
    '''
    # Get result and infix equation equivalent
    try:
        result = rpn_compute(tokens["tokens"])
        infix = rpn_to_infix(tokens["tokens"])
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    
    # Get current date_time
    now = datetime.now()
    date_time = now.strftime("%m/%d/%Y %H:%M:%S")

    # Create new operation to add it to mongodb collection
    op = Operation(date_time=date_time, rpn=tokens["tokens"], infix=infix, result=result)

    # Inserting data into MongoDB
    rpn_collection.insert_one(op.dict())

    # Return the operation created
    return op.dict()


@app.get("/operations", description="Returns all operations in the database as JSON response.", response_model=List[Operation])
def get_operations():
    '''
    Returns:
        response (list[Operations]): List of all Operations in database.
    '''
    # Get all operations from mongo and sort them by date_time in descending order
    operations = []
    for op in rpn_collection.find().sort("date_time", -1):
        operation = Operation(**op)
        operations.append(operation)
    # Return the response object with the csv data and headers
    return operations


@app.get("/operations_csv", description="Returns all operations in the database as CSV format.", response_class=Response)
def get_operations_as_csv():
    '''
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

