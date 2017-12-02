import sys
import xml.etree.ElementTree as ET
import os
from .models import Payment

class DataLoader(object):
    varx = 1

    def __init__(self, varx=0):
        self.varx = varx

    def validate(self):
        return True

    def load_data(self):

        payment_list = []

        directory = "../XML_Reader/Payments"
        file_list = os.listdir(directory)
        file_list.sort()

        for file in file_list:
            filename = os.fsdecode(file)
            full_path = os.path.join(directory, filename)
            print('Loading from file %s' % full_path, file=sys.stderr)

            new_payment = self.load_payment_from_file(full_path)
            payment_list.append(new_question)

        return payment_list


    def load_payment_from_file(self,full_path):

        payment_tree = ET.parse(full_path)
        root = payment_tree.getroot()
        new_payment = Question()

        for child in root:
            name = child.get('name')
            print('Loading payment %s' % name, file=sys.stderr)
            print(child.tag, file=sys.stderr)

        return new_payment


