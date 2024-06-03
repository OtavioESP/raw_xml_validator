# raw_xml_validator
Just a quick raw validator for XML files, made for a college work.

### Information
- Python Version: 3.10.x

### How to Run
- Ensure you have a file named "teste.xml" in the same directory.
- Run in the terminal:
    ```
    python main.py
    ```

### Description
This file represents the functional version, not just a validation of a specific XML, but of any valid XML and its own XSD. The only issue is that the data written in the final txt file may be somewhat "buggy". So feel free to improve it !! :3



### XML Validation Rules
1. The file needs to have a root tag which contains the whole file.
2. All tags need to open and close at the same depth.
3. All tags must follow the data type of its XSD representation


### Example XML
```xml
<pessoa>
    <nome>
        Joaozinho da Silva
    </nome>
    <idade>
        32
    </idade>
    <altura>
        184
    </altura>
    <peso>
        78.2
    </peso>
    <endereco>
        <rua>
            <teste>
                Olaaaaa
            </teste>
        </rua>
        <numero>
        234
        </numero>
    </endereco>
</pessoa>
