from tkinter import * 
from tkinter.font import * 
import os 
from database import *

#---------------------------------------------------------------- GUI
window = Tk() 
window.title("Restaurant Manager Software")
width = window.winfo_screenwidth()
height = window.winfo_screenheight()
window.geometry("%dx%d" %(width , height))

window.grid_columnconfigure(0,weight=1)
window.grid_columnconfigure(1,weight=4)

window.grid_rowconfigure(0,weight=1)
# window.state('zoomed') # maximizes the window

pad_x = 5
pad_y = 5
arial_font = Font(family = 'Arial' , size = 18 )
# **************************************************************** Receipt Frame

def load_reciepts(reciept_id):
    list_box.delete(0,END)
    reciepts = db.get_reciept_by_reciept_id(reciept_id)
    for reciept in reciepts:
        list_box.insert(0,"%s\t%s\t %s\t %s" %(reciept[1], reciept[2] , reciept[3] , reciept[4]))

receipt_frame = LabelFrame(window , text = "Receipt" , font = arial_font , padx= pad_x , pady= pad_y)
receipt_frame.grid(row = 0, column = 0 , sticky='nsew' , padx= pad_x , pady= pad_y)

receipt_frame.grid_rowconfigure(1, weight = 1)
receipt_frame.grid_columnconfigure(0,weight = 1)

#order number and total frame
order_num_and_total_frame = LabelFrame(receipt_frame , font = arial_font, padx= pad_x , pady= pad_y)
order_num_and_total_frame.grid(row=0, column=0, sticky='nsew')
order_num_and_total_frame.grid_columnconfigure(0,weight=1)
order_num_and_total_frame.grid_columnconfigure(1,weight=1)

#order number label and entry
order_num_label = Label(order_num_and_total_frame, text = 'Order Number:',font=arial_font)
order_num_label.grid(row=0,column=0, sticky=W)

order_num_entry = Entry(order_num_and_total_frame, font= arial_font , width = 10  ,justify = 'center')
order_num_entry.grid(row = 1 , column = 0 , sticky='nsew')

#total label and entry
total_label = Label(order_num_and_total_frame, text= 'Total:' , font=arial_font)
total_label.grid(row=0,column=1, sticky=W)

total_entry = Entry(order_num_and_total_frame, font= arial_font, width=10 , justify='center')
total_entry.grid(row=1, column = 1, sticky='nsew')

total_price = 0.0
total_entry.insert(0,total_price)

def add_total_price(price):
    total = float(total_entry.get())
    total += float(price)
    total_entry.delete(0,END)
    total_entry.insert(0,total)

def subtract_total_price(price):
    total = float(total_entry.get())
    total -= float(price)
    total_entry.delete(0,END)
    total_entry.insert(0,total)

def subtract_all_from_total(total_price):
    total = float(total_entry.get())
    total_price = float(total_price)
    total -= total_price
    total_entry.delete(0,END)
    total_entry.insert(0,total)

def get_total():
    total_reciept_price = 0
    for each_item in list_box.get(0, END):
        fields = each_item.split('\t')
        total_item_price = float(fields[3]) 
        total_reciept_price += total_item_price
    total_entry.delete(0, END)
    total_entry.insert(0, total_reciept_price)  

def entry_key_release(key):
    try:
        reciept_id = int(order_num_entry.get())
        load_reciepts(reciept_id)
        get_total()
    except:
        list_box.delete(0,END)

order_num_entry.bind('<KeyRelease>' , entry_key_release)

max_reciept_number = db.get_max_reciept()
if max_reciept_number[0][0] == None:
    max_reciept_number = 0
else:
    max_reciept_number = int(max_reciept_number[0][0])

max_reciept_number += 1
order_num_entry.insert(0,max_reciept_number)

list_box = Listbox(receipt_frame)
list_box.grid(row = 1 , column = 0 , sticky='nsew' , padx= pad_x , pady= pad_y)
list_box.configure(justify=LEFT)

#-- buttons of listbox frame 
list_box_buttons_frame = LabelFrame(receipt_frame)
list_box_buttons_frame.grid(row = 2, column = 0 , sticky='nsew' , padx= pad_x , pady= pad_y)

list_box_buttons_frame.grid_columnconfigure(0,weight=1)
list_box_buttons_frame.grid_columnconfigure(1,weight=1)
list_box_buttons_frame.grid_columnconfigure(2,weight=1)
list_box_buttons_frame.grid_columnconfigure(3,weight=1)
#-- buttons 

def delete_reciept_item():
    reciept_id = int(order_num_entry.get())
    menu_item = list_box.get(ACTIVE)
    menu_item_name = menu_item.split('\t')[0]
    result = db.get_menu_item_by_name(menu_item_name)
    menu_item_id = int(result[0][0])
    db.delete_reciept(reciept_id,menu_item_id)
    load_reciepts(reciept_id)
    subtract_all_from_total(menu_item.split('\t')[3])

delete_button = Button(list_box_buttons_frame , text= "Delete Item" ,font= arial_font , command = delete_reciept_item)
delete_button.grid(row= 0 , column = 0 , sticky='nsew')

def new_reciept():
    list_box.delete(0,END)
    max_reciept_number = db.get_max_reciept()
    if max_reciept_number[0][0] == 0:
        max_reciept_number = 0
    else:
        max_reciept_number = int(max_reciept_number[0][0])
    max_reciept_number += 1
    order_num_entry.delete(0,END)
    order_num_entry.insert(0,max_reciept_number)
    total_entry.delete(0,END)
    total_entry.insert(0,0.0)

new_button = Button(list_box_buttons_frame , text= "New Reciept" ,font= arial_font, command = new_reciept)
new_button.grid(row= 0 , column = 1 , sticky='nsew')

def increase_count():
    reciept_id = int(order_num_entry.get())
    menu_item = list_box.get(ACTIVE)
    menu_item_name = menu_item.split('\t')[0]
    result = db.get_menu_item_by_name(menu_item_name)
    menu_item_id = int(result[0][0])
    db.increase_count(reciept_id , menu_item_id)
    load_reciepts(reciept_id)
    add_total_price(result[0][2])
    

add_button = Button(list_box_buttons_frame , text= "+" ,font= arial_font, command = increase_count)
add_button.grid(row= 0 , column = 2 , sticky='nsew')

def decrease_count():
    reciept_id = int(order_num_entry.get())
    menu_item = list_box.get(ACTIVE)
    menu_item_name = menu_item.split('\t')[0]
    result = db.get_menu_item_by_name(menu_item_name)
    menu_item_id = int(result[0][0])
    db.decrease_count(reciept_id , menu_item_id)
    load_reciepts(reciept_id)
    subtract_total_price(result[0][2])

minus_button = Button(list_box_buttons_frame , text= "-" ,font= arial_font, command = decrease_count )
minus_button.grid(row= 0 , column = 3 , sticky='nsew')
#***************************************************************** Menu Frame
menu_frame = LabelFrame(window , text = "Food & Drinks Menu", font = arial_font , padx= pad_x , pady= pad_y)
menu_frame.grid(row = 0, column= 1 , sticky='nsew' , padx= pad_x , pady= pad_y)

menu_frame.grid_columnconfigure(0,weight=1)
menu_frame.grid_columnconfigure(1,weight=1)

menu_frame.grid_rowconfigure(0,weight=1)

# -- drinks frame 
drinks_frame = LabelFrame(menu_frame, text= "Drinks Menu" , padx= pad_x , pady= pad_y)
drinks_frame.grid(row=0, column=0 , sticky='nsew' , padx= pad_x , pady= pad_y)
drinks_frame.grid_columnconfigure(0,weight=1)
drinks_frame.grid_rowconfigure(0,weight=1)

listbox_drinks = Listbox(drinks_frame , font= arial_font , exportselection=False)
listbox_drinks.grid(sticky='nsew')
listbox_drinks.configure(justify=LEFT)

drinks = db.get_menu_food(False)
for drink in drinks:
    listbox_drinks.insert(END , drink[1])

drink_scrollbar = Scrollbar(listbox_drinks , orient='vertical' , command=listbox_drinks.yview)
drink_scrollbar.pack(side='right' , fill='y')
listbox_drinks.config(yscrollcommand=drink_scrollbar.set)

def add_drink(event):
    active = listbox_drinks.get(ACTIVE)
    drink_item = db.get_menu_item_by_name(active)
    menu_id = drink_item[0][0]
    price = drink_item[0][2]
    reciept_id = int(order_num_entry.get())

    result = db.get_reciept_by_reciept_id_menu_id(reciept_id,menu_id)
    if len(result) == 0:
        db.insert_into_table_reciept(reciept_id,menu_id,1,price)
    else:
        db.increase_count(reciept_id,menu_id)
    load_reciepts(reciept_id)
    add_total_price(price)

listbox_drinks.bind('<Double-Button>' , add_drink)
#-- food frame
food_frame = LabelFrame(menu_frame, text="Food Menu" , padx= pad_x , pady= pad_y)
food_frame.grid(row = 0 , column = 1 , sticky='nsew' , padx= pad_x , pady= pad_y)
food_frame.grid_columnconfigure(0,weight =1)
food_frame.grid_rowconfigure(0,weight =1)

listbox_foods = Listbox(food_frame , font= arial_font , exportselection=False)
listbox_foods.grid(sticky='nsew')
listbox_foods.configure(justify=LEFT)

foods = db.get_menu_food(True)
for food in foods:
    listbox_foods.insert(END, food[1])

food_scrollbar = Scrollbar(listbox_foods , orient='vertical' , command = listbox_foods.yview)
food_scrollbar.pack(side = 'right' , fill = 'y')
listbox_foods.config(yscrollcommand=food_scrollbar.set)
def add_food(event):
    active = listbox_foods.get(ACTIVE)
    food_item = db.get_menu_item_by_name(active)
    menu_id = food_item[0][0]
    price = food_item[0][2]
    reciept_id = int(order_num_entry.get())

    result = db.get_reciept_by_reciept_id_menu_id(reciept_id,menu_id)
    if len(result) == 0:
        db.insert_into_table_reciept(reciept_id,menu_id,1,price)
    else:
        db.increase_count(reciept_id,menu_id)
    load_reciepts(reciept_id)
    add_total_price(price)

listbox_foods.bind('<Double-Button>' , add_food)

#**************************************************************** Buttons Frame
buttons_frame = LabelFrame(window , font = arial_font, padx= pad_x , pady= pad_y)
buttons_frame.grid(row = 1 , column = 1, padx= pad_x , pady= pad_y)

from tkinter import messagebox

def exit_program():
    message_box = messagebox.askquestion("Exit" , "Are you sure you want to exit?" , icon= 'warning')
    if message_box == 'yes':
        window.destroy()

window.protocol("WM_DELETE_WINDOW" , exit_program)
exit_button = Button(buttons_frame , text = "Exit" ,font = arial_font, command = exit_program)
exit_button.grid(row = 0 , column = 0)

from subprocess import call
def open_calculator():
    os.system("open -a Calculator") # opens the calculator on macOS

calculator_button = Button(buttons_frame , text = "Calculator" , font = arial_font , command = open_calculator)
calculator_button.grid(row = 0 , column = 1)

import webbrowser
def open_website():
    webbrowser.open("https://www.mcdonalds.com/us/en-us/full-menu.html")

open_website_button = Button(buttons_frame , text= "Our Website" , font = arial_font , command = open_website)
open_website_button.grid(row=0 ,column=2 )

window.mainloop() 
