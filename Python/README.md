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
        <td>Create new virtual enviroment: `python3.14.exe -m venv venv`</td>
        <td>Create new virtual enviroment: `python3.14 -m venv venv` </td>
    </tr>
    <tr>
        <td>Load it form cli: `.\venv\Scripts\Activate.ps1`</td>
        <td>Load it form cli: `.\venv\Scripts\activate`</td>
    </tr>
    <tr>
        <td>Load it form cli: `deactivate` </td>
        <td>Load it form cli: `deactivate` </td>
    </tr>
</table>

## Data Types
To work with data types use the file `datatypes.py` script.

<b>Variable definition:</b> 
A variable in python is a collection of letters (without spaces) defined by the programmer to name a value and save it in memory to be used along the script. This `name` must have a mean and relation to what the stored value is about.

This is a variable can be defined and pinted by CLI:
```py
my_cool_variable = 42
print(my_cool_variable)
```

In this example I defined a variable called `my_cool_variable` and stored the value `42` in memory. To show the content of this variable I used print function and the variable name.

