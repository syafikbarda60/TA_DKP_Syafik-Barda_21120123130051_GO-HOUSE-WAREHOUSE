#Graphical User Interface
import tkinter as tk
from tkinter import messagebox, simpledialog
from PIL import ImageTk, Image 
import json


#username untuk login
users = {"admin": "123"}

# barang disimpan sebagai list
warehouse_items = []
# barang yang terjual disimpan sebagai list
sold_items = []

# fungsi untuk menyimpan item dalam file
def save_items():
    with open('items.json', 'w') as f:
        json.dump(warehouse_items, f)

# fungsi untuk ambil item dlm file
def load_items():
    global warehouse_items
    try:
        with open('items.json', 'r') as f:
            warehouse_items = json.load(f)
    except FileNotFoundError:
        warehouse_items = []

# fungsi untuk menyimpan barang yang telah di jual dlam file
def save_sold_items():
    with open('sold_items.json', 'w') as f:
        json.dump(sold_items, f)

# fungsi untuk melihat barang yang telah di jual
def load_sold_items():
    global sold_items
    try:
        with open('sold_items.json', 'r') as f:
            sold_items = json.load(f)
    except FileNotFoundError:
        sold_items = []
#class and method
class WarehouseManagement:
    def __init__(self, master):
        self.master = master
        self.master.title("GO-HOUSE WAREHOUSE - Add/Edit Items")
        self.master.geometry('925x500+300+200')
        self.master.resizable(False, False)

        image = Image.open("C:/file kuliah/program/bg2.png")
        self.img = ImageTk.PhotoImage(image)
        self.img_label = tk.Label(master, image=self.img, bg='white')
        self.img_label.grid(row=0, column=0, columnspan=2, padx=5, pady=5)
        self.img_label.place_configure(x = -50, y = 0)
    
        self.name_label = tk.Label(master, text="Item Name:", bg="#FF5733", fg="#fdf5e6", font=("Palatino", 12, "bold"))
        self.name_label.grid(row=0, column=0, padx=5, pady=5)
        self.name_entry = tk.Entry(master)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5)

        self.quantity_label = tk.Label(master, text="Quantity:", bg="#FF5733", fg="#fdf5e6", font=("Palatino", 12, "bold"))
        self.quantity_label.grid(row=1, column=0, padx=5, pady=5)
        self.quantity_entry = tk.Entry(master)
        self.quantity_entry.grid(row=1, column=1, padx=5, pady=5)

        self.add_button = tk.Button(master, text="Add Item", command=self.add_item, bg="#FF5733", fg="#fdf5e6", font=("Palatino", 12, "bold"))
        self.add_button.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

        
        self.items_listbox = tk.Listbox(master, width = 100, height = 10)
        self.items_listbox.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

        self.load_items()

        self.edit_button = tk.Button(master, text="Edit Item", command=self.edit_item,  bg="#FF5733", fg="#fdf5e6", font=("Palatino", 12, "bold"))
        self.edit_button.grid(row=4, column=0, padx=5, pady=5)

        self.delete_button = tk.Button(master, text="Delete Item", command=self.delete_item,  bg="#FF5733", fg="#fdf5e6", font=("Palatino", 12, "bold"))
        self.delete_button.grid(row=4, column=1, padx=5, pady=5)
        
        self.back_button = tk.Button(master, text="Back", command=self.back_to_main,  bg="#FF5733", fg="#fdf5e6", font=("Palatino", 12, "bold"))
        self.back_button.grid(row=5, column=0, columnspan=2, padx=5, pady=5)
    #function
    def load_items(self):
        self.items_listbox.delete(0, tk.END)
        #perulangan
        for item in warehouse_items:
            self.items_listbox.insert(tk.END, f"{item['name']} - {item['quantity']}")

    def add_item(self):
        name = self.name_entry.get()
        quantity = self.quantity_entry.get()
        #pengkondisian
        if not name or not quantity:
            messagebox.showerror("Error", "Please enter all fields")
            return

        try:
            quantity = int(quantity)
        except ValueError:
            messagebox.showerror("Error", "Quantity must be a number")
            return

        warehouse_items.append({"name": name, "quantity": quantity})
        save_items()
        self.load_items()

    def edit_item(self):
        selected_item_index = self.items_listbox.curselection()
        if not selected_item_index:
            messagebox.showerror("Error", "Please select an item to edit")
            return

        selected_item = warehouse_items[selected_item_index[0]]
        new_name = simpledialog.askstring("Edit Item", "Enter new name:", initialvalue=selected_item['name'])
        new_quantity = simpledialog.askinteger("Edit Item", "Enter new quantity:", initialvalue=selected_item['quantity'])

        if new_name and new_quantity is not None:
            warehouse_items[selected_item_index[0]] = {"name": new_name, "quantity": new_quantity}
            save_items()
            self.load_items()

    def delete_item(self):
        selected_item_index = self.items_listbox.curselection()
        if not selected_item_index:
            messagebox.showerror("Error", "Please select an item to delete")
            return

        del warehouse_items[selected_item_index[0]]
        save_items()
        self.load_items()

    def back_to_main(self):
        self.master.destroy()
        root = tk.Tk()
        root.geometry('925x500+300+200')
        root.configure(bg="#fff")
        MainScreen(root)
        root.mainloop()

class SellItems:
    def __init__(self, master):
        self.master = master
        self.master.title("GO-HOUSE WAREHOUSE - Sell Items")
        self.master.geometry('925x500+300+200')
        self.master.resizable(False, False)

        image = Image.open("C:/file kuliah/program/bg2.png")
        self.img = ImageTk.PhotoImage(image)
        self.img_label = tk.Label(master, image=self.img, bg='white')
        self.img_label.grid(row=0, column=0, columnspan=2, padx=5, pady=5)
        self.img_label.place_configure(x = -50, y = 0)

       
        self.items_listbox = tk.Listbox(master, width = 100, height = 10)
        self.items_listbox.grid(row=0, column=0, columnspan=2, padx=5, pady=5)

        self.load_items()

        self.sell_button = tk.Button(master, text="Sell Item", command=self.sell_item, bg="#FF5733", fg="#fdf5e6", font=("Palatino", 12, "bold"))
        self.sell_button.grid(row=1, column=0, columnspan=2, padx=5, pady=5)
        
        self.back_button = tk.Button(master, text="Back", command=self.back_to_main, bg="#FF5733", fg="#fdf5e6", font=("Palatino", 12, "bold"))
        self.back_button.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

    def load_items(self):
        self.items_listbox.delete(0, tk.END)
        for item in warehouse_items:
            self.items_listbox.insert(tk.END, f"{item['name']} - {item['quantity']}")

    def sell_item(self):
        selected_item_index = self.items_listbox.curselection()
        if not selected_item_index:
            messagebox.showerror("Error", "Please select an item to sell")
            return

        selected_item = warehouse_items[selected_item_index[0]]
        sell_quantity = simpledialog.askinteger("Sell Item", "Enter quantity to sell:", initialvalue=1)

        if sell_quantity is not None:
            if sell_quantity > selected_item['quantity']:
                messagebox.showerror("Error", "Not enough stock available")
                return

            sold_item = selected_item.copy()
            sold_item['quantity'] = sell_quantity
            sold_items.append(sold_item)
            save_sold_items()

            warehouse_items[selected_item_index[0]]['quantity'] -= sell_quantity
            if warehouse_items[selected_item_index[0]]['quantity'] == 0:
                del warehouse_items[selected_item_index[0]]
            save_items()
            self.load_items()

    def back_to_main(self):
        self.master.destroy()
        root = tk.Tk()
        root.geometry('925x500+300+200')
        root.configure(bg="#fff")
        MainScreen(root)
        root.mainloop()

class SoldItems:
    def __init__(self, master):
        self.master = master
        self.master.title("GO-HOUSE WAREHOUSE - Sold Items")
        self.master.geometry('925x500+300+200')
        self.master.resizable(False, False)

        image = Image.open("C:/file kuliah/program/bg2.png")
        self.img = ImageTk.PhotoImage(image)
        self.img_label = tk.Label(master, image=self.img, bg='white')
        self.img_label.grid(row=0, column=0, columnspan=2, padx=5, pady=5)
        self.img_label.place_configure(x = -50, y = 0)

        self.sold_items_listbox = tk.Listbox(master, width = 100, height = 10)
        self.sold_items_listbox.grid(row=0, column=0, columnspan=2, padx=5, pady=5)
        

        self.load_sold_items()

        self.back_button = tk.Button(master, text="Back", command=self.back_to_main, bg="#FF5733", fg="#fdf5e6", font=("Palatino", 12, "bold"))
        self.back_button.grid(row=1, column=0, columnspan=2, padx=5, pady=5)
    

    def load_sold_items(self):
        self.sold_items_listbox.delete(0, tk.END)
        for item in sold_items:
            self.sold_items_listbox.insert(tk.END, f"{item['name']} - {item['quantity']}")

    def back_to_main(self):
        self.master.destroy()
        root = tk.Tk()
        root.geometry('925x500+300+200')
        root.configure(bg="#fff")
        MainScreen(root)
        root.mainloop()

class MainScreen:
    def __init__(self, master):
        self.master = master
        self.master.configure(bg="#fff")
        self.master.title("GO-HOUSE WAREHOUSE")
        self.master.geometry('925x500+300+200')
        self.master.resizable(False, False)

        image = Image.open("C:/file kuliah/program/bgmain.png")
        self.img = ImageTk.PhotoImage(image)
        self.img_label = tk.Label(master, image=self.img, bg='white')
        self.img_label.grid(row=0, column=0, columnspan=2, padx=5, pady=5)
        self.img_label.place_configure(x = -50, y = 0)

   
        self.add_edit_button = tk.Button(master, text="Add/Edit Items", command=self.open_add_edit_window, bg="#FF5733", fg="#fdf5e6", font=("Palatino", 15, "bold"))
        self.add_edit_button.pack(pady=20)
        self.add_edit_button.place_configure(x = 100, y = 50)

        self.sell_button = tk.Button(master, text="Sell Items", command=self.open_sell_window, bg="#FF5733", fg="#fdf5e6", font=("Palatino", 15, "bold"))
        self.sell_button.pack(pady=20)
        self.sell_button.place_configure(x = 425, y = 50)

        self.view_sold_button = tk.Button(master, text="View Sold Items", command=self.open_sold_items_window, bg="#FF5733", fg="#fdf5e6", font=("Palatino", 15, "bold"))
        self.view_sold_button.pack(pady=20)
        self.view_sold_button.place_configure(x = 715, y = 50)
        
        self.exit_button = tk.Button(master, text="Exit", command=self.exit_program, bg="#FF5733", fg="#fdf5e6", font=("Palatino", 15, "bold"))
        self.exit_button.pack(pady=20)
        self.exit_button.place_configure(x = 450, y = 450)

    def open_add_edit_window(self):
        self.master.destroy()
        root = tk.Tk()
        root.geometry('925x500+300+200')
        root.configure(bg="#fff")
        WarehouseManagement(root)
        root.mainloop()

    def open_sell_window(self):
        self.master.destroy()
        root = tk.Tk()
        root.geometry('925x500+300+200')
        root.configure(bg="#fff")
        SellItems(root)
        root.mainloop()

    def open_sold_items_window(self):
        self.master.destroy()
        root = tk.Tk()
        root.geometry('925x500+300+200')
        root.configure(bg="#fff")
        SoldItems(root)
        root.mainloop()
        
    def exit_program(self):
        self.master.quit()

class LoginScreen:
    def __init__(self, master):
        self.master = master
        self.master.configure(bg="#fff")
        self.master.title("Login")
        self.master.geometry('925x500+300+200')
        self.master.resizable(False, False)

       
        image = Image.open("C:/file kuliah/program/loginbaru.png")
        self.img = ImageTk.PhotoImage(image)
        self.img_label = tk.Label(master, image=self.img, bg='white')
        self.img_label.grid(row=0, column=0, columnspan=2, padx=5, pady=5)
        self.img_label.place_configure(x = 0, y = 50)

        image2 = Image.open("C:/file kuliah/kotak.png")
        self.img2 = ImageTk.PhotoImage(image2)
        self.img2_label = tk.Label(master, image=self.img2, bg='white')
        self.img2_label.grid(row=0, column=0, columnspan=2, padx=5, pady=5)
        self.img2_label.place_configure(x = 400, y = -10)

        
        self.heading_label = tk.Label(master, text ="LOGIN", bg = "#ff3131", fg = "#fdf5e6", font=("Palatino", 30, "bold"))
        self.heading_label.place_configure(x = 600, y = 80)

        
        self.username_label = tk.Label(master, text="Username:", bg="#ff3131", fg="#fdf5e6", font=("palatino", 12, "bold", "italic"))
        self.username_label.grid(row=1, column=0, padx=5, pady=5)
        self.username_label.place_configure(x = 550, y = 150)
        self.username_entry = tk.Entry(master, border = 0)
        self.username_entry.grid(row=1, column=1, padx=5, pady=5,)
        self.username_entry.place_configure(x = 550, y = 180)
        

        self.password_label = tk.Label(master, text="Password:", bg="#ff3131", fg="#fdf5e6", font=("palatino", 12, "bold", "italic"))
        self.password_label.grid(row=2, column=0, padx=5, pady=5)
        self.password_label.place_configure(x = 550, y = 210)
        self.password_entry = tk.Entry(master, show="*", border = 0)
        self.password_entry.grid(row=2, column=3, padx=5, pady=5,)
        self.password_entry.place_configure(x = 550, y = 240)
        

        self.login_button = tk.Button(master, text="Login", command=self.login, bg="#ff3131", fg="#fdf5e6", font=("palatino", 15, "bold"))
        self.login_button.grid(row=3, column=0, columnspan=2, padx=5, pady=5)
        self.login_button.place_configure(x = 630, y = 290)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username in users and users[username] == password:
            self.master.destroy()
            root = tk.Tk()
            root.geometry('925x500+300+200')
            root.configure(bg="#fff")
            MainScreen(root)
            root.mainloop()
        else:
            messagebox.showerror("Error", "Invalid username or password")

def main():
    load_items()
    load_sold_items()
    root = tk.Tk()
    root.title('go-house warehouse')
    root.geometry('600x400+50+50')
    root.resizable(False, False)
    LoginScreen(root)
    root.mainloop()

if __name__ == "__main__":
    main()
