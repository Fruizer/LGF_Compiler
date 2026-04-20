import tkinter as tk
from tkinter import scrolledtext
import sys
import random
import json
import os

# --- AUDIO ENGINE (PYGAME) ---
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame

pygame.mixer.init()
sounds = {}

def load_sounds():
    try:
        sounds['click'] = pygame.mixer.Sound("click.mp3")
        sounds['right'] = pygame.mixer.Sound("rightAnswer.mp3")
        sounds['wrong'] = pygame.mixer.Sound("wrongAnswer.mp3")
        sounds['spin'] = pygame.mixer.Sound("spin.mp3")
        sounds['gacha'] = pygame.mixer.Sound("gachagot.mp3")
    except Exception as e:
        print(f"[SYSTEM] Audio files missing or failed to load: {e}")

load_sounds()

def play_sound(name, loop=0):
    """Plays a sound and returns the channel so it can be stopped if needed."""
    if name in sounds:
        try:
            return sounds[name].play(loops=loop)
        except:
            pass
    return None

active_spin_channel = None # Used to track the looping spin sound

# --- GAME STATE & QUEST ENGINE ---
lgf_coins = 0
symbol_table = {}
inventory = ["Default Theme"] 
equipped_theme = "Default Theme"

quests_completed = 0
current_difficulty = "EASY"
is_pulling = False 

# THE ULTIMATE BUILT-IN RETRO FONT
RETRO_FONT = "Fixedsys"

# --- THE SAVE SYSTEM ---
SAVE_FILE = "lgf_save_data.json"

def load_progress():
    global lgf_coins, inventory, equipped_theme, quests_completed
    if os.path.exists(SAVE_FILE):
        try:
            with open(SAVE_FILE, "r") as f:
                data = json.load(f)
                lgf_coins = data.get("coins", 0)
                inventory = data.get("inventory", ["Default Theme"])
                equipped_theme = data.get("equipped_theme", "Default Theme")
                quests_completed = data.get("quests_completed", 0)
        except Exception as e:
            print(f"Error loading save data: {e}")

def save_progress():
    data = {
        "coins": lgf_coins,
        "inventory": inventory,
        "equipped_theme": equipped_theme,
        "quests_completed": quests_completed
    }
    with open(SAVE_FILE, "w") as f:
        json.dump(data, f)

load_progress()

# --- THE PREMIUM RETRO THEME ENGINE ---
themes = {
    "Default Theme": {"bg": "#13111C", "panel": "#1E1E1E", "accent": "#007acc", "hover": "#0099ff", "text": "white", "success": "#4af626", "btn_fg": "white"},
    "Cyberpunk Neon Syntax": {"bg": "#0d0221", "panel": "#261447", "accent": "#f706d2", "hover": "#ff33e0", "text": "#0ff0fc", "success": "#00ff00", "btn_fg": "white"},
    "Hacker Terminal Font": {"bg": "#000000", "panel": "#0a0a0a", "accent": "#00ff00", "hover": "#33ff33", "text": "#00ff00", "success": "#00ff00", "btn_fg": "black"},
    "Abyssal Void Dark Mode": {"bg": "#050505", "panel": "#0f0f0f", "accent": "#8a0303", "hover": "#b30000", "text": "#d3d3d3", "success": "#ff3333", "btn_fg": "white"},
    "OLED Pure Black": {"bg": "#000000", "panel": "#0a0a0a", "accent": "#ffffff", "hover": "#cccccc", "text": "#ffffff", "success": "#aaaaaa", "btn_fg": "black"},
    "Solar Flare Light Mode": {"bg": "#fdf6e3", "panel": "#eee8d5", "accent": "#b58900", "hover": "#d9a400", "text": "#073642", "success": "#859900", "btn_fg": "white"},
    "Ocean Trench Deep Blue": {"bg": "#001b2e", "panel": "#002a4a", "accent": "#00a8cc", "hover": "#00c2eb", "text": "#e0fbfc", "success": "#00f5d4", "btn_fg": "black"},
    "Crimson Bloodline": {"bg": "#1a0000", "panel": "#330000", "accent": "#ff0000", "hover": "#ff3333", "text": "#ffcccc", "success": "#ff4d4d", "btn_fg": "white"},
    "Synthwave Sunset": {"bg": "#2b0f4c", "panel": "#3d1466", "accent": "#ff9e00", "hover": "#ffb733", "text": "#f706d2", "success": "#ff007f", "btn_fg": "black"},
    "Matrix Glitch": {"bg": "#001100", "panel": "#002200", "accent": "#33ff33", "hover": "#66ff66", "text": "#ccffcc", "success": "#66ff66", "btn_fg": "black"},
    
    "GAMEBOY CLASSIC": {"bg": "#8bac0f", "panel": "#9bbc0f", "accent": "#0f380f", "hover": "#306230", "text": "#0f380f", "success": "#0f380f", "btn_fg": "white"},
    "RADIANT PROTOCOL": {"bg": "#0f1923", "panel": "#1b2733", "accent": "#ff4655", "hover": "#ff7b87", "text": "#ece8e1", "success": "#00ffcc", "btn_fg": "white"},
    "GILBERTO GREEN": {"bg": "#0a1a0f", "panel": "#112b18", "accent": "#4caf50", "hover": "#66ffa6", "text": "#e8f5e9", "success": "#81c784", "btn_fg": "black"},
    
    "THE GOLDEN COMPILER": {"bg": "#0B0800", "panel": "#1C1400", "accent": "#FFD700", "hover": "#ffe033", "text": "#FFF2B2", "success": "#FFB300", "btn_fg": "black"},
    "FEU TAMARAWS": {"bg": "#014421", "panel": "#012b15", "accent": "#F2A900", "hover": "#ffbb33", "text": "#ffffff", "success": "#FFD700", "btn_fg": "black"},
    "FEU TECH ACM": {"bg": "#0a050f", "panel": "#140a1f", "accent": "#9d4edd", "hover": "#b366ff", "text": "#e0caff", "success": "#c77dff", "btn_fg": "white"}
}

quest_db = {
    "EASY": [
        {"task": "MISSION: Declare an OUNT (Integer).", "target": "OUNT", "reward": 50},
        {"task": "MISSION: Declare a YEARN (String).", "target": "YEARN", "reward": 50},
        {"task": "MISSION: Declare a TAMARAW (Bool).", "target": "TAMARAW", "reward": 50},
        {"task": "MISSION: Declare a HERO (Char).", "target": "HERO", "reward": 50},
        {"task": "MISSION: Declare an OUNT equal to 0.", "target": "OUNT_ZERO", "reward": 50},
        {"task": "MISSION: Declare a TAMARAW as True.", "target": "TAMARAW_TRUE", "reward": 50}
    ],
    "MEDIUM": [
        {"task": "MISSION: Print data using RELEASE.", "target": "RELEASE", "reward": 100},
        {"task": "MISSION: Declare TWO different OUNT variables.", "target": "TWO_OUNT", "reward": 100},
        {"task": "MISSION: Declare TWO different YEARN variables.", "target": "TWO_YEARN", "reward": 100},
        {"task": "MISSION: Add two numbers.", "target": "MATH_ADD", "reward": 150},
        {"task": "MISSION: Subtract two numbers.", "target": "MATH_SUB", "reward": 150},
        {"task": "MISSION: Multiply two numbers.", "target": "MATH_MUL", "reward": 150}
    ],
    "HARD": [
        {"task": "MISSION: Declare an OUNT, then RELEASE it.", "target": "COMBO_OUNT_RELEASE", "reward": 250},
        {"task": "MISSION: Declare a YEARN, then RELEASE it.", "target": "COMBO_YEARN_RELEASE", "reward": 250},
        {"task": "MISSION: Declare a TAMARAW and an OUNT.", "target": "COMBO_TAMARAW_OUNT", "reward": 250},
        {"task": "MISSION: Declare TWO different HERO variables.", "target": "TWO_HERO", "reward": 250}
    ],
    "EXTREME": [
        {"task": "MISSION: Multiply two numbers and RELEASE the result.", "target": "MATH_COMBO_MUL", "reward": 500},
        {"task": "MISSION: Subtract two numbers and RELEASE the result.", "target": "MATH_COMBO_SUB", "reward": 500},
        {"task": "MISSION: Declare an OUNT, YEARN, and TAMARAW in one run.", "target": "TRI_COMBO", "reward": 800}
    ]
}

def generate_quest():
    global current_difficulty
    if quests_completed < 3:
        current_difficulty = "EASY"
    elif quests_completed < 8:
        current_difficulty = random.choices(["EASY", "MEDIUM"], weights=[30, 70], k=1)[0]
    elif quests_completed < 12:
        current_difficulty = random.choices(["MEDIUM", "HARD"], weights=[40, 60], k=1)[0]
    else:
        current_difficulty = random.choices(["HARD", "EXTREME"], weights=[40, 60], k=1)[0]
        
    pool = quest_db[current_difficulty]
    return random.choice(pool)

active_quest = generate_quest()

# --- THE VERBOSE COMPILER ENGINE ---
def lgf_compiler(source_code):
    print(f"Input Code: {source_code}\n")
    cleaned_code = source_code.replace(":>", " :> ").replace(",", " , ")
    cleaned_code = cleaned_code.replace("+", " + ").replace("-", " - ").replace("*", " * ").replace("/", " / ")
    words = cleaned_code.split()
    if not words: return

    print("--- STARTING LEXICAL ANALYSIS ---")
    tokens = []
    for word in words:
        if word in ["OUNT", "HERO", "TAMARAW", "YEARN"]: 
            tokens.append(("DATATYPE", word))
            print(f"[LEXER] Found '{word}' -> Identified as DATATYPE")
        elif word == "IS": 
            tokens.append(("ASSIGN", word))
            print(f"[LEXER] Found '{word}' -> Identified as ASSIGN OPERATOR")
        elif word == ":>": 
            tokens.append(("DELIMITER", word))
            print(f"[LEXER] Found '{word}' -> Identified as DELIMITER")
        elif word == "RELEASE": 
            tokens.append(("OUTPUT_CMD", word))
            print(f"[LEXER] Found '{word}' -> Identified as OUTPUT_CMD")
        elif word == "EndThat": 
            tokens.append(("NEWLINE", word))
            print(f"[LEXER] Found '{word}' -> Identified as NEWLINE")
        elif word == ",": 
            tokens.append(("COMMA", word))
            print(f"[LEXER] Found '{word}' -> Identified as COMMA")
        elif word in ["+", "-", "*", "/"]: 
            tokens.append(("MATH_OP", word))
            print(f"[LEXER] Found '{word}' -> Identified as MATH_OP")
        elif word.isdigit(): 
            tokens.append(("LITERAL_INT", word))
            print(f"[LEXER] Found '{word}' -> Identified as LITERAL_INT")
        elif word.startswith('"') and word.endswith('"'): 
            tokens.append(("LITERAL_STRING", word))
            print(f"[LEXER] Found '{word}' -> Identified as LITERAL_STRING")
        elif word.startswith("'") and word.endswith("'") and len(word) == 3: 
            tokens.append(("LITERAL_CHAR", word))
            print(f"[LEXER] Found '{word}' -> Identified as LITERAL_CHAR")
        elif word in ["True", "False"]: 
            tokens.append(("LITERAL_BOOL", word))
            print(f"[LEXER] Found '{word}' -> Identified as LITERAL_BOOL")
        else: 
            tokens.append(("IDENTIFIER", word))
            print(f"[LEXER] Found '{word}' -> Identified as IDENTIFIER")
    print("Lexical Analysis Complete.\n")

    print("--- STARTING SYNTAX ANALYSIS ---")
    print("[PARSER] Checking statement structure...")
    is_assignment = False
    is_math_assignment = False
    is_release = False

    if tokens[0][0] == "DATATYPE":
        if len(tokens) == 5 and (tokens[1][0] == "IDENTIFIER" and tokens[2][0] == "ASSIGN" and tokens[3][0].startswith("LITERAL") and tokens[4][0] == "DELIMITER"):
            is_assignment = True
            print("[PARSER] Expected rule: [DATATYPE] [IDENTIFIER] [ASSIGN] [LITERAL] [DELIMITER]")
            print("[PARSER] Actual structure matches expected rule perfectly.")
            print("Syntax Analysis Complete. No structural errors.\n")
        elif len(tokens) == 7 and (tokens[1][0] == "IDENTIFIER" and tokens[2][0] == "ASSIGN" and tokens[4][0] == "MATH_OP" and tokens[6][0] == "DELIMITER"):
            is_math_assignment = True
            print("[PARSER] Expected rule: [DATATYPE] [IDENTIFIER] [ASSIGN] [LITERAL] [MATH_OP] [LITERAL] [DELIMITER]")
            print("[PARSER] Actual structure matches expected rule perfectly.")
            print("Syntax Analysis Complete. No structural errors.\n")
        else:
            print("[PARSER] FATAL ERROR: Syntax invalid. Structure does not match known rules.")
            return
    elif tokens[0][0] == "OUTPUT_CMD":
        is_release = True
        if tokens[-1][0] != "DELIMITER":
            print("[PARSER] FATAL ERROR: Missing delimiter ':>'.")
            return
        print("[PARSER] Expected rule: RELEASE [Identifier/Literal], EndThat :> (or similar)")
        print("[PARSER] Structure accepted for RELEASE command.")
        print("Syntax Analysis Complete. No structural errors.\n")
    else:
        print("[PARSER] FATAL ERROR: Unknown statement structure.")
        return

    print("--- STARTING SEMANTIC ANALYSIS ---")
    if is_assignment:
        print("[SEMANTICS] Checking Type Compatibility...")
        var_type, var_name, var_value, literal_type = tokens[0][1], tokens[1][1], tokens[3][1], tokens[3][0]
        print(f"[SEMANTICS] Variable '{var_name}' is declared as '{var_type}'. Value is '{var_value}'.")
        
        is_valid_type = (var_type == "OUNT" and literal_type == "LITERAL_INT") or \
                        (var_type == "YEARN" and literal_type == "LITERAL_STRING") or \
                        (var_type == "HERO" and literal_type == "LITERAL_CHAR") or \
                        (var_type == "TAMARAW" and literal_type == "LITERAL_BOOL")

        if is_valid_type:
            print("[SEMANTICS] Types match. No coercion needed.")
            symbol_table[var_name] = {"type": var_type, "value": var_value}
            print(f"[SEMANTICS] Binding variable '{var_name}' to Symbol Table.")
            print("Semantic Analysis Complete.\n")
        else:
            print(f"[SEMANTICS] FATAL ERROR: Type mismatch. Cannot coerce {literal_type} into {var_type}.")
            
    elif is_math_assignment:
        print("[SEMANTICS] Checking Operation Validity...")
        var_type, var_name = tokens[0][1], tokens[1][1]
        val1, operator, val2 = tokens[3][1], tokens[4][1], tokens[5][1]
        print(f"[SEMANTICS] Variable '{var_name}' declared as '{var_type}'. Operation: {val1} {operator} {val2}")
        
        if var_type != "OUNT":
            print("[SEMANTICS] FATAL ERROR: Math operations are only allowed for OUNT types.")
            return
        try:
            if operator == "+": result = int(val1) + int(val2)
            elif operator == "-": result = int(val1) - int(val2)
            elif operator == "*": result = int(val1) * int(val2)
            elif operator == "/": result = int(val1) // int(val2)
            
            print("[SEMANTICS] Operation successful.")
            symbol_table[var_name] = {"type": "OUNT", "value": result}
            print(f"[SEMANTICS] Binding variable '{var_name}' (Value: {result}) to Symbol Table.")
            print("Semantic Analysis Complete.\n")
        except Exception:
            print("[SEMANTICS] FATAL ERROR: Invalid math operation.")
            
    elif is_release:
        print("[SEMANTICS] Executing Output Command...")
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
        print("Semantic Analysis Complete.\n")

# --- THE SMOOTH TYPEWRITER ENGINE ---
class RedirectText(object):
    def __init__(self, text_ctrl):
        self.output = text_ctrl
        self.queue = ""
        self.is_typing = False

    def write(self, string):
        self.queue += string
        if not self.is_typing:
            self.type_char()

    def type_char(self):
        if self.queue:
            self.is_typing = True
            chunk_size = 4 
            chunk = self.queue[:chunk_size]
            self.queue = self.queue[chunk_size:]
            
            self.output.insert(tk.END, chunk)
            self.output.see(tk.END)
            self.output.update_idletasks()
            self.output.after(1, self.type_char) 
        else:
            self.is_typing = False
            
    def flush(self): pass

def highlight_syntax(event=None):
    for tag in ["keyword", "string"]:
        code_input.tag_remove(tag, "1.0", tk.END)
        
    t = themes[equipped_theme]
    
    code_input.tag_config("keyword", foreground=t["accent"], font=(RETRO_FONT, 22, "bold"))
    code_input.tag_config("string", foreground=t["success"])
    
    keywords = ["OUNT", "YEARN", "TAMARAW", "HERO", "RELEASE", "EndThat", "IS"]
    
    for word in keywords:
        start = "1.0"
        while True:
            idx = code_input.search(r'\b' + word + r'\b', start, stopindex=tk.END, regexp=True)
            if not idx: break
            end = f"{idx}+{len(word)}c"
            code_input.tag_add("keyword", idx, end)
            start = end
            
    start = "1.0"
    while True:
        count = tk.IntVar()
        idx = code_input.search(r'"[^"]*"', start, stopindex=tk.END, count=count, regexp=True)
        if not idx: break
        end = f"{idx}+{count.get()}c"
        code_input.tag_add("string", idx, end)
        start = end

def execute_code():
    global symbol_table
    symbol_table.clear()
    
    btn_execute.config(state=tk.DISABLED) 
    
    print("\n" + "="*50)
    print("[SYSTEM] INITIATING COMPILER CYCLE...\n")
    
    code = code_input.get("1.0", tk.END).strip()
    if not code:
        print("[SYSTEM] The editor is empty.\n")
        root.after(100, lambda: wait_for_typing(code))
        return

    lines = [line.strip() for line in code.split('\n') if line.strip()]
    for line in lines: lgf_compiler(line)
    
    wait_for_typing(code)

def wait_for_typing(code):
    if getattr(sys.stdout, 'is_typing', False):
        root.after(50, lambda: wait_for_typing(code))
    else:
        check_rewards(code)

def check_rewards(code):
    global lgf_coins, quests_completed
    output_text = console_output.get("1.0", tk.END)
    recent_output = output_text.split("[SYSTEM] INITIATING COMPILER CYCLE...")[-1]
    
    if "FATAL ERROR" in recent_output:
        print("\n[SYSTEM] Compilation failed. 0 Coins awarded.\n")
        play_sound('wrong') # AUDIO CUE
        btn_execute.config(state=tk.NORMAL)
        return

    quest_passed = False
    
    if active_quest["target"] in ["OUNT", "YEARN", "TAMARAW", "HERO"]:
        if any(data["type"] == active_quest["target"] for data in symbol_table.values()): quest_passed = True
    elif active_quest["target"] == "OUNT_ZERO":
        if any(data["type"] == "OUNT" and int(data["value"]) == 0 for data in symbol_table.values()): quest_passed = True
    elif active_quest["target"] == "TAMARAW_TRUE":
        if any(data["type"] == "TAMARAW" and str(data["value"]) == "True" for data in symbol_table.values()): quest_passed = True
    elif active_quest["target"] == "RELEASE":
        if "RELEASE" in code: quest_passed = True
    elif active_quest["target"] == "TWO_OUNT":
        if sum(1 for data in symbol_table.values() if data["type"] == "OUNT") >= 2: quest_passed = True
    elif active_quest["target"] == "TWO_YEARN":
        if sum(1 for data in symbol_table.values() if data["type"] == "YEARN") >= 2: quest_passed = True
    elif active_quest["target"] == "TWO_HERO":
        if sum(1 for data in symbol_table.values() if data["type"] == "HERO") >= 2: quest_passed = True
    elif active_quest["target"] == "COMBO_OUNT_RELEASE":
        if any(data["type"] == "OUNT" for data in symbol_table.values()) and "RELEASE" in code: quest_passed = True
    elif active_quest["target"] == "COMBO_YEARN_RELEASE":
        if any(data["type"] == "YEARN" for data in symbol_table.values()) and "RELEASE" in code: quest_passed = True
    elif active_quest["target"] == "COMBO_TAMARAW_OUNT":
        if any(data["type"] == "TAMARAW" for data in symbol_table.values()) and any(data["type"] == "OUNT" for data in symbol_table.values()): quest_passed = True
    elif active_quest["target"] == "TRI_COMBO":
        if any(d["type"] == "OUNT" for d in symbol_table.values()) and any(d["type"] == "YEARN" for d in symbol_table.values()) and any(d["type"] == "TAMARAW" for d in symbol_table.values()): quest_passed = True
    elif active_quest["target"] == "MATH_ADD":
        if "+" in code and any(data["type"] == "OUNT" for data in symbol_table.values()): quest_passed = True
    elif active_quest["target"] == "MATH_SUB":
        if "-" in code and any(data["type"] == "OUNT" for data in symbol_table.values()): quest_passed = True
    elif active_quest["target"] == "MATH_MUL":
        if "*" in code and any(data["type"] == "OUNT" for data in symbol_table.values()): quest_passed = True
    elif active_quest["target"] == "MATH_COMBO_MUL":
        if "*" in code and "RELEASE" in code: quest_passed = True
    elif active_quest["target"] == "MATH_COMBO_SUB":
        if "-" in code and "RELEASE" in code: quest_passed = True

    if quest_passed:
        reward = active_quest["reward"]
        lgf_coins += reward
        quests_completed += 1
        print(f"\n[QUEST COMPLETE] Target acquired! +{reward} Coins.\n")
        play_sound('right') # AUDIO CUE
        update_coin_labels()
        save_progress() 
        btn_next.pack(side=tk.LEFT, padx=10)
    else:
        print("\n[SYSTEM] Target ignored. 0 Coins.\n")
        play_sound('wrong') # AUDIO CUE
        btn_execute.config(state=tk.NORMAL)

def next_quest():
    global active_quest
    active_quest = generate_quest()
    lbl_quest.config(text=active_quest["task"]) 
    code_input.delete("1.0", tk.END)
    highlight_syntax()
    btn_next.pack_forget()
    btn_execute.config(state=tk.NORMAL)

# --- THE GACHA ANIMATION SYSTEM ---
def pull_gacha():
    global lgf_coins, inventory, is_pulling, active_spin_channel
    if is_pulling: return 
    
    loot_pool = list(themes.keys())
    loot_pool.remove("Default Theme")
    
    rates = {
        "THE GOLDEN COMPILER": 1.0, "FEU TAMARAWS": 1.0, "FEU TECH ACM": 1.0,
        "GILBERTO GREEN": 3.0, "RADIANT PROTOCOL": 3.0
    }
    drop_rates = [rates.get(theme, 9.1) for theme in loot_pool]
    
    if lgf_coins >= 100:
        lgf_coins -= 100
        update_coin_labels()
        save_progress()
        is_pulling = True
        btn_pull.config(state=tk.DISABLED)
        
        # Start looping the spin sound seamlessly
        active_spin_channel = play_sound('spin', loop=-1)
        
        won_item = random.choices(loot_pool, weights=drop_rates, k=1)[0]
        flashes = 20
        base_delay = 40
        
        def animate_roll(current_flash):
            if current_flash < flashes:
                fake_item = random.choice(loot_pool)
                gacha_result.config(text=f"Rolling... [{fake_item}]", fg=themes["Default Theme"]["text"])
                next_delay = base_delay + int((current_flash ** 1.5) * 2) 
                root.after(next_delay, animate_roll, current_flash + 1)
            else:
                finalize_pull(won_item)
        animate_roll(0) 
    else:
        gacha_result.config(text="[ERROR] Insufficient funds.", fg="#ff4c4c")
        play_sound('wrong') # Audio Cue for error

def finalize_pull(won_item):
    global is_pulling, lgf_coins, active_spin_channel
    
    # Kill the spin sound, blast the gacha sound
    if active_spin_channel:
        active_spin_channel.stop()
    play_sound('gacha')
    
    if won_item not in inventory: 
        inventory.append(won_item)
        inventory_listbox.insert(tk.END, won_item)
        if won_item in ["THE GOLDEN COMPILER", "FEU TAMARAWS", "FEU TECH ACM"]:
            gacha_result.config(text=f"[LEGENDARY DROP] YOU UNLOCKED: [{won_item}]!!!", fg=themes[won_item]["accent"])
        elif won_item in ["GILBERTO GREEN", "RADIANT PROTOCOL"]:
            gacha_result.config(text=f"[EPIC DROP] YOU UNLOCKED: [{won_item}]!", fg=themes[won_item]["success"])
        else:
            gacha_result.config(text=f"[SUCCESS] YOU UNLOCKED: [{won_item}]", fg=themes[won_item]["success"])
    else:
        lgf_coins += 25
        gacha_result.config(text=f"[DUPLICATE] Pulled {won_item}. Refunded 25 Coins.", fg="#888888")
        
    update_coin_labels()
    save_progress() 
    is_pulling = False
    btn_pull.config(state=tk.NORMAL)

def equip_item():
    global equipped_theme
    selection = inventory_listbox.curselection()
    if selection:
        item = inventory_listbox.get(selection[0])
        equipped_theme = item
        lbl_equipped.config(text=f"Equipped: [{equipped_theme}]")
        gacha_result.config(text=f"[SYSTEM] Equipped {equipped_theme} successfully.", fg=themes[equipped_theme]["accent"])
        apply_theme(equipped_theme)
        save_progress() 
    else:
        gacha_result.config(text="[WARNING] Select an item from your vault first.", fg="#ff4c4c")
        play_sound('wrong')

# --- DEV TOOLS ---
def enable_dev_mode(event=None):
    global lgf_coins
    lgf_coins += 99999
    update_coin_labels()
    save_progress()
    lbl_menu_dev.config(text="[ DEV FUNDS INJECTED ]", fg="#ffd700")
    play_sound('gacha')

def disable_dev_mode(event=None):
    global lgf_coins, inventory, equipped_theme
    lgf_coins = 0
    inventory = ["Default Theme"]
    inventory_listbox.delete(0, tk.END)
    inventory_listbox.insert(tk.END, "Default Theme")
    equipped_theme = "Default Theme"
    lbl_equipped.config(text=f"Equipped: [{equipped_theme}]")
    apply_theme("Default Theme")
    update_coin_labels()
    save_progress() 
    lbl_menu_dev.config(text="Developer Edition", fg=themes["Default Theme"]["accent"])
    gacha_result.config(text="Account wiped. Awaiting transaction...", fg=themes["Default Theme"]["text"])
    play_sound('wrong')

def unlock_all_skins(event=None):
    global inventory
    for theme_name in themes.keys():
        if theme_name not in inventory:
            inventory.append(theme_name)
            inventory_listbox.insert(tk.END, theme_name)
    save_progress()
    lbl_menu_dev.config(text="[ ALL SKINS UNLOCKED ]", fg="#ffd700")
    play_sound('gacha')

# --- THE UI ENGINE (3D BLOCKY EDITION) ---
def apply_theme(theme_name):
    t = themes[theme_name]
    
    def bind_button_events(btn, default_bg, hover_bg):
        btn.bind("<Enter>", lambda e, b=btn, c=hover_bg: b.configure(bg=c))
        btn.bind("<Leave>", lambda e, b=btn, c=default_bg: b.configure(bg=c))
        btn.bind("<Button-1>", lambda e: play_sound('click'), add="+") # AUDIO CUE
    
    root.configure(bg=t["bg"])
    for frame in [menu_frame, coding_frame, gacha_frame, cheat_frame, pull_left, codex_container, btn_action_frame]:
        frame.configure(bg=t["bg"])
        
    for frame in [mission_frame, inv_right, type_card, op_card, syntax_card]:
        frame.configure(bg=t["panel"], highlightbackground=t["accent"], highlightcolor=t["accent"])
        
    lbl_menu_title.configure(bg=t["bg"], fg=t["text"])
    if lbl_menu_dev.cget("text") not in ["[ GOD MODE ACTIVATED ]", "[ DEV FUNDS INJECTED ]", "[ ALL SKINS UNLOCKED ]"]:
        lbl_menu_dev.configure(bg=t["bg"], fg=t["accent"])
    else:
        lbl_menu_dev.configure(bg=t["bg"]) 
    lbl_menu_coins.configure(bg=t["bg"], fg=t["success"])
    
    # --- 3D BUTTONS & HOVERS ---
    btn_menu_arena.configure(bg=t["accent"], fg=t["btn_fg"], activebackground=t["hover"])
    bind_button_events(btn_menu_arena, t["accent"], t["hover"])
    
    btn_menu_market.configure(bg=t["panel"], fg=t["text"], activebackground=t["accent"])
    bind_button_events(btn_menu_market, t["panel"], t["accent"])
    
    btn_menu_codex.configure(bg=t["panel"], fg=t["text"], activebackground=t["accent"])
    bind_button_events(btn_menu_codex, t["panel"], t["accent"])
    
    btn_back_arena.configure(bg=t["panel"], fg=t["text"], activebackground=t["accent"])
    bind_button_events(btn_back_arena, t["panel"], t["accent"])
    
    btn_execute.configure(bg=t["accent"], fg=t["btn_fg"], activebackground=t["hover"])
    bind_button_events(btn_execute, t["accent"], t["hover"])
    
    btn_next.configure(bg=t["panel"], fg=t["text"], activebackground=t["accent"])
    bind_button_events(btn_next, t["panel"], t["accent"])
    
    btn_back_market.configure(bg=t["panel"], fg=t["text"], activebackground=t["accent"])
    bind_button_events(btn_back_market, t["panel"], t["accent"])
    
    btn_pull.configure(bg=t["accent"], fg=t["btn_fg"], activebackground=t["hover"])
    bind_button_events(btn_pull, t["accent"], t["hover"])
    
    btn_equip.configure(bg=t["accent"], fg=t["btn_fg"], activebackground=t["hover"])
    bind_button_events(btn_equip, t["accent"], t["hover"])
    
    btn_back_codex.configure(bg=t["panel"], fg=t["text"], activebackground=t["accent"])
    bind_button_events(btn_back_codex, t["panel"], t["accent"])

    # UI colors
    lbl_quest.configure(bg=t["panel"], fg=t["success"])
    code_input.configure(bg=t["panel"], fg=t["text"], insertbackground=t["text"])
    console_container.configure(bg=t["bg"])
    console_header.configure(bg=t["panel"], fg=t["text"])
    console_output.configure(bg=t["bg"], fg=t["success"])
    
    lbl_market_title.configure(bg=t["bg"], fg=t["text"])
    lbl_gacha_coins.configure(bg=t["bg"], fg=t["success"])
    if "SUCCESS" not in gacha_result.cget("text") and "LEGENDARY" not in gacha_result.cget("text") and "EPIC" not in gacha_result.cget("text"):
        gacha_result.configure(bg=t["bg"], fg=t["text"])
    else:
        gacha_result.configure(bg=t["bg"])
        
    lbl_vault_title.configure(bg=t["panel"], fg=t["text"])
    lbl_equipped.configure(bg=t["panel"], fg=t["success"])
    inventory_listbox.configure(bg=t["bg"], fg=t["text"], selectbackground=t["accent"], selectforeground=t["btn_fg"])
    
    lbl_codex_title.configure(bg=t["bg"], fg=t["accent"])
    lbl_type_title.configure(bg=t["panel"], fg=t["text"])
    lbl_type_text.configure(bg=t["panel"], fg=t["text"])
    lbl_op_title.configure(bg=t["panel"], fg=t["text"])
    lbl_op_text.configure(bg=t["panel"], fg=t["text"])
    lbl_syntax_title.configure(bg=t["panel"], fg=t["text"])
    lbl_syntax_text.configure(bg=t["panel"], fg=t["text"])
    
    highlight_syntax()

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
root.state("zoomed") 
root.title("LGF Client")

menu_frame = tk.Frame(root)
coding_frame = tk.Frame(root)
gacha_frame = tk.Frame(root)
cheat_frame = tk.Frame(root)

# ==========================================
# SCREEN 0: THE BOOT-UP SEQUENCE
# ==========================================
boot_frame = tk.Frame(root, bg="#050505")
lbl_boot = tk.Label(boot_frame, text="", bg="#050505", fg="#00ff00", font=(RETRO_FONT, 16, "bold"), justify=tk.LEFT)
lbl_boot.pack(anchor="nw", padx=20, pady=20)

def run_boot_sequence():
    boot_frame.pack(fill=tk.BOTH, expand=True)
    messages = [
        "LGF_OS v3.1.4 [INITIALIZING...]",
        "LOADING AUDIO MIXER... [OK]",
        "LOADING LEXICAL STATE MACHINE... [OK]",
        "MOUNTING VAULT DATA... [OK]",
        "ESTABLISHING NEURAL LINK... [OK]",
        "SYSTEM READY."
    ]
    def show_message(index):
        if index < len(messages):
            current_text = lbl_boot.cget("text")
            lbl_boot.config(text=current_text + "\n> " + messages[index])
            root.after(300, show_message, index + 1)
        else:
            root.after(800, finish_boot)
            
    def finish_boot():
        boot_frame.pack_forget()
        show_frame(menu_frame)

    root.after(500, show_message, 0)

# ==========================================
# SCREEN 1: MAIN MENU
# ==========================================
lbl_menu_title = tk.Label(menu_frame, text="LGF COMPILER", font=(RETRO_FONT, 54, "bold"))
lbl_menu_title.pack(pady=(100, 10))

lbl_menu_dev = tk.Label(menu_frame, text="Developer Edition", font=(RETRO_FONT, 17, "italic"))
lbl_menu_dev.pack(pady=(0, 40))

lbl_menu_coins = tk.Label(menu_frame, text=f"[VAULT]: {lgf_coins} Coins", font=(RETRO_FONT, 20, "bold"))
lbl_menu_coins.pack(pady=10)

btn_menu_arena = tk.Button(menu_frame, text="ENTER ARENA", font=(RETRO_FONT, 17, "bold"), width=22, pady=3, bd=5, relief=tk.RAISED, command=lambda: show_frame(coding_frame))
btn_menu_arena.pack(pady=10)

btn_menu_market = tk.Button(menu_frame, text="THE MARKETPLACE", font=(RETRO_FONT, 17, "bold"), width=22, pady=3, bd=5, relief=tk.RAISED, command=lambda: show_frame(gacha_frame))
btn_menu_market.pack(pady=10)

btn_menu_codex = tk.Button(menu_frame, text="ACCESS CODEX", font=(RETRO_FONT, 17, "bold"), width=22, pady=3, bd=5, relief=tk.RAISED, command=lambda: show_frame(cheat_frame))
btn_menu_codex.pack(pady=10)

# ==========================================
# SCREEN 2: CODING ARENA
# ==========================================
btn_back_arena = tk.Button(coding_frame, text="RETURN TO MENU", font=(RETRO_FONT, 12, "bold"), bd=5, relief=tk.RAISED, command=lambda: show_frame(menu_frame))
btn_back_arena.pack(anchor="nw", padx=10, pady=10)

mission_frame = tk.Frame(coding_frame, bd=5, relief=tk.RAISED)
mission_frame.pack(fill=tk.X, padx=20, pady=(10, 20))

lbl_quest = tk.Label(mission_frame, text=active_quest["task"], font=(RETRO_FONT, 24, "bold"), pady=20)
lbl_quest.pack()

code_input = tk.Text(coding_frame, height=5, font=(RETRO_FONT, 22), bd=4, relief=tk.SUNKEN)
code_input.pack(fill=tk.X, padx=20)
code_input.bind("<KeyRelease>", highlight_syntax)

btn_action_frame = tk.Frame(coding_frame)
btn_action_frame.pack(pady=15)

btn_execute = tk.Button(btn_action_frame, text="COMPILE & EXECUTE", font=(RETRO_FONT, 14, "bold"), pady=3, bd=5, relief=tk.RAISED, command=execute_code)
btn_execute.pack(side=tk.LEFT, padx=10)

btn_next = tk.Button(btn_action_frame, text="NEXT MISSION", font=(RETRO_FONT, 14, "bold"), pady=3, bd=5, relief=tk.RAISED, command=next_quest)

console_container = tk.Frame(coding_frame, bd=5, relief=tk.SUNKEN)
console_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))

console_header = tk.Label(console_container, text="[ SYSTEM TERMINAL ]", font=(RETRO_FONT, 16, "bold"), anchor="w", padx=10, pady=4)
console_header.pack(fill=tk.X)

console_output = scrolledtext.ScrolledText(console_container, height=8, font=(RETRO_FONT, 18), bd=0, highlightthickness=0, padx=10, pady=10)
console_output.pack(fill=tk.BOTH, expand=True)

sys.stdout = RedirectText(console_output)

# ==========================================
# SCREEN 3: GACHA PULL (THE MARKETPLACE)
# ==========================================
pull_left = tk.Frame(gacha_frame)
pull_left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

inv_right = tk.Frame(gacha_frame, width=450, bd=5, relief=tk.RAISED)
inv_right.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)

btn_back_market = tk.Button(pull_left, text="RETURN TO MENU", font=(RETRO_FONT, 12, "bold"), bd=5, relief=tk.RAISED, command=lambda: show_frame(menu_frame))
btn_back_market.pack(anchor="nw", padx=10, pady=10)

lbl_market_title = tk.Label(pull_left, text="THE MARKETPLACE", font=(RETRO_FONT, 42, "bold"))
lbl_market_title.pack(pady=30)

lbl_gacha_coins = tk.Label(pull_left, text=f"[VAULT]: {lgf_coins} Coins", font=(RETRO_FONT, 22, "bold"))
lbl_gacha_coins.pack(pady=10)

btn_pull = tk.Button(pull_left, text="PULL SKIN (100 COINS)", font=(RETRO_FONT, 18, "bold"), pady=5, bd=5, relief=tk.RAISED, command=pull_gacha)
btn_pull.pack(pady=30)

gacha_result = tk.Label(pull_left, text="Awaiting transaction...", font=(RETRO_FONT, 18))
gacha_result.pack(pady=20)

lbl_vault_title = tk.Label(inv_right, text="YOUR VAULT", font=(RETRO_FONT, 24, "bold"))
lbl_vault_title.pack(pady=(20, 10))

lbl_equipped = tk.Label(inv_right, text=f"Equipped: [{equipped_theme}]", font=(RETRO_FONT, 14, "italic"), wraplength=300)
lbl_equipped.pack(pady=(0, 20))

inventory_listbox = tk.Listbox(inv_right, font=(RETRO_FONT, 20), bd=4, relief=tk.SUNKEN)
inventory_listbox.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))

for item in inventory:
    inventory_listbox.insert(tk.END, item)

btn_equip = tk.Button(inv_right, text="EQUIP SELECTED", font=(RETRO_FONT, 16, "bold"), pady=5, bd=5, relief=tk.RAISED, command=equip_item)
btn_equip.pack(fill=tk.X, padx=20, pady=(0, 20))

# ==========================================
# SCREEN 4: CHEAT SHEET (THE CODEX)
# ==========================================
btn_back_codex = tk.Button(cheat_frame, text="RETURN TO MENU", font=(RETRO_FONT, 12, "bold"), bd=5, relief=tk.RAISED, command=lambda: show_frame(menu_frame))
btn_back_codex.pack(anchor="nw", padx=10, pady=10)

lbl_codex_title = tk.Label(cheat_frame, text="LGF CODEX", font=(RETRO_FONT, 42, "bold"))
lbl_codex_title.pack(pady=10)

codex_container = tk.Frame(cheat_frame)
codex_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

type_card = tk.Frame(codex_container, bd=5, relief=tk.RAISED)
type_card.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)

lbl_type_title = tk.Label(type_card, text="DATA TYPES", font=(RETRO_FONT, 24, "bold"))
lbl_type_title.pack(pady=(30, 20))

types_text = """OUNT    : Integer values\n\nYEARN   : Text/String values\n\nHERO    : Single character\n\nTAMARAW : Boolean true/false\n\n\n*WARNING: Lexer is case-sensitive!\nStrings need "Double Quotes"."""
lbl_type_text = tk.Label(type_card, text=types_text, font=(RETRO_FONT, 20), justify="left")
lbl_type_text.pack(anchor="w", padx=30, pady=10)

op_card = tk.Frame(codex_container, bd=5, relief=tk.RAISED)
op_card.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)

lbl_op_title = tk.Label(op_card, text="OPERATORS & I/O", font=(RETRO_FONT, 24, "bold"))
lbl_op_title.pack(pady=(30, 20))

op_text = """OPERATORS:\nIS : Assignment Operator (=)\n\n:> : Statement Delimiter (;)\n\n\nI/O KEYWORDS:\nRELEASE : Output display data\n\nEndThat : Line break (\\n)"""
lbl_op_text = tk.Label(op_card, text=op_text, font=(RETRO_FONT, 20), justify="left")
lbl_op_text.pack(anchor="w", padx=30, pady=10)

syntax_card = tk.Frame(codex_container, bd=5, relief=tk.RAISED)
syntax_card.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)

lbl_syntax_title = tk.Label(syntax_card, text="GRAMMAR RULES", font=(RETRO_FONT, 24, "bold"))
lbl_syntax_title.pack(pady=(30, 20))

syntax_text = """VARIABLE DECLARATION:\n[Type] [Name] IS [Literal] :>\n\nEx: OUNT age IS 21 :>\n\n\nOUTPUT STATEMENT:\nRELEASE [Identifier], EndThat :>\n\nEx: RELEASE age, EndThat :>"""
lbl_syntax_text = tk.Label(syntax_card, text=syntax_text, font=(RETRO_FONT, 20), justify="left")
lbl_syntax_text.pack(anchor="w", padx=30, pady=10)

# --- STARTUP ---
apply_theme(equipped_theme) 
run_boot_sequence() 

# SECRET HOTKEYS
root.bind('<F9>', enable_dev_mode)
root.bind('<F10>', disable_dev_mode)
root.bind('<F11>', unlock_all_skins)

root.mainloop()