# Python Notes
<b>Important information:</b> 

- Python verison `3.14`
- Create python virtual enviroment:

<table>
    <tr>
        <th>Windows</th>
        <th>Linux</th>
    </tr>
    <tr>
        <td>Create new virtual enviroment: <code>python3.14.exe -m venv venv</code></td>
        <td>Create new virtual enviroment: <code>python3.14 -m venv venv</code></td>
    </tr>
    <tr>
        <td>Load it form cli: <code>.\venv\Scripts\Activate.ps1</code></td>
        <td>Load it form cli: <code>.\venv\Scripts\activate<code></td>
    </tr>
    <tr>
        <td>Load it form cli: <code>deactivate</code></td>
        <td>Load it form cli: <code>deactivate</code></td>
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
        <td>To create an string python requires double, single and triple quotation</td>
    </tr>
    <tr>
        <td><code>Integrer</code></td>
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
        <td><code>True</code> or <code>Flase</code></td>
        <td></td>
    </tr>
    <tr>
        <td><code>list</code></td>
        <td><code>["Uno", 2, False, 0, None]</code></td>
        <td>It Requires of square brakets and the element's are sparated by comma.<br> It is mutable, it means that it can be changes </td>
    </tr>
    <tr>
        <td><code>dictionary</code></td>
        <td><code>{"key_1":22, "key_2:"cien"}</code></td>
        <td>It Requires of curly brakets, the element's are sparated by comma and each element is defined by a key and value</td>
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

This is how a variable can be defined and pinted by CLI:
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
pyhton datatypes.py --help
pyhton datatypes.py
```
## Flow control
It allows you to control how the script is executed. There are ways to control it like:
- `IF/ELIF/ELSE`
- `FOR`
- `WHILE`
- `BREAK`
- `CONTINUE`
- `NESTED FOR`
- `MATCH` --> Avatiilabe from python `3.10` onwards

Examples:
```py
pyhton flowcontrol.py
```

## Functions, Methods, and Classes
### Function = Methods
Function is a group of code that executes specific job and it is reused across the script main utilization. To save code lines these code lines are contaned within an function name whithout spaces. 

An example of a function is `print()` which is used in python to display information on CLI. This is how a function can be defined:
```py
def read_keyboard_and_print() -> None:
    in_var = input("Enter_messages: ")
    print(in_var)
read_keyboard_and_print()
```

<b>Advantages:</b>
- Functions helps to maintain a code clean and easy to read.
- Reduce the number or code lines.
- As the code is struced by blocks it is easier to maintain.

To execute the code example run the command: `python Python/flowcontrol.py `

### Clasess
Clasess are objects object which contains atributes and methods insde.
<b>built-in class in Python is </b> a strictly defined dictionary with built-in methods. i.e: All datatypes are classes.

#### Initialization
This is how a class can determent which are main initial input parameters needed for class execution.
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
This how information can be structure for machi-to machine comunication like SSH, telenet, NETCONF, GNMI. This data format is dictated by the device you want to conned with.
Most common used types:
- XML
- JSON
- YAML

### XML (Xtensable Markup Lenguague)
Data format used in HTL files and use the concept of `tags` for opening and closing. `Netconf` uses this data structure.
i.e.: 
```html
<interface>
    <name>eth0</name>
    <description>MGMT access</description>
</interface>
```

<b>NOTES:</b>
- Lately is not used so ofent as there are more flexible and hubman readable data-structures. However this is one of the most for network automation.
- Indentiation is not required but it is very usefull to make the information more easy to read.
- To make a list or identify a list, the tags will be repeted inside a bigger context. Sometimes it uses attributes of `id=1...2`, this depends on application requirements.

#### Reading a xml file with python
Follow this procedue:
1. Install `xmltodict`: `pip install xmltodict`
2. use the method `xmltodict.parse(xml_content)` to parse the data
3. Execute the script to see how parsed informa: `python Python/xmlreader.py `

### JSON (Java Script Object Notation)
It's the most used nowodays for programing and use the concept of `key` and `values`. It is similar to python dictionary 
i.e.:
```json
{
    "interface": "eth0",
    "description": "MGMT access"
}
```

<b>NOTES:</b>
- By default the json file is just a collection of strings and to be able to use it, this file should be converted to in memory object.
- Json requires double questos to any key or strings while python can use single and double quotes.
- Lists are defined by `[]`.
- Collection of `keys:values` should be contained within `{}` and `,`. The same for global context.

#### Reading a json file with python
- Follow this procedue to parse json to dict:
    1. `json` library is installed by default in python
    2. Use `json.load()` or `json.loads()` to convert the string to a python dictionary.<br>
    <b>Notes:</b> 
    - To use `json.loads()` the string should be in memory already. It means, the .json file has to be read already.
    - To use `json.load()` the file should be opened by python and the json function will read and parse the data.

    3. Execute the script to see how parsed informa: `python Python/jsondata.py `

- Follow this procedue to paconvert dict to json:
    1. `json` library is installed by default in python
    2. Use `json.dump()` or `json.dumps()` to convert the string to a python dictionary.<br>
    <b>Notes:</b> 
    - To use `json.dump()` the string should be in memory and it is used to export to file.
    - To use `json.dumps()` the string should be in memory and it is used to hold the information in RAM.

    3. Execute the script to see how parsed informa: `python Python/jsondata.py `

### YAML (Yet Another Markup Lenguage)
It is very human reable and similar to JSON. Its susually sued in sowftware development but this format is not used to transmmit data between devices. it uses the concept of tree and branches.
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
- Identiation is important to keep everithing in the needed contexte
- Lists are deviced by one of the item in the list having the character `-`
- File extension can be `yaml` or `yml`. Systems interpretate both as yaml files.

#### Reading a yaml file with python
- Follow this procedue to parse json to dict:
    1. Install `pyyaml`: `pip install pyyaml`
    2. Use `yaml.safe_load()` to convert the string to a python dictionary.<br>
    <b>Notes:</b> Do not use `yaml.load()` becase it can open scurity breaches.
    3. Execute the script to see how parsed informa: `python Python/yamlreader.py`

## API (Application Programming Interface)
API is how network comonenetes can comunicate each other, it uses HTTP protocol and JSON or XML for data structure. As it uses HTTP protocol, APIs uses its methods to send and received information: `GET`, `POST`, `PUT`, `DELETE`.

<b>3 tier Application exmaple:</b>This is how micro services architecture works, by having front, middleware and backend servers which interace eachother for some determiniated object. Companies like Amazon runs hundreds of micro servers like below.

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
- Key transmision potentially suseptible to interceptions.
- Typically used for readonly users.
#### Rest API-OAUTH
- Generates a tocker from authentication server.
- Tokens can be checked at anytime to prove validation.
- Ability to limit the scope and autherization time spam.
- OAUTH => Open Authentication
### REST API
- There is no specific standar to construct API request.
- Request and its type can change depending on the software.
- API documentation is critical for building requests.
### REST Structures:
1. URL or URI: Uniform Resouce Locator, Uniform Resource Identifier.
2. Method: Get, post, delete, put, update.
3. Header: Usually uses HTTP headers added in `name:value` pairs.
i.e.: Keep-alive, timeout, max, content-type, etc.
4. Body: Data of the message.
### Webhooks
- Usually called reverse APIs.
- HTTP/S post message triggered by an event.
- Usually it is used to provide event notifications.
- Ligthweigth APIs driving events.
- Application can be registered with URL.
- APP with webhook muct be allways running.
### HTTP/S
#### Methods or Verbs
List of used methods:
- `GET`: Used to retrieve data from remote end.
- `POST`: Create new data in the remote end.
- `DELETE`: Remove information from the remote end.
- `PUT/PATCH`: Update information in the remote end.
#### Headers
This is the metadata used to interact with remote ends and it can indicate the propuse of the message and additional specificiations.
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

In there you can create collections and inside a collection, there are many type of requests thta can be done.

### Quering API with Python
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