from langchain_community.llms import Ollama
from app.rag import retrieve_docs
from app.prompts import VULNERABLE_RAG_PROMPT
from app.logger import log_interaction
from app.tools import calculator, mock_sensitive_api


llm = Ollama(model="llama3")


def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


def maybe_use_tool(question: str):
    lower_q = question.lower()

    if "calculate:" in lower_q:
        expr = question.split("calculate:", 1)[1].strip()
        return calculator(expr)

    if "call api" in lower_q or "show employee data" in lower_q:
        return mock_sensitive_api()

    return None


def ask_question(business_id: str, question: str):
    docs = retrieve_docs(business_id, question, k=3)
    context = format_docs(docs)

    tool_result = maybe_use_tool(question)

    prompt = VULNERABLE_RAG_PROMPT.format(
        context=context,
        question=question
    )

    if tool_result:
        prompt += f"\n\nTool result:\n{tool_result}\n"

    answer = llm.invoke(prompt)

    log_data = {
        "business_id": business_id,
        "question": question,
        "retrieved_chunks": [
            {
                "content": d.page_content,
                "metadata": d.metadata
            }
            for d in docs
        ],
        "tool_result": tool_result,
        "final_prompt": prompt,
        "answer": answer,
    }

    log_file = log_interaction(log_data)

    return {
        "answer": answer,
        "tool_result": tool_result,
        "log_file": log_file,
    }
