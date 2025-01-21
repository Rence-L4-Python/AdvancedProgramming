import requests
import customtkinter
import tkinter as tk
from tkinter import messagebox
from CTkScrollableDropdown import *

from objectsforuse import currencies
from api_key_config import API_KEY

BASE_URL = "https://api.freecurrencyapi.com/v1/latest"

def get_currency_rate(base_currency, target_currency):
    params = {
        "apikey": API_KEY,
        "base_currency": base_currency,
        "currencies": target_currency
    }
    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()
        return data["data"].get(target_currency, None)
    except requests.exceptions.RequestException as e:
        messagebox.showerror("API Error", f"Failed to fetch data: {e}")
        return None

def convert_currency():
    base_currency = base_currency_var.get().split(" - ")[0]
    target_currency = target_currency_var.get().split(" - ")[0]
    amount = amount_entry.get()

    if not amount.isdigit():
        result_entry.configure(state="normal")
        result_entry.delete(0, "end")
        result_entry.insert(0, "Enter a number before converting!")
        result_entry.configure(state="readonly")
        return
    
    amount = float(amount)
    rate = get_currency_rate(base_currency, target_currency)

    if rate:
        converted_amount = round(amount * rate, 2)
        result_entry.configure(state="normal")
        result_entry.delete(0, "end")
        result_entry.insert(0, f"{converted_amount} {target_currency}")
        result_entry.configure(state="readonly")
    else:
        result_entry.configure(state="normal")
        result_entry.delete(0, "end")
        result_entry.insert(0, "Conversion Failed")
        result_entry.configure(state="readonly")

def swap_currencies():
    temp = base_currency_var.get()
    base_currency_var.set(target_currency_var.get())
    target_currency_var.set(temp)

def validate_numeric_input(action, value_if_allowed):
    if action == "1":
        return value_if_allowed.replace(".", "", 1).isdigit()
    return True

# Tkinter Base
customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("green")

root = customtkinter.CTk()
root.title("How Much Is A Meal? A Comparison Calculator")
root.geometry("1500x750")
root.resizable(False, False)

section_left = customtkinter.CTkFrame(root, corner_radius=0)
section_left.pack(fill="both", expand=True, anchor="w", side="left")
section_right = customtkinter.CTkFrame(root, corner_radius=0, width=450)
section_right.configure(fg_color="#364C96")
section_right.pack(fill="both", anchor="e", side="right")

#region Leaflet.js Map
globalMap = customtkinter.CTkFrame(section_left, corner_radius=0)
globalMap.configure(fg_color="#D9D9D9")
globalMap.pack(fill="both", expand=True, anchor="nw", side="top")
globalMap.pack_propagate(False)
#endregion

#region Meal Comparison
mealComparison = customtkinter.CTkFrame(section_left, corner_radius=0)
mealComparison.configure(fg_color="#9B9B9B")
mealComparison.pack(fill="x", expand=True, anchor="sw", side="left")
mealComparison.pack_propagate(False)
#endregion

#region Currency Converter
currencyConverter = customtkinter.CTkFrame(section_right, corner_radius=0, width=450)
currencyConverter.configure(fg_color="transparent")
currencyConverter.pack(expand=True, ipady=142.5)
currencyConverter.pack_propagate(False)

vcmd = currencyConverter.register(validate_numeric_input)
currencies_display = [f"{key} - {value}" for key, value in currencies.items()]

cc_title = customtkinter.CTkLabel(currencyConverter, text="Currency Converter", font=("Calibri", 36, "bold"), text_color="#FFFFFF")
cc_title.pack(anchor="w", padx=38, pady=(35,0))

base_currency_frame = customtkinter.CTkFrame(currencyConverter, corner_radius=0, border_width=2, width=15)
base_currency_frame.configure(fg_color="#FFFFFF")
base_currency_frame.pack(anchor="w", padx=38, pady=(38,19))
base_currency_var = tk.StringVar(value="USD - United States Dollar")
base_currency_label = customtkinter.CTkLabel(base_currency_frame, text="From", font=("Calibri", 12, "bold"), text_color="gray", height=4, width=40)
base_currency_label.pack(anchor="center", padx=4, pady=0, side="left")
base_currency_dropdown = customtkinter.CTkComboBox(base_currency_frame, variable=base_currency_var, values=currencies_display, font=("Calibri", 12), width=222, corner_radius=0)
base_currency_dropdown.configure(state="readonly")
base_currency_dropdown.pack(anchor="w")
CTkScrollableDropdown(base_currency_dropdown, values=currencies_display, justify="left", button_color="transparent")

amount_entry = customtkinter.CTkEntry(currencyConverter, width=375, validate="key", validatecommand=(vcmd, "%d", "%P"))
amount_entry.pack(pady=(0,19))

swap_button = customtkinter.CTkButton(currencyConverter, text="↑↓", font=("Calibri", 16, "bold"), command=swap_currencies, width= 10)
swap_button.pack(anchor="w", padx=38)

target_currency_frame = customtkinter.CTkFrame(currencyConverter, corner_radius=0, border_width=2, width=15)
target_currency_frame.configure(fg_color="#FFFFFF")
target_currency_frame.pack(anchor="w", padx=38, pady=19)
target_currency_var = tk.StringVar(value="EUR - Euro")
target_currency_label = customtkinter.CTkLabel(target_currency_frame, text="To", font=("Calibri", 12, "bold"), text_color="gray", height=4, width=40)
target_currency_label.pack(anchor="center", padx=4, pady=0, side="left")
target_currency_dropdown = customtkinter.CTkComboBox(target_currency_frame, variable=target_currency_var, values=currencies_display, font=("Calibri", 12), width=222, corner_radius=0)
target_currency_dropdown.configure(state="readonly")
target_currency_dropdown.pack(anchor="w")
CTkScrollableDropdown(target_currency_dropdown, values=currencies_display, justify="left", button_color="transparent")

result_entry = customtkinter.CTkEntry(currencyConverter, width=375)
result_entry.pack(pady=(0,38))
result_entry.configure(state="readonly")

convert_button = customtkinter.CTkButton(currencyConverter, command=convert_currency, text="Convert", font=("Calibri", 24, "bold"), width=112.5, height=60)
convert_button.pack(fill="x", padx=38, pady=10)

#endregion

root.mainloop()