from jinja2 import Template

def generate_interface_config(interface_data:dict) -> str:
    if not all(key in interface_data for key in ["name", "description", "ip_address", "subnet_mask"]):
        raise ValueError("Missing required interface data")
    template_str = """
interface {{ name }}
 description {{ description }}
 ip address {{ ip_address }} {{ subnet_mask }}
 no shutdown
"""
    template = Template(template_str.strip())
    return template.render(interface_data)