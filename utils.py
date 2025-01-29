import xml.etree.ElementTree as ET
import base64
import os
import requests

def extract_clickable(xml_input):
    
    try:
        # Parse XML input
        if isinstance(xml_input, str):
            if xml_input.startswith('http://') or xml_input.startswith('https://'):
                response = requests.get(xml_input)
                response.raise_for_status()
                xml_content = response.text
                root = ET.fromstring(xml_content)
            elif os.path.isfile(xml_input):
                tree = ET.parse(xml_input)
                root = tree.getroot()
            else:
                root = ET.fromstring(xml_input)
        else:
            raise ValueError("Invalid XML input type.")

        
        clickable_elements = root.findall('.//*[@clickable="true"]')
        
        result = [ET.tostring(action_elem, encoding='unicode') for action_elem in clickable_elements]
        for action_elem in clickable_elements:
            ET.tostring(action_elem, encoding='unicode')
        
        return result
    
    except ET.ParseError as e:
        print(f"XML Parse Error: {e}")
        return ""
    except Exception as e:
        print(f"Unexpected error: {e}")
        return ""

def encode_image(input_source):
    try:
        if isinstance(input_source, str):
            # Check if it's a URL
            if input_source.startswith('http://') or input_source.startswith('https://'):
                response = requests.get(input_source)
                response.raise_for_status()
                image_data = response.content
            # Check if it's a file path
            elif os.path.isfile(input_source):
                with open(input_source, 'rb') as image_file:
                    image_data = image_file.read()
            else:
                raise ValueError("Invalid file path or URL.")
        else:
            # Assume it's a file-like object
            image_data = input_source.read()

        # Encode the image data
        encoded_image = base64.b64encode(image_data).decode()
        return encoded_image

    except Exception as e:
        print(f"Error encoding image: {e}")
        return None
