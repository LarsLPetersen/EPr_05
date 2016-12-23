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
from functools import partial


class SortChoice:
    """ """
    def __init__(self):
        """ """
        self.choice = None
        self.root = tk.Toplevel()
        #self.root.resizable(0,0)
        self.container = tk.LabelFrame(self.root, text = "Sortierkriterium", width = 35)
        self.container.pack()
        self.choices = pb_constants.GUI_SORT_CHOICES
        
        global choice
        choice = tk.StringVar()
        choice.set(self.choices[2])
        
        self.sbox = tk.Spinbox(self.container, textvariable = choice, \
                values = self.choices, command = lambda: choice.get(), state = "readonly").grid(row = 0)
        self.button_sort = tk.Button(self.container, text = "Sortieren", \
                command = self.get_choice).grid(row = 1, ipady = 5)
        
    
    def get_choice(self):
        """ """
        global choice
        return(choice.get())
    
        
class Application:
    """ """
    
    def __init__(self):
        """ """
        
        self.current_phonebook = None
        self.current_phonebook_list = None
        
        self.phonebook_name = "N/A"
        
        #global root
        self.root = tk.Tk()
        self.root.title("Telefonbuch Manager")
        #self.root.resizable(0,0)
          
        # Create a menu bar
        self.menubar = tk.Menu(self.root)
        self.root.config(menu = self.menubar) # Display the menu bar

        # menu offering general actions
        self.general_menu = tk.Menu(self.menubar, tearoff = 0)
        self.menubar.add_cascade(label = "Telefonbuch Manager", menu = self.general_menu)
        
        self.general_menu.add_command(label = "Info", command = self.info)          
        self.general_menu.add_separator()
        self.general_menu.add_command(label = "Telefonbuch Manager beenden", command = self.quit)
         
        # menu offering actions on the open phonebook
        self.phonebook_menu = tk.Menu(self.menubar, tearoff = 0)  
        self.menubar.add_cascade(label = "Telefonbuch", menu = self.phonebook_menu)
        self.phonebook_menu.add_command(label = "Neu", command = self.new_phonebook)
        self.phonebook_menu.add_command(label = "Öffnen...", \
                command = self.open_phonebook)
                #command = partial(self.open_phonebook, (self.middle_frame, self.phonebook_list)))
        self.phonebook_menu.add_separator()
    

        self.phonebook_menu.add_command(label = "Durchsuchen...", \
                command = self.search_phonebook)
        
        self.phonebook_menu.add_command(label = "Sortieren...",  \
                command = self.sort_phonebook)
        self.phonebook_menu.add_separator()
        
        
        self.phonebook_menu.add_command(label = "Speichern", \
                command = self.save_phonebook)          
        self.phonebook_menu.add_command(label = "Speichern unter...", \
                command = self.save_phonebook_as)
        self.phonebook_menu.add_separator()
        self.phonebook_menu.add_command(label = "Schließen", \
                command = self.close_phonebook)
         
        # menu offering actions concerning phonebook a single phonebook entry
        """
        self.entry_menu = tk.Menu(self.menubar, tearoff = 0)  
        self.menubar.add_cascade(label = "Eintrag", menu = self.entry_menu)
        
        self.entry_menu.add_command(label = "Bearbeiten...", command = self.dummy)          
        self.entry_menu.add_command(label = "Löschen", command = self.dummy)
        """
        
        self.top_frame = tk.LabelFrame(self.root, text = "Allgemeine Information")
        self.top_frame.pack(side = "top", fill = "both", expand = "yes")
        
        global phonebook_name
        phonebook_name = tk.StringVar()
        phonebook_name.set("Aktuelles Telefonbuch: N/A")
        self.l1 = tk.Label(self.top_frame, textvariable = phonebook_name)
        self.l1.grid(row = 0, sticky = tk.W)
        
        #self.l1 = tk.Label(self.top_frame, text = "Aktuelles Telefonbuch: {}".format(self.phonebook_name))
        #self.l1.pack(side = "top")
        
        global num_entries
        num_entries = tk.StringVar()
        num_entries.set("Anzahl Einträge: N/A")
        self.l2 = tk.Label(self.top_frame, textvariable = num_entries)
        self.l2.grid(row = 1, sticky = tk.W)
        
        #self.l2 = tk.Label(self.top_frame, text = "Anzahl der Einträge:")
        #self.l2.pack(side = "bottom")
        
        self.middle_frame = tk.LabelFrame(self.root, text = "Einträge")
        self.middle_frame.pack()
        
        #self.phonebook_list = PhonebookList(self.middle_frame, None)
        self.phonebook_list = tk.Listbox(self.middle_frame, height = 20, width = 85)
        self.phonebook_list.pack()
        
        
        self.bottom_frame = tk.LabelFrame(self.root, text = "Ausgewählten Eintrag ...")
        self.bottom_frame.pack(side = "bottom", fill = "both")

        self.button_modify = tk.Button(self.bottom_frame, text = "bearbeiten", command = self.dummy)
        self.button_modify.pack(side = "left")
        
        self.button_delete = tk.Button(self.bottom_frame, text = "löschen", default = tk.DISABLED, command = self.dummy)
        self.button_delete.pack(side = "right")

        tk.mainloop()

    
    def search_phonebook(self):
        """ """
        pass
        
    
    def sort_phonebook(self):
        """ """
        print("Sortieren...")
        if self.current_phonebook is not None:
            sc = SortChoice()
            criterion = sc.get_choice()
            print(criterion)
            self.current_phonebook.entries = self.current_phonebook.sort(criterion, self.current_phonebook.entries) 
        else: 
            info = "Sortieren nicht möglich.\n\nAktuell kein Telefonbuch offen."
            messagebox.showinfo(title = "Info", message = info)
        self.update()
        
        
    def info(self):
        """ """
        
        messagebox.showinfo(title = "Info", message = pb_constants.GUI_INFO)
    
    
    def update(self):
        """ """
        global phonebook_name
        global num_entries
        
        if self.current_phonebook is None:
            phonebook_name.set("Aktuelles Telefonbuch: N/A")
            num_entries.set("Anzahl Einträge: N/A")
            self.phonebook_list.delete(0, tk.END)
        else:
            phonebook_name.set("Aktuelles Telefonbuch: {}".format(self.current_phonebook.file_name))
            num_entries.set("Anzahl Einträge: {}".format(self.current_phonebook.nb_of_entries))
            self.phonebook_list.delete(0, tk.END)
            index = 1
            for entry in self.current_phonebook.entries:
                self.phonebook_list.insert(index, entry)
                index += 1
        
        self.l1.update()
        self.l2.update()
        self.phonebook_list.update()
            

    def close_phonebook(self):
        """ """
        print("Schließen...")
        if self.current_phonebook is not None:
            self.current_phonebook = None
        else: 
            info = "Aktuell kein Telefonbuch offen."
            messagebox.showinfo(title = "Info", message = info)
        self.update()
    
    
    def save_phonebook(self):
        """ """
        print("Speichern...")
        if self.current_phonebook is not None:
            self.current_phonebook.write_to_file(self.current_phonebook.file_name, self.current_phonebook.entries)
            info = "Telefonbuch {} wurde gespeichert.".format(self.current_phonebook.file_name)
            messagebox.showinfo(title = "Info", message = info)
        else:
            info = "Speichern nicht möglich.\n\nAktuell kein Telefonbuch offen."
            messagebox.showinfo(title = "Info", message = info)
        
    
    def save_phonebook_as(self):
        """ """
        print("Speichern unter...")
        if self.current_phonebook is not None:
            file_name = filedialog.asksaveasfilename(defaultextension = ".pkl", initialfile = "Telefonbuch_XY")
        
            if file_name != "":
                phone_book = PhoneBook(file_name)
                info = "Telefonbuch wurde unter {} gespeichert.".format(file_name)
                messagebox.showinfo(title = "Info", message = info)
            else: pass
        else:
            info = "Speichern nicht möglich.\n\nAktuell kein Telefonbuch offen."
            messagebox.showinfo(title = "Info", message = info)
                           
    
    def new_phonebook(self):
        """ """
        print("Neues Telefonbuch...")
        file_name = filedialog.asksaveasfilename(defaultextension = ".pkl", initialfile = "Telefonbuch_XY")
        
        if file_name != "":
            phone_book = PhoneBook(file_name)
            info = "Telefonbuch {} wurde angelegt.".format(file_name)
            messagebox.showinfo(title = "Info", message = info)
        else: pass
        
            
    def open_phonebook(self):
        """ """
        print("Telefonbuch öffnen...")
        file_name = filedialog.askopenfilename(filetypes = [("Pickle", ".pkl")])              
        
        if file_name != "":
            self.current_phonebook = PhoneBook(file_name)
            self.update()
        else: pass
        

    def quit(self):
        """ """
        sys.exit()
        
            
    def dummy(self):
        print("Dummy...")

     

if __name__ == "__main__":
    
    gui = Application()