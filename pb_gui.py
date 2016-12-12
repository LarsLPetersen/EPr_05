"""..."""

__author__ = "6360278: Qasim Raza, 6290157: Lars Petersen"
__copyright__ = ""
__credits__ = "" 
__email__ = "qasimr@icloud.com, petersen@informatik.uni-frankfurt.de"

import tkinter as tk
import sys
from tkinter import filedialog
from tkinter import messagebox
#import pb_phonebook
from pb_phonebook import *
import pb_constants
import pickle

class ApplicationGUI:
    """ """
    
    def __init__(self):
        """ """
        global window
        window = tk.Tk()
        window.title("Telefonbuch Manager")
          
        # Create a menu bar
        menubar = tk.Menu(window)
        window.config(menu = menubar) # Display the menu bar

        # menu offering general actions
        general_menu = tk.Menu(menubar, tearoff = 0)
        menubar.add_cascade(label = "Telefonbuch Manager", menu = general_menu)
        
        general_menu.add_command(label = "Info", command = self.info)          
        general_menu.add_separator()
        general_menu.add_command(label = "Neues Telefonbuch anlegen", command = self.new_phonebook)
        general_menu.add_command(label = "Telefonbuch öffnen...", command = self.open_phonebook)
        general_menu.add_separator()
        general_menu.add_command(label = "Telefonbuch Manager beenden", command = self.quit)
        
        # menu offering actions on the open phonebook
        phonebook_menu = tk.Menu(menubar, tearoff = 0)  
        menubar.add_cascade(label = "Telefonbuch", menu = phonebook_menu)
        
        phonebook_menu.add_command(label = "Durchsuchen...", command = self.dummy)
        phonebook_menu.add_command(label = "Sortieren...", command = self.dummy)
        phonebook_menu.add_separator()
        phonebook_menu.add_command(label = "Speichern", command = self.dummy)          
        phonebook_menu.add_command(label = "Speichern unter...", command = self.dummy)
        phonebook_menu.add_separator()
        phonebook_menu.add_command(label = "Schließen", command = self.dummy)
          
        # menu offering actions concerning phonebook a single phonebook entry
        entry_menu = tk.Menu(menubar, tearoff = 0)  
        menubar.add_cascade(label = "Eintrag", menu = entry_menu)
        
        entry_menu.add_command(label = "Bearbeiten...", command = self.dummy)          
        entry_menu.add_command(label = "Löschen", command = self.dummy)
        
        tk.mainloop()

    
    def info(self):
        """ """
        
        messagebox.showinfo(title = "Info", message = pb_constants.GUI_INFO)
        
        
    def new_phonebook(self):
        """ """
        
        file_name = filedialog.asksaveasfilename(defaultextension = ".pkl", initialfile = "Telefonbuch_XY")
        
        if file_name != "":
            phone_book = PhoneBook(file_name)
            return phone_book
        else: pass
        
            
    def open_phonebook(self):
        """ """
        
        file_name = filedialog.askopenfilename(filetypes = [("Pickle", ".pkl")])              
        
        if file_name != "":
            phone_book = PhoneBook(file_name)
            self.show_phonebook(phone_book)
        else: pass
        
    
    def show_phonebook(self, phone_book):
        """ """
        global window 
        lb = tk.Listbox(window)
        index = 1
        for entry in phone_book.entries:
            lb.insert(index,repr(entry))
            index += 1
        lb.pack()
        
        
    def quit(self):
        """ """
        
        sys.exit()
        
            
    def dummy(self):
        print('dummy called')
     
 
 
if __name__ == "__main__":
    
    gui = ApplicationGUI()