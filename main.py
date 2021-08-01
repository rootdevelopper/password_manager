from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import pyperclip
import json


# ---------------------------- PASSWORD GENERATOR ------------------------------- #

# Password Generator Project
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [choice(letters) for _ in range(randint(8, 10))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]

    password_list = password_letters + password_symbols + password_numbers
    shuffle(password_list)

    password = "".join(password_list)
    password_entry.insert(0, password)
    # pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    new_data = {
        website: {
            "email": email,
            "password": password
        }
    }

    if len(website) == 0 or len(password) == 0:
        messagebox.showinfo(title="Oops", message="Please make sure you haven't left any fields empty.")
    else:
        is_ok = messagebox.askokcancel(title=website, message=f"These are the details entered: \nEmail: {email} "
                                                              f"\nPassword: {password} \nIs it ok to save?")
        if is_ok:
            # save_as_json(new_data)
            try:
                data = load_json_data()
                print(f'loaded data {data}')
                with open('data.json', "w") as data_file:
                    data.update(new_data)
                    json.dump(data, data_file, indent=4)

            except json.decoder.JSONDecodeError:
                save_as_json(new_data)
            except FileNotFoundError:
                save_as_json(new_data)
            finally:
                website_entry.delete(0, END)
                password_entry.delete(0, END)


def load_json_data():
    with open('data.json', "r") as data_file:
        data = json.load(data_file)
        print(data)
        return data


def save_as_json(new_data):
    with open("data.json", "w") as datafile:
        json.dump(new_data, datafile, indent=4)


def save_as_csv(email, password, website):
    with open("data.txt", "a") as data_file:
        data_file.write(f"{website} | {email} | {password}\n")


# ---------------------------- Search PPassword ------------------------ #
def search_password():
    website = website_entry.get()
    print(f"search for {website}")
    data = load_json_data()
    if data is None:
        messagebox.showerror(title="Oops",
                             message="There are no passwords saved yet, please save at least one password first")
    if website in data:
        saved_email = data[website]['email']
        saved_password = data[website]['password']
        print(f'saved email {saved_email}')
        print(f'saved pass {saved_password}')
        messagebox.showinfo(title=f"{website}", message=f"E-mail: {saved_email}\npassword: {saved_password} \n")


# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

canvas = Canvas(height=200, width=200)
logo_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(row=0, column=1)

# Labels
website_label = Label(text="Website:")
website_label.grid(row=1, column=0)
email_label = Label(text="Email/Username:")
email_label.grid(row=2, column=0)
password_label = Label(text="Password:")
password_label.grid(row=3, column=0)

# Entries
website_entry = Entry(width=35)
website_entry.grid(row=1, column=1, columnspan=2)
website_entry.focus()
email_entry = Entry(width=35)
email_entry.grid(row=2, column=1, columnspan=2)
email_entry.insert(0, "someuseremail@someuseremail.com")
password_entry = Entry(width=21)
password_entry.grid(row=3, column=1)

# Buttons

search_password_button = Button(text="Search", command=search_password)
search_password_button.grid(row=1, column=3)
generate_password_button = Button(text="Generate Password", command=generate_password)
generate_password_button.grid(row=3, column=2)
add_button = Button(text="Add", width=36, command=save)
add_button.grid(row=4, column=1, columnspan=2)

window.mainloop()
