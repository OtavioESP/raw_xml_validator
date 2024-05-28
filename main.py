from raw_validate_xml import RawValidateXML
from validate_xsd import ValidateXSD
from validate_xml import ValidateXML

raw_xml_validation = RawValidateXML().run()

if raw_xml_validation:
    xsd_data = ValidateXSD().run()
    xml_data = ValidateXML(xsd_data).run()
