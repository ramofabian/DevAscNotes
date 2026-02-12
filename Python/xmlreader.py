import xmltodict
import sys, os

def read_xml_file(file_path):
    """Reads an XML file and converts it to a dictionary."""
    with open(file_path, 'r') as file:
        xml_content = file.read()
        data_dict = xmltodict.parse(xml_content)
        return data_dict


file_name = 'r1.xml'
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

# Read the XML file and print the data as a dictionary
data = read_xml_file(build_path)
print(f"XML Data as Dictionary:\n{data}")

print(f"\nAccessing Specific Data:\n{'-'*30}")
# Example: Accessing specific data from the dictionary  
print(f"Router: {data['router']['hostname']}")
print(f"interface: {data['router']['interfaces']['interface'][0]['name']}")