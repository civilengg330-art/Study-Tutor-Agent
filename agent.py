import os

from dotenv import load_dotenv
from crewai import Agent, Task, Crew, LLM

from tools import calculator
from memory import get_memory_text


# Load environment variables
load_dotenv()


def create_study_tutor():

    llm = LLM(
        model="groq/openai/gpt-oss-120b",
        api_key=os.getenv("GROQ_API_KEY"),
        temperature=0.3
    )

    tutor = Agent(
        role="Study Tutor",

        goal=(
            "Help students understand academic concepts clearly, "
            "answer questions accurately, simplify difficult topics, "
            "and create useful practice questions."
        ),

        backstory=(
            "You are a patient university study tutor. "
            "You explain difficult concepts step by step. "
            "You adapt explanations to the student's level. "
            "You use tools when calculations are required."
        ),

        llm=llm,

        tools=[
            calculator
        ],

        verbose=False
    )

    return tutor


def ask_tutor(question):

    tutor = create_study_tutor()

    previous_memory = get_memory_text()

    task = Task(
        description=f"""
        Answer the student's question.

        Student question:
        {question}

        Previous conversation:
        {previous_memory}

        Instructions:

        1. Answer clearly.
        2. Explain difficult concepts step by step.
        3. Use the Calculator tool when mathematical calculation is needed.
        4. Do not invent facts.
        5. If the student asks for an example, provide a simple example.
        6. Adapt the explanation to the student's apparent level.
        """,

        expected_output=(
            "A clear, accurate and student-friendly answer."
        ),

        agent=tutor
    )

    crew = Crew(
        agents=[tutor],
        tasks=[task],
        verbose=False
    )

    result = crew.kickoff()

    return str(result)
