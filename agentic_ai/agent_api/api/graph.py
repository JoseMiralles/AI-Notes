from pydantic import BaseModel, Field
from typing import List, TypedDict
from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph import StateGraph, END
from IPython.display import Image, display
from rich import print as rprint
from chains.chain_generate_questions import get_generate_questions_chain
from chains.chain_questions_corrector import get_questions_corrector_chain
from functions import execute_query, fill_sql_template, load_chinook_schema, load_template_fields, build_tree

class QuestionSQLPair(BaseModel):
    question: str = Field(description="A synthetic user question about the data.")
    sql_query: str = Field(description="A valid SQL query to answer the question.")

class QuestionBatch(BaseModel):
    items: List[QuestionSQLPair] = Field(description="A list of question-query pairs")

class GraphState(TypedDict):
    schema: str
    questions: List[QuestionSQLPair]
    errors: List[str]
    iterations: int
    target_table: str
    question_number: int
    template_fields: str

questions_corrector_chain = get_generate_questions_chain(QuestionBatch)

def generate_questions(state: GraphState):
    
    print("---GENERATING QUESTIONS---")

    result = questions_corrector_chain.invoke({
    "template_fields": state["template_fields"],
    "schema": state["schema"],
    "target_table": state["target_table"],
    "question_number": state["question_number"]
    })

    return {
        "questions": result.items,
        "iterations": 0,
        "errors": []
    }

def validate_queries(state: GraphState):

    print("---VLIDATING QUERIES---")
    questions = state["questions"]
    errors = []

    for i, item in enumerate(questions):
        try:
            converted_sql_query = fill_sql_template(item.sql_query)
            query_res = execute_query(converted_sql_query, "./data/Chinook_Sqlite.sqlite")
            errors.append(None)
        except Exception as e:
            errors.append(f"Query {i+1} Failed: {str(e)}")
    
    return {"errors": errors}

corrector_chain = get_questions_corrector_chain(QuestionBatch)

def correct_queries(state: GraphState):
    
    print (f"---CORRECTING ERRORS (Iteration {state['iterations'] + 1})---")

    schema = state["schema"]
    questions = state["questions"]
    errors = state["errors"]

    new_questions = list(questions)

    for i, error in enumerate(errors):
        if error:
            print(f"Fixing Question {i+1}...")
            
            fixed_pair = corrector_chain.invoke({
                "schema": schema,
                "question": questions[i].question,
                "spl": questions[i].spl_query,
                "error": error
            })
            
            new_questions[i] = fixed_pair

    return {
        "questions": new_questions,
        "iterations": state["iterations"] + 1,
        "errors": []
    }

def decide_next_step(state: GraphState):
    if state["errors"] and state["iterations"] < 3:
        return "correct"
    return "end"

workflow = StateGraph(GraphState)

workflow.add_node("generate", generate_questions)
workflow.add_node("validate", validate_queries)
workflow.add_node("correct", correct_queries)

workflow.set_entry_point("generate")
workflow.add_edge("generate", "validate")
workflow.add_conditional_edges("validate", decide_next_step, {"correct": "correct", "end": END})
workflow.add_edge("correct", "validate")

app = workflow.compile()

inputs = {
    "schema": load_chinook_schema(db_path="./data/Chinook_Sqlite.sqlite"),
    "questions": [],
    "errors": [],
    "iterations": 3,
    "target_table": "employees",
    "question_number": 5,
    "template_fields": load_template_fields()
}

final_state = app.invoke(inputs)
