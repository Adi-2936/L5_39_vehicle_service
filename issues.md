# Static Analysis Findings and Fixes

The table records findings from the original `vehicle_service.py`. Line numbers refer to the original file before the fixes were applied.

| Issue | Type | Original line(s) | Description | Fix approach |
|---|---|---:|---|---|
| Shell command injection (`B602`) | Security - High | 61 | `subprocess.call()` built a shell command by concatenating the caller-provided folder and executed it with `shell=True`. A malicious folder value could execute another command. | Replaced the shell command with `shutil.copy2()` and constructed the destination with `pathlib.Path`. |
| MD5 warning (`B324`) | Security - High | 39 | Bandit treated MD5 as a weak security hash. In this program it creates a stable display identifier rather than protecting security-sensitive data. | Preserved the existing job-card value and made the non-security purpose explicit with `usedforsecurity=False`. |
| Hard-coded password (`B105`) | Security - Low | 8 | The source contained the password-like constant `ADMIN_PASSWORD`, which could expose a credential if it were used. | Removed the unused constant. A real credential would instead come from a protected secret store or environment configuration. |
| Mutable default argument (`W0102`) | Bug | 12 | The default `history=[]` object was reused across calls, so unrelated calls silently shared state. | Changed the default to `None` and created a new list inside the function. |
| Broad exception handler (`W0718`) | Reliability | 23 | Catching `Exception` could hide programming errors unrelated to a missing vehicle record. | Narrowed the handler to `KeyError`, the expected failure when a vehicle is absent. |
| Missing output encoding (`W1514`) | Portability | 50 | The JSON writer depended on the operating system's default text encoding. | Opened the output file explicitly with `encoding="utf-8"`. |
| Non-PEP 8 identifiers (`C0103`) | Maintainability | 12-59 | Function, parameter, and local variable names used camelCase, making the module inconsistent with Python conventions. | Renamed identifiers to snake_case and updated every call site. |
| Missing documentation (`C0114`, `C0116`) | Maintainability | 1, 12-64 | The module and its functions had no docstrings explaining their responsibilities. | Added a module docstring and concise function docstrings. |
| Spacing and line-length errors (`E225`, `E231`, `E302`, `E501`) | Style | 7, 43, 49, 77 | Flake8 found missing spaces, insufficient blank lines, and one line longer than 79 characters. | Reformatted the rate mapping, assignments, function spacing, and long print statement to conform to PEP 8. |

## Additional robustness improvements

- Added validation for empty vehicle numbers and unsupported service types so invalid bookings fail clearly instead of creating zero-cost records.
- Replaced the manual total and busiest-vehicle loops with direct, readable expressions.
- Added an `if __name__ == "__main__"` guard so importing the module does not run the demonstration or write a file.
- Retained the demonstration's observable output, including the existing job-card identifier.

## Verification summary

| Tool | Original result | Final result |
|---|---:|---:|
| Pylint | 4.66/10 | 10.00/10 |
| Bandit | 4 findings: 2 high, 2 low | 0 findings |
| Flake8 | 4 violations | 0 violations |
