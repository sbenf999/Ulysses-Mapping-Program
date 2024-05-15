import customtkinter
from tkintermapview import TkinterMapView
from database_handler import Handler
from settings import *

import os

customtkinter.set_default_color_theme("dark-blue")

try:
    import httplib  # python < 3.0
except:
    import http.client as httplib

def have_internet() -> bool:
    conn = httplib.HTTPSConnection("8.8.8.8", timeout=5)
    try:
        conn.request("HEAD", "/")
        return True
    except Exception:
        return False
    finally:
        conn.close()

class App(customtkinter.CTk):

    APP_NAME = "Ulysses Mapping System"
    WIDTH = 600
    HEIGHT = 340

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title(App.APP_NAME)
        self.geometry(str(App.WIDTH) + "x" + str(App.HEIGHT))
        self.minsize(App.WIDTH, App.HEIGHT)

        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.bind("<Shift-q>", self.on_closing)
        self.bind("<Command-w>", self.on_closing)
        self.createcommand('tk::mac::Quit', self.on_closing)
        self.after(201, lambda :self.iconbitmap('Icons/logo.ico'))
        
        self.marker_list = []

        # ============ create two CTkFrames ============

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.frame_left = customtkinter.CTkFrame(master=self, width=150, corner_radius=0, fg_color=None)
        self.frame_left.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")

        self.frame_right = customtkinter.CTkFrame(master=self, corner_radius=0)
        self.frame_right.grid(row=0, column=1, rowspan=1, pady=0, padx=0, sticky="nsew")

        # ============ frame_left ============
        
            
        self.menu_setup()

        # ============ frame_right ============

        self.frame_right.grid_rowconfigure(1, weight=1)
        self.frame_right.grid_rowconfigure(0, weight=0)
        self.frame_right.grid_columnconfigure(0, weight=1)
        self.frame_right.grid_columnconfigure(1, weight=0)
        self.frame_right.grid_columnconfigure(2, weight=1)

        self.map_widget = TkinterMapView(self.frame_right, corner_radius=0)
        self.map_widget.grid(row=1, rowspan=1, column=0, columnspan=3, sticky="nswe", padx=(0, 0), pady=(0, 0))

        #default values
        if have_internet():
            self.map_widget.set_position(52.51684718010206, 1.0062599873536904, marker=False)
            self.map_widget.set_zoom(9)
            self.map_option_menu.set("OpenStreetMap")
            
            Handler.create_database()
            for longitude, latitude, name in Handler.load_locations():
                new_marker = self.map_widget.set_marker(longitude, latitude, text=name)
        
        else:
            # path for the database to use
            script_directory = os.path.dirname(os.path.abspath(__file__))
            try:
                database_path = os.path.join(script_directory, "Offline/offline_tiles.db")

                # create map widget and only use the tiles from the database, not the online server (use_database_only=True)
                self.map_widget = TkinterMapView(self.frame_right, width=1000, height=700, corner_radius=0, use_database_only=True,
                                            max_zoom=18, database_path=database_path)
                self.map_widget.grid(row=1, rowspan=1, column=0, columnspan=3, sticky="nswe", padx=(0, 0), pady=(0, 0))
                self.map_widget.set_tile_server("https://a.tile.openstreetmap.org/{z}/{x}/{y}.png")
                self.map_widget.set_position(52.51684718010206, 1.0062599873536904, marker=False)
                self.map_widget.set_zoom(9)
                self.map_widget.add_right_click_menu_command(label="Add Marker",
                                                    command=self.add_marker_event,
                                                    pass_coords=True)
                
                self.button_3.destroy()
                
                self.button_4 = customtkinter.CTkButton(master=self.frame_left,
                                                        text="Use online maps",
                                                        command=self.open_online)
                self.button_4.grid(pady=(20, 0), padx=(5, 5), row=0, column=0)
                
                if not have_internet():
                    self.button_4.configure(state="disabled", text="Use online maps")

            except Exception as e:
                self.map_label_offline_on = customtkinter.CTkLabel(self.frame_left, text="Error: No DB", anchor="w")
                self.map_label_offline_on.grid(row=1, column=0, padx=(20, 20), pady=(20, 0))
            
        
        self.map_widget.add_right_click_menu_command(label="Add Marker",
                                                command=self.add_marker_event,
                                                pass_coords=True)
                
    def menu_setup(self):
        self.frame_left.grid_rowconfigure(2, weight=1)
        
        self.logo_label = customtkinter.CTkLabel(self.frame_left, text="U.M.S +", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.version_number = customtkinter.CTkLabel(self.frame_left, text="v0.2.1-24", font=customtkinter.CTkFont(size=10))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 0))
        self.version_number.grid(row=1, column=0, padx=20, pady=(0, 10))
        
        self.button_3 = customtkinter.CTkButton(master=self.frame_left,
                                                text="Open offline database",
                                                command=self.open_offline_db)
        self.button_3.grid(pady=10, padx=20, row=2, column=0)
        
        self.button_5 = customtkinter.CTkButton(master=self.frame_left,
                                                text="Settings", command=self.open_settings)
        self.button_5.grid(pady=(5, 10), padx=(5, 5), row=3, column=0)

        self.map_label = customtkinter.CTkLabel(self.frame_left, text="Tile Server & Appearance:", anchor="w")
        self.map_label.grid(row=4, column=0, padx=(5, 5), pady=(20, 0))
        self.map_option_menu = customtkinter.CTkOptionMenu(self.frame_left, values=["OpenStreetMap", "Satellite imagery"],
                                                                       command=self.change_map)
        self.map_option_menu.grid(row=5, column=0, padx=(2, 2), pady=(10, 20))

#         self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.frame_left, values=["Light", "Dark", "System"],
#                                                                        command=self.change_appearance_mode)
#         self.appearance_mode_optionemenu.grid(row=6, column=0, padx=(5, 5), pady=(10, 20))

        self.change_appearance_mode("Dark")
    
    def open_settings(self):
        settings_window = Settings()
        settings_window.mainloop()
        
    def add_marker_event(self, coords):
        print("Add marker:", coords)
        self.entry = customtkinter.CTkEntry(master=self.frame_right,
                                            placeholder_text="Marker name...")
        self.entry.grid(row=0, column=0, sticky="we", padx=(12, 0), pady=12)
        
        def map_marker_label_setter():
            new_marker = self.map_widget.set_marker(coords[0], coords[1], text=self.entry.get())
            Handler.create_database()
            Handler.add_location(coords[0], coords[1], self.entry.get())
            self.entry.destroy()
            self.button_5.destroy()
        
        self.button_5 = customtkinter.CTkButton(master=self.frame_right,
                                                text="Set",
                                                width=90,
                                                command=map_marker_label_setter)
        self.button_5.grid(row=0, column=1, sticky="w", padx=(12, 0), pady=12)

        

    def set_marker_event(self):
        current_position = self.map_widget.get_position()
        self.marker_list.append(self.map_widget.set_marker(current_position[0], current_position[1]))
    
    def open_online(self):
        self.button_3.destroy()
        self.button_4.destroy()
        self.menu_setup()
        self.button_3 = customtkinter.CTkButton(master=self.frame_left,
                                                text="Open offline database",
                                                command=self.open_offline_db)
        self.button_3.grid(pady=10, padx=20, row=2, column=0)
        self.map_widget = TkinterMapView(self.frame_right, corner_radius=0)
        self.map_widget.grid(row=1, rowspan=1, column=0, columnspan=3, sticky="nswe", padx=(0, 0), pady=(0, 0))
        self.map_widget.set_position(52.51684718010206, 1.0062599873536904, marker=False)
        self.map_widget.set_zoom(9)
        self.map_option_menu.set("OpenStreetMap")
        self.map_widget.add_right_click_menu_command(label="Add Marker",
                                                command=self.add_marker_event,
                                                pass_coords=True)
        
        for longitude, latitude, name in Handler.load_locations():
            new_marker = self.map_widget.set_marker(longitude, latitude, text=name)
        
    def open_offline_db(self):
        self.button_3.destroy()
        self.menu_setup()
        self.map_widget.add_right_click_menu_command(label="Add Marker",
                                                command=self.add_marker_event,
                                                pass_coords=True)
        # path for the database to use
        script_directory = os.path.dirname(os.path.abspath(__file__))
        try:
            database_path = os.path.join(script_directory, "Offline/offline_tiles.db")

            # create map widget and only use the tiles from the database, not the online server (use_database_only=True)
            self.map_widget = TkinterMapView(self.frame_right, width=1000, height=700, corner_radius=0, use_database_only=True,
                                        max_zoom=16, database_path=database_path)
            self.map_widget.grid(row=1, rowspan=1, column=0, columnspan=3, sticky="nswe", padx=(0, 0), pady=(0, 0))
            self.map_widget.set_tile_server("https://a.tile.openstreetmap.org/{z}/{x}/{y}.png")
            self.map_widget.set_position(52.51684718010206, 1.0062599873536904, marker=False)
            self.map_widget.set_zoom(9)
            self.map_widget.add_right_click_menu_command(label="Add Marker",
                                                command=self.add_marker_event,
                                                pass_coords=True)
            
            self.button_3.destroy()
            
            self.button_4 = customtkinter.CTkButton(master=self.frame_left,
                                                    text="Use online maps",
                                                    command=self.open_online)
            self.button_4.grid(pady=10, padx=20, row=2, column=0)
            
            if not have_internet():
                self.button_4.configure(state="disabled", text="Use online maps")
                
            for longitude, latitude, name in Handler.load_locations():
                new_marker = self.map_widget.set_marker(longitude, latitude, text=name)

        except Exception as e:
            self.map_label_offline_on = customtkinter.CTkLabel(self.frame_left, text="Error: No DB", anchor="w")
            self.map_label_offline_on.grid(row=1, column=0, padx=(20, 20), pady=(20, 0))
            print(e)
        
    def change_appearance_mode(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_map(self, new_map: str):
        if new_map == "OpenStreetMap":
            self.map_widget.set_tile_server("https://a.tile.openstreetmap.org/{z}/{x}/{y}.png")
        elif new_map == "Satellite imagery":
            self.map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=s&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)

    def on_closing(self, event=0):
        self.destroy()

    def start(self):
        self.mainloop()


if __name__ == "__main__":
    app = App()
    app.start()