from langchain_core.prompts import ChatPromptTemplate
from llm import llm

corrector_prompt = ChatPromptTemplate.from_messages([
    ("system", """You are SQL Debugger.
    Your job is to fix an invalid SQL query based on an error message.
    
    1. Analyze the Schema and the Error.
    2. Rewrite the SQL query to fix the mistake.
    3. Keep the original User Question (unless it was nonsensical).
    """),
    ("human", """
    Schema: {schema}
    Original Question: {question}
    Bad SQL: {sql}
    Error Message: {error}
    
    Return the fixed Question/SQL pair.
    """),
])


def get_questions_corrector_chain(QuestionBatchClass):

    structured_llm = llm.with_structured_output(QuestionBatchClass)
    return corrector_prompt | structured_llm