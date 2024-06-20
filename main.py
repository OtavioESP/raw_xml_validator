from raw_validate_xml import RawValidateXML
from validate_by_xsd import ValidateByXSD

print("Rodando para erro1.xml")
print("\n\n\n")
erro1 = RawValidateXML(file_path="./xmls/erro1.xml").run()
print("=-=-=-=-=-"*6)
print("\n\n\n\n\n")

print("Rodando para erro2.xml")
print("\n\n\n")
erro2 = RawValidateXML(file_path="./xmls/erro2.xml").run()
print("=-=-=-=-=-"*6)
print("\n\n\n\n\n")

print("Rodando para bigstu.xml")
print("\n\n\n")
bigstu = RawValidateXML(file_path="./xmls/bigstu.xml").run()
print("=-=-=-=-=-"*6)
print("\n\n\n\n\n")

print("Rodando para stu.xml")
print("\n\n\n")
stu = RawValidateXML(file_path="./xmls/stu.xml").run()
print("=-=-=-=-=-"*6)
print("\n\n\n\n\n")

print("Rodando para stu.xsd")
print("\n\n\n")
stu = ValidateByXSD(xsd_file_path="./xmls/stu.xsd", xml_file_path="./xmls/stu.xml").run()
print("=-=-=-=-=-"*6)
print("\n\n\n\n\n")
