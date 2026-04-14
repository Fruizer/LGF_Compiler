import tkinter as tk
from tkinter import scrolledtext
import sys
import random

# --- GAME STATE & QUEST ENGINE ---
lgf_coins = 0
symbol_table = {}
inventory = []
equipped_theme = "Default Theme"

quests_completed = 0
current_difficulty = "EASY"

quest_db = {
    "EASY": [
        {"task": "MISSION: Declare an OUNT (Integer).", "target": "OUNT", "reward": 50},
        {"task": "MISSION: Declare a YEARN (String).", "target": "YEARN", "reward": 50},
        {"task": "MISSION: Declare a TAMARAW (Bool).", "target": "TAMARAW", "reward": 50}
    ],
    "MEDIUM": [
        {"task": "MISSION: Print data using RELEASE.", "target": "RELEASE", "reward": 100},
        {"task": "MISSION: Declare a HERO (Char).", "target": "HERO", "reward": 100}
    ],
    "HARD": [
        {"task": "MISSION: Declare an OUNT, then RELEASE it.", "target": "COMBO_OUNT_RELEASE", "reward": 250}
    ]
}

def generate_quest():
    """Pulls a random quest based on the current difficulty tier."""
    global current_difficulty
    
    if quests_completed >= 5:
        current_difficulty = "HARD"
    elif quests_completed >= 2:
        current_difficulty = "MEDIUM"
        
    pool = quest_db[current_difficulty]
    return random.choice(pool)

active_quest = generate_quest()

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
    def __init__(self, text_ctrl):
        self.output = text_ctrl
    def write(self, string):
        self.output.insert(tk.END, string)
        self.output.see(tk.END)
    def flush(self):
        pass

def execute_code():
    """Runs the compiler, verifies quest completion, and handles UI locking."""
    global symbol_table, lgf_coins, active_quest, quests_completed
    symbol_table.clear()
    console_output.delete("1.0", tk.END)
    
    code = code_input.get("1.0", tk.END).strip()
    if not code:
        console_output.insert(tk.END, "[SYSTEM] The editor is empty. Type something.\n")
        return

    lines = [line.strip() for line in code.split('\n') if line.strip()]
    for line in lines:
        lgf_compiler(line)
    
    output_text = console_output.get("1.0", tk.END)
    if "FATAL ERROR" in output_text:
        console_output.insert(tk.END, "\n[SYSTEM] Compilation failed. 0 Coins awarded. Fix your code.\n")
        return

    # --- QUEST VERIFICATION ---
    quest_passed = False
    
    if active_quest["target"] in ["OUNT", "YEARN", "TAMARAW", "HERO"]:
        for var_name, data in symbol_table.items():
            if data["type"] == active_quest["target"]:
                quest_passed = True
                
    elif active_quest["target"] == "RELEASE":
        if "RELEASE" in code:
            quest_passed = True
            
    elif active_quest["target"] == "COMBO_OUNT_RELEASE":
        has_ount = any(data["type"] == "OUNT" for data in symbol_table.values())
        if has_ount and "RELEASE" in code:
            quest_passed = True

    # --- REWARD SYSTEM & UI LOCKING ---
    if quest_passed:
        reward = active_quest["reward"]
        lgf_coins += reward
        quests_completed += 1
        
        console_output.insert(tk.END, f"\n[QUEST COMPLETE] Target acquired! +{reward} Coins.\n")
        update_coin_labels()
        
        # Lock the execute button and show the Next button
        btn_execute.config(state=tk.DISABLED)
        btn_next.pack(side=tk.LEFT, padx=10)
    else:
        console_output.insert(tk.END, "\n[SYSTEM] Code works, but you ignored the mission target. 0 Coins.\n")

def next_quest():
    """Wipes the arena and loads the next mission."""
    global active_quest
    
    # Generate new target and update the big UI label
    active_quest = generate_quest()
    lbl_quest.config(text=active_quest["task"]) 
    
    # Wipe the code and console clean
    code_input.delete("1.0", tk.END)
    console_output.delete("1.0", tk.END)
    
    # Hide the Next button and unlock the Execute button
    btn_next.pack_forget()
    btn_execute.config(state=tk.NORMAL)

def pull_gacha():
    global lgf_coins, inventory
    
    loot_pool = ["Cyberpunk Neon Syntax", "Hacker Terminal Font", "Abyssal Void Dark Mode", "OLED Pure Black"]
    
    if lgf_coins >= 100:
        lgf_coins -= 100
        won_item = random.choice(loot_pool)
        
        if won_item not in inventory: 
            inventory.append(won_item)
            inventory_listbox.insert(tk.END, won_item)
            
        gacha_result.config(text=f"[SUCCESS] YOU UNLOCKED: [{won_item}]", fg="#4af626")
    else:
        gacha_result.config(text="[ERROR] Insufficient funds. Complete more quests.", fg="#ff4c4c")
    
    update_coin_labels()

def equip_item():
    global equipped_theme
    
    selection = inventory_listbox.curselection()
    
    if selection:
        item = inventory_listbox.get(selection[0])
        equipped_theme = item
        lbl_equipped.config(text=f"Equipped: [{equipped_theme}]")
        gacha_result.config(text=f"[SYSTEM] Equipped {equipped_theme} successfully.", fg="#007acc")
    else:
        gacha_result.config(text="[WARNING] Select an item from your vault first.", fg="#ff4c4c")

# --- THE ROUTER ---
def show_frame(frame_to_show):
    menu_frame.pack_forget()
    coding_frame.pack_forget()
    gacha_frame.pack_forget()
    cheat_frame.pack_forget()
    frame_to_show.pack(fill=tk.BOTH, expand=True)

def update_coin_labels():
    lbl_menu_coins.config(text=f"[VAULT]: {lgf_coins} Coins")
    lbl_gacha_coins.config(text=f"[VAULT]: {lgf_coins} Coins")

# --- GUI SETUP ---
root = tk.Tk()
root.geometry("1280x720")

root.title("LGF Client")
root.configure(bg="#13111C")

menu_frame = tk.Frame(root, bg="#13111C")
coding_frame = tk.Frame(root, bg="#13111C")
gacha_frame = tk.Frame(root, bg="#13111C")
cheat_frame = tk.Frame(root, bg="#13111C")

# ==========================================
# SCREEN 1: MAIN MENU
# ==========================================
tk.Label(menu_frame, text="LGF COMPILER", font=("Consolas", 36, "bold"), bg="#13111C", fg="white").pack(pady=(120, 10))
tk.Label(menu_frame, text="Developer Edition", font=("Consolas", 14, "italic"), bg="#13111C", fg="#8a2be2").pack(pady=(0, 30))

lbl_menu_coins = tk.Label(menu_frame, text=f"[VAULT]: {lgf_coins} Coins", font=("Consolas", 16, "bold"), bg="#13111C", fg="#ffd700")
lbl_menu_coins.pack(pady=10)

tk.Button(menu_frame, text="ENTER ARENA", font=("Consolas", 14, "bold"), bg="#007acc", fg="white", width=25, command=lambda: show_frame(coding_frame)).pack(pady=10)
tk.Button(menu_frame, text="THE MARKETPLACE", font=("Consolas", 14, "bold"), bg="#8a2be2", fg="white", width=25, command=lambda: show_frame(gacha_frame)).pack(pady=10)
tk.Button(menu_frame, text="ACCESS CODEX", font=("Consolas", 14, "bold"), bg="#2d2d2d", fg="white", width=25, command=lambda: show_frame(cheat_frame)).pack(pady=10)

# ==========================================
# SCREEN 2: CODING ARENA
# ==========================================
tk.Button(coding_frame, text="RETURN TO MENU", font=("Consolas", 10), bg="#2d2d2d", fg="white", command=lambda: show_frame(menu_frame)).pack(anchor="nw", padx=10, pady=10)

# The Massive Mission Box
mission_frame = tk.Frame(coding_frame, bg="#1E1E1E", bd=1, relief="solid", highlightbackground="#4af626", highlightthickness=2)
mission_frame.pack(fill=tk.X, padx=20, pady=(10, 20))

lbl_quest = tk.Label(mission_frame, text=active_quest["task"], font=("Consolas", 18, "bold"), bg="#1E1E1E", fg="#4af626", pady=15)
lbl_quest.pack()

# The Code Editor
code_input = tk.Text(coding_frame, height=8, bg="#1e1e1e", fg="#ce9178", font=("Consolas", 12), insertbackground="white")
code_input.pack(fill=tk.X, padx=20)

# The Action Buttons Frame
btn_action_frame = tk.Frame(coding_frame, bg="#13111C")
btn_action_frame.pack(pady=15)

btn_execute = tk.Button(btn_action_frame, text="COMPILE & EXECUTE", font=("Consolas", 12, "bold"), bg="#007acc", fg="white", command=execute_code)
btn_execute.pack(side=tk.LEFT, padx=10)

# The Next button is created but kept hidden initially
btn_next = tk.Button(btn_action_frame, text="NEXT MISSION", font=("Consolas", 12, "bold"), bg="#8a2be2", fg="white", command=next_quest)

# --- THE MODERN CONSOLE PANEL ---
console_container = tk.Frame(coding_frame, bg="#0a0a0a", bd=0, highlightbackground="#333333", highlightthickness=1)
console_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))

console_header = tk.Label(console_container, text="[ SYSTEM TERMINAL ]", font=("Consolas", 10, "bold"), bg="#1e1e1e", fg="#888888", anchor="w", padx=10, pady=4)
console_header.pack(fill=tk.X)

console_output = scrolledtext.ScrolledText(console_container, height=12, bg="#0a0a0a", fg="#4af626", font=("Consolas", 10), bd=0, highlightthickness=0, padx=10, pady=10)
console_output.pack(fill=tk.BOTH, expand=True)

sys.stdout = RedirectText(console_output)

# ==========================================
# SCREEN 3: GACHA PULL (THE MARKETPLACE)
# ==========================================
pull_left = tk.Frame(gacha_frame, bg="#13111C")
pull_left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

inv_right = tk.Frame(gacha_frame, bg="#1E1E1E", width=300)
inv_right.pack(side=tk.RIGHT, fill=tk.Y)

# --- LEFT SIDE ---
tk.Button(pull_left, text="RETURN TO MENU", font=("Consolas", 10), bg="#2d2d2d", fg="white", command=lambda: show_frame(menu_frame)).pack(anchor="nw", padx=10, pady=10)

tk.Label(pull_left, text="THE MARKETPLACE", font=("Consolas", 28, "bold"), bg="#13111C", fg="#8a2be2").pack(pady=20)

lbl_gacha_coins = tk.Label(pull_left, text=f"[VAULT]: {lgf_coins} Coins", font=("Consolas", 16, "bold"), bg="#13111C", fg="#ffd700")
lbl_gacha_coins.pack(pady=10)

tk.Button(pull_left, text="PULL SKIN (100 COINS)", font=("Consolas", 16, "bold"), bg="#8a2be2", fg="white", command=pull_gacha).pack(pady=20)

gacha_result = tk.Label(pull_left, text="Awaiting transaction...", font=("Consolas", 14), bg="#13111C", fg="white")
gacha_result.pack(pady=20)

# --- RIGHT SIDE ---
tk.Label(inv_right, text="YOUR VAULT", font=("Consolas", 18, "bold"), bg="#1E1E1E", fg="white").pack(pady=(20, 5))

lbl_equipped = tk.Label(inv_right, text=f"Equipped: [{equipped_theme}]", font=("Consolas", 10, "italic"), bg="#1E1E1E", fg="#4af626", wraplength=250)
lbl_equipped.pack(pady=(0, 15))

inventory_listbox = tk.Listbox(inv_right, bg="#13111C", fg="white", font=("Consolas", 12), selectbackground="#8a2be2", selectforeground="white", bd=0, highlightthickness=1, highlightcolor="#8a2be2")
inventory_listbox.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 15))

tk.Button(inv_right, text="EQUIP SELECTED", font=("Consolas", 12, "bold"), bg="#007acc", fg="white", command=equip_item).pack(fill=tk.X, padx=20, pady=(0, 20))

# ==========================================
# SCREEN 4: CHEAT SHEET (THE CODEX)
# ==========================================
tk.Button(cheat_frame, text="RETURN TO MENU", font=("Consolas", 10), bg="#2d2d2d", fg="white", command=lambda: show_frame(menu_frame)).pack(anchor="nw", padx=10, pady=10)

tk.Label(cheat_frame, text="LGF CODEX", font=("Consolas", 28, "bold"), bg="#13111C", fg="#007acc").pack(pady=10)

codex_container = tk.Frame(cheat_frame, bg="#13111C")
codex_container.pack(fill=tk.BOTH, expand=True, padx=40, pady=20)

# --- CARD 1: Data Types ---
type_card = tk.Frame(codex_container, bg="#1E1E1E", bd=1, relief="solid", highlightbackground="#8a2be2", highlightthickness=2)
type_card.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)

tk.Label(type_card, text="PRIMITIVE TYPES", font=("Consolas", 16, "bold"), bg="#1E1E1E", fg="#8a2be2").pack(pady=(20, 10))

types_text = """OUNT    : Integer (Numeric values only)
YEARN   : String (Requires "Double Quotes")
HERO    : Character (Requires 'Single Quotes')
TAMARAW : Boolean (Must be True or False)

*WARNING: The Lexer is case-sensitive and
enforces strict quotation marks."""

tk.Label(type_card, text=types_text, font=("Consolas", 12), bg="#1E1E1E", fg="white", justify="left").pack(anchor="w", padx=20, pady=10)

# --- CARD 2: Syntax & Commands ---
syntax_card = tk.Frame(codex_container, bg="#1E1E1E", bd=1, relief="solid", highlightbackground="#007acc", highlightthickness=2)
syntax_card.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10)

tk.Label(syntax_card, text="CORE SYNTAX", font=("Consolas", 16, "bold"), bg="#1E1E1E", fg="#007acc").pack(pady=(20, 10))

syntax_text = """DECLARATION RULE:
[Type] [Name] IS [Value] :>
Ex: OUNT age IS 21 :>

OUTPUT COMMAND:
RELEASE [Variable], EndThat :>
Ex: RELEASE age, EndThat :>"""
tk.Label(syntax_card, text=syntax_text, font=("Consolas", 14), bg="#1E1E1E", fg="white", justify="left").pack(anchor="w", padx=30, pady=10)

# --- START ---
show_frame(menu_frame)
root.mainloop()