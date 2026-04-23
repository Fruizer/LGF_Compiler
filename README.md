# LGF Compiler OS

**A Gamified, Retro-Arcade Development Environment and Custom Language Compiler**

LGF Compiler OS is a fully functional, gamified IDE built in Python. It features a custom-built compiler pipeline (Lexical, Syntax, and Semantic analysis) designed to parse and execute the proprietary **LGF Syntax**. 

Wrapped in a cinematic, 8-bit retro arcade aesthetic, the client turns programming into a game where developers complete coding missions to earn currency, rank up from *Code Freshman* to *The Gilberto*, roll for cosmetic themes in a Gacha Marketplace, and visualize their logic via an Abstract Syntax Tree (AST) generator.

## Core Features

* **Custom Compiler Engine & AST Visualizer:** A ground-up parser that processes the LGF syntax, strictly enforcing data types, grammar rules, and semantic logic. Successfully compiled scripts can be viewed as an interactive, dynamically generated Abstract Syntax Tree (AST) logic graph.
* **Gamified Mission & Rank System:** A dynamic quest engine that scales in difficulty (Easy to EXTREME). Earn EXP to rank up through 6 tiers of developer status.
* **The Marketplace (Gacha Economy):** Spend hard-earned coins to pull for IDE skins, featuring aesthetic nods to tactical shooters and university organizations. Features a weighted RNG system with Normal, Epic, and Legendary drop rates. 
* **Cinematic Retro UI & Audio Engine:** Built natively with Tkinter and powered by `pygame-ce` for audio. Features 3D extruded geometry, live syntax highlighting, a CRT-style typewriter terminal effect, and seamless 8-bit sound design.
* **Persistent Progression:** A local JSON save state architecture that permanently tracks your coin vault, EXP, unlocked inventory, and equipped themes across sessions.


### Data Types
* `OUNT` : Integer values (e.g., `100`)
* `YEARN` : String values (must be enclosed in double quotes, e.g., `"Gilberto"`)
* `HERO` : Single Character (must be enclosed in single quotes, e.g., `'A'`)
* `TAMARAW` : Boolean values (`True` or `False`)

### Operators & I/O
* `IS` : Assignment Operator (Functions as `=`)
* `:>` : Statement Delimiter (Functions as `;` and is required at the end of lines)
* `RELEASE` : Output Command (Functions as `print`)
* `EndThat` : Line Break Command (Functions as `\n`)

### Example Program
```text
OUNT age IS 21 :>
YEARN name IS "Software Engineer" :>
RELEASE name, EndThat :>