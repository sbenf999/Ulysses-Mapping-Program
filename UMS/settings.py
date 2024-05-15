import customtkinter
import os
import sqlite3
from tkintermapview import TkinterMapView
import tkinter
import glob

customtkinter.set_default_color_theme("dark-blue")

class Settings(customtkinter.CTk):
    
    APP_NAME = "Uylesses Mapping System - Settings"
    WIDTH = 500
    HEIGHT = 290
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title(Settings.APP_NAME)
        self.geometry(str(Settings.WIDTH) + "x" + str(Settings.HEIGHT))
        self.minsize(Settings.WIDTH, Settings.HEIGHT)

        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.bind("<Shift-q>", self.on_closing)
        self.bind("<Command-w>", self.on_closing)
        self.createcommand('tk::mac::Quit', self.on_closing)
        self.after(201, lambda :self.iconbitmap('Icons/settings.ico'))
        
        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Settings", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.version_number = customtkinter.CTkLabel(self.sidebar_frame, text="v0.2.1-24", font=customtkinter.CTkFont(size=10))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 0))
        self.version_number.grid(row=1, column=0, padx=20, pady=(0, 10))
        self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame, command=self.on_closing, text="Close & save")
        self.sidebar_button_1.grid(row=2, column=0, padx=20, pady=10)
        self.sidebar_button_2 = customtkinter.CTkButton(self.sidebar_frame, command=self.offline_tile_daemon, text="Offline tile daemon")
        self.sidebar_button_2.grid(row=3, column=0, padx=20, pady=10)

        # create tabview
        self.tabview = customtkinter.CTkTabview(self, width=250)
        self.tabview.grid(row=0, column=2, padx=(5, 8), pady=(10, 5), sticky="nsew")
        self.tabview.add("Default database")
        self.tabview.add("Select default marker overlay")
        self.tabview.tab("Default database").grid_columnconfigure(0, weight=1)  # configure grid of individual tabs
        self.tabview.tab("Select default marker overlay").grid_columnconfigure(0, weight=1)
        
        def check_offline_db():
            offline_db_ls = []
            files = glob.glob('./*.db')
            for file in files:
                file = file[2:]
                if file[len(file)-4] != "M":
                    offline_db_ls.append(file)
                    
            return offline_db_ls
                
            
        self.optionmenu_1 = customtkinter.CTkOptionMenu(self.tabview.tab("Default database"), dynamic_resizing=False,
                                                        values=check_offline_db())
        self.optionmenu_1.grid(row=0, column=0, padx=20, pady=(20, 10))
        print(self.optionmenu_1.get())

        self.string_input_button = customtkinter.CTkButton(self.tabview.tab("Default database"), text="Specify database path",
                                                           command=self.open_input_dialog_event)
        self.string_input_button.grid(row=2, column=0, padx=20, pady=(10, 10))
        
        self.label_tab_2 = customtkinter.CTkLabel(self.tabview.tab("Select default marker overlay"), text="CTkLabel on Tab 2")
        self.label_tab_2.grid(row=0, column=0, padx=20, pady=20)

#         # create scrollable frame
#         self.scrollable_frame = customtkinter.CTkScrollableFrame(self, label_text="CTkScrollableFrame")
#         self.scrollable_frame.grid(row=1, column=2, padx=(20, 0), pady=(20, 0), sticky="nsew")
#         self.scrollable_frame.grid_columnconfigure(0, weight=1)
#         self.scrollable_frame_switches = []
#         for i in range(100):
#             switch = customtkinter.CTkSwitch(master=self.scrollable_frame, text=f"CTkSwitch {i}")
#             switch.grid(row=i, column=0, padx=10, pady=(0, 20))
#             self.scrollable_frame_switches.append(switch)
# 
#         # set default values
#         self.scrollable_frame_switches[0].select()
#         self.scrollable_frame_switches[4].select()
#         self.appearance_mode_optionemenu.set("Dark")
#         self.scaling_optionemenu.set("100%")
#         self.optionmenu_1.set("CTkOptionmenu")
#         self.combobox_1.set("CTkComboBox")


    def offline_tile_daemon(self):
        pass

    def open_input_dialog_event(self):
        dialog = customtkinter.CTkInputDialog(text="Type path:", title="Specify database path")
        dialog.after(201, lambda :dialog.iconbitmap('settings.ico'))
        print("DB Path:", dialog.get_input())

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def sidebar_button_event(self):
        print("sidebar_button click")
        
    def on_closing(self, event=0):
        self.destroy()

if __name__ == "__main__":
    app = Settings()
    app.mainloop()