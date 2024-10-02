from sympy import symbols, And, Or, Equivalent, satisfiable
from generate_test import generate
from pl_to_nl import parse_equivalent
from tthelper import get_truth_table, get_solution
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

symbols_list, statements = [], []

@app.get("/generate_puzzle")
def get():
    global symbols_list, statements
    # Recrusively generate statements, until we get a valid solution
    while True:
        symbols_list, statements = generate(num_symbols=10)
        if get_solution(statements, check=True):
            return {"statements": parse_equivalent(statements)}

@app.get("/solution")
def get():
    global statements    
    if dct is False:
        return {"solution": "No solution"}
    else:
        return {"solution": get_solution(statements)}

@app.get("/truth_table")
def get():
    global symbols_list, statements
    truth_table = get_truth_table(statements, symbols_list)
    return {"truth_table": truth_table}

# Statement : (Propositional Logic, Answer(Is A a knight or knave))
dct = {
    "A says A is knave": ("PARADOX", "No soln"),
    "A says A is knight": ("A → A", "AMBIGUOUS: If A is knight, statement is true. If A is knave, statement is false"),
    "A says B is knave": ("A → ¬B", "AMBIGUOUS: IF A is knight, B is knave. If A is knave B is knight"),
    "A says B is knight": ("A → B", "AMBIGUOUS: IF A is knight, B is knight. If A is knave B is knave"),
    "A says they are both knaves": ("A → (¬A ∧ ¬B)", "A is knave and B is knight"),
    "A says they are both knights": ("A → (A ∧ B)", "AMBIGUOUS: IF A is knight, B is knight. If A is knave B is knave"),
}