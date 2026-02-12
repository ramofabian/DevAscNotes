import yaml
import os, sys

def read_yaml_file(file_path):
    """Reads a YAML file and converts it to a dictionary."""
    with open(file_path, 'r') as file:
        json_content = file.read()
        data_dict = yaml.safe_load(json_content)
        return data_dict

file_name = 'r1.yml'
# Build the file path dynamically
initial_path = os.getcwd().split(os.sep)
if not "Python" in initial_path:
    initial_path.append("Python")
if not "DataSerialization" in initial_path:
    initial_path.append("DataSerialization")

initial_path.append(file_name)
build_path = os.sep.join(initial_path)
# print(f"Constructed file path: {build_path}")

# Check if the file exists
if not os.path.isfile(build_path):
    print(f"Error: The file '{file_name}' does not exist at the path: {build_path}")
    sys.exit(1) 

# Read the YAML  file and print the data as a dictionary
data = read_yaml_file(build_path)
print(f"YAML Data as Dictionary:\n{data}")

# Sample dictionary data structure (if file read fails or for testing)
print(f"\nAccessing Specific Data:\n{'-'*30}")
# Example: Accessing specific data from the dictionary  
print(f"Router: {data['router']['hostname']}")
print(f"interface: {data['router']['interfaces'][0]['name']}")