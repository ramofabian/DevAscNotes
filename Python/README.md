# Python Notes
<b>Important information:</b> 

- Python version: `3.14`
- Create python virtual environment:

<table>
    <tr>
        <th>Windows</th>
        <th>Linux</th>
    </tr>
    <tr>
        <td>Create new virtual environment: <code><PYTHON-PATH>/python3.14.exe -m venv venv</code></td>
        <td>Create new virtual environment: <code>python3.14 -m venv venv</code></td>
    </tr>
    <tr>
        <td>Load it form the cli: <code>venv\Scripts\Activate.ps1</code></td>
        <td>Load it form the cli: <code>.\venv\Scripts\activate<code></td>
    </tr>
    <tr>
        <td>Load it form the cli: <code>deactivate</code></td>
        <td>Load it form the cli: <code>deactivate</code></td>
    </tr>
</table>

## Data Types
To work with data types use the file `datatypes.py` script.

<b>Variable definition:</b> 
A variable in python is a collection of letters (without spaces) defined by the programmer to name a value and save it in memory to be used along the script. This `name` must have a mean and relation to what the stored value is about.

<table>
    <tr>
        <th>Kind</th>
        <th>Value</th>
        <th>Comments</th>
    </tr>
    <tr>
        <td><code>String</code></td>
        <td>"this please enter the username"</td>
        <td>To create a string python requires double, single and triple quotation</td>
    </tr>
    <tr>
        <td><code>Integer</code></td>
        <td>100</td>
        <td></td>
    </tr>
    <tr>
        <td><code>Float</code></td>
        <td>100.20</td>
        <td>It requires the use of a "." instead of comma</td>
    </tr>
    <tr>
        <td><code>Bool</code></td>
        <td><code>True</code> or <code>False</code></td>
        <td></td>
    </tr>
    <tr>
        <td><code>list</code></td>
        <td><code>["Uno", 2, False, 0, None]</code></td>
        <td>It Requires of square brackets and the element's are separated by comma.<br> It is mutable, it means that it can be changed </td>
    </tr>
    <tr>
        <td><code>dictionary</code></td>
        <td><code>{"key_1":22, "key_2:"cien"}</code></td>
        <td>It Requires of curly brackets, the element's are separated by comma and each element is defined by a key and value</td>
    </tr>
    <tr>
        <td><code>None</code></td>
        <td><code>None</code></td>
        <td>it means empty variable, there is an absence of any value</td>
    </tr>
    <tr>
        <td><code>Tuple</code></td>
        <td><code>(1, 2, 3, 4)</code></td>
        <td>Unmutable list of objects and it does not allow its modificiation</td>
    </tr>
</table>

This is how a variable can be defined and printed by CLI:
```py
int_var = 42
print(int_var)
float_var = 3.14
print(float_var)
string_var = "Hello, World!"
print(string_var)
list_var = [1, 2, 3, 4, 5]
print(list_var)
dict_var = {"name": "Alice", "age": 30, "city": "New York"}
print(dict_var)
```

To work more with datatypes execute and check the script `datatypes.py`:
```py
python datatypes.py --help
python datatypes.py
```
## Flow control
It allows you to control how the script is executed. There are ways to control it like:
- `IF/ELIF/ELSE`
- `FOR`
- `WHILE`
- `BREAK`
- `CONTINUE`
- `NESTED FOR`
- `MATCH` --> Available from python `3.10` onwards

Examples:
```py
python flowcontrol.py
```

## Functions, Methods, and Classes
### Function = Methods
Function is a group of code that executes a specific job and it is reused across the script main utilization. To save code lines these code lines are contained within a function name without spaces. 

An example of a function is `print()` which is used in python to display information on CLI. This is how a function can be defined:
```py
def read_keyboard_and_print() -> None:
    in_var = input("Enter_messages: ")
    print(in_var)
read_keyboard_and_print()
```

<b>Advantages:</b>
- Functions help to keep a code clean and easy to read.
- Reduce the number of code lines.
- As the code is structured by blocks it is easier to maintain.

To execute the code example run the command: `python Python/flowcontrol.py `

### Clasess
Classes are objects that contain attributes and methods.
<b>A built-in class in Python is </b> a strictly defined dictionary with built-in methods. i.e: All datatypes are classes.

#### Initialization
This is how a class can determine which are main initial input parameters needed for class execution.
```py
class Car:
    def __init__(self, make: str, model: str, year: int, mileage: int, condition: str, color: str) -> None:
        self.make = make
        self.model = model
        self.year = year
        self.mileage = mileage
        self.condition = condition
        self.color = color
```

#### Methods
This is how functions can be defined within a class. To see all build-in and custom methods available run the line as below:
```py
print(dir(print()))
print(dir(input()))
```

To execute the code example run the command: `python Python/functionMethodClasses.py `

## Data Serialization
This how information can be structured for machi-to-machine communication like SSH, telnet, NETCONF, GNMI. This data format is dictated by the device you want to connect with.
Most common used types:
- XML
- JSON
- YAML

### XML (Extensible Markup Lenguague)
Data format used in HTL files and use the concept of `tags` for opening and closing. `Netconf` uses this data structure.
i.e.: 
```html
<interface>
    <name>eth0</name>
    <description>MGMT access</description>
</interface>
```

<b>NOTES:</b>
- Lately is not used so often as there are more flexible and human-readable data-structures. However this is one of the most for network automation.
- Indentation is not required but it is very useful to make the information more easy to read.
- To make a list or identify a list, the tags will be repeated inside a bigger context. Sometimes it uses attributes of `id=1...2`, this depends on application requirements.

#### Reading a xml file with python
Follow this procedure:
1. Install `xmltodict`: `pip install xmltodict`
2. use the method `xmltodict.parse(xml_content)` to parse the data
3. Execute the script to see how parsed information: `python Python/xmlreader.py `

### JSON (Java Script Object Notation)
It's the most used nowadays for programming and use the concept of `key` and `values`. It is similar to python dictionary 
i.e.:
```json
{
    "interface": "eth0",
    "description": "MGMT access"
}
```

<b>NOTES:</b>
- By default the json file is just a collection of strings and to be able to use it, this file should be converted to in memory object.
- Json requires double quotes to any key or strings while python can use single and double quotes.
- Lists are defined by `[]`.
- Collection of `keys:values` should be contained within `{}` and `,`. The same for global context.

#### Reading a json file with python
- Follow this procedure to parse json to dict:
    1. `json` library is installed by default in python
    2. Use `json.load()` or `json.loads()` to convert the string to a python dictionary.<br>
    <b>Notes:</b> 
    - To use `json.loads()` the string should be in memory already. It means, the .json file has to be read already.
    - To use `json.load()` the file should be opened by python and the json function will read and parse the data.

    3. Execute the script to see how parsed information: `python Python/jsondata.py `

- Follow this procedure to convert dict to json:
    1. `json` library is installed by default in python
    2. Use `json.dump()` or `json.dumps()` to convert the string to a python dictionary.<br>
    <b>Notes:</b> 
    - To use `json.dump()` the string should be in memory and it is used to export to file.
    - To use `json.dumps()` the string should be in memory and it is used to hold the information in RAM.

    3. Execute the script to see how parsed information: `python Python/jsondata.py `

### YAML (Yet Another Markup Language)
It is very human readable and similar to JSON. Its usually used in software development but this format is not used to transmit data between devices. it uses the concept of tree and branches.
i.e.:
```yml
---
router1:
    hostname: r1
    ip: "192.168.0.1/24"
    interfaces:
    - ifacename: eth0
      id: 0
      enable: true
    - ifacename: eth1
      id: 1
      enable: true
    - ifacename: eth2
      id: 2
      enable: false
```

<b>NOTES:</b>
- Indentation is important to keep everything in the needed context.
- Lists are divided by one of the item in the list having the character `-`
- File extension can be `yaml` or `yml`. Systems interpret both as yaml files.

#### Reading a yaml file with python
- Follow this procedue to parse json to dict:
    1. Install `pyyaml`: `pip install pyyaml`
    2. Use `yaml.safe_load()` to convert the string to a python dictionary.<br>
    <b>Notes:</b> Do not use `yaml.load()` because it can open security vulnerabilities.
    3. Execute the script to see how parsed informa: `python Python/yamlreader.py`

## API (Application Programming Interface)
API is how network component can communicate each other, it uses HTTP protocol and JSON or XML for data structure. As it uses HTTP protocol, APIs uses its methods to send and receive information: `GET`, `POST`, `PUT`, `DELETE`.

<b>3 tier Application example:</b>This is how microservices architecture works, by having front, middleware and backend servers which interact eachother for some determined object. Companies like Amazon runs hundreds of micro servers like below.

```bash
                           API
+-----------+         +------------+         +-----------+-------> Database Server         
| Front end |  HTTP   | APP Server |  HTTP   | BAackend  |-------> Logistics Server         
|  Server   |-------->| Middleware |<------->|  Server   |-------> Order Server
+-----------+  JSON   +------------+  JSON   +-----------+-------> Monitoring Server
      ^                     
      |                     
   Web portal               
 i.e.: Amazon.com           
      | 
+-----------+
| Client    |
| computer  |
+-----------+

```

<b>Usual work of automation engineer:</b> We create code to be executed from a client computer or server to execute specific tasks in normal network operations like: Network deployment, maintenance, migrations, etc.

```bash                       
+------------+         +------------+           |-------> Database Server         
|  Client    |         |    Run     |    API    |-------> Network Controller Server         
| computer   |-------->|    Code    |<--------->|-------> Routers
| or server  |         +------------+           |-------> Switches     
|____________|                                  |-------> Monitoring Systems
|            |
| VS Code    |
|____________|
|            |
| Script .py |
+------------+
```
### Authentication
#### Basic Authentication
- It sends credentials in uncrypted plain text.
- Most risky one.
- Use SSL or TLS with basic authentication.
#### API Key Authentication
- Pre-shared  key by client and server.
- Key transmission potentially susceptible to interceptions.
- Typically used for read-only users.
#### Rest API-OAUTH
- Generates a token from authentication server.
- Tokens can be checked at anytime to prove validation.
- Ability to limit the scope and authorization time spam.
- OAUTH => Open Authentication
### REST API
- There is no specific standard to construct API request.
- Request and its type can change depending on the software.
- API documentation is critical for building requests.
### REST Structures:
1. URL or URI: Uniform Resource Locator, Uniform Resource Identifier.
2. Method: Get, post, delete, put, update.
3. Header: Usually uses HTTP headers added in `name:value` pairs.
i.e.: Keep-alive, timeout, max, content-type, etc.
4. Body: Data of the message.
### Webhooks
- Usually called reverse APIs.
- HTTP/S post message triggered by an event.
- Usually it is used to provide event notifications.
- Lightweight APIs driving events.
- Application can be registered with URL.
- APP with webhook must be allways running.
### HTTP/S
#### Methods or Verbs
List of used methods:
- `GET`: Used to retrieve data from remote end.
- `POST`: Create new data in the remote end.
- `DELETE`: Remove information from the remote end.
- `PUT/PATCH`: Update information in the remote end.
#### Headers
This is the metadata used to interact with remote ends and it can indicate the purpose of the message and additional specifications.
#### Payload
Some time this field is empty and some others might cotains filters for a query itself.
#### Response codes
<table>
    <tr>
        <th colspan=2>100s codes</th>
        <th colspan=2>200s codes</th>
        <th colspan=2>300s codes</th>
        <th colspan=2>400s codes</th>
        <th colspan=2>500s codes</th>
    </tr>
    <tr>
        <td colspan=2>Informational</td>
        <td colspan=2>Success</td>
        <td colspan=2>Redirection</td>
        <td colspan=2>Client side error</td>
        <td colspan=2>Server side error</td>
    </tr>
    <tr>
        <td>Code</td>
        <td>Description</td>
        <td>Code</td>
        <td>Description</td>
        <td>Code</td>
        <td>Description</td>
        <td>Code</td>
        <td>Description</td>
        <td>Code</td>
        <td>Description</td>
    </tr>
    <tr>
        <td>101</td>
        <td>Continue code<br>final response will be seen when request will be completed</td>
        <td>200</td>
        <td>OK<br>Request was successfull and completed</td>
        <td>301</td>
        <td>Endoint moved to another location permanently</td>
        <td>400</td>
        <td>Bad request</td>
        <td>500</td>
        <td>Internal server error</td>
    </tr>
    <tr>
        <td></td>
        <td></td>
        <td>201</td>
        <td>Created<br>Request was created</td>
        <td>302</td>
        <td>Found</td>
        <td>401</td>
        <td>Unauthorized login</td>
        <td>502</td>
        <td>Bad gateway</td>
    </tr>
    <tr>
        <td></td>
        <td></td>
        <td>202</td>
        <td>No Content</td>
        <td>304</td>
        <td>Not found</td>
        <td>403</td>
        <td>Forbidden</td>
        <td>503</td>
        <td>Server unavailable</td>
    </tr>
    <tr>
        <td></td>
        <td></td>
        <td></td>
        <td></td>
        <td></td>
        <td></td>
        <td>404</td>
        <td>Not found</td>
        <td></td>
        <td></td>
    </tr>
    <tr>
        <td></td>
        <td></td>
        <td></td>
        <td></td>
        <td></td>
        <td></td>
        <td>408</td>
        <td>Request timeout</td>
        <td></td>
        <td></td>
    </tr>
    <tr>
        <td></td>
        <td></td>
        <td></td>
        <td></td>
        <td></td>
        <td></td>
        <td>429</td>
        <td>Too many requests</td>
        <td></td>
        <td></td>
    </tr>
</table>

### Tools
There are many tools that can be used to interact with APIs, among them the most important ones are:
- Postman: [LINK](https://www.postman.com/) 
- Bruno: [LINK](https://www.usebruno.com/)

There you can create collections and inside a collection, there are many type of requests that can be done.

### Querying API with Python
#### Requirements
- rich
- requests
- json

Commands to install libraries:
```bash
pip install rich
pip install requests
pip install json
```
#### Execution
Example:
```py
import requests
import json
from rich.console import Console

cli = Console()
base_url = "https://swapi.info/api/"
respose = requests.get(base_url + "people")
cli.print(response)
```

To see full code and the challenge execute the python script:
```bash
python Python/APIs/swapi.py 
```
### Building your own API using Flask
Commmon python modules:
- Flask
- FastApi

In those modules, the concept of routes is the same as endpoints. Specific modules that can execute specific task or tasks.
```bash
http://localhost:8080/|-->Login
                      |-->Logout
                      |-->getdata
                      |-->Pushdata
```
### Pre-requisities
Libraries:
- flask
```sh
pip install flask
```
### Flask app initialization script
This is how Flask app should be initializated/

```py
from flask import Flask, jsonify, request

# Create a Flask application instance
app = Flask(__name__)

if __name__ == '__main__':
    app.run(debug=True)
```

### Adding a route
```py
@app.route('/api/data', methods=['GET'])
def hello():
    # Return a JSON response
    return jsonify({'message': 'Hello, World!'})
```

### Executing the api with Basic Authentication method enabled
```sh
python /Python/flaskapi/myapi.py
```
Body for `POST` request:
```json
{
    "make": "Ford",
    "model": "Focus",
    "year": "2026"
}
```
### Executing the api with Web Token used as a param 
```sh
#Install JWT library
pip install jwt
python /Python/flaskapi2/readhumanapi.py

#NOTE: Special postman script for reading the token and saving it in enviroment variable
pm.collectionVariables.set('token', pm.response.json().token)
```
Body for `POST` request:
```json
{
    "name": "Merlot",
    "age": 55
}
```

### Executing the api with Bearer Token used in Athentication header 
Refrerences:
- https://www.geeksforgeeks.org/python/flask-api-authentication-with-json-web-tokens/
- https://medium.com/@alfininfo/easy-way-to-create-and-validate-bearer-token-in-flask-application-95d7e8cb2ffd
```sh
python /Python/flaskapi3/readdogsapi.py

#NOTE: Special postman script for reading the token and saving it in enviroment variable
pm.collectionVariables.set('token', pm.response.json().token)
```
Body for `POST` request:
```json
{
    "doglist":
    [
        {
            "name": "Benji",
            "age": 3,
            "breed": "Asutralian Sheperd"
        },
                {
            "name": "Hachi",
            "age": 10,
            "breed": "Golden Retriver"
        }
    ]
}
```
<!-- 
### Executing the api with OAuth2
Refrerences: https://realpython.com/flask-google-login/
```sh
pip install Authlib 
python /Python/flaskapi3/readdogsapi.py

#NOTE: Special postman script for reading the token and saving it in enviroment variable
pm.collectionVariables.set('token', pm.response.json().token)
```
Body for `POST` request:
```json
{
    "doglist":
    [
        {
            "name": "Benji",
            "age": 3,
            "breed": "Asutralian Sheperd"
        },
                {
            "name": "Hachi",
            "age": 10,
            "breed": "Golden Retriver"
        }
    ]
}
``` -->