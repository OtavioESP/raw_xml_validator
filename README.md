# raw_xml_validator
Just a quick validator for XML files, made for the college.

### Information
- Python Version: 3.10.x

### How to Run
- Ensure you have a file named "teste.xml" in the same directory.
- Run in the terminal:
    ```
    python raw_validate_xml.py
    ```

### Description
This file represents the functional version, not just a validation of a specific XML, but of any valid XML. The only issue is that the data written in the final txt file may be somewhat "buggy". So feel free to create your XML to test! :3

### XML Validation Rules
1. It needs to have a father tag wich contains the whole file.
2. All tags need to open and close at the same depth.

### Example XML
```xml
<person>
    <name>
        <first>
            Joaozinho da Silva Pereira
        </first>
        <last>
            Andrade
        </last>
    </name>
    <cpf>
        example of a CPF
    </cpf>
    <address>
        <street>
            Avenida dos Andradas 2984
            <number>
                928
            </number>
            <district>
                Santa Lucia
            </district>
            <state>
                Minas Gerais
                <city>
                    Belzonte
                </city>
            </state>
            <complement>
                Apartment: 901
            </complement>
        </street>
    </address>
</person>
