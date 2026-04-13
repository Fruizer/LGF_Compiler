import tkinter as tk
from tkinter import scrolledtext
import sys

# --- GAME STATE VARIABLES ---
lgf_coins = 0
current_quest_index = 0
quests = [
    {"title": "Quest 1: The Basics", "task": "Declare an OUNT (Integer) variable.", "target_token": "OUNT", "reward": 50},
    {"title": "Quest 2: Speak Up", "task": "Use the RELEASE command to print something.", "target_token": "OUTPUT_CMD", "reward": 100}
]

symbol_table = {}

def lgf_compiler(source_code):
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
            print(f"[LEXER] Found '{word}' -> Identified as NEWLINE_MANIPULATOR")
        elif word == ",":
            tokens.append(("COMMA", word))
            print(f"[LEXER] Found '{word}' -> Identified as COMMA")
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

    # PARSER THINGS
    print("--- STARTING SYNTAX ANALYSIS ---")
    print("[PARSER] Checking statement structure...")

    is_assignment = False
    is_release = False

    if tokens[0][0] == "DATATYPE":
        is_assignment = True
        print("[PARSER] Expected rule: [DATATYPE] [IDENTIFIER] [ASSIGN] [LITERAL] [DELIMITER]")
        if len(tokens) == 5:
            if (tokens[1][0] == "IDENTIFIER" and
                tokens[2][0] == "ASSIGN" and
                tokens[3][0].startswith("LITERAL") and
                tokens[4][0] == "DELIMITER"):
                print("[PARSER] Actual structure matches expected rule perfectly.")
                print("Syntax Analysis Complete. No structural errors.\n")
            else:
                print("[PARSER] FATAL ERROR: Syntax is invalid. Wrong token order.")
                return
        else:
            print("[PARSER] FATAL ERROR: Syntax is invalid. Missing or extra tokens.")
            return

    elif tokens[0][0] == "OUTPUT_CMD":
        is_release = True
        print("[PARSER] Expected rule: RELEASE [Identifier/Literal], EndThat :> (or similar list)")
        if tokens[-1][0] != "DELIMITER":
            print("[PARSER] FATAL ERROR: Missing delimiter ':>' at the end.")
            return
        print("[PARSER] Structure accepted for RELEASE command.")
        print("Syntax Analysis Complete. No structural errors.\n")

    else:
        print("[PARSER] FATAL ERROR: Unknown statement structure.")
        return

    # SEMANTIC ANALYSIS
    print("--- STARTING SEMANTIC ANALYSIS ---")
    
    if is_assignment:
        print("[SEMANTICS] Checking Type Compatibility...")
        var_type = tokens[0][1]
        var_name = tokens[1][1]
        var_value = tokens[3][1]
        literal_type = tokens[3][0]

        print(f"[SEMANTICS] Variable '{var_name}' is declared as '{var_type}'. Value is '{var_value}'.")

        is_valid_type = False
        if var_type == "OUNT" and literal_type == "LITERAL_INT":
            is_valid_type = True
        elif var_type == "YEARN" and literal_type == "LITERAL_STRING":
            is_valid_type = True
        elif var_type == "HERO" and literal_type == "LITERAL_CHAR":
            is_valid_type = True
        elif var_type == "TAMARAW" and literal_type == "LITERAL_BOOL":
            is_valid_type = True

        if is_valid_type:
            print("[SEMANTICS] Types match. No coercion needed.")
            symbol_table[var_name] = {"type": var_type, "value": var_value}
            print(f"[SEMANTICS] Binding variable '{var_name}' to Symbol Table.")
        else:
            print(f"[SEMANTICS] FATAL ERROR: Variable '{var_name}' is declared as '{var_type}', but value is a different type.")
            print("[SEMANTICS] Recovery Strategy: Compiler will discard assignment.")
            
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
            elif tok_type == "COMMA":
                pass
                
        print("\n=== PROGRAM OUTPUT ===")
        print(output_string)
        print("======================\n")

    print("Semantic Analysis Complete.\n")
    print("-" * 50)

# GUI AREAS

class RedirectText(object):
    """Utility class to redirect print() statements to the GUI text box."""
    def __init__(self, text_ctrl):
        self.output = text_ctrl
    def write(self, string):
        self.output.insert(tk.END, string)
        self.output.see(tk.END)
    def flush(self):
        pass

def clear_console():
    console_output.delete("1.0", tk.END)
    global symbol_table
    symbol_table.clear()

def execute_code():
    global symbol_table
    symbol_table.clear()
    
    code = code_input.get("1.0", tk.END).strip()
    
    if code.lower() == "clear":
        clear_console()
        code_input.delete("1.0", tk.END)
        return

    if code:
        lines = [line.strip() for line in code.split('\n') if line.strip()]
        for line in lines:
            lgf_compiler(line)
            

# MAIN
root = tk.Tk()
root.title("LGF Compiler IDE")
root.geometry("900x600")
root.configure(bg="#1e1e1e")

bg_color = "#1e1e1e"
fg_color = "#d4d4d4"
accent_color = "#007acc"
font_main = ("Consolas", 11)

left_frame = tk.Frame(root, bg=bg_color, width=300)
left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

right_frame = tk.Frame(root, bg=bg_color)
right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

# --- NEW GAMIFICATION UI ---

# 1. The Coin Tracker & Gacha Button
stat_frame = tk.Frame(left_frame, bg=bg_color)
stat_frame.pack(fill=tk.X, pady=(0, 10))

lbl_coins = tk.Label(stat_frame, text=f"🪙 LGF Coins: {lgf_coins}", bg=bg_color, fg="#ffd700", font=("Consolas", 14, "bold"))
lbl_coins.pack(side=tk.LEFT)

btn_gacha = tk.Button(stat_frame, text="🎁 Gacha Pull", bg="#8a2be2", fg="white", font=("Consolas", 10, "bold"), relief="flat")
btn_gacha.pack(side=tk.RIGHT)

# 2. The Quest Board
lbl_quest_title = tk.Label(left_frame, text="📜 ACTIVE QUEST", bg=bg_color, fg="#4af626", font=("Consolas", 14, "bold"))
lbl_quest_title.pack(anchor="w", pady=(10, 0))

lbl_quest_desc = tk.Label(left_frame, text=quests[current_quest_index]["task"], bg=bg_color, fg="white", font=("Consolas", 10), wraplength=280, justify="left")
lbl_quest_desc.pack(anchor="w", pady=(0, 20))

# --- END GAMIFICATION UI ---

lbl_cheat = tk.Label(left_frame, text="LGF CHEAT SHEET", bg=bg_color, fg=accent_color, font=("Consolas", 14, "bold"))
lbl_cheat.pack(anchor="w", pady=(0, 10))

cheat_text = """DATA TYPES:
• OUNT: Integer
• HERO: Char ('A')
• TAMARAW: Bool (True/False)
• YEARN: String ("Text")

OPERATORS:
• IS: Assignment (=)
• :>: Delimiter (;)

I/O COMMANDS:
• RELEASE: Print data
• EndThat: Line break

GRAMMAR RULES:
1. Declaration:
[Type] [Name] IS [Value] :>
Ex: OUNT age IS 20 :>

2. Output:
RELEASE [Name/Value], EndThat :>
Ex: RELEASE age, EndThat :>"""

cheat_box = tk.Text(left_frame, height=25, width=30, bg="#252526", fg="#9cdcfe", font=("Consolas", 10), bd=0, padx=10, pady=10)
cheat_box.insert(tk.END, cheat_text)
cheat_box.config(state=tk.DISABLED)
cheat_box.pack()

lbl_input = tk.Label(right_frame, text="CODE EDITOR", bg=bg_color, fg=accent_color, font=("Consolas", 12, "bold"))
lbl_input.pack(anchor="w")

code_input = tk.Text(right_frame, height=5, bg="#1e1e1e", fg="#ce9178", font=font_main, insertbackground="white", bd=1, relief="solid")
code_input.pack(fill=tk.X, pady=(0, 10))

btn_frame = tk.Frame(right_frame, bg=bg_color)
btn_frame.pack(fill=tk.X, pady=(0, 10))

btn_run = tk.Button(btn_frame, text="▶ RUN CODE", bg=accent_color, fg="white", font=("Consolas", 10, "bold"), command=execute_code, relief="flat", padx=10)
btn_run.pack(side=tk.LEFT, padx=(0, 10))

btn_clear = tk.Button(btn_frame, text="CLEAR CONSOLE", bg="#555555", fg="white", font=("Consolas", 10, "bold"), command=clear_console, relief="flat", padx=10)
btn_clear.pack(side=tk.LEFT)

lbl_output = tk.Label(right_frame, text="COMPILER CONSOLE", bg=bg_color, fg=accent_color, font=("Consolas", 12, "bold"))
lbl_output.pack(anchor="w")

console_output = scrolledtext.ScrolledText(right_frame, height=15, bg="#000000", fg="#4af626", font=font_main, bd=0, padx=10, pady=10)
console_output.pack(fill=tk.BOTH, expand=True)

sys.stdout = RedirectText(console_output)

print("LGF Compiler Initialized. Waiting for code...\n")

root.mainloop()