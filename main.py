import tkinter as tk
from tkinter import scrolledtext
import sys
import random

# --- GAME STATE ---
lgf_coins = 0
symbol_table = {}
inventory = []
equipped_theme = "Default Theme"

# --- CORE COMPILER LOGIC ---
def lgf_compiler(source_code):
    """Your actual lexical, syntax, and semantic engine."""
    print(f"\nInput Code: {source_code}\n")

    cleaned_code = source_code.replace(":>", " :> ").replace(",", " , ")
    words = cleaned_code.split()

    if not words:
        return

    # LEXER ANALYSIS
    print("--- STARTING LEXICAL ANALYSIS ---")
    tokens = []
    for word in words:
        if word in ["OUNT", "HERO", "TAMARAW", "YEARN"]:
            tokens.append(("DATATYPE", word))
        elif word == "IS":
            tokens.append(("ASSIGN", word))
        elif word == ":>":
            tokens.append(("DELIMITER", word))
        elif word == "RELEASE":
            tokens.append(("OUTPUT_CMD", word))
        elif word == "EndThat":
            tokens.append(("NEWLINE", word))
        elif word == ",":
            tokens.append(("COMMA", word))
        elif word.isdigit():
            tokens.append(("LITERAL_INT", word))
        elif word.startswith('"') and word.endswith('"'):
            tokens.append(("LITERAL_STRING", word))
        elif word.startswith("'") and word.endswith("'") and len(word) == 3:
            tokens.append(("LITERAL_CHAR", word))
        elif word in ["True", "False"]:
            tokens.append(("LITERAL_BOOL", word))
        else:
            tokens.append(("IDENTIFIER", word))
    print("Lexical Analysis Complete.\n")

    # PARSER
    print("--- STARTING SYNTAX ANALYSIS ---")
    is_assignment = False
    is_release = False

    if tokens[0][0] == "DATATYPE":
        is_assignment = True
        if len(tokens) == 5 and (tokens[1][0] == "IDENTIFIER" and tokens[2][0] == "ASSIGN" and tokens[3][0].startswith("LITERAL") and tokens[4][0] == "DELIMITER"):
            print("Syntax Analysis Complete. No structural errors.\n")
        else:
            print("[PARSER] FATAL ERROR: Syntax is invalid. Fix your grammar.")
            return
    elif tokens[0][0] == "OUTPUT_CMD":
        is_release = True
        if tokens[-1][0] != "DELIMITER":
            print("[PARSER] FATAL ERROR: Missing delimiter ':>' at the end.")
            return
        print("Syntax Analysis Complete. No structural errors.\n")
    else:
        print("[PARSER] FATAL ERROR: Unknown statement structure.")
        return

    # SEMANTICS
    print("--- STARTING SEMANTIC ANALYSIS ---")
    if is_assignment:
        var_type, var_name, var_value, literal_type = tokens[0][1], tokens[1][1], tokens[3][1], tokens[3][0]
        
        is_valid_type = (var_type == "OUNT" and literal_type == "LITERAL_INT") or \
                        (var_type == "YEARN" and literal_type == "LITERAL_STRING") or \
                        (var_type == "HERO" and literal_type == "LITERAL_CHAR") or \
                        (var_type == "TAMARAW" and literal_type == "LITERAL_BOOL")

        if is_valid_type:
            symbol_table[var_name] = {"type": var_type, "value": var_value}
            print(f"[SEMANTICS] Binding variable '{var_name}' to Symbol Table.")
        else:
            print(f"[SEMANTICS] FATAL ERROR: Type mismatch. Cannot put {literal_type} into {var_type}.")
            
    elif is_release:
        output_string = ""
        for i in range(1, len(tokens) - 1):
            tok_type, tok_val = tokens[i]
            if tok_type == "IDENTIFIER":
                if tok_val in symbol_table:
                    output_string += str(symbol_table[tok_val]["value"]).replace('"', '').replace("'", "")
                else:
                    print(f"[SEMANTICS] FATAL ERROR: Variable '{tok_val}' is not defined!")
                    return
            elif tok_type.startswith("LITERAL"):
                output_string += str(tok_val).replace('"', '').replace("'", "")
            elif tok_type == "NEWLINE":
                output_string += "\n"
                
        print("\n=== PROGRAM OUTPUT ===")
        print(output_string)
        print("======================\n")

# --- UI REDIRECTION & EXECUTION ---
class RedirectText(object):
    """Redirects print() statements to the Tkinter text box."""
    def __init__(self, text_ctrl):
        self.output = text_ctrl
    def write(self, string):
        self.output.insert(tk.END, string)
        self.output.see(tk.END)
    def flush(self):
        pass

def execute_code():
    """Runs the real compiler and awards coins based on success."""
    global symbol_table, lgf_coins
    symbol_table.clear()
    console_output.delete("1.0", tk.END)
    
    code = code_input.get("1.0", tk.END).strip()
    if not code:
        console_output.insert(tk.END, "Bro, the editor is empty. Type something.\n")
        return

    # Run the actual compiler line by line
    lines = [line.strip() for line in code.split('\n') if line.strip()]
    for line in lines:
        lgf_compiler(line)
    
    # Check if the compiler threw any errors
    output_text = console_output.get("1.0", tk.END)
    if "FATAL ERROR" in output_text:
        console_output.insert(tk.END, "\n💀 [SYSTEM] Compilation failed. 0 Coins awarded. Fix your code.\n")
    else:
        reward = len(lines) * 20 # 20 coins per successful line
        lgf_coins += reward
        console_output.insert(tk.END, f"\n✨ [SYSTEM] Flawless Execution! +{reward} LGF Coins added to vault.\n")
        update_coin_labels()

def pull_gacha():
    """Spends coins and adds the item directly to the Inventory Listbox."""
    global lgf_coins, inventory
    
    loot_pool = ["Cyberpunk Neon Syntax", "Hacker Terminal Font", "Abyssal Void Dark Mode", "OLED Pure Black"]
    
    if lgf_coins >= 100:
        lgf_coins -= 100
        won_item = random.choice(loot_pool)
        
        # Prevent duplicates
        if won_item not in inventory: 
            inventory.append(won_item)
            inventory_listbox.insert(tk.END, won_item)
            
        gacha_result.config(text=f"🎉 YOU UNLOCKED: [{won_item}]! 🎉", fg="#4af626")
    else:
        gacha_result.config(text="❌ Bro, you are broke. Go write some flawless code.", fg="#ff4c4c")
    
    update_coin_labels()

def equip_item():
    """Takes the selected item from the listbox and 'equips' it."""
    global equipped_theme
    
    # Get the index of the clicked item
    selection = inventory_listbox.curselection()
    
    if selection:
        item = inventory_listbox.get(selection[0])
        equipped_theme = item
        lbl_equipped.config(text=f"Equipped: [{equipped_theme}]")
        gacha_result.config(text=f"✨ Equipped {equipped_theme} successfully!", fg="#007acc")
    else:
        gacha_result.config(text="⚠️ Select an item from your vault first.", fg="#ff4c4c")

# --- THE ROUTER ---
def show_frame(frame_to_show):
    menu_frame.pack_forget()
    coding_frame.pack_forget()
    gacha_frame.pack_forget()
    cheat_frame.pack_forget()
    frame_to_show.pack(fill=tk.BOTH, expand=True)

def update_coin_labels():
    lbl_menu_coins.config(text=f"🪙 Vault: {lgf_coins}")
    lbl_gacha_coins.config(text=f"🪙 Vault: {lgf_coins}")

# --- GUI SETUP ---
root = tk.Tk()
root.geometry("850x650")
root.title("LGF Client")
root.configure(bg="#13111C") # Sleeker dark mode

menu_frame = tk.Frame(root, bg="#13111C")
coding_frame = tk.Frame(root, bg="#13111C")
gacha_frame = tk.Frame(root, bg="#13111C")
cheat_frame = tk.Frame(root, bg="#13111C")

# ==========================================
# SCREEN 1: MAIN MENU
# ==========================================
tk.Label(menu_frame, text="LGF COMPILER", font=("Consolas", 36, "bold"), bg="#13111C", fg="white").pack(pady=(120, 10))
tk.Label(menu_frame, text="Developer Edition", font=("Consolas", 14, "italic"), bg="#13111C", fg="#8a2be2").pack(pady=(0, 30))

lbl_menu_coins = tk.Label(menu_frame, text=f"🪙 Vault: {lgf_coins}", font=("Consolas", 16, "bold"), bg="#13111C", fg="#ffd700")
lbl_menu_coins.pack(pady=10)

tk.Button(menu_frame, text="PLAY", font=("Consolas", 14, "bold"), bg="#007acc", fg="white", width=25, command=lambda: show_frame(coding_frame)).pack(pady=10)
tk.Button(menu_frame, text="PULL", font=("Consolas", 14, "bold"), bg="#8a2be2", fg="white", width=25, command=lambda: show_frame(gacha_frame)).pack(pady=10)
tk.Button(menu_frame, text="CODEX", font=("Consolas", 14, "bold"), bg="#2d2d2d", fg="white", width=25, command=lambda: show_frame(cheat_frame)).pack(pady=10)

# ==========================================
# SCREEN 2: CODING ARENA
# ==========================================
tk.Button(coding_frame, text="⬅ MAIN MENU", font=("Consolas", 10), bg="#2d2d2d", fg="white", command=lambda: show_frame(menu_frame)).pack(anchor="nw", padx=10, pady=10)

tk.Label(coding_frame, text="MISSION: Declare an OUNT variable perfectly.", font=("Consolas", 12, "bold"), bg="#13111C", fg="#4af626").pack(pady=5)

code_input = tk.Text(coding_frame, height=8, bg="#1e1e1e", fg="#ce9178", font=("Consolas", 12), insertbackground="white")
code_input.pack(fill=tk.X, padx=20)

tk.Button(coding_frame, text="COMPILE & EXECUTE", font=("Consolas", 12, "bold"), bg="#007acc", fg="white", command=execute_code).pack(pady=10)

console_output = scrolledtext.ScrolledText(coding_frame, height=12, bg="#000000", fg="#4af626", font=("Consolas", 10))
console_output.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
sys.stdout = RedirectText(console_output) # Route prints to terminal

# ==========================================
# SCREEN 3: GACHA PULL (THE MARKETPLACE)
# ==========================================
pull_left = tk.Frame(gacha_frame, bg="#13111C")
pull_left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

inv_right = tk.Frame(gacha_frame, bg="#1E1E1E", width=300)
inv_right.pack(side=tk.RIGHT, fill=tk.Y)

# --- LEFT SIDE (The Store) ---
tk.Button(pull_left, text="⬅ MAIN MENU", font=("Consolas", 10), bg="#2d2d2d", fg="white", command=lambda: show_frame(menu_frame)).pack(anchor="nw", padx=10, pady=10)

tk.Label(pull_left, text="THE MARKETPLACE", font=("Consolas", 28, "bold"), bg="#13111C", fg="#8a2be2").pack(pady=20)

lbl_gacha_coins = tk.Label(pull_left, text=f"🪙 Vault: {lgf_coins}", font=("Consolas", 16, "bold"), bg="#13111C", fg="#ffd700")
lbl_gacha_coins.pack(pady=10)

tk.Button(pull_left, text="PULL SKIN (100 COINS)", font=("Consolas", 16, "bold"), bg="#8a2be2", fg="white", command=pull_gacha).pack(pady=20)

gacha_result = tk.Label(pull_left, text="Awaiting transaction...", font=("Consolas", 14), bg="#13111C", fg="white")
gacha_result.pack(pady=20)

# --- RIGHT SIDE (The Vault) ---
tk.Label(inv_right, text="YOUR VAULT", font=("Consolas", 18, "bold"), bg="#1E1E1E", fg="white").pack(pady=(20, 5))

lbl_equipped = tk.Label(inv_right, text=f"Equipped: [{equipped_theme}]", font=("Consolas", 10, "italic"), bg="#1E1E1E", fg="#4af626", wraplength=250)
lbl_equipped.pack(pady=(0, 15))

# Clickable listbox
inventory_listbox = tk.Listbox(inv_right, bg="#13111C", fg="white", font=("Consolas", 12), selectbackground="#8a2be2", selectforeground="white", bd=0, highlightthickness=1, highlightcolor="#8a2be2")
inventory_listbox.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 15))

tk.Button(inv_right, text="EQUIP SELECTED", font=("Consolas", 12, "bold"), bg="#007acc", fg="white", command=equip_item).pack(fill=tk.X, padx=20, pady=(0, 20))

# ==========================================
# SCREEN 4: CHEAT SHEET
# ==========================================
tk.Button(cheat_frame, text="⬅ MAIN MENU", font=("Consolas", 10), bg="#2d2d2d", fg="white", command=lambda: show_frame(menu_frame)).pack(anchor="nw", padx=10, pady=10)

tk.Label(cheat_frame, text="LGF CODEX", font=("Consolas", 28, "bold"), bg="#13111C", fg="#007acc").pack(pady=20)

codex_text = """OUNT    : Integer (e.g. OUNT age IS 21 :>)
YEARN   : String (e.g. YEARN name IS "Renzo" :>)
RELEASE : Print Command (e.g. RELEASE name, EndThat :>)
:>      : Delimiter (Ends all assignments)"""

tk.Label(cheat_frame, text=codex_text, font=("Consolas", 14), bg="#13111C", fg="white", justify="left").pack(pady=20)

# --- START ---
show_frame(menu_frame)
root.mainloop()