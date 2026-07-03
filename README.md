# Universal Palette

A lightweight Linux utility for launching a customizable command palette with configurable settings.
[ Theres a image.png file in the folder if you want to check it out ] 

---

##  Features

- Fast command palette launcher
- Configurable via `config.toml`
- Lightweight and minimal design
- Easy integration with any Linux desktop environment
- Works without requiring a specific window manager
- You can also use web search : Type a question hit enter your default browser opens with that question , neat right? 

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


## KEYBINDING
If you use hyprland or similar go into your config file and type: for example 
```ini
bind = SUPER, M, exec, python3 ~/path-or-folder-youdownloaded-it-in/Universal palette/main.py
# THE FOLDER USES A SPACE so Universal palette 

```
## CONFIGURATION EXAMPLE
[ui]
theme= "dark"
[search]
fuzzy=true
history=true



{screenshots will be provided as image files feel free to check them out in the project folder]

## DEPENDENCIES
It uses rapidfuzz and tomllib
install rapidfuzz : Sudo pacman -S python-rapidfuzz 
IF you are on python 3.11+ you already have tomllib if not then install via : sudo pacman -S python-tomli



