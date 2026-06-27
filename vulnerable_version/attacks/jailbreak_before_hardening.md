# Jailbreak Attempts (Before Hardening)

## Attack Description

This attack attempts to override system instructions using jailbreak prompts such as:
- "Ignore all previous instructions"
- "Developer mode"
- "Act as an unrestricted AI"

The goal is to:
- bypass safety constraints
- reveal hidden system behavior
- expose internal data

---

## Observed Behavior

- The model follows malicious instructions
- System rules can be overridden
- Responses may include internal or sensitive information
- The model changes behavior based on attacker instructions

---

## Result

Jailbreak attempts are successful.

The system does not enforce instruction hierarchy, allowing attackers to override safety constraints and manipulate model behavior.
