import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import sqlite3

# Create a connection to the SQLite database
conn = sqlite3.connect('shopping.db')
c = conn.cursor()

# Create tables if they don't exist
c.execute('''CREATE TABLE IF NOT EXISTS CUSTOMER (
                C_ID INTEGER PRIMARY KEY,
                CNAME VARCHAR(50),
                ADDRESS VARCHAR(75),
                PHONE_NUMBER BIGINT,
                EMAIL VARCHAR(25))''')

c.execute('''CREATE TABLE IF NOT EXISTS VENDOR (
                VID INT PRIMARY KEY,
                VNAME VARCHAR(50),
                ADDRESS VARCHAR(75),
                PHONE_NUMBER BIGINT,
                EMAIL VARCHAR(25))''')

c.execute('''CREATE TABLE IF NOT EXISTS PRODUCT
             (
                PID INT PRIMARY KEY,
                PNAME VARCHAR(50),
                AMOUNT DECIMAL(12,2),
                VID INT,
                FOREIGN KEY (VID) REFERENCES VENDOR(VID) ON DELETE CASCADE
             )''')

c.execute('''CREATE TABLE IF NOT EXISTS MYORDER(
                ORD_ID INT PRIMARY KEY,
                PID INT,
                CID INT,
                DATE DATE,
                AMOUNT DECIMAL(12,2),
                FOREIGN KEY (PID) REFERENCES PRODUCT(PID) ON DELETE CASCADE,
                FOREIGN KEY (CID) REFERENCES CUSTOMER(C_ID) ON DELETE CASCADE
             )''')

c.execute('''CREATE TABLE IF NOT EXISTS ORDER_DETAILS(
                ORD_ID INT,
                PID INT,
                QUANTITY INT,
                PRIMARY KEY(PID, ORD_ID),
                FOREIGN KEY (ORD_ID) REFERENCES MYORDER(ORD_ID) ON DELETE CASCADE,
                FOREIGN KEY (PID) REFERENCES PRODUCT(PID) ON DELETE CASCADE
             )''')

c.execute('''CREATE TABLE IF NOT EXISTS STOCK(
                PID INT PRIMARY KEY,
                QUANTITY INT,
                FOREIGN KEY (PID) REFERENCES PRODUCT(PID) ON DELETE CASCADE
             )''')

c.execute('''CREATE TABLE IF NOT EXISTS LOGIN
             (
                UserName VARCHAR(25),
                Password VARCHAR(20),
                PRIMARY KEY(UserName, Password)
             )''')

# Initial setup add login details
c.execute("INSERT OR IGNORE INTO LOGIN VALUES ('admin', 'admin')")

# Function to navigate to the login page
def goto_login():
    main_frame.grid_forget()
    login_frame.grid(row=0, column=0, padx=10, pady=10)
    signup_frame.grid(row=0, column=1, padx=10, pady=10)

# Function to perform login
def login():
    username = username_entry.get()
    password = password_entry.get()
    c.execute("SELECT * FROM LOGIN WHERE UserName=? AND Password=?", (username, password))
    if c.fetchone():
        login_frame.grid_forget()
        customer_entry_frame.grid(row=0, column=0, padx=10, pady=10)
        signup_frame.grid_forget()
    else:
        messagebox.showerror("Login Failed", "Invalid username or password.")

# Function to perform signup
def signup():
    username = signup_username_entry.get()
    password = signup_password_entry.get()
    phone = signup_phone_entry.get()
    if username and password and phone:
        c.execute("INSERT INTO LOGIN (UserName, Password) VALUES (?, ?)", (username, password))
        conn.commit()
        c.execute("INSERT INTO CUSTOMER (CNAME, PHONE_NUMBER) VALUES (?, ?)", ("", phone))
        conn.commit()
        messagebox.showinfo("Success", "Signup successful. You can now login.")
        # After signup, go to the login page
        goto_login()
    else:
        messagebox.showerror("Error", "Please enter username, password, and phone number.")

# Function to display products
def display_products():
    products_frame.grid(row=0, column=0, padx=10, pady=10)
    c.execute("SELECT * FROM PRODUCT")
    for row in c.fetchall():
        ttk.Label(products_frame, text=row[1]).pack()
        ttk.Button(products_frame, text="Add to Cart", command=lambda pid=row[0]: add_to_cart(pid)).pack()

# Function to add product to cart
def add_to_cart(product_id):
    # You can add code here to handle adding product to cart and updating database
    messagebox.showinfo("Success", "Product added to cart successfully.")

# Main application window
root = tk.Tk()
root.title("Shopping Management System")

# Main page with image
main_frame = ttk.Frame(root)
main_frame.grid(row=0, column=0, padx=10, pady=10)
image = Image.open("Online-Shopping-System-1024x576.jpg")  
photo = ImageTk.PhotoImage(image)
label = ttk.Label(main_frame, image=photo)
label.photo = photo
label.grid(row=0, column=0)
login_button = ttk.Button(main_frame, text="Login", command=goto_login)
login_button.grid(row=1, column=0, pady=10)

# Login page
login_frame = ttk.Frame(root)
username_label = ttk.Label(login_frame, text="Username:")
username_label.grid(row=0, column=0, padx=5, pady=5)
username_entry = ttk.Entry(login_frame)
username_entry.grid(row=0, column=1, padx=5, pady=5)
password_label = ttk.Label(login_frame, text="Password:")
password_label.grid(row=1, column=0, padx=5, pady=5)
password_entry = ttk.Entry(login_frame, show="*")
password_entry.grid(row=1, column=1, padx=5, pady=5)
login_button = ttk.Button(login_frame, text="Login", command=login)
login_button.grid(row=2, column=0, columnspan=2, pady=10)

# Signup page
signup_frame = ttk.Frame(root)
signup_username_label = ttk.Label(signup_frame, text="Username:")
signup_username_label.grid(row=0, column=0, padx=5, pady=5)
signup_username_entry = ttk.Entry(signup_frame)
signup_username_entry.grid(row=0, column=1, padx=5, pady=5)
signup_password_label = ttk.Label(signup_frame, text="Password:")
signup_password_label.grid(row=1, column=0, padx=5, pady=5)
signup_password_entry = ttk.Entry(signup_frame, show="*")
signup_password_entry.grid(row=1, column=1, padx=5, pady=5)
signup_phone_label = ttk.Label(signup_frame, text="Phone Number:")
signup_phone_label.grid(row=2, column=0, padx=5, pady=5)
signup_phone_entry = ttk.Entry(signup_frame)
signup_phone_entry.grid(row=2, column=1, padx=5, pady=5)
signup_button = ttk.Button(signup_frame, text="Signup", command=signup)
signup_button.grid(row=3, column=0, columnspan=2, pady=10)

# Customer entry page
customer_entry_frame = ttk.Frame(root)

cname_label = ttk.Label(customer_entry_frame, text="Customer Name:")
cname_label.grid(row=0, column=0, padx=5, pady=5)
cname_entry = ttk.Entry(customer_entry_frame)
cname_entry.grid(row=0, column=1, padx=5, pady=5)

address_label = ttk.Label(customer_entry_frame, text="Address:")
address_label.grid(row=1, column=0, padx=5, pady=5)
address_entry = ttk.Entry(customer_entry_frame)
address_entry.grid(row=1, column=1, padx=5, pady=5)

phone_label = ttk.Label(customer_entry_frame, text="Phone Number:")
phone_label.grid(row=2, column=0, padx=5, pady=5)
phone_entry = ttk.Entry(customer_entry_frame)
phone_entry.grid(row=2, column=1, padx=5, pady=5)

email_label = ttk.Label(customer_entry_frame, text="Email:")
email_label.grid(row=3, column=0, padx=5, pady=5)
email_entry = ttk.Entry(customer_entry_frame)
email_entry.grid(row=3, column=1, padx=5, pady=5)

def add_customer():
    cname = cname_entry.get()
    address = address_entry.get()
    phone = phone_entry.get()
    email = email_entry.get()
    if cname and address and phone and email:
        c.execute("INSERT INTO CUSTOMER (CNAME, ADDRESS, PHONE_NUMBER, EMAIL) VALUES (?, ?, ?, ?)", (cname, address, phone, email))
        conn.commit()
        messagebox.showinfo("Success", "Customer added successfully.")
        cname_entry.delete(0, tk.END)
        address_entry.delete(0, tk.END)
        phone_entry.delete(0, tk.END)
        email_entry.delete(0, tk.END)

add_customer_button = ttk.Button(customer_entry_frame, text="Add Customer", command=add_customer)
add_customer_button.grid(row=4, column=0, columnspan=2, pady=10)

# Product display and cart
products_frame = ttk.Frame(root)

def display_products():
    products_frame.grid(row=0, column=0, padx=10, pady=10)
    c.execute("SELECT * FROM PRODUCT")
    for row in c.fetchall():
        ttk.Label(products_frame, text=row[1]).pack()
        ttk.Button(products_frame, text="Add to Cart", command=lambda pid=row[0]: add_to_cart(pid)).pack()

def add_to_cart(product_id):
    # You can store the product IDs in a list for simplicity
    cart.append(product_id)
    messagebox.showinfo("Success", "Product added to cart successfully.")


display_products_button = ttk.Button(products_frame, text="Display Products", command=display_products)
display_products_button.pack()


root.mainloop()

# Close the database connection
conn.close()
