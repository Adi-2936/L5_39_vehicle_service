# Lab 5 Reflection

## 1. Which issues were the easiest to fix, and which were the hardest? Why?

The easiest issues were the PEP 8 formatting, naming, missing docstrings, and missing UTF-8 encoding because each warning pointed to a specific line and the intended correction was clear. The mutable default argument was also straightforward after recognizing that one list object was being reused across calls.

The hardest issue was the backup function. It combined user-controlled text with a shell command, so the fix had to remove the injection risk without losing the file-copying behavior. Replacing the command with `shutil.copy2()` and using `Path` objects made the operation safer and portable. The MD5 warning also required judgment because the hash is only a short, deterministic job-card identifier, not a password hash, signature, or security token.

## 2. Did the static analysis tools report any false positives? If so, describe one example.

Bandit's `B324` warning about MD5 was a contextual false positive. MD5 would be unsafe for password storage or other security-sensitive hashing, but this program uses it only to generate a repeatable eight-character display ID from a vehicle number. I kept the algorithm so the program's output stayed the same and passed `usedforsecurity=False` to document that purpose explicitly. This removed the warning without pretending that MD5 is secure.

## 3. How would you integrate static analysis tools into your actual software development workflow?

I would run Flake8 and Pylint in my editor or a pre-commit hook so style and maintainability problems are caught before a commit. I would run Bandit in continuous integration on every pull request and block merges for high-severity findings until they are fixed or reviewed with a documented reason. I would also save the tool configuration in the repository so local checks and CI use the same rules, and I would rerun tests after applying fixes because a clean static-analysis report does not prove that behavior is correct.

## 4. What tangible improvements did you observe in the code quality, readability, or potential robustness after applying the fixes?

Pylint improved from 4.66/10 to 10.00/10. Bandit's four findings, including two high-severity findings, dropped to zero, and Flake8's four violations also dropped to zero. The code now avoids shared state from a mutable default, catches only the expected exception, rejects invalid booking data, writes JSON with a defined encoding, and backs up files without invoking a shell. Snake_case names, docstrings, simpler calculations, and the main guard make the module easier to read, import, test, and maintain. The demonstration still produces the same totals, job-card ID, record count, and busiest vehicle as before the changes.
