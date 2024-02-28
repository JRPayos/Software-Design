import tkinter as tk # tkinter library
from tkinter import *
from tkinter import ttk
from tkinter.ttk import *
from tkinter import messagebox
from tkcalendar import DateEntry
import pyodbc # database connector
from PIL import ImageTk, Image # for image background



# region WINDOW SETTINGS
window = Tk()
window.title("STUDENT MANAGEMENT SYSTEM")
window.resizable(width=False, height=False)
window.geometry('1000x600+60+10')
window.configure(bg='#000000')
# endregion
# region IMAGE Import
background_image = Image.open("computershop.png").resize((1200, 910))
bg = ImageTk.PhotoImage(background_image)
# iconbitmap
window.iconbitmap('D:\Coding\PycharmProjects\Computer Hardware Inventory\CompInv.ico')
# endregion

# region MS ACCESS DATABASE CONNECTOR & CONNECTION
connection_str = r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=D:\Coding\PycharmProjects\Computer Hardware Inventory\CompInventory.accdb;'
conn = pyodbc.connect(connection_str)
c = conn.cursor()
# endregion


# region FRAME

# CANVAS image background

mainframe = tk.Frame(window, width=1000, height=800)
mainframe.pack(fill='both', expand=True)
background_canvas = tk.Canvas(mainframe)
background_canvas.pack(fill='both', expand=1)
background_canvas.create_image(0, -260, image=bg, anchor=NW)
background_canvas.create_text(535, 80, text='COMPUTER HARDWARE EQUIPMENTS LTD.', font=('verdana', 25, 'bold'),
                              fill='#1e4382')
# MAINFRAME connected to CANVAS
loginframe = tk.Frame(mainframe, bg='#1e4382')
loginframe.place(relx=0.5, rely=0.5, anchor='center')


# endregion

# region FUNCTIONS

# goes to the database frame
def gotodatabase():
    loginframe.place_forget()
    database_frame.place(relx=0.13, rely=0.18)
    registerframe.place(relx=0.13, rely=0.7)
    db_button_frame.place(relx=0.7, rely=0.4)

# login for admin
def login():
    admin_user = admin_username_entry.get().strip()
    admin_password = admin_password_entry.get().strip()
    c.execute("SELECT * FROM `admin` WHERE `admin_user` = ? and `admin_password` = ?",
              (f'{admin_user}', f'{admin_password}'))
    user = c.fetchone()
    if user is not None:
        #messagebox.showinfo('Admin Login', 'Admin Logged in')
        gotodatabase()
        c.execute("SELECT * FROM inventory")

        for item in tree.get_children():
            tree.delete(item)

        # loop for database records
        rows = c.fetchall()
        for row in rows:
            print(row)
            tree.insert('', 'end', values=(row.item_id, row.item_name, row.item_inventory, row.last_updated))
        #conn.close()

        # deletes the entries
        admin_username_entry.delete(0, END)
        admin_password_entry.delete(0, END)

    else:
        messagebox.showwarning('Admin Login', 'Wrong Admin Username or Password')

# refresh the records
def refresh():
    #deletes the redundant data
    for item in tree.get_children():
        tree.delete(item)

    #conn.connect()
    c.execute("SELECT * FROM inventory ORDER BY item_id ASC")

    # loop for database records

    rows = c.fetchall()

    for row in rows:
        print(row)
        tree.insert("", 'end', values=(row.item_id, row.item_name, row.item_inventory, row.last_updated))
    #conn.close()

def clear():
    id_entry_reg.delete(0, END)
    in_entry_reg.delete(0, END)
    ic_entry_reg.delete(0, END)

#select a record
def select(e):

    id_entry_reg.delete(0, END)
    selected = tree.focus()
    values = tree.item(selected, 'values')
    id_entry_reg.insert(0, values[0])
    in_entry_reg.insert(0, values[1])
    ic_entry_reg.insert(0, values[2])


# deselect a record
def deselect(e):
    x = tree.selection()
    tree.selection_remove(x)
    clear()

# deletes a record
def delete():
    x = tree.selection()[0]
    tree.delete(x)

    #conn.connect()
    item_id = id_entry_reg.get().strip()
    c.execute("DELETE FROM `inventory` WHERE `item_id` = ?", f'{item_id}')
    conn.commit()

    id_entry_reg.delete(0, END)

    messagebox.showinfo('Invetory Data ', "Item has been deleted successfully")

# check existing sid
def check_itemid(item_id):
    item_id = id_entry_reg.get().strip()
    c.execute("SELECT * FROM `inventory` WHERE `item_id` = ?", f'{item_id}')
    user = c.fetchone()
    if user is not None:
        return True
    else:
        return False

# add/register record
def add():
    # conn.connect()
    item_id = id_entry_reg.get().strip()
    item_name = in_entry_reg.get().strip()
    item_inventory = ic_entry_reg.get().strip()
    dt = lu_de_reg.get_date()
    last_updated = dt.strftime("%Y-%m-%d")


    if len(item_id) > 0 and len(item_name) > 0 and len(item_inventory) > 0 and len(last_updated) > 0:
        if check_itemid(item_id) == False:
            #vals = (item_id, item_name, item_inventory, last_updated,)
            #insert_query = "INSERT INTO `CompInventory`.`inventory` (`item_id`, `item_name`, `item_inventory`, `last_updated`) VALUES (?, ?, ?, ?);"
            c.execute("INSERT INTO `inventory` (`item_id`, `item_name`, `item_inventory`, `last_updated`) VALUES (?, ?, ?, ?);",
                      (f'{item_id}', f'{item_name}', f'{item_inventory}', f'{last_updated}'))
            conn.commit()
            messagebox.showinfo('Inventory added', "Item has been uploaded successfully")

            #clears the entries
            id_entry_reg.delete(0, END)
            in_entry_reg.delete(0, END)
            ic_entry_reg.delete(0, END)


        else:
            messagebox.showwarning('Existing ItemID',
                                   'This Item ID Already Exists or has an Existing Record in the Database')
    else:
        messagebox.showwarning('Empty/Incomplete Fields', 'Please fill all the information')

# update records
def update():
    item_id = id_entry_reg.get().strip()
    item_name = in_entry_reg.get().strip()
    item_inventory = ic_entry_reg.get().strip()
    dt = lu_de_reg.get_date()
    last_updated = dt.strftime("%Y-%m-%d")

#SQL UPDATE problem
    if len(item_id) > 0 and len(item_name) > 0 and len(item_inventory) > 0 and len(last_updated) > 0:
        if check_itemid(item_id) == True:
            c.execute("UPDATE `inventory` SET `item_name` = ?, `item_inventory`= ?, `last_updated` = ? WHERE `item_id` = ?;",
                    ( f'{item_name}', f'{item_inventory}', f'{last_updated}', f'{item_id}'))
            conn.commit()
            messagebox.showinfo('Inventory updated', "Item has been updated successfully")
        else:
            messagebox.showwarning('No Existing ItemID',
                                   'This Item does not exist or has not been added in the Database'
                                   '\nUpdating cannot be done!')

    else:
        messagebox.showwarning('Empty/Incomplete Fields', 'Please fill all the information')



# logout admin
def logout():
    database_frame.place_forget()
    registerframe.place_forget()
    db_button_frame.place_forget()
    loginframe.place(relx=0.5, rely=0.5, anchor='center')
    messagebox.showinfo('Admin Logout', 'Admin Logged out Sucessfully')

def about():
    messagebox.showinfo('About', 'Created by Adamson Computer Engineering Students'
                                 '\nA requirement for Software Design Lecture')

# maximum sid length
def max_sid(*args):
    max_len = 9
    s = sid_var.get()
    if len(s) > max_len:
        sid_var.set(s[:max_len])



# endregion

# region MAINFRAME
style = ttk.Style(window)
style.theme_use('clam')
style.configure('tree.heading', background="blue")

# MENUBAR
menubar = tk.Menu(mainframe)
account_menu = Menu(menubar)
database_menu = Menu(menubar)
account_menu.add_command(label='About', command=about)
account_menu.add_command(label='Logout', command=logout)
account_menu.add_command(label='Exit', command=quit)
menubar.add_cascade(menu=account_menu, label='Admin')
window.configure(menu=menubar)
# endregion

# region DATABASE FRAME
database_frame = Frame(window)

title = Label(database_frame, text="PRODUCT INVENTORY", font=('Helvetica', 15, 'bold'))
title.grid(row=0, column=0, columnspan=2)
tree = ttk.Treeview(database_frame, column=("c1", "c2", "c3", "c4"), show='headings')

tree.column("#1", minwidth=0, width=90, stretch=NO, anchor=CENTER)
tree.heading("#1", text="ITEM ID")
tree.column("#2", minwidth=0, width=120, stretch=NO, anchor=CENTER)
tree.heading("#2", text="ITEM NAME")
tree.column("#3", minwidth=0, width=140, stretch=NO, anchor=CENTER)
tree.heading("#3", text="ITEM INVENTORY")
tree.column("#4", minwidth=0, width=140, stretch=NO, anchor=CENTER)
tree.heading("#4", text="LAST UPDATED")
tree.grid(row=1, column=0)

#treeview keybinds
tree.bind("<ButtonRelease-1>", select)
tree.bind("<Button-1>", deselect)

sb = tk.Scrollbar(database_frame, orient=VERTICAL)
sb.grid(row=1, column=1, sticky=NS)
tree.configure(yscrollcommand=sb.set, selectmode='browse')
sb.configure(command=tree.yview)

# endregion


# region LOGIN PAGE DESIGN
welcome_label = tk.Label(loginframe, text='Welcome Admin!', bg='#1e4382', fg='white', font=('Arial', 17, 'bold'))
welcome_label.grid(row=0, column=0,columnspan=2, padx=10, pady=10)
admin_username_label = tk.Label(loginframe, text='Username:', bg='#1e4382', fg='white', font=('Arial', 15, 'bold'))
admin_username_label.grid(row=1, column=0, padx=10, pady=30)
admin_password_label = tk.Label(loginframe, text='Password:', bg='#1e4382', fg='white', font=('Arial', 15, 'bold'))
admin_password_label.grid(row=2, column=0)

admin_username_entry = tk.Entry(loginframe, font=('Arial', 15))
admin_username_entry.grid(row=1, column=1, padx=10, pady=30)
admin_password_entry = tk.Entry(loginframe, show='*', font=('Arial', 15))
admin_password_entry.grid(row=2, column=1)

admin_login_but1 = tk.Button(loginframe, text='LOGIN', fg='white', bg='black', font=('Arial', 15, 'bold'), width=28,
                             command=login)
admin_login_but1.grid(row=3, column=0, columnspan=2, pady=30)
window.bind('<Return>', lambda event: login())

# endregion


# region REGISTRATION PAGE DESIGN
registerframe = tk.Frame(mainframe, bg='#1e4382')

title_reg = tk. Label(registerframe, text='ITEM INVENTORY', bg='#1e4382', fg='white', font=('Arial', 12, 'bold'))
title_reg.grid(row=0, column=0, columnspan=3)
id_reg = tk.Label(registerframe, text='Item ID:', bg='#1e4382', fg='white', font=('Arial', 12, 'bold'))
id_reg.grid(row=1, column=0, padx=6, pady=6)
in_reg = tk.Label(registerframe, text='Item Name:', bg='#1e4382', fg='white', font=('Arial', 12, 'bold'))
in_reg.grid(row=2, column=0, padx=6, pady=6)
ic_reg = tk.Label(registerframe, text='Item Count:', bg='#1e4382', fg='white', font=('Arial', 12, 'bold'))
ic_reg.grid(row=3, column=0, padx=6, pady=6)
lu_reg = tk.Label(registerframe, text='Last Updated:', bg='#1e4382', fg='white', font=('Arial', 12, 'bold'))
lu_reg.grid(row=1, column=2, padx=6, pady=6)

sid_var = StringVar()
sid_var.trace_variable("w", max_sid)

# ITEM/PRODUCT ENTRIES
id_entry_reg = tk.Entry(registerframe, font=('Arial', 12), textvariable=sid_var)
id_entry_reg.grid(row=1, column=1, padx=6, pady=6)
in_entry_reg = tk.Entry(registerframe, font=('Arial', 12))
in_entry_reg.grid(row=2, column=1, padx=6, pady=6)
ic_entry_reg = tk.Entry(registerframe, font=('Arial', 12))
ic_entry_reg.grid(row=3, column=1, padx=6, pady=6)

lu_frame = tk.Frame(registerframe)
lu_frame.grid(row=2, column=2, padx=6, pady=6)
lu_de_reg = DateEntry(lu_frame, width=20, background="#1e4382", foreground='white', font=('Arial', 11), state='readonly',)
lu_de_reg.grid()
clear_button = tk.Button(registerframe, text='CLEAR ENTRIES', bg='gray', fg='white', font=('Arial', 10, 'bold'), width=20, command=clear)
clear_button.grid(row=3, column=2, padx=6, pady=6)

# DATABASE EDIT BUTTONS
db_button_frame = tk.Frame(mainframe)
register_button = tk.Button(db_button_frame, text='ADD ITEM', bg='gray', fg='white', font=('Arial', 10, 'bold'), width=20,
                            command=add)
register_button.grid(row=0, column=0, pady=5)
update_button = tk.Button(db_button_frame, text='UPDATE ITEM', bg='gray', fg='white', font=('Arial', 10, 'bold'), width=20,
                            command=update)
update_button.grid(row=1, column=0, padx=10, pady=5)
delete_button = tk.Button(db_button_frame, text='DELETE ITEM', bg='gray', fg='white', font=('Arial', 10, 'bold'),
                          width=20, command=delete)
delete_button.grid(row=2, column=0, pady=5)
refresh_button = tk.Button(db_button_frame, text='REFRESH ITEMS', bg='gray', fg='white', font=('Arial', 10, 'bold'),
                           width=20, command=refresh)
refresh_button.grid(row=3, column=0, padx=10, pady=5)
order_id_button = tk.Button(db_button_frame, text='ORDER ID DESC', bg='gray', fg='white', font=('Arial', 10, 'bold'),
                           width=20)
order_id_button.grid(row=4, column=0, padx=10, pady=5)


# endregion


window.mainloop()




