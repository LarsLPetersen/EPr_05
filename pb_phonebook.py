"""Contains the main class PhoneBook"""

__author__ = "6360278: Qasim Raza, 6290157: Lars Petersen"
__copyright__ = ""
__credits__ = "" 
__email__ = "qasimr@icloud.com, petersen@informatik.uni-frankfurt.de"


import os.path
import pickle
import pprint
import constants
import random
from operator import attrgetter


class PhoneBookEntry(object):
    """Class defining a single phone book entry"""
    
    def __init__(self, first_name, second_name, city, postal_code, \
                 street, phone_number = None):
        """ """
        
        self.first_name = first_name
        self.second_name = second_name
        self.city = city
        self.postal_code = postal_code
        self.street = street
        self.phone_number = phone_number
    
    
    def update(self, first_name, second_name, city, postal_code, \
                     street, phone_number = None):
        """ """         
        
        self.first_name = first_name
        self.second_name = second_name
        self.city = city
        self.postal_code = postal_code
        self.street = street
        self.phone_number = phone_number
        
        return self
        
    
    def __repr__(self):
        """ """
        
        return repr((self.first_name, self.second_name, self.city, \
                     self.postal_code, self.street, self.phone_number))
                     
    def to_list(self):
        """ """
        
        result = []
        result.append(self.first_name)
        result.append(self.second_name)
        result.append(self.city)
        result.append(self.postal_code)
        result.append(self.street)
        result.append(self.phone_number)
       
        return result
        
    
    def __eq__(self, other):
        """ """
        
        if ((self.first_name == other.first_name) and \
           (self.second_name == other.second_name) and \
           (self.city == other.city) and \
           (self.postal_code == other.postal_code) and \
           (self.street == other.street) and \
           (self.phone_number == other.phone_number)):
            return True
        else:
            return False



class PhoneBook(object):
    """Class containing entries"""
    
    def __init__(self, name, test_mode = False):
        """ """
        
        """
        self.name = name
        self.file_name = name + ".pkl"
        self.entries = self.read_from_file(self.file_name) 
        self.nb_of_entries = len(self.entries)
            
        """
        if not test_mode:
            self.name = name
            self.file_name = name + ".pkl"
            self.entries = self.read_from_file(self.file_name) 
            self.nb_of_entries = len(self.entries)
        
        else:    
            self.name = "Example_Phonebook"
            self.file_name = name + ".pkl"
            self.entries = self.generate_testbook()
            self.write_to_file(self.file_name)
            self.nb_of_entries = len(self.entries)
    
    
    
    def add_entry(self, entry):
        """ """
        
        if not entry in self:
            self.entries.append(entry)
            self.nb_of_entries += 1
            return 
        else:
            print("Eintrag schon da")
    
    
    def __contains__(self, entry):
        """ """
        
        for pb_entry in self.entries:
            if pb_entry == entry:
                return True
                break
            else:
                return False
                
    
    def search(self, criterion):
        """ """
        
        result = []
        if criterion[0] == "Vorname":
            for entry in self.entries:
                if entry.first_name == criterion[1]:
                    result.append(entry.to_list())
                    
        elif criterion[0] == "Nachname":
            for entry in self.entries:
                if entry.second_name == criterion[1]:
                    result.append(entry.to_list())
        
        elif criterion[0] == "Stadt":
            for entry in self.entries:
                if entry.city == criterion[1]:
                    result.append(entry.to_list())
                    
        elif criterion[0] == "PLZ":
            for entry in self.entries:
                if entry.postal_code == criterion[1]:
                    result.append(entry.to_list())
                    
        elif criterion[0] == "Straße":
            for entry in self.entries:
                if entry.street == criterion[1]:
                    result.append(entry.to_list())
        
        elif criterion[0] == "Telefonnummer":
            for entry in self.entries:
                if entry.phone_number == criterion[1]:
                    result.append(entry.to_list())
                    
        else: pass
        
        return result
    
    
    def delete_entry(self, entry):
        """ """
        
        if entry in self:
            self.entries.remove(entry)
        else:
            pass
    
    
    def sort(self, criterion, entries):
        """ """
        
        if criterion == "Vorname":
            entries.sort(key = attrgetter("first_name", "second_name", \
                        "city", "postal_code", "street", "phone_number"))
            return entries
                         
        elif criterion == "Nachname":
            entries.sort(key = attrgetter("second_name", "first_name", \
                        "city", "postal_code", "street", "phone_number"))
            return entries
                         
        elif criterion == "Stadt":
            entries.sort(key = attrgetter("city", "second_name", \
                        "first_name", "postal_code", "street", "phone_number"))
            return entries
            
        elif criterion == "PLZ":
            entries.sort(key = attrgetter("postal_code", "second_name", \
                        "first_name", "city", "street", "phone_number"))
            return entries
            
        elif criterion == "Straße":
            entries.sort(key = attrgetter("street", "second_name", \
                        "first_name", "city", "postal_code", "phone_number"))
            return entries
                        
        elif criterion == "Telefonnummer":
            entries.sort(key = attrgetter("phone_number", "second_name", \
                        "first_name", "city", "postal_code", "street"))
            return entries
            
        else: pass
        
        
    def write_to_file(self, file_name):
        """ """
        
        output = open(file_name, "wb")
        pickle.dump(self.entries, output)
        output.close()
        
    
    def read_from_file(self, file_name):
        """ """
        
        if os.path.isfile(file_name):
            input = open(file_name, "rb")
            entries = pickle.load(input)
            return entries
            input.close()
        else:
            self.write_to_file(file_name, [])
            return []
            

    def generate_testbook(self):
        """ """
        
        entries = [PhoneBookEntry(random.sample(constants.FIRST_NAMES, 1)[0], \
                   random.sample(constants.SECOND_NAMES, 1)[0], \
                   random.sample(constants.CITIES, 1)[0], \
                   random.sample(constants.POSTAL_CODES, 1)[0], \
                   random.sample(constants.STREETS, 1)[0], \
                   random.sample(constants.PHONE_NUMBERS, 1)[0])
                   for i in range(20)]
                    
        return entries
        

    
if __name__ == "__main__":
    
    """
    fn1 = "testbuch1"
    pb1 = PhoneBook(fn1)
    print("pb1.entries =", pb1.entries)
    """
    
    fn2 = "Example_PhoneBook"
    pb2 = PhoneBook(fn2)
    #pb2.write_to_file("Example_PhoneBook.pkl")
    
    print("Example_PhoneBook")
    for entry in pb2.entries:
        print(entry.to_list())
    """
    #print(pb2.entries)
    print("Mozart")
    print(pb2.search(["Nachname", "Mozart"]))
    
    criterion = "Nachname"
    l = pb2.sort(criterion, pb2.entries)
    print(criterion)
    for entry in l:
        print(entry.to_list())
    for entry in l:
        print(repr(entry))
    entry1 = PhoneBookEntry("a", "b", "c", "d", "e")
    entry2 = PhoneBookEntry("a", "b", "c", "d", "e")
    entry3 = PhoneBookEntry("a", "b", "c", "d", "f")
    entry4 = PhoneBookEntry("a", "b", "c", "d", "f")
    print("entry1.to_list() =", entry1.to_list())
    
    
    pb1.add_entry(entry1)
    pb1.add_entry(entry3)
    
    for entry in pb1.entries:
        print(entry.to_list())
    input()
    pb1.delete_entry(entry1)
    for entry in pb1.entries:
        print(entry.to_list())
    print("pb1.entries =", pb1.entries)    
    pb1.write_to_file("testbuch1.pkl")
    pb1.add_entry(entry2)
    r = (entry1.is_equal(entry2))
    l = [entry1, entry2, entry4]
    lr = (entry3 in l)
    print(r)
    print(lr)
    """