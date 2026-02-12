import json
import sys, os

def read_json_file(file_path):
    """Reads a JSON file and converts it to a dictionary."""
    with open(file_path, 'r') as file:
        json_content = file.read()
        data_dict = json.loads(json_content)
        return data_dict

file_name = 'r1.json'
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

# Read the JSON  file and print the data as a dictionary
data = read_json_file(build_path)
print(f"JSON Data as Dictionary:\n{data}")

# Sample dictionary data structure (if file read fails or for testing)
print(f"\nAccessing Specific Data:\n{'-'*30}")
# Example: Accessing specific data from the dictionary  
print(f"Router: {data['router']['hostname']}")
print(f"interface: {data['router']['interfaces'][0]['name']}")


sample_data = {
    "router": {
        "hostname": "Router1",
        "interfaces": [
            {"name": "eth0", "ip": "192.168.1.1"},
            {"name": "eth1", "ip": "192.168.2.1"}
        ]
    }
}

# Example: Dump a dictionary into a JSON file
print(f"\n\nDumping Dictionary to JSON File:\n{'-'*30}")
output_file = 'output.json'
output_path = os.path.join(os.path.dirname(build_path), output_file)

with open(output_path, 'w') as file:
    json.dump(sample_data, file, indent=4)
    
print(f"Dictionary successfully written to: {output_path}")

