from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from PIL import Image, ImageTk
import os
import datetime
import smtplib
import os
print(os.path.exists("D:/download-poy/dl pics/Images"))

class AdminSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("CSGO POS")
        self.root.geometry("1920x1080")
        self.root.config(bg="#444444")

        # Variables to store login details
        self.username_var = StringVar()
        self.password_var = StringVar()
        self.total_var = DoubleVar(value=0.00)
        self.quantity_var = IntVar(value=1)
        self.selected_product = None
        self.balance_var = DoubleVar(value=0.00)

        # Frame to hold login options
        self.login_option_frame = Frame(self.root, bg="#2b2b2b")
        self.login_option_frame.pack(pady=70)

        # Label and ComboBox for login options
        Label(self.login_option_frame, text="Select Type of Login:", bg="#2b2b2b", fg="white", font=("Arial Black", 12)).grid(row=0, column=0, padx=20, pady=20)
        self.login_options = ttk.Combobox(self.login_option_frame, values=["Counter-Terrorist", "Terrorist"], state="readonly", font=("Arial Black", 12))
        self.login_options.grid(row=0, column=1, padx=20, pady=20)

        # Center the ComboBox
        self.login_option_frame.grid_columnconfigure(1, weight=1)

        # Button to trigger login
        Button(self.login_option_frame, text="Login", command=self.login, bg="#3cba54", fg="white", font=("Arial Black", 12)).grid(row=1, columnspan=2, pady=20)

        # Frame to hold login entries
        self.login_frame = Frame(self.root, bg="#2b2b2b")

    def login(self):
        login_type = self.login_options.get()
        if login_type == "":
            messagebox.showerror("Login Error", "Please select a login type.")
        elif login_type == "Counter-Terrorist":
            self.ct_login()
        elif login_type == "Terrorist":
            self.t_login()

    def ct_login(self):
        self.clear_login_frame()
        Label(self.login_frame, text="Counter-Terrorist Login", bg="#2b2b2b", fg="#A7C7E7", font=("Arial Black", 14, "bold")).pack(pady=20)
        Label(self.login_frame, text="Username:", bg="#2b2b2b", fg="white", font=("Arial Black", 12)).pack(pady=10, padx=100)
        Entry(self.login_frame, textvariable=self.username_var, font=("Arial Black", 12)).pack(pady=5)
        Label(self.login_frame, text="Password:", bg="#2b2b2b", fg="white", font=("Arial Black", 12)).pack(pady=5)
        password_entry = Entry(self.login_frame, textvariable=self.password_var, show="*", font=("Arial Black", 12))
        password_entry.pack(pady=5)
        Button(self.login_frame, text="Login", command=self.ct_validate, bg="#4CAF50", fg="white", font=("Arial Black", 12)).pack(pady=30)
        self.login_frame.pack(pady=20)
    def t_login(self):
        self.clear_login_frame()
        Label(self.login_frame, text="Terrorist Login", bg="#2b2b2b", fg="#FFBF00", font=("Arial Black", 14, "bold")).pack(pady=20)
        Label(self.login_frame, text="Username:", bg="#2b2b2b", fg="white", font=("Arial Black", 12)).pack(pady=10, padx=100)
        Entry(self.login_frame, textvariable=self.username_var, font=("Arial Black", 12)).pack(pady=5)
        Label(self.login_frame, text="Password:", bg="#2b2b2b", fg="white", font=("Arial Black", 12)).pack(pady=5)
        password_entry = Entry(self.login_frame, textvariable=self.password_var, show="*", font=("Arial Black", 12))
        password_entry.pack(pady=5)
        Button(self.login_frame, text="Login", command=self.t_validate, bg="#4CAF50", fg="white", font=("Arial Black", 12)).pack(pady=30)
        self.login_frame.pack(pady=20)

    def ct_validate(self):
        username = self.username_var.get()
        password = self.password_var.get()
        if username == "a" and password == "a":
            messagebox.showinfo("Counter-Terrorist Login", "Login successful!")
            self.open_ct_admin_window()
            self.root.iconify()
        else:
            messagebox.showerror("Counter-Terrorist Login", "Invalid username or password!")

    def t_validate(self):
        username = self.username_var.get()
        password = self.password_var.get()
        if username == "a" and password == "a":
            messagebox.showinfo("Terrorist Login", "Login successful!")
            self.open_t_admin_window()
            self.root.iconify()
        else:
            messagebox.showerror("Terrorist Login", "Invalid username or password!")

    def add_to_cart(self, cart_listbox, item_name, item_price):
        quantity = self.quantity_var.get()
        if quantity <= 0:
            messagebox.showerror("Invalid Quantity", "Please enter a valid quantity.")
            return

        # Keep track of items in the cart
        if not hasattr(self, 'cart_items'):
            self.cart_items = {}

        # Check for existing item
        if item_name in self.cart_items:
            # Update existing item
            i = self.cart_items[item_name]
            item = cart_listbox.get(i)
            item_parts = item.split(" $")  # Adjust based on your actual delimiter
            current_quantity = int(item_parts[0].split(" x ")[1])
            new_quantity = current_quantity + quantity
            new_total_price = item_price * new_quantity
            cart_listbox.delete(i)
            cart_listbox.insert(i, f"{item_name.ljust(20)} x {new_quantity:>2} ${new_total_price:>5,.2f}")
            self.cart_items[item_name] = i
            self.update_total(new_total_price - (current_quantity * item_price))
        else:
            # Add new item to cart
            total_price = item_price * quantity
            i = cart_listbox.size()
            cart_listbox.insert(END, f"{item_name.ljust(20)} x {quantity:>2} ${total_price:>5,.2f}")
            self.cart_items[item_name] = i
            self.update_total(total_price)

    def remove_item(self):
        selected_item = self.cart_listbox.get(ANCHOR)
        if not selected_item:
            return

        item_name = selected_item.split(" x")[0].strip()
        if item_name in self.cart_items:
            # Find the index of the selected item in the listbox
            index = self.cart_listbox.get(0, END).index(selected_item)
            self.cart_listbox.delete(index)
            del self.cart_items[item_name]

            # Update the total price
            item_parts = selected_item.split(" $")
            total_price = float(item_parts[1].replace(",", ""))
            self.update_total(-total_price)
            self.product_name.config(text="Product:")
            self.quantity_var.set(1)

    def clear(self):
        self.cart_listbox.delete(0, END)
        self.total_var.set(0)
        self.quantity_var.set(1)
        self.product_name.config(text="Product:")
        self.update_total()
        if hasattr(self, 'cart_items'):
            self.cart_items = {}

    def update_total(self, price=0):
        self.total_var.set(self.total_var.get() + price)
        self.total_label.config(text=f"TOTAL: ${self.total_var.get():,.2f}")

    def update_product(self, product_name, price):
        self.selected_product = product_name
        self.product_name.config(text=f"Product: {product_name} - ${price:,.2f}")
        self.quantity_var.set(1)

    def confirm_order(self):
        self.login_option_frame.pack_propagate(0)
        total = self.total_var.get()
        cash = self.balance_var.get()
        response =messagebox.askyesno(" ", "DO YOU WANT TO BUY ALL THE ITEMS IN THE CART?")
        if total > cash:
            messagebox.showerror("Error", "Insufficient cash balance.")
            return
        if response == YES and cash >= total:
            receipt_response = messagebox.askyesno(" ", "DO YOU WANT TO PRINT YOUR RECEIPT?")
            if receipt_response == YES:
                self.show_email_window()
            else:
                self.checkout()            
        else:
            return

    def show_email_window(self):
        self.email_window = Toplevel(self.root)
        self.email_window.title("Email Receipt")
        self.email_window.geometry("400x200")
        self.email_window.config(bg="#2b2b2b")

        Label(self.email_window, text="Enter your email address:", bg="#2b2b2b", fg="white", font=("Arial Black", 12)).pack(pady=20)
        self.email_entry = Entry(self.email_window, width=30, font=("Arial Black", 12))
        self.email_entry.pack(pady=10)
        Button(self.email_window, text="Send Receipt", command=self.send_receipt, bg="#4CAF50", fg="white", font=("Arial Black", 12)).pack(pady=20)

    def send_receipt(self):
        email = self.email_entry.get()
        if email:
            self.email_receipt(email)
            self.email_window.destroy()
            messagebox.showinfo("Email Receipt", "Receipt sent successfully!")
        else:
            messagebox.showerror("Email Error", "Please enter a valid email address.")

    def email_receipt(self, email):
        cart_items = self.cart_listbox.get(0, END)
        total = self.total_var.get()
        cash = self.balance_var.get()
        payment_method = "Cash"  # Example payment method, can be changed dynamically
        time_of_payment = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        receipt_content = "OFFICIAL RECEIPT\nCWHW+9QQ Cavite Civic Center\nCavite City, 4103 Cavite\n"
        receipt_content += "\n" + "-" * 55 + "\n"
        receipt_content += "------------PURCHASED ITEMS-------------\n\n"
        for item in cart_items:
            receipt_content += item + "\n"
        receipt_content += "\n" + "-" * 55 + "\n\n"
        receipt_content += f"TOTAL: ${total:,.2f}\n"
        receipt_content += f"Cash: ${cash:,.2f}\n"
        receipt_content += f"Change: ${cash - total:,.2f}\n"
        receipt_content += f"Payment Method: {payment_method}\n\n"
        receipt_content += "-" * 55 + "\n"
        receipt_content += f"Time of Payment: {time_of_payment}\n"
        receipt_content += "\nThank you for shopping with us!\nWe hope to see you again soon."

        try:
            smtp_server = "smtp.gmail.com"
            smtp_port = 587
            smtp_username = "csgopos2024@gmail.com"
            smtp_password = "ootn ooiy qqxk vhnr"
            from_email = "csgopos2024@gmail.com"
            to_email = email

            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(smtp_username, smtp_password)
                message = f"Subject: CSGO POS Receipt\n\n{receipt_content}"
                server.sendmail(from_email, to_email, message)
        except smtplib.SMTPAuthenticationError:
            messagebox.showerror("Email Error", "Failed to authenticate with the email server. Please check your username and password.")
        except smtplib.SMTPException as e:
            messagebox.showerror("Email Error", f"An error occurred while sending the email: {e}")
        except Exception as e:
            messagebox.showerror("Email Error", f"An unexpected error occurred: {e}")
        self.cart_listbox.delete(0, END)
        self.product_name.config(text="Product:")
        self.total_var.set(0)
        self.balance_var.set(0.0)
        if hasattr(self, 'cart_items'):
            self.cart_items = {}


    def checkout(self):
        cart_items = self.cart_listbox.get(0, END)
        total = self.total_var.get()
        cash = self.balance_var.get()
        payment_method = "Cash"  # Example payment method, can be changed dynamically
        time_of_payment = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        receipt_content = "OFFICIAL RECEIPT\nCWHW+9QQ Cavite Civic Center\nCavite City, 4103 Cavite\n"
        receipt_content += "\n" + "-" * 55 + "\n"
        receipt_content += "------------PURCHASED ITEMS-------------\n\n"
        for item in cart_items:
            receipt_content += item + "\n"
        receipt_content += "\n" + "-" * 55 + "\n\n"
        receipt_content += f"TOTAL: ${total:,.2f}\n"
        receipt_content += f"Cash: ${cash:,.2f}\n"
        receipt_content += f"Change: ${cash - total:,.2f}\n"
        receipt_content += f"Payment Method: {payment_method}\n\n"
        receipt_content += "-" * 55 + "\n"
        receipt_content += f"Time of Payment: {time_of_payment}\n"
        receipt_content += "\nThank you for shopping with us!\nWe hope to see you again soon."

        if total > cash:
            messagebox.showerror("Error", "Insufficient cash balance.")
            return
        else:
            messagebox.showinfo(" ", "TRANSACTION COMPLETED.\n THANK YOU FOR SHOPPING WITH CSGO POS")    
            self.show_receipt_popup(receipt_content)
            self.cart_listbox.delete(0, END)
            self.product_name.config(text="Product:")
            self.total_var.set(0)
            self.cart_listbox.delete(0, END)

    def show_receipt_popup(self, receipt_content):
        receipt_popup = Toplevel(self.root)
        receipt_popup.title("")
        receipt_popup.overrideredirect(True)  # Remove window decorations

        # Get the width and height of the screen
        screen_width = receipt_popup.winfo_screenwidth()
        screen_height = receipt_popup.winfo_screenheight()

        # Calculate the position to place the window on the left side
        window_width = 500
        window_height = 900
        x = 0  # Distance from the left edge of the screen
        y = (screen_height - window_height) // 2

        # Set the position of the window
        receipt_popup.geometry(f"{window_width}x{window_height}+{x}+{y}")

        # Add a close button
        close_button = Button(receipt_popup, text="Close", command=receipt_popup.destroy, font=("Arial", 12))
        close_button.pack(padx=10, pady=10, side=BOTTOM)

        receipt_label = Label(receipt_popup, text=receipt_content, fg="black", font=("Arial", 12), justify="left")
        receipt_label.pack(padx=20, pady=20, fill="both", expand=True)
        self.product_name.config(text="Product:")
        self.total_var.set(0)
        self.balance_var.set(0.00)
        self.update_total()
        if hasattr(self, 'cart_items'):
            self.cart_items = {}

    def open_ct_admin_window(self):
        ct_admin_window = Toplevel(self.root)
        ct_admin_window.title("Counter-Terrorist Admin")
        ct_admin_window.geometry("1920x1080")
        ct_admin_window.config(bg="#2b2b2b")
        ct_admin_window.grid_rowconfigure(0, weight=1)
        ct_admin_window.grid_columnconfigure(0, weight=1)
        
        self.prices = {
            "Kevlar Vest": 650,
            "Kevlar + Helmet": 1000,
            "Zeus 27": 200,
            "Defuse Kit": 400,
            "P2000": 200,
            "Dual Barettas": 300,
            "P250": 300,
            "Five-SeveN": 500,
            "Desert Eagle": 700,
            "Nova": 1050,
            "XM1014": 2000,
            "MP5-SD": 1500,
            "P90": 2350,
            "MP9": 1250,
            "Famas": 2250,
            "M4A1-S": 2900,
            "SSG 08": 1700,
            "AUG": 3300,
            "AWP": 4750,
            "Flashbang": 200,
            "Smoke Grenade": 300,
            "Explosive Grenade": 300,
            "Incendiary Grenade": 600,
            "Decoy Grenade": 50,
        }

        # Load images
        image_folder = "D:\download-poy\dl pics\POS CSGO theme\Images"
        image_files = [
            "kevlar.png", "kevlar + helmet.png", "zeus x27.png", "defuse kit.png",  # Equipment
            "p2000.png", "dual barettas.png", "p250.png", "five seven.png", "deagle.png",  # Pistols
            "nova.png", "xm1014.png", "mp5sd.png", "p90.png", "mp9.png",  # Mid-Tier
            "famas.png", "m4a1s.png", "ssg 08.png", "aug.png", "awp.png",  # Rifles
            "flashbang.png", "smoke.png", "he.png", "molo.png", "decoy.png"  # Grenades
        ]

        # Dictionary to hold categories and their respective buttons
        categories = {
            "1 Equipment": ["kevlar.png", "kevlar + helmet.png", "zeus x27.png", "defuse kit.png"],
            "2 Pistols": ["p2000.png", "dual barettas.png", "p250.png", "five seven.png", "deagle.png"],
            "3 Mid-Tier": ["nova.png", "xm1014.png", "mp5sd.png", "p90.png", "mp9.png"],
            "4 Rifles": ["famas.png", "m4a1s.png", "ssg 08.png", "aug.png", "awp.png"],
            "5 Grenades": ["flashbang.png", "smoke.png", "he.png", "incendiary.png", "decoy.png"]
        }

        # Mapping of file names to desired button names
        button_names = {
            "kevlar.png": "Kevlar Vest",
            "kevlar + helmet.png": "Kevlar + Helmet",
            "zeus x27.png": "Zeus 27",
            "defuse kit.png": "Defuse Kit",
            "p2000.png": "P2000",
            "dual barettas.png": "Dual Barettas",
            "p250.png": "P250",
            "five seven.png": "Five-SeveN",
            "deagle.png": "Desert Eagle",
            "nova.png": "Nova",
            "xm1014.png": "XM1014",
            "mp5sd.png": "MP5-SD",
            "p90.png": "P90",
            "mp9.png": "MP9",
            "famas.png": "Famas",
            "m4a1s.png": "M4A1-S",
            "ssg 08.png": "SSG 08",
            "aug.png": "AUG",
            "awp.png": "AWP",
            "flashbang.png": "Flashbang",
            "smoke.png": "Smoke Grenade",
            "he.png": "Explosive Grenade",
            "incendiary.png": "Incendiary Grenade",
            "decoy.png": "Decoy Grenade"
        }
        
        
        for category, category_images in categories.items():
            category_frame = Frame(ct_admin_window, bd=2, relief="groove", bg="#2b2b2b")
            category_frame.pack(padx=5, pady=5, side=LEFT, fill="both", expand=False)

            category_label = Label(category_frame, text=category, bg="#2b2b2b", fg="#ffffff", font=("Arial Black", 14, "bold"))
            category_label.pack(padx=5, pady=5)

            # Create a frame for buttons under each category
            button_frame = Frame(category_frame, bg="#2b2b2b")
            button_frame.pack(padx=5, pady=5, fill="both", expand=True)

        # Create buttons with images and names for each category
            for index, image_name in enumerate(category_images, start=1):
                image_path = os.path.join(image_folder, image_name)
                image = Image.open(image_path)
                image.thumbnail((100, 45))  # Resize image
                button_image = ImageTk.PhotoImage(image)

                # Get the desired button name from the mapping
                button_name = button_names.get(image_name, "Unnamed")

                button = Button(button_frame, image=button_image, text=f"{index}. {button_name} \n${self.prices[button_name]}",
                                compound="top", justify="center", padx=10, pady=10, bg="#444444", fg="#A7C7E7", font=("Arial", 12, "bold"),
                                command=lambda name=button_name, price=self.prices[button_name]: self.update_product(name, price))
                button.image = button_image
                button.pack(pady=5, padx=5, fill="both", expand=True)

         #Cart frame
        self.cart_frame = Frame(ct_admin_window, bd=2, relief="groove", bg="#2b2b2b")
        self.cart_frame.pack(padx=5, pady=5, side=RIGHT, fill="both", expand=True)

        # Cart listbox
        self.cart_label = Label(self.cart_frame, text="MY CART:", font=("Arial Black", 14, "bold"), bg="#2b2b2b", fg="White")
        self.cart_label.pack(padx=10, pady=10, anchor="w")

        self.dash_frame = Frame(self.cart_frame, bg="#2b2b2b")
        self.dash_frame.pack(padx=5, pady=5, side="top", anchor="w")

        self.item = Label(self.dash_frame, text="Item:", font=("Arial Black", 13, "bold"), bg="#2b2b2b", fg="White")
        self.item.pack(padx=5, pady=5, side="left")

        self.quantity = Label(self.dash_frame, text="Quantity & Price:", font=("Arial Black", 13, "bold"), bg="#2b2b2b", fg="White")
        self.quantity.pack(padx=130, pady=5, side="left")
        
        self.cart_listbox = Listbox(self.cart_frame, justify="left", height=22, font=("Courier", 13, "bold"))
        self.cart_listbox.pack(padx=5, pady=5, fill="both", expand=False)

        #product label
        self.product_name = Label(self.cart_frame, text="Product: ", font=("Arial Black", 13, "bold"), bg="#2b2b2b", fg="White")
        self.product_name.pack(padx=10, pady=5, side="top", anchor="w")

        # Quantity label and entry
        self.quantity_frame = Frame(self.cart_frame, bg="#2b2b2b")
        self.quantity_frame.pack(padx=5, pady=5, side="top", anchor="w")

        self.quantity_label = Label(self.quantity_frame, text="Quantity:", bg="#2b2b2b", fg="White", font=("Arial Black", 13, "bold"))
        self.quantity_label.pack(padx=5, pady=5, side="left")

        self.quantity_entry = Entry(self.quantity_frame, textvariable=self.quantity_var, width=8, font=("Arial Black", 13))
        self.quantity_entry.pack(padx=5, pady=5, side="left")

        # Add to cart button and Remove from cart button
        self.add_button_frame = Frame(self.cart_frame, bg="#2b2b2b")
        self.add_button_frame.pack(padx=5, pady=5, side="top", anchor="center")

        self.add_button = Button(self.add_button_frame, text="Add to Cart", command=lambda: self.add_to_cart(self.cart_listbox, self.selected_product, self.prices[self.selected_product]),
                                font=("Arial Black", 12, "bold"), bg="#3cba54", fg="white")
        self.add_button.pack(padx=10, pady=5, side="left")

        self.remove_button = Button(self.add_button_frame, text="Remove Item", command=self.remove_item, font=("Arial Black", 13, "bold"), bg="#FF6347", fg="white")
        self.remove_button.pack(padx=10, pady=5, side="left")

        self.clear_button = Button(self.add_button_frame, text="Clear List", command=self.clear, font=("Arial Black", 13, "bold"), bg="#FFA500", fg="white")
        self.clear_button.pack(padx=10, pady=5, side="left")

        # Total label
        self.total_label_frame = Frame(self.cart_frame, bg="#2b2b2b")
        self.total_label_frame.pack(padx=5, pady=5, side="top", anchor="e")

        self.total_label = Label(self.total_label_frame, text="TOTAL: $0.00", font=("Arial Black", 13, "bold"), bg="#2b2b2b", fg="White")
        self.total_label.pack(padx=10, pady=5, side="left")

        self.balance_label = Label(self.total_label_frame, text="CASH: $ ", font=("Arial Black", 13, "bold"), bg="#2b2b2b", fg="White")
        self.balance_label.pack(padx=10, pady=5, side="left")
        self.balance_entry = Entry(self.total_label_frame, textvariable=self.balance_var, font=("Arial Black", 13, "bold"), bg="#2b2b2b", fg="White")
        self.balance_entry.pack(pady=5, side="left")

        # Checkout Button
        self.checkout_button_frame = Frame(self.cart_frame, bg="#2b2b2b")
        self.checkout_button_frame.pack(padx=10, pady=5, side="top", anchor="e")

        self.checkout_button = Button(self.checkout_button_frame, text="CHECKOUT", command=self.confirm_order, font=("Arial Black", 13, "bold"), bg="#0D47A1", fg="white")
        self.checkout_button.pack(padx=10, pady=5, side="right")


    def open_t_admin_window(self):
        t_admin_window = Toplevel(self.root)
        t_admin_window.title("Counter-Terrorist Admin")
        t_admin_window.geometry("1920x1080")
        t_admin_window.config(bg="#2b2b2b")
        t_admin_window.grid_rowconfigure(0, weight=1)
        t_admin_window.grid_columnconfigure(0, weight=1)
        
        self.prices = {
            "Kevlar Vest": 650,
            "Kevlar + Helmet": 1000,
            "Zeus 27": 200,
            "Glock-18": 200,
            "Dual Barettas": 300,
            "P250": 300,
            "Tec-9": 500,
            "Desert Eagle": 700,
            "Nova": 1050,
            "XM1014": 2000,
            "MP5-SD": 1500,
            "P90": 2350,
            "MAC-10": 1050,
            "Galil AR": 1800,
            "AK-47": 2700,
            "SSG 08": 1700,
            "SG 553": 3000,
            "AWP": 4750,
            "Flashbang": 200,
            "Smoke Grenade": 300,
            "Explosive Grenade": 300,
            "Molotov": 400,
            "Decoy Grenade": 50
        }

        # Load images
        image_folder = "D:\download-poy\dl pics\POS CSGO theme\Images"
        image_files = [
            "kevlar.png", "kevlar + helmet.png", "zeus x27.png",  # Equipment
            "g18.png", "dual barettas.png", "p250.png", "tec9.png", "deagle.png",  # Pistols
            "nova.png", "xm1014.png", "mp5sd.png", "p90.png", "mac10.png",  # Mid-Tier
            "galil.png", "ak47.png", "ssg 08.png", "sg553.png", "awp.png",  # Rifles
            "flashbang.png", "smoke.png", "he.png", "molo.png", "decoy.png"  # Grenades
        ]

        # Dictionary to hold categories and their respective buttons
        categories = {
            "1 Equipment": ["kevlar.png", "kevlar + helmet.png", "zeus x27.png"],
            "2 Pistols": ["g18.png", "dual barettas.png", "p250.png", "tec9.png", "deagle.png"],
            "3 Mid-Tier": ["nova.png", "xm1014.png", "mp5sd.png", "p90.png", "mac10.png"],
            "4 Rifles": ["galil.png", "ak47.png", "ssg 08.png", "sg553.png", "awp.png"],
            "5 Grenades": ["flashbang.png", "smoke.png", "he.png", "molo.png", "decoy.png"]
        }

        # Mapping of file names to desired button names
        button_names = {
            "kevlar.png": "Kevlar Vest",
            "kevlar + helmet.png": "Kevlar + Helmet",
            "zeus x27.png": "Zeus 27",
            "g18.png": "Glock-18",
            "dual barettas.png": "Dual Barettas",
            "p250.png": "P250",
            "tec9.png": "Tec-9",
            "deagle.png": "Desert Eagle",
            "nova.png": "Nova",
            "xm1014.png": "XM1014",
            "mp5sd.png": "MP5-SD",
            "p90.png": "P90",
            "mac10.png": "MAC-10",
            "galil.png": "Galil AR",
            "ak47.png": "AK-47",
            "ssg 08.png": "SSG 08",
            "sg553.png": "SG 553",
            "awp.png": "AWP",
            "flashbang.png": "Flashbang",
            "smoke.png": "Smoke Grenade",
            "he.png": "Explosive Grenade",
            "molo.png": "Molotov",
            "decoy.png": "Decoy Grenade"
        }
        
        for category, category_images in categories.items():
            category_frame = Frame(t_admin_window, bd=2, relief="groove", bg="#2b2b2b")
            category_frame.pack(padx=5, pady=5, side=LEFT, fill="both", expand=False)

            category_label = Label(category_frame, text=category, bg="#2b2b2b", fg="#ffffff", font=("Arial Black", 14, "bold"))
            category_label.pack(padx=5, pady=5)

            # Create a frame for buttons under each category
            button_frame = Frame(category_frame, bg="#2b2b2b")
            button_frame.pack(padx=5, pady=5, fill="both", expand=True)

         # Create buttons with images and names for each category
            for index, image_name in enumerate(category_images, start=1):
                image_path = os.path.join(image_folder, image_name)
                image = Image.open(image_path)
                image.thumbnail((100, 45))  # Resize image
                button_image = ImageTk.PhotoImage(image)

                # Get the desired button name from the mapping
                button_name = button_names.get(image_name, "Unnamed")

                button = Button(button_frame, image=button_image, text=f"{index}. {button_name} \n${self.prices[button_name]}",
                                compound="top", justify="center", padx=10, pady=10, bg="#444444", fg="#FFBF00", font=("Arial", 12, "bold"),
                                command=lambda name=button_name, price=self.prices[button_name]: self.update_product(name, price))
                button.image = button_image
                button.pack(pady=5, padx=5, fill="both", expand=True)

         #Cart frame
        self.cart_frame = Frame(t_admin_window, bd=2, relief="groove", bg="#2b2b2b")
        self.cart_frame.pack(padx=5, pady=5, side=RIGHT, fill="both", expand=True)

        # Cart listbox
        self.cart_label = Label(self.cart_frame, text="MY CART:", font=("Arial Black", 14, "bold"), bg="#2b2b2b", fg="White")
        self.cart_label.pack(padx=10, pady=10, anchor="w")

        self.dash_frame = Frame(self.cart_frame, bg="#2b2b2b")
        self.dash_frame.pack(padx=5, pady=5, side="top", anchor="w")

        self.item = Label(self.dash_frame, text="Item:", font=("Arial Black", 13, "bold"), bg="#2b2b2b", fg="White")
        self.item.pack(padx=5, pady=5, side="left")

        self.quantity = Label(self.dash_frame, text="Quantity & Price:", font=("Arial Black", 13, "bold"), bg="#2b2b2b", fg="White")
        self.quantity.pack(padx=130, pady=5, side="left")
        
        self.cart_listbox = Listbox(self.cart_frame, justify="left", height=22, font=("Courier", 13, "bold"))
        self.cart_listbox.pack(padx=5, pady=5, fill="both", expand=False)

        #product label
        self.product_name = Label(self.cart_frame, text="Product: ", font=("Arial Black", 13, "bold"), bg="#2b2b2b", fg="White")
        self.product_name.pack(padx=10, pady=5, side="top", anchor="w")

        # Quantity label and entry
        self.quantity_frame = Frame(self.cart_frame, bg="#2b2b2b")
        self.quantity_frame.pack(padx=5, pady=5, side="top", anchor="w")

        self.quantity_label = Label(self.quantity_frame, text="Quantity:", bg="#2b2b2b", fg="White", font=("Arial Black", 13, "bold"))
        self.quantity_label.pack(padx=5, pady=5, side="left")

        self.quantity_entry = Entry(self.quantity_frame, textvariable=self.quantity_var, width=8, font=("Arial Black", 13))
        self.quantity_entry.pack(padx=5, pady=5, side="left")

        # Add to cart button and Remove from cart button
        self.add_button_frame = Frame(self.cart_frame, bg="#2b2b2b")
        self.add_button_frame.pack(padx=5, pady=5, side="top", anchor="center")

        self.add_button = Button(self.add_button_frame, text="Add to Cart", command=lambda: self.add_to_cart(self.cart_listbox, self.selected_product, self.prices[self.selected_product]),
                                font=("Arial Black", 12, "bold"), bg="#3cba54", fg="white")
        self.add_button.pack(padx=10, pady=5, side="left")

        self.remove_button = Button(self.add_button_frame, text="Remove Item", command=self.remove_item, font=("Arial Black", 13, "bold"), bg="#FF6347", fg="white")
        self.remove_button.pack(padx=10, pady=5, side="left")

        self.clear_button = Button(self.add_button_frame, text="Clear List", command=self.clear, font=("Arial Black", 13, "bold"), bg="#FFA500", fg="white")
        self.clear_button.pack(padx=10, pady=5, side="left")

        # Total label
        self.total_label_frame = Frame(self.cart_frame, bg="#2b2b2b")
        self.total_label_frame.pack(padx=5, pady=5, side="top", anchor="e")

        self.total_label = Label(self.total_label_frame, text="TOTAL: $0.00", font=("Arial Black", 14, "bold"), bg="#2b2b2b", fg="White")
        self.total_label.pack(padx=10, pady=5, side="left")

        self.balance_label = Label(self.total_label_frame, text="CASH: $ ", font=("Arial Black", 13, "bold"), bg="#2b2b2b", fg="White")
        self.balance_label.pack(padx=10, pady=5, side="left")
        self.balance_entry = Entry(self.total_label_frame, textvariable=self.balance_var, font=("Arial Black", 13, "bold"), bg="#2b2b2b", fg="White")
        self.balance_entry.pack(pady=5, side="left")

        # Checkout Button
        self.checkout_button_frame = Frame(self.cart_frame, bg="#2b2b2b")
        self.checkout_button_frame.pack(padx=10, pady=5, side="top", anchor="e")

        self.checkout_button = Button(self.checkout_button_frame, text="CHECKOUT", command=self.confirm_order, font=("Arial Black", 13, "bold"), bg="#0D47A1", fg="white")
        self.checkout_button.pack(padx=10, pady=5, side="right")



    def clear_login_frame(self):
        for widget in self.login_frame.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = Tk()
    app = AdminSystem(root)
    root.mainloop()