import os
import tkinter as tk
from tkinter import messagebox, ttk

import requests
from PIL import Image, ImageTk


def fetch_product_data():
    headers = {
        "Authorization": "Token 01b7b793ffde9ee0c4f6d9ba0e7d985ac6ce330c"
    }

    response = requests.get("http://localhost:8000/products/", headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        messagebox.showerror(
            "Error", "Failed to fetch product data from the API."
        )
        return []


def fetch_categories():
    headers = {
        "Authorization": "Token 01b7b793ffde9ee0c4f6d9ba0e7d985ac6ce330c"
    }

    response = requests.get(
        "http://localhost:8000/categories/", headers=headers
    )

    if response.status_code == 200:
        return response.json()
    else:
        messagebox.showerror(
            "Error", "Failed to fetch categories from the API."
        )
        return []


root = tk.Tk()
root.title("E-commerce App")

frame = ttk.Frame(root)
frame.pack()

columns = ("Name", "Category", "Price")
tree = ttk.Treeview(frame, columns=columns, show="headings")
tree.heading("Name", text="Name")
tree.heading("Category", text="Category")
tree.heading("Price", text="Price")
tree.pack()


def populate_product_list():
    product_data = fetch_product_data()
    categories = fetch_categories()

    for item in tree.get_children():
        tree.delete(item)

    for product in product_data:
        name = product["name"]
        category = categories[0]["name"]
        price = product["price"]

        thumbnail_url = product["thumbnail"]

        temp = thumbnail_url.split("/")
        thumbnail_name = temp[len(temp) - 1]

        path = os.getcwd()
        thumbnail_path = (
            path + "/ecommerce_project/assets/thumbnails/" + thumbnail_name
        )

        img = Image.open(thumbnail_path)
        thumbnail = ImageTk.PhotoImage(img)

        tree.insert("", "end", values=(name, category, price), image=thumbnail)


refresh_button = ttk.Button(
    frame, text="Refresh", command=populate_product_list
)
refresh_button.pack()

populate_product_list()

root.mainloop()
