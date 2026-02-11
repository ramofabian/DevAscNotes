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
pyhton flowcontrol.py --help
pyhton flowcontrol.py
```