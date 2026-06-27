## After Hardening

- Direct prompt injection attempts are ignored by the system
- Malicious instructions like "ignore all instructions" are not executed
- Sensitive tool invocation is blocked even when explicitly requested
- No API calls are made for unauthorized or unsafe requests
- No sensitive data (e.g., salaries, internal records) is exposed
- System falls back to a safe response when the request is not allowed

## Result

The combined attack (prompt injection + tool misuse) no longer succeeds.  
The system correctly enforces instruction hierarchy and tool authorization, preventing both instruction override and data exfiltration.
