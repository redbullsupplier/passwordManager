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
    master_password_label = ttk.Label(root, text="Insert your master password.")
    master_password_label.pack()
    master_password_entry.pack(pady=10, padx=20)

    # field 2
    service_name_entry = ttk.Entry(root)
    service_name_label = ttk.Label(root, text = "Service name")
    service_name_label.pack()
    service_name_entry.pack(pady=10, padx=20)

    # field 3
    user_email_entry = ttk.Entry(root)
    user_email_label = ttk.Label(root, text="Please insert the username/email.")
    user_email_label.pack()
    user_email_entry.pack(pady=10, padx=20)

    # field 4
    password_entry = ttk.Entry(root, show="*")
    password_label = ttk.Label(root, text="Please insert the password.")
    password_label.pack()
    password_entry.pack(pady=10, padx=20)



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

    # button 1
    button_for_entry = ttk.Button(root, text="Submit", command=submit_entry)
    button_for_entry.pack(pady=10, padx=20)

    def generate_pass():
        randnum = secrets.SystemRandom().randint(8, 18)
        randompass = crypto.generate_password(randnum)
        password_entry.delete(0, tk.END)
        password_entry.insert(0, randompass)

    # button 2
    button_for_generation = ttk.Button(root, text="Generate Password", command=generate_pass)
    button_for_generation.pack()

def show_vault_screen(root):
    list_funsies = tk.Listbox(root)
    entries = storage.list_all()
    ids = []
    for entry in entries:
        service = entry[0]
        ids.append(entry[1])
        list_funsies.insert(tk.END, service)

    list_funsies.pack()
    def on_entry_click(event):
        idHelper = list_funsies.curselection()
        logical = logic.retrieve_entry(current_master_password, ids[idHelper[0]])
        popup = tk.Toplevel(root)
        user_email_entry = ttk.Entry(popup)
        popup.geometry("200x200")
        user_email_entry.pack()
        user_email_entry.insert(0, logical['user_or_email'])
        password_entry = ttk.Entry(popup)
        password_entry.pack()
        password_entry.insert(0, logical['password'])
    list_funsies.bind("<<ListboxSelect>>", on_entry_click)

    def delete_entry():
        idHelper = list_funsies.curselection()
        storage.delete_entry(ids[idHelper[0]])
        clear_screen(root)
        show_vault_screen(root)

    deleteButton = ttk.Button(root, text="Delete", command=delete_entry)
    deleteButton.pack()

    def add_another_entry():
        clear_screen(root)
        show_new_entry_screen(root)

    addButton = ttk.Button(root, text = "Add another entry", command=add_another_entry)
    addButton.pack()

def returning_user_screen(root):
    master_password_entry = ttk.Entry(root, show="*")
    master_password_label = ttk.Label(root, text="Insert your master password.")
    master_password_label.pack()
    master_password_entry.pack(pady=10, padx=20)
    failure_label = ttk.Label(root)
    failure_label.pack()

    def comparison():
        compare = logic.request_master_password(master_password_entry.get())
        if compare:
            global current_master_password
            current_master_password = master_password_entry.get() 
            clear_screen(root)
            show_vault_screen(root)
        else:
            failure_label.config(text="Wrong master password.")

    master_password_button = ttk.Button(root, text="Submit", command=comparison)
    master_password_button.pack()
    
        
def clear_screen(root):
    for widget in root.winfo_children():
        widget.destroy()


def show_new_entry_screen(root):
    # field 1
    service_name_entry = ttk.Entry(root)
    service_name_label = ttk.Label(root, text = "Service name")
    service_name_label.pack()
    service_name_entry.pack(pady=10, padx=20)

    # field 2
    user_email_entry = ttk.Entry(root)
    user_email_label = ttk.Label(root, text="Please insert the username/email.")
    user_email_label.pack()
    user_email_entry.pack(pady=10, padx=20)

    # field 3
    password_entry = ttk.Entry(root, show="*")
    password_label = ttk.Label(root, text="Please insert the password.")
    password_label.pack()
    password_entry.pack(pady=10, padx=20)

    def submit_entry():
        the_service_name = service_name_entry.get()
        the_user_email = user_email_entry.get()
        the_password = password_entry.get()
        logic.new_entry(current_master_password, the_service_name, the_user_email, the_password)
        clear_screen(root)
        show_vault_screen(root)

    # button 1
    button_for_entry = ttk.Button(root, text="Submit", command=submit_entry)
    button_for_entry.pack(pady=10, padx=20)

    def generate_pass():
        randnum = secrets.SystemRandom().randint(8, 18)
        randompass = crypto.generate_password(randnum)
        password_entry.delete(0, tk.END)
        password_entry.insert(0, randompass)

    # button 2
    button_for_generation = ttk.Button(root, text="Generate Password", command=generate_pass)
    button_for_generation.pack()