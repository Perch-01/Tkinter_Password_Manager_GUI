import tkinter
from tkinter import messagebox
import os
import random
import pyperclip
from constants import letters, symbols, numbers, PATH_TO_IMAGE, PATH_TO_PASSWORD, WHITE, BLACK, MAX_NU_OF_SYMBOLS, MIN_NU_OF_SYMBOLS
import json

# ---------------------------- PASSWORD GENERATOR ------------------------------- #


def generatePassword():
    passw = ''
    toPush = []
    for n in range(MIN_NU_OF_SYMBOLS, MAX_NU_OF_SYMBOLS):
        toPush.append(1)
    for n in range(MIN_NU_OF_SYMBOLS, MAX_NU_OF_SYMBOLS):
        toPush.append(2)
    for n in range(MIN_NU_OF_SYMBOLS, MAX_NU_OF_SYMBOLS):
        toPush.append(3)
    while(len(toPush) != 0):
        # get a random index in topush array
        index = random.randint(0, len(toPush)-1)
        char = toPush[index]
        toPush.pop(index)

        if(char == 1):
            passw += letters[random.randint(0, len(letters)-1)]
        elif(char == 2):
            passw += symbols[random.randint(0, len(symbols)-1)]
        elif(char == 3):
            passw += numbers[random.randint(0, len(numbers)-1)]

    password_entry.delete(0, tkinter.END)
    password_entry.insert(0, passw)
    pyperclip.copy(passw)
# ---------------------------- SAVE PASSWORD ------------------------------- #


def savePassword():
    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    if len(website) == 0:
        messagebox.showinfo(
            title='Oops', message='You cannot leave the website field empty')
        return
    elif len(email) == 0:
        messagebox.showinfo(
            title='Oops', message='You cannot leave the email field empty')
        return
    elif len(password) == 0:
        messagebox.showinfo(
            title='Oops', message='You cannot leave the password field empty')
        return
    is_ok = messagebox.askokcancel(
        title=website, message=f"These are the details entered: \nEmail: {email}\nPassword: {password}")
    if is_ok:
        new_entry = {
            website: {
                'password': password,
                'email': email
            }
        }
        writeToFile(new_entry)
        website_entry.delete(0, tkinter.END)
        password_entry.delete(0, tkinter.END)


def writeToFile(entry):
    try:
        with open(PATH_TO_PASSWORD, mode='r') as file:
            pass
    except:
        # File doesnt exist, create it
        with open(PATH_TO_PASSWORD, mode='w') as file:
            # use JSON.dump to write data to a json file
            json.dump(entry, file, indent=4)
    else:
        # File exists, append to it
        with open(PATH_TO_PASSWORD, mode='r') as file:
            all_data = json.load(file)
            new_data = all_data.copy()
            # This is a way of updating dictionaries automaticallty
            new_data.update(entry)
            # use JSON.dump to write data to a json file
            with open(PATH_TO_PASSWORD, mode='w') as file_:
                json.dump(new_data, file_, indent=4)


def searchForPassword():
    website_value=website_entry.get()
    if(website_value == ''):
        messagebox.showinfo(
            title='Oops', message='Enter a website for us to use and search for your password')
        return
    try:
        with open(PATH_TO_PASSWORD, mode='r') as file:
            pass
    except:
        messagebox.showinfo(
            title='Password not found', message='You have not stored any password relating to this website')
    else:
        with open(PATH_TO_PASSWORD, mode='r') as file:
            all_data = json.load(file)
            try:
                all_data[website_value]
            except:
                messagebox.showinfo(
                    title='Password not found', message='You have not stored any password relating to this website')
            else:
                messagebox.showinfo(
                    title='Password found!', message=f'{website_value}\nEmail: {all_data[website_value]["email"]}\Password: {all_data[website_value]["password"]}\n\n Password has been copied to your clipboard!')
                pyperclip.copy(all_data[website_value]["password"])


# ---------------------------- UI SETUP ------------------------------- #
window = tkinter.Tk()
window.title('Password Manager')
window.configure(padx=50, pady=30, bg=WHITE)

canvas = tkinter.Canvas(width=200, height=230,
                        bg=WHITE, highlightthickness=0)
logo_img = tkinter.PhotoImage(file=PATH_TO_IMAGE)
# x and y coordinates are half of the width & height of the image
canvas.create_image(100, 145.5, image=logo_img)
canvas.grid(column=1, row=0)

tkinter.Label(text='Website:',  bg=WHITE, fg=BLACK).grid(row=1, column=0)
tkinter.Label(text='Email/Username:',  bg=WHITE,
              fg=BLACK).grid(row=2, column=0)
tkinter.Label(text='Password:',  bg=WHITE, fg=BLACK).grid(row=3, column=0)


website_entry = tkinter.Entry(width=22, bg=WHITE, highlightthickness=0)
website_entry.grid(
    row=1, column=1, columnspan=1, pady=5)
website_entry.focus()
email_entry = tkinter.Entry(width=39, bg=WHITE, highlightthickness=0)
email_entry.grid(
    row=2, column=1, columnspan=2, pady=2)
password_entry = tkinter.Entry(
    width=22, bg=WHITE, highlightthickness=0)
password_entry.grid(row=3, column=1, columnspan=1, pady=2)

search_website_button = tkinter.Button(
    text='Search for password', command=searchForPassword, bg=WHITE, highlightthickness=0, borderwidth=0).grid(row=1, column=2, columnspan=1, pady=2)
generate_password_button = tkinter.Button(
    text='Generate Password', command=generatePassword, bg=WHITE, highlightthickness=0, borderwidth=0).grid(row=3, column=2, columnspan=1, pady=2)
add_button = tkinter.Button(
    text='Add', command=savePassword, bg=WHITE, highlightthickness=0, borderwidth=0, width=36).grid(row=4, column=1, columnspan=2, pady=5)
window.mainloop()
