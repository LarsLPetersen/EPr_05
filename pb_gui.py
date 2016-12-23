"""Contains the main GUI classes of the Application

   Application   -- main window
   SearchChoice  -- window for setting the search criteria for the phonebook
   SortChoice    -- window for setting the sort criteria of the phonebook    
"""

__author__ = "6360278: Qasim Raza, 6290157: Lars Petersen"
__copyright__ = ""
__credits__ = "" 
__email__ = "qasimr@icloud.com, petersen@informatik.uni-frankfurt.de"


# built-in modules
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import sys
import pickle

# customized modules
from pb_phonebook import *
import pb_constants


class SearchChoice:
    """Window for setting the search criteria for the phonebook"""
    
    def __init__(self, parent):
        """Creates the SearchChoice-Window"""
        
        self.root = tk.Toplevel()
        self.container = tk.LabelFrame(self.root, text = "Suchkriterien")
        self.container.pack()
        self.choices = pb_constants.GUI_SORT_CHOICES
        self.parent = parent
        
        global choice
        choice = tk.StringVar()
        choice.set("")
        
        global entry
        entry = tk.StringVar()
        entry.set("")
        
        self.sbox = tk.Spinbox(self.container, textvariable = choice, \
                values = self.choices, command = lambda: choice.get(), \
                state = "readonly").grid(row = 0, column = 0)
        
        self.entry = tk.Entry(self.container, textvariable = entry)
        self.entry.grid(row = 0, column = 1)
        
        self.button_search = tk.Button(self.container, text = "Suchen", \
                command = self.search_entries)
        self.button_search.grid(row = 1, column = 1, ipady = 5)
        
    
    def search_entries(self):
        """Performs the actual search on the current phonebook entries"""
        
        global choice
        self.parent.search_criterion[0] = choice.get()
        
        global entry
        self.parent.search_criterion[1] = entry.get()
        
        self.parent.current_phonebook_list = \
            self.parent.current_phonebook.search(self.parent.search_criterion)
        self.parent.update()


class SortChoice:
    """Window for setting the sort criterium for the current phonebook"""
    
    def __init__(self, parent):
        """ """
        self.root = tk.Toplevel()
        self.container = tk.LabelFrame(self.root, text = "Sortierkriterium")
        self.container.pack()
        self.choices = pb_constants.GUI_SORT_CHOICES
        self.parent = parent
        
        global choice
        choice = tk.StringVar()
        choice.set(self.choices[2])
        
        self.sbox = tk.Spinbox(self.container, textvariable = choice, \
                values = self.choices, command = lambda: choice.get(), \
                state = "readonly").grid(row = 0)
        self.button_sort = tk.Button(self.container, text = "Sortieren", \
                command = self.sort_entries).grid(row = 1, ipady = 5)
        
    
    def sort_entries(self):
        """Performs the actual sorting on the phonebook entries"""
        
        global choice
        self.parent.sort_criterion = choice.get()
        self.parent.current_phonebook_list = \
            self.parent.current_phonebook.sort(self.parent.sort_criterion,\
                                        self.parent.current_phonebook.entries)
        self.parent.update()
        
        
class Application:
    """ """
    
    def __init__(self):
        """ """
        
        self.current_phonebook = None
        self.original_phonebook = None
        self.current_phonebook_list = None
        self.current_entry = None
        self.sort_criterion = None
        self.search_criterion = [None, None]
        
        self.root = tk.Tk()
        self.root.title("Telefonbuch Manager")
          
        # Create a menu bar
        self.menubar = tk.Menu(self.root)
        self.root.config(menu = self.menubar) # Display the menu bar

        # menu offering general actions on the manager
        self.general_menu = tk.Menu(self.menubar, tearoff = 0)
        self.menubar.add_cascade(label = "Manager", menu = self.general_menu)
        self.general_menu.add_command(label = "Info", command = self.info)          
        self.general_menu.add_separator()
        self.general_menu.add_command(label = "Manager beenden", \
                                      command = self.quit)
         
        # menu offering actions on phonebooks
        self.phonebook_menu = tk.Menu(self.menubar, tearoff = 0)  
        self.menubar.add_cascade(label = "Telefonbuch", \
                                 menu = self.phonebook_menu)
        self.phonebook_menu.add_command(label = "Neu", \
                                        command = self.new_phonebook)
        self.phonebook_menu.add_command(label = "Öffnen...", \
                                        command = self.open_phonebook)
        self.phonebook_menu.add_separator()
        self.phonebook_menu.add_command(label = "Durchsuchen", \
                                        command = self.call_search_dialog)
        self.phonebook_menu.add_command(label = "Sortieren",  \
                                        command = self.call_sort_dialog)
        self.phonebook_menu.add_command(label = "Zurücksetzen",  \
                                        command = self.back_to_start)
        self.phonebook_menu.add_separator()
        self.phonebook_menu.add_command(label = "Speichern", \
                                        command = self.save_phonebook)          
        self.phonebook_menu.add_command(label = "Speichern unter...", \
                                        command = self.save_phonebook_as)
        self.phonebook_menu.add_separator()
        self.phonebook_menu.add_command(label = "Schließen", \
                                        command = self.close_phonebook)
         
        # menu offering actions concerning a single phonebook entry
        self.entry_menu = tk.Menu(self.menubar, tearoff = 0)  
        self.menubar.add_cascade(label = "Eintrag", menu = self.entry_menu)
        self.entry_menu.add_command(label = "Neu...", command = self.dummy)          
        self.entry_menu.add_command(label = "Bearbeiten...", \
                                    command = self.dummy)          
        self.entry_menu.add_command(label = "Löschen", command = self.dummy)
        
        
        # building the widgets
        self.top_frame = tk.LabelFrame(self.root, \
                                       text = "Allgemeine Information")
        self.top_frame.pack(side = "top", fill = "both", expand = "yes")
        
        global phonebook_name
        phonebook_name = tk.StringVar()
        phonebook_name.set("Aktuelles Telefonbuch: N/A")
        
        self.label_pb_name = tk.Label(self.top_frame, \
                                      textvariable = phonebook_name)
        self.label_pb_name.grid(row = 0, sticky = tk.W)
        
        global num_entries
        num_entries = tk.StringVar()
        num_entries.set("Anzahl Einträge: N/A")
        
        self.label_pb_count = tk.Label(self.top_frame, \
                                       textvariable = num_entries)
        self.label_pb_count.grid(row = 1, sticky = tk.W)
        
        self.middle_frame = tk.LabelFrame(self.root, text = "Einträge")
        self.middle_frame.pack()
        
        # the Listbox showing all the Entries
        self.phonebook_list = tk.Listbox(self.middle_frame, \
                                         height = 20, width = 85)
        self.phonebook_list.pack()
        
        tk.mainloop()

    
    def back_to_start(self):
        """Reset the list of entries to get back to original state"""
        
        if self.current_phonebook is not None:
            self.current_phonebook = self.original_phonebook
            self.current_phonebook_list = self.current_phonebook.entries
            self.update()
        else: 
            info = "Zurücksetzen nicht möglich.\n\n" + \
                   "Aktuell kein Telefonbuch offen."
            messagebox.showinfo(title = "Info", message = info)
        
        
    def call_sort_dialog(self):
        """Calls the dialog for setting the sort criterium"""
        
        if self.current_phonebook is not None:
            sort_dialog = SortChoice(self)
        else: 
            info = "Sortieren nicht möglich.\n\nAktuell kein Telefonbuch offen."
            messagebox.showinfo(title = "Info", message = info)
        self.update()
        
    
    def call_search_dialog(self):
        """Call the dialog for setting the search criteria"""
        
        if self.current_phonebook is not None:
            sc = SearchChoice(self)
        else: 
            info = "Suche nicht möglich.\n\nAktuell kein Telefonbuch offen."
            messagebox.showinfo(title = "Info", message = info)
        self.update()
    
    
    def info(self):
        """Prints the author info into a message box"""
        
        messagebox.showinfo(title = "Info", message = pb_constants.GUI_INFO)
    
    
    def echo(self, entry):
        """Brings a PhoneBookEntry into a more readable string format"""
        
        result = ""
        result += entry.first_name.ljust(15) + entry.second_name.ljust(15) + \
                  entry.city.ljust(15) + entry.postal_code.ljust(9) + \
                  entry.street.ljust(20) + entry.phone_number.ljust(15)
        return result
        
        
    def update(self):
        """Updates the widgets to contain the current information"""
        
        global phonebook_name
        global num_entries
        
        if self.current_phonebook is None:
            phonebook_name.set("Aktuelles Telefonbuch: N/A")
            num_entries.set("Anzahl Einträge: N/A")
            self.phonebook_list.delete(0, tk.END)
        else:
            info_phonebook = "Aktuelles " + \
                    "Telefonbuch: {}".format(self.current_phonebook.file_name)
            phonebook_name.set(info_phonebook)
            
            info_num_entries = "Anzahl " + \
                    "Einträge: {}".format(self.current_phonebook.nb_of_entries)
            num_entries.set(info_num_entries)
            
            self.phonebook_list.delete(0, tk.END)
            index = 1
            for entry in self.current_phonebook_list:
                self.phonebook_list.insert(index, self.echo(entry))
                index += 1
        
        self.label_pb_name.update()
        self.label_pb_count.update()
        self.phonebook_list.update()
            

    def close_phonebook(self):
        """Closes the current PhoneBook - its entries are no longer visible"""
        
        if self.current_phonebook is not None:
            self.current_phonebook = None
        else: 
            info = "Aktuell kein Telefonbuch offen."
            messagebox.showinfo(title = "Info", message = info)
        self.update()
    
    
    def save_phonebook(self):
        """Saves the current PhoneBook to disk - under the current name"""
        
        if self.current_phonebook is not None:
            self.current_phonebook.write_to_file(\
              self.current_phonebook.file_name, self.current_phonebook.entries)
            info = "Telefonbuch " + self.current_phonebook.file_name + \
                   " wurde gespeichert."
            messagebox.showinfo(title = "Info", message = info)
        else:
            info = "Speichern nicht möglich.\n\nAktuell kein Telefonbuch offen."
            messagebox.showinfo(title = "Info", message = info)
        
    
    def save_phonebook_as(self):
        """Saves the current PhoneBook to disk - under a possibly new name"""
        
        if self.current_phonebook is not None:
            file_name = filedialog.asksaveasfilename(defaultextension = ".pkl",\
                                             initialfile = "Telefonbuch_XY")
        
            if file_name != "":
                phone_book = PhoneBook(file_name)
                info = "Telefonbuch wurde unter " + file_name + " gespeichert."
                messagebox.showinfo(title = "Info", message = info)
            else: pass
        else:
            info = "Speichern nicht möglich.\n\nAktuell kein Telefonbuch offen."
            messagebox.showinfo(title = "Info", message = info)
                           
    
    def new_phonebook(self):
        """Creates a new PhoneBook and saves it"""
        
        file_name = filedialog.asksaveasfilename(defaultextension = ".pkl", \
                                            initialfile = "Telefonbuch_XY")
        
        if file_name != "":
            phone_book = PhoneBook(file_name)
            info = "Telefonbuch {} wurde angelegt.".format(file_name)
            messagebox.showinfo(title = "Info", message = info)
        else: pass
        
            
    def open_phonebook(self):
        """Opens an existing internal PhoneBook and displays its contents"""
        
        file_name = filedialog.askopenfilename(filetypes = [("Pickle", ".pkl")])              
        
        if file_name != "":
            self.current_phonebook = PhoneBook(file_name)
            self.original_phonebook = self.current_phonebook
            self.current_phonebook_list = PhoneBook(file_name).entries
            self.update()
        else: pass
        

    def quit(self):
        """Quits the application"""
        
        sys.exit()


    def dummy(self):
        """Partially shows what has not been implemented yet in the GUI"""
        
        info = "Funktionalität noch nicht umgesetzt..."
        messagebox.showinfo(title = "Info", message = info)
        
        
if __name__ == "__main__":
    gui = Application()