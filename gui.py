import tkinter as tk
import tkinter.ttk as ttk
import storage
import logic
import sv_ttk
import crypto
import secrets
import sys
import os

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)


current_master_password = None

def run_app():
    root = tk.Tk()
    root.title("Moha's Password Manager")
    image_logo = tk.PhotoImage(file=resource_path("logo.png"))
    root.iconphoto(True, image_logo)
    image_logo = image_logo.subsample(4, 4)
    image = ttk.Label(root, image=image_logo)
    image.place(relx=1.0, rely=1.0, anchor="se")
    storage.create_table()
    root.geometry("700x700")
    if storage.list_all():
        returning_user_screen(root)
    else:
        show_add_entry_screen(root)
    sv_ttk.set_theme("dark")
    root.mainloop()
    
        
def show_add_entry_screen(root):
    # field 1
    master_password_entry = ttk.Entry(root, show="*")
    master_password_label = ttk.Label(root, text="Insert your master password:")
    master_password_label.place(relx= 0.2, rely=0.4, anchor="center")
    master_password_entry.place(relx=0.6, rely=0.4, relwidth=0.5, anchor="center")

    # field 2
    service_name_entry = ttk.Entry(root)
    service_name_label = ttk.Label(root, text = "Service name: ")
    service_name_label.place(relx=0.2, rely=0.47, anchor="center")
    service_name_entry.place(relx=0.6, rely=0.47, relwidth=0.5, anchor="center")

    # field 3
    user_email_entry = ttk.Entry(root)
    user_email_label = ttk.Label(root, text="Please insert the username/email: ")
    user_email_label.place(relx=0.05, rely=0.54, anchor="w")
    user_email_entry.place(relx=0.6, rely=0.54, relwidth=0.5, anchor="center")

    # field 4
    password_entry = ttk.Entry(root, show="*")
    password_label = ttk.Label(root, text="Please insert the password: ")
    password_label.place(relx=0.08, rely=0.61, anchor="w")
    password_entry.place(relx=0.6, rely=0.61, relwidth=0.5, anchor="center")



    def submit_entry():
        the_master_password = master_password_entry.get()
        global current_master_password
        current_master_password = the_master_password
        the_service_name = service_name_entry.get()
        the_user_email = user_email_entry.get()
        the_password = password_entry.get()
        logic.new_entry(the_master_password, the_service_name, the_user_email, the_password)
        clear_screen(root)
        show_vault_screen(root)

    #button 1
    button_for_entry = ttk.Button(root, text="Submit", command=submit_entry)
    button_for_entry.place(relx=0.8, rely=0.7, anchor="center")

    def generate_pass():
        randnum = secrets.SystemRandom().randint(8, 18)
        randompass = crypto.generate_password(randnum)
        password_entry.delete(0, tk.END)
        password_entry.insert(0, randompass)

    #button 2
    button_for_generation = ttk.Button(root, text="Generate Password", command=generate_pass)
    button_for_generation.place(relx=0.2, rely=0.7, anchor="center")

def show_vault_screen(root):
    def populate_listbox(entries):
        list_funsies.delete(0, tk.END)
        ids.clear()
        for entry in entries:
            service = entry[0]
            ids.append(entry[1])
            list_funsies.insert(tk.END, service)

    list_funsies = tk.Listbox(root)
    entries = storage.list_all()
    ids = []
    populate_listbox(entries)

    list_funsies.place(relx=0.28, rely=0.1, relwidth=0.5, relheight=0.7, anchor="n")
    def on_entry_click(event):
        idHelper = list_funsies.curselection()
        logical = logic.retrieve_entry(current_master_password, ids[idHelper[0]])
        popup = tk.Toplevel(root)
        user_email_entry = ttk.Entry(popup)
        popup.geometry("400x100")
        user_email_entry.place(relx=0.45, rely=0.1, relwidth=0.8, anchor="n")
        user_email_entry.insert(0, logical['user_or_email'])
        password_entry = ttk.Entry(popup)
        password_entry.place(relx=0.45, rely=0.4, relwidth=0.8, anchor="n")
        password_entry.insert(0, logical['password'])
    list_funsies.bind("<<ListboxSelect>>", on_entry_click)

    def delete_entry():
        idHelper = list_funsies.curselection()
        storage.delete_entry(ids[idHelper[0]])
        clear_screen(root)
        show_vault_screen(root)

    deleteButton = ttk.Button(root, text="Delete", command=delete_entry)
    deleteButton.place(relx=0.28, rely=0.85, anchor="center")

    def add_another_entry():
        clear_screen(root)
        show_new_entry_screen(root)
    
    addButton = ttk.Button(root, text = "Add another entry", command=add_another_entry)
    addButton.place(relx=0.13, rely=0.85, anchor="center")

    def run_search():
        search_term = search_entry.get()
        results = storage.search_entries(search_term)
        populate_listbox(results)

    search_label = ttk.Label(root, text="Search for a service name:")
    search_label.place(relx=0.315, rely=0.05, anchor="w")
    search_entry = ttk.Entry(root)
    search_entry.place(relx=0.7, rely=0.05, relwidth=0.3, anchor="center")


    searchButton = ttk.Button(root, text="Search", command=run_search)
    searchButton.place(relx=0.9, rely=0.05, anchor="center")

    



def returning_user_screen(root):
    master_password_entry = ttk.Entry(root, show="*")
    master_password_label = ttk.Label(root, text="Insert your master password: ")
    master_password_label.place(relx=0.1, rely=0.4, anchor="w")
    master_password_entry.place(relx=0.6, rely=0.4, relwidth=0.3, anchor="center")


    def comparison():
        compare = logic.request_master_password(master_password_entry.get())
        if compare:
            global current_master_password
            current_master_password = master_password_entry.get() 
            clear_screen(root)
            show_vault_screen(root)
        else:
            master_password_label.config(text="Wrong master password.")

    master_password_button = ttk.Button(root, text="Submit", command=comparison)
    master_password_button.place(relx=0.82, rely=0.4, relwidth=0.1, anchor="center")


def clear_screen(root):
    for widget in root.winfo_children():
        widget.destroy()


def show_new_entry_screen(root):
    # field 1
    service_name_entry = ttk.Entry(root)
    service_name_label = ttk.Label(root, text = "Service name: ")
    service_name_label.place(relx=0.2, rely=0.47, anchor="center")
    service_name_entry.place(relx=0.6, rely=0.47, relwidth=0.5, anchor="center")

    # field 2
    user_email_entry = ttk.Entry(root)
    user_email_label = ttk.Label(root, text="Please insert the username/email: ")
    user_email_label.place(relx=0.05, rely=0.54, anchor="w")
    user_email_entry.place(relx=0.6, rely=0.54, relwidth=0.5, anchor="center")

    # field 3
    password_entry = ttk.Entry(root, show="*")
    password_label = ttk.Label(root, text="Please insert the password: ")
    password_label.place(relx=0.08, rely=0.61, anchor="w")
    password_entry.place(relx=0.6, rely=0.61, relwidth=0.5, anchor="center")

    def submit_entry():
        the_service_name = service_name_entry.get()
        the_user_email = user_email_entry.get()
        the_password = password_entry.get()
        logic.new_entry(current_master_password, the_service_name, the_user_email, the_password)
        clear_screen(root)
        show_vault_screen(root)

        #button 1
    button_for_entry = ttk.Button(root, text="Submit", command=submit_entry)
    button_for_entry.place(relx=0.8, rely=0.7, anchor="center")

    def generate_pass():
        randnum = secrets.SystemRandom().randint(8, 18)
        randompass = crypto.generate_password(randnum)
        password_entry.delete(0, tk.END)
        password_entry.insert(0, randompass)

    
    button_for_generation = ttk.Button(root, text="Generate Password", command=generate_pass)
    button_for_generation.place(relx=0.2, rely=0.7, anchor="center")

    