import requests
import customtkinter
import tkinter as tk
from tkinter import messagebox
from CTkScrollableDropdown import *
from PIL import Image, ImageTk
import io

from objectsforuse import currencies, countrycodeconversion
from api_key_config import API_KEY

CURR_URL = "https://api.freecurrencyapi.com/v1/latest"
WB_URL = "https://api.worldbank.org/v2/country/{}/indicator/PA.NUS.PPP?format=json"

#region Currency Converter Code
def get_currency_rate(base_currency, target_currency):
    params = {
        "apikey": API_KEY,
        "base_currency": base_currency,
        "currencies": target_currency
    }
    try:
        response = requests.get(CURR_URL, params=params)
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
#endregion

#region World Bank PPP Data Fetcher Code
def get_ppp_conversion_factor(country_code):
    try:
        url = WB_URL.format(country_code)
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        if len(data) > 1 and isinstance(data[1], list):
            for entry in data[1]:
                if "value" in entry and entry["value"] is not None:
                    return entry["value"]
        return None
    except requests.exceptions.RequestException as e:
        messagebox.showerror("API Error", f"Failed to fetch data: {e}")
        return None

def update_ppp_labels():
    base_currency = base_currency_var.get().split(" - ")[0]
    target_currency = target_currency_var.get().split(" - ")[0]

    base_country_code = countrycodeconversion.get(base_currency)
    target_country_code = countrycodeconversion.get(target_currency)

    base_ppp = get_ppp_conversion_factor(base_country_code) if base_country_code else None
    target_ppp = get_ppp_conversion_factor(target_country_code) if target_country_code else None

    pppc_bc_label_value.configure(text=f"{base_currency}: {base_ppp if base_ppp is not None else 'N/A'}")
    pppc_tc_label_value.configure(text=f"{target_currency}: {target_ppp if target_ppp is not None else 'N/A'}")

    if base_ppp is not None and target_ppp is not None:
        ratio = round(base_ppp / target_ppp, 2)
        ppp_ratio_label.configure(text=f"PPP Ratio: {ratio}x ({base_currency} relative to {target_currency})")
    else:
        ppp_ratio_label.configure(text="PPP Ratio: N/A")
#endregion

#region FlagsAPI
def get_flag_image(country_code):
    url = f"https://flagsapi.com/{country_code}/flat/64.png"
    try:
        response = requests.get(url)
        response.raise_for_status()

        image_data = response.content
        image = Image.open(io.BytesIO(image_data))
        return ImageTk.PhotoImage(image)
    except requests.exceptions.RequestException as e:
        print(f"Error loading flag for {country_code}: for {e}")

def update_flags():
    base_currency = base_currency_var.get().split(" - ")[0]
    target_currency = target_currency_var.get().split(" - ")[0]

    base_country_code = countrycodeconversion.get(base_currency)
    target_country_code = countrycodeconversion.get(target_currency)

    if base_country_code:
        base_flag_img = get_flag_image(base_country_code)
        if base_flag_img:
            base_flag_label.configure(image=base_flag_img)
            base_flag_label.image = base_flag_img

    if target_country_code:
        target_flag_img = get_flag_image(target_country_code)
        if target_flag_img:
            target_flag_label.configure(image=target_flag_img)
            target_flag_label.image = target_flag_img
#endregion

# Tkinter Base
customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("green")

root = customtkinter.CTk()
root.title("Currency Exchange")
root.geometry("600x750")
root.resizable(False, False)

section_left = customtkinter.CTkFrame(root, corner_radius=0)
section_left.pack(fill="both", expand=True, anchor="n", side="bottom", pady=0)
section_right = customtkinter.CTkFrame(root, corner_radius=0, width=550)
section_right.configure(fg_color="#364C96")
section_right.pack(fill="both", anchor="s", side="top", pady=0)

#region PPP Comparison
pppComparison = customtkinter.CTkFrame(section_left, corner_radius=0)
pppComparison.configure(fg_color="#1E2746")
pppComparison.pack(fill="both", expand=True, anchor="s", side="left")

pppComparison_frame = customtkinter.CTkFrame(pppComparison, width=500)
pppComparison_frame.configure(fg_color="transparent")
pppComparison_frame.pack()
pppComparison_frame.pack_propagate(False)

pppComparison_title = customtkinter.CTkLabel(pppComparison_frame, text="Purchasing Power Parity (PPP) | LCU per international $", justify="left", font=("Calibri", 16, "bold"), text_color="white")
pppComparison_title.pack(anchor="w", padx=(100,0), pady=(70,0))

pppc_bc_label_value = customtkinter.CTkLabel(pppComparison_frame, text="...", text_color="white", font=("Calibri", 16))
pppc_bc_label_value.pack(anchor="w", padx=(100,0), pady=(0,20))

pppc_tc_label_value = customtkinter.CTkLabel(pppComparison_frame, text="...", text_color="white", font=("Calibri", 16))
pppc_tc_label_value.pack(anchor="w", padx=(100,0), pady=0)

ppp_ratio_label = customtkinter.CTkLabel(pppComparison_frame, text="PPP Ratio: ...", text_color="white", font=("Calibri", 16, "bold"))
ppp_ratio_label.pack(anchor="w", padx=(100,0), pady=0)
#endregion

#region Currency Converter
currencyConverter = customtkinter.CTkFrame(section_right, corner_radius=0, width=450)
currencyConverter.configure(fg_color="transparent")
currencyConverter.pack(expand=True, ipady=142.5)
currencyConverter.pack_propagate(False)

vcmd = currencyConverter.register(validate_numeric_input)
currencies_display = [f"{key} - {value}" for key, value in currencies.items()]

cc_title = customtkinter.CTkLabel(currencyConverter, text="💱 Currency Exchange!", font=("Calibri", 36, "bold"), text_color="#FFFFFF")
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

swap_button = customtkinter.CTkButton(currencyConverter, text="↑↓", font=("Calibri", 16, "bold"), command=lambda:[swap_currencies()], width= 10)
swap_button.pack(anchor="w", padx=38)

target_currency_frame = customtkinter.CTkFrame(currencyConverter, corner_radius=0, border_width=2, width=15)
target_currency_frame.configure(fg_color="#FFFFFF")
target_currency_frame.pack(anchor="w", padx=38, pady=19)
target_currency_var = tk.StringVar(value="PHP - Philippine Peso")
target_currency_label = customtkinter.CTkLabel(target_currency_frame, text="To", font=("Calibri", 12, "bold"), text_color="gray", height=4, width=40)
target_currency_label.pack(anchor="center", padx=4, pady=0, side="left")
target_currency_dropdown = customtkinter.CTkComboBox(target_currency_frame, variable=target_currency_var, values=currencies_display, font=("Calibri", 12), width=222, corner_radius=0)
target_currency_dropdown.configure(state="readonly")
target_currency_dropdown.pack(anchor="w")
CTkScrollableDropdown(target_currency_dropdown, values=currencies_display, justify="left", button_color="transparent")

result_entry = customtkinter.CTkEntry(currencyConverter, width=375)
result_entry.pack(pady=(0,38))
result_entry.configure(state="readonly")

convert_button = customtkinter.CTkButton(currencyConverter, command=lambda:[convert_currency(), update_ppp_labels(), update_flags()], text="Convert", font=("Calibri", 24, "bold"), width=112.5, height=60)
convert_button.pack(fill="x", padx=38, pady=10)
#endregion

#region FlagsAPI
flag_frame = customtkinter.CTkFrame(section_left, fg_color="#1E2746")
flag_frame.place(x=60, y=60)

base_flag_label = tk.Label(flag_frame, bg="#1E2746")
base_flag_label.pack(side="top", pady=(0,10))

target_flag_label = tk.Label(flag_frame, bg="#1E2746")
target_flag_label.pack(side="bottom")
#endregion

update_ppp_labels()
update_flags()
root.mainloop()