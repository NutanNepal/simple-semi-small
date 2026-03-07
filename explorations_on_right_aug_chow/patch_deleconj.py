import json

with open("deleconjright.ipynb", "r") as f:
    nb = json.load(f)

# Find the cell we want to modify (the one that starts with flat_division)
target_idx = None
for i, cell in enumerate(nb["cells"]):
    if cell["cell_type"] == "code" and "def flat_division" in "".join(cell["source"]):
        target_idx = i
        break

if target_idx is not None:
    source = nb["cells"][target_idx]["source"]
    
    new_source = []
    for line in source:
        new_source.append(line)
        if "return flat_div" in line:
            new_source.append("\n")
            new_source.append("def get_pal0_part(f):\n")
            new_source.append("    \"\"\"\n")
            new_source.append("    Extracts the Pal(0) part of a Laurent polynomial f.\n")
            new_source.append("    \"\"\"\n")
            new_source.append("    if f == 0: return f\n")
            new_source.append("    x_var = f.parent().gen()\n")
            new_source.append("    f_inv = f.subs({x_var: x_var**-1})\n")
            new_source.append("    numerator = (x_var**2) * f_inv - f\n")
            new_source.append("    denominator = (x_var**2) - 1\n")
            new_source.append("    q, r = numerator.quo_rem(denominator)\n")
            new_source.append("    return q\n")
            new_source.append("\n")
            
    nb["cells"][target_idx]["source"] = new_source
    
    with open("deleconjright.ipynb", "w") as f:
        json.dump(nb, f, indent=1)
    
    print("Notebook updated successfully.")
else:
    print("Target cell not found.")
