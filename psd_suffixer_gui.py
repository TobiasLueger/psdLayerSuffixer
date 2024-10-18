import customtkinter as ctk
import os
import webbrowser  # To open the tip link in the default web browser
from tkinter import filedialog, messagebox
from psd_tools import PSDImage
from collections import defaultdict
import json
import tempfile



def rename_duplicate_layers(psd, suffix='_'):
    # Collect all layer names and count their occurrences
    name_counts = defaultdict(int)
    for layer in psd.descendants():
        name_counts[layer.name] += 1

    # Rename duplicate layers
    name_counters = defaultdict(int)
    for layer in psd.descendants():
        if name_counts[layer.name] > 1:
            name_counters[layer.name] += 1
            new_name = f"{layer.name}{suffix}{name_counters[layer.name]}"
            print(f"Renaming layer '{layer.name}' to '{new_name}'")
            layer.name = new_name
        else:
            print(f"Layer '{layer.name}' is unique. No renaming needed.")

def main():
    # Set appearance mode and default color theme
    ctk.set_appearance_mode("light")

    pink_theme_json = '''
    {
    "CTk": {
        "fg_color": ["#FBE8E6", "#6D4C6C"]
    },
    "CTkToplevel": {
        "fg_color": ["#FBE8E6", "#6D4C6C"]
    },
    "CTkFrame": {
        "corner_radius": 6,
        "border_width": 0,
        "fg_color": ["#FFF1EA", "#5D3A4A"],
        "top_fg_color": ["#F4D8D0", "#5A2F3E"],
        "border_color": ["#C6A6A5", "#6F3D4B"]
    },
    "CTkButton": {
        "corner_radius": 6,
        "border_width": 0,
        "fg_color": ["#F29C9C", "#BF3E3E"],
        "hover_color": ["#F5B3B3", "#C85C5C"],
        "border_color": ["#F4A3A0", "#A8A8A8"],
        "text_color": ["#FFFFFF", "#FFFFFFF"],
        "text_color_disabled": ["#D8A7A2", "#B68D8D"]
    },
    "CTkLabel": {
        "corner_radius": 0,
        "fg_color": "transparent",
        "text_color": ["#6D4C6C", "#FDF5F5"]
    },
    "CTkEntry": {
        "corner_radius": 6,
        "border_width": 1,
        "fg_color": ["#FDF5F5", "#3C2A2F"],
        "border_color": ["#D8A7A2", "#6F3D4B"],
        "text_color": ["#6D4C6C", "#FDF5F5"],
        "placeholder_text_color": ["#C5A2A2", "#B68D8D"]
    },
    "CTkCheckBox": {
        "corner_radius": 6,
        "border_width": 3,
        "fg_color": ["#F5B3B3", "#C85C5C"],
        "border_color": ["#F4A3A0", "#A8A8A8"],
        "hover_color": ["#F5B3B3", "#C85C5C"],
        "checkmark_color": ["#FDF5F5", "#D8A7A2"],
        "text_color": ["#6D4C6C", "#FDF5F5"],
        "text_color_disabled": ["#B68D8D", "#A67D7D"]
    },
    "CTkSwitch": {
        "corner_radius": 1000,
        "border_width": 3,
        "button_length": 0,
        "fg_color": ["#D8A7A2", "#6F3D4B"],
        "progress_color": ["#F5B3B3", "#C85C5C"],
        "button_color": ["#6D4C6C", "#F6E7E6"],
        "button_hover_color": ["#5C3B3B", "#F9F9F9"],
        "text_color": ["#6D4C6C", "#FDF5F5"],
        "text_color_disabled": ["#B68D8D", "#A67D7D"]
    },
    "CTkRadioButton": {
        "corner_radius": 1000,
        "border_width_checked": 6,
        "border_width_unchecked": 3,
        "fg_color": ["#F5B3B3", "#C85C5C"],
        "border_color": ["#F4A3A0", "#A8A8A8"],
        "hover_color": ["#F29C9C", "#BF3E3E"],
        "text_color": ["#6D4C6C", "#FDF5F5"],
        "text_color_disabled": ["#B68D8D", "#A67D7D"]
    },
    "CTkProgressBar": {
        "corner_radius": 1000,
        "border_width": 0,
        "fg_color": ["#D8A7A2", "#6F3D4B"],
        "progress_color": ["#F5B3B3", "#C85C5C"],
        "border_color": ["#B68D8D", "#B68D8D"]
    },
    "CTkSlider": {
        "corner_radius": 1000,
        "button_corner_radius": 1000,
        "border_width": 6,
        "button_length": 0,
        "fg_color": ["#D8A7A2", "#6F3D4B"],
        "progress_color": ["#C5A2A2", "#B68D8D"],
        "button_color": ["#F5B3B3", "#C85C5C"],
        "button_hover_color": ["#F29C9C", "#BF3E3E"]
    },
    "CTkOptionMenu": {
        "corner_radius": 6,
        "fg_color": ["#F5B3B3", "#C85C5C"],
        "button_color": ["#F29C9C", "#BF3E3E"],
        "button_hover_color": ["#E57C7C", "#B64D4D"],
        "text_color": ["#FDF5F5", "#FDF5F5"],
        "text_color_disabled": ["#D8A7A2", "#B68D8D"]
    },
    "CTkComboBox": {
        "corner_radius": 6,
        "border_width": 2,
        "fg_color": ["#FDF5F5", "#3C2A2F"],
        "border_color": ["#D8A7A2", "#6F3D4B"],
        "button_color": ["#D8A7A2", "#6F3D4B"],
        "button_hover_color": ["#C5A2A2", "#B68D8D"],
        "text_color": ["#6D4C6C", "#FDF5F5"],
        "text_color_disabled": ["#C5A2A2", "#A67D7D"]
    },
    "CTkScrollbar": {
        "corner_radius": 1000,
        "border_spacing": 4,
        "fg_color": "transparent",
        "button_color": ["#D8A7A2", "#6F3D4B"],
        "button_hover_color": ["#C5A2A2", "#B68D8D"]
    },
    "CTkSegmentedButton": {
        "corner_radius": 6,
        "border_width": 2,
        "fg_color": ["#D8A7A2", "#6F3D4B"],
        "selected_color": ["#F5B3B3", "#C85C5C"],
        "selected_hover_color": ["#F29C9C", "#BF3E3E"],
        "unselected_color": ["#D8A7A2", "#6F3D4B"],
        "unselected_hover_color": ["#C5A2A2", "#B68D8D"],
        "text_color": ["#FDF5F5", "#FDF5F5"],
        "text_color_disabled": ["#D8A7A2", "#B68D8D"]
    },
    "CTkTextbox": {
        "corner_radius": 6,
        "border_width": 0,
        "fg_color": ["#FDF5F5", "#3C2A2F"],
        "border_color": ["#D8A7A2", "#6F3D4B"],
        "text_color": ["#6D4C6C", "#FDF5F5"],
        "scrollbar_button_color": ["#D8A7A2", "#6F3D4B"],
        "scrollbar_button_hover_color": ["#C5A2A2", "#B68D8D"]
    },
    "CTkScrollableFrame": {
        "label_fg_color": ["#F1D3D1", "#6F3D4B"]
    },
    "DropdownMenu": {
        "fg_color": ["#FBE8E6", "#6F3D4B"],
        "hover_color": ["#F4D8D0", "#5A2F3E"],
        "text_color": ["#6D4C6C", "#FBE8E6"]
    },
    "CTkFont": {
        "macOS": {
        "family": "SF Display",
        "size": 13,
        "weight": "bold"
        },
        "Windows": {
        "family": "Roboto",
        "size": 13,
        "weight": "bold"
        },
        "Linux": {
        "family": "bold",
        "size": 13,
        "weight": "normal"
        }
    }
    }
    '''
    # theme_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "pink.json")
    # ctk.set_default_color_theme(theme_path)
    # ctk.ThemeManager.load_theme(json.loads(pink_theme_json))
    # Create a temporary file to hold the theme
    with tempfile.NamedTemporaryFile('w', delete=False, suffix='.json') as tmp_theme_file:
        tmp_theme_file.write(pink_theme_json)
        tmp_theme_file_path = tmp_theme_file.name

    # Set the theme using the path to the temporary file
    ctk.set_default_color_theme(tmp_theme_file_path)

    app = ctk.CTk()
    app.title("PSD Layer Renamer")
    app.geometry("500x430")  # Increased height to accommodate new elements
    app.resizable(False, False)

    # Define StringVars
    input_file_path = ctk.StringVar()
    output_folder_path = ctk.StringVar()

    def select_input_file():
        file_path = filedialog.askopenfilename(
            title="Select Input PSD File",
            filetypes=[("PSD files", "*.psd")]
        )
        input_file_path.set(file_path)

    def select_output_folder():
        folder_path = filedialog.askdirectory(
            title="Select Output Folder"
        )
        output_folder_path.set(folder_path)

    def start_process():
        input_file = input_file_path.get()
        output_folder = output_folder_path.get()

        if not input_file:
            messagebox.showerror("Error", "Please select an input file.")
            return
        if not output_folder:
            messagebox.showerror("Error", "Please select an output folder.")
            return

        try:
            psd = PSDImage.open(input_file)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open PSD file:\n{e}")
            return

        # Rename layers
        rename_duplicate_layers(psd)

        # Construct the output file path
        input_filename = os.path.basename(input_file)
        name, ext = os.path.splitext(input_filename)
        output_filename = f"{name}_new{ext}"
        output_file = os.path.join(output_folder, output_filename)

        # Save the modified PSD file
        try:
            psd.save(output_file)
            messagebox.showinfo("Success", f"Modified PSD saved as '{output_file}'.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save PSD file:\n{e}")

    # Function to open the tip link
    def open_tip_link(event):
        webbrowser.open_new("https://streamelements.com/oftoto/tip")  # Replace with your actual tip link

    # GUI Layout with padding
    padding = {"padx": 20, "pady": 10}

    # Add spacing at the top
    top_spacing = ctk.CTkLabel(app, text="", height=20)
    top_spacing.pack()  # Adds space at the top

    # Input File Widgets
    input_label = ctk.CTkLabel(app, text="Input PSD File:", font=("Helvetica", 14))
    input_label.pack(**padding)

    input_entry = ctk.CTkEntry(app, textvariable=input_file_path, width=300)
    input_entry.pack()

    input_button = ctk.CTkButton(app, text="Browse", command=select_input_file)
    input_button.pack(**padding)

    # Output Folder Widgets
    output_label = ctk.CTkLabel(app, text="Output Folder:", font=("Helvetica", 14))
    output_label.pack(**padding)

    output_entry = ctk.CTkEntry(app, textvariable=output_folder_path, width=300)
    output_entry.pack()

    output_button = ctk.CTkButton(app, text="Browse", command=select_output_folder)
    output_button.pack(**padding)

    # Start Button
    start_button = ctk.CTkButton(app, text="Start Renaming", command=start_process)
    start_button.pack(pady=30)

    # Tip Link Label
    tip_label = ctk.CTkLabel(
        app,
        text="💖 If you like the tool, you can by me a coffee here.",
        font=("Helvetica", 12, "underline"),
        text_color="#e09090",
        cursor="hand2"  # Changes cursor to hand icon when hovered
    )
    tip_label.pack(pady=10)

    # Make the "here" part clickable
    tip_label.bind("<Button-1>", open_tip_link)

    app.mainloop()

if __name__ == '__main__':
    main()