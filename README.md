## LGF Compiler OS

**A Gamified, Retro-Arcade Development Environment and Custom Language Compiler**

LGF Compiler OS is a fully functional, gamified IDE built in Python. It features a custom-built compiler pipeline (Lexical, Syntax, and Semantic analysis) designed to parse and execute the proprietary **LGF Syntax**. Wrapped in a cinematic, 8-bit retro arcade aesthetic, the client turns programming into a game where developers complete coding missions to earn currency, roll for cosmetic themes in a Gacha Marketplace, and rank up their skills.

##  Core Features

* **Custom Compiler Engine:** A ground-up parser that processes the LGF syntax, strictly enforcing data types, grammar rules, and semantic logic before execution.
* **Gamified Mission System:** A dynamic quest engine that scales in difficulty. Traverse through 4 tiers of complexity (Easy, Medium, Hard, and EXTREME) to earn coins. 
* **The Marketplace (Gacha Economy):** Spend hard-earned coins to pull for IDE skins. Features a weighted RNG system with Normal (9.1%), Epic (3%), and Legendary (1%) drop rates. 
* **Cinematic Retro UI:** Built with pure Tkinter but engineered to feel like a high-end arcade cabinet. Features 3D extruded geometry, tactile hover states, live syntax highlighting, and a CRT-style typewriter terminal effect.
* **Persistent Progression:** A local JSON save state architecture that permanently tracks your coin vault, unlocked inventory, and equipped themes across sessions.

## The LGF Syntax (Documentation)

The LGF language is strictly typed and requires precise grammar. 

### Data Types
* `OUNT` : Integer values (e.g., `100`)
* `YEARN` : String values (must be enclosed in double quotes, e.g., `"Gilberto"`)
* `HERO` : Single Character (must be enclosed in single quotes, e.g., `'A'`)
* `TAMARAW` : Boolean values (`True` or `False`)

### Operators & I/O
* `IS` : Assignment Operator (Functions as `=`)
* `:>` : Statement Delimiter (Functions as `;` and is required at the end of lines)
* `RELEASE` : Output Command (Functions as `print`)
* `EndThat` : Newline Command (Functions as `\n`)

### Example Program
```text
OUNT age IS 21 :>
YEARN name IS "Software Engineer" :>
RELEASE name, EndThat :>
```

##  Developer Tools & Hotkeys

For testing and debugging purposes, the OS includes built-in backdoor overrides:
* `[ F9 ]` **Inject Funds:** Instantly adds 99,999 Coins to the Vault for testing Gacha economy rates.
* `[ F10 ]` **Wipe Data:** Completely erases the local `lgf_save_data.json`, resetting the account to standard progression.
* `[ F11 ]` **Wardrobe Override:** Instantly unlocks all standard, Epic, and Legendary skins (including *FEU TECH ACM*, *GILBERTO GREEN*, and *FEU TAMARAWS*) directly into the Vault.


---
**Developed by Lorenzo Gilbert Flores** *BS Computer Science, Specialization in Software Engineering*
```