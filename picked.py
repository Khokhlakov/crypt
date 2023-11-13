import tkinter as tk
from tkinter import ttk
import tkinter.messagebox
import customtkinter
import imageio.v3 as iio
import numpy as np

# Imports sistemas criptograficos
from Desplazamiento import Desplazamiento
from Multiplicativo import Multiplicativo
from Afin import Afin
from Hill import Hill

from tkinter import PhotoImage

# Change image format (tkinter only receives .ppm)
from PIL import Image

# File explorer
from tkinter import filedialog

import sys
import os
#To use with pyinstaller
# determine if application is a script file or frozen exe
if getattr(sys, 'frozen', False):
    application_path = os.path.dirname(sys._MEIPASS)
elif __file__:
    application_path = os.path.dirname(__file__)

bundle_dir = os.path.abspath(os.path.dirname(__file__))
path_to_dat = os.path.join(bundle_dir, 'livai.ppm')

config_path = os.path.join(application_path, "livai.ppm")


customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


LARGEFONT =("Verdana", 35)
dice_image = customtkinter.CTkImage(Image.open("dice.png"), size=(18, 18))
larrow_image = customtkinter.CTkImage(Image.open("larrow.png"), size=(18, 18))


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        """
        

        ### Start img mngmnt
        # create main entry and button
        label_file_explorer = customtkinter.CTkLabel(self, 
                            text = "File Explorer using Tkinter",
                            width = 100, height = 4)
        

        imgName = ""
        def browseFiles():
            imgName = filedialog.askopenfilename(initialdir = "/",
                                                title = "Select a File",
                                                filetypes = (("Picture files",
                                                                "*.png;*.jpg;*.ppm;*.bmp"),
                                                            ('All files', '*.*')))
            imgList = imgName.split(".")
            if imgList[1] != "ppm":
                anyFormatImage = Image.open(imgName)
                imgName = imgList[0]+".ppm"
                anyFormatImage.save(imgName)


            # Change label contents
            label_file_explorer.configure(text="File Opened: "+imgName)
            print(imgName)
            imgPrueba = PhotoImage(file=imgName)

            testImg.configure(image=imgPrueba)
            testImg.image = imgPrueba

        
        button_explore = customtkinter.CTkButton(self, 
                                text = "Browse Files",
                                command = browseFiles) 

        label_file_explorer.grid(column = 4, row = 0)
        
        button_explore.grid(column = 4, row = 1)

        testImg = customtkinter.CTkLabel(self)
        
        testImg.grid(column = 4,row = 2)
        ### End img mngmnt


        self.entry = customtkinter.CTkEntry(self, placeholder_text="CTkEntry")
        self.entry.grid(row=3, column=1, columnspan=2, padx=(20, 0), pady=(20, 20), sticky="nsew")

        self.main_button_1 = customtkinter.CTkButton(master=self, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"))
        self.main_button_1.grid(row=3, column=3, padx=(20, 20), pady=(20, 20), sticky="nsew")

        # create textbox
        self.textbox = customtkinter.CTkTextbox(self, width=250)
        self.textbox.grid(row=0, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")

        # create tabview
        self.tabview = customtkinter.CTkTabview(self, width=250)
        self.tabview.grid(row=0, column=2, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.tabview.add("CTkTabview")
        self.tabview.add("Tab 2")
        self.tabview.add("Tab 3")
        self.tabview.tab("CTkTabview").grid_columnconfigure(0, weight=1)  # configure grid of individual tabs
        self.tabview.tab("Tab 2").grid_columnconfigure(0, weight=1)

        # Test

        #if '_MEIPASS2' in os.environ:
        #    filename = os.path.join(os.environ['_MEIPASS2'], filename)

        imgg = PhotoImage(file=path_to_dat)
        print("asd")
        print(config_path) 
        print(path_to_dat)   

        #test = ImageTk.PhotoImage(Image.open("livai.png"))
        #label1 = tk.Label(self.tabview.tab("CTkTabview"), image=test)
        label1 = tk.Label(self.tabview.tab("CTkTabview"), image=imgg)
        #label1.image = test
        label1.image = imgg
        label1.place(x=0, y=0)

        self.optionmenu_1 = customtkinter.CTkOptionMenu(self.tabview.tab("CTkTabview"), dynamic_resizing=False,
                                                        values=["Value 1", "Value 2", "Value Long Long Long"])
        self.optionmenu_1.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.combobox_1 = customtkinter.CTkComboBox(self.tabview.tab("CTkTabview"),
                                                    values=["Value 1", "Value 2", "Value Long....."])
        self.combobox_1.grid(row=1, column=0, padx=20, pady=(10, 10))
        self.string_input_button = customtkinter.CTkButton(self.tabview.tab("CTkTabview"), text="Open CTkInputDialog",
                                                           command=self.open_input_dialog_event)
        self.string_input_button.grid(row=2, column=0, padx=20, pady=(10, 10))
        self.label_tab_2 = customtkinter.CTkLabel(self.tabview.tab("Tab 2"), text="CTkLabel on Tab 2")
        self.label_tab_2.grid(row=0, column=0, padx=20, pady=20)

        # create radiobutton frame
        self.radiobutton_frame = customtkinter.CTkFrame(self)
        self.radiobutton_frame.grid(row=0, column=3, padx=(20, 20), pady=(20, 0), sticky="nsew")
        self.radio_var = tk.IntVar(value=0)
        self.label_radio_group = customtkinter.CTkLabel(master=self.radiobutton_frame, text="CTkRadioButton Group:")
        self.label_radio_group.grid(row=0, column=2, columnspan=1, padx=10, pady=10, sticky="")
        self.radio_button_1 = customtkinter.CTkRadioButton(master=self.radiobutton_frame, variable=self.radio_var, value=0)
        self.radio_button_1.grid(row=1, column=2, pady=10, padx=20, sticky="n")
        self.radio_button_2 = customtkinter.CTkRadioButton(master=self.radiobutton_frame, variable=self.radio_var, value=1)
        self.radio_button_2.grid(row=2, column=2, pady=10, padx=20, sticky="n")
        self.radio_button_3 = customtkinter.CTkRadioButton(master=self.radiobutton_frame, variable=self.radio_var, value=2)
        self.radio_button_3.grid(row=3, column=2, pady=10, padx=20, sticky="n")

        # create slider and progressbar frame
        self.slider_progressbar_frame = customtkinter.CTkFrame(self, fg_color="transparent")
        self.slider_progressbar_frame.grid(row=1, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.slider_progressbar_frame.grid_columnconfigure(0, weight=1)
        self.slider_progressbar_frame.grid_rowconfigure(4, weight=1)
        self.seg_button_1 = customtkinter.CTkSegmentedButton(self.slider_progressbar_frame)
        self.seg_button_1.grid(row=0, column=0, padx=(20, 10), pady=(10, 10), sticky="ew")
        self.progressbar_1 = customtkinter.CTkProgressBar(self.slider_progressbar_frame)
        self.progressbar_1.grid(row=1, column=0, padx=(20, 10), pady=(10, 10), sticky="ew")
        self.progressbar_2 = customtkinter.CTkProgressBar(self.slider_progressbar_frame)
        self.progressbar_2.grid(row=2, column=0, padx=(20, 10), pady=(10, 10), sticky="ew")
        self.slider_1 = customtkinter.CTkSlider(self.slider_progressbar_frame, from_=0, to=1, number_of_steps=4)
        self.slider_1.grid(row=3, column=0, padx=(20, 10), pady=(10, 10), sticky="ew")
        self.slider_2 = customtkinter.CTkSlider(self.slider_progressbar_frame, orientation="vertical")
        self.slider_2.grid(row=0, column=1, rowspan=5, padx=(10, 10), pady=(10, 10), sticky="ns")
        self.progressbar_3 = customtkinter.CTkProgressBar(self.slider_progressbar_frame, orientation="vertical")
        self.progressbar_3.grid(row=0, column=2, rowspan=5, padx=(10, 20), pady=(10, 10), sticky="ns")

        # create checkbox and switch frame
        self.checkbox_slider_frame = customtkinter.CTkFrame(self)
        self.checkbox_slider_frame.grid(row=1, column=3, padx=(20, 20), pady=(20, 0), sticky="nsew")
        self.checkbox_1 = customtkinter.CTkCheckBox(master=self.checkbox_slider_frame)
        self.checkbox_1.grid(row=1, column=0, pady=(20, 0), padx=20, sticky="n")
        self.checkbox_2 = customtkinter.CTkCheckBox(master=self.checkbox_slider_frame)
        self.checkbox_2.grid(row=2, column=0, pady=(20, 0), padx=20, sticky="n")
        self.checkbox_3 = customtkinter.CTkCheckBox(master=self.checkbox_slider_frame)
        self.checkbox_3.grid(row=3, column=0, pady=20, padx=20, sticky="n")

        # set default values
        self.sidebar_button_3.configure(state="disabled", text="Disabled CTkButton")
        self.checkbox_3.configure(state="disabled")
        self.checkbox_1.select()
        self.scrollable_frame_switches[0].select()
        self.scrollable_frame_switches[4].select()
        self.radio_button_3.configure(state="disabled")
        self.appearance_mode_optionemenu.set("Dark")
        self.scaling_optionemenu.set("100%")
        self.optionmenu_1.set("CTkOptionmenu")
        self.combobox_1.set("CTkComboBox")
        self.slider_1.configure(command=self.progressbar_2.set)
        self.slider_2.configure(command=self.progressbar_3.set)
        self.progressbar_1.configure(mode="indeterminnate")
        self.progressbar_1.start()
        self.textbox.insert("0.0", "CTkTextbox\n\n" + "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua.\n\n" * 20)
        self.seg_button_1.configure(values=["CTkSegmentedButton", "Value 2", "Value 3"])
        self.seg_button_1.set("Value 2")
        """

        #self.title("CustomTkinter complex_example.py")
        self.geometry(f"{1100}x{580}")
        # New init
        # creating a container
        self.container = customtkinter.CTkFrame(self)
        self.container.pack(side = "top", fill = "both", expand = True)



        # configure grid layout (4x4)
        self.container.grid_columnconfigure(1, weight=1)
        self.container.grid_columnconfigure(2, weight=0)
        self.container.grid_rowconfigure((0, 1, 2), weight=1)

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self.container, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=3, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="CustomTkinter", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame, 
                                                        text ="Home",
                                                        command=lambda: self.show_frame(HomePage))
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)
        
        self.sidebar_button_2 = customtkinter.CTkButton(self.sidebar_frame, command=self.sidebar_button_event)
        self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)
        self.sidebar_button_3 = customtkinter.CTkButton(self.sidebar_frame, command=self.sidebar_button_event)
        self.sidebar_button_3.grid(row=3, column=0, padx=20, pady=10)
        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))
        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"],
                                                               command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20))

        # Set default values
        self.sidebar_button_3.configure(state="disabled", text="Disabled CTkButton")
        #self.scrollable_frame_switches[0].select()
        #self.scrollable_frame_switches[4].select()
        self.appearance_mode_optionemenu.set("Dark")
        self.scaling_optionemenu.set("100%")


        self.scrollable_frame = customtkinter.CTkScrollableFrame(self.container)
        self.scrollable_frame.grid(row = 0, column = 1, rowspan = 3, sticky ="nsew")
        self.scrollable_frame.grid_columnconfigure(0, weight=1)

        #self.container.grid_rowconfigure(0, weight = 1)
        #self.container.grid_columnconfigure(0, weight = 1)

        # initializing frames to an empty array
        self.frames = {}

        # iterating through a tuple consisting
        # of the different page layouts
        for F in (HomePage, AffinePage, HillPage, Page2):

            frame = F(self.scrollable_frame, self)

            # initializing frame of that object from
            # Homepage, page1, page2 respectively with
            # for loop
            self.frames[F] = frame

            frame.grid(row = 0, column = 0, sticky ="nsew")

        self.show_frame(HomePage)

    # to display the current frame passed as
    # parameter
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


    def open_input_dialog_event(self):
        dialog = customtkinter.CTkInputDialog(text="Type in a number:", title="CTkInputDialog")
        print("CTkInputDialog:", dialog.get_input())

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def sidebar_button_event(self):
        print("sidebar_button click")



# first window frame Homepage

class HomePage(customtkinter.CTkFrame):
    def __init__(self, parent, controller):
        customtkinter.CTkFrame.__init__(self, parent)

        self.columnconfigure(0,weight=0)
        self.columnconfigure(1,weight=1)

        # create tabview
        self.tabview = customtkinter.CTkTabview(self, width=250)
        self.tabview.grid(row=0, column=0, padx=(20, 0), pady=(20, 0), rowspan=10, sticky="nsew")
        self.tabview.add("Classical ciphers")
        self.tabview.add("Block ciphers")
        self.tabview.tab("Classical ciphers").grid_columnconfigure(0, weight=1)  # configure grid of individual tabs
        
        self.tabview.tab("Block ciphers").grid_columnconfigure(0, weight=1)

        # Basic ciphers
        affineButton = customtkinter.CTkButton(self.tabview.tab("Classical ciphers"), 
                                               text ="Affine",
                                               command = lambda : controller.show_frame(AffinePage))
        affineButton.grid(row = 0, column = 0, padx = 10, pady = 10)

        hillButton = customtkinter.CTkButton(self.tabview.tab("Classical ciphers"), 
                                             text ="Hill",
                                             command = lambda : controller.show_frame(HillPage))
        hillButton.grid(row = 0, column = 1, padx = 10, pady = 10)

        multiplicativeButton = customtkinter.CTkButton(self.tabview.tab("Classical ciphers"), text ="Multiplicative")
        multiplicativeButton.grid(row = 1, column = 0, padx = 10, pady = 10)
        
        permutationButton = customtkinter.CTkButton(self.tabview.tab("Classical ciphers"), text ="Permutation")
        permutationButton.grid(row = 1, column = 1, padx = 10, pady = 10)

        shiftButton = customtkinter.CTkButton(self.tabview.tab("Classical ciphers"), text ="Shift")
        shiftButton.grid(row = 2, column = 0, padx = 10, pady = 10)
        
        transpositionButton = customtkinter.CTkButton(self.tabview.tab("Classical ciphers"), text ="Transposition")
        transpositionButton.grid(row = 2, column = 1, padx = 10, pady = 10)

        vigenereButton = customtkinter.CTkButton(self.tabview.tab("Classical ciphers"), text ="Vigenere")
        vigenereButton.grid(row = 3, column = 0, padx = 10, pady = 10)
        
        # Block ciphers

        button1 = customtkinter.CTkButton(self.tabview.tab("Block ciphers"), text ="Affine",
        command = lambda : controller.show_frame(AffinePage))
        button1.grid(row = 0, column = 0, padx = 10, pady = 10)

        button2 = customtkinter.CTkButton(self.tabview.tab("Block ciphers"), text ="Page 2",
        command = lambda : controller.show_frame(Page2))
        button2.grid(row = 0, column = 1, padx = 10, pady = 10)

        # Digital signatures
        self.ds_frame = customtkinter.CTkFrame(self)
        self.ds_frame.grid(row = 0, column = 1, rowspan=5, padx=(20, 20), pady=(20, 0), sticky="ew")
        self.ds_frame.grid_columnconfigure(0, weight=1)
        self.ds_frame_label = customtkinter.CTkLabel(self.ds_frame, 
                                                     text="Generate a digital signature",
                                                     corner_radius=6, 
                                                     fg_color=['#979DA2', 'gray29'], 
                                                     text_color=['#DCE4EE', '#DCE4EE'])
        self.ds_frame_label.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="")

        
        button1 = customtkinter.CTkButton(self.ds_frame, text ="Affine",
        command = lambda : controller.show_frame(AffinePage))
        button1.grid(row = 1, column = 0, padx = 10, pady = 10)

        button2 = customtkinter.CTkButton(self.ds_frame, text ="Page 2",
        command = lambda : controller.show_frame(Page2))
        button2.grid(row = 1, column = 1, padx = 10, pady = 10)

        

       

    def open_input_dialog_event(self):
        dialog = customtkinter.CTkInputDialog(text="Type in a number:", title="CTkInputDialog")
        print("CTkInputDialog:", dialog.get_input())

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def sidebar_button_event(self):
        print("sidebar_button click")



# AffinePage window frame
class AffinePage(customtkinter.CTkFrame):
    def __init__(self, parent, controller):
        self.system = Afin()
        self.currentKey = ""

        customtkinter.CTkFrame.__init__(self, parent)

        self.grid_columnconfigure((0,2), weight=1)
        self.grid_columnconfigure(1, weight=0)

        label = customtkinter.CTkLabel(self,
                                       text="Affine Cipher",
                                       font=customtkinter.CTkFont(size=20, weight="bold"))
        label.grid(row=0, column=0, columnspan=3, padx=20, pady=(10,0), sticky="w")

        # input
        self.entry = customtkinter.CTkTextbox(self)
        self.entry.grid(row=1, column=0, rowspan=4, padx=(20, 0), pady=(20, 10), sticky="nsew")
        self.entry.insert("0.0", "Attack at noon")

        self.swapFrame = customtkinter.CTkFrame(self, width=30, height=30, fg_color=self.cget("fg_color")) #their units in pixels
        button3 = customtkinter.CTkButton(self.swapFrame, 
                                          text ="",
                                          image=larrow_image,
                                          command=self.swap)
        self.swapFrame.grid_propagate(False)
        self.swapFrame.columnconfigure(0, weight=1)
        self.swapFrame.rowconfigure(0,weight=1)
        self.swapFrame.grid(row=1, column=1, sticky="n", pady=20)
        button3.grid(sticky="wens")

        button1 = customtkinter.CTkButton(self, text ="Encrypt", command=self.encrypt)
        button1.grid(row = 2, column = 1, padx = 5, pady = 5, sticky="sew")

        button2 = customtkinter.CTkButton(self, text ="Decrypt", command=self.decrypt)
        button2.grid(row = 3, column = 1, padx = 5, pady = 5, sticky="sew")

        
        # output
        self.textbox = customtkinter.CTkTextbox(self, state="disabled")
        self.textbox.grid(row=1, column=2, rowspan=3, padx=(0,20), pady=(20, 0), sticky="nsew")
        self.textbox.insert("0.0", "")
        button1 = customtkinter.CTkButton(self, text ="Copy",
                            command = self.copyToClipboard)
        button1.grid(row = 4, column = 2, padx = (0,20), pady = (0,10), sticky="ew")

        # Key part
        self.keyFrame = customtkinter.CTkFrame(self, fg_color=self.cget("fg_color"))
        self.keyFrame.columnconfigure(0, weight=0)
        self.keyFrame.columnconfigure(1, weight=1)
        self.keyFrame.grid(row = 5, column = 0, columnspan=3, padx=20, pady=20, sticky="ew")
        button1 = customtkinter.CTkButton(self.keyFrame, 
                                          compound="right",
                                          text ="Generate Key      ",
                                          image=dice_image,
                                          command = lambda : controller.show_frame(HomePage))
        button1.grid(row = 0, column = 0, padx = (0,5), pady = 0)

        self.entryKey = customtkinter.CTkEntry(self.keyFrame, placeholder_text="Enter key")
        self.entryKey.grid(row=0, column=1, padx=(5, 0), pady=0, sticky="ew")

        # Analysis
        button2 = customtkinter.CTkButton(self, text ="Analyze",
                            command = lambda : controller.show_frame(Page2))
        button2.grid(row = 6, column = 0, padx = 10, pady = 10)
    
    def encrypt(self):
        inputKey = self.entryKey.get()
        inputText = self.entry.get("0.0", tk.END)

        if inputKey != self.currentKey:
            self.currentKey = inputKey
            self.system.setKey(inputKey)

        cipherText = self.system.encrypt(inputText)
        self.textbox.configure(state="normal")
        self.textbox.delete('1.0', tk.END)
        self.textbox.insert("0.0", cipherText)
        self.textbox.configure(state="disabled")
        
    def decrypt(self):
        inputKey = self.entryKey.get()
        inputText = self.entry.get("0.0", tk.END)

        if inputKey != self.currentKey:
            self.currentKey = inputKey
            self.system.setKey(inputKey)

        cipherText = self.system.decrypt(inputText)
        self.textbox.configure(state="normal")
        self.textbox.delete('0.0', tk.END)
        self.textbox.insert("0.0", cipherText)
        self.textbox.configure(state="disabled")
    
    def copyToClipboard(self):
        self.clipboard_clear()
        self.clipboard_append(self.textbox.get("0.0", tk.END))

    def swap(self):
        self.entry.delete('0.0', tk.END)
        self.entry.insert("0.0", self.textbox.get("0.0", tk.END))


# Hill window frame
class HillPage(customtkinter.CTkFrame):

    def __init__(self, parent, controller):
        self.system = Hill()
        self.keyLen = 5
        self.dirty = False
        self.dirtyOutput = False
        

        customtkinter.CTkFrame.__init__(self, parent)
        self.grid_columnconfigure((0,2), weight=1)
        self.grid_columnconfigure((1,3), weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=0)

        label = customtkinter.CTkLabel(self,
                                       text="Hill Cipher",
                                       font=customtkinter.CTkFont(size=20, weight="bold"))
        label.grid(row=0, column=0, columnspan=3, padx=20, pady=(10,0), sticky="w")

        # input image dir: self.imgName
        ### Start img mngmnt
        self.inputImgFrame = customtkinter.CTkFrame(self)
        self.inputImgFrame.configure(width=300,height=300)
        self.inputImgFrame.grid_propagate(False)
        self.inputImgFrame.columnconfigure(0, weight=1)
        self.inputImgFrame.rowconfigure(0, weight=1)
        self.inputImgFrame.grid(column = 0, row = 1, rowspan=3, padx=(20, 0), pady=0, sticky="nsew")
        self.inputImg = customtkinter.CTkLabel(self.inputImgFrame, 
                                               text="",
                                               corner_radius=6,
                                               fg_color=['#979DA2', 'gray29'],
                                               text_color=['#DCE4EE', '#DCE4EE'])
        self.inputImg.grid(column = 0, row = 0, padx=0, pady=0, sticky="nsew")
        self.button_explore = customtkinter.CTkButton(self, 
                                text = "Input image",
                                command = lambda: self.browseFiles()) 
        self.button_explore.grid(column = 0, row = 4, padx = (20,0), pady = 0, sticky="new")
        ### End img mngmnt

        # middle buttons
        self.swapFrame = customtkinter.CTkFrame(self, width=30, height=30, fg_color=self.cget("fg_color")) #their units in pixels
        button3 = customtkinter.CTkButton(self.swapFrame, 
                                          text ="",
                                          image=larrow_image,
                                          command=self.swap)
        self.swapFrame.grid_propagate(False)
        self.swapFrame.columnconfigure(0, weight=1)
        self.swapFrame.rowconfigure(0,weight=1)
        self.swapFrame.grid(row=1, column=1, sticky="n", pady=0)
        button3.grid(sticky="wens")

        button1 = customtkinter.CTkButton(self, text ="Encrypt", command=self.encrypt)
        button1.grid(row = 2, column = 1, padx = 5, pady = 5, sticky="sew")

        button2 = customtkinter.CTkButton(self, text ="Decrypt", command=self.decrypt)
        button2.grid(row = 3, column = 1, padx = 5, pady = 5, sticky="sew")

        # output
        self.outputImgFrame = customtkinter.CTkFrame(self)
        self.outputImgFrame.grid_propagate(False)
        self.outputImgFrame.columnconfigure(0, weight=1)
        self.outputImgFrame.rowconfigure(0, weight=1)
        self.outputImgFrame.configure(width=300,height=300)
        self.outputImgFrame.grid(column = 2, row = 1, rowspan=3, padx=(0, 20), pady=0, sticky="nsew")
        self.outputImg = customtkinter.CTkLabel(self.outputImgFrame, 
                                               text="",
                                               corner_radius=6,
                                               fg_color=['#979DA2', 'gray29'],
                                               text_color=['#DCE4EE', '#DCE4EE'])
        self.outputImg.grid(column = 0, row = 0, padx=0, pady=0, sticky="nsew")

        self.buttonSave = customtkinter.CTkButton(self, 
                                text = "Save",
                                command = self.saveFile) 
        self.buttonSave.grid(column = 2, row = 4, padx = (0,20), pady = (0,10), sticky="new")

        # Key Part
        self.keyFrame = customtkinter.CTkFrame(self, fg_color=self.cget("fg_color"))
        self.keyFrame.columnconfigure(2, weight=1)
        self.keyFrame.grid(row = 5, column = 0, columnspan=3, padx=20, pady=20, sticky="new")
        button1 = customtkinter.CTkButton(self.keyFrame, 
                                          compound="right",
                                          text ="Generate Key      ",
                                          image=dice_image,
                                          command = lambda : self.changeKey(int(self.seg_button.get())))
        button1.grid(row = 0, column = 3, padx = (0,5), pady = 0, sticky="new")


        self.keyLenFrame = customtkinter.CTkFrame(self.keyFrame)
        self.keyLenFrame.grid(row = 0, column = 1, padx=0, pady=0, sticky="new")
        self.keyLenFrame.grid_columnconfigure(0, weight=1)
        self.keyLenFrame.grid_rowconfigure(0, weight=1)
        self.ds_frame_label = customtkinter.CTkLabel(self.keyLenFrame, 
                                                     text="Key length",
                                                     corner_radius=6)
        self.ds_frame_label.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")


        self.seg_button = customtkinter.CTkSegmentedButton(self.keyFrame)
        self.seg_button.grid(row=0, column=2, padx=(0, 5), pady=0, sticky="new")
        self.seg_button.configure(values=["1", "2", "3", "4", "5", "6", "7"])
        self.seg_button.set("5")

        # Key display
        self.currentKeyFrame = customtkinter.CTkFrame(self.keyFrame, fg_color=self.cget("fg_color"))
        self.currentKeyFrame.grid_propagate(False)
        self.currentKeyFrame.grid(row = 0, column = 0, padx=(0,10), pady=0, sticky="new")
        self.currentKeyFrameLabel = customtkinter.CTkLabel(self.currentKeyFrame, 
                                                     text="Current Key",
                                                     corner_radius=6, 
                                                     fg_color=['#979DA2', 'gray29'], 
                                                     text_color=['#DCE4EE', '#DCE4EE'])
        self.currentKeyFrameLabel.grid(row=0, column=0, columnspan=1, padx=0, pady=0, sticky="ew")

        self.textbox = customtkinter.CTkTextbox(self.currentKeyFrame, state="disabled")
        self.textbox.grid(row=1, column=0, padx=0, pady=0, sticky="nsew")
        self.textbox.insert("0.0", "")

        # Analysis
        button2 = customtkinter.CTkButton(self, text ="Cryptanalysis",
                            command = lambda : controller.show_frame(Page2))
        button2.grid(row = 8, column = 0, padx = 10, pady = 10)

        self.changeKey(5)

    def browseFiles(self):
        # image dir
        self.dirty = True
        self.imgName = filedialog.askopenfilename(initialdir = "/",
                                                    title = "Select a File",
                                                    filetypes = (("Picture files",
                                                                "*.png;*.jpg;*.ppm;*.bmp"),
                                                                ('All files', '*.*')))
        # file to be encrypted
        # original: self.img
        self.img = np.array(iio.imread(self.imgName))

        self.original_shape = self.img.shape
        n = self.keyLen
        residue = self.img.shape[0] % n
        if residue != 0:
            newShape = list(self.img.shape)
            newOverallShape = list(self.img.shape)
            newShape[0] = n-residue
            newOverallShape[0] += n-residue
            if len(self.img.shape) < 3:
                self.img = np.append(self.img, np.random.randint(0, 255, size=newShape, dtype=int) , axis=0)
            else:
                self.img = np.append(self.img, np.random.randint(0, 1, size=newShape, dtype=int) , axis=0)
            self.original_shape = newOverallShape

        # file to be displayed
        imgList = self.imgName.split(".")
        self.anyFormatImage = Image.open(self.imgName)
        self.anyFormatImage.thumbnail((500,500), Image.LANCZOS)
        self.originalFormat = imgList[1]
        self.resizedImgName = imgList[0]+".ppm"
        self.anyFormatImage.save(self.resizedImgName)

        # Change label contents
        imgObject = PhotoImage(file = self.resizedImgName)

        self.inputImg.configure(image=imgObject)
        self.inputImg.image = imgObject
    
    def encrypt(self):
        if self.dirty:
            self.dirtyOutput = True

            encoded_image_vector = self.system.encode(self.img)

            # Reshape to the original shape of the image
            self.encoded_image = encoded_image_vector.reshape(self.original_shape)

            self.encoded_img_name = 'output.' + "png"
            self.encoded_img_name_for_display = 'dispOutput.' + "png"
            img2 = self.encoded_image.astype('uint8')
            iio.imwrite(self.encoded_img_name, img2)
            iio.imwrite(self.encoded_img_name_for_display, img2)
            self.downloadableImage = Image.open(self.encoded_img_name)

            # Reformat to be displayed
            imgList = self.encoded_img_name.split(".")
            self.anyFormatImage = Image.open(self.encoded_img_name_for_display)
            self.anyFormatImage.thumbnail((500,500), Image.LANCZOS)
            self.resizedImageName = imgList[0]+".ppm"
            self.anyFormatImage.save(self.resizedImageName)

            # Change label contents
            imgObject = PhotoImage(file = self.resizedImageName)

            self.outputImg.configure(image=imgObject)
            self.outputImg.image = imgObject


    def decrypt(self):
        if self.dirty:
            self.dirtyOutput = True

            encoded_image_vector = self.system.decode(self.img)

            # Reshape to the original shape of the image
            self.encoded_image = encoded_image_vector.reshape(self.original_shape)

            self.encoded_img_name = 'output.' + "png"
            self.encoded_img_name_for_display = 'dispOutput.' + "png"
            img2 = self.encoded_image.astype('uint8')
            iio.imwrite(self.encoded_img_name, img2)
            iio.imwrite(self.encoded_img_name_for_display, img2)
            self.downloadableImage = Image.open(self.encoded_img_name)

            # Reformat to be displayed
            imgList = self.encoded_img_name.split(".")
            self.anyFormatImage = Image.open(self.encoded_img_name_for_display)
            self.anyFormatImage.thumbnail((500,500), Image.LANCZOS)
            self.resizedImageName = imgList[0]+".ppm"
            self.anyFormatImage.save(self.resizedImageName)

            # Change label contents
            imgObject = PhotoImage(file = self.resizedImageName)

            self.outputImg.configure(image=imgObject)
            self.outputImg.image = imgObject


    def changeKey(self, keySize):
        if keySize != self.keyLen and self.dirty:
            self.keyLen = keySize
            self.updateImageDimensions()
        self.system.setKeyLen(keySize)
        self.system.setKey()

        # Display key
        self.textbox.configure(state="normal")
        self.textbox.delete('0.0', tk.END)
        self.textbox.insert("0.0", self.system.codeKey)
        self.textbox.configure(state="disabled")

    def saveFile(self):
        if self.dirtyOutput:
            file = filedialog.asksaveasfile(mode='wb', 
                                            filetypes = (("png","*.png"),
                                                        ('All files', '*.*')),
                                            defaultextension=".png")
            if file:
                self.downloadableImage.save(file) # saves the image to the input file name. 
        
    def updateImageDimensions(self):
        self.img = np.array(iio.imread(self.imgName))
        self.original_shape = self.img.shape
        n = self.keyLen
        residue = self.img.shape[0] % n
        if residue != 0:
            newShape = list(self.img.shape)
            newOverallShape = list(self.img.shape)
            newShape[0] = n-residue
            newOverallShape[0] += n-residue
            if len(self.img.shape) < 3:
                self.img = np.append(self.img, np.random.randint(0, 255, size=newShape, dtype=int) , axis=0)
            else:
                self.img = np.append(self.img, np.random.randint(0, 1, size=newShape, dtype=int) , axis=0)
            self.original_shape = newOverallShape
    
    def swap(self):
        if self.dirtyOutput:
            self.imgName = self.encoded_img_name
            self.img = np.array(iio.imread(self.imgName))
            self.original_shape = self.img.shape

            # file to be displayed
            imgList = self.imgName.split(".")
            self.anyFormatImage = Image.open(self.imgName)
            self.anyFormatImage.thumbnail((500,500), Image.LANCZOS)
            self.originalFormat = imgList[1]
            self.resizedImgName = imgList[0]+".ppm"
            self.anyFormatImage.save(self.resizedImgName)

            # Change label contents
            imgObject = PhotoImage(file = self.resizedImgName)

            self.inputImg.configure(image=imgObject)
            self.inputImg.image = imgObject

# third window frame page2
class Page2(customtkinter.CTkFrame):
    def __init__(self, parent, controller):
        customtkinter.CTkFrame.__init__(self, parent)
        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="CustomTkinter", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame, command=self.sidebar_button_event)
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)
        self.sidebar_button_2 = customtkinter.CTkButton(self.sidebar_frame, command=self.sidebar_button_event)
        self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)
        self.sidebar_button_3 = customtkinter.CTkButton(self.sidebar_frame, command=self.sidebar_button_event)
        self.sidebar_button_3.grid(row=3, column=0, padx=20, pady=10)
        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))
        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"],
                                                               command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20))

        # create main entry and button
        self.entry = customtkinter.CTkEntry(self, placeholder_text="CTkEntry")
        self.entry.grid(row=3, column=1, columnspan=2, padx=(20, 0), pady=(20, 20), sticky="nsew")

        self.main_button_1 = customtkinter.CTkButton(master=self, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"))
        self.main_button_1.grid(row=3, column=3, padx=(20, 20), pady=(20, 20), sticky="nsew")

        # create textbox
        self.textbox = customtkinter.CTkTextbox(self, width=250)
        self.textbox.grid(row=0, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")

        # create tabview
        self.tabview = customtkinter.CTkTabview(self, width=250)
        self.tabview.grid(row=0, column=2, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.tabview.add("CTkTabview")
        self.tabview.add("Tab 2")
        self.tabview.add("Tab 3")
        self.tabview.tab("CTkTabview").grid_columnconfigure(0, weight=1)  # configure grid of individual tabs
        self.tabview.tab("Tab 2").grid_columnconfigure(0, weight=1)

        self.optionmenu_1 = customtkinter.CTkOptionMenu(self.tabview.tab("CTkTabview"), dynamic_resizing=False,
                                                        values=["Value 1", "Value 2", "Value Long Long Long"])
        self.optionmenu_1.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.combobox_1 = customtkinter.CTkComboBox(self.tabview.tab("CTkTabview"),
                                                    values=["Value 1", "Value 2", "Value Long....."])
        self.combobox_1.grid(row=1, column=0, padx=20, pady=(10, 10))
        self.string_input_button = customtkinter.CTkButton(self.tabview.tab("CTkTabview"), text="Open CTkInputDialog",
                                                           command=self.open_input_dialog_event)
        self.string_input_button.grid(row=2, column=0, padx=20, pady=(10, 10))
        self.label_tab_2 = customtkinter.CTkLabel(self.tabview.tab("Tab 2"), text="CTkLabel on Tab 2")
        self.label_tab_2.grid(row=0, column=0, padx=20, pady=20)

        # create radiobutton frame
        self.radiobutton_frame = customtkinter.CTkFrame(self)
        self.radiobutton_frame.grid(row=0, column=3, padx=(20, 20), pady=(20, 0), sticky="nsew")
        self.radio_var = tkinter.IntVar(value=0)
        self.label_radio_group = customtkinter.CTkLabel(master=self.radiobutton_frame, text="CTkRadioButton Group:")
        self.label_radio_group.grid(row=0, column=2, columnspan=1, padx=10, pady=10, sticky="")
        self.radio_button_1 = customtkinter.CTkRadioButton(master=self.radiobutton_frame, variable=self.radio_var, value=0)
        self.radio_button_1.grid(row=1, column=2, pady=10, padx=20, sticky="n")
        self.radio_button_2 = customtkinter.CTkRadioButton(master=self.radiobutton_frame, variable=self.radio_var, value=1)
        self.radio_button_2.grid(row=2, column=2, pady=10, padx=20, sticky="n")
        self.radio_button_3 = customtkinter.CTkRadioButton(master=self.radiobutton_frame, variable=self.radio_var, value=2)
        self.radio_button_3.grid(row=3, column=2, pady=10, padx=20, sticky="n")

        # create slider and progressbar frame
        self.slider_progressbar_frame = customtkinter.CTkFrame(self, fg_color="transparent")
        self.slider_progressbar_frame.grid(row=1, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.slider_progressbar_frame.grid_columnconfigure(0, weight=1)
        self.slider_progressbar_frame.grid_rowconfigure(4, weight=1)
        self.seg_button_1 = customtkinter.CTkSegmentedButton(self.slider_progressbar_frame)
        self.seg_button_1.grid(row=0, column=0, padx=(20, 10), pady=(10, 10), sticky="ew")
        self.progressbar_1 = customtkinter.CTkProgressBar(self.slider_progressbar_frame)
        self.progressbar_1.grid(row=1, column=0, padx=(20, 10), pady=(10, 10), sticky="ew")
        self.progressbar_2 = customtkinter.CTkProgressBar(self.slider_progressbar_frame)
        self.progressbar_2.grid(row=2, column=0, padx=(20, 10), pady=(10, 10), sticky="ew")
        self.slider_1 = customtkinter.CTkSlider(self.slider_progressbar_frame, from_=0, to=1, number_of_steps=4)
        self.slider_1.grid(row=3, column=0, padx=(20, 10), pady=(10, 10), sticky="ew")
        self.slider_2 = customtkinter.CTkSlider(self.slider_progressbar_frame, orientation="vertical")
        self.slider_2.grid(row=0, column=1, rowspan=5, padx=(10, 10), pady=(10, 10), sticky="ns")
        self.progressbar_3 = customtkinter.CTkProgressBar(self.slider_progressbar_frame, orientation="vertical")
        self.progressbar_3.grid(row=0, column=2, rowspan=5, padx=(10, 20), pady=(10, 10), sticky="ns")

        # create scrollable frame
        self.scrollable_frame = customtkinter.CTkScrollableFrame(self, label_text="CTkScrollableFrame")
        self.scrollable_frame.grid(row=1, column=2, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.scrollable_frame.grid_columnconfigure(0, weight=1)
        self.scrollable_frame_switches = []
        for i in range(100):
            switch = customtkinter.CTkSwitch(master=self.scrollable_frame, text=f"CTkSwitch {i}")
            switch.grid(row=i, column=0, padx=10, pady=(0, 20))
            self.scrollable_frame_switches.append(switch)

        # create checkbox and switch frame
        self.checkbox_slider_frame = customtkinter.CTkFrame(self)
        self.checkbox_slider_frame.grid(row=1, column=3, padx=(20, 20), pady=(20, 0), sticky="nsew")
        self.checkbox_1 = customtkinter.CTkCheckBox(master=self.checkbox_slider_frame)
        self.checkbox_1.grid(row=1, column=0, pady=(20, 0), padx=20, sticky="n")
        self.checkbox_2 = customtkinter.CTkCheckBox(master=self.checkbox_slider_frame)
        self.checkbox_2.grid(row=2, column=0, pady=(20, 0), padx=20, sticky="n")
        self.checkbox_3 = customtkinter.CTkCheckBox(master=self.checkbox_slider_frame)
        self.checkbox_3.grid(row=3, column=0, pady=20, padx=20, sticky="n")

        # set default values
        self.sidebar_button_3.configure(state="disabled", text="Disabled CTkButton")
        self.checkbox_3.configure(state="disabled")
        self.checkbox_1.select()
        self.scrollable_frame_switches[0].select()
        self.scrollable_frame_switches[4].select()
        self.radio_button_3.configure(state="disabled")
        self.appearance_mode_optionemenu.set("Dark")
        self.scaling_optionemenu.set("100%")
        self.optionmenu_1.set("CTkOptionmenu")
        self.combobox_1.set("CTkComboBox")
        self.slider_1.configure(command=self.progressbar_2.set)
        self.slider_2.configure(command=self.progressbar_3.set)
        self.progressbar_1.configure(mode="indeterminnate")
        self.progressbar_1.start()
        self.textbox.insert("0.0", "CTkTextbox\n\n" + "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua.\n\n" * 20)
        self.seg_button_1.configure(values=["CTkSegmentedButton", "Value 2", "Value 3"])
        self.seg_button_1.set("Value 2")

    def open_input_dialog_event(self):
        dialog = customtkinter.CTkInputDialog(text="Type in a number:", title="CTkInputDialog")
        print("CTkInputDialog:", dialog.get_input())

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def sidebar_button_event(self):
        print("sidebar_button click")



if __name__ == "__main__":
    app = App()
    app.mainloop()

  

                                                                                                  
