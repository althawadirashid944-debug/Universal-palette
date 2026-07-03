#!/usr/bin/env python3

import os
import sys
import atexit

LOCK_FILE = "/tmp/universal_palette.lock"

def cleanup():
    if os.path.exists(LOCK_FILE):
        os.remove(LOCK_FILE)

atexit.register(cleanup)

if os.path.exists(LOCK_FILE):
    print("Already running")
    sys.exit()

open(LOCK_FILE, "w").close() 
from pathlib import Path
import tomllib

config_path = Path(__file__).parent / "config.toml"

with open(config_path, "rb") as f:
    config = tomllib.load(f)

print(config) 



import gi
import subprocess 
import webbrowser
import urllib.parse 
from rapidfuzz import process, fuzz 


gi.require_version("Gtk", "4.0")
from gi.repository import Gtk


class PaletteWindow(Gtk.ApplicationWindow):
    def __init__(self, app):
        super().__init__(application=app)

        self.set_title("Command palette")
        self.set_default_size(600, 80)
        self.set_resizable(False)
        self.set_decorated(False)

        self.entry = Gtk.Entry()
        self.entry.set_placeholder_text("Type a command...")

        self.set_child(self.entry)
        self.entry.connect("activate", self.on_enter)
        
        self.apps = self.load_apps() 
        self.flatpak_apps = {
            k: v for k, v in self.apps.items()
            if isinstance(v, str) and v.startswith("flatpak:") 
        } 
        print([app for app in self.apps.keys() if "fire" in app]) 

    def on_enter(self, entry):
        text = entry.get_text() 
        if not text:
            return 
        self.handle_command(text)
        entry.set_text("") 
        self.hide() 

    def handle_command(self, text):
     text = text.strip()

     if not text:
      return

     # 1. explicit system commands
     if text == "exit":
        self.cmd_exit("")
        return

     if text.startswith("echo "):
        self.cmd_echo(text[5:])
        return

     if text.startswith("file "):
        self.file_search(text[5:])
        return

     # 2. web search shortcut
     if text.startswith("search "):
        self.web_search(text[7:])
        return

     # 3. APP LAUNCH MODE (default)
     app = self.find_app(text)

     if app:
        self.launch(app)
        return 
        

     
     # 4. fallback → web search
     self.web_search(text) 
    def launch(self, app):
     try:
        if not app:
            return

        if isinstance(app, str) and app.startswith("flatpak:"):
            app_id = app.split("flatpak:", 1)[1]
            subprocess.Popen(["flatpak", "run", app_id]) 
            
            return

        subprocess.Popen(app.split())
        print("Opened:", app) 
        

     except Exception as e:
        print("Launch error:", e) 
        self.cmd_exit() 
    def cmd_exit(self, args):
        print("Exiting application...")
        self.get_application().quit()

    def cmd_open(self, args):
     if not args:
        print("No application specified")
        return 
        

     app = args.strip() 
     if self.open_flatpak(args):
        print(f"Flatpak opened: {args}")
        return
        

     try:
        subprocess.Popen(app.split())
        print(f"Opened: {app}")
        return 
        self.cmd_exit() 
     except Exception:
        pass 
        

     try:
        subprocess.Popen(["gtk-launch", app])
        print(f"Opened (gtk-launch): {app}")
        return
     except Exception:
        pass 
        
      
    def load_apps(self):
      apps = {}

      paths = [
        "/usr/share/applications",
        os.path.expanduser("~/.local/share/applications")
     ]

      for path in paths:
         if not os.path.exists(path):
            continue

         for file in os.listdir(path):
            if not file.endswith(".desktop"):
                continue

            full = os.path.join(path, file)

            try:
                with open(full, "r", errors="ignore") as f:
                    lines = f.readlines()

                name = None
                exec_cmd = None
                in_main = False

                for line in lines:
                    line = line.strip()

                    if line == "[Desktop Entry]":
                        in_main = True
                        continue

                    if line.startswith("[") and line != "[Desktop Entry]":
                        in_main = False

                    if not in_main:
                        continue

                    if line.startswith("Name="):
                        name = line.split("=", 1)[1].lower()

                    elif line.startswith("Exec="):
                        exec_line = line.split("=", 1)[1].strip()

                        for token in ["%u", "%U", "%f", "%F", "%i", "%c"]:
                            exec_line = exec_line.replace(token, "")

                        exec_cmd = exec_line.split()[0]

                if name and exec_cmd:
                    clean_name = name
                    clean_name = clean_name.replace("web browser", "")
                    clean_name = clean_name.replace("mozilla", "")
                    clean_name = clean_name.strip()

                    apps[clean_name] = exec_cmd

            except Exception as e:
                print("ERROR:", file, e)


         # Flatpak apps
         try:
               result = subprocess.run(
              ["flatpak", "list", "--app", "--columns=application,name"],
              capture_output=True,
              text=True
             )

               for line in result.stdout.splitlines():
                   parts = line.split("\t") if "\t" in line else line.split()

                   if len(parts) >= 2:
                     app_id = parts[0]
                     name = parts[1].lower()

                     apps[name] = f"flatpak:{app_id}"

         except Exception as e:
                print("Flatpak error:", e)

         return apps

    
    def find_app(self, query):
     
     key = query.lower().strip()
     print("QUERY:", key)
     print("HAS FIREFOX:", "firefox" in self.apps) 

     # 1. exact match first
     if key in self.apps:
        return self.apps[key]

     # 2. Partial matches
     partial=[]
     for name in self.apps:
        if key in name:
            partial.append(name)
        if len(partial) ==1:
            print("PARTIAL MATCH:", partial[0])
            return self.apps[partial[0]]
        if len(partial) > 1:
            print("Multiple partial matches were found", partial)
            return self.apps[partial[0]] 
     # Fuzzy fallback this fella hella weird
     matches = process.extract(
        key,
        self.apps.keys(),
        scorer=fuzz.ratio,
        limit=1
     )
     
    
     
        

     
    def cmd_echo(self, args):
        print(args)

    def file_search(self, args):
        if not args:
            print("No search query provided.")
            return 
            

        matches = []

        for root, dirs, files in os.walk("/home"):
            for f in files:
                if args.lower() in f.lower():
                    matches.append(os.path.join(root, f))
                    if len(matches) >= 20:
                        break
            if len(matches) >= 20:
                break

        print("\n".join(matches))
    def web_search(self, args):
        if not args:
            print("No search query provided.")
            return
            

        query = urllib.parse.quote(args) 
        url = f"https://www.google.com/search?q={query}"

        try:
            subprocess.Popen(["xdg-open", url])
            print(f"Opened web search for: {args}") 
            
        except Exception as e:
            print(f"Failed to open web search: {e}") 
            



class App(Gtk.Application):
    def __init__(self):
        super().__init__(application_id="com.example.palette")

    def do_activate(self):
        window = PaletteWindow(self)
        window.present()
    def do_shutdown(self):
    

     if os.path.exists(LOCK_FILE):
        os.remove(LOCK_FILE)

     Gtk.Application.do_shutdown(self) 
if __name__ == "__main__":
    app = App()
    app.run()  