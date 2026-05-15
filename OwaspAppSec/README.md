# OWASP Threats and App Security
In this section we will present basic information about security best practices in software development.
## Environment Variables
- Good option to avoid adding confidential information hardcoded in the script.
- Store this information in the OS RAM memory this information.
- By default, the defined variable is stored in RAM by the time we have the session enable.
- Defining a variable from OS:
    - **Linux**: `<key>=<value>`. i.e: `DB_PASSWORD="my_password"`
    - **Windows**: `set <key>=<value>`. i.e: `set testVar=TEST^&1`
- Calling the variable from OS: 
    - **Linux**: `echo $<key>`. i.e: `echo $DB_PASSWORD`
    - **Windows**: `set <key>`. i.e: `set testVar`
- Calling the variable from Python using `os.getenv`:
```py
import os
PASS = os.getenv('DB_PASSWORD')
print(PASS)
``` 
- Define environment variables to be always available:
    - **Linux**:
        - Add the variable in files and then log off and log in:
            - `.profile`: exclusive to the username
            - `bashrc`: Available for all users.
- Calling the variable from Python using `dotenv`:
    - This library requires an additional file with `.env` extension to store the data and then call it.
    - **Note**: Make sure that `.gitignore` file has listed this file to not upload this information.
    - Installation: `pip install python-dotenv`
    - The content inside the `.env` file can look like this:
```sh
PASS ="my_pass"
HOST ="192.168.2.2"
USER ="user1"
```
    - Python script:
```py
import os
from dotevn import load_dotenv

load_dotenv()
PASS=os.getenv(PASS)
HOST=os.getenv(HOST)
USER=os.getenv(USER)

print(f"{PASS}\n{HOST}\n{USER}")
```

## AWS Secrets Manager
- It is an alternative to virtual environment variables. 
- It uses AWS infrastructure to manage all confidential or secrete information. 
- The script should connect to AWS Secret Manager with a token and then extract the needed information (python library `boto3`).
- It is used for always running application.

## Linters and detection tools
- A linter is a special library which checks the code and verify whether there are mistakes, security vulnerabilities and brings some recommendations aligned to international standard like PEP8. One example is `pylint` and `bandit`
```bash
pip3 install bandit
bandit <python script>
```
- Output example:
```sh
$ bandit test.py
[main]  INFO    profile include tests: None
[main]  INFO    profile exclude tests: None
[main]  INFO    cli include tests: None
[main]  INFO    cli exclude tests: None
[main]  INFO    running on Python 3.9.10
Run started:2026-05-14 10:07:31.955398

Test results:
>> Issue: [B404:blacklist] Consider possible security implications associated with the subprocess module.
   Severity: Low   Confidence: High
   CWE: CWE-78 (https://cwe.mitre.org/data/definitions/78.html)
   More Info: https://bandit.readthedocs.io/en/1.8.6/blacklists/blacklist_imports.html#b404-import-subprocess
   Location: .\test.py:2:0
1       import os
2       import subprocess
3

--------------------------------------------------
>> Issue: [B105:hardcoded_password_string] Possible hardcoded password: 'hunter2'
   Severity: Low   Confidence: Medium
   CWE: CWE-259 (https://cwe.mitre.org/data/definitions/259.html)
   More Info: https://bandit.readthedocs.io/en/1.8.6/plugins/b105_hardcoded_password_string.html
   Location: .\test.py:4:11
3
4       password = "hunter2"  # hardcoded password (Bandit will catch this)
5

--------------------------------------------------
>> Issue: [B307:blacklist] Use of possibly insecure function - consider using safer ast.literal_eval.
   Severity: Medium   Confidence: High
   CWE: CWE-78 (https://cwe.mitre.org/data/definitions/78.html)
   More Info: https://bandit.readthedocs.io/en/1.8.6/blacklists/blacklist_calls.html#b307-eval
   Location: .\test.py:7:11
6       def dangerous_eval(user_input):
7           return eval(user_input)  # Bandit flags this as a major issue
8

--------------------------------------------------
>> Issue: [B605:start_process_with_a_shell] Starting a process with a shell: Seems safe, but may be changed in the future, consider rewriting without shell
   Severity: Low   Confidence: High
   CWE: CWE-78 (https://cwe.mitre.org/data/definitions/78.html)
   More Info: https://bandit.readthedocs.io/en/1.8.6/plugins/b605_start_process_with_a_shell.html
   Location: .\test.py:10:4
9       def insecure_shell():
10          os.system("ls -l")  # Bandit flags this as unsafe
11          subprocess.call("rm -rf /tmp/somedir", shell=True)  # shell=True is dangerous

--------------------------------------------------
>> Issue: [B607:start_process_with_partial_path] Starting a process with a partial executable path
   Severity: Low   Confidence: High
   CWE: CWE-78 (https://cwe.mitre.org/data/definitions/78.html)
   More Info: https://bandit.readthedocs.io/en/1.8.6/plugins/b607_start_process_with_partial_path.html
   Location: .\test.py:10:4
9       def insecure_shell():
10          os.system("ls -l")  # Bandit flags this as unsafe
11          subprocess.call("rm -rf /tmp/somedir", shell=True)  # shell=True is dangerous

--------------------------------------------------
>> Issue: [B607:start_process_with_partial_path] Starting a process with a partial executable path
   Severity: Low   Confidence: High
   CWE: CWE-78 (https://cwe.mitre.org/data/definitions/78.html)
   More Info: https://bandit.readthedocs.io/en/1.8.6/plugins/b607_start_process_with_partial_path.html
   Location: .\test.py:11:4
10          os.system("ls -l")  # Bandit flags this as unsafe
11          subprocess.call("rm -rf /tmp/somedir", shell=True)  # shell=True is dangerous
12

--------------------------------------------------
>> Issue: [B602:subprocess_popen_with_shell_equals_true] subprocess call with shell=True seems safe, but may be changed in the future, consider rewriting without shell
   Severity: Low   Confidence: High
   CWE: CWE-78 (https://cwe.mitre.org/data/definitions/78.html)
   More Info: https://bandit.readthedocs.io/en/1.8.6/plugins/b602_subprocess_popen_with_shell_equals_true.html
   Location: .\test.py:11:4
10          os.system("ls -l")  # Bandit flags this as unsafe
11          subprocess.call("rm -rf /tmp/somedir", shell=True)  # shell=True is dangerous
12

--------------------------------------------------

Code scanned:
        Total lines of code: 10
        Total lines skipped (#nosec): 0

Run metrics:
        Total issues (by severity):
                Undefined: 0
                Low: 6
                Medium: 1
                High: 0
        Total issues (by confidence):
                Undefined: 0
                Low: 0
                Medium: 1
                High: 6
Files skipped (0):
(venv) 
```
## Ansible-vault
- Ansible feature to handle file and encrypt this information.
```sh
#Encrypting group-vars
ansible-vault encrypt <file>
# then enter a password

#Dencrypting group-vars
ansible-vault dencrypt <file>
# then enter a password

#Creating an encrypted file
ansible-vault create <file>
# then enter a password
# the add the file inside playbook at vars_files section
```
- To Ansible be able to execute a playbook and the encrypted information use the command as below:
```bash
ansible-playbook -i <INVENTORY> <PLAYBOOK-FILE> --ask-vault-pass
```
## Source Control and CI/CD (Github)
- This is used for building pipelines
- Go to git_repo/settings/Secrets and variables:
    - Then under actions create:
        - Environment secrets, variables
        - Repository secrets  
## OWASP Top 10
- It is a standard awareness document for developers and web application security. It represents a broad consensus about the most critical security risks to web applications.
- Link: https://owasp.org/Top10/2025/
- It is updated every 4 years.