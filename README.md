# LGF Compiler IDE: Gamified Edition

A custom programming language compiler and Integrated Development Environment (IDE) built entirely in Python. 

The LGF Compiler performs real-time **Lexical**, **Syntax**, and **Semantic Analysis** to tokenize code, enforce strict grammatical rules, and ensure type safety. 

To make learning the custom syntax engaging, this IDE features built-in **RPG mechanics**. Users can track active learning quests, earn "LGF Coins" for writing bug-free code, and eventually spend them in a Gacha-style storefront.

## Tech Stack
* **Language:** Python 3
* **GUI Framework:** Tkinter
* **Core Concepts:** Tokenization, Abstract Syntax Parsing, Symbol Tables, Gamification / State Management

---

## Gamification Features

* **Active Quest Board:** A built-in tutorial system that assigns coding missions (e.g., "Declare an OUNT variable").
* **LGF Coin Economy:** A state tracker for user currency, laying the groundwork for rewarding successful compilation.
* **Gacha System (WIP):** A storefront allowing users to spend earned coins on cosmetic IDE unlocks.

---

## The LGF Language Architecture

The LGF language uses a custom syntax with strict typing and delimiter rules.

### Data Types
| Keyword | Standard Equivalent |
| :--- | :--- |
| `OUNT` | Integer |
| `HERO` | Character |
| `TAMARAW` | Boolean |
| `YEARN` | String |

### Operators & Delimiters
* `IS` : Assignment Operator (equivalent to `=`)
* `:>` : End-of-Statement Delimiter (equivalent to `;`)
* `,` : Item Separator

### I/O Commands
* `RELEASE` : Standard Output (Print command)
* `EndThat` : Newline Manipulator

---

## Compilation Phases

When code is executed in the IDE, the compiler processes it through three distinct phases:

### 1. Lexical Analysis (Scanner)
The compiler breaks down the raw string input into a stream of categorized tokens. It identifies literals, commands, and delimiters, flagging them for the parser.

### 2. Syntax Analysis (Parser)
The parser validates the token sequence against strict grammatical rules. 
* **Variable Declarations** must follow: `[Type] [Name] IS [Value] :>`
* If the structure is out of order, a fatal parsing error is thrown.

### 3. Semantic Analysis (Type Checker)
The compiler enforces strict type safety by cross-referencing the declared `DATATYPE` with the actual `LITERAL` provided. Valid variables are bound to the **Symbol Table** in memory.

---