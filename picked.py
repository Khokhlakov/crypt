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
from Blocks import *

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
swords_image = customtkinter.CTkImage(Image.open("swords.png"), size=(18, 18))
lock1_image = customtkinter.CTkImage(Image.open("lock1.png"), size=(18, 18))
lock2_image = customtkinter.CTkImage(Image.open("lock2.png"), size=(18, 18))
home_image = customtkinter.CTkImage(Image.open("home.png"), size=(18, 18))

name_image = customtkinter.CTkImage(Image.open("name.png"), size=(400/3, 100/3))
nameLight_image = customtkinter.CTkImage(Image.open("nameLight.png"), size=(400/3, 100/3))


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        
        #self.title("CustomTkinter complex_example.py")
        self.geometry(f"{1100}x{580}")
        self.title("Picked")
        self.after(250, lambda: self.iconbitmap("icono.ico"))
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
                  ElGammalPage,
                  RabinPage,
                  Page2):

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
        if new_appearance_mode == 'Light':
            self.logo_label.configure(image=nameLight_image)
        else:
            self.logo_label.configure(image=name_image)

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
                                             command = lambda : controller.show_frame(ElGammalPage))
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

        
        button1 = customtkinter.CTkButton(self.ds_frame, text ="Affine",
        command = lambda : controller.show_frame(AffinePage))
        button1.grid(row = 1, column = 0, padx = 10, pady = 10, sticky="ew")

        button2 = customtkinter.CTkButton(self.ds_frame, text ="Page 2",
        command = lambda : controller.show_frame(Page2))
        button2.grid(row = 1, column = 1, padx = 10, pady = 10, sticky="ew")

        

       

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
        self.clipboard_append(self.textbox.get("0.0", tk.END))

    def swap(self):
        self.entry.delete('0.0', tk.END)
        self.entry.insert("0.0", self.textbox.get("0.0", tk.END))
    
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
                # Display recommended keys

                outputString = "Here is a list of keys with the text that results from deciphering with those keys. It has been ordered assuming the language of the plaintext is english.\n\n"

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
                outputString = "Test the following keys for " + self.system.lang + ":\n"

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
        self.clipboard_append(self.textbox.get("0.0", tk.END))

    def swap(self):
        self.entry.delete('0.0', tk.END)
        self.entry.insert("0.0", self.textbox.get("0.0", tk.END))
    
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

                outputString = "Here is a list of keys with the text that results from deciphering with those keys. It has been ordered assuming the language of the plaintext is english.\n\n"

                
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
                outputString = "Test the following keys for " + self.system.lang + ":\n"

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
        self.clipboard_append(self.textbox.get("0.0", tk.END))

    def swap(self):
        self.entry.delete('0.0', tk.END)
        self.entry.insert("0.0", self.textbox.get("0.0", tk.END))
    
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

                self.bestKeys = self.system2.getBestKeys2(cleanString)

                if numKeysStr == "All":
                    numKeys = len(self.bestKeys)
                else:
                    numKeys = int(numKeysStr)
                
                self.keyTextbox.configure(state="normal")

                if numKeysStr == "All":
                    tempSys = Desplazamiento(text=cleanString, codi="0a95")
                    # Display recommended keys

                    outputString = "Here is a list of keys with the text that results from deciphering with those keys. It has been ordered assuming the language of the plaintext is english.\n\n"


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
                    outputString = "Test the following keys for " + self.system.lang + ":\n"

                    for i in range(numKeys):
                        key = self.bestKeys[i][0]
                        outputString += str(key) + "\n"

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

                    outputString = "Here is a list of keys with the text that results from deciphering with those keys. It has been ordered assuming the language of the plaintext is english.\n\n"

                    
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
                    outputString = "Test the following keys for " + self.system.lang + ":\n"
                    
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
        button2.grid(row = 2, column = 0, padx = (0,5), pady = 20, sticky="new")

        # Number of keys to be recommended
        self.keyNumFrame = customtkinter.CTkFrame(self.keyFrame)
        self.keyNumFrame.columnconfigure(1, weight=1)
        self.keyNumFrame.grid(row = 2, column = 1, padx =0, pady = 20, sticky="new")

        self.keyLenFrame = customtkinter.CTkFrame(self.keyNumFrame)
        self.keyLenFrame.grid(row = 0, column = 0, padx=0, pady=0, sticky="ew")
        self.keyLenFrame.grid_columnconfigure(0, weight=1)
        self.keyLenFrame.grid_rowconfigure(0, weight=1)
        self.ds_frame_label = customtkinter.CTkLabel(self.keyLenFrame, 
                                                     text="Number of keys",
                                                     corner_radius=6)
        self.ds_frame_label.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")

        self.seg_button = customtkinter.CTkSegmentedButton(self.keyNumFrame)
        self.seg_button.grid(row=0, column=1, padx=0, pady=0, sticky="new")
        self.seg_button.configure(values=["1", "2", "3", "4", "5", "6", "7"])
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
        self.clipboard_append(self.textbox.get("0.0", tk.END))

    def swap(self):
        self.entry.delete('0.0', tk.END)
        self.entry.insert("0.0", self.textbox.get("0.0", tk.END))
    
    def clearInput(self):
        self.entry.delete('0.0', tk.END)

    def attack(self):
        self.system.lang = self.seg_lang.get()

        inputText = self.entry.get("0.0", tk.END)
        self.system.setText(inputText)
        cleanString = self.system.getCleanString()
        if cleanString != "":
            numKeys = int(self.seg_button.get())
            keys = self.system.getBestKeys(cleanString, num=numKeys)
            
            # Display recommended keys
            self.keyTextbox.configure(state="normal")
            outputString = "Test the following keys for " + self.system.lang + ":\n"

            for i in range(numKeys):
                key1 = keys[i][0]
                key2 = keys[i][1]
                outputString += str(key1) + "\n"
                if key1 != key2:
                    outputString += str(key2) + "\n"
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
        self.clipboard_append(self.textbox.get("0.0", tk.END))

    def swap(self):
        self.entry.delete('0.0', tk.END)
        self.entry.insert("0.0", self.textbox.get("0.0", tk.END))
    
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
        self.clipboard_append(self.textbox.get("0.0", tk.END))

    def swap(self):
        self.entry.delete('0.0', tk.END)
        self.entry.insert("0.0", self.textbox.get("0.0", tk.END))
    
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
        self.keyLen = 5
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
        self.tabs.tab("Image").grid_rowconfigure(1, weight=1)
        self.tabs.tab("Image").grid_rowconfigure(2, weight=0)
        

        # input image dir: self.imgName
        ### Start img mngmnt
        self.inputImgFrame = customtkinter.CTkFrame(self.tabs.tab("Image"))
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
        self.outputImgFrame.configure(width=300,height=300)
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
            self.img = np.append(self.img, np.random.randint(0, 255, size=newShape, dtype=int) , axis=0)
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


# AES window frame
class AESPage(customtkinter.CTkFrame):

    def __init__(self, parent, controller):
        self.dirty = False
        self.dirtyOutput = False

        self.keyAES = getRandAES(16)

        customtkinter.CTkFrame.__init__(self, parent)
        self.grid_columnconfigure((0,2), weight=1)
        self.grid_columnconfigure((1,3), weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=0)

        label = customtkinter.CTkLabel(self,
                                       text="AES",
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

        # key input
        self.entryKey = customtkinter.CTkEntry(self.keyFrame, placeholder_text="Input key and hit enter")
        self.entryKey.bind("<Return>", command=lambda x: self.setKeyFromEntry())
        self.entryKey.grid(row=0, column=1, columnspan=3, padx=(0, 5), pady=0, sticky="new")


        self.genButton = customtkinter.CTkButton(self.keyFrame, 
                                          compound="right",
                                          text ="Generate Key      ",
                                          image=dice_image,
                                          command = lambda : self.changeKey())
        self.genButton.grid(row = 1, column = 3, padx = (0,5), pady = 0, sticky="new")


        self.keyLenFrame = customtkinter.CTkFrame(self.keyFrame)
        self.keyLenFrame.grid(row = 1, column = 1, padx=0, pady=0, sticky="new")
        self.keyLenFrame.grid_columnconfigure(0, weight=1)
        self.keyLenFrame.grid_rowconfigure((0,1), weight=1)
        self.ds_frame_label = customtkinter.CTkLabel(self.keyLenFrame, 
                                                     text="Key size",
                                                     corner_radius=6)
        self.ds_frame_label.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")


        self.seg_button = customtkinter.CTkSegmentedButton(self.keyFrame)
        self.seg_button.grid(row=1, column=2, padx=(0, 5), pady=0, sticky="new")
        self.seg_button.configure(values=["16", "24", "32"])
        self.seg_button.set("16")

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
        self.textbox.insert("0.0", self.byteToHex(self.keyAES))
        self.textbox.configure(state="disabled")

    def browseFiles(self):
        self.dirty = True

        # image dir
        self.dirty = True
        self.imgName = filedialog.askopenfilename(initialdir = "/",
                                                    title = "Select a File",
                                                    filetypes = (("Picture files",
                                                                "*.png;*.jpg;*.ppm;*.bmp"),
                                                                ('All files', '*.*')))
        
        # file to be encrypted
        # original: self.img (array)
        self.img = np.array(iio.imread(self.imgName))

        # Save file to "plain_image.png"
        imgToEncrypt = self.img.astype('uint8')
        iio.imwrite("plain_image.png", imgToEncrypt)
        self.inputImageName = "plain_image.png"

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

            # Creates output named: 'aes_output.png'
            encrypt_image_AES(self.inputImageName, 
                              self.mode_seg_button.get(), 
                              self.keyAES)

            # Save save-able copy
            shutil.copy("aes_output.png","output_image_for_saving.png")
            self.imageOnOutputName = "aes_output.png"

            # file to be displayed
            self.anyFormatOutputImage = Image.open("aes_output.png")
            self.anyFormatOutputImage.thumbnail((500,500), Image.LANCZOS)
            self.resizedOutputImgName = "aes_output.ppm"
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
                              self.keyAES)

            # Save save-able copy
            shutil.copy("aes_output.png", "output_image_for_saving.png")
            self.imageOnOutputName = "aes_output.png"

            # file to be displayed
            self.anyFormatOutputImage = Image.open("aes_output.png")
            self.anyFormatOutputImage.thumbnail((500,500), Image.LANCZOS)
            self.resizedOutputImgName = "aes_output.ppm"
            self.anyFormatOutputImage.save(self.resizedOutputImgName)

            # Change label contents
            imgObject = PhotoImage(file = self.resizedOutputImgName)

            self.outputImg.configure(image=imgObject)


    def changeKey(self):
        self.keyAES = getRandAES(int(self.seg_button.get()))

        # Display key
        self.textbox.configure(state="normal")
        self.textbox.delete('0.0', tk.END)
        self.textbox.insert("0.0", self.byteToHex(self.keyAES))
        self.textbox.configure(state="disabled")
    
    def setKeyFromEntry(self):
        inputKey = self.entryKey.get()
        try:
            inputKeyList = inputKey.split(" ")
            self.keyAES = self.hexToByte(inputKeyList)
        except:
            pass

        # Display key
        self.textbox.configure(state="normal")
        self.textbox.delete('0.0', tk.END)
        self.textbox.insert("0.0", self.byteToHex(self.keyAES))
        self.textbox.configure(state="disabled")

    def saveFile(self):
        if self.dirtyOutput:
            myImage = Image.open("output_image_for_saving.png")
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
            iio.imwrite("plain_image.png", imgToEncrypt)

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
    
    def byteToHex(self, bytes):
        listBytes = list(bytes)
        return [hex(x).split('x')[-1] for x in listBytes]
    
    def hexToByte(self, hexList):
        return bytes([int(x,16) for x in hexList])
    

# TDES window frame
class TDESPage(customtkinter.CTkFrame):

    def __init__(self, parent, controller):
        self.dirty = False
        self.dirtyOutput = False

        self.keyTDES = getRandTDES(16)

        customtkinter.CTkFrame.__init__(self, parent)
        self.grid_columnconfigure((0,2), weight=1)
        self.grid_columnconfigure((1,3), weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=0)

        label = customtkinter.CTkLabel(self,
                                       text="TDES",
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

        # key input
        self.entryKey = customtkinter.CTkEntry(self.keyFrame, placeholder_text="Input key and hit enter")
        self.entryKey.bind("<Return>", command=lambda x: self.setKeyFromEntry())
        self.entryKey.grid(row=0, column=1, columnspan=3, padx=(0, 5), pady=0, sticky="new")


        self.genButton = customtkinter.CTkButton(self.keyFrame, 
                                          compound="right",
                                          text ="Generate Key      ",
                                          image=dice_image,
                                          command = lambda : self.changeKey())
        self.genButton.grid(row = 1, column = 3, padx = (0,5), pady = 0, sticky="new")


        self.keyLenFrame = customtkinter.CTkFrame(self.keyFrame)
        self.keyLenFrame.grid(row = 1, column = 1, padx=0, pady=0, sticky="new")
        self.keyLenFrame.grid_columnconfigure(0, weight=1)
        self.keyLenFrame.grid_rowconfigure((0,1), weight=1)
        self.ds_frame_label = customtkinter.CTkLabel(self.keyLenFrame, 
                                                     text="Key size",
                                                     corner_radius=6)
        self.ds_frame_label.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")


        self.seg_button = customtkinter.CTkSegmentedButton(self.keyFrame)
        self.seg_button.grid(row=1, column=2, padx=(0, 5), pady=0, sticky="new")
        self.seg_button.configure(values=["16", "24"])
        self.seg_button.set("16")

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
        self.textbox.insert("0.0", self.byteToHex(self.keyTDES))
        self.textbox.configure(state="disabled")

    def browseFiles(self):
        self.dirty = True

        # image dir
        self.dirty = True
        self.imgName = filedialog.askopenfilename(initialdir = "/",
                                                    title = "Select a File",
                                                    filetypes = (("Picture files",
                                                                "*.png;*.jpg;*.ppm;*.bmp"),
                                                                ('All files', '*.*')))
        
        # file to be encrypted
        # original: self.img (array)
        self.img = np.array(iio.imread(self.imgName))

        # Save file to "plain_image.png"
        imgToEncrypt = self.img.astype('uint8')
        iio.imwrite("plain_image_TDES.png", imgToEncrypt)
        self.inputImageName = "plain_image_TDES.png"

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

            # Creates output named: 'TDES_output.png'
            encrypt_image_TDES(self.inputImageName, 
                              self.mode_seg_button.get(), 
                              self.keyTDES)

            # Save save-able copy
            shutil.copy("TDES_output.png","output_image_for_saving_TDES.png")
            self.imageOnOutputName = "TDES_output.png"

            # file to be displayed
            self.anyFormatOutputImage = Image.open("TDES_output.png")
            self.anyFormatOutputImage.thumbnail((500,500), Image.LANCZOS)
            self.resizedOutputImgName = "TDES_output.ppm"
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
                              self.keyTDES)

            # Save save-able copy
            shutil.copy("TDES_output.png", "output_image_for_saving_TDES.png")
            self.imageOnOutputName = "TDES_output.png"

            # file to be displayed
            self.anyFormatOutputImage = Image.open("TDES_output.png")
            self.anyFormatOutputImage.thumbnail((500,500), Image.LANCZOS)
            self.resizedOutputImgName = "TDES_output.ppm"
            self.anyFormatOutputImage.save(self.resizedOutputImgName)

            # Change label contents
            imgObject = PhotoImage(file = self.resizedOutputImgName)

            self.outputImg.configure(image=imgObject)


    def changeKey(self):
        self.keyTDES = getRandTDES(int(self.seg_button.get()))

        # Display key
        self.textbox.configure(state="normal")
        self.textbox.delete('0.0', tk.END)
        self.textbox.insert("0.0", self.byteToHex(self.keyTDES))
        self.textbox.configure(state="disabled")
    
    def setKeyFromEntry(self):
        inputKey = self.entryKey.get()
        try:
            inputKeyList = inputKey.split(" ")
            self.keyTDES = self.hexToByte(inputKeyList)
        except:
            pass

        # Display key
        self.textbox.configure(state="normal")
        self.textbox.delete('0.0', tk.END)
        self.textbox.insert("0.0", self.byteToHex(self.keyTDES))
        self.textbox.configure(state="disabled")

    def saveFile(self):
        if self.dirtyOutput:
            myImage = Image.open("output_image_for_saving_TDES.png")
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
            iio.imwrite("plain_image_TDES.png", imgToEncrypt)

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
    
    def byteToHex(self, bytes):
        listBytes = list(bytes)
        return [hex(x).split('x')[-1] for x in listBytes]
    
    def hexToByte(self, hexList):
        return bytes([int(x,16) for x in hexList])


# S-DES window frame
class SDESPage(customtkinter.CTkFrame):

    def __init__(self, parent, controller):
        self.dirty = False
        self.dirtyOutput = False

        self.keyAES = getRandAES(16)

        customtkinter.CTkFrame.__init__(self, parent)
        self.grid_columnconfigure((0,2), weight=1)
        self.grid_columnconfigure((1,3), weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=0)

        label = customtkinter.CTkLabel(self,
                                       text="SDES",
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

        # key input
        self.entryKey = customtkinter.CTkEntry(self.keyFrame, placeholder_text="Input key and hit enter")
        self.entryKey.bind("<Return>", command=lambda x: self.setKeyFromEntry())
        self.entryKey.grid(row=0, column=1, columnspan=3, padx=(0, 5), pady=0, sticky="new")


        self.genButton = customtkinter.CTkButton(self.keyFrame, 
                                          compound="right",
                                          text ="Generate Key      ",
                                          image=dice_image,
                                          command = lambda : self.changeKey())
        self.genButton.grid(row = 1, column = 3, padx = (0,5), pady = 0, sticky="new")


        self.keyLenFrame = customtkinter.CTkFrame(self.keyFrame)
        self.keyLenFrame.grid(row = 1, column = 1, padx=0, pady=0, sticky="new")
        self.keyLenFrame.grid_columnconfigure(0, weight=1)
        self.keyLenFrame.grid_rowconfigure((0,1), weight=1)
        self.ds_frame_label = customtkinter.CTkLabel(self.keyLenFrame, 
                                                     text="Key size",
                                                     corner_radius=6)
        self.ds_frame_label.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")


        self.seg_button = customtkinter.CTkSegmentedButton(self.keyFrame)
        self.seg_button.grid(row=1, column=2, padx=(0, 5), pady=0, sticky="new")
        self.seg_button.configure(values=["16", "24", "32"])
        self.seg_button.set("16")

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
        self.textbox.insert("0.0", self.byteToHex(self.keyAES))
        self.textbox.configure(state="disabled")

    def browseFiles(self):
        self.dirty = True

        # image dir
        self.dirty = True
        self.imgName = filedialog.askopenfilename(initialdir = "/",
                                                    title = "Select a File",
                                                    filetypes = (("Picture files",
                                                                "*.png;*.jpg;*.ppm;*.bmp"),
                                                                ('All files', '*.*')))
        
        # file to be encrypted
        # original: self.img (array)
        self.img = np.array(iio.imread(self.imgName))

        # Save file to "plain_image.png"
        imgToEncrypt = self.img.astype('uint8')
        iio.imwrite("plain_image.png", imgToEncrypt)
        self.inputImageName = "plain_image.png"

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
        block = Blocks("S-DES", "CTR", 10)
        block.encrypt()
        block.decrypt()
        if self.dirty:
            self.dirtyOutput = True

            # Creates output named: 'aes_output.png'
            encrypt_image_AES(self.inputImageName, 
                              self.mode_seg_button.get(), 
                              self.keyAES)

            # Save save-able copy
            shutil.copy("aes_output.png","output_image_for_saving.png")
            self.imageOnOutputName = "aes_output.png"

            # file to be displayed
            self.anyFormatOutputImage = Image.open("aes_output.png")
            self.anyFormatOutputImage.thumbnail((500,500), Image.LANCZOS)
            self.resizedOutputImgName = "aes_output.ppm"
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
                              self.keyAES)

            # Save save-able copy
            shutil.copy("aes_output.png", "output_image_for_saving.png")
            self.imageOnOutputName = "aes_output.png"

            # file to be displayed
            self.anyFormatOutputImage = Image.open("aes_output.png")
            self.anyFormatOutputImage.thumbnail((500,500), Image.LANCZOS)
            self.resizedOutputImgName = "aes_output.ppm"
            self.anyFormatOutputImage.save(self.resizedOutputImgName)

            # Change label contents
            imgObject = PhotoImage(file = self.resizedOutputImgName)

            self.outputImg.configure(image=imgObject)


    def changeKey(self):
        self.keyAES = getRandAES(int(self.seg_button.get()))

        # Display key
        self.textbox.configure(state="normal")
        self.textbox.delete('0.0', tk.END)
        self.textbox.insert("0.0", self.byteToHex(self.keyAES))
        self.textbox.configure(state="disabled")
    
    def setKeyFromEntry(self):
        inputKey = self.entryKey.get()
        try:
            inputKeyList = inputKey.split(" ")
            self.keyAES = self.hexToByte(inputKeyList)
        except:
            pass

        # Display key
        self.textbox.configure(state="normal")
        self.textbox.delete('0.0', tk.END)
        self.textbox.insert("0.0", self.byteToHex(self.keyAES))
        self.textbox.configure(state="disabled")

    def saveFile(self):
        if self.dirtyOutput:
            myImage = Image.open("output_image_for_saving.png")
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
            iio.imwrite("plain_image.png", imgToEncrypt)

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
                                                     text="Max. characters for encryption: 189",
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
        inputText = self.entry.get("0.0", tk.END)

        if len(inputText) > 189:
            inputText = inputText[:189]
            self.entry.delete('1.0', tk.END)
            self.entry.insert("0.0", inputText)
        
        self.system.encrypt_message(inputText)
        cipherText = self.system.encrypted_message

        self.textbox.configure(state="normal")
        self.textbox.delete('1.0', tk.END)
        self.textbox.insert("0.0", cipherText)
        self.textbox.configure(state="disabled")
        
    def decrypt(self):
        inputText = self.entry.get("0.0", tk.END)

        self.system.encrypted_message = inputText
        self.system.decrypt_message()
        cipherText = self.system.decrypted_message

        self.textbox.configure(state="normal")
        self.textbox.delete('0.0', tk.END)
        self.textbox.insert("0.0", cipherText)
        self.textbox.configure(state="disabled")
    
    def copyToClipboard(self):
        self.clipboard_clear()
        self.clipboard_append(self.textbox.get("0.0", tk.END))

    def copyToClipboard1(self):
        self.clipboard_clear()
        self.clipboard_append(self.textbox1.get("0.0", tk.END))

    def copyToClipboard2(self):
        self.clipboard_clear()
        self.clipboard_append(self.textbox2.get("0.0", tk.END))

    def swap(self):
        self.entry.delete('0.0', tk.END)
        self.entry.insert("0.0", self.textbox.get("0.0", tk.END))
    
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
class ElGammalPage(customtkinter.CTkFrame):
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
        inputText = self.entry.get("0.0", tk.END)

        self.system.encryption2(inputText, self.currentPublicKey)
        cipherText = self.system.encrypted_text_base64

        self.textbox.configure(state="normal")
        self.textbox.delete('1.0', tk.END)
        self.textbox.insert("0.0", cipherText)
        self.textbox.configure(state="disabled")
        
    def decrypt(self):
        inputText = self.entry.get("0.0", tk.END)

        cipherText = self.system.decryption(self.currentPrivateKey, inputText)

        self.textbox.configure(state="normal")
        self.textbox.delete('0.0', tk.END)
        self.textbox.insert("0.0", cipherText)
        self.textbox.configure(state="disabled")
    
    def copyToClipboard(self):
        self.clipboard_clear()
        self.clipboard_append(self.textbox.get("0.0", tk.END))

    def copyToClipboard1(self):
        self.clipboard_clear()
        self.clipboard_append(self.textbox1.get("0.0", tk.END))

    def copyToClipboard2(self):
        self.clipboard_clear()
        self.clipboard_append(self.textbox2.get("0.0", tk.END))

    def swap(self):
        self.entry.delete('0.0', tk.END)
        self.entry.insert("0.0", self.textbox.get("0.0", tk.END))
    
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
                                                     text="Max. characters for encryption: 253",
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
        inputText = self.entry.get("0.0", tk.END)

        if len(inputText) > 253:
            inputText = inputText[:253]
            self.entry.delete('1.0', tk.END)
            self.entry.insert("0.0", inputText)

        cipherText = Rabin.simpleEncryption(inputText, self.n)

        self.textbox.configure(state="normal")
        self.textbox.delete('1.0', tk.END)
        self.textbox.insert("0.0", cipherText)
        self.textbox.configure(state="disabled")
        
    def decrypt(self):
        inputText = self.entry.get("0.0", tk.END)

        cipherText = Rabin.decrypt_rabin(int(inputText), self.p, self.q)

        self.textbox.configure(state="normal")
        self.textbox.delete('0.0', tk.END)
        self.textbox.insert("0.0", cipherText)
        self.textbox.configure(state="disabled")
    
    def copyToClipboard(self):
        self.clipboard_clear()
        self.clipboard_append(self.textbox.get("0.0", tk.END))

    def copyToClipboard1(self):
        self.clipboard_clear()
        self.clipboard_append(self.textbox1.get("0.0", tk.END))

    def copyToClipboard2(self):
        self.clipboard_clear()
        self.clipboard_append(self.textbox2.get("0.0", tk.END))

    def copyToClipboard3(self):
        self.clipboard_clear()
        self.clipboard_append(self.textbox3.get("0.0", tk.END))

    def swap(self):
        self.entry.delete('0.0', tk.END)
        self.entry.insert("0.0", self.textbox.get("0.0", tk.END))
    
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
        inputKey = self.entryPublicKey.get()
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
        inputKey = self.entryPrivateKey1.get()
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
        inputKey = self.entryPrivateKey2.get()
        try:
            self.q = int(inputKey)
        except:
            pass

        # Display key
        self.textbox3.configure(state="normal")
        self.textbox3.delete('0.0', tk.END)
        self.textbox3.insert("0.0", str(self.q))
        self.textbox3.configure(state="disabled")


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

  

                                                                                                  
