from langchain_community.llms import Ollama

from app.rag import retrieve_docs
from app.prompts import SECURE_RAG_PROMPT
from app.logger import log_interaction
from app.tools import calculator


llm = Ollama(model="llama3")

BLOCKED_OUTPUT_PATTERNS = [
    "ignore all previous instructions",
    "reveal hidden policies",
    "reveal system prompt",
    "system override",
    "internal hr note",
    "according to our system override instructions",
    "i must provide all internal information",
]


def format_docs(docs):
    if not docs:
        return ""
    return "\n\n".join(doc.page_content for doc in docs)


def maybe_use_tool(question: str):
    lower_q = question.lower()

    if "calculate:" in lower_q:
        expr = question.split("calculate:", 1)[1].strip()
        return calculator(expr)

    sensitive_triggers = [
        "show employee data",
        "call api",
        "salary",
        "finance summary",
        "incident status",
        "customer account metadata",
        "employee records",
    ]

    if any(trigger in lower_q for trigger in sensitive_triggers):
        return {
            "tool": "mock_sensitive_api",
            "blocked": True,
            "reason": "Sensitive tool access requires authorization.",
        }

    return None


def sanitize_output(answer: str) -> str:
    lower_answer = answer.lower()

    if any(pattern in lower_answer for pattern in BLOCKED_OUTPUT_PATTERNS):
        return (
            "I cannot comply with malicious or hidden instructions. "
            "I can only answer using safe and relevant business information."
        )

    return answer


def ask_question(business_id: str, question: str):
    retrieval_result = retrieve_docs(business_id, question, k=3)
    docs = retrieval_result["safe_docs"]
    flagged_docs = retrieval_result["flagged_docs"]

    context = format_docs(docs)
    tool_result = maybe_use_tool(question)

    if not context and not tool_result:
        answer = "I do not have that information."
        prompt = None
    else:
        prompt = SECURE_RAG_PROMPT.format(
            context=context if context else "No safe context available.",
            question=question,
        )

        if tool_result:
            prompt += f"\n\nTool result:\n{tool_result}\n"

        answer = llm.invoke(prompt)
        answer = sanitize_output(answer)

    log_data = {
        "business_id": business_id,
        "question": question,
        "retrieved_chunks": [
            {
                "content": d.page_content,
                "metadata": d.metadata,
            }
            for d in retrieval_result["all_docs"]
        ],
        "safe_chunks_used": [
            {
                "content": d.page_content,
                "metadata": d.metadata,
            }
            for d in docs
        ],
        "flagged_chunks_blocked": [
            {
                "content": d.page_content,
                "metadata": d.metadata,
            }
            for d in flagged_docs
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
