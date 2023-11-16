import argparse
import csv
import xml.etree.ElementTree as ET

parser = argparse.ArgumentParser(description='Перевод матрицы кореспонденции в OD tazRelation format')

parser.add_argument('--begin', type=int, help='Начало поездки')
parser.add_argument('--end', type=int, help='Конец поездки')
parser.add_argument('--id', type=str, help='Тип транспортного средвства')
parser.add_argument('file', type=str, help='Путь к файлу csv без расширения файла')

args = parser.parse_args()

def generate_xml(id: str, begin: int, end: int):
    root = ET.Element("data", 
       attrib={
           "xmlns:xsi": "https://www.w3.org/2001/XMLSchema-instance",
           "xsi:noNamespaceSchemaLocation": "https://sumo.dlr.de/xsd/datamode_file.xsd"
       })

    return (root, ET.SubElement(root, "interval", 
       attrib={
           "id": id, 
           "begin": str(begin),  
           "end": str(end)
       }))

def csv_to_taz_relation(interval: ET.Element, input_file: str):
   with open(input_file, 'r', ) as csvfile:
       reader = csv.reader(csvfile, delimiter=';')  
       headers = next(reader)
       for row in reader:
           for i in range(1, len(row)):
               ET.SubElement(interval, "tazRelation", attrib={"count": row[i], "from": row[0], "to": headers[i]})

root, interval = generate_xml(args.id, args.begin, args.end)
csv_to_taz_relation(interval, args.file + '.csv')
ET.ElementTree(root).write(args.file + '.xml')