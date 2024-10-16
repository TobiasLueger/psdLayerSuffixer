from psd_tools import PSDImage
from collections import defaultdict

def rename_duplicate_layers(psd, suffix='_'):
    # First, collect all layer names and count their occurrences
    name_counts = defaultdict(int)
    for layer in psd.descendants():
        name_counts[layer.name] += 1

    # Now, create a counter for each name to track renaming
    name_counters = defaultdict(int)
    for layer in psd.descendants():
        if name_counts[layer.name] > 1:
            name_counters[layer.name] += 1
            new_name = f"{layer.name}{suffix}{name_counters[layer.name]}"
            print(f"Renaming layer '{layer.name}' to '{new_name}'")
            layer.name = new_name
        else:
            # No renaming needed if the name is unique
            print(f"Layer '{layer.name}' is unique. No renaming needed.")

def main():
    input_file = input("Geben Sie den Pfad zur Eingabe-PSD-Datei ein: ")
    output_file = input("Geben Sie den Pfad zur Ausgabe-PSD-Datei ein: ")

    # PSD-Datei öffnen
    try:
        psd = PSDImage.open(input_file)
    except FileNotFoundError:
        print(f"Die Datei '{input_file}' wurde nicht gefunden.")
        return

    # Ebenen umbenennen
    rename_duplicate_layers(psd)

    # Geänderte PSD-Datei speichern
    try:
        psd.save(output_file)
        print(f"Die modifizierte PSD wurde als '{output_file}' gespeichert.")
    except Exception as e:
        print(f"Fehler beim Speichern der Datei: {e}")

if __name__ == '__main__':
    main()