import argparse, sys

def print_variable(my_cool_variable):
    #Printing a variable
    print(f"My defined variable is {type(my_cool_variable)} and contains the value:", my_cool_variable)
    print("Size of the variable in bytes:", sys.getsizeof(my_cool_variable))
    print("-" * 40)

def main():
    parser = argparse.ArgumentParser(description="A simple script to demonstrate data types in Python.")
    args = parser.parse_args()
    int_var = 42
    float_var = 3.14
    string_var = "Hello, World!"
    list_var = [1, 2, 3, 4, 5]
    dict_var = {"name": "Alice", "age": 30, "city": "New York"}
    bool_var = True
    none_var = None
    print_variable(my_cool_variable=int_var)
    print_variable(my_cool_variable=float_var)
    print_variable(my_cool_variable=string_var)
    print_variable(my_cool_variable=list_var)
    print_variable(my_cool_variable=dict_var)
    print_variable(my_cool_variable=bool_var)
    print_variable(my_cool_variable=none_var)

if __name__ == "__main__":
    main()

    