import tkinter as tk
from tkinter import font as tkfont
import random

# Define all Pokémon types and their unique colors
all_types = [
    "Normal", "Fire", "Water", "Electric", "Grass", "Ice", "Fighting",
    "Poison", "Ground", "Flying", "Psychic", "Bug", "Rock", "Ghost",
    "Dragon", "Dark", "Steel", "Fairy"
]

type_colors = {
    "Normal": "#A8A878", "Fire": "#F08030", "Water": "#6890F0", "Electric": "#F8D030",
    "Grass": "#78C850", "Ice": "#98D8D8", "Fighting": "#C03028", "Poison": "#A040A0",
    "Ground": "#E0C068", "Flying": "#A890F0", "Psychic": "#F85888", "Bug": "#A8B820",
    "Rock": "#B8A038", "Ghost": "#705898", "Dragon": "#7038F8", "Dark": "#705848",
    "Steel": "#B8B8D0", "Fairy": "#F0B6BC"
}

type_weaknesses = {
    "Normal": ["Fighting"], "Fire": ["Water", "Ground", "Rock"], "Water": ["Electric", "Grass"],
    "Electric": ["Ground"], "Grass": ["Fire", "Ice", "Poison", "Flying", "Bug"], "Ice": ["Fire", "Fighting", "Rock", "Steel"],
    "Fighting": ["Flying", "Psychic", "Fairy"], "Poison": ["Ground", "Psychic"], "Ground": ["Water", "Grass", "Ice"],
    "Flying": ["Electric", "Ice", "Rock"], "Psychic": ["Bug", "Ghost", "Dark"], "Bug": ["Fire", "Flying", "Rock"],
    "Rock": ["Water", "Grass", "Fighting", "Ground", "Steel"], "Ghost": ["Ghost", "Dark"], "Dragon": ["Ice", "Dragon", "Fairy"],
    "Dark": ["Fighting", "Bug", "Fairy"], "Steel": ["Fire", "Fighting", "Ground"], "Fairy": ["Poison", "Steel"]
}

type_immunities = {
    "Normal": ["Ghost"], "Ground": ["Electric"], "Flying": ["Ground"],
    "Ghost": ["Normal", "Fighting"], "Dark": ["Psychic"], "Steel": ["Poison"], "Fairy": ["Dragon"]
}

type_strengths = {
    "Normal": [], "Fire": ["Grass", "Ice", "Bug", "Steel"], "Water": ["Fire", "Ground", "Rock"],
    "Electric": ["Water", "Flying"], "Grass": ["Water", "Ground", "Rock"], "Ice": ["Grass", "Ground", "Flying", "Dragon"],
    "Fighting": ["Normal", "Ice", "Rock", "Dark", "Steel"], "Poison": ["Grass", "Fairy"], "Ground": ["Fire", "Electric", "Poison", "Rock", "Steel"],
    "Flying": ["Grass", "Fighting", "Bug"], "Psychic": ["Fighting", "Poison"], "Bug": ["Grass", "Psychic", "Dark"],
    "Rock": ["Fire", "Ice", "Flying", "Bug"], "Ghost": ["Psychic", "Ghost"], "Dragon": ["Dragon"],
    "Dark": ["Psychic", "Ghost"], "Steel": ["Ice", "Rock", "Fairy"], "Fairy": ["Fighting", "Dragon", "Dark"]
}

type_resistances = {
    "Normal": [], "Fire": ["Bug", "Ice", "Fire"], "Water": [], "Electric": [], "Grass": ["Bug"],
    "Ice": [], "Fighting": [], "Poison": [], "Ground": [], "Flying": [], "Psychic": [], "Bug": [],
    "Rock": [], "Ghost": [], "Dragon": [], "Dark": [], "Steel": [], "Fairy": []
}

def get_weaknesses_strengths_immunities(type1, type2=None):
    weaknesses = set(type_weaknesses.get(type1.capitalize(), []))
    immunities = set(type_immunities.get(type1.capitalize(), []))
    strengths = set(type_strengths.get(type1.capitalize(), []))
    resistances = set(type_resistances.get(type1.capitalize(), []))

    if type2:
        weaknesses.update(type_weaknesses.get(type2.capitalize(), []))
        immunities.update(type_immunities.get(type2.capitalize(), []))
        strengths.update(type_strengths.get(type2.capitalize(), []))
        resistances.update(type_resistances.get(type2.capitalize(), []))

    filtered_weaknesses = [w for w in weaknesses if w not in immunities]
    filtered_weaknesses = [w for w in filtered_weaknesses if w not in resistances]
    return sorted(filtered_weaknesses), sorted(list(immunities)), sorted(list(strengths))

def calculate_4x_weaknesses(type1, type2=None):
    type1_weaknesses = set(type_weaknesses.get(type1.capitalize(), []))
    type2_weaknesses = set(type_weaknesses.get(type2.capitalize(), [])) if type2 else set()
    combined_weaknesses = type1_weaknesses.intersection(type2_weaknesses)
    return sorted(combined_weaknesses)

def calculate_4x_resistances(type1, type2=None):
    type1_resistances = set(type_resistances.get(type1.capitalize(), []))
    type2_resistances = set(type_resistances.get(type2.capitalize(), [])) if type2 else set()
    combined_resistances = type1_resistances.intersection(type2_resistances)
    return sorted(combined_resistances)

def update_suggestions(menu, listbox, type_color_map):
    typed = menu.get().strip().capitalize()
    listbox.delete(0, tk.END)
    if typed:
        for item in all_types:
            if item.startswith(typed):
                listbox.insert(tk.END, item)
        if listbox.size() > 0:
            listbox.place(x=menu.winfo_x(), y=menu.winfo_y() + menu.winfo_height())
            listbox.lift()
            for index in range(listbox.size()):
                type_name = listbox.get(index)
                listbox.itemconfig(index, {'bg': type_color_map.get(type_name, "#ffffff")})
        else:
            listbox.place_forget()
    else:
        listbox.place_forget()

def select_suggestion(event, var, listbox):
    selected = listbox.curselection()
    if selected:
        var.set(listbox.get(selected[0]))
        listbox.place_forget()

def clear_inputs():
    type1_var.set("")
    type2_var.set("")
    listbox_suggestions1.place_forget()
    listbox_suggestions2.place_forget()

def display_results():
    type1 = type1_var.get().strip()
    type2 = type2_var.get().strip() or None

    if type1.capitalize() not in all_types or (type2 and type2.capitalize() not in all_types):
        result_text.set("Onbekende type(s) ingevoerd.")
        result_area.config(bg="#FFDDDD")
        clear_inputs()
        return

    if type2:
        weaknesses, immunities, strengths = get_weaknesses_strengths_immunities(type1, type2)
        fourx_weaknesses = calculate_4x_weaknesses(type1, type2)
        fourx_resistances = calculate_4x_resistances(type1, type2)
    else:
        weaknesses, immunities, strengths = get_weaknesses_strengths_immunities(type1)
        fourx_weaknesses = []
        fourx_resistances = []

    # Ensure there is no overlap between weaknesses and resistances
    normal_weaknesses = [w for w in weaknesses if w not in fourx_weaknesses and w not in strengths and w not in immunities]
    normal_resistances = [r for r in strengths if r not in fourx_resistances and r not in weaknesses and r not in immunities]

    result_message = f"Resultaten voor {' en '.join(filter(None, [type1, type2]))}:\n\n"

    # Add sections to the result message only if they are not empty
    if fourx_weaknesses:
        result_message += f"• 4x Zwakheden: {', '.join(fourx_weaknesses)}\n"

    if normal_weaknesses:
        result_message += f"• Gewone Zwakheden: {', '.join(normal_weaknesses)}\n"

    if fourx_resistances:
        result_message += f"• 4x Weerstanden: {', '.join(fourx_resistances)}\n"

    if normal_resistances:
        result_message += f"• Gewone Weerstanden: {', '.join(normal_resistances)}\n"

    if strengths:
        result_message += f"• Sterktes: {', '.join(strengths)}\n"

    if immunities:
        result_message += f"• Immuniteiten: {', '.join(immunities)}\n"

    if result_message == f"Resultaten voor {' en '.join(filter(None, [type1, type2]))}:\n\n":
        result_message = "Geen relevante resultaten gevonden."

    result_text.set(result_message)
    result_area.config(bg="#FFFFFF")
    clear_inputs()

def randomize_types():
    selected_types = random.sample(all_types, random.choice([1, 2]))
    type1_var.set(selected_types[0])
    
    if len(selected_types) > 1:
        type2_var.set(selected_types[1])
    else:
        type2_var.set("")

root = tk.Tk()
root.title("Pokémon Type Zwakheden, Immuniteiten en Sterktes")
root.geometry("900x600")  # Verhoogde breedte en hoogte van het venster
root.configure(bg="#f4f4f9")

default_font = tkfont.Font(family="Helvetica", size=12)
header_font = tkfont.Font(family="Helvetica", size=14, weight="bold")

# Labels and Entry fields
tk.Label(root, text="Kies het eerste type:", font=header_font, bg="#f4f4f9", fg="#333333").grid(row=0, column=0, padx=10, pady=5, sticky="w")
tk.Label(root, text="Kies het tweede type (optioneel):", font=header_font, bg="#f4f4f9", fg="#333333").grid(row=1, column=0, padx=10, pady=5, sticky="w")

type1_var = tk.StringVar()
type1_var.set("")  # Default to empty
type1_menu = tk.Entry(root, textvariable=type1_var, font=default_font, width=20)
type1_menu.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

type2_var = tk.StringVar()
type2_var.set("")  # Default to empty
type2_menu = tk.Entry(root, textvariable=type2_var, font=default_font, width=20)
type2_menu.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

# Create listboxes for type suggestions
listbox_suggestions1 = tk.Listbox(root, height=5, font=default_font)
listbox_suggestions1.bind("<Double-1>", lambda e: select_suggestion(e, type1_var, listbox_suggestions1))
listbox_suggestions2 = tk.Listbox(root, height=5, font=default_font)
listbox_suggestions2.bind("<Double-1>", lambda e: select_suggestion(e, type2_var, listbox_suggestions2))

type1_menu.bind("<KeyRelease>", lambda e: update_suggestions(type1_menu, listbox_suggestions1, type_colors))
type2_menu.bind("<KeyRelease>", lambda e: update_suggestions(type2_menu, listbox_suggestions2, type_colors))

def on_tab(event):
    if listbox_suggestions1.place_info():
        listbox_suggestions1.focus_set()
        listbox_suggestions1.select_set(0)
        listbox_suggestions1.event_generate('<Down>')
    elif listbox_suggestions2.place_info():
        listbox_suggestions2.focus_set()
        listbox_suggestions2.select_set(0)
        listbox_suggestions2.event_generate('<Down>')
    return "break"

def on_enter(event):
    if listbox_suggestions1.place_info():
        select_suggestion(event, type1_var, listbox_suggestions1)
    elif listbox_suggestions2.place_info():
        select_suggestion(event, type2_var, listbox_suggestions2)
    return "break"

root.bind('<Tab>', on_tab)
root.bind('<Return>', on_enter)

# Buttons
tk.Button(root, text="Bereken", font=default_font, command=display_results, bg="#007BFF", fg="#FFFFFF").grid(row=2, column=0, padx=10, pady=10, sticky="ew")
tk.Button(root, text="Willekeurig Type", font=default_font, command=randomize_types, bg="#28A745", fg="#FFFFFF").grid(row=3, column=0, padx=10, pady=10, sticky="ew")

# Adjusted the results area to be taller
result_text = tk.StringVar()
result_area = tk.Frame(root, bg="#ffffff", borderwidth=1, relief="solid")
result_label = tk.Label(result_area, textvariable=result_text, font=default_font, bg="#ffffff", fg="#333333", justify=tk.LEFT, anchor='nw', padx=10, pady=10)

# Increased padding and set the fill and expand options to allow the label to stretch
result_label.pack(fill=tk.BOTH, expand=True)
result_area.grid(row=4, column=0, columnspan=3, padx=10, pady=10, sticky='nsew')

# Place the suggestion listboxes below the second input and next to the buttons
listbox_suggestions1.grid(row=2, column=1, padx=10, pady=5, sticky="ew")
listbox_suggestions2.grid(row=3, column=1, padx=10, pady=5, sticky="ew")

# Hide the suggestion listboxes initially
listbox_suggestions1.place_forget()
listbox_suggestions2.place_forget()

# Modify grid row configuration to expand more
root.columnconfigure(1, weight=1)
root.rowconfigure(4, weight=3)  # Increased weight to make the results box taller

# Start the main loop
root.mainloop()
