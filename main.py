from modules.rpn_calculator_console.rpn_calculator import *

from fastapi import FastAPI
from datetime import datetime

app = FastAPI()


@app.get("/")
def welcome():
    return {"message": "Hello, please go to http://127.0.0.1:8000/rpn/{equation} where 'equation' is a valid RPN equation that you want to compute."}

@app.get("/rpn/{tokens}")
def compute_rpn(tokens: str):
    '''
    Returns the reverse polish notation equation in infix notation.

    Parameters:
        tokens (str): A rpn equation
    Returns:
        result (dict): Dictionnary representing the json response expected
    '''
    # Get result and infix equation equivalent
    result = rpn_compute(tokens)
    infix = rpn_to_infix(tokens)
    # Get current date_time
    now = datetime.now()
    date_time = now.strftime("%m/%d/%Y %H:%M:%S")

    return {"date_time": date_time, "rpn": tokens, "infix": infix, "result": result}

