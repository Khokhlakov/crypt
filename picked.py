import tkinter as tk
from tkinter import ttk
import tkinter.messagebox
import customtkinter
import imageio.v3 as iio
import numpy as np
from random import randint
import shutil

# Imports sistemas criptograficos
from Desplazamiento import Desplazamiento
from Multiplicativo import Multiplicativo
from Afin import Afin
from Vigenere import Vigenere
from Permutacion import Permutacion
from Substitution import Substitution
from Hill import Hill
from RSA import RSAEncryption
from ELGamal import ElGamalCryptosystem
import Rabin
from SDES import SimplerDES
from DSA import DSA_Signature
from Blocks import *

from AlgBrauer import *

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
# vvvvv
path_to_dat = os.path.join(bundle_dir, 'livai.ppm')

config_path = os.path.join(application_path, "livai.ppm")


customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


LARGEFONT =("Verdana", 35)

path_to_dice = os.path.join(bundle_dir, "dice.png")
path_to_larrow = os.path.join(bundle_dir, "larrow.png")
path_to_swords = os.path.join(bundle_dir, "swords.png")
path_to_lock1 = os.path.join(bundle_dir, "lock1.png")
path_to_lock2 = os.path.join(bundle_dir, "lock2.png")
path_to_home = os.path.join(bundle_dir, "home.png")
path_to_save = os.path.join(bundle_dir, "save.png")
path_to_name = os.path.join(bundle_dir, "name.png")
path_to_nameL = os.path.join(bundle_dir, "nameLight.png")
path_to_icon = os.path.join(bundle_dir, "icono.ico")
path_to_sampleQuiver = os.path.join(bundle_dir, "sampleQuiver1.png")


dice_image = customtkinter.CTkImage(Image.open(path_to_dice), size=(18, 18))
larrow_image = customtkinter.CTkImage(Image.open(path_to_larrow), size=(18, 18))
swords_image = customtkinter.CTkImage(Image.open(path_to_swords), size=(18, 18))
lock1_image = customtkinter.CTkImage(Image.open(path_to_lock1), size=(18, 18))
lock2_image = customtkinter.CTkImage(Image.open(path_to_lock2), size=(18, 18))
home_image = customtkinter.CTkImage(Image.open(path_to_home), size=(18, 18))
save_image = customtkinter.CTkImage(Image.open(path_to_save), size=(18, 18))

name_image = customtkinter.CTkImage(dark_image=Image.open(path_to_name), 
                                    light_image=Image.open(path_to_nameL), 
                                    size=(400/3, 100/3))


# Everything will be stored here
if not os.path.exists("PiCKED App"):
   # Create a new directory because it does not exist
   os.makedirs("PiCKED App")


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        
        #self.title("CustomTkinter complex_example.py")
        self.geometry(f"{1100}x{580}")
        self.title("PiCKED")
        self.after(250, lambda: self.iconbitmap(path_to_icon))
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
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, 
                                                 image=name_image,
                                                 text="")
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame, 
                                                        compound="right",
                                                        text ="Home                   ", 
                                                        image=home_image,
                                                        command=lambda: self.show_frame(HomePage))
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)
        
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
        self.appearance_mode_optionemenu.set("Dark")
        self.scaling_optionemenu.set("100%")


        self.scrollable_frame = customtkinter.CTkScrollableFrame(self.container)
        self.scrollable_frame.grid(row = 0, column = 1, rowspan = 3, sticky ="nsew")
        self.scrollable_frame.grid_columnconfigure(0, weight=1)
        self.scrollable_frame.propagate(False)

        #self.container.grid_rowconfigure(0, weight = 1)
        #self.container.grid_columnconfigure(0, weight = 1)

        # initializing frames to an empty array
        self.frames = {}

        # iterating through a tuple consisting
        # of the different page layouts
        for F in (HomePage, 
                  AffinePage, 
                  HillPage, 
                  MultiplicativePage, 
                  ShiftPage, 
                  VigenerePage, 
                  PermutationPage, 
                  SubstitutionPage,
                  AESPage, 
                  TDESPage,
                  SDESPage,
                  RSAPage,
                  ElGamalPage,
                  RabinPage,
                  DSAPage):

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

        self.columnconfigure((0,1),weight=1)

        # create tabview
        self.tabview = customtkinter.CTkTabview(self, width=250)
        self.tabview.grid(row=0, column=0, padx=(20, 0), pady=(20, 0), rowspan=10, sticky="nsew")
        self.tabview.add("Classical ciphers")
        self.tabview.add("Block ciphers")
        self.tabview.add("Public key")
        self.tabview.tab("Classical ciphers").grid_columnconfigure((0,1), weight=1)  # configure grid of individual tabs
        
        self.tabview.tab("Block ciphers").grid_columnconfigure((0,1), weight=1)

        self.tabview.tab("Public key").grid_columnconfigure((0,1), weight=1)

        # Basic ciphers
        affineButton = customtkinter.CTkButton(self.tabview.tab("Classical ciphers"), 
                                               text ="Affine",
                                               command = lambda : controller.show_frame(AffinePage))
        affineButton.grid(row = 0, column = 0, padx = 10, pady = 10, sticky="ew")

        hillButton = customtkinter.CTkButton(self.tabview.tab("Classical ciphers"), 
                                             text ="Hill",
                                             command = lambda : controller.show_frame(HillPage))
        hillButton.grid(row = 0, column = 1, padx = 10, pady = 10, sticky="ew")

        multiplicativeButton = customtkinter.CTkButton(self.tabview.tab("Classical ciphers"), 
                                                       text ="Multiplicative",
                                                       command=lambda : controller.show_frame(MultiplicativePage))
        multiplicativeButton.grid(row = 1, column = 0, padx = 10, pady = 10, sticky="ew")
        
        permutationButton = customtkinter.CTkButton(self.tabview.tab("Classical ciphers"), 
                                                    text ="Permutation",
                                                    command=lambda : controller.show_frame(PermutationPage))
        permutationButton.grid(row = 1, column = 1, padx = 10, pady = 10, sticky="ew")

        shiftButton = customtkinter.CTkButton(self.tabview.tab("Classical ciphers"), 
                                              text ="Shift",
                                              command=lambda : controller.show_frame(ShiftPage))
        shiftButton.grid(row = 2, column = 0, padx = 10, pady = 10, sticky="ew")
        
        substitutionButton = customtkinter.CTkButton(self.tabview.tab("Classical ciphers"), 
                                                      text ="Substitution",
                                                      command=lambda : controller.show_frame(SubstitutionPage))
        substitutionButton.grid(row = 2, column = 1, padx = 10, pady = 10, sticky="ew")

        vigenereButton = customtkinter.CTkButton(self.tabview.tab("Classical ciphers"), 
                                                 text ="Vigenere",
                                                 command=lambda : controller.show_frame(VigenerePage))
        vigenereButton.grid(row = 3, column = 0, padx = 10, pady = 10, sticky="ew")
        
        # Block ciphers
        aesButton = customtkinter.CTkButton(self.tabview.tab("Block ciphers"), 
                                             text ="AES",
                                             command = lambda : controller.show_frame(AESPage))
        aesButton.grid(row = 0, column = 0, padx = 10, pady = 10, sticky="ew")

        sdesButton = customtkinter.CTkButton(self.tabview.tab("Block ciphers"), 
                                             text ="S-DES",
                                             command = lambda : controller.show_frame(SDESPage))
        sdesButton.grid(row = 0, column = 1, padx = 10, pady = 10, sticky="ew")

        tdesButton = customtkinter.CTkButton(self.tabview.tab("Block ciphers"), 
                                             text ="T-DES",
                                             command=lambda : controller.show_frame(TDESPage))
        tdesButton.grid(row = 1, column = 0, padx = 10, pady = 10, sticky="ew")

        # Public Key
        sdesButton = customtkinter.CTkButton(self.tabview.tab("Public key"), 
                                             text ="ElGamal",
                                             command = lambda : controller.show_frame(ElGamalPage))
        sdesButton.grid(row = 0, column = 0, padx = 10, pady = 10, sticky="ew")


        aesButton = customtkinter.CTkButton(self.tabview.tab("Public key"), 
                                             text ="RSA",
                                             command = lambda : controller.show_frame(RSAPage))
        aesButton.grid(row = 0, column = 1, padx = 10, pady = 10, sticky="ew")


        tdesButton = customtkinter.CTkButton(self.tabview.tab("Public key"), 
                                             text ="Rabin",
                                             command= lambda : controller.show_frame(RabinPage))
        tdesButton.grid(row = 1, column = 0, padx = 10, pady = 10, sticky="ew")

        # Digital signatures
        self.ds_frame = customtkinter.CTkFrame(self)
        self.ds_frame.grid(row = 0, column = 1, rowspan=5, padx=(20, 20), pady=(20, 0), sticky="ew")
        self.ds_frame.grid_columnconfigure((0,1), weight=1)
        self.ds_frame_label = customtkinter.CTkLabel(self.ds_frame, 
                                                     text="Generate a digital signature",
                                                     corner_radius=6, 
                                                     fg_color=['#979DA2', 'gray29'], 
                                                     text_color=['#DCE4EE', '#DCE4EE'])
        self.ds_frame_label.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="")

        
        dsabutton = customtkinter.CTkButton(self.ds_frame, 
                                          text ="DSA", 
                                          command = lambda : controller.show_frame(DSAPage))
        dsabutton.grid(row = 1, column = 0, columnspan=2, padx = 10, pady = 10, sticky="ew")


        # Brauering
        self.br_frame = customtkinter.CTkFrame(self)
        self.br_frame.grid(row = 5, column = 1, rowspan=5, padx=(20, 20), pady=(20, 0), sticky="ew")
        self.br_frame.grid_columnconfigure((0,1), weight=1)
        self.br_frame_label = customtkinter.CTkLabel(self.br_frame, 
                                                     text="Build a Brauer configuration algebra",
                                                     corner_radius=6, 
                                                     fg_color=['#979DA2', 'gray29'], 
                                                     text_color=['#DCE4EE', '#DCE4EE'])
        self.br_frame_label.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="")

        self.entryKey = customtkinter.CTkEntry(self.br_frame, placeholder_text="Input message")
        self.entryKey.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

        brbutton = customtkinter.CTkButton(self.br_frame, 
                                          text ="Build", 
                                          command = self.popUp)
        brbutton.grid(row = 2, column = 0, columnspan=2, padx = 10, pady = 10, sticky="ew")

        

       

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
    
    def popUp(self):
        # get key length
        self.message = self.entryKey.get().lower().strip()
        if len(self.message) == 0:
            self.entryKey.delete(0, tk.END)
            self.br_frame_label.focus()
        else:
            self.popUp2()

    def popUp2(self):
        # create popUp window (more like pop back)
        top = customtkinter.CTkToplevel()
        top.geometry("900x500")
        top.title("PiCKED")
        top.after(250, lambda: top.iconbitmap(path_to_icon))
        top.grid_columnconfigure(0, weight=1)
        top.grid_rowconfigure(0, weight=1)
        
        
        scrollable_frame = customtkinter.CTkScrollableFrame(top, label_text="")
        scrollable_frame.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")
        scrollable_frame.grid_columnconfigure(1, weight=1)

        customtkinter.CTkLabel(scrollable_frame, 
                            text= "BRAUER QUIVER", 
                            font=customtkinter.CTkFont(size=20, weight="bold")).grid(column=0,row=0)

        # image frame
        imgFrame = customtkinter.CTkFrame(scrollable_frame)
        imgFrame.configure(width=400,height=400)
        imgFrame.grid_propagate(False)
        imgFrame.columnconfigure(0, weight=1)
        imgFrame.rowconfigure(0, weight=1)
        imgFrame.grid(column = 0, row = 1, rowspan=1, padx=(20,5), pady=(10,0), sticky="nsew")
        imageLabel = customtkinter.CTkLabel(imgFrame, 
                                                text="",
                                                corner_radius=6,
                                                fg_color=['#979DA2', 'gray29'],
                                                text_color=['#DCE4EE', '#DCE4EE'])
        imageLabel.grid(column = 0, row = 0, padx=0, pady=0, sticky="nsew")

        # Calcular algebra stuff
        self.resultados = obtener_resultados(self.message)
        try:
            the_image_path = crear_grafo(self.resultados["Ciclos"])
            the_image = Image.open(the_image_path)
            the_image.thumbnail((600,600), Image.LANCZOS)
            daPath = os.path.join("PiCKED App","Brauervisualization.ppm")
            the_image.save(daPath)

            # Change label contents
            imgObject = PhotoImage(file = daPath)
            
            imageLabel.configure(image=imgObject)

            # save button
            buttonSave = customtkinter.CTkButton(scrollable_frame, 
                                                        text = "Save",
                                                        command = lambda : self.saveQuiver(self.resultados))
            buttonSave.grid(column = 0, row = 2, padx = (20,5), pady = (0,10), sticky="new")
        except:
            the_image = Image.open(path_to_sampleQuiver)
            the_image.thumbnail((600,600), Image.LANCZOS)
            daPath = os.path.join("PiCKED App","Brauervisualization.ppm")
            the_image.save(daPath)

            # Change label contents
            imgObject = PhotoImage(file = daPath)
            
            imageLabel.configure(image=imgObject)

            # save button
            buttonSave = customtkinter.CTkButton(scrollable_frame, 
                                                        text = "Save",
                                                        command = self.saveQuiverDemo)
            buttonSave.grid(column = 0, row = 2, padx = (20,5), pady = (0,10), sticky="new")
        # output

        outStr = "Original message:\n\t" + self.message + "\n\nPolygons:\n"
        counter = 1
        for polygon in self.resultados["R1"]:
            outStr += "\tW" + str(counter) + ": " + polygon + "\n"
            counter += 1
        outStr += "\nVertices:\n\t{ " 
        lsVert = list(self.resultados["R0"])
        for i in range(len(lsVert)):
            if i < len(lsVert)-1:
                outStr += lsVert[i] + " , "
            else:
                outStr += lsVert[i] + " }\n\n"
        outStr += "Number of loops:\n\t" + str(sum(self.resultados["NLoops"].values())) + "\n\n"
        outStr += "Dimension of the Brauer Configuration Algebra:\n\t" + str(self.resultados["D"]) + "\n\n"
        outStr += "Dimension of the center:\n\t" + str(self.resultados["DZ"]) + "\n\n"
        
        textbox = customtkinter.CTkTextbox(scrollable_frame, state="normal")
        textbox.grid(row=1, column=1, rowspan=2, padx=(5,20), pady=(10, 0), sticky="nsew")
        textbox.insert("0.0", outStr)
        textbox.configure(state="disabled")

        
    
    def saveQuiver(self, resultados):
        file = filedialog.asksaveasfile(mode='wb', 
                                        filetypes = (("png","*.png"),
                                                    ('All files', '*.*')),
                                        defaultextension=".png")
        if file:
            crear_grafo(resultados["Ciclos"], file.name)
    
    def saveQuiverDemo(self):
        myImage = Image.open(path_to_sampleQuiver)
        file = filedialog.asksaveasfile(mode='wb', 
                                        filetypes = (("png","*.png"),
                                                    ('All files', '*.*')),
                                        defaultextension=".png")
        if file:
            myImage.save(file) # saves the image to the input file name. 


# AffinePage window frame
class AffinePage(customtkinter.CTkFrame):
    def __init__(self, parent, controller):
        self.system = Afin(key=[1,0])
        self.currentKey = "(1,0)"

        customtkinter.CTkFrame.__init__(self, parent)

        self.grid_columnconfigure((0,2), weight=1)
        self.grid_columnconfigure(1, weight=0)

        label = customtkinter.CTkLabel(self,
                                       text="AFFINE CIPHER",
                                       font=customtkinter.CTkFont(size=20, weight="bold"))
        label.grid(row=0, column=0, columnspan=3, padx=20, pady=(10,0), sticky="w")

        # input
        self.entry = customtkinter.CTkTextbox(self)
        self.entry.grid(row=1, column=0, rowspan=3, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.entry.insert("0.0", "Attack at noon")
        button1 = customtkinter.CTkButton(self, text ="Clear",
                            command = self.clearInput)
        button1.grid(row = 4, column = 0, padx = (20,0), pady = (0,10), sticky="ew")

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

        button1 = customtkinter.CTkButton(self,
                                          compound="right",
                                          text ="Encrypt                ", 
                                          image=lock1_image,
                                          command=self.encrypt)
        button1.grid(row = 2, column = 1, padx = 5, pady = 5, sticky="sew")

        button2 = customtkinter.CTkButton(self, 
                                          compound="right",
                                          text ="Decrypt                ", 
                                          image=lock2_image,
                                          command=self.decrypt)
        button2.grid(row = 3, column = 1, padx = 5, pady = 5, sticky="sew")

        
        # output
        self.textbox = customtkinter.CTkTextbox(self, state="disabled")
        self.textbox.grid(row=1, column=2, rowspan=3, padx=(0,20), pady=(20, 0), sticky="nsew")
        self.textbox.insert("0.0", "")
        button1 = customtkinter.CTkButton(self, text ="Copy",
                            command = self.copyToClipboard)
        button1.grid(row = 4, column = 2, padx = (0,20), pady = (0,10), sticky="ew")

        # Key part (generation)
        self.keyFrame = customtkinter.CTkFrame(self, fg_color=self.cget("fg_color"))
        self.keyFrame.columnconfigure(0, weight=0)
        self.keyFrame.columnconfigure(1, weight=1)
        self.keyFrame.grid(row = 5, column = 0, columnspan=3, padx=20, pady=20, sticky="ew")
        button1 = customtkinter.CTkButton(self.keyFrame, 
                                          compound="right",
                                          text ="Generate Key      ",
                                          image=dice_image,
                                          command = self.generateKey)
        button1.grid(row = 0, column = 0, padx = (0,5), pady = 0)

        self.entryKey = customtkinter.CTkEntry(self.keyFrame, placeholder_text="Input key and hit enter")
        self.entryKey.bind("<Return>", command=lambda x: self.setKeyFromEntry())
        self.entryKey.grid(row=0, column=1, padx=(5, 0), pady=0, sticky="ew")

        # Key display
        self.currentKeyFrame = customtkinter.CTkFrame(self.keyFrame, fg_color=self.cget("fg_color"))
        self.currentKeyFrame.columnconfigure(0, weight=1)
        self.currentKeyFrame.grid(row = 1, column = 0, padx = (0,5), pady = 5, sticky="ew")
        self.currentKeyFrameLabel = customtkinter.CTkLabel(self.currentKeyFrame, 
                                                     text="Current Key:",
                                                     corner_radius=6, 
                                                     fg_color=['#979DA2', 'gray29'], 
                                                     text_color=['#DCE4EE', '#DCE4EE'])
        self.currentKeyFrameLabel.grid(row=0, column=0, columnspan=1, padx=0, pady=0, sticky="ew")

        self.currentKeyFrameNumber = customtkinter.CTkLabel(self.keyFrame, 
                                                     text="(1,0)",
                                                     anchor="w")
        self.currentKeyFrameNumber.grid(row=1, column=1, columnspan=1, padx=(5, 0), pady=0, sticky="ew")

        # Analysis
        button2 = customtkinter.CTkButton(self.keyFrame,
                                          compound="right",
                                          text ="Attack                   ",
                                          image=swords_image,
                                          command = self.attack)
        button2.grid(row = 2, column = 0, padx = (0,5), pady = 20, sticky="new")

        # Number of keys to be recommended
        self.keyNumFrame = customtkinter.CTkFrame(self.keyFrame)
        self.keyNumFrame.columnconfigure(1, weight=1)
        self.keyNumFrame.grid(row = 2, column = 1, padx =0, pady = 20, sticky="new")

        self.keyLenFrame = customtkinter.CTkFrame(self.keyNumFrame)
        self.keyLenFrame.grid(row = 0, column = 0, padx=0, pady=0, sticky="new")
        self.keyLenFrame.grid_columnconfigure(0, weight=1)
        self.keyLenFrame.grid_rowconfigure(0, weight=1)
        self.ds_frame_label = customtkinter.CTkLabel(self.keyLenFrame, 
                                                     text="Number of keys",
                                                     corner_radius=6)
        self.ds_frame_label.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")


        self.seg_button = customtkinter.CTkSegmentedButton(self.keyNumFrame)
        self.seg_button.grid(row=0, column=1, padx=0, pady=0, sticky="new")
        self.seg_button.configure(values=["1", "2", "3", "4", "5", "6", "7", "All"])
        self.seg_button.set("1")

        # language to be used
        self.langTextFrame = customtkinter.CTkFrame(self.keyNumFrame)
        self.langTextFrame.grid(row = 1, column = 0, padx=0, pady=(5,0), sticky="new")
        self.langTextFrame.grid_columnconfigure(0, weight=1)
        self.langTextFrame.grid_rowconfigure(0, weight=1)
        self.langLabel = customtkinter.CTkLabel(self.langTextFrame, 
                                                     text="Language",
                                                     corner_radius=6)
        self.langLabel.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")

        self.seg_lang = customtkinter.CTkSegmentedButton(self.keyNumFrame)
        self.seg_lang.grid(row=1, column=1, padx=0, pady=(5,0), sticky="new")
        self.seg_lang.configure(values=["English", "French", "German", "Italian", "Portuguese", "Spanish"])
        self.seg_lang.set("English")

        # attack textbox
        self.keyTextbox = customtkinter.CTkTextbox(self.keyFrame, state="disabled")
        self.keyTextbox.grid(row=3, column=0, columnspan=2, padx=0, pady=0, sticky="ew")
        self.keyTextbox.insert("0.0", "")
    
    def encrypt(self):
        inputText = self.entry.get("0.0", tk.END)

        cipherText = self.system.encrypt(inputText)
        self.textbox.configure(state="normal")
        self.textbox.delete('1.0', tk.END)
        self.textbox.insert("0.0", cipherText)
        self.textbox.configure(state="disabled")
        
    def decrypt(self):
        inputText = self.entry.get("0.0", tk.END)

        cipherText = self.system.decrypt(inputText)
        self.textbox.configure(state="normal")
        self.textbox.delete('0.0', tk.END)
        self.textbox.insert("0.0", cipherText)
        self.textbox.configure(state="disabled")
    
    def copyToClipboard(self):
        self.clipboard_clear()
        self.clipboard_append(self.textbox.get('1.0', 'end-1c'))

    def swap(self):
        self.entry.delete('0.0', tk.END)
        self.entry.insert("0.0", self.textbox.get('1.0', 'end-1c'))
    
    def clearInput(self):
        self.entry.delete('0.0', tk.END)

    def attack(self):
        self.system.lang = self.seg_lang.get()

        inputText = self.entry.get("0.0", tk.END)
        self.system.setText(inputText)
        cleanString = self.system.getCleanString()
        if cleanString != "":
            
            numKeysStr = self.seg_button.get()
            if numKeysStr == "All":
                numKeys = 312
            else:
                numKeys = int(numKeysStr)


            keys1, keys2 = self.system.getBestKeys(cleanString, num=int(numKeys))

            if numKeysStr == "All":
                # Display recommended keys

                tempSys = Afin(text=cleanString)
                tempSys.lang = self.seg_lang.get()
                # Display recommended keys
                outputString = "Here is a list of keys with the text that results from deciphering with those keys. It has been ordered assuming the language of the plaintext is "+ self.seg_lang.get() +".\n\n"

                # Display recommended keys
                self.keyTextbox.configure(state="normal")


                for i in range(numKeys):
                    key1 = keys1[i][0]
                    key2 = keys2[i][0]

                    tempSys.setKey(key1)
                    result = tempSys.decrypt()
                    splitText = True
                    if len(result) <= 100:
                        splitText = False
                    else:
                        rInt = randint(31, len(result)-61)
                    if splitText:
                        outputString += "("+str(keys1[i][0]) + "):\n" + result[:30]+"..."+result[rInt:rInt+30]+"..."+ result[-30:] + "\n\n"
                    else:
                        outputString += "("+str(keys1[i][0]) + "):\n" + result + "\n\n"

                    if key1 != key2:
                        tempSys.setKey(key2)
                        result = tempSys.decrypt()
                        splitText = True
                        if len(result) <= 100:
                            splitText = False
                        else:
                            rInt = randint(31, len(result)-61)
                        if splitText:
                            outputString += "("+str(keys2[i][0]) + "):\n" + result[:30]+"..."+result[rInt:rInt+30]+"..."+ result[-30:] + "\n\n"
                        else:
                            outputString += "("+str(keys2[i][0]) + "):\n" + result + "\n\n"
                    outputString += "\n"
            else:
            
                # Display recommended keys

                self.keyTextbox.configure(state="normal")
                outputString = "Keep in mind that frequency analysis may be ineffective for short inputs.\nTest the following keys for " + self.system.lang + ":\n"

                for i in range(numKeys):
                    key1 = keys1[i][0]
                    key2 = keys2[i][0]
                    outputString += "(" + keys1[i][0] + ")\n"
                    if key1 != key2:
                        outputString += "(" + keys2[i][0] + ")\n"
                    outputString += "\n"
                    

            self.keyTextbox.delete('0.0', tk.END)
            self.keyTextbox.insert("0.0", outputString)
            self.keyTextbox.configure(state="disabled")
        else:
            self.keyTextbox.configure(state="normal")
            self.keyTextbox.delete('0.0', tk.END)
            self.keyTextbox.insert("0.0", "The input box is empty!")
            self.keyTextbox.configure(state="disabled")
    
    def generateKey(self):
        newKey = self.system.generateKey()
        self.system.setKey(newKey)
        newKeyStr = "(" + str(newKey[0]) + "," + str(newKey[1]) + ")"
        self.currentKeyFrameNumber.configure(text=newKeyStr)
        self.currentKey = newKeyStr
    
    def setKeyFromEntry(self):
        inputKey = self.entryKey.get()

        self.system.setKey(inputKey)
        newKeyStr = "(" + str(self.system.codeKey[0]) + "," + str(self.system.codeKey[1]) + ")"
        self.currentKeyFrameNumber.configure(text=newKeyStr)
        self.currentKey = newKeyStr


# Multiplicative window frame
class MultiplicativePage(customtkinter.CTkFrame):
    def __init__(self, parent, controller):
        self.system = Multiplicativo(key=1)
        self.currentKey = "1"

        customtkinter.CTkFrame.__init__(self, parent)

        self.grid_columnconfigure((0,2), weight=1)
        self.grid_columnconfigure(1, weight=0)

        label = customtkinter.CTkLabel(self,
                                       text="MULTIPLICATIVE CIPHER",
                                       font=customtkinter.CTkFont(size=20, weight="bold"))
        label.grid(row=0, column=0, columnspan=3, padx=20, pady=(10,0), sticky="w")

        # input
        self.entry = customtkinter.CTkTextbox(self)
        self.entry.grid(row=1, column=0, rowspan=3, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.entry.insert("0.0", "Attack at noon")
        button1 = customtkinter.CTkButton(self, text ="Clear",
                            command = self.clearInput)
        button1.grid(row = 4, column = 0, padx = (20,0), pady = (0,10), sticky="ew")

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

        button1 = customtkinter.CTkButton(self,
                                          compound="right",
                                          text ="Encrypt                ", 
                                          image=lock1_image,
                                          command=self.encrypt)
        button1.grid(row = 2, column = 1, padx = 5, pady = 5, sticky="sew")

        button2 = customtkinter.CTkButton(self, 
                                          compound="right",
                                          text ="Decrypt                ", 
                                          image=lock2_image,
                                          command=self.decrypt)
        button2.grid(row = 3, column = 1, padx = 5, pady = 5, sticky="sew")

        
        # output
        self.textbox = customtkinter.CTkTextbox(self, state="disabled")
        self.textbox.grid(row=1, column=2, rowspan=3, padx=(0,20), pady=(20, 0), sticky="nsew")
        self.textbox.insert("0.0", "")
        button1 = customtkinter.CTkButton(self, text ="Copy",
                            command = self.copyToClipboard)
        button1.grid(row = 4, column = 2, padx = (0,20), pady = (0,10), sticky="ew")

        # Key part (generation)
        self.keyFrame = customtkinter.CTkFrame(self, fg_color=self.cget("fg_color"))
        self.keyFrame.columnconfigure(0, weight=0)
        self.keyFrame.columnconfigure(1, weight=1)
        self.keyFrame.grid(row = 5, column = 0, columnspan=3, padx=20, pady=20, sticky="ew")
        button1 = customtkinter.CTkButton(self.keyFrame, 
                                          compound="right",
                                          text ="Generate Key      ",
                                          image=dice_image,
                                          command = self.generateKey)
        button1.grid(row = 0, column = 0, padx = (0,5), pady = 0)

        self.entryKey = customtkinter.CTkEntry(self.keyFrame, placeholder_text="Input key and hit enter")
        self.entryKey.bind("<Return>", command=lambda x: self.setKeyFromEntry())
        self.entryKey.grid(row=0, column=1, padx=(5, 0), pady=0, sticky="ew")

        # Key display
        self.currentKeyFrame = customtkinter.CTkFrame(self.keyFrame, fg_color=self.cget("fg_color"))
        self.currentKeyFrame.columnconfigure(0, weight=1)
        self.currentKeyFrame.grid(row = 1, column = 0, padx = (0,5), pady = 5, sticky="ew")
        self.currentKeyFrameLabel = customtkinter.CTkLabel(self.currentKeyFrame, 
                                                     text="Current Key:",
                                                     corner_radius=6, 
                                                     fg_color=['#979DA2', 'gray29'], 
                                                     text_color=['#DCE4EE', '#DCE4EE'])
        self.currentKeyFrameLabel.grid(row=0, column=0, columnspan=1, padx=0, pady=0, sticky="ew")

        self.currentKeyFrameNumber = customtkinter.CTkLabel(self.keyFrame, 
                                                     text="1",
                                                     anchor="w")
        self.currentKeyFrameNumber.grid(row=1, column=1, columnspan=1, padx=(5, 0), pady=0, sticky="ew")

        # Analysis
        button2 = customtkinter.CTkButton(self.keyFrame,
                                          compound="right",
                                          text ="Attack                   ",
                                          image=swords_image,
                                          command = self.attack)
        button2.grid(row = 2, column = 0, padx = (0,5), pady = 20, sticky="new")

        # Number of keys to be recommended
        self.keyNumFrame = customtkinter.CTkFrame(self.keyFrame)
        self.keyNumFrame.columnconfigure(1, weight=1)
        self.keyNumFrame.grid(row = 2, column = 1, padx =0, pady = 20, sticky="new")

        self.keyLenFrame = customtkinter.CTkFrame(self.keyNumFrame)
        self.keyLenFrame.grid(row = 0, column = 0, padx=0, pady=0, sticky="new")
        self.keyLenFrame.grid_columnconfigure(0, weight=1)
        self.keyLenFrame.grid_rowconfigure(0, weight=1)
        self.ds_frame_label = customtkinter.CTkLabel(self.keyLenFrame, 
                                                     text="Number of keys",
                                                     corner_radius=6)
        self.ds_frame_label.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")


        self.seg_button = customtkinter.CTkSegmentedButton(self.keyNumFrame)
        self.seg_button.grid(row=0, column=1, padx=0, pady=0, sticky="new")
        self.seg_button.configure(values=["1", "2", "3", "4", "5", "6", "7", "All"])
        self.seg_button.set("1")

        # language to be used
        self.langTextFrame = customtkinter.CTkFrame(self.keyNumFrame)
        self.langTextFrame.grid(row = 1, column = 0, padx=0, pady=(5,0), sticky="new")
        self.langTextFrame.grid_columnconfigure(0, weight=1)
        self.langTextFrame.grid_rowconfigure(0, weight=1)
        self.langLabel = customtkinter.CTkLabel(self.langTextFrame, 
                                                     text="Language",
                                                     corner_radius=6)
        self.langLabel.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")

        self.seg_lang = customtkinter.CTkSegmentedButton(self.keyNumFrame)
        self.seg_lang.grid(row=1, column=1, padx=0, pady=(5,0), sticky="new")
        self.seg_lang.configure(values=["English", "French", "German", "Italian", "Portuguese", "Spanish"])
        self.seg_lang.set("English")

        # attack textbox
        self.keyTextbox = customtkinter.CTkTextbox(self.keyFrame, state="disabled")
        self.keyTextbox.grid(row=3, column=0, columnspan=2, padx=0, pady=0, sticky="ew")
        self.keyTextbox.insert("0.0", "")
    
    def encrypt(self):
        inputText = self.entry.get("0.0", tk.END)

        cipherText = self.system.encrypt(inputText)
        self.textbox.configure(state="normal")
        self.textbox.delete('1.0', tk.END)
        self.textbox.insert("0.0", cipherText)
        self.textbox.configure(state="disabled")
        
    def decrypt(self):
        inputText = self.entry.get("0.0", tk.END)

        cipherText = self.system.decrypt(inputText)
        self.textbox.configure(state="normal")
        self.textbox.delete('0.0', tk.END)
        self.textbox.insert("0.0", cipherText)
        self.textbox.configure(state="disabled")
    
    def copyToClipboard(self):
        self.clipboard_clear()
        self.clipboard_append(self.textbox.get('1.0', 'end-1c'))

    def swap(self):
        self.entry.delete('0.0', tk.END)
        self.entry.insert("0.0", self.textbox.get('1.0', 'end-1c'))
    
    def clearInput(self):
        self.entry.delete('0.0', tk.END)

    def attack(self):
        self.system.lang = self.seg_lang.get()

        inputText = self.entry.get("0.0", tk.END)
        self.system.setText(inputText)
        cleanString = self.system.getCleanString()
        if cleanString != "":
            numKeysStr = self.seg_button.get()
            if numKeysStr == "All":
                numKeys = 12
            else:
                numKeys = int(numKeysStr)
            keys1, keys2 = self.system.getBestKeys(cleanString, num=numKeys)

            
            if numKeysStr == "All":
                tempSys = Multiplicativo(text=cleanString)
                # Display recommended keys
                tempSys.lang = self.seg_lang.get()
                outputString = "Here is a list of keys with the text that results from deciphering with those keys. It has been ordered assuming the language of the plaintext is "+ self.seg_lang.get()+".\n\n"

                
                # Display recommended keys
                self.keyTextbox.configure(state="normal")


                for i in range(numKeys):
                    key1 = keys1[i][0]
                    key2 = keys2[i][0]

                    tempSys.setKey(key1)
                    result = tempSys.decrypt()
                    splitText = True
                    if len(result) <= 100:
                        splitText = False
                    else:
                        rInt = randint(31, len(result)-61)
                    if splitText:
                        outputString += str(keys1[i][0]) + ":\n" + result[:30]+"..."+result[rInt:rInt+30]+"..."+ result[-30:] + "\n\n"
                    else:
                        outputString += str(keys1[i][0]) + ":\n" + result + "\n\n"

                    if key1 != key2:
                        tempSys.setKey(key2)
                        result = tempSys.decrypt()
                        splitText = True
                        if len(result) <= 100:
                            splitText = False
                        else:
                            rInt = randint(31, len(result)-61)
                        if splitText:
                            outputString += str(keys2[i][0]) + ":\n" + result[:30]+"..."+result[rInt:rInt+30]+"..."+ result[-30:] + "\n\n"
                        else:
                            outputString += str(keys2[i][0]) + ":\n" + result + "\n\n"
                    outputString += "\n"
            else:
                # Display recommended keys
                self.keyTextbox.configure(state="normal")
                outputString = "Keep in mind that frequency analysis may be ineffective for short inputs.\nTest the following keys for " + self.system.lang + ":\n"

                for i in range(numKeys):
                    key1 = keys1[i][0]
                    key2 = keys2[i][0]
                    outputString += str(keys1[i][0]) + "\n"
                    if key1 != key2:
                        outputString += str(keys2[i][0]) + "\n"
                    outputString += "\n"

            self.keyTextbox.delete('0.0', tk.END)
            self.keyTextbox.insert("0.0", outputString)
            self.keyTextbox.configure(state="disabled")
        else:
            self.keyTextbox.configure(state="normal")
            self.keyTextbox.delete('0.0', tk.END)
            self.keyTextbox.insert("0.0", "The input box is empty!")
            self.keyTextbox.configure(state="disabled")
    
    def generateKey(self):
        newKey = self.system.generateKey()
        self.system.setKey(newKey)
        newKeyStr = str(newKey)
        self.currentKeyFrameNumber.configure(text=newKeyStr)
        self.currentKey = newKeyStr
    
    def setKeyFromEntry(self):
        inputKey = self.entryKey.get()

        self.system.setKey(inputKey)
        newKeyStr = str(self.system.codeKey)
        self.currentKeyFrameNumber.configure(text=newKeyStr)
        self.currentKey = newKeyStr


# Shift window frame
class ShiftPage(customtkinter.CTkFrame):
    def __init__(self, parent, controller):
        self.system = Desplazamiento(key=0)
        self.system2 = Desplazamiento(key=0, codi="0a95")
        self.code = "ASCII"
        self.currentKey = "0"

        customtkinter.CTkFrame.__init__(self, parent)

        self.grid_columnconfigure((0,2), weight=1)
        self.grid_columnconfigure(1, weight=0)

        label = customtkinter.CTkLabel(self,
                                       text="SHIFT CIPHER",
                                       font=customtkinter.CTkFont(size=20, weight="bold"))
        label.grid(row=0, column=0, columnspan=3, padx=20, pady=(10,0), sticky="w")

        # input
        self.entry = customtkinter.CTkTextbox(self)
        self.entry.grid(row=1, column=0, rowspan=3, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.entry.insert("0.0", "Attack at noon")
        button1 = customtkinter.CTkButton(self, text ="Clear",
                            command = self.clearInput)
        button1.grid(row = 4, column = 0, padx = (20,0), pady = (0,10), sticky="ew")

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

        button1 = customtkinter.CTkButton(self,
                                          compound="right",
                                          text ="Encrypt                ", 
                                          image=lock1_image,
                                          command=self.encrypt)
        button1.grid(row = 2, column = 1, padx = 5, pady = 5, sticky="sew")

        button2 = customtkinter.CTkButton(self, 
                                          compound="right",
                                          text ="Decrypt                ", 
                                          image=lock2_image,
                                          command=self.decrypt)
        button2.grid(row = 3, column = 1, padx = 5, pady = 5, sticky="sew")

        
        # output
        self.textbox = customtkinter.CTkTextbox(self, state="disabled")
        self.textbox.grid(row=1, column=2, rowspan=3, padx=(0,20), pady=(20, 0), sticky="nsew")
        self.textbox.insert("0.0", "")
        button1 = customtkinter.CTkButton(self, text ="Copy",
                            command = self.copyToClipboard)
        button1.grid(row = 4, column = 2, padx = (0,20), pady = (0,10), sticky="ew")

        # Key part (generation)
        self.keyFrame = customtkinter.CTkFrame(self, fg_color=self.cget("fg_color"))
        self.keyFrame.columnconfigure(0, weight=0)
        self.keyFrame.columnconfigure(1, weight=1)
        self.keyFrame.grid(row = 5, column = 0, columnspan=3, padx=20, pady=20, sticky="ew")
        button1 = customtkinter.CTkButton(self.keyFrame, 
                                          compound="right",
                                          text ="Generate Key      ",
                                          image=dice_image,
                                          command = self.generateKey)
        button1.grid(row = 0, column = 0, padx = (0,5), pady = 0)

        self.entryKey = customtkinter.CTkEntry(self.keyFrame, placeholder_text="Input key and hit enter")
        self.entryKey.bind("<Return>", command=lambda x: self.setKeyFromEntry())
        self.entryKey.grid(row=0, column=1, padx=(5, 0), pady=0, sticky="ew")

        # Key display
        self.currentKeyFrame = customtkinter.CTkFrame(self.keyFrame, fg_color=self.cget("fg_color"))
        self.currentKeyFrame.columnconfigure(0, weight=1)
        self.currentKeyFrame.grid(row = 1, column = 0, padx = (0,5), pady = 5, sticky="ew")
        self.currentKeyFrameLabel = customtkinter.CTkLabel(self.currentKeyFrame, 
                                                     text="Current Key:",
                                                     corner_radius=6, 
                                                     fg_color=['#979DA2', 'gray29'], 
                                                     text_color=['#DCE4EE', '#DCE4EE'])
        self.currentKeyFrameLabel.grid(row=0, column=0, columnspan=1, padx=0, pady=0, sticky="ew")

        self.currentKeyFrameNumber = customtkinter.CTkLabel(self.keyFrame, 
                                                     text="0",
                                                     anchor="w")
        self.currentKeyFrameNumber.grid(row=1, column=1, columnspan=1, padx=(5, 0), pady=0, sticky="ew")

        self.encodingButton = customtkinter.CTkButton(self.keyFrame,
                                          text ="ASCII",
                                          command = self.swapCode)
        self.encodingButton.grid(row = 2, column = 0, padx = (0,5), pady=(0, 5))

        # Analysis
        button2 = customtkinter.CTkButton(self.keyFrame,
                                          compound="right",
                                          text ="Attack                   ",
                                          image=swords_image,
                                          command = self.attack)
        button2.grid(row = 3, column = 0, padx = (0,5), pady = 20, sticky="new")

        # Number of keys to be recommended
        self.keyNumFrame = customtkinter.CTkFrame(self.keyFrame)
        self.keyNumFrame.columnconfigure(1, weight=1)
        self.keyNumFrame.grid(row = 3, column = 1, padx =0, pady = 20, sticky="new")

        self.keyLenFrame = customtkinter.CTkFrame(self.keyNumFrame)
        self.keyLenFrame.grid(row = 0, column = 0, padx=0, pady=0, sticky="new")
        self.keyLenFrame.grid_columnconfigure(0, weight=1)
        self.keyLenFrame.grid_rowconfigure(0, weight=1)
        self.ds_frame_label = customtkinter.CTkLabel(self.keyLenFrame, 
                                                     text="Number of keys",
                                                     corner_radius=6)
        self.ds_frame_label.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")


        self.seg_button = customtkinter.CTkSegmentedButton(self.keyNumFrame)
        self.seg_button.grid(row=0, column=1, padx=0, pady=0, sticky="new")
        self.seg_button.configure(values=["1", "2", "3", "4", "5", "6", "7", "All"])
        self.seg_button.set("1")

        # language to be used
        self.langTextFrame = customtkinter.CTkFrame(self.keyNumFrame)
        self.langTextFrame.grid(row = 1, column = 0, padx=0, pady=(5,0), sticky="new")
        self.langTextFrame.grid_columnconfigure(0, weight=1)
        self.langTextFrame.grid_rowconfigure(0, weight=1)
        self.langLabel = customtkinter.CTkLabel(self.langTextFrame, 
                                                     text="Language",
                                                     corner_radius=6)
        self.langLabel.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")

        self.seg_lang = customtkinter.CTkSegmentedButton(self.keyNumFrame)
        self.seg_lang.grid(row=1, column=1, padx=0, pady=(5,0), sticky="new")
        self.seg_lang.configure(values=["English", "French", "German", "Italian", "Portuguese", "Spanish"])
        self.seg_lang.set("English")

        # Attack textbox
        self.keyTextbox = customtkinter.CTkTextbox(self.keyFrame, state="disabled")
        self.keyTextbox.grid(row=4, column=0, columnspan=2, padx=0, pady=0, sticky="ew")
        self.keyTextbox.insert("0.0", "")
    
    def encrypt(self):
        inputText = self.entry.get("0.0", tk.END)

        encoding = self.code
        if encoding == "ASCII":
            cipherText = self.system2.encrypt(inputText)
        else:
            cipherText = self.system.encrypt(inputText)

        
        self.textbox.configure(state="normal")
        self.textbox.delete('1.0', tk.END)
        self.textbox.insert("0.0", cipherText)
        self.textbox.configure(state="disabled")
        
    def decrypt(self):
        encoding = self.code
        
        inputText = self.entry.get("0.0", tk.END)

        if encoding == "ASCII":
            cipherText = self.system2.decrypt(inputText)
        else:
            cipherText = self.system.decrypt(inputText)
        
        self.textbox.configure(state="normal")
        self.textbox.delete('0.0', tk.END)
        self.textbox.insert("0.0", cipherText)
        self.textbox.configure(state="disabled")
    
    def copyToClipboard(self):
        self.clipboard_clear()
        self.clipboard_append(self.textbox.get('1.0', 'end-1c'))

    def swap(self):
        self.entry.delete('0.0', tk.END)
        self.entry.insert("0.0", self.textbox.get('1.0', 'end-1c'))
    
    def clearInput(self):
        self.entry.delete('0.0', tk.END)

    def attack(self):
        encoding = self.code
        self.system.lang = self.seg_lang.get()
        self.system2.lang = self.seg_lang.get()

        inputText = self.entry.get("0.0", tk.END)
        
        if encoding == "ASCII":
            self.system2.setText(inputText)
            cleanString = self.system2.getCleanString()
            if cleanString != "":
                numKeysStr = self.seg_button.get()

                self.bestKeys, self.bestKeys2 = self.system2.getBestKeys2(cleanString)

                if numKeysStr == "All":
                    numKeys = len(self.bestKeys)
                else:
                    numKeys = int(numKeysStr)
                
                self.keyTextbox.configure(state="normal")

                if numKeysStr == "All":
                    tempSys = Desplazamiento(text=cleanString, codi="0a95")
                    # Display recommended keys

                    tempSys.lang = self.seg_lang.get()
                    outputString = "Here is a list of keys with the text that results from deciphering with those keys. It has been ordered assuming the language of the plaintext is "+self.system2.lang+".\n\n"


                    for i in range(numKeys):
                        key = self.bestKeys[i][0]

                        tempSys.setKey(key)
                        result = tempSys.decrypt()
                        splitText = True
                        if len(result) <= 100:
                            splitText = False
                        else:
                            rInt = randint(31, len(result)-61)
                        
                        if splitText:
                            outputString += str(key) + ":\n" + result[:30]+"..."+result[rInt:rInt+30]+"..."+ result[-30:] + "\n\n"
                        else:
                            outputString += str(key) + ":\n" + result + "\n\n"
                else:
                    outputString = "Keep in mind that frequency analysis may be ineffective for short inputs.\nTest the following keys for " + self.system.lang + ":\n"

                    for i in range(numKeys):
                        key = self.bestKeys[i][0]
                        key2 = self.bestKeys2[i][0]
                        outputString += str(key) + "\n" + str(key2) + "\n"

                self.keyTextbox.delete('0.0', tk.END)
                self.keyTextbox.insert("0.0", outputString)
                self.keyTextbox.configure(state="disabled")
            else:
                self.keyTextbox.configure(state="normal")
                self.keyTextbox.delete('0.0', tk.END)
                self.keyTextbox.insert("0.0", "The input box is empty!")
                self.keyTextbox.configure(state="disabled")


        else:
            self.system.setText(inputText)
            cleanString = self.system.getCleanString()
            if cleanString != "":
                numKeysStr = self.seg_button.get()

                if numKeysStr == "All":
                    numKeys = 26
                else:
                    numKeys = int(numKeysStr)
                keys1, keys2 = self.system.getBestKeys(cleanString, num=numKeys)
                if numKeysStr == "All":
                    tempSys = Desplazamiento(text=cleanString)
                    # Display recommended keys
                    tempSys.lang = self.seg_lang.get()
                    outputString = "Here is a list of keys with the text that results from deciphering with those keys. It has been ordered assuming the language of the plaintext is "+ self.system.lang +".\n\n"

                    
                    # Display recommended keys
                    self.keyTextbox.configure(state="normal")
                    
                    for i in range(numKeys):
                        key1 = keys1[i][0]
                        key2 = keys2[i][0]

                        tempSys.setKey(key1)
                        result = tempSys.decrypt()
                        splitText = True
                        if len(result) <= 100:
                            splitText = False
                        else:
                            rInt = randint(31, len(result)-61)
                        if splitText:
                            outputString += str(keys1[i][0]) + ":\n" + result[:30]+"..."+result[rInt:rInt+30]+"..."+ result[-30:] + "\n\n"
                        else:
                            outputString += str(keys1[i][0]) + ":\n" + result + "\n\n"

                        if key1 != key2:
                            tempSys.setKey(key2)
                            result = tempSys.decrypt()
                            splitText = True
                            if len(result) <= 100:
                                splitText = False
                            else:
                                rInt = randint(31, len(result)-61)
                            if splitText:
                                outputString += str(keys2[i][0]) + ":\n" + result[:30]+"..."+result[rInt:rInt+30]+"..."+ result[-30:] + "\n\n"
                            else:
                                outputString += str(keys2[i][0]) + ":\n" + result + "\n\n"
                        outputString += "\n"
                    

                else:
                    # Display recommended keys
                    self.keyTextbox.configure(state="normal")
                    outputString = "Keep in mind that frequency analysis may be ineffective for short inputs.\nTest the following keys for " + self.system.lang + ":\n"
                    
                    for i in range(numKeys):
                        key1 = keys1[i][0]
                        key2 = keys2[i][0]
                        outputString += str(keys1[i][0]) + "\n"
                        if key1 != key2:
                            outputString += str(keys2[i][0]) + "\n"
                        outputString += "\n"

                self.keyTextbox.delete('0.0', tk.END)
                self.keyTextbox.insert("0.0", outputString)
                self.keyTextbox.configure(state="disabled")
            else:
                self.keyTextbox.configure(state="normal")
                self.keyTextbox.delete('0.0', tk.END)
                self.keyTextbox.insert("0.0", "The input box is empty!")
                self.keyTextbox.configure(state="disabled")
    
    def generateKey(self):
        encoding = self.code
        if encoding == "ASCII":
            newKey = self.system2.generateKey()
            self.system2.setKey(newKey)
        else:
            newKey = self.system.generateKey()
            self.system.setKey(newKey)

        newKeyStr = str(newKey)
        self.currentKeyFrameNumber.configure(text=newKeyStr)
        self.currentKey = newKeyStr
    
    def setKeyFromEntry(self):
        encoding = self.code
        inputKey = self.entryKey.get()

        if encoding == "ASCII":
            self.system2.setKey(inputKey)
            newKeyStr = str(self.system2.codeKey)
        else:
            self.system.setKey(inputKey)
            newKeyStr = str(self.system.codeKey)
        
        self.currentKeyFrameNumber.configure(text=newKeyStr)
        self.currentKey = newKeyStr

    def swapCode(self):
        self.system2.setKey(0)
        self.system.setKey(0)

        self.currentKeyFrameNumber.configure(text="0")
        self.currentKey = "0"

        if self.code == "ASCII":
            self.code = "Simple encoding"
        else:
            self.code = "ASCII"
        self.encodingButton.configure(text=self.code)
        

# Vigenere window frame
class VigenerePage(customtkinter.CTkFrame):
    def __init__(self, parent, controller):
        self.system = Vigenere(key=[0])
        self.currentKey = "A = (0)"
        self.brauerString = ""

        customtkinter.CTkFrame.__init__(self, parent)

        self.grid_columnconfigure((0,2), weight=1)
        self.grid_columnconfigure(1, weight=0)

        label = customtkinter.CTkLabel(self,
                                       text="VIGENERE CIPHER",
                                       font=customtkinter.CTkFont(size=20, weight="bold"))
        label.grid(row=0, column=0, columnspan=3, padx=20, pady=(10,0), sticky="w")

        # input
        self.entry = customtkinter.CTkTextbox(self)
        self.entry.grid(row=1, column=0, rowspan=3, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.entry.insert("0.0", "Attack at noon")
        button1 = customtkinter.CTkButton(self, text ="Clear",
                            command = self.clearInput)
        button1.grid(row = 4, column = 0, padx = (20,0), pady = (0,10), sticky="ew")

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

        button1 = customtkinter.CTkButton(self,
                                          compound="right",
                                          text ="Encrypt                ", 
                                          image=lock1_image,
                                          command=self.encrypt)
        button1.grid(row = 2, column = 1, padx = 5, pady = 5, sticky="sew")

        button2 = customtkinter.CTkButton(self, 
                                          compound="right",
                                          text ="Decrypt                ", 
                                          image=lock2_image,
                                          command=self.decrypt)
        button2.grid(row = 3, column = 1, padx = 5, pady = 5, sticky="sew")

        
        # output
        self.textbox = customtkinter.CTkTextbox(self, state="disabled")
        self.textbox.grid(row=1, column=2, rowspan=3, padx=(0,20), pady=(20, 0), sticky="nsew")
        self.textbox.insert("0.0", "")
        button1 = customtkinter.CTkButton(self, text ="Copy",
                            command = self.copyToClipboard)
        button1.grid(row = 4, column = 2, padx = (0,20), pady = (0,10), sticky="ew")

        # Key part (generation)
        self.keyFrame = customtkinter.CTkFrame(self, fg_color=self.cget("fg_color"))
        self.keyFrame.columnconfigure(0, weight=0)
        self.keyFrame.columnconfigure(1, weight=1)
        self.keyFrame.grid(row = 5, column = 0, columnspan=3, padx=20, pady=20, sticky="ew")
        button1 = customtkinter.CTkButton(self.keyFrame, 
                                          compound="right",
                                          text ="Generate Key      ",
                                          image=dice_image,
                                          command = self.generateKey)
        button1.grid(row = 0, column = 0, padx = (0,5), pady = 0)

        self.entryKey = customtkinter.CTkEntry(self.keyFrame, placeholder_text="Input key and hit enter")
        self.entryKey.bind("<Return>", command=lambda x: self.setKeyFromEntry())
        self.entryKey.grid(row=0, column=1, padx=(5, 0), pady=0, sticky="ew")

        # Key display
        self.currentKeyFrame = customtkinter.CTkFrame(self.keyFrame, fg_color=self.cget("fg_color"))
        self.currentKeyFrame.columnconfigure(0, weight=1)
        self.currentKeyFrame.grid(row = 1, column = 0, padx = (0,5), pady = 5, sticky="ew")
        self.currentKeyFrameLabel = customtkinter.CTkLabel(self.currentKeyFrame, 
                                                     text="Current Key:",
                                                     corner_radius=6, 
                                                     fg_color=['#979DA2', 'gray29'], 
                                                     text_color=['#DCE4EE', '#DCE4EE'])
        self.currentKeyFrameLabel.grid(row=0, column=0, columnspan=1, padx=0, pady=0, sticky="ew")

        self.currentKeyFrameNumber = customtkinter.CTkLabel(self.keyFrame, 
                                                     text="A = (0)",
                                                     anchor="w")
        self.currentKeyFrameNumber.grid(row=1, column=1, columnspan=1, padx=(5, 0), pady=0, sticky="ew")

        # Analysis
        button2 = customtkinter.CTkButton(self.keyFrame,
                                          compound="right",
                                          text ="Attack                   ",
                                          image=swords_image,
                                          command = self.attack)
        button2.grid(row = 2, column = 0, padx = (0,5), pady = (25,0), sticky="new")

        # Number of keys to be recommended
        self.keyNumFrame = customtkinter.CTkFrame(self.keyFrame)
        self.keyNumFrame.columnconfigure(1, weight=1)
        self.keyNumFrame.grid(row = 2, column = 1, padx =0, pady = 20, sticky="new")

        self.keyLenFrame = customtkinter.CTkFrame(self.keyNumFrame)
        self.keyLenFrame.grid(row = 0, column = 0, padx=(5,0), pady=(5,0), sticky="ew")
        self.keyLenFrame.grid_columnconfigure(0, weight=1)
        self.keyLenFrame.grid_rowconfigure(0, weight=1)
        self.ds_frame_label = customtkinter.CTkLabel(self.keyLenFrame, 
                                                     text="Number of keys",
                                                     corner_radius=6)
        self.ds_frame_label.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")

        self.seg_button = customtkinter.CTkSegmentedButton(self.keyNumFrame)
        self.seg_button.grid(row=0, column=1, padx=(0,5), pady=(5,0), sticky="new")
        self.seg_button.configure(values=["1", "2", "3", "4", "5", "6", "7", "All"])
        self.seg_button.set("1")

        # language to be used
        self.langTextFrame = customtkinter.CTkFrame(self.keyNumFrame)
        self.langTextFrame.grid(row = 1, column = 0, padx=(5,0), pady=5, sticky="new")
        self.langTextFrame.grid_columnconfigure(0, weight=1)
        self.langTextFrame.grid_rowconfigure(0, weight=1)
        self.langLabel = customtkinter.CTkLabel(self.langTextFrame, 
                                                     text="Language",
                                                     corner_radius=6)
        self.langLabel.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")

        self.seg_lang = customtkinter.CTkSegmentedButton(self.keyNumFrame)
        self.seg_lang.grid(row=1, column=1, padx=(0,5), pady=5, sticky="new")
        self.seg_lang.configure(values=["English", "French", "German", "Italian", "Portuguese", "Spanish"])
        self.seg_lang.set("English")

        # Brauer stuff
        buttonBrauer = customtkinter.CTkButton(self.keyFrame,
                                          text ="Analysis (Brauer)",
                                          command = self.popUP)
        buttonBrauer.grid(row = 3, column = 0, padx = (0,5), pady = (10,5), sticky="new")

        # Number of keys to be recommended
        self.brauerFrame = customtkinter.CTkFrame(self.keyFrame)
        self.brauerFrame.columnconfigure(1, weight=1)
        self.brauerFrame.grid(row = 3, column = 1, padx =0, pady = 5, sticky="new")

        self.brauerSegFrame = customtkinter.CTkFrame(self.brauerFrame)
        self.brauerSegFrame.grid(row = 0, column = 0, padx=(5,0), pady=5, sticky="ew")
        self.brauerSegFrame.grid_columnconfigure(0, weight=1)
        self.brauerSegFrame.grid_rowconfigure(0, weight=1)
        self.ds_frame_labelBrauer = customtkinter.CTkLabel(self.brauerSegFrame, 
                                                     text="Key length",
                                                     corner_radius=6)
        self.ds_frame_labelBrauer.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")

        self.seg_buttonBrauer = customtkinter.CTkSegmentedButton(self.brauerFrame)
        self.seg_buttonBrauer.grid(row=0, column=1, padx=(0,5), pady=5, sticky="new")
        self.seg_buttonBrauer.configure(values=["2", "3", "4", "5", "6", "7", "8"])
        self.seg_buttonBrauer.set("5")

        # Attack textbox
        self.keyTextbox = customtkinter.CTkTextbox(self.keyFrame, state="disabled")
        self.keyTextbox.grid(row=4, column=0, columnspan=2, padx=0, pady=0, sticky="ew")
        self.keyTextbox.insert("0.0", "")
    
    def encrypt(self):
        inputText = self.entry.get("0.0", tk.END)

        cipherText = self.system.encrypt(inputText)
        self.textbox.configure(state="normal")
        self.textbox.delete('1.0', tk.END)
        self.textbox.insert("0.0", cipherText)
        self.textbox.configure(state="disabled")
        
    def decrypt(self):
        inputText = self.entry.get("0.0", tk.END)

        cipherText = self.system.decrypt(inputText)
        self.textbox.configure(state="normal")
        self.textbox.delete('0.0', tk.END)
        self.textbox.insert("0.0", cipherText)
        self.textbox.configure(state="disabled")
    
    def copyToClipboard(self):
        self.clipboard_clear()
        self.clipboard_append(self.textbox.get('1.0', 'end-1c'))

    def swap(self):
        self.entry.delete('0.0', tk.END)
        self.entry.insert("0.0", self.textbox.get('1.0', 'end-1c'))
    
    def clearInput(self):
        self.entry.delete('0.0', tk.END)

    def attack(self):
        self.system.lang = self.seg_lang.get()

        inputText = self.entry.get("0.0", tk.END)
        self.system.setText(inputText)
        cleanString = self.system.getCleanString()
        if cleanString != "":
            numKeysStr = self.seg_button.get()
            afterMessage = ""
            keys = self.system.getBestKeys(cleanString)
            

            if numKeysStr == "All":
                # Display recommended keys
                
                self.keyTextbox.configure(state="normal")
                outputString = "Keep in mind that frequency analysis may be ineffective for short inputs, furthermore, longer keys may reduce its effectiveness.\nTest the following keys for " + self.system.lang + ". The keys have been ordered according to the coincidence index of their length. Additionally, 3 key candidates are given per key length, these candidates are computed with 3 different criteria:\n1) Maximum sum of products\n2) Minimum difference with sum of squared probabilities of the language\n3) Most persistent letter\n\n"

                tempSys = Vigenere(text=cleanString)
                tempSys.lang = self.seg_lang.get()
                afterMessage = "\n\nAny key longer than {} will result in a one-time pad.".format(len(keys)+1)

                for i in range(len(keys)):
                    outputString += "For a key of length {}:\n".format(len(keys[i][0]))
                    key1 = keys[i][0]
                    key2 = keys[i][1]
                    key3 = keys[i][2]


                    tempSys.setKey(key1)
                    result = tempSys.decrypt()
                    splitText = True
                    if len(result) <= 100:
                        splitText = False
                    else:
                        rInt = randint(31, len(result)-61)
                    if splitText:
                        outputString += "\t1){}: ".format(key1)+ result[:30]+"..."+result[rInt:rInt+30]+"..."+ result[-30:] + "\n"
                    else:
                        outputString += "\t1){}: ".format(key1) + result + "\n"

                    tempSys.setKey(key2)
                    result = tempSys.decrypt()
                    splitText = True
                    if len(result) <= 100:
                        splitText = False
                    else:
                        rInt = randint(31, len(result)-61)
                    if splitText:
                        outputString += "\t1){}: ".format(key2) + result[:30]+"..."+result[rInt:rInt+30]+"..."+ result[-30:] + "\n"
                    else:
                        outputString += "\t1){}: ".format(key2) + result + "\n"

                    tempSys.setKey(key3)
                    result = tempSys.decrypt()
                    splitText = True
                    if len(result) <= 100:
                        splitText = False
                    else:
                        rInt = randint(31, len(result)-61)
                    if splitText:
                        outputString += "\t1){}: ".format(key3) + result[:30]+"..."+result[rInt:rInt+30]+"..."+ result[-30:] + "\n"
                    else:
                        outputString += "\t1){}: ".format(key3) + result + "\n"

                    
                    outputString += "\n"
                
                outputString += afterMessage
                self.keyTextbox.delete('0.0', tk.END)
                self.keyTextbox.insert("0.0", outputString)
                self.keyTextbox.configure(state="disabled")

            else:

                numKeys = int(numKeysStr)
                if len(keys) < numKeys:
                    numKeys = len(keys)
                    afterMessage = "\n\nThe largest key length possible for the given ciphertext is {}. Anything longer will result in a one-time pad.".format(len(keys)+1)
                else:
                    keys = keys[:numKeys]
                # Display recommended keys
                self.keyTextbox.configure(state="normal")
                outputString = "Keep in mind that frequency analysis may be ineffective for short inputs, furthermore, longer keys may reduce its effectiveness.\nTest the following keys for " + self.system.lang + ". The keys have been ordered according to the coincidence index of their length. Additionally, 3 key candidates are given per key length, these candidates are computed with 3 different criteria:\n1) Maximum sum of products\n2) Minimum difference with sum of squared probabilities of the language\n3) Most persistent letter\n\n"

                for i in range(numKeys):
                    outputString += "For a key of length {}:\n".format(len(keys[i][0]))
                    key1 = keys[i][0]
                    key2 = keys[i][1]
                    key3 = keys[i][2]
                    outputString += "\t1){}\n".format(key1)
                    outputString += "\t2){}\n".format(key2)
                    outputString += "\t3){}\n\n".format(key3)
                outputString += afterMessage
                self.keyTextbox.delete('0.0', tk.END)
                self.keyTextbox.insert("0.0", outputString)
                self.keyTextbox.configure(state="disabled")



        else:
            self.keyTextbox.configure(state="normal")
            self.keyTextbox.delete('0.0', tk.END)
            self.keyTextbox.insert("0.0", "The input box is empty!")
            self.keyTextbox.configure(state="disabled")
    
    def generateKey(self):
        newKey = self.system.generateKey()
        self.system.setKey(newKey)

        newKeyStr = ""
        for i in newKey:
            newKeyStr += chr(i+65)
        self.currentKey = newKeyStr
        newKeyStr += " = ("+str(newKey)[1:-1]+")"
        self.currentKeyFrameNumber.configure(text=newKeyStr)
    
    def setKeyFromEntry(self):
        inputKey = self.entryKey.get()
        self.system.setKey(inputKey)

        newKeyStr = ""
        for i in self.system.codeKey:
            newKeyStr += chr(i+65)
        self.currentKey = newKeyStr

        newKeyStr += " = ("+str(self.system.codeKey)[1:-1]+")"
        self.currentKeyFrameNumber.configure(text=newKeyStr)
    
    def popUP(self):
        # get key length
        keyLen = int(self.seg_buttonBrauer.get())

        # get input string
        inputText = self.entry.get("1.0", "end-1c")
        self.system.setText(inputText)
        cleanString = self.system.getCleanString()
        self.originalBrauerMsg = cleanString
        if len(cleanString) > 0:
            upperBound = min(keyLen, len(cleanString))
            newStr = ""
            polygonsString = "\tW1: "
            for i in range(upperBound):
                for j in range(i, len(cleanString), keyLen):
                    newStr += cleanString[j]
                    polygonsString += cleanString[j]

                newStr += " "
                if i < upperBound-1:
                    polygonsString += "\n\tW" + str(i+2) + ": "

            self.polygonString = polygonsString
            self.brauerString = newStr[:-1].lower()

            self.popUp2() # xD
    
    def popUp2(self):
        # create popUp window (more like pop back)
        top = customtkinter.CTkToplevel()
        top.geometry("900x500")
        top.title("PiCKED")
        top.after(250, lambda: top.iconbitmap(path_to_icon))
        top.grid_columnconfigure(0, weight=1)
        top.grid_rowconfigure(0, weight=1)
        
        
        scrollable_frame = customtkinter.CTkScrollableFrame(top, label_text="")
        scrollable_frame.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")
        scrollable_frame.grid_columnconfigure(1, weight=1)

        customtkinter.CTkLabel(scrollable_frame, 
                            text= "BRAUER QUIVER", 
                            font=customtkinter.CTkFont(size=20, weight="bold")).grid(column=0,row=0)

        # image frame
        imgFrame = customtkinter.CTkFrame(scrollable_frame)
        imgFrame.configure(width=400,height=400)
        imgFrame.grid_propagate(False)
        imgFrame.columnconfigure(0, weight=1)
        imgFrame.rowconfigure(0, weight=1)
        imgFrame.grid(column = 0, row = 1, rowspan=1, padx=(20,5), pady=(10,0), sticky="nsew")
        imageLabel = customtkinter.CTkLabel(imgFrame, 
                                                text="",
                                                corner_radius=6,
                                                fg_color=['#979DA2', 'gray29'],
                                                text_color=['#DCE4EE', '#DCE4EE'])
        imageLabel.grid(column = 0, row = 0, padx=0, pady=0, sticky="nsew")

        # Calcular algebra stuff
        self.resultados = obtener_resultados(self.brauerString)

        try:
            the_image_path = crear_grafo(self.resultados["Ciclos"])
            the_image = Image.open(the_image_path)
            the_image.thumbnail((600,600), Image.LANCZOS)
            daPath = os.path.join("PiCKED App","Brauervisualization.ppm")
            the_image.save(daPath)

            # Change label contents
            imgObject = PhotoImage(file = daPath)
            
            imageLabel.configure(image=imgObject)

            # save button
            buttonSave = customtkinter.CTkButton(scrollable_frame, 
                                                        text = "Save",
                                                        command = lambda : self.saveQuiver(self.resultados))
            buttonSave.grid(column = 0, row = 2, padx = (20,5), pady = (0,10), sticky="new")
        except:
            the_image = Image.open(path_to_sampleQuiver)
            the_image.thumbnail((600,600), Image.LANCZOS)
            daPath = os.path.join("PiCKED App","Brauervisualization.ppm")
            the_image.save(daPath)

            # Change label contents
            imgObject = PhotoImage(file = daPath)
            
            imageLabel.configure(image=imgObject)

            # save button
            buttonSave = customtkinter.CTkButton(scrollable_frame, 
                                                        text = "Save",
                                                        command = self.saveQuiverDemo) 
            buttonSave.grid(column = 0, row = 2, padx = (20,5), pady = (0,10), sticky="new")


        # output
        ICInfo = self.system.getFreqIndexForKeyLen(self.originalBrauerMsg, int(self.seg_buttonBrauer.get()))

        outStr = "Vigenere ciphertext:\n\t" + self.originalBrauerMsg.lower() + "\n\n"
        outStr += "Presumed key length:\n\t" + self.seg_buttonBrauer.get() + "\n\nPolygons (cosets):\n"
        counter = 1
        for polygon in self.resultados["R1"]:
            outStr += "\tW" + str(counter) + ": " + polygon + "\n"
            counter += 1
        outStr += "\nVertices:\n\t{ " 
        lsVert = list(self.resultados["R0"])
        for i in range(len(lsVert)):
            if i < len(lsVert)-1:
                outStr += lsVert[i] + " , "
            else:
                outStr += lsVert[i] + " }\n\n"
        outStr += "Number of loops:\n\t" + str(sum(self.resultados["NLoops"].values())) + "\n\n"
        outStr += "Dimension of the Brauer Configuration Algebra:\n\t" + str(self.resultados["D"]) + "\n\n"
        outStr += "Dimension of the center:\n\t" + str(self.resultados["DZ"]) + "\n\n"
        if ICInfo != None:
            outStr += "Average index of coincidence for cosets of length at least 2:\n\t" + str(ICInfo[1]) + "\n\nIndices of coincidence of each coset of length at least 2:\n"
            for coset in ICInfo[0]:
                outStr += "\t"+ coset + ":\n\t\t" + str(ICInfo[0][coset]) + "\n\n"
        else:
            outStr += "Since the key is at least as long as the ciphertext, no information can be extracted."
        
        
        textbox = customtkinter.CTkTextbox(scrollable_frame, state="normal")
        textbox.grid(row=1, column=1, rowspan=2, padx=(5,20), pady=(10, 0), sticky="nsew")
        textbox.insert("0.0", outStr)
        textbox.configure(state="disabled")

        
    
    def saveQuiver(self, resultados):
        file = filedialog.asksaveasfile(mode='wb', 
                                        filetypes = (("png","*.png"),
                                                    ('All files', '*.*')),
                                        defaultextension=".png")
        if file:
            crear_grafo(resultados["Ciclos"], file.name)
    
    def saveQuiverDemo(self):
        myImage = Image.open(path_to_sampleQuiver)
        file = filedialog.asksaveasfile(mode='wb', 
                                        filetypes = (("png","*.png"),
                                                    ('All files', '*.*')),
                                        defaultextension=".png")
        if file:
            myImage.save(file) # saves the image to the input file name. 


# Permutacion window frame
class PermutationPage(customtkinter.CTkFrame):
    def __init__(self, parent, controller):
        self.lastAttackedText = ""
        self.system = Permutacion(key=[0])
        self.currentKey = "(0)"

        customtkinter.CTkFrame.__init__(self, parent)

        self.grid_columnconfigure((0,2), weight=1)
        self.grid_columnconfigure(1, weight=0)

        label = customtkinter.CTkLabel(self,
                                       text="PERMUTATION CIPHER",
                                       font=customtkinter.CTkFont(size=20, weight="bold"))
        label.grid(row=0, column=0, columnspan=3, padx=20, pady=(10,0), sticky="w")

        # input
        self.entry = customtkinter.CTkTextbox(self)
        self.entry.grid(row=1, column=0, rowspan=3, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.entry.insert("0.0", "Attack at noon")
        button1 = customtkinter.CTkButton(self, text ="Clear",
                            command = self.clearInput)
        button1.grid(row = 4, column = 0, padx = (20,0), pady = (0,10), sticky="ew")

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

        button1 = customtkinter.CTkButton(self,
                                          compound="right",
                                          text ="Encrypt                ", 
                                          image=lock1_image,
                                          command=self.encrypt)
        button1.grid(row = 2, column = 1, padx = 5, pady = 5, sticky="sew")

        button2 = customtkinter.CTkButton(self, 
                                          compound="right",
                                          text ="Decrypt                ", 
                                          image=lock2_image,
                                          command=self.decrypt)
        button2.grid(row = 3, column = 1, padx = 5, pady = 5, sticky="sew")

        
        # output
        self.textbox = customtkinter.CTkTextbox(self, state="disabled")
        self.textbox.grid(row=1, column=2, rowspan=3, padx=(0,20), pady=(20, 0), sticky="nsew")
        self.textbox.insert("0.0", "")
        button1 = customtkinter.CTkButton(self, text ="Copy",
                            command = self.copyToClipboard)
        button1.grid(row = 4, column = 2, padx = (0,20), pady = (0,10), sticky="ew")

        # Key part (generation)
        self.keyFrame = customtkinter.CTkFrame(self, fg_color=self.cget("fg_color"))
        self.keyFrame.columnconfigure(0, weight=0)
        self.keyFrame.columnconfigure(1, weight=1)
        self.keyFrame.grid(row = 5, column = 0, columnspan=3, padx=20, pady=20, sticky="ew")
        button1 = customtkinter.CTkButton(self.keyFrame, 
                                          compound="right",
                                          text ="Generate Key      ",
                                          image=dice_image,
                                          command = self.generateKey)
        button1.grid(row = 0, column = 0, padx = (0,5), pady = 0)

        self.entryKey = customtkinter.CTkEntry(self.keyFrame, placeholder_text="Input key and hit enter")
        self.entryKey.bind("<Return>", command=lambda x: self.setKeyFromEntry())
        self.entryKey.grid(row=0, column=1, padx=(5, 0), pady=0, sticky="ew")

        # Key display
        self.currentKeyFrame = customtkinter.CTkFrame(self.keyFrame, fg_color=self.cget("fg_color"))
        self.currentKeyFrame.columnconfigure(0, weight=1)
        self.currentKeyFrame.grid(row = 1, column = 0, padx = (0,5), pady = 5, sticky="ew")
        self.currentKeyFrameLabel = customtkinter.CTkLabel(self.currentKeyFrame, 
                                                     text="Current Key:",
                                                     corner_radius=6, 
                                                     fg_color=['#979DA2', 'gray29'], 
                                                     text_color=['#DCE4EE', '#DCE4EE'])
        self.currentKeyFrameLabel.grid(row=0, column=0, columnspan=1, padx=0, pady=0, sticky="ew")

        self.currentKeyFrameNumber = customtkinter.CTkLabel(self.keyFrame, 
                                                     text="(0)",
                                                     anchor="w")
        self.currentKeyFrameNumber.grid(row=1, column=1, columnspan=1, padx=(5, 0), pady=0, sticky="ew")

        # Analysis
        button2 = customtkinter.CTkButton(self.keyFrame,
                                          compound="right",
                                          text ="Attack                   ",
                                          image=swords_image,
                                          command = self.attack)
        button2.grid(row = 2, column = 0, padx = (0,5), pady = 20, sticky="new")

        # Number of keys to be recommended
        self.keyNumFrame = customtkinter.CTkFrame(self.keyFrame)
        self.keyNumFrame.columnconfigure(1, weight=1)
        self.keyNumFrame.grid(row = 2, column = 1, padx =0, pady = 20, sticky="new")

        self.keyLenFrame = customtkinter.CTkFrame(self.keyNumFrame)
        self.keyLenFrame.grid(row = 0, column = 0, padx=0, pady=0, sticky="new")
        self.keyLenFrame.grid_columnconfigure(0, weight=1)
        self.keyLenFrame.grid_rowconfigure(0, weight=1)
        self.ds_frame_label = customtkinter.CTkLabel(self.keyLenFrame, 
                                                     text="Number of keys",
                                                     corner_radius=6)
        self.ds_frame_label.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")


        self.seg_button = customtkinter.CTkSegmentedButton(self.keyNumFrame)
        self.seg_button.grid(row=0, column=1, padx=(0, 5), pady=0, sticky="new")
        self.seg_button.configure(values=["10", "100", "1000", "46232"])
        self.seg_button.set("10")
        
        # Attack textbox
        self.keyTextbox = customtkinter.CTkTextbox(self.keyFrame, state="disabled")
        self.keyTextbox.grid(row=3, column=0, columnspan=2, padx=0, pady=0, sticky="ew")
        self.keyTextbox.configure(state="normal")
        self.keyTextbox.insert("0.0", "This brute force attack can take some time.")
        self.keyTextbox.configure(state="disabled")
    
    def encrypt(self):
        inputText = self.entry.get("0.0", tk.END)

        cipherText = self.system.encrypt(inputText)
        self.textbox.configure(state="normal")
        self.textbox.delete('1.0', tk.END)
        self.textbox.insert("0.0", cipherText)
        self.textbox.configure(state="disabled")
        
    def decrypt(self):
        inputText = self.entry.get("0.0", tk.END)

        cipherText = self.system.decrypt(inputText)
        self.textbox.configure(state="normal")
        self.textbox.delete('0.0', tk.END)
        self.textbox.insert("0.0", cipherText)
        self.textbox.configure(state="disabled")
    
    def copyToClipboard(self):
        self.clipboard_clear()
        self.clipboard_append(self.textbox.get('1.0', 'end-1c'))

    def swap(self):
        self.entry.delete('0.0', tk.END)
        self.entry.insert("0.0", self.textbox.get('1.0', 'end-1c'))
    
    def clearInput(self):
        self.entry.delete('0.0', tk.END)

    def attack(self):

        inputText = self.entry.get("0.0", tk.END)
        self.system.setText(inputText)
        cleanString = self.system.getCleanString()
        if cleanString != "":
            numKeys = int(self.seg_button.get())

            if self.lastAttackedText != cleanString:
                # This computation is costly
                self.bestKeys = self.system.getBestKeys(cleanString)
                keys = self.bestKeys[:numKeys]
            else:
                keys = self.bestKeys[:numKeys]
            self.lastAttackedText = cleanString
            
            # Display recommended keys
            splitText = True
            if len(cleanString) <= 100:
                splitText = False
            else:
                rInt = randint(31, len(cleanString)-61)

            self.keyTextbox.configure(state="normal")
            outputString = "Here is a list of keys with the text that results from deciphering with those keys. It has been ordered assuming the language of the plaintext is english.\n\n"

            for i in range(numKeys):
                key = keys[i][0]
                text = keys[i][1]
                outputString += str(key) + "\n"
                if splitText:
                    outputString += text[:31]+"..." + text[rInt:rInt+31]+"..."+text[-30:] + "\n"
                else:
                    outputString += text + "\n"
                outputString += "\n"

            self.keyTextbox.delete('0.0', tk.END)
            self.keyTextbox.insert("0.0", outputString)
            self.keyTextbox.configure(state="disabled")
        else:
            self.keyTextbox.configure(state="normal")
            self.keyTextbox.delete('0.0', tk.END)
            self.keyTextbox.insert("0.0", "The input box is empty!")
            self.keyTextbox.configure(state="disabled")
    
    def generateKey(self):
        newKey = self.system.generateKey()
        self.system.setKey(newKey)
        newKeyStr = "("+str(newKey)[1:-1]+")"
        self.currentKeyFrameNumber.configure(text=newKeyStr)
        self.currentKey = newKeyStr
    
    def setKeyFromEntry(self):
        inputKey = self.entryKey.get()

        self.system.setKey(inputKey)
        newKeyStr = "("+str(self.system.codeKey)[1:-1]+")"
        self.currentKeyFrameNumber.configure(text=newKeyStr)
        self.currentKey = newKeyStr


# Substitution window frame
class SubstitutionPage(customtkinter.CTkFrame):
    def __init__(self, parent, controller):
        self.lastAttackedText = ""
        self.system = Substitution(key="A")
        self.currentKey = "A"

        customtkinter.CTkFrame.__init__(self, parent)

        self.grid_columnconfigure((0,2), weight=1)
        self.grid_columnconfigure(1, weight=0)

        label = customtkinter.CTkLabel(self,
                                       text="SUBSTITUTION CIPHER",
                                       font=customtkinter.CTkFont(size=20, weight="bold"))
        label.grid(row=0, column=0, columnspan=3, padx=20, pady=(10,0), sticky="w")

        # input
        self.entry = customtkinter.CTkTextbox(self)
        self.entry.grid(row=1, column=0, rowspan=3, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.entry.insert("0.0", "Attack at noon")
        button1 = customtkinter.CTkButton(self, text ="Clear",
                            command = self.clearInput)
        button1.grid(row = 4, column = 0, padx = (20,0), pady = (0,10), sticky="ew")

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

        button1 = customtkinter.CTkButton(self,
                                          compound="right",
                                          text ="Encrypt                ", 
                                          image=lock1_image,
                                          command=self.encrypt)
        button1.grid(row = 2, column = 1, padx = 5, pady = 5, sticky="sew")

        button2 = customtkinter.CTkButton(self, 
                                          compound="right",
                                          text ="Decrypt                ", 
                                          image=lock2_image,
                                          command=self.decrypt)
        button2.grid(row = 3, column = 1, padx = 5, pady = 5, sticky="sew")

        
        # output
        self.textbox = customtkinter.CTkTextbox(self, state="disabled")
        self.textbox.grid(row=1, column=2, rowspan=3, padx=(0,20), pady=(20, 0), sticky="nsew")
        self.textbox.insert("0.0", "")
        button1 = customtkinter.CTkButton(self, text ="Copy",
                            command = self.copyToClipboard)
        button1.grid(row = 4, column = 2, padx = (0,20), pady = (0,10), sticky="ew")

        # Key part (generation)
        self.keyFrame = customtkinter.CTkFrame(self, fg_color=self.cget("fg_color"))
        self.keyFrame.columnconfigure(0, weight=0)
        self.keyFrame.columnconfigure(1, weight=1)
        self.keyFrame.grid(row = 5, column = 0, columnspan=3, padx=20, pady=20, sticky="ew")
        button1 = customtkinter.CTkButton(self.keyFrame, 
                                          compound="right",
                                          text ="Generate Key      ",
                                          image=dice_image,
                                          command = self.generateKey)
        button1.grid(row = 0, column = 0, padx = (0,5), pady = 0)

        self.entryKey = customtkinter.CTkEntry(self.keyFrame, placeholder_text="Input key and hit enter")
        self.entryKey.bind("<Return>", command=lambda x: self.setKeyFromEntry())
        self.entryKey.grid(row=0, column=1, padx=(5, 0), pady=0, sticky="ew")

        # Key display
        self.currentKeyFrame = customtkinter.CTkFrame(self.keyFrame, fg_color=self.cget("fg_color"))
        self.currentKeyFrame.columnconfigure(0, weight=1)
        self.currentKeyFrame.grid(row = 1, column = 0, padx = (0,5), pady = 5, sticky="ew")
        self.currentKeyFrameLabel = customtkinter.CTkLabel(self.currentKeyFrame, 
                                                     text="Current Key:",
                                                     corner_radius=6, 
                                                     fg_color=['#979DA2', 'gray29'], 
                                                     text_color=['#DCE4EE', '#DCE4EE'])
        self.currentKeyFrameLabel.grid(row=0, column=0, columnspan=1, padx=0, pady=0, sticky="ew")

        self.currentKeyFrameNumber = customtkinter.CTkLabel(self.keyFrame, 
                                                     text="A",
                                                     anchor="w")
        self.currentKeyFrameNumber.grid(row=1, column=1, columnspan=1, padx=(5, 0), pady=0, sticky="ew")

        # Analysis
        button2 = customtkinter.CTkButton(self.keyFrame,
                                          compound="right",
                                          text ="Attack                   ",
                                          image=swords_image,
                                          command = self.attack)
        button2.grid(row = 2, column = 0, padx = (0,5), pady = 20, sticky="new")

        # Number of keys to be recommended
        self.keyNumFrame = customtkinter.CTkFrame(self.keyFrame)
        self.keyNumFrame.columnconfigure(1, weight=1)
        self.keyNumFrame.grid(row = 2, column = 1, padx =0, pady = 20, sticky="new")

        self.keyLenFrame = customtkinter.CTkFrame(self.keyNumFrame)
        self.keyLenFrame.grid(row = 0, column = 0, padx=0, pady=0, sticky="new")
        self.keyLenFrame.grid_columnconfigure(0, weight=1)
        self.keyLenFrame.grid_rowconfigure(0, weight=1)
        self.ds_frame_label = customtkinter.CTkLabel(self.keyLenFrame, 
                                                     text="Number of keys",
                                                     corner_radius=6)
        self.ds_frame_label.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")


        self.seg_button = customtkinter.CTkSegmentedButton(self.keyNumFrame)
        self.seg_button.grid(row=0, column=1, padx=(0, 5), pady=0, sticky="new")
        self.seg_button.configure(values=["10", "100", "1000", "10000"])
        self.seg_button.set("10")
        
        # Attack textbox
        self.keyTextbox = customtkinter.CTkTextbox(self.keyFrame, state="disabled")
        self.keyTextbox.grid(row=3, column=0, columnspan=2, padx=0, pady=0, sticky="ew")
        self.keyTextbox.configure(state="normal")
        self.keyTextbox.insert("0.0", "This brute force attack can take several minutes.")
        self.keyTextbox.configure(state="disabled")
    
    def encrypt(self):
        inputText = self.entry.get("0.0", tk.END)

        self.system.setText(inputText)
        cipherText = self.system.encrypt()

        self.textbox.configure(state="normal")
        self.textbox.delete('1.0', tk.END)
        self.textbox.insert("0.0", cipherText)
        self.textbox.configure(state="disabled")
        
    def decrypt(self):
        inputText = self.entry.get("0.0", tk.END)

        self.system.setText(inputText)
        cipherText = self.system.decrypt()

        self.textbox.configure(state="normal")
        self.textbox.delete('0.0', tk.END)
        self.textbox.insert("0.0", cipherText)
        self.textbox.configure(state="disabled")
    
    def copyToClipboard(self):
        self.clipboard_clear()
        self.clipboard_append(self.textbox.get('1.0', 'end-1c'))

    def swap(self):
        self.entry.delete('0.0', tk.END)
        self.entry.insert("0.0", self.textbox.get('1.0', 'end-1c'))
    
    def clearInput(self):
        self.entry.delete('0.0', tk.END)

    def attack(self):

        inputText = self.entry.get("0.0", tk.END)
        
        self.system.setText(inputText)
        cleanString = self.system.cleanText
        if cleanString != "":
            numKeysStr = self.seg_button.get()
            numKeys = int(numKeysStr)

            if self.lastAttackedText != cleanString:
                # This computation is costly
                if len(cleanString) > 500:
                    self.bestKeys = self.system.getBestKeys(cleanString[:500])
                else:
                    self.bestKeys = self.system.getBestKeys(cleanString)
                keys = self.bestKeys[:numKeys]
            else:
                keys = self.bestKeys[:numKeys]
            self.lastAttackedText = cleanString
            
            # Display recommended keys
            splitText = True
            if len(cleanString) <= 100:
                splitText = False
            elif len(cleanString) > 500:
                rInt = randint(31, 439)
            else:
                rInt = randint(31, len(cleanString)-61)

            self.keyTextbox.configure(state="normal")
            outputString = "Here is a list of prompts with the text that results from deciphering with them. It has been ordered assuming the language of the plaintext is english. The key is a permutation of such prompts.\n\n"

            for i in range(numKeys):
                key = keys[i][0]
                text = keys[i][1]
                outputString += str(key) + "\n"
                if splitText:
                    outputString += text[:31]+"..." + text[rInt:rInt+31]+"..."+text[-30:] + "\n"
                else:
                    outputString += text + "\n"
                outputString += "\n"

            self.keyTextbox.delete('0.0', tk.END)
            self.keyTextbox.insert("0.0", outputString)
            self.keyTextbox.configure(state="disabled")
        else:
            self.keyTextbox.configure(state="normal")
            self.keyTextbox.delete('0.0', tk.END)
            self.keyTextbox.insert("0.0", "The input box is empty!")
            self.keyTextbox.configure(state="disabled")
    
    def generateKey(self):
        self.system.setRandomKey()
        newKey = self.system.key
        self.currentKeyFrameNumber.configure(text=newKey)
        self.currentKey = newKey
    
    def setKeyFromEntry(self):
        inputKey = self.entryKey.get()

        self.system.setKey(inputKey)
        newKeyStr = self.system.key
        self.currentKeyFrameNumber.configure(text=newKeyStr)
        self.currentKey = newKeyStr


# Hill window frame
class HillPage(customtkinter.CTkFrame):

    def __init__(self, parent, controller):
        self.system = Hill()
        self.tsystem = Hill(mode="t")
        self.keyLen = 4
        self.tkeyLen = 4
        self.iv = self.system.getIVStr()
        self.dirty = False
        self.dirtyOutput = False
        
        customtkinter.CTkFrame.__init__(self, parent)
        label = customtkinter.CTkLabel(self,
                                       text="HILL CIPHER",
                                       font=customtkinter.CTkFont(size=20, weight="bold"))
        label.grid(row=0, column=0, padx=20, pady=(10,0), sticky="w")
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)


        self.tabs = customtkinter.CTkTabview(self)
        self.tabs.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
        self.tabs.add("Image")
        self.tabs.add("Text")
        self.tabs.tab("Image").grid_columnconfigure((0,2), weight=1)
        self.tabs.tab("Image").grid_columnconfigure((1,3), weight=0)
        self.tabs.tab("Image").grid_rowconfigure(2, weight=0)
        
        ### IMG PART

        # input image dir: self.imgName
        ### Start img mngmnt
        self.inputImgFrame = customtkinter.CTkFrame(self.tabs.tab("Image"))
        self.inputImgFrame.configure(width=350,height=350)
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
        self.button_explore = customtkinter.CTkButton(self.tabs.tab("Image"), 
                                                    text = "Input image",
                                                    command = lambda: self.browseFiles()) 
        self.button_explore.grid(column = 0, row = 4, padx = (20,0), pady = 0, sticky="new")
        ### End img mngmnt

        # middle buttons
        self.swapFrame = customtkinter.CTkFrame(self.tabs.tab("Image"), width=30, height=30, fg_color=self.cget("fg_color")) #their units in pixels
        button3 = customtkinter.CTkButton(self.swapFrame, 
                                          text ="",
                                          image=larrow_image,
                                          command=self.swap)
        self.swapFrame.grid_propagate(False)
        self.swapFrame.columnconfigure(0, weight=1)
        self.swapFrame.rowconfigure(0,weight=1)
        self.swapFrame.grid(row=1, column=1, sticky="n", pady=0)
        button3.grid(sticky="wens")

        button1 = customtkinter.CTkButton(self.tabs.tab("Image"),
                                          compound="right",
                                          text ="Encrypt                ", 
                                          image=lock1_image,
                                          command=self.encrypt)
        button1.grid(row = 2, column = 1, padx = 5, pady = 5, sticky="sew")

        button2 = customtkinter.CTkButton(self.tabs.tab("Image"),
                                          compound="right",
                                          text ="Decrypt                ", 
                                          image=lock2_image,
                                          command=self.decrypt)
        button2.grid(row = 3, column = 1, padx = 5, pady = 5, sticky="sew")

        # output
        self.outputImgFrame = customtkinter.CTkFrame(self.tabs.tab("Image"))
        self.outputImgFrame.grid_propagate(False)
        self.outputImgFrame.columnconfigure(0, weight=1)
        self.outputImgFrame.rowconfigure(0, weight=1)
        self.outputImgFrame.configure(width=350,height=350)
        self.outputImgFrame.grid(column = 2, row = 1, rowspan=3, padx=(0, 20), pady=0, sticky="nsew")
        self.outputImg = customtkinter.CTkLabel(self.outputImgFrame, 
                                               text="",
                                               corner_radius=6,
                                               fg_color=['#979DA2', 'gray29'],
                                               text_color=['#DCE4EE', '#DCE4EE'])
        self.outputImg.grid(column = 0, row = 0, padx=0, pady=0, sticky="nsew")

        self.buttonSave = customtkinter.CTkButton(self.tabs.tab("Image"), 
                                                  text = "Save",
                                                  command = self.saveFile) 
        self.buttonSave.grid(column = 2, row = 4, padx = (0,20), pady = (0,10), sticky="new")

        # Key Part
        self.keyFrame = customtkinter.CTkFrame(self.tabs.tab("Image"), fg_color=self.cget("fg_color"))
        self.keyFrame.columnconfigure(2, weight=1)
        self.keyFrame.grid(row = 5, column = 0, columnspan=3, padx=20, pady=20, sticky="new")

        # key input
        self.entryKey = customtkinter.CTkEntry(self.keyFrame, placeholder_text="Input key and hit enter")
        self.entryKey.bind("<Return>", command=lambda x: self.setKeyFromEntry())
        self.entryKey.grid(row=1, column=1, columnspan=3, padx=(0, 5), pady=0, sticky="new")
        self.entryIV = customtkinter.CTkEntry(self.keyFrame, placeholder_text="Input initial vector and hit enter (length must coincide with key)")
        self.entryIV.bind("<Return>", command=lambda x: self.setIVFromEntry())
        self.entryIV.grid(row=2, column=1, columnspan=3, padx=(0, 5), pady=0, sticky="new")



        button1 = customtkinter.CTkButton(self.keyFrame, 
                                          compound="right",
                                          text ="Generate Key      ",
                                          image=dice_image,
                                          command = lambda : self.changeKey(int(self.seg_button.get())))
        button1.grid(row = 3, column = 3, padx = (0,5), pady = 0, sticky="new")

        
        self.keyLenFrame = customtkinter.CTkFrame(self.keyFrame)
        self.keyLenFrame.grid(row = 3, column = 1, padx=0, pady=0, sticky="new")
        self.keyLenFrame.grid_columnconfigure(0, weight=1)
        self.keyLenFrame.grid_rowconfigure(0, weight=1)
        self.ds_frame_label = customtkinter.CTkLabel(self.keyLenFrame, 
                                                     text="Key length",
                                                     corner_radius=6)
        self.ds_frame_label.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")

        
        self.seg_button = customtkinter.CTkSegmentedButton(self.keyFrame)
        self.seg_button.grid(row=3, column=2, padx=(0, 5), pady=0, sticky="new")
        self.seg_button.configure(values=["1", "2", "3", "4", "5", "6", "7"])
        self.seg_button.set("5")

        # Key display
        self.currentKeyFrame = customtkinter.CTkFrame(self.keyFrame, fg_color=self.cget("fg_color"))
        self.currentKeyFrame.grid(row = 0, column = 0, rowspan=4, padx=(0,10), pady=0, sticky="new")
        self.currentKeyFrameLabel = customtkinter.CTkLabel(self.currentKeyFrame, 
                                                     text="Current Key & IV (Hex)",
                                                     corner_radius=6, 
                                                     fg_color=['#979DA2', 'gray29'], 
                                                     text_color=['#DCE4EE', '#DCE4EE'])
        self.currentKeyFrameLabel.grid(row=0, column=0, columnspan=1, padx=0, pady=0, sticky="ew")

        self.textbox = customtkinter.CTkTextbox(self.currentKeyFrame, state="disabled", height = 160)
        self.textbox.grid(row=1, column=0, padx=0, pady=0, sticky="nsew")
        self.textbox.insert("0.0", "")

        ### TEXT PART

        # input
        self.tabs.tab("Text").columnconfigure((0,2), weight=1)
        self.tentry = customtkinter.CTkTextbox(self.tabs.tab("Text"))
        self.tentry.grid(row=1, column=0, rowspan=3, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.tentry.delete('0.0', tk.END)
        self.tentry.insert("0.0", "Attack at noon")
        tbutton1 = customtkinter.CTkButton(self.tabs.tab("Text"), text ="Clear",
                            command = self.tclearInput)
        tbutton1.grid(row = 4, column = 0, padx = (20,0), pady = (0,10), sticky="ew")

        self.tswapFrame = customtkinter.CTkFrame(self.tabs.tab("Text"), width=30, height=30, fg_color=self.cget("fg_color")) #their units in pixels
        tbutton3 = customtkinter.CTkButton(self.tswapFrame, 
                                          text ="",
                                          image=larrow_image,
                                          command=self.tswap)
        self.tswapFrame.grid_propagate(False)
        self.tswapFrame.columnconfigure(0, weight=1)
        self.tswapFrame.rowconfigure(0,weight=1)
        self.tswapFrame.grid(row=1, column=1, sticky="n", pady=20)
        tbutton3.grid(sticky="wens")

        tbutton11 = customtkinter.CTkButton(self.tabs.tab("Text"),
                                          compound="right",
                                          text ="Encrypt                ", 
                                          image=lock1_image,
                                          command=self.tencrypt)
        tbutton11.grid(row = 2, column = 1, padx = 5, pady = 5, sticky="sew")

        tbutton2 = customtkinter.CTkButton(self.tabs.tab("Text"), 
                                          compound="right",
                                          text ="Decrypt                ", 
                                          image=lock2_image,
                                          command=self.tdecrypt)
        tbutton2.grid(row = 3, column = 1, padx = 5, pady = 5, sticky="sew")

        
        # output
        self.ttextboxOut = customtkinter.CTkTextbox(self.tabs.tab("Text"), state="disabled")
        self.ttextboxOut.grid(row=1, column=2, rowspan=3, padx=(0,20), pady=(20, 0), sticky="nsew")
        self.ttextboxOut.insert("0.0", "")
        tbutton111 = customtkinter.CTkButton(self.tabs.tab("Text"), text ="Copy",
                            command = self.tcopyToClipboard)
        tbutton111.grid(row = 4, column = 2, padx = (0,20), pady = (0,10), sticky="ew")

        # Key Part
        self.tkeyFrame = customtkinter.CTkFrame(self.tabs.tab("Text"), fg_color=self.cget("fg_color"))
        self.tkeyFrame.columnconfigure(2, weight=1)
        self.tkeyFrame.grid(row = 5, column = 0, columnspan=3, padx=20, pady=20, sticky="new")

        # key input
        self.tentryKey = customtkinter.CTkEntry(self.tkeyFrame, placeholder_text="Input key in hexadecimal and hit enter")
        self.tentryKey.bind("<Return>", command=lambda x: self.tsetKeyFromEntry())
        self.tentryKey.grid(row=0, column=1, columnspan=3, padx=(0, 5), pady=0, sticky="new")

        tbutton12 = customtkinter.CTkButton(self.tkeyFrame, 
                                          compound="right",
                                          text ="Generate Key      ",
                                          image=dice_image,
                                          command = lambda : self.tchangeKey(int(self.tseg_button.get())))
        tbutton12.grid(row = 1, column = 3, padx = (0,5), pady = 0, sticky="new")

        self.tkeyLenFrame = customtkinter.CTkFrame(self.tkeyFrame)
        self.tkeyLenFrame.grid(row = 1, column = 1, padx=0, pady=0, sticky="new")
        self.tkeyLenFrame.grid_columnconfigure(0, weight=1)
        self.tkeyLenFrame.grid_rowconfigure(0, weight=1)
        self.tds_frame_label = customtkinter.CTkLabel(self.tkeyLenFrame, 
                                                     text="Key length",
                                                     corner_radius=6)
        self.tds_frame_label.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")


        self.tseg_button = customtkinter.CTkSegmentedButton(self.tkeyFrame)
        self.tseg_button.grid(row=1, column=2, padx=(0, 5), pady=0, sticky="new")
        self.tseg_button.configure(values=["1", "2", "3", "4", "5", "6", "7"])
        self.tseg_button.set("5")

        # Key display
        self.tcurrentKeyFrame = customtkinter.CTkFrame(self.tkeyFrame, fg_color=self.cget("fg_color"))
        self.tcurrentKeyFrame.grid_propagate(False)
        self.tcurrentKeyFrame.grid(row = 0, column = 0, rowspan=2, padx=(0,10), pady=0, sticky="new")
        self.tcurrentKeyFrameLabel = customtkinter.CTkLabel(self.tcurrentKeyFrame, 
                                                     text="Current Key",
                                                     corner_radius=6, 
                                                     fg_color=['#979DA2', 'gray29'], 
                                                     text_color=['#DCE4EE', '#DCE4EE'])
        self.tcurrentKeyFrameLabel.grid(row=0, column=0, columnspan=1, padx=0, pady=0, sticky="ew")

        self.ttextbox = customtkinter.CTkTextbox(self.tcurrentKeyFrame, state="disabled")
        self.ttextbox.grid(row=1, column=0, padx=0, pady=0, sticky="nsew")
        self.ttextbox.insert("0.0", "")

        self.changeKey(5)
        self.tchangeKey(5)

    def browseFiles(self):
        # image dir
        self.imgName = filedialog.askopenfilename(initialdir = "/",
                                                    title = "Select a File",
                                                    filetypes = (("Picture files",
                                                                "*.png;*.jpg;*.ppm;*.bmp"),
                                                                ('All files', '*.*')))
        if self.imgName != "":
            self.dirty = True
            # file to be encrypted
            # original: self.img
            self.img = np.array(iio.imread(self.imgName)).astype(int)

            self.original_shape = self.img.shape
            

            # file to be displayed
            imgList = self.imgName.split(".")
            self.anyFormatImage = Image.open(self.imgName)
            self.anyFormatImage.thumbnail((500,500), Image.LANCZOS)
            self.originalFormat = imgList[1]
            self.resizedImgName = "hillInput.ppm"
            self.resizedImgName = os.path.join("PiCKED App",self.resizedImgName)
            self.anyFormatImage.save(self.resizedImgName)

            # Change label contents
            imgObject = PhotoImage(file = self.resizedImgName)

            self.inputImg.configure(image=imgObject)

    def tclearInput(self):
        self.tentry.delete('0.0', tk.END)

    def tcopyToClipboard(self):
        self.clipboard_clear()
        self.clipboard_append(self.ttextboxOut.get('1.0', 'end-1c'))

    def encrypt(self):
        if self.dirty:
            self.dirtyOutput = True

            # add padding
            n = self.keyLen
            residue = self.img.shape[0] % n
            if residue != 0:
                newShape = list(self.img.shape)
                newOverallShape = list(self.img.shape)
                newShape[0] = n-residue
                newOverallShape[0] += n-residue
                if len(self.img.shape) < 3:
                    self.img = np.append(self.img, np.random.randint(0, 255, size=newShape, dtype=int) , axis=0).astype(int)
                    self.img[-1,-1] = n-residue
                else:
                    self.img = np.append(self.img, np.random.randint(0, 1, size=newShape, dtype=int) , axis=0).astype(int)
                    self.img[-1,-1,-1] = n-residue
                self.original_shape = newOverallShape
            else:
                if len(self.img.shape) < 3:
                    self.img[-1,-1] = 0
                else:
                    self.img[-1,-1,-1] = 0



            encoded_image_vector = self.system.encode(self.img)

            # Reshape to the original shape of the image
            self.encoded_image = encoded_image_vector.reshape(self.original_shape)

            self.encoded_img_name = os.path.join("PiCKED App", "output.png")
            self.encoded_img_name_for_display = os.path.join("PiCKED App", 'dispOutput.png')
            img2 = self.encoded_image.astype('uint8')
            iio.imwrite(self.encoded_img_name, img2)
            iio.imwrite(self.encoded_img_name_for_display, img2)
            self.downloadableImage = Image.open(self.encoded_img_name)

            # Reformat to be displayed
            imgList = self.encoded_img_name.split(".")
            self.anyFormatImage = Image.open(self.encoded_img_name_for_display)
            self.anyFormatImage.thumbnail((500,500), Image.LANCZOS)
            self.resizedImageName = os.path.join("PiCKED App", "hillOutput.ppm")
            self.anyFormatImage.save(self.resizedImageName)

            # Change label contents
            imgObject = PhotoImage(file = self.resizedImageName)

            self.outputImg.configure(image=imgObject)

    def tencrypt(self):
        inputText = self.tentry.get('1.0', 'end-1c')
        outText = self.tsystem.encodeStr(inputText)

        self.ttextboxOut.configure(state="normal")
        self.ttextboxOut.delete('0.0', tk.END)
        self.ttextboxOut.insert("0.0", outText)
        self.ttextboxOut.configure(state="disabled")
        
    def tdecrypt(self):
        inputText = self.tentry.get('1.0', 'end-1c')

        cipherText = self.tsystem.decodeStr(inputText)
        self.ttextboxOut.configure(state="normal")
        self.ttextboxOut.delete('0.0', tk.END)
        self.ttextboxOut.insert("0.0", cipherText)
        self.ttextboxOut.configure(state="disabled")

    def decrypt(self):
        if self.dirty:
            self.dirtyOutput = True

            encoded_image_vector = self.system.decode(self.img)

            # remove padding
            if len(encoded_image_vector.shape) < 3:
                pad = encoded_image_vector[-1,-1]
                if pad != 0:
                    encoded_image_vector = encoded_image_vector[:-pad,:]
            else:
                pad = encoded_image_vector[-1,-1,-1]
                if pad != 0:
                    encoded_image_vector = encoded_image_vector[:-pad,:,:]


            # Reshape to the original shape of the image
            self.encoded_image = encoded_image_vector

            self.encoded_img_name = os.path.join("PiCKED App", 'output.png')
            self.encoded_img_name_for_display = os.path.join("PiCKED App", 'dispOutput.png')
            img2 = self.encoded_image.astype('uint8')
            iio.imwrite(self.encoded_img_name, img2)
            iio.imwrite(self.encoded_img_name_for_display, img2)
            self.downloadableImage = Image.open(self.encoded_img_name)

            # Reformat to be displayed
            imgList = self.encoded_img_name.split(".")
            self.anyFormatImage = Image.open(self.encoded_img_name_for_display)
            self.anyFormatImage.thumbnail((500,500), Image.LANCZOS)
            self.resizedImageName = os.path.join("PiCKED App", "hillOutput.ppm")
            self.anyFormatImage.save(self.resizedImageName)

            # Change label contents
            imgObject = PhotoImage(file = self.resizedImageName)

            self.outputImg.configure(image=imgObject)


    def changeKey(self, keySize):
        if keySize != self.keyLen:
            self.keyLen = keySize
            self.system.setKeyLen(keySize)
            self.system.setIV()
        self.system.setKey()

        # Display key
        self.textbox.configure(state="normal")
        self.textbox.delete('0.0', tk.END)
        self.textbox.insert("0.0", "Key:\n"+self.system.getKeyStr()+"\nInitial vector:\n" + self.system.getIVStr())
        self.textbox.configure(state="disabled")
    
    def changeOnlyKey(self, keySize):
        if keySize != self.keyLen:
            self.keyLen = keySize
            self.system.setKeyLen(keySize)
        self.system.setKey()
    
    def setKeyFromEntry(self):
        inStr = self.entryKey.get()
        if int(self.seg_button.get()) != self.keyLen:
            self.keyLen = int(self.seg_button.get())
            self.system.setKeyLen(self.keyLen)
        self.system.setIVManual(self.system.getIVStr())
        try:
            self.system.setKeyManual(inStr)
                # Display key
            self.textbox.configure(state="normal")
            self.textbox.delete('0.0', tk.END)
            self.textbox.insert("0.0", "Key:\n"+self.system.getKeyStr()+"\nInitial vector:\n" + self.system.getIVStr())
            self.textbox.configure(state="disabled")
        except:
            self.changeOnlyKey(int(self.seg_button.get()))
            # Display key
            self.textbox.configure(state="normal")
            self.textbox.delete('0.0', tk.END)
            self.textbox.insert("0.0", "Matrix must be invertible module 256, resetting to:\n" + self.system.getKeyStr()+"\nInitial vector:\n" + self.system.getIVStr())
            self.textbox.configure(state="disabled")

        
    
    def tsetKeyFromEntry(self):
        inStr = self.tentryKey.get()
        if int(self.tseg_button.get()) != self.tkeyLen:
            self.tkeyLen = int(self.tseg_button.get())
            self.tsystem.setKeyLen(self.tkeyLen)
        
        try:
            self.tsystem.setKeyManual(inStr)
            # Display key
            self.ttextbox.configure(state="normal")
            self.ttextbox.delete('0.0', tk.END)
            self.ttextbox.insert("0.0", self.tsystem.getKeyStr())
            self.ttextbox.configure(state="disabled")
        except:
            self.tchangeKey(int(self.tseg_button.get()))
            # Display key
            self.ttextbox.configure(state="normal")
            self.ttextbox.delete('0.0', tk.END)
            self.ttextbox.insert("0.0", "Matrix must be invertible module 256, resetting to:\n" + self.tsystem.getKeyStr())
            self.ttextbox.configure(state="disabled")
                            

        

    def setIVFromEntry(self):
        inStr = self.entryIV.get()
        try:
            self.system.setIVManual(inStr)
        except:
            pass

        # Display key
        self.textbox.configure(state="normal")
        self.textbox.delete('0.0', tk.END)
        self.textbox.insert("0.0", "Key:\n"+self.system.getKeyStr()+"\n\nInitial vector:\n" + self.system.getIVStr())
        self.textbox.configure(state="disabled")

    def tchangeKey(self, keySize):
        if keySize != self.tkeyLen:
            self.tkeyLen = keySize
            self.tsystem.setKeyLen(keySize)
        self.tsystem.setKey()

        # Display key
        self.ttextbox.configure(state="normal")
        self.ttextbox.delete('0.0', tk.END)
        self.ttextbox.insert("0.0", self.tsystem.getKeyStr())
        self.ttextbox.configure(state="disabled")

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
            self.img = np.append(self.img, np.random.randint(0, 255, size=newShape, dtype=int) , axis=0)
            self.original_shape = newOverallShape
    
    def swap(self):
        if self.dirtyOutput:
            self.imgName = self.encoded_img_name
            self.img = np.array(iio.imread(self.imgName)).astype(int)
            self.original_shape = self.img.shape
            

            # file to be displayed
            imgList = self.imgName.split(".")
            self.anyFormatImage = Image.open(self.imgName)
            self.anyFormatImage.thumbnail((500,500), Image.LANCZOS)
            self.originalFormat = imgList[1]
            self.resizedImgName = os.path.join("PiCKED App", "hillInput.ppm")
            self.anyFormatImage.save(self.resizedImgName)

            # Change label contents
            imgObject = PhotoImage(file = self.resizedImgName)

            self.inputImg.configure(image=imgObject)
            self.inputImg.image = imgObject

    def tswap(self):
        self.tentry.delete('0.0', tk.END)
        self.tentry.insert("0.0", self.ttextboxOut.get('1.0', 'end-1c'))

# AES window frame
class AESPage(customtkinter.CTkFrame):

    def __init__(self, parent, controller):
        self.dirty = False
        self.dirtyOutput = False

        self.keyAES = getRandAES(16)
        self.ivAES = getRandAESIV()

        customtkinter.CTkFrame.__init__(self, parent)
        self.grid_columnconfigure((0,2), weight=1)
        self.grid_columnconfigure((1,3), weight=0)
        self.grid_rowconfigure(2, weight=0)

        label = customtkinter.CTkLabel(self,
                                       text="AES",
                                       font=customtkinter.CTkFont(size=20, weight="bold"))
        label.grid(row=0, column=0, columnspan=3, padx=20, pady=(10,0), sticky="w")

        # input image dir: self.imgName
        ### Start img mngmnt
        self.inputImgFrame = customtkinter.CTkFrame(self)
        self.inputImgFrame.configure(width=350,height=350)
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

        button1 = customtkinter.CTkButton(self,
                                          compound="right",
                                          text ="Encrypt                ", 
                                          image=lock1_image,
                                          command=self.encrypt)
        button1.grid(row = 2, column = 1, padx = 5, pady = 5, sticky="sew")

        button2 = customtkinter.CTkButton(self,
                                          compound="right",
                                          text ="Decrypt                ", 
                                          image=lock2_image,
                                          command=self.decrypt)
        button2.grid(row = 3, column = 1, padx = 5, pady = 5, sticky="sew")

        # output
        self.outputImgFrame = customtkinter.CTkFrame(self)
        self.outputImgFrame.grid_propagate(False)
        self.outputImgFrame.columnconfigure(0, weight=1)
        self.outputImgFrame.rowconfigure(0, weight=1)
        self.outputImgFrame.configure(width=350,height=350)
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

        # key input
        self.entryKey = customtkinter.CTkEntry(self.keyFrame, placeholder_text="Input key and hit enter")
        self.entryKey.bind("<Return>", command=lambda x: self.setKeyFromEntry())
        self.entryKey.grid(row=0, column=1, columnspan=3, padx=(0, 5), pady=0, sticky="new")
        self.entryIV = customtkinter.CTkEntry(self.keyFrame, placeholder_text="Input initial vector and hit enter")
        self.entryIV.bind("<Return>", command=lambda x: self.setIVFromEntry())
        self.entryIV.grid(row=1, column=1, columnspan=3, padx=(0, 5), pady=0, sticky="new")


        self.genButton = customtkinter.CTkButton(self.keyFrame, 
                                          compound="right",
                                          text ="Generate Key      ",
                                          image=dice_image,
                                          command = lambda : self.changeKey())
        self.genButton.grid(row = 2, column = 3, padx = (0,5), pady = 0, sticky="new")

        self.genButton2 = customtkinter.CTkButton(self.keyFrame, 
                                          compound="right",
                                          text ="Generate IV         ",
                                          image=dice_image,
                                          command = lambda : self.changeIV())
        self.genButton2.grid(row = 3, column = 3, padx = (0,5), pady = 0, sticky="new")



        self.keyLenFrame = customtkinter.CTkFrame(self.keyFrame)
        self.keyLenFrame.grid(row = 2, column = 1, padx=0, pady=0, sticky="new")
        self.keyLenFrame.grid_columnconfigure(0, weight=1)
        self.keyLenFrame.grid_rowconfigure((0,1), weight=1)
        self.ds_frame_label = customtkinter.CTkLabel(self.keyLenFrame, 
                                                     text="Key size",
                                                     corner_radius=6)
        self.ds_frame_label.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")


        self.seg_button = customtkinter.CTkSegmentedButton(self.keyFrame)
        self.seg_button.grid(row=2, column=2, padx=(0, 5), pady=0, sticky="new")
        self.seg_button.configure(values=["16", "24", "32"])
        self.seg_button.set("16")

        # block mode
        self.keyModeFrame = customtkinter.CTkFrame(self.keyFrame)
        self.keyModeFrame.grid(row = 3, column = 1, padx=0, pady=0, sticky="new")
        self.keyModeFrame.grid_columnconfigure(0, weight=1)
        self.keyModeFrame.grid_rowconfigure(0, weight=1)
        self.mode_frame_label = customtkinter.CTkLabel(self.keyModeFrame, 
                                                     text="Mode",
                                                     corner_radius=6)
        self.mode_frame_label.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")


        self.mode_seg_button = customtkinter.CTkSegmentedButton(self.keyFrame)
        self.mode_seg_button.grid(row=3, column=2, padx=(0, 5), pady=0, sticky="new")
        self.mode_seg_button.configure(values=["ECB", "CBC", "OFB", "CTR"])
        self.mode_seg_button.set("CBC")

        # Key display
        self.currentKeyFrame = customtkinter.CTkFrame(self.keyFrame, fg_color=self.cget("fg_color"), height=150)
        self.currentKeyFrame.grid(row = 0, column = 0, rowspan=4, padx=(0,5), pady=0, sticky="new")
        self.currentKeyFrameLabel = customtkinter.CTkLabel(self.currentKeyFrame, 
                                                     text="Current Key & IV (Hex)",
                                                     corner_radius=6, 
                                                     fg_color=['#979DA2', 'gray29'], 
                                                     text_color=['#DCE4EE', '#DCE4EE'])
        self.currentKeyFrameLabel.grid(row=0, column=0, columnspan=1, padx=0, pady=0, sticky="ew")

        self.textbox = customtkinter.CTkTextbox(self.currentKeyFrame, state="disabled", height=150)
        self.textbox.grid(row=1, column=0, padx=0, pady=0, sticky="nsew")

        
        # Display key
        outStr = "Key:\n" + self.byteToHex(self.keyAES) + "\n\nInitial vector:\n" + self.byteToHex(self.ivAES)
        self.textbox.configure(state="normal")
        self.textbox.delete('0.0', tk.END)
        self.textbox.insert("0.0", outStr)
        self.textbox.configure(state="disabled")

    def browseFiles(self):
        # image dir
        self.imgName = filedialog.askopenfilename(initialdir = "/",
                                                    title = "Select a File",
                                                    filetypes = (("Picture files",
                                                                "*.png;*.jpg;*.ppm;*.bmp"),
                                                                ('All files', '*.*')))
        if self.imgName != "":
            self.dirty = True
            # file to be encrypted
            # original: self.img (array)
            self.img = np.array(iio.imread(self.imgName))

            # Save file to "plain_image.png"
            imgToEncrypt = self.img.astype('uint8')
            self.inputImageName = os.path.join("PiCKED App", "plain_image.png")
            iio.imwrite(self.inputImageName, imgToEncrypt)
            

            # file to be displayed
            imgList = self.imgName.split(".")
            self.anyFormatImage = Image.open(self.imgName)
            self.anyFormatImage.thumbnail((500,500), Image.LANCZOS)
            self.originalFormat = imgList[1]
            self.resizedImgName = os.path.join("PiCKED App", "AESOutput.ppm")
            self.anyFormatImage.save(self.resizedImgName)

            # Change label contents
            imgObject = PhotoImage(file = self.resizedImgName)

            self.inputImg.configure(image=imgObject)
    
    def encrypt(self):
        if self.dirty:
            self.dirtyOutput = True

            # Creates output named: 'aes_output.png'
            encrypt_image_AES(self.inputImageName, 
                              self.mode_seg_button.get(), 
                              self.keyAES,
                              self.ivAES)

            # Save save-able copy 
            shutil.copy(os.path.join("PiCKED App", "aes_output.png"),os.path.join("PiCKED App", "output_image_for_saving.png"))
            self.imageOnOutputName = os.path.join("PiCKED App", "aes_output.png")

            # file to be displayed
            self.anyFormatOutputImage = Image.open(os.path.join("PiCKED App", "aes_output.png"))
            self.anyFormatOutputImage.thumbnail((500,500), Image.LANCZOS)
            self.resizedOutputImgName = os.path.join("PiCKED App", "aes_output.ppm")
            self.anyFormatOutputImage.save(self.resizedOutputImgName)

            # Change label contents
            imgObject = PhotoImage(file = self.resizedOutputImgName)

            self.outputImg.configure(image=imgObject)


    def decrypt(self):
        if self.dirty:
            self.dirtyOutput = True

            # Creates output named: 'aes_output.png'
            decrypt_image_AES(self.inputImageName, 
                              self.mode_seg_button.get(), 
                              self.keyAES,
                              self.ivAES)

            # Save save-able copy
            shutil.copy(os.path.join("PiCKED App", "aes_output.png"), os.path.join("PiCKED App", "output_image_for_saving.png"))
            self.imageOnOutputName = os.path.join("PiCKED App", "aes_output.png")

            # file to be displayed
            self.anyFormatOutputImage = Image.open(os.path.join("PiCKED App", "aes_output.png"))
            self.anyFormatOutputImage.thumbnail((500,500), Image.LANCZOS)
            self.resizedOutputImgName = os.path.join("PiCKED App", "aes_output.ppm")
            self.anyFormatOutputImage.save(self.resizedOutputImgName)

            # Change label contents
            imgObject = PhotoImage(file = self.resizedOutputImgName)

            self.outputImg.configure(image=imgObject)


    def changeKey(self):
        self.keyAES = getRandAES(int(self.seg_button.get()))

        # Display key
        outStr = "Key:\n" + self.byteToHex(self.keyAES) + "\n\nInitial vector:\n" + self.byteToHex(self.ivAES)
        self.textbox.configure(state="normal")
        self.textbox.delete('0.0', tk.END)
        self.textbox.insert("0.0", outStr)
        self.textbox.configure(state="disabled")
    
    def changeIV(self):
        self.ivAES = getRandAESIV()

        # Display key
        outStr = "Key:\n" + self.byteToHex(self.keyAES) + "\n\nInitial vector:\n" + self.byteToHex(self.ivAES)
        self.textbox.configure(state="normal")
        self.textbox.delete('0.0', tk.END)
        self.textbox.insert("0.0", outStr)
        self.textbox.configure(state="disabled")
    
    def setKeyFromEntry(self):
        inputKey = self.entryKey.get().strip()
        try:
            inputKeyList = inputKey.split(" ")
            if len(inputKeyList) >= int(self.seg_button.get()):
                self.keyAES = self.hexToByte(inputKeyList[:int(self.seg_button.get())])
            else:
                newList = ["00"]*int(self.seg_button.get())
                newList[0:len(inputKeyList)] = inputKeyList[:]
                self.keyAES = self.hexToByte(newList)
                
        except:
            pass

        # Display key
        outStr = "Key:\n" + self.byteToHex(self.keyAES) + "\n\nInitial vector:\n" + self.byteToHex(self.ivAES)
        self.textbox.configure(state="normal")
        self.textbox.delete('0.0', tk.END)
        self.textbox.insert("0.0", outStr)
        self.textbox.configure(state="disabled")
    
    def setIVFromEntry(self):
        inputIV = self.entryIV.get().strip()
        try:
            inputIVList = inputIV.split(" ")
            if len(inputIVList) >= 16:
                self.ivAES = self.hexToByte(inputIVList[:16])
            else:
                newList = ["00"]*16
                newList[0:len(inputIVList)] = inputIVList[:]
                self.ivAES = self.hexToByte(newList)
        except:
            pass

        # Display key
        outStr = "Key:\n" + self.byteToHex(self.keyAES) + "\n\nInitial vector:\n" + self.byteToHex(self.ivAES)
        self.textbox.configure(state="normal")
        self.textbox.delete('0.0', tk.END)
        self.textbox.insert("0.0", outStr)
        self.textbox.configure(state="disabled")

    def saveFile(self):
        if self.dirtyOutput:
            myImage = Image.open(os.path.join("PiCKED App", "output_image_for_saving.png"))
            file = filedialog.asksaveasfile(mode='wb', 
                                            filetypes = (("png","*.png"),
                                                        ('All files', '*.*')),
                                            defaultextension=".png")
            if file:
                myImage.save(file) # saves the image to the input file name. 
    
    def swap(self):
        if self.dirtyOutput:
            self.imgName = self.imageOnOutputName
            self.img = np.array(iio.imread(self.imgName))
            self.original_shape = self.img.shape

            # Save file to "plain_image.png"
            imgToEncrypt = self.img.astype('uint8')
            iio.imwrite(os.path.join("PiCKED App", "plain_image.png"), imgToEncrypt)

            # file to be displayed
            imgList = self.imgName.split(".")
            self.anyFormatImage = Image.open(self.imgName)
            self.anyFormatImage.thumbnail((500,500), Image.LANCZOS)
            self.originalFormat = imgList[1]
            self.resizedImgName = os.path.join("PiCKED App", "AESInput.ppm")
            self.anyFormatImage.save(self.resizedImgName)

            # Change label contents
            imgObject = PhotoImage(file = self.resizedImgName)

            self.inputImg.configure(image=imgObject)
    
    def byteToHex(self, bytes):
        listBytes = list(bytes)
        return "".join(hex(x).split('x')[-1]+" " for x in listBytes)[:-1]
    
    def hexToByte(self, hexList):
        return bytes([int(x,16) for x in hexList])
    

# TDES window frame
class TDESPage(customtkinter.CTkFrame):

    def __init__(self, parent, controller):
        self.dirty = False
        self.dirtyOutput = False

        self.keyTDES = getRandTDES(16)
        self.ivTDES = getRandTDESIV()
        self.keyLen = 16

        customtkinter.CTkFrame.__init__(self, parent)
        self.grid_columnconfigure((0,2), weight=1)
        self.grid_columnconfigure((1,3), weight=0)
        self.grid_rowconfigure(2, weight=0)

        label = customtkinter.CTkLabel(self,
                                       text="TDES",
                                       font=customtkinter.CTkFont(size=20, weight="bold"))
        label.grid(row=0, column=0, columnspan=3, padx=20, pady=(10,0), sticky="w")

        # input image dir: self.imgName
        ### Start img mngmnt
        self.inputImgFrame = customtkinter.CTkFrame(self)
        self.inputImgFrame.configure(width=350,height=350)
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

        button1 = customtkinter.CTkButton(self,
                                          compound="right",
                                          text ="Encrypt                ", 
                                          image=lock1_image,
                                          command=self.encrypt)
        button1.grid(row = 2, column = 1, padx = 5, pady = 5, sticky="sew")

        button2 = customtkinter.CTkButton(self,
                                          compound="right",
                                          text ="Decrypt                ", 
                                          image=lock2_image,
                                          command=self.decrypt)
        button2.grid(row = 3, column = 1, padx = 5, pady = 5, sticky="sew")

        # output
        self.outputImgFrame = customtkinter.CTkFrame(self)
        self.outputImgFrame.grid_propagate(False)
        self.outputImgFrame.columnconfigure(0, weight=1)
        self.outputImgFrame.rowconfigure(0, weight=1)
        self.outputImgFrame.configure(width=350,height=350)
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

        # key input
        self.entryKey = customtkinter.CTkEntry(self.keyFrame, placeholder_text="Input key and hit enter")
        self.entryKey.bind("<Return>", command=lambda x: self.setKeyFromEntry())
        self.entryKey.grid(row=0, column=1, columnspan=3, padx=(0, 5), pady=0, sticky="new")
        self.entryIV = customtkinter.CTkEntry(self.keyFrame, placeholder_text="Input initial vector and hit enter")
        self.entryIV.bind("<Return>", command=lambda x: self.setIVFromEntry())
        self.entryIV.grid(row=1, column=1, columnspan=3, padx=(0, 5), pady=0, sticky="new")


        self.genButton = customtkinter.CTkButton(self.keyFrame, 
                                          compound="right",
                                          text ="Generate Key      ",
                                          image=dice_image,
                                          command = lambda : self.changeKey())
        self.genButton.grid(row = 2, column = 3, padx = (0,5), pady = 0, sticky="new")

        self.genButton2 = customtkinter.CTkButton(self.keyFrame, 
                                          compound="right",
                                          text ="Generate IV         ",
                                          image=dice_image,
                                          command = lambda : self.changeIV())
        self.genButton2.grid(row = 3, column = 3, padx = (0,5), pady = 0, sticky="new")



        self.keyLenFrame = customtkinter.CTkFrame(self.keyFrame)
        self.keyLenFrame.grid(row = 2, column = 1, padx=0, pady=0, sticky="new")
        self.keyLenFrame.grid_columnconfigure(0, weight=1)
        self.keyLenFrame.grid_rowconfigure((0,1), weight=1)
        self.ds_frame_label = customtkinter.CTkLabel(self.keyLenFrame, 
                                                     text="Key size",
                                                     corner_radius=6)
        self.ds_frame_label.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")


        self.seg_button = customtkinter.CTkSegmentedButton(self.keyFrame)
        self.seg_button.grid(row=2, column=2, padx=(0, 5), pady=0, sticky="new")
        self.seg_button.configure(values=["16", "24"])
        self.seg_button.set("16")

        # block mode
        self.keyModeFrame = customtkinter.CTkFrame(self.keyFrame)
        self.keyModeFrame.grid(row = 3, column = 1, padx=0, pady=0, sticky="new")
        self.keyModeFrame.grid_columnconfigure(0, weight=1)
        self.keyModeFrame.grid_rowconfigure(0, weight=1)
        self.mode_frame_label = customtkinter.CTkLabel(self.keyModeFrame, 
                                                     text="Mode",
                                                     corner_radius=6)
        self.mode_frame_label.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")


        self.mode_seg_button = customtkinter.CTkSegmentedButton(self.keyFrame)
        self.mode_seg_button.grid(row=3, column=2, padx=(0, 5), pady=0, sticky="new")
        self.mode_seg_button.configure(values=["ECB", "CBC", "OFB", "CTR"])
        self.mode_seg_button.set("CBC")

        # Key display
        self.currentKeyFrame = customtkinter.CTkFrame(self.keyFrame, fg_color=self.cget("fg_color"), height=150)
        self.currentKeyFrame.grid(row = 0, column = 0, rowspan=4, padx=(0,5), pady=0, sticky="new")
        self.currentKeyFrameLabel = customtkinter.CTkLabel(self.currentKeyFrame, 
                                                     text="Current Key & IV (Hex)",
                                                     corner_radius=6, 
                                                     fg_color=['#979DA2', 'gray29'], 
                                                     text_color=['#DCE4EE', '#DCE4EE'])
        self.currentKeyFrameLabel.grid(row=0, column=0, columnspan=1, padx=0, pady=0, sticky="ew")

        self.textbox = customtkinter.CTkTextbox(self.currentKeyFrame, state="disabled", height=130)
        self.textbox.grid_propagate(False)
        self.textbox.grid(row=1, column=0, padx=0, pady=(0,10), sticky="nsew")

        
        # Display key
        outStr = "Key:\n" + self.byteToHex(self.keyTDES) + "\n\nInitial vector:\n" + self.byteToHex(self.ivTDES)
        self.textbox.configure(state="normal")
        self.textbox.delete('0.0', tk.END)
        self.textbox.insert("0.0", outStr)
        self.textbox.configure(state="disabled")

    def browseFiles(self):
        # image dir
        self.imgName = filedialog.askopenfilename(initialdir = "/",
                                                    title = "Select a File",
                                                    filetypes = (("Picture files",
                                                                "*.png;*.jpg;*.ppm;*.bmp"),
                                                                ('All files', '*.*')))
        
        if self.imgName != "":
            self.dirty = True
            # file to be encrypted
            # original: self.img (array)
            self.img = np.array(iio.imread(self.imgName))

            # Save file to "plain_image.png"
            imgToEncrypt = self.img.astype('uint8')
            iio.imwrite(os.path.join("PiCKED App", "plain_image_TDES.png"), imgToEncrypt)
            self.inputImageName = os.path.join("PiCKED App", "plain_image_TDES.png")

            # file to be displayed
            imgList = self.imgName.split(".")
            self.anyFormatImage = Image.open(self.imgName)
            self.anyFormatImage.thumbnail((500,500), Image.LANCZOS)
            self.originalFormat = imgList[1]
            self.resizedImgName = os.path.join("PiCKED App", "TDESInput.ppm")
            self.anyFormatImage.save(self.resizedImgName)

            # Change label contents
            imgObject = PhotoImage(file = self.resizedImgName)

            self.inputImg.configure(image=imgObject)
    
    def encrypt(self):
        if self.dirty:
            self.dirtyOutput = True

            # Creates output named: 'TDES_output.png'
            encrypt_image_TDES(self.inputImageName, 
                              self.mode_seg_button.get(), 
                              self.keyTDES, 
                              self.ivTDES)

            # Save save-able copy
            shutil.copy(os.path.join("PiCKED App", "TDES_output.png"), os.path.join("PiCKED App", "output_image_for_saving_TDES.png"))
            self.imageOnOutputName = os.path.join("PiCKED App", "TDES_output.png")

            # file to be displayed
            self.anyFormatOutputImage = Image.open(os.path.join("PiCKED App", "TDES_output.png"))
            self.anyFormatOutputImage.thumbnail((500,500), Image.LANCZOS)
            self.resizedOutputImgName = os.path.join("PiCKED App", "TDES_output.ppm")
            self.anyFormatOutputImage.save(self.resizedOutputImgName)

            # Change label contents
            imgObject = PhotoImage(file = self.resizedOutputImgName)

            self.outputImg.configure(image=imgObject)


    def decrypt(self):
        if self.dirty:
            self.dirtyOutput = True

            # Creates output named: 'TDES_output.png'
            decrypt_image_TDES(self.inputImageName, 
                              self.mode_seg_button.get(), 
                              self.keyTDES, 
                              self.ivTDES)

            # Save save-able copy
            shutil.copy(os.path.join("PiCKED App", "TDES_output.png"), os.path.join("PiCKED App", "output_image_for_saving_TDES.png"))
            self.imageOnOutputName = os.path.join("PiCKED App", "TDES_output.png")

            # file to be displayed
            self.anyFormatOutputImage = Image.open(os.path.join("PiCKED App", "TDES_output.png"))
            self.anyFormatOutputImage.thumbnail((500,500), Image.LANCZOS)
            self.resizedOutputImgName = os.path.join("PiCKED App", "TDES_output.ppm")
            self.anyFormatOutputImage.save(self.resizedOutputImgName)

            # Change label contents
            imgObject = PhotoImage(file = self.resizedOutputImgName)

            self.outputImg.configure(image=imgObject)


    def changeKey(self):
        self.keyTDES = getRandTDES(int(self.seg_button.get()))

        # Display key
        outStr = "Key:\n" + self.byteToHex(self.keyTDES) + "\n\nInitial vector:\n" + self.byteToHex(self.ivTDES)
        self.textbox.configure(state="normal")
        self.textbox.delete('0.0', tk.END)
        self.textbox.insert("0.0", outStr)
        self.textbox.configure(state="disabled")
    
    def changeIV(self):
        self.ivTDES = getRandTDESIV()

        # Display key
        outStr = "Key:\n" + self.byteToHex(self.keyTDES) + "\n\nInitial vector:\n" + self.byteToHex(self.ivTDES)
        self.textbox.configure(state="normal")
        self.textbox.delete('0.0', tk.END)
        self.textbox.insert("0.0", outStr)
        self.textbox.configure(state="disabled")
    
    def setKeyFromEntry(self):
        inputKey = self.entryKey.get().strip()
        try:
            inputKeyList = inputKey.split(" ")
            if len(inputKeyList) >= int(self.seg_button.get()):
                self.keyTDES = self.hexToByte(inputKeyList[:int(self.seg_button.get())])
            else:
                newList = ["00"]*int(self.seg_button.get())
                newList[0:len(inputKeyList)] = inputKeyList[:]
                self.keyTDES = self.hexToByte(newList)
                
        except:
            pass

        # Display key
        outStr = "Key:\n" + self.byteToHex(self.keyTDES) + "\n\nInitial vector:\n" + self.byteToHex(self.ivTDES)
        self.textbox.configure(state="normal")
        self.textbox.delete('0.0', tk.END)
        self.textbox.insert("0.0", outStr)
        self.textbox.configure(state="disabled")
    
    def setIVFromEntry(self):
        inputIV = self.entryIV.get().strip()
        try:
            inputIVList = inputIV.split(" ")
            if len(inputIVList) >= 16:
                self.ivTDES = self.hexToByte(inputIVList[:16])
            else:
                newList = ["00"]*16
                newList[0:len(inputIVList)] = inputIVList[:]
                self.ivTDES = self.hexToByte(newList)
        except:
            pass

        # Display key
        outStr = "Key:\n" + self.byteToHex(self.keyTDES) + "\n\nInitial vector:\n" + self.byteToHex(self.ivTDES)
        self.textbox.configure(state="normal")
        self.textbox.delete('0.0', tk.END)
        self.textbox.insert("0.0", outStr)
        self.textbox.configure(state="disabled")

    def saveFile(self):
        if self.dirtyOutput:
            myImage = Image.open(os.path.join("PiCKED App", "output_image_for_saving_TDES.png"))
            file = filedialog.asksaveasfile(mode='wb', 
                                            filetypes = (("png","*.png"),
                                                        ('All files', '*.*')),
                                            defaultextension=".png")
            if file:
                myImage.save(file) # saves the image to the input file name. 
    
    def swap(self):
        if self.dirtyOutput:
            self.imgName = self.imageOnOutputName
            self.img = np.array(iio.imread(self.imgName))
            self.original_shape = self.img.shape

            # Save file to "plain_image_TDES.png"
            imgToEncrypt = self.img.astype('uint8')
            iio.imwrite(os.path.join("PiCKED App", "plain_image_TDES.png"), imgToEncrypt)

            # file to be displayed
            imgList = self.imgName.split(".")
            self.anyFormatImage = Image.open(self.imgName)
            self.anyFormatImage.thumbnail((500,500), Image.LANCZOS)
            self.originalFormat = imgList[1]
            self.resizedImgName = os.path.join("PiCKED App", "TDESInput.ppm")
            self.anyFormatImage.save(self.resizedImgName)

            # Change label contents
            imgObject = PhotoImage(file = self.resizedImgName)

            self.inputImg.configure(image=imgObject)
    
    def byteToHex(self, bytes):
        listBytes = list(bytes)
        return "".join(hex(x).split('x')[-1]+" " for x in listBytes)[:-1]
    
    def hexToByte(self, hexList):
        return bytes([int(x,16) for x in hexList])


# S-DES window frame
class SDESPage(customtkinter.CTkFrame):

    def __init__(self, parent, controller):
        self.dirty = False
        self.dirtyOutput = False

        self.system = SimplerDES()
        self.system.setRandomIV()
        self.system.setRandomKey()
        self.keySDES = ''.join(str(x) for x in self.system.key)
        self.ivSDES = str(self.system.iv)

        customtkinter.CTkFrame.__init__(self, parent)
        self.grid_columnconfigure((0,2), weight=1)
        self.grid_columnconfigure((1,3), weight=0)
        self.grid_rowconfigure(2, weight=0)

        label = customtkinter.CTkLabel(self,
                                       text="SDES",
                                       font=customtkinter.CTkFont(size=20, weight="bold"))
        label.grid(row=0, column=0, columnspan=3, padx=20, pady=(10,0), sticky="w")

        # input image dir: self.imgName
        ### Start img mngmnt
        self.inputImgFrame = customtkinter.CTkFrame(self)
        self.inputImgFrame.configure(width=350,height=350)
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

        button1 = customtkinter.CTkButton(self,
                                          compound="right",
                                          text ="Encrypt                ", 
                                          image=lock1_image,
                                          command=self.encrypt)
        button1.grid(row = 2, column = 1, padx = 5, pady = 5, sticky="sew")

        button2 = customtkinter.CTkButton(self,
                                          compound="right",
                                          text ="Decrypt                ", 
                                          image=lock2_image,
                                          command=self.decrypt)
        button2.grid(row = 3, column = 1, padx = 5, pady = 5, sticky="sew")

        # output
        self.outputImgFrame = customtkinter.CTkFrame(self)
        self.outputImgFrame.grid_propagate(False)
        self.outputImgFrame.columnconfigure(0, weight=1)
        self.outputImgFrame.rowconfigure(0, weight=1)
        self.outputImgFrame.configure(width=350,height=350)
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

        # key input
        self.entryKey = customtkinter.CTkEntry(self.keyFrame, placeholder_text="Input key and hit enter")
        self.entryKey.bind("<Return>", command=lambda x: self.setKeyFromEntry())
        self.entryKey.grid(row=0, column=1, columnspan=3, padx=(0, 5), pady=0, sticky="new")
        # entry private key
        self.entryIV = customtkinter.CTkEntry(self.keyFrame, placeholder_text="Input iv (integer in range [0,255]) and hit enter")
        self.entryIV.bind("<Return>", command=lambda x: self.setIVFromEntry())
        self.entryIV.grid(row=1, column=1, columnspan=3, padx=(0, 5), pady=0, sticky="ew")


        self.genButton = customtkinter.CTkButton(self.keyFrame, 
                                          compound="right",
                                          text ="Generate Key      ",
                                          image=dice_image,
                                          command = lambda : self.changeKey())
        self.genButton.grid(row = 2, column = 3, padx = (0,5), pady = 0, sticky="new")


        # block mode
        self.keyModeFrame = customtkinter.CTkFrame(self.keyFrame)
        self.keyModeFrame.grid(row = 2, column = 1, padx=0, pady=0, sticky="new")
        self.keyModeFrame.grid_columnconfigure(0, weight=1)
        self.keyModeFrame.grid_rowconfigure(0, weight=1)
        self.mode_frame_label = customtkinter.CTkLabel(self.keyModeFrame, 
                                                     text="Mode",
                                                     corner_radius=6)
        self.mode_frame_label.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")


        self.mode_seg_button = customtkinter.CTkSegmentedButton(self.keyFrame)
        self.mode_seg_button.grid(row=2, column=2, padx=(0, 5), pady=0, sticky="new")
        self.mode_seg_button.configure(values=["ECB", "CBC", "OFB", "CTR"])
        self.mode_seg_button.set("CBC")

        # Key display
        self.currentKeyFrame = customtkinter.CTkFrame(self.keyFrame, fg_color=self.cget("fg_color"), height=150)
        self.currentKeyFrame.grid_propagate(False)
        self.currentKeyFrame.grid(row = 0, column = 0, rowspan=3, padx=(0,5), pady=0, sticky="new")
        self.currentKeyFrameLabel = customtkinter.CTkLabel(self.currentKeyFrame, 
                                                     text="Current Key",
                                                     corner_radius=6, 
                                                     fg_color=['#979DA2', 'gray29'], 
                                                     text_color=['#DCE4EE', '#DCE4EE'])
        self.currentKeyFrameLabel.grid(row=0, column=0, columnspan=1, padx=0, pady=0, sticky="ew")

        self.textbox = customtkinter.CTkTextbox(self.currentKeyFrame, state="disabled")
        self.textbox.grid(row=1, column=0, padx=0, pady=0, sticky="nsew")
        self.textbox.insert("0.0", "")

        
        # Display key
        self.textbox.configure(state="normal")
        self.textbox.delete('0.0', tk.END)
        self.textbox.insert("0.0", "Key:\n" + self.keySDES + "\n\nIV:\n" +self.ivSDES)
        self.textbox.configure(state="disabled")

    def browseFiles(self):
        # image dir
        self.imgName = filedialog.askopenfilename(initialdir = "/",
                                                    title = "Select a File",
                                                    filetypes = (("Picture files",
                                                                "*.png;*.jpg;*.ppm;*.bmp"),
                                                                ('All files', '*.*')))
        if self.imgName != "":
            self.dirty = True
            # file to be encrypted
            # original: self.img (array)
            self.img = np.array(iio.imread(self.imgName))

            # Save file to "plain_image_sdes.png"
            imgToEncrypt = self.img.astype('uint8')
            iio.imwrite(os.path.join("PiCKED App", "plain_image_sdes.png"), imgToEncrypt)
            self.inputImageName = os.path.join("PiCKED App", "plain_image_sdes.png")

            # file to be displayed
            imgList = self.imgName.split(".")
            self.anyFormatImage = Image.open(self.imgName)
            self.anyFormatImage.thumbnail((500,500), Image.LANCZOS)
            self.originalFormat = imgList[1]
            self.resizedImgName = os.path.join("PiCKED App", "SDESInput.ppm")
            self.anyFormatImage.save(self.resizedImgName)

            # Change label contents
            imgObject = PhotoImage(file = self.resizedImgName)

            self.inputImg.configure(image=imgObject)
    
    def encrypt(self):
        if self.dirty:
            self.dirtyOutput = True

            # Creates output named: 'sdes_output.png'
            if self.mode_seg_button.get() == "ECB":
                self.system.encryptECB(self.inputImageName)
            elif self.mode_seg_button.get() == "CBC":
                self.system.encryptCBC(self.inputImageName)
            elif self.mode_seg_button.get() == "OFB":
                self.system.encryptOFB(self.inputImageName)
            elif self.mode_seg_button.get() == "CTR":
                self.system.encryptCTR(self.inputImageName)


            # Save save-able copy
            shutil.copy(os.path.join("PiCKED App", "sdes_output.png"), os.path.join("PiCKED App", "output_image_for_saving_sdes.png"))
            self.imageOnOutputName = os.path.join("PiCKED App", "sdes_output.png")

            # file to be displayed
            self.anyFormatOutputImage = Image.open(os.path.join("PiCKED App", "sdes_output.png"))
            self.anyFormatOutputImage.thumbnail((500,500), Image.LANCZOS)
            self.resizedOutputImgName = os.path.join("PiCKED App", "sdes_output.ppm")
            self.anyFormatOutputImage.save(self.resizedOutputImgName)

            # Change label contents
            imgObject = PhotoImage(file = self.resizedOutputImgName)

            self.outputImg.configure(image=imgObject)


    def decrypt(self):
        if self.dirty:
            self.dirtyOutput = True

            # Creates output named: 'sdes_output.png'
            if self.mode_seg_button.get() == "ECB":
                self.system.decryptECB(self.inputImageName)
            elif self.mode_seg_button.get() == "CBC":
                self.system.decryptCBC(self.inputImageName)
            elif self.mode_seg_button.get() == "OFB":
                self.system.decryptOFB(self.inputImageName)
            elif self.mode_seg_button.get() == "CTR":
                self.system.decryptCTR(self.inputImageName)

            # Save save-able copy
            shutil.copy(os.path.join("PiCKED App", "sdes_output.png"), os.path.join("PiCKED App", "output_image_for_saving_sdes.png"))
            self.imageOnOutputName = os.path.join("PiCKED App", "sdes_output.png")

            # file to be displayed
            self.anyFormatOutputImage = Image.open(os.path.join("PiCKED App", "sdes_output.png"))
            self.anyFormatOutputImage.thumbnail((500,500), Image.LANCZOS)
            self.resizedOutputImgName = os.path.join("PiCKED App", "sdes_output.ppm")
            self.anyFormatOutputImage.save(self.resizedOutputImgName)

            # Change label contents
            imgObject = PhotoImage(file = self.resizedOutputImgName)

            self.outputImg.configure(image=imgObject)


    def changeKey(self):
        self.system.setRandomKey()
        self.system.setRandomIV()
        self.keySDES = ''.join(str(x) for x in self.system.key)
        self.ivSDES = str(self.system.iv)

        # Display key
        self.textbox.configure(state="normal")
        self.textbox.delete('0.0', tk.END)
        self.textbox.insert("0.0", "Key:\n" + self.keySDES + "\n\nIV:\n" +self.ivSDES)
        self.textbox.configure(state="disabled")
    
    def setKeyFromEntry(self):
        inputKey = self.entryKey.get()
        try:
            inputKeyList = list(inputKey.strip())
            outputList = [0]*10
            for i in range(len(inputKeyList)):
                if int(inputKeyList[i]) == 1 and i<10:
                    outputList[i] = 1

            self.system.setKey(outputList)
            self.keySDES = ''.join(str(x) for x in self.system.key)
        except:
            pass

        # Display key
        self.textbox.configure(state="normal")
        self.textbox.delete('0.0', tk.END)
        self.textbox.insert("0.0", "Key:\n" + self.keySDES + "\n\nIV:\n" +self.ivSDES)
        self.textbox.configure(state="disabled")
    
    def setIVFromEntry(self):
        inputKey = self.entryIV.get()
        try:
            inputInt = int(inputKey.strip())%256
            
            self.system.setIV(inputInt)
            self.ivSDES = str(self.system.iv)
        except:
            pass

        # Display key
        self.textbox.configure(state="normal")
        self.textbox.delete('0.0', tk.END)
        self.textbox.insert("0.0", "Key:\n" + self.keySDES + "\n\nIV:\n" +self.ivSDES)
        self.textbox.configure(state="disabled")

    def saveFile(self):
        if self.dirtyOutput:
            myImage = Image.open(os.path.join("PiCKED App", "output_image_for_saving_sdes.png"))
            file = filedialog.asksaveasfile(mode='wb', 
                                            filetypes = (("png","*.png"),
                                                        ('All files', '*.*')),
                                            defaultextension=".png")
            if file:
                myImage.save(file) # saves the image to the input file name. 
    
    def swap(self):
        if self.dirtyOutput:
            self.imgName = self.imageOnOutputName
            self.img = np.array(iio.imread(self.imgName))
            self.original_shape = self.img.shape

            # Save file to "plain_image_sdes.png"
            imgToEncrypt = self.img.astype('uint8')
            iio.imwrite(os.path.join("PiCKED App", "plain_image_sdes.png"), imgToEncrypt)

            # file to be displayed
            imgList = self.imgName.split(".")
            self.anyFormatImage = Image.open(self.imgName)
            self.anyFormatImage.thumbnail((500,500), Image.LANCZOS)
            self.originalFormat = imgList[1]
            self.resizedImgName = os.path.join("PiCKED App", "SDESInput.ppm")
            self.anyFormatImage.save(self.resizedImgName)

            # Change label contents
            imgObject = PhotoImage(file = self.resizedImgName)

            self.inputImg.configure(image=imgObject)
    
    def byteToHex(self, bytes):
        listBytes = list(bytes)
        return [hex(x).split('x')[-1] for x in listBytes]
    
    def hexToByte(self, hexList):
        return bytes([int(x,16) for x in hexList])


# RSA window frame
class RSAPage(customtkinter.CTkFrame):
    def __init__(self, parent, controller):
        self.system = RSAEncryption()
        self.currentPrivateKey = self.system.private_key_base64
        self.currentPublicKey = self.system.public_key_base64

        customtkinter.CTkFrame.__init__(self, parent)

        self.grid_columnconfigure((0,2), weight=1)
        self.grid_columnconfigure(1, weight=0)

        label = customtkinter.CTkLabel(self,
                                       text="RSA",
                                       font=customtkinter.CTkFont(size=20, weight="bold"))
        label.grid(row=0, column=0, columnspan=3, padx=20, pady=(10,0), sticky="w")

        # input
        self.entry = customtkinter.CTkTextbox(self)
        self.entry.grid(row=2, column=0, rowspan=2, padx=(20, 0), pady=0, sticky="nsew")
        self.entry.insert("0.0", "Attack at noon")

        self.maxNumLabel = customtkinter.CTkLabel(self, 
                                                     text="Max. characters for encryption: 190",
                                                     corner_radius=6, 
                                                     fg_color=['#979DA2', 'gray29'], 
                                                     text_color=['#DCE4EE', '#DCE4EE'])
        self.maxNumLabel.grid(row=1, column=0, padx=(20,0), pady=(20,0), sticky="ew")

        button1 = customtkinter.CTkButton(self, text ="Clear",
                            command = self.clearInput)
        button1.grid(row = 4, column = 0, padx = (20,0), pady = (0,10), sticky="ew")

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

        button1 = customtkinter.CTkButton(self,
                                          compound="right",
                                          text ="Encrypt                ", 
                                          image=lock1_image,
                                          command=self.encrypt)
        button1.grid(row = 2, column = 1, padx = 5, pady = 5, sticky="sew")

        button2 = customtkinter.CTkButton(self, 
                                          compound="right",
                                          text ="Decrypt                ", 
                                          image=lock2_image,
                                          command=self.decrypt)
        button2.grid(row = 3, column = 1, padx = 5, pady = 5, sticky="sew")

        
        # output
        self.textbox = customtkinter.CTkTextbox(self, state="disabled")
        self.textbox.grid(row=1, column=2, rowspan=3, padx=(0,20), pady=(20, 0), sticky="nsew")
        self.textbox.insert("0.0", "")
        button1 = customtkinter.CTkButton(self, text ="Copy",
                            command = self.copyToClipboard)
        button1.grid(row = 4, column = 2, padx = (0,20), pady = (0,10), sticky="ew")

        # Key part (generation)
        self.keyFrame = customtkinter.CTkFrame(self, fg_color=self.cget("fg_color"))
        self.keyFrame.columnconfigure(0, weight=0)
        self.keyFrame.columnconfigure(1, weight=1)
        self.keyFrame.grid(row = 5, column = 0, columnspan=3, padx=20, pady=(20,0), sticky="ew")
        button1 = customtkinter.CTkButton(self.keyFrame, 
                                          compound="right",
                                          text ="Generate Keys     ",
                                          image=dice_image,
                                          command = self.generateKey)
        button1.grid(row = 0, column = 0, padx = (0,5), pady = 0, sticky="new")

        # entry public key
        self.entryPublicKey = customtkinter.CTkEntry(self.keyFrame, placeholder_text="Input public key and hit enter")
        self.entryPublicKey.bind("<Return>", command=lambda x: self.setPublicKeyFromEntry())
        self.entryPublicKey.grid(row=0, column=1, padx=(5, 0), pady=0, sticky="ew")
        # entry private key
        self.entryPrivateKey = customtkinter.CTkEntry(self.keyFrame, placeholder_text="Input private key and hit enter")
        self.entryPrivateKey.bind("<Return>", command=lambda x: self.setPrivateKeyFromEntry())
        self.entryPrivateKey.grid(row=1, column=1, padx=(5, 0), pady=(5,0), sticky="ew")

        # Key display
        self.currentKeyFrame = customtkinter.CTkFrame(self.keyFrame, fg_color=self.cget("fg_color"))
        self.currentKeyFrame.columnconfigure((0,1), weight=1)
        self.currentKeyFrame.grid(row = 6, column = 0, rowspan=3, columnspan=2, padx=0, pady=(5,0), sticky="new")

        # public key display
        self.currentKeyFrameLabel = customtkinter.CTkLabel(self.currentKeyFrame, 
                                                     text="Public Key (Base 64)",
                                                     corner_radius=6, 
                                                     fg_color=['#979DA2', 'gray29'], 
                                                     text_color=['#DCE4EE', '#DCE4EE'])
        self.currentKeyFrameLabel.grid(row=0, column=0, columnspan=1, padx=(0,5), pady=0, sticky="ew")

        self.textbox1 = customtkinter.CTkTextbox(self.currentKeyFrame, state="disabled")
        self.textbox1.grid(row=1, column=0, padx=(0,5), pady=0, sticky="nsew")
        self.textbox1.insert("0.0", "")

        copyButton1 = customtkinter.CTkButton(self.currentKeyFrame, text ="Copy",
                            command = self.copyToClipboard1)
        copyButton1.grid(row = 2, column = 0, padx = (0,5), pady = 0, sticky="ew")

        # private key display
        self.currentKeyFrameLabel = customtkinter.CTkLabel(self.currentKeyFrame, 
                                                     text="Private Key (Base 64)",
                                                     corner_radius=6, 
                                                     fg_color=['#979DA2', 'gray29'], 
                                                     text_color=['#DCE4EE', '#DCE4EE'])
        self.currentKeyFrameLabel.grid(row=0, column=1, columnspan=1, padx=(5,0), pady=0, sticky="ew")

        self.textbox2 = customtkinter.CTkTextbox(self.currentKeyFrame, state="disabled")
        self.textbox2.grid(row=1, column=1, padx=(5,0), pady=0, sticky="nsew")
        self.textbox2.insert("0.0", "")

        copyButton2 = customtkinter.CTkButton(self.currentKeyFrame, text ="Copy",
                            command = self.copyToClipboard2)
        copyButton2.grid(row = 2, column = 1, padx = (5,0), pady = 0, sticky="ew")

        
        # Display public key
        self.textbox1.configure(state="normal")
        self.textbox1.delete('0.0', tk.END)
        self.textbox1.insert("0.0", self.currentPublicKey)
        self.textbox1.configure(state="disabled")

        # Display private key
        self.textbox2.configure(state="normal")
        self.textbox2.delete('0.0', tk.END)
        self.textbox2.insert("0.0", self.currentPrivateKey)
        self.textbox2.configure(state="disabled")
        
    
    def encrypt(self):
        inputText = self.entry.get("1.0", "end-1c")

        #if len(inputText) > 190:
        #    inputText = inputText[:190]
        #    self.entry.delete('1.0', tk.END)
        #    self.entry.insert("0.0", inputText)
        
        self.system.encrypt_message(inputText)
        cipherText = self.system.encrypted_message

        self.textbox.configure(state="normal")
        self.textbox.delete('1.0', tk.END)
        self.textbox.insert("0.0", cipherText)
        self.textbox.configure(state="disabled")
        
    def decrypt(self):
        inputText = self.entry.get("1.0", "end-1c")

        self.system.encrypted_message = inputText
        self.system.decrypt_message()
        cipherText = self.system.decrypted_message

        self.textbox.configure(state="normal")
        self.textbox.delete('0.0', tk.END)
        self.textbox.insert("0.0", cipherText)
        self.textbox.configure(state="disabled")
    
    def copyToClipboard(self):
        self.clipboard_clear()
        self.clipboard_append(self.textbox.get('1.0', 'end-1c'))

    def copyToClipboard1(self):
        self.clipboard_clear()
        self.clipboard_append(self.textbox1.get('1.0', 'end-1c'))

    def copyToClipboard2(self):
        self.clipboard_clear()
        self.clipboard_append(self.textbox2.get('1.0', 'end-1c'))

    def swap(self):
        self.entry.delete('0.0', tk.END)
        self.entry.insert("0.0", self.textbox.get('1.0', 'end-1c'))
    
    def clearInput(self):
        self.entry.delete('0.0', tk.END)
    
    def generateKey(self):
        self.system.generate_keys(2048)
        self.currentPrivateKey = self.system.private_key_base64
        self.currentPublicKey = self.system.public_key_base64

        # Display keys
        self.textbox1.configure(state="normal")
        self.textbox1.delete('0.0', tk.END)
        self.textbox1.insert("0.0", self.currentPublicKey)
        self.textbox1.configure(state="disabled")

        self.textbox2.configure(state="normal")
        self.textbox2.delete('0.0', tk.END)
        self.textbox2.insert("0.0", self.currentPrivateKey)
        self.textbox2.configure(state="disabled")
    
    def setPublicKeyFromEntry(self):
        inputKey = self.entryPublicKey.get()
        self.currentPublicKey = inputKey
        self.system.set_public_key(inputKey)

        # Display key
        self.textbox1.configure(state="normal")
        self.textbox1.delete('0.0', tk.END)
        self.textbox1.insert("0.0", self.currentPublicKey)
        self.textbox1.configure(state="disabled")
    
    def setPrivateKeyFromEntry(self):
        inputKey = self.entryPrivateKey.get()
        self.currentPrivateKey = inputKey
        self.system.set_private_key(inputKey)

        # Display key
        self.textbox2.configure(state="normal")
        self.textbox2.delete('0.0', tk.END)
        self.textbox2.insert("0.0", self.currentPrivateKey)
        self.textbox2.configure(state="disabled")


# ElGammal window frame
class ElGamalPage(customtkinter.CTkFrame):
    def __init__(self, parent, controller):
        self.system = ElGamalCryptosystem()
        self.system.generate_new_key()
        self.currentPrivateKey = self.system.private_key_base64
        self.currentPublicKey = self.system.public_key_base64

        customtkinter.CTkFrame.__init__(self, parent)

        self.grid_columnconfigure((0,2), weight=1)
        self.grid_columnconfigure(1, weight=0)

        label = customtkinter.CTkLabel(self,
                                       text="ELGAMAL",
                                       font=customtkinter.CTkFont(size=20, weight="bold"))
        label.grid(row=0, column=0, columnspan=3, padx=20, pady=(10,0), sticky="w")

        # input
        self.entry = customtkinter.CTkTextbox(self)
        self.entry.grid(row=1, column=0, rowspan=3, padx=(20, 0), pady=(20,0), sticky="nsew")
        self.entry.insert("0.0", "Attack at noon")

        button1 = customtkinter.CTkButton(self, text ="Clear",
                            command = self.clearInput)
        button1.grid(row = 4, column = 0, padx = (20,0), pady = (0,10), sticky="ew")

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

        button1 = customtkinter.CTkButton(self,
                                          compound="right",
                                          text ="Encrypt                ", 
                                          image=lock1_image,
                                          command=self.encrypt)
        button1.grid(row = 2, column = 1, padx = 5, pady = 5, sticky="sew")

        button2 = customtkinter.CTkButton(self, 
                                          compound="right",
                                          text ="Decrypt                ", 
                                          image=lock2_image,
                                          command=self.decrypt)
        button2.grid(row = 3, column = 1, padx = 5, pady = 5, sticky="sew")

        
        # output
        self.textbox = customtkinter.CTkTextbox(self, state="disabled")
        self.textbox.grid(row=1, column=2, rowspan=3, padx=(0,20), pady=(20, 0), sticky="nsew")
        self.textbox.insert("0.0", "")
        button1 = customtkinter.CTkButton(self, text ="Copy",
                            command = self.copyToClipboard)
        button1.grid(row = 4, column = 2, padx = (0,20), pady = (0,10), sticky="ew")

        # Key part (generation)
        self.keyFrame = customtkinter.CTkFrame(self, fg_color=self.cget("fg_color"))
        self.keyFrame.columnconfigure(0, weight=0)
        self.keyFrame.columnconfigure(1, weight=1)
        self.keyFrame.grid(row = 5, column = 0, columnspan=3, padx=20, pady=(20,0), sticky="ew")
        button1 = customtkinter.CTkButton(self.keyFrame, 
                                          compound="right",
                                          text ="Generate Keys     ",
                                          image=dice_image,
                                          command = self.generateKey)
        button1.grid(row = 0, column = 0, padx = (0,5), pady = 0, sticky="new")


        # entry public key
        self.entryPublicKey = customtkinter.CTkEntry(self.keyFrame, placeholder_text="Input public key and hit enter")
        self.entryPublicKey.bind("<Return>", command=lambda x: self.setPublicKeyFromEntry())
        self.entryPublicKey.grid(row=0, column=1, padx=(5, 0), pady=0, sticky="ew")
        # entry public key
        self.entryPrivateKey = customtkinter.CTkEntry(self.keyFrame, placeholder_text="Input private key and hit enter")
        self.entryPrivateKey.bind("<Return>", command=lambda x: self.setPrivateKeyFromEntry())
        self.entryPrivateKey.grid(row=1, column=1, padx=(5, 0), pady=(5,0), sticky="ew")

        # Key display
        self.currentKeyFrame = customtkinter.CTkFrame(self.keyFrame, fg_color=self.cget("fg_color"))
        self.currentKeyFrame.columnconfigure((0,1), weight=1)
        self.currentKeyFrame.grid(row = 6, column = 0, rowspan=3, columnspan=2, padx=0, pady=(5,0), sticky="new")

        # public key display
        self.currentKeyFrameLabel = customtkinter.CTkLabel(self.currentKeyFrame, 
                                                     text="Public Key (Base 64)",
                                                     corner_radius=6, 
                                                     fg_color=['#979DA2', 'gray29'], 
                                                     text_color=['#DCE4EE', '#DCE4EE'])
        self.currentKeyFrameLabel.grid(row=0, column=0, columnspan=1, padx=(0,5), pady=0, sticky="ew")

        self.textbox1 = customtkinter.CTkTextbox(self.currentKeyFrame, state="disabled")
        self.textbox1.grid(row=1, column=0, padx=(0,5), pady=0, sticky="nsew")
        self.textbox1.insert("0.0", "")

        copyButton1 = customtkinter.CTkButton(self.currentKeyFrame, text ="Copy",
                            command = self.copyToClipboard1)
        copyButton1.grid(row = 2, column = 0, padx = (0,5), pady = 0, sticky="ew")

        # private key display
        self.currentKeyFrameLabel = customtkinter.CTkLabel(self.currentKeyFrame, 
                                                     text="Private Key (Base 64)",
                                                     corner_radius=6, 
                                                     fg_color=['#979DA2', 'gray29'], 
                                                     text_color=['#DCE4EE', '#DCE4EE'])
        self.currentKeyFrameLabel.grid(row=0, column=1, columnspan=1, padx=(5,0), pady=0, sticky="ew")

        self.textbox2 = customtkinter.CTkTextbox(self.currentKeyFrame, state="disabled")
        self.textbox2.grid(row=1, column=1, padx=(5,0), pady=0, sticky="nsew")
        self.textbox2.insert("0.0", "")

        copyButton2 = customtkinter.CTkButton(self.currentKeyFrame, text ="Copy",
                            command = self.copyToClipboard2)
        copyButton2.grid(row = 2, column = 1, padx = (5,0), pady = 0, sticky="ew")

        
        # Display public key
        self.textbox1.configure(state="normal")
        self.textbox1.delete('0.0', tk.END)
        self.textbox1.insert("0.0", self.currentPublicKey)
        self.textbox1.configure(state="disabled")

        # Display private key
        self.textbox2.configure(state="normal")
        self.textbox2.delete('0.0', tk.END)
        self.textbox2.insert("0.0", self.currentPrivateKey)
        self.textbox2.configure(state="disabled")
        
    
    def encrypt(self):
        inputText = self.entry.get("1.0", "end-1c")

        self.system.encryption2(inputText, self.currentPublicKey)
        cipherText = self.system.encrypted_text_base64

        self.textbox.configure(state="normal")
        self.textbox.delete('1.0', tk.END)
        self.textbox.insert("0.0", cipherText)
        self.textbox.configure(state="disabled")
        
    def decrypt(self):
        inputText = self.entry.get("1.0", "end-1c")

        cipherText = self.system.decryption(self.currentPrivateKey, inputText)

        self.textbox.configure(state="normal")
        self.textbox.delete('0.0', tk.END)
        self.textbox.insert("0.0", cipherText)
        self.textbox.configure(state="disabled")
    
    def copyToClipboard(self):
        self.clipboard_clear()
        self.clipboard_append(self.textbox.get('1.0', 'end-1c'))

    def copyToClipboard1(self):
        self.clipboard_clear()
        self.clipboard_append(self.textbox1.get('1.0', 'end-1c'))

    def copyToClipboard2(self):
        self.clipboard_clear()
        self.clipboard_append(self.textbox2.get('1.0', 'end-1c'))

    def swap(self):
        self.entry.delete('0.0', tk.END)
        self.entry.insert("0.0", self.textbox.get('1.0', 'end-1c'))
    
    def clearInput(self):
        self.entry.delete('0.0', tk.END)
    
    def generateKey(self):
        self.system.generate_new_key()
        self.currentPrivateKey = self.system.private_key_base64
        self.currentPublicKey = self.system.public_key_base64

        # Display keys
        self.textbox1.configure(state="normal")
        self.textbox1.delete('0.0', tk.END)
        self.textbox1.insert("0.0", self.currentPublicKey)
        self.textbox1.configure(state="disabled")

        self.textbox2.configure(state="normal")
        self.textbox2.delete('0.0', tk.END)
        self.textbox2.insert("0.0", self.currentPrivateKey)
        self.textbox2.configure(state="disabled")
    
    def setPublicKeyFromEntry(self):
        inputKey = self.entryPublicKey.get()
        self.currentPublicKey = inputKey

        # Display key
        self.textbox1.configure(state="normal")
        self.textbox1.delete('0.0', tk.END)
        self.textbox1.insert("0.0", self.currentPublicKey)
        self.textbox1.configure(state="disabled")
    
    def setPrivateKeyFromEntry(self):
        inputKey = self.entryPrivateKey.get()
        self.currentPrivateKey = inputKey

        # Display key
        self.textbox2.configure(state="normal")
        self.textbox2.delete('0.0', tk.END)
        self.textbox2.insert("0.0", self.currentPrivateKey)
        self.textbox2.configure(state="disabled")


# Rabin window frame
class RabinPage(customtkinter.CTkFrame):
    def __init__(self, parent, controller):
        self.n, self.p, self.q = Rabin.generate_keys_rabin(bits = 2048)

        customtkinter.CTkFrame.__init__(self, parent)

        self.grid_columnconfigure((0,2), weight=1)
        self.grid_columnconfigure(1, weight=0)

        label = customtkinter.CTkLabel(self,
                                       text="RABIN",
                                       font=customtkinter.CTkFont(size=20, weight="bold"))
        label.grid(row=0, column=0, columnspan=3, padx=20, pady=(10,0), sticky="w")

        # input
        self.entry = customtkinter.CTkTextbox(self)
        self.entry.grid(row=2, column=0, rowspan=2, padx=(20, 0), pady=0, sticky="nsew")
        self.entry.insert("0.0", "Attack at noon")

        self.maxNumLabel = customtkinter.CTkLabel(self, 
                                                     text="Max. characters for encryption: 254",
                                                     corner_radius=6, 
                                                     fg_color=['#979DA2', 'gray29'], 
                                                     text_color=['#DCE4EE', '#DCE4EE'])
        self.maxNumLabel.grid(row=1, column=0, padx=(20,0), pady=(20,0), sticky="ew")

        button1 = customtkinter.CTkButton(self, text ="Clear",
                            command = self.clearInput)
        button1.grid(row = 4, column = 0, padx = (20,0), pady = (0,10), sticky="ew")

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

        button1 = customtkinter.CTkButton(self,
                                          compound="right",
                                          text ="Encrypt                ", 
                                          image=lock1_image,
                                          command=self.encrypt)
        button1.grid(row = 2, column = 1, padx = 5, pady = 5, sticky="sew")

        button2 = customtkinter.CTkButton(self, 
                                          compound="right",
                                          text ="Decrypt                ", 
                                          image=lock2_image,
                                          command=self.decrypt)
        button2.grid(row = 3, column = 1, padx = 5, pady = 5, sticky="sew")

        
        # output
        self.textbox = customtkinter.CTkTextbox(self, state="disabled")
        self.textbox.grid(row=1, column=2, rowspan=3, padx=(0,20), pady=(20, 0), sticky="nsew")
        self.textbox.insert("0.0", "")
        button1 = customtkinter.CTkButton(self, text ="Copy",
                            command = self.copyToClipboard)
        button1.grid(row = 4, column = 2, padx = (0,20), pady = (0,10), sticky="ew")

        # Key part (generation)
        self.keyFrame = customtkinter.CTkFrame(self, fg_color=self.cget("fg_color"))
        self.keyFrame.columnconfigure(0, weight=0)
        self.keyFrame.columnconfigure(1, weight=1)
        self.keyFrame.grid(row = 5, column = 0, columnspan=3, padx=20, pady=(20,0), sticky="ew")
        button1 = customtkinter.CTkButton(self.keyFrame, 
                                          compound="right",
                                          text ="Generate Keys     ",
                                          image=dice_image,
                                          command = self.generateKey)
        button1.grid(row = 0, column = 0, padx = (0,5), pady = 0, sticky="new")


        # entry public key
        self.entryPublicKey = customtkinter.CTkEntry(self.keyFrame, placeholder_text="Input public key and hit enter")
        self.entryPublicKey.bind("<Return>", command=lambda x: self.setPublicKeyFromEntry())
        self.entryPublicKey.grid(row=0, column=1, padx=(5, 0), pady=0, sticky="ew")
        # entry public key1
        self.entryPrivateKey1 = customtkinter.CTkEntry(self.keyFrame, placeholder_text="Input private key part p and hit enter")
        self.entryPrivateKey1.bind("<Return>", command=lambda x: self.setPrivateKeyFromEntry1())
        self.entryPrivateKey1.grid(row=1, column=1, padx=(5, 0), pady=(5,0), sticky="ew")
        # entry public key2
        self.entryPrivateKey2 = customtkinter.CTkEntry(self.keyFrame, placeholder_text="Input private key part q and hit enter")
        self.entryPrivateKey2.bind("<Return>", command=lambda x: self.setPrivateKeyFromEntry2())
        self.entryPrivateKey2.grid(row=3, column=1, padx=(5, 0), pady=(5,0), sticky="ew")


        # Key display
        self.currentKeyFrame = customtkinter.CTkFrame(self.keyFrame, fg_color=self.cget("fg_color"))
        self.currentKeyFrame.columnconfigure((0,1,2), weight=1)
        self.currentKeyFrame.grid(row = 6, column = 0, rowspan=3, columnspan=2, padx=0, pady=(5,0), sticky="new")

        # public key display
        self.currentKeyFrameLabel = customtkinter.CTkLabel(self.currentKeyFrame, 
                                                     text="Public Key: n",
                                                     corner_radius=6, 
                                                     fg_color=['#979DA2', 'gray29'], 
                                                     text_color=['#DCE4EE', '#DCE4EE'])
        self.currentKeyFrameLabel.grid(row=0, column=0, columnspan=1, padx=(0,5), pady=0, sticky="ew")

        self.textbox1 = customtkinter.CTkTextbox(self.currentKeyFrame, state="disabled")
        self.textbox1.grid(row=1, column=0, padx=(0,5), pady=0, sticky="nsew")
        self.textbox1.insert("0.0", "")

        copyButton1 = customtkinter.CTkButton(self.currentKeyFrame, text ="Copy",
                            command = self.copyToClipboard1)
        copyButton1.grid(row = 2, column = 0, padx = (0,5), pady = 0, sticky="ew")

        # private key display1
        self.currentKeyFrameLabel = customtkinter.CTkLabel(self.currentKeyFrame, 
                                                     text="Private Key: p",
                                                     corner_radius=6, 
                                                     fg_color=['#979DA2', 'gray29'], 
                                                     text_color=['#DCE4EE', '#DCE4EE'])
        self.currentKeyFrameLabel.grid(row=0, column=1, columnspan=1, padx=(5,0), pady=0, sticky="ew")

        self.textbox2 = customtkinter.CTkTextbox(self.currentKeyFrame, state="disabled")
        self.textbox2.grid(row=1, column=1, padx=0, pady=0, sticky="nsew")
        self.textbox2.insert("0.0", "")

        copyButton2 = customtkinter.CTkButton(self.currentKeyFrame, text ="Copy",
                            command = self.copyToClipboard2)
        copyButton2.grid(row = 2, column = 1, padx = (5,0), pady = 0, sticky="ew")

        # private key display2
        self.currentKeyFrameLabel3 = customtkinter.CTkLabel(self.currentKeyFrame, 
                                                     text="Private Key: q",
                                                     corner_radius=6, 
                                                     fg_color=['#979DA2', 'gray29'], 
                                                     text_color=['#DCE4EE', '#DCE4EE'])
        self.currentKeyFrameLabel3.grid(row=0, column=2, columnspan=1, padx=(5,0), pady=0, sticky="ew")

        self.textbox3 = customtkinter.CTkTextbox(self.currentKeyFrame, state="disabled")
        self.textbox3.grid(row=1, column=2, padx=(5,0), pady=0, sticky="nsew")
        self.textbox3.insert("0.0", "")

        copyButton3 = customtkinter.CTkButton(self.currentKeyFrame, text ="Copy",
                            command = self.copyToClipboard3)
        copyButton3.grid(row = 2, column = 2, padx = (5,0), pady = 0, sticky="ew")

        
        # Display public key
        self.textbox1.configure(state="normal")
        self.textbox1.delete('0.0', tk.END)
        self.textbox1.insert("0.0", str(self.n))
        self.textbox1.configure(state="disabled")
        # Display private key1
        self.textbox2.configure(state="normal")
        self.textbox2.delete('0.0', tk.END)
        self.textbox2.insert("0.0", str(self.p))
        self.textbox2.configure(state="disabled")
        # Display private key2
        self.textbox3.configure(state="normal")
        self.textbox3.delete('0.0', tk.END)
        self.textbox3.insert("0.0", str(self.q))
        self.textbox3.configure(state="disabled")
        
    
    def encrypt(self):
        inputText = self.entry.get("1.0", "end-1c")

        if len(inputText) > 254:
            inputText = inputText[:254]
            self.entry.delete('1.0', tk.END)
            self.entry.insert("0.0", inputText)
        
        
        self.outText = Rabin.simpleEncryption(inputText, self.n)
        self.textbox.configure(state="normal")
        self.textbox.delete('1.0', tk.END)
        self.textbox.insert("0.0", self.outText)
        self.textbox.configure(state="disabled")
        
    def decrypt(self):
        inputText = self.entry.get("1.0", "end-1c")

        self.outText = Rabin.decrypt_rabin(int(inputText), self.p, self.q)

        self.textbox.configure(state="normal")
        self.textbox.delete('0.0', tk.END)
        self.textbox.insert("0.0", self.outText)
        self.textbox.configure(state="disabled")
    
    def copyToClipboard(self):
        self.clipboard_clear()
        self.clipboard_append(self.textbox.get('1.0', 'end-1c'))

    def copyToClipboard1(self):
        self.clipboard_clear()
        self.clipboard_append(self.textbox1.get('1.0', 'end-1c'))

    def copyToClipboard2(self):
        self.clipboard_clear()
        self.clipboard_append(self.textbox2.get('1.0', 'end-1c'))

    def copyToClipboard3(self):
        self.clipboard_clear()
        self.clipboard_append(self.textbox3.get('1.0', 'end-1c'))

    def swap(self):
        self.entry.delete('0.0', tk.END)
        self.entry.insert("0.0", self.textbox.get('1.0', 'end-1c'))
    
    def clearInput(self):
        self.entry.delete('0.0', tk.END)
    
    def generateKey(self):
        self.n, self.p, self.q = Rabin.generate_keys_rabin(bits = 2048)

        # Display keys
        self.textbox1.configure(state="normal")
        self.textbox1.delete('0.0', tk.END)
        self.textbox1.insert("0.0", str(self.n))
        self.textbox1.configure(state="disabled")

        # Display private key1
        self.textbox2.configure(state="normal")
        self.textbox2.delete('0.0', tk.END)
        self.textbox2.insert("0.0", str(self.p))
        self.textbox2.configure(state="disabled")
        # Display private key2
        self.textbox3.configure(state="normal")
        self.textbox3.delete('0.0', tk.END)
        self.textbox3.insert("0.0", str(self.q))
        self.textbox3.configure(state="disabled")
    
    def setPublicKeyFromEntry(self):
        inputKey = self.entryPublicKey.get().strip()
        try:
            self.n = int(inputKey)
        except:
            pass

        # Display key
        self.textbox1.configure(state="normal")
        self.textbox1.delete('0.0', tk.END)
        self.textbox1.insert("0.0", str(self.n))
        self.textbox1.configure(state="disabled")
    
    def setPrivateKeyFromEntry1(self):
        inputKey = self.entryPrivateKey1.get().strip()
        try:
            self.p = int(inputKey)
        except:
            pass

        # Display key
        self.textbox2.configure(state="normal")
        self.textbox2.delete('0.0', tk.END)
        self.textbox2.insert("0.0", str(self.p))
        self.textbox2.configure(state="disabled")
    
    def setPrivateKeyFromEntry2(self):
        inputKey = self.entryPrivateKey2.get().strip()
        try:
            self.q = int(inputKey)
        except:
            pass

        # Display key
        self.textbox3.configure(state="normal")
        self.textbox3.delete('0.0', tk.END)
        self.textbox3.insert("0.0", str(self.q))
        self.textbox3.configure(state="disabled")


# ElGammal window frame
class DSAPage(customtkinter.CTkFrame):
    def __init__(self, parent, controller):
        self.system = DSA_Signature()
        self.system.get_random_key() # 1024
        self.currentPrivateKey = self.system.get_private_key()
        self.currentPublicKey = self.system.get_public_key()
        self.dirtySign = False
        self.dirtyVerify = False
        self.dirtySignature = False
        self.signName = ""
        self.verifyName = ""
        self.signatureName = ""
        self.signBytes = None
        self.verifyBytes = None
        self.userSignature = None
        self.generatedSignature = None

        customtkinter.CTkFrame.__init__(self, parent)

        self.grid_columnconfigure((0,2), weight=1)
        self.grid_columnconfigure(1, weight=0)

        label = customtkinter.CTkLabel(self,
                                       text="DIGITAL SIGNATURE ALGORITHM WITH SHA-256",
                                       font=customtkinter.CTkFont(size=20, weight="bold"))
        label.grid(row=0, column=0, columnspan=3, padx=20, pady=10, sticky="w")


        
        # Sign file display
        self.signLabel = customtkinter.CTkLabel(self, 
                                                     text="File Signing",
                                                     corner_radius=6, 
                                                     fg_color=['#979DA2', 'gray29'], 
                                                     text_color=['#DCE4EE', '#DCE4EE'])
        self.signLabel.grid(row=1, column=0, columnspan=1, padx=5, pady=(0,5), sticky="ew")

        self.buttonSignIn = customtkinter.CTkButton(self, text ="Input file",
                            command = self.inputSign)
        self.buttonSignIn.grid(row = 2, column = 0, padx = 5, pady = (0,5), sticky="ew")

        self.textboxSign = customtkinter.CTkTextbox(self, state="disabled")
        self.textboxSign.grid(row=3, column=0, rowspan=2, padx=5, pady=0, sticky="nsew")
        self.textboxSign.insert("0.0", "")

        self.saveSign = customtkinter.CTkButton(self, text ="Save signature", 
                                                compound="right",
                                                image=save_image,
                                                command = self.saveSignature)
        self.saveSign.grid(row = 5, column = 0, padx = 5, pady = 0, sticky="ew")
        self.saveSign.grid_remove()
        self.buttonSign = customtkinter.CTkButton(self, text ="Sign file",
                            command = self.sign)
        self.buttonSign.grid(row = 5, column = 0, padx = 5, pady = 0, sticky="ew")


        # verify signature display
        self.verifyLabel = customtkinter.CTkLabel(self, 
                                                     text="Signature Verification",
                                                     corner_radius=6, 
                                                     fg_color=['#979DA2', 'gray29'], 
                                                     text_color=['#DCE4EE', '#DCE4EE'])
        self.verifyLabel.grid(row=1, column=2, columnspan=1, padx=5, pady=(0,5), sticky="ew")
        self.buttonVerifyIn = customtkinter.CTkButton(self, text ="Input file",
                            command = self.inputVerify)
        self.buttonVerifyIn.grid(row = 2, column = 2, padx = 5, pady=(0,5), sticky="ew")
        self.buttonVerifyIn = customtkinter.CTkButton(self, text ="Input signature",
                            command = self.inputSignature)
        self.buttonVerifyIn.grid(row = 3, column = 2, padx = 5, pady=0, sticky="ew")

        self.textboxVerify = customtkinter.CTkTextbox(self, state="disabled")
        self.textboxVerify.grid(row=4, column=2, padx=5, pady=(5,0), sticky="nsew")
        self.textboxVerify.insert("0.0", "")

        self.buttonVerify = customtkinter.CTkButton(self, text ="Verify signature",
                            command = self.verify)
        self.buttonVerify.grid(row = 5, column = 2, padx = 5, pady = 0, sticky="ew")


        # Key part (generation)
        self.keyFrame = customtkinter.CTkFrame(self, fg_color=self.cget("fg_color"))
        self.keyFrame.columnconfigure(0, weight=0)
        self.keyFrame.columnconfigure(1, weight=1)
        self.keyFrame.grid(row = 6, column = 0, columnspan=3, padx=5, pady=(20,0), sticky="ew")
        button1 = customtkinter.CTkButton(self.keyFrame, 
                                          compound="right",
                                          text ="Generate Keys     ",
                                          image=dice_image,
                                          command = self.generateKey)
        button1.grid(row = 0, column = 0, padx = (0,5), pady = 0, sticky="new")


        # entry public key
        self.entryPublicKey = customtkinter.CTkEntry(self.keyFrame, placeholder_text="Input public key and hit enter")
        self.entryPublicKey.bind("<Return>", command=lambda x: self.setPublicKeyFromEntry())
        self.entryPublicKey.grid(row=0, column=1, padx=(5, 0), pady=0, sticky="ew")
        # entry public key
        self.entryPrivateKey = customtkinter.CTkEntry(self.keyFrame, placeholder_text="Input private key and hit enter")
        self.entryPrivateKey.bind("<Return>", command=lambda x: self.setPrivateKeyFromEntry())
        self.entryPrivateKey.grid(row=1, column=1, padx=(5, 0), pady=(5,0), sticky="ew")

        # Key display
        self.currentKeyFrame = customtkinter.CTkFrame(self.keyFrame, fg_color=self.cget("fg_color"))
        self.currentKeyFrame.columnconfigure((0,1), weight=1)
        self.currentKeyFrame.grid(row = 6, column = 0, rowspan=3, columnspan=2, padx=0, pady=(5,0), sticky="new")

        # public key display
        self.currentKeyFrameLabel = customtkinter.CTkLabel(self.currentKeyFrame, 
                                                     text="Public Key (Base 64)",
                                                     corner_radius=6, 
                                                     fg_color=['#979DA2', 'gray29'], 
                                                     text_color=['#DCE4EE', '#DCE4EE'])
        self.currentKeyFrameLabel.grid(row=0, column=0, columnspan=1, padx=(0,5), pady=0, sticky="ew")

        self.textbox1 = customtkinter.CTkTextbox(self.currentKeyFrame, state="disabled")
        self.textbox1.grid(row=1, column=0, padx=(0,5), pady=0, sticky="nsew")
        self.textbox1.insert("0.0", "")

        copyButton1 = customtkinter.CTkButton(self.currentKeyFrame, text ="Copy",
                            command = self.copyToClipboard1)
        copyButton1.grid(row = 2, column = 0, padx = (0,5), pady = 0, sticky="ew")

        # private key display
        self.currentKeyFrameLabel = customtkinter.CTkLabel(self.currentKeyFrame, 
                                                     text="Private Key (Base 64)",
                                                     corner_radius=6, 
                                                     fg_color=['#979DA2', 'gray29'], 
                                                     text_color=['#DCE4EE', '#DCE4EE'])
        self.currentKeyFrameLabel.grid(row=0, column=1, columnspan=1, padx=(5,0), pady=0, sticky="ew")

        self.textbox2 = customtkinter.CTkTextbox(self.currentKeyFrame, state="disabled")
        self.textbox2.grid(row=1, column=1, padx=(5,0), pady=0, sticky="nsew")
        self.textbox2.insert("0.0", "")

        copyButton2 = customtkinter.CTkButton(self.currentKeyFrame, text ="Copy",
                            command = self.copyToClipboard2)
        copyButton2.grid(row = 2, column = 1, padx = (5,0), pady = 0, sticky="ew")

        
        # Display public key
        self.textbox1.configure(state="normal")
        self.textbox1.delete('0.0', tk.END)
        self.textbox1.insert("0.0", self.currentPublicKey)
        self.textbox1.configure(state="disabled")

        # Display private key
        self.textbox2.configure(state="normal")
        self.textbox2.delete('0.0', tk.END)
        self.textbox2.insert("0.0", self.currentPrivateKey)
        self.textbox2.configure(state="disabled")
        
    
    def sign(self):
        if self.dirtySign:
            self.generatedSignature = self.system.sign_with_user_private_key(self.currentPrivateKey, self.signBytes)

            self.textboxSign.configure(state="normal")
            self.textboxSign.delete('0.0', tk.END)
            self.textboxSign.insert("0.0", "Currently selected file:\n\t" + self.signName + "\nA signature for " + self.signName + " has been successfully created.")
            self.textboxSign.configure(state="disabled")

            self.saveSign.grid()
            self.buttonSign.grid_remove()
        else:
            self.textboxSign.configure(state="normal")
            self.textboxSign.delete('0.0', tk.END)
            self.textboxSign.insert("0.0", "No file has been entered.")
            self.textboxSign.configure(state="disabled")

        
    def verify(self):
        if self.dirtyVerify and self.dirtySignature:
            correct = self.system.verify_signature(self.verifyBytes, self.currentPublicKey, self.userSignature)

            self.textboxVerify.configure(state="normal")
            self.textboxVerify.delete('0.0', tk.END)
            if correct:
                self.textboxVerify.insert("0.0", "Currently selected file:\n\t" + self.verifyName + "\nCurrently selected signature:\n\t" + self.signatureName + "\n\nThe signed file is authentic.")
            else:
                self.textboxVerify.insert("0.0", "Currently selected file:\n\t" + self.verifyName + "\nCurrently selected signature:\n\t" + self.signatureName + "\n\nThe signature is invalid for the given file and public key. The file may have been tampered with.")
            self.textboxVerify.configure(state="disabled")
        elif self.dirtyVerify:
            self.textboxVerify.configure(state="normal")
            self.textboxVerify.delete('0.0', tk.END)
            self.textboxVerify.insert("0.0", "Currently selected file:\n\t" + self.verifyName + "\nNo signature has been entered.")
            self.textboxVerify.configure(state="disabled")
        else:
            self.textboxVerify.configure(state="normal")
            self.textboxVerify.delete('0.0', tk.END)
            self.textboxVerify.insert("0.0", "No file has been entered.")
            self.textboxVerify.configure(state="disabled")
    
    def inputVerify(self):
        # image dir
        
        verifyInput = filedialog.askopenfilename(initialdir = "/",
                                                    title = "Select a File")
        if verifyInput != "":
            self.dirtyVerify = True
            # name of file
            self.verifyName = os.path.basename(verifyInput)
            self.verifyBytes = self.system.leer_archivo_como_bytes(verifyInput)

            self.textboxVerify.configure(state="normal")
            self.textboxVerify.delete('0.0', tk.END)
            if self.dirtySignature:
                self.textboxVerify.insert("0.0", "Currently selected file:\n\t" + self.verifyName + "\nCurrently selected signature:\n\t" + self.signatureName)
            else:
                self.textboxVerify.insert("0.0", "Currently selected file:\n\t" + self.verifyName + "\nNo signature has been entered yet.")
            self.textboxVerify.configure(state="disabled")

    def inputSign(self):
        # image dir
        signInput = filedialog.askopenfilename(initialdir = "/",
                                                    title = "Select a File")
        if signInput != "":
            
            self.dirtySign = True
            
            # name of file
            self.signName = os.path.basename(signInput)
            self.signBytes = self.system.leer_archivo_como_bytes(signInput)

            self.textboxSign.configure(state="normal")
            self.textboxSign.delete('0.0', tk.END)
            self.textboxSign.insert("0.0", "Currently selected file:\n\t" + self.signName + "\n")
            self.textboxSign.configure(state="disabled")
            self.buttonSign.grid()
            self.saveSign.grid_remove()

    def inputSignature(self):
        # image dir
        
        signInput = filedialog.askopenfilename(initialdir = "/",
                                                    title = "Select a File")
        if signInput != "":
            self.dirtySignature = True
            # name of file
            self.signatureName = os.path.basename(signInput)
            self.userSignature = self.system.leer_archivo_como_bytes(signInput).hex()
            self.textboxVerify.configure(state="normal")
            self.textboxVerify.delete('0.0', tk.END)
            self.textboxVerify.insert("0.0", "Currently selected file:\n\t" + self.verifyName + "\nCurrently selected signature:\n\t" + self.signatureName)
            self.textboxVerify.configure(state="disabled")

    def saveSignature(self):
        file = filedialog.asksaveasfile(mode='wb', 
                                        filetypes = (("sig","*.sig"),
                                                    ('All files', '*.*')),
                                        defaultextension=".sig")
        if file:
            out_file = open(file.name, "wb")
            out_file.write(bytes.fromhex(self.generatedSignature))
            out_file.close()

    def copyToClipboard(self):
        self.clipboard_clear()
        self.clipboard_append(self.textbox.get('1.0', 'end-1c'))

    def copyToClipboard1(self):
        self.clipboard_clear()
        self.clipboard_append(self.textbox1.get('1.0', 'end-1c'))

    def copyToClipboard2(self):
        self.clipboard_clear()
        self.clipboard_append(self.textbox2.get('1.0', 'end-1c'))

    def swap(self):
        self.entry.delete('0.0', tk.END)
        self.entry.insert("0.0", self.textbox.get('1.0', 'end-1c'))
    
    def clearInput(self):
        self.entry.delete('0.0', tk.END)
    
    def generateKey(self):
        self.system.get_random_key()
        self.currentPrivateKey = self.system.get_private_key()
        self.currentPublicKey = self.system.get_public_key()

        # Display keys
        self.textbox1.configure(state="normal")
        self.textbox1.delete('0.0', tk.END)
        self.textbox1.insert("0.0", self.currentPublicKey)
        self.textbox1.configure(state="disabled")

        self.textbox2.configure(state="normal")
        self.textbox2.delete('0.0', tk.END)
        self.textbox2.insert("0.0", self.currentPrivateKey)
        self.textbox2.configure(state="disabled")
    
    def setPublicKeyFromEntry(self):
        inputKey = self.entryPublicKey.get()
        self.currentPublicKey = inputKey

        # Display key
        self.textbox1.configure(state="normal")
        self.textbox1.delete('0.0', tk.END)
        self.textbox1.insert("0.0", self.currentPublicKey)
        self.textbox1.configure(state="disabled")
    
    def setPrivateKeyFromEntry(self):
        inputKey = self.entryPrivateKey.get()
        self.currentPrivateKey = inputKey

        # Display key
        self.textbox2.configure(state="normal")
        self.textbox2.delete('0.0', tk.END)
        self.textbox2.insert("0.0", self.currentPrivateKey)
        self.textbox2.configure(state="disabled")


if __name__ == "__main__":
    
 
    # Adjust size
    app = App()
    app.mainloop()


                                                                                                  
