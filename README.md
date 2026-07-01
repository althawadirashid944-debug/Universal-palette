# Universal Palette

A lightweight Linux utility for launching a customizable command palette with configurable settings.

---

##  Features

- Fast command palette launcher
- Configurable via `config.toml`
- Lightweight and minimal design
- Easy integration with any Linux desktop environment
- Works without requiring a specific window manager

---

## Projects structure
Universal palette/
├── main.py
├── config.toml
├── README.md 

---
## Note 
The keybind for this tool is set through your settings not the config the config is mainly for customisation.
KEYBINDS should be handled  by your window manager or desktop environment NOT the config.
Extra things :
Project is in early development, but it is quite stable for now. Config format may change over time , YOUR contributions and  feedback ARE very welcome.

## CONFIGURATION EXAMPLE
[ui]
theme= "dark"
[search]
fuzzy=true
history=true



{screenshots will be provided as image files feel free to check them out in the project folder]

## DEPENDENCIES
It uses rapidfuzz
so to install: python -m pip install rapidfuzz  OR python3 -m pip install rapidfuzz
and tomllib so : python -m pip install tomllib OR python3 -m pip install tomllib

