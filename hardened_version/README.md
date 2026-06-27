1. Prompt hardening
Tell the model clearly that retrieved docs are untrusted data, not instructions.
2. Retrieval hardening
Detect and filter suspicious chunks before they reach the model.
3. Tool hardening
Stop sensitive tools from being callable just because the user asked.
4. Output hardening
Prevent the assistant from leaking sensitive data even if something slips through.