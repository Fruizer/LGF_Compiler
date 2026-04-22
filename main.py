import tkinter as tk
from tkinter import scrolledtext, Toplevel, Canvas
import sys
import random
import json
import os

# --- AUDIO ENGINE (PYGAME) ---
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame

pygame.mixer.init()
sounds = {}

# NEW: This function helps the .exe find your mp3 files when bundled!
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def load_sounds():
    try:
        sounds['click'] = pygame.mixer.Sound(resource_path("click.mp3"))
        sounds['right'] = pygame.mixer.Sound(resource_path("rightAnswer.mp3"))
        sounds['wrong'] = pygame.mixer.Sound(resource_path("wrongAnswer.mp3"))
        sounds['spin'] = pygame.mixer.Sound(resource_path("spin.mp3"))
        sounds['gacha'] = pygame.mixer.Sound(resource_path("gachagot.mp3"))
    except Exception as e:
        print(f"[SYSTEM] Audio files missing or failed to load: {e}")

load_sounds()

def play_sound(name, loop=0):
    if name in sounds:
        try:
            return sounds[name].play(loops=loop)
        except:
            pass
    return None

active_spin_channel = None 

# --- GAME STATE & QUEST ENGINE ---
lgf_coins = 0
lgf_exp = 0    
symbol_table = {}
inventory = ["Default Theme"] 
equipped_theme = "Default Theme"
latest_ast = None # NEW: Holds the visual logic tree data

quests_completed = 0
current_difficulty = "EASY"
is_pulling = False 

RETRO_FONT = "Fixedsys"
SAVE_FILE = "lgf_save_data.json"

# --- RANKING SYSTEM ---
RANKS = [
    (0, "Code Freshman"),
    (500, "Syntax Sophomore"),
    (1500, "Logic Junior"),
    (3000, "Senior Engineer"),
    (6000, "LGF Master"),
    (10000, "The Gilberto")
]

def get_rank_info(exp):
    current_rank = "Code Freshman"
    next_threshold = 500
    for i, (threshold, name) in enumerate(RANKS):
        if exp >= threshold:
            current_rank = name
            if i + 1 < len(RANKS):
                next_threshold = RANKS[i+1][0]
            else:
                next_threshold = "MAX"
    return current_rank, next_threshold

def load_progress():
    global lgf_coins, lgf_exp, inventory, equipped_theme, quests_completed
    if os.path.exists(SAVE_FILE):
        try:
            with open(SAVE_FILE, "r") as f:
                data = json.load(f)
                lgf_coins = data.get("coins", 0)
                lgf_exp = data.get("exp", 0) 
                inventory = data.get("inventory", ["Default Theme"])
                equipped_theme = data.get("equipped_theme", "Default Theme")
                quests_completed = data.get("quests_completed", 0)
        except Exception as e:
            print(f"Error loading save data: {e}")

def save_progress():
    data = {
        "coins": lgf_coins,
        "exp": lgf_exp, 
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
        {"task": "MISSION: Declare an OUNT equal to 0.", "target": "OUNT_ZERO", "reward": 50}
    ],
    "MEDIUM": [
        {"task": "MISSION: Print data using RELEASE.", "target": "RELEASE", "reward": 100},
        {"task": "MISSION: Declare TWO different OUNT variables.", "target": "TWO_OUNT", "reward": 100},
        {"task": "MISSION: Add two numbers.", "target": "MATH_ADD", "reward": 150},
        {"task": "MISSION: Subtract two numbers.", "target": "MATH_SUB", "reward": 150}
    ],
    "HARD": [
        {"task": "MISSION: Declare an OUNT, then RELEASE it.", "target": "COMBO_OUNT_RELEASE", "reward": 250},
        {"task": "MISSION: Declare a TAMARAW and an OUNT.", "target": "COMBO_TAMARAW_OUNT", "reward": 250},
        {"task": "MISSION: Add two numbers and RELEASE result.", "target": "MATH_COMBO_ADD", "reward": 300}
    ],
    "EXTREME": [
        {"task": "MISSION: Multiply two numbers and RELEASE result.", "target": "MATH_COMBO_MUL", "reward": 500},
        {"task": "MISSION: TRI COMBO! Declare OUNT, YEARN, TAMARAW.", "target": "TRI_COMBO", "reward": 800},
        {"task": "MISSION: EXTREME! Declare 3 variable types AND use RELEASE.", "target": "EXTREME_RELEASE", "reward": 1500}
    ]
}

def generate_quest():
    global current_difficulty
    if quests_completed < 4:
        current_difficulty = "EASY"
    elif quests_completed < 10:
        current_difficulty = random.choices(["EASY", "MEDIUM"], weights=[20, 80], k=1)[0]
    elif quests_completed < 15:
        current_difficulty = random.choices(["MEDIUM", "HARD"], weights=[30, 70], k=1)[0]
    else:
        current_difficulty = random.choices(["HARD", "EXTREME"], weights=[40, 60], k=1)[0]
        
    pool = quest_db[current_difficulty]
    return random.choice(pool)

active_quest = generate_quest()

# --- THE VERBOSE COMPILER ENGINE WITH AST GENERATION ---
def lgf_compiler(source_code):
    global latest_ast
    print(f"Input Code: {source_code}\n")
    cleaned_code = source_code.replace(":>", " :> ").replace(",", " , ")
    cleaned_code = cleaned_code.replace("+", " + ").replace("-", " - ").replace("*", " * ").replace("/", " / ")
    words = cleaned_code.split()
    if not words: return False

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
        elif word in ["+", "-", "*", "/"]: 
            tokens.append(("MATH_OP", word))
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
        print(f"[LEXER] Found '{word}' -> {tokens[-1][0]}")
    print("Lexical Analysis Complete.\n")

    print("--- STARTING SYNTAX ANALYSIS ---")
    is_assignment = False
    is_math_assignment = False
    is_release = False

    if tokens[0][0] == "DATATYPE":
        if len(tokens) == 5 and (tokens[1][0] == "IDENTIFIER" and tokens[2][0] == "ASSIGN" and tokens[3][0].startswith("LITERAL") and tokens[4][0] == "DELIMITER"):
            is_assignment = True
            print("[PARSER] Syntax Valid: Standard Assignment")
        elif len(tokens) == 7 and (tokens[1][0] == "IDENTIFIER" and tokens[2][0] == "ASSIGN" and tokens[4][0] == "MATH_OP" and tokens[6][0] == "DELIMITER"):
            is_math_assignment = True
            print("[PARSER] Syntax Valid: Math Assignment")
        else:
            print("[PARSER] FATAL ERROR: Syntax invalid.")
            return False
    elif tokens[0][0] == "OUTPUT_CMD":
        is_release = True
        if tokens[-1][0] != "DELIMITER":
            print("[PARSER] FATAL ERROR: Missing delimiter ':>'.")
            return False
        print("[PARSER] Syntax Valid: Release Command")
    else:
        print("[PARSER] FATAL ERROR: Unknown statement.")
        return False

    print("--- STARTING SEMANTIC ANALYSIS ---")
    if is_assignment:
        var_type, var_name, var_value, literal_type = tokens[0][1], tokens[1][1], tokens[3][1], tokens[3][0]
        is_valid_type = (var_type == "OUNT" and literal_type == "LITERAL_INT") or \
                        (var_type == "YEARN" and literal_type == "LITERAL_STRING") or \
                        (var_type == "HERO" and literal_type == "LITERAL_CHAR") or \
                        (var_type == "TAMARAW" and literal_type == "LITERAL_BOOL")

        if is_valid_type:
            symbol_table[var_name] = {"type": var_type, "value": var_value}
            print(f"[SEMANTICS] Bound '{var_name}' to Symbol Table.")
            # Construct AST
            latest_ast = {"name": "ASSIGN (IS)", "left": {"name": f"VAR: {var_name}\n({var_type})"}, "right": {"name": f"VAL:\n{var_value}"}}
        else:
            print(f"[SEMANTICS] FATAL ERROR: Type mismatch.")
            return False
            
    elif is_math_assignment:
        var_type, var_name = tokens[0][1], tokens[1][1]
        val1, operator, val2 = tokens[3][1], tokens[4][1], tokens[5][1]
        if var_type != "OUNT":
            print("[SEMANTICS] FATAL ERROR: Math only allowed for OUNT.")
            return False
        try:
            if operator == "+": result = int(val1) + int(val2)
            elif operator == "-": result = int(val1) - int(val2)
            elif operator == "*": result = int(val1) * int(val2)
            elif operator == "/": result = int(val1) // int(val2)
            symbol_table[var_name] = {"type": "OUNT", "value": result}
            print(f"[SEMANTICS] Bound '{var_name}' = {result}.")
            # Construct AST
            latest_ast = {
                "name": "ASSIGN (IS)", 
                "left": {"name": f"VAR: {var_name}\n({var_type})"}, 
                "right": {
                    "name": f"OP: {operator}", 
                    "left": {"name": f"VAL:\n{val1}"}, 
                    "right": {"name": f"VAL:\n{val2}"}
                }
            }
        except Exception:
            print("[SEMANTICS] FATAL ERROR: Invalid math.")
            return False
            
    elif is_release:
        output_string = ""
        ast_children = []
        for i in range(1, len(tokens) - 1):
            tok_type, tok_val = tokens[i]
            if tok_type == "IDENTIFIER":
                if tok_val in symbol_table:
                    output_string += str(symbol_table[tok_val]["value"]).replace('"', '').replace("'", "")
                    ast_children.append({"name": f"VAR REF:\n{tok_val}"})
                else:
                    print(f"[SEMANTICS] FATAL ERROR: '{tok_val}' not defined!")
                    return False
            elif tok_type.startswith("LITERAL"):
                output_string += str(tok_val).replace('"', '').replace("'", "")
            elif tok_type == "NEWLINE":
                output_string += "\n"
                ast_children.append({"name": f"CMD:\nEndThat"})
        print("\n=== PROGRAM OUTPUT ===")
        print(output_string)
        print("======================\n")
        
        # Construct AST for Output
        if len(ast_children) == 1:
            latest_ast = {"name": "OUTPUT (RELEASE)", "left": ast_children[0]}
        elif len(ast_children) > 1:
            latest_ast = {"name": "OUTPUT (RELEASE)", "left": ast_children[0], "right": ast_children[1]}
        else:
            latest_ast = {"name": "OUTPUT (RELEASE)", "left": {"name": "EMPTY"}}

    return True

# --- AST VISUALIZER MODAL ---
def draw_ast_node(canvas, node, x, y, x_offset, t):
    box_width, box_height = 100, 60
    
    # Draw connections first so they go behind nodes
    if "left" in node:
        canvas.create_line(x, y + box_height/2, x - x_offset, y + 100, fill=t["accent"], width=3, arrow=tk.LAST)
        draw_ast_node(canvas, node["left"], x - x_offset, y + 100, x_offset / 1.5, t)
    if "right" in node:
        canvas.create_line(x, y + box_height/2, x + x_offset, y + 100, fill=t["accent"], width=3, arrow=tk.LAST)
        draw_ast_node(canvas, node["right"], x + x_offset, y + 100, x_offset / 1.5, t)
        
    # Draw actual node
    canvas.create_rectangle(x - box_width/2, y - box_height/2, x + box_width/2, y + box_height/2, 
                            fill=t["panel"], outline=t["success"], width=3)
    canvas.create_text(x, y, text=node["name"], fill=t["text"], font=(RETRO_FONT, 14, "bold"), justify="center")

def show_ast_visualizer():
    global latest_ast
    if not latest_ast:
        print("[SYSTEM] No AST available. Compile a valid script first.")
        return
        
    play_sound('click')
    t = themes[equipped_theme]
    
    ast_window = Toplevel(root)
    ast_window.title("LGF OS - Abstract Syntax Tree")
    ast_window.geometry("800x600")
    ast_window.configure(bg=t["bg"])
    
    lbl_title = tk.Label(ast_window, text="LOGIC GRAPH GENERATED", font=(RETRO_FONT, 24, "bold"), bg=t["bg"], fg=t["success"])
    lbl_title.pack(pady=20)
    
    canvas = Canvas(ast_window, bg=t["bg"], highlightthickness=0)
    canvas.pack(fill=tk.BOTH, expand=True)
    
    # Start drawing from top center
    draw_ast_node(canvas, latest_ast, 400, 80, 200, t)

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
    global symbol_table, latest_ast
    symbol_table.clear()
    latest_ast = None
    btn_execute.config(state=tk.DISABLED) 
    btn_view_ast.pack_forget() # Hide AST button until success
    
    print("\n" + "="*50)
    print("[SYSTEM] INITIATING COMPILER CYCLE...\n")
    
    code = code_input.get("1.0", tk.END).strip()
    if not code:
        print("[SYSTEM] The editor is empty.\n")
        root.after(100, lambda: wait_for_typing(code, False))
        return

    lines = [line.strip() for line in code.split('\n') if line.strip()]
    success = True
    for line in lines: 
        if not lgf_compiler(line): success = False
    
    wait_for_typing(code, success)

def wait_for_typing(code, success):
    if getattr(sys.stdout, 'is_typing', False):
        root.after(50, lambda: wait_for_typing(code, success))
    else:
        check_rewards(code, success)

def check_rewards(code, success):
    global lgf_coins, lgf_exp, quests_completed
    
    if not success:
        print("\n[SYSTEM] Compilation failed. 0 EXP / 0 Coins awarded.\n")
        play_sound('wrong') 
        btn_execute.config(state=tk.NORMAL)
        return
        
    # Show AST Button on success!
    btn_view_ast.pack(side=tk.LEFT, padx=10)

    quest_passed = False
    target = active_quest["target"]
    
    if target in ["OUNT", "YEARN", "TAMARAW", "HERO"]:
        if any(data["type"] == target for data in symbol_table.values()): quest_passed = True
    elif target == "OUNT_ZERO":
        if any(data["type"] == "OUNT" and int(data["value"]) == 0 for data in symbol_table.values()): quest_passed = True
    elif target == "RELEASE":
        if "RELEASE" in code: quest_passed = True
    elif target == "TWO_OUNT":
        if sum(1 for data in symbol_table.values() if data["type"] == "OUNT") >= 2: quest_passed = True
    elif target == "COMBO_OUNT_RELEASE":
        if any(data["type"] == "OUNT" for data in symbol_table.values()) and "RELEASE" in code: quest_passed = True
    elif target == "COMBO_TAMARAW_OUNT":
        if any(data["type"] == "TAMARAW" for data in symbol_table.values()) and any(data["type"] == "OUNT" for data in symbol_table.values()): quest_passed = True
    elif target == "MATH_ADD":
        if "+" in code and any(data["type"] == "OUNT" for data in symbol_table.values()): quest_passed = True
    elif target == "MATH_SUB":
        if "-" in code and any(data["type"] == "OUNT" for data in symbol_table.values()): quest_passed = True
    elif target == "MATH_COMBO_ADD":
        if "+" in code and "RELEASE" in code: quest_passed = True
    elif target == "MATH_COMBO_MUL":
        if "*" in code and "RELEASE" in code: quest_passed = True
    elif target == "TRI_COMBO":
        if any(d["type"] == "OUNT" for d in symbol_table.values()) and any(d["type"] == "YEARN" for d in symbol_table.values()) and any(d["type"] == "TAMARAW" for d in symbol_table.values()): quest_passed = True
    elif target == "EXTREME_RELEASE":
        types = set(d["type"] for d in symbol_table.values())
        if len(types) >= 3 and "RELEASE" in code: quest_passed = True

    if quest_passed:
        reward = active_quest["reward"]
        old_rank, _ = get_rank_info(lgf_exp)
        lgf_exp += reward
        lgf_coins += reward
        quests_completed += 1
        new_rank, _ = get_rank_info(lgf_exp)
        
        print(f"\n[QUEST COMPLETE] Target acquired! +{reward} EXP / +{reward} Coins.\n")
        if new_rank != old_rank:
            print("*"*50)
            print(f"[PROMOTION] YOU HAVE RANKED UP TO: {new_rank.upper()}!!!")
            print("*"*50 + "\n")
            play_sound('gacha') 
        else:
            play_sound('right') 
            
        update_stats_labels()
        save_progress() 
        btn_next.pack(side=tk.LEFT, padx=10)
    else:
        print("\n[SYSTEM] Target ignored. 0 EXP / 0 Coins.\n")
        play_sound('wrong') 
        btn_execute.config(state=tk.NORMAL)

def next_quest():
    global active_quest
    active_quest = generate_quest()
    lbl_quest.config(text=active_quest["task"]) 
    code_input.delete("1.0", tk.END)
    console_output.delete("1.0", tk.END) 
    highlight_syntax()
    btn_next.pack_forget()
    btn_view_ast.pack_forget()
    btn_execute.config(state=tk.NORMAL)

# --- THE GACHA ANIMATION SYSTEM ---
def pull_gacha():
    global lgf_coins, inventory, is_pulling, active_spin_channel
    if is_pulling: return 
    
    loot_pool = list(themes.keys())
    loot_pool.remove("Default Theme")
    drop_rates = [1.0 if t in ["THE GOLDEN COMPILER", "FEU TAMARAWS", "FEU TECH ACM"] else 3.0 if t in ["GILBERTO GREEN", "RADIANT PROTOCOL"] else 9.1 for t in loot_pool]
    
    if lgf_coins >= 100:
        lgf_coins -= 100
        update_stats_labels()
        save_progress()
        is_pulling = True
        btn_pull.config(state=tk.DISABLED)
        
        active_spin_channel = play_sound('spin', loop=-1)
        won_item = random.choices(loot_pool, weights=drop_rates, k=1)[0]
        
        def animate_roll(current_flash):
            if current_flash < 20:
                gacha_result.config(text=f"Rolling... [{random.choice(loot_pool)}]", fg=themes["Default Theme"]["text"])
                root.after(40 + int((current_flash ** 1.5) * 2), animate_roll, current_flash + 1)
            else:
                finalize_pull(won_item)
        animate_roll(0) 
    else:
        gacha_result.config(text="[ERROR] Insufficient funds.", fg="#ff4c4c")
        play_sound('wrong') 

def finalize_pull(won_item):
    global is_pulling, lgf_coins, active_spin_channel
    if active_spin_channel: active_spin_channel.stop()
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
        
    update_stats_labels()
    save_progress() 
    is_pulling = False
    btn_pull.config(state=tk.NORMAL)

def equip_item():
    global equipped_theme
    selection = inventory_listbox.curselection()
    if selection:
        equipped_theme = inventory_listbox.get(selection[0])
        lbl_equipped.config(text=f"Equipped: [{equipped_theme}]")
        gacha_result.config(text=f"[SYSTEM] Equipped {equipped_theme} successfully.", fg=themes[equipped_theme]["accent"])
        apply_theme(equipped_theme)
        save_progress() 
    else:
        gacha_result.config(text="[WARNING] Select an item from your vault first.", fg="#ff4c4c")
        play_sound('wrong')

# --- DEV TOOLS ---
def enable_dev_mode(event=None):
    global lgf_coins, lgf_exp
    lgf_coins += 99999
    lgf_exp += 99999
    update_stats_labels()
    save_progress()
    lbl_menu_dev.config(text="[ GOD MODE ACTIVATED ]", fg="#ffd700")
    play_sound('gacha')

def disable_dev_mode(event=None):
    global lgf_coins, lgf_exp, inventory, equipped_theme
    lgf_coins = 0
    lgf_exp = 0
    inventory = ["Default Theme"]
    inventory_listbox.delete(0, tk.END)
    inventory_listbox.insert(tk.END, "Default Theme")
    equipped_theme = "Default Theme"
    lbl_equipped.config(text=f"Equipped: [{equipped_theme}]")
    apply_theme("Default Theme")
    update_stats_labels()
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
        btn.bind("<Button-1>", lambda e: play_sound('click'), add="+") 
    
    root.configure(bg=t["bg"])
    for frame in [menu_frame, coding_frame, gacha_frame, cheat_frame, pull_left, codex_container, btn_action_frame]:
        frame.configure(bg=t["bg"])
        
    for frame in [mission_frame, inv_right, type_card, op_card, syntax_card]:
        frame.configure(bg=t["panel"], highlightbackground=t["accent"], highlightcolor=t["accent"])
        
    lbl_menu_title.configure(bg=t["bg"], fg=t["text"])
    lbl_menu_dev.configure(bg=t["bg"], fg=t["accent"] if lbl_menu_dev.cget("text") not in ["[ GOD MODE ACTIVATED ]", "[ DEV FUNDS INJECTED ]", "[ ALL SKINS UNLOCKED ]"] else t["bg"])
    lbl_menu_rank.configure(bg=t["bg"], fg=t["accent"])
    lbl_menu_exp.configure(bg=t["bg"], fg=t["success"])
    lbl_menu_coins.configure(bg=t["bg"], fg=t["success"])
    
    for btn in [btn_menu_arena, btn_execute, btn_pull, btn_equip, btn_view_ast]:
        btn.configure(bg=t["accent"], fg=t["btn_fg"], activebackground=t["hover"])
        bind_button_events(btn, t["accent"], t["hover"])
        
    for btn in [btn_menu_market, btn_menu_codex, btn_back_arena, btn_next, btn_back_market, btn_back_codex]:
        btn.configure(bg=t["panel"], fg=t["text"], activebackground=t["accent"])
        bind_button_events(btn, t["panel"], t["accent"])

    lbl_quest.configure(bg=t["panel"], fg=t["success"])
    code_input.configure(bg=t["panel"], fg=t["text"], insertbackground=t["text"])
    console_container.configure(bg=t["bg"])
    console_header.configure(bg=t["panel"], fg=t["text"])
    console_output.configure(bg=t["bg"], fg=t["success"])
    
    lbl_market_title.configure(bg=t["bg"], fg=t["text"])
    lbl_gacha_coins.configure(bg=t["bg"], fg=t["success"])
    gacha_result.configure(bg=t["bg"], fg=t["text"] if "SUCCESS" not in gacha_result.cget("text") and "LEGENDARY" not in gacha_result.cget("text") and "EPIC" not in gacha_result.cget("text") else t["bg"])
        
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
    for f in [menu_frame, coding_frame, gacha_frame, cheat_frame]: f.pack_forget()
    frame_to_show.pack(fill=tk.BOTH, expand=True)

def update_stats_labels():
    current_rank, next_threshold = get_rank_info(lgf_exp)
    lbl_menu_rank.config(text=f"[{current_rank}]")
    lbl_menu_exp.config(text=f"[EXP]: {lgf_exp} (MAX RANK)" if next_threshold == "MAX" else f"[EXP]: {lgf_exp} / {next_threshold}")
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
    messages = ["LGF_OS v3.1.4 [INITIALIZING...]", "LOADING AUDIO MIXER... [OK]", "LOADING LEXICAL STATE MACHINE... [OK]", "MOUNTING VAULT DATA... [OK]", "ESTABLISHING NEURAL LINK... [OK]", "SYSTEM READY."]
    def show_message(index):
        if index < len(messages):
            lbl_boot.config(text=lbl_boot.cget("text") + "\n> " + messages[index])
            root.after(300, show_message, index + 1)
        else:
            root.after(800, lambda: [boot_frame.pack_forget(), show_frame(menu_frame)])
    root.after(500, show_message, 0)

# ==========================================
# SCREEN 1: MAIN MENU
# ==========================================
lbl_menu_title = tk.Label(menu_frame, text="LGF COMPILER", font=(RETRO_FONT, 54, "bold"))
lbl_menu_title.pack(pady=(80, 10))

lbl_menu_dev = tk.Label(menu_frame, text="Developer Edition", font=(RETRO_FONT, 17, "italic"))
lbl_menu_dev.pack(pady=(0, 20))

lbl_menu_rank = tk.Label(menu_frame, text="[Rank Loading...]", font=(RETRO_FONT, 24, "bold"))
lbl_menu_rank.pack(pady=(0, 5))
lbl_menu_exp = tk.Label(menu_frame, text="[EXP Loading...]", font=(RETRO_FONT, 16))
lbl_menu_exp.pack(pady=(0, 20))
lbl_menu_coins = tk.Label(menu_frame, text=f"[VAULT]: {lgf_coins} Coins", font=(RETRO_FONT, 20, "bold"))
lbl_menu_coins.pack(pady=(0, 20))

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

# NEW BUTTON FOR AST VISUALIZER
btn_view_ast = tk.Button(btn_action_frame, text="VIEW AST", font=(RETRO_FONT, 14, "bold"), pady=3, bd=5, relief=tk.RAISED, command=show_ast_visualizer)
# It starts hidden, only shown upon successful compilation

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
for item in inventory: inventory_listbox.insert(tk.END, item)
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

update_stats_labels() 
apply_theme(equipped_theme) 
run_boot_sequence() 

root.bind('<F9>', enable_dev_mode)
root.bind('<F10>', disable_dev_mode)
root.bind('<F11>', unlock_all_skins)

root.mainloop()