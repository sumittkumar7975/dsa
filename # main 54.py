# main.py

import tkinter as tk
from tkinter import messagebox
import sqlite3
from datetime import datetime
import os

# ---------------- DATABASE FOLDER SETUP ----------------
# Create folder if not exists
if not os.path.exists("data"):
    os.makedirs("data")

# Database will be stored inside data/app.db
conn = sqlite3.connect("data/app.db")
cursor = conn.cursor()

# ---------------- DATABASE SETUP ----------------
cursor.execute('''CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE,
    password TEXT
)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS contacts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    phone TEXT,
    email TEXT,
    company TEXT
)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS meetings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    contact_name TEXT,
    date TEXT,
    start_time TEXT,
    end_time TEXT,
    title TEXT,
    notes TEXT
)''')

conn.commit()

# ---------------- LOGIN WINDOW ----------------
root = tk.Tk()
root.title("Contact & Meet Hub")
root.geometry("400x300")

email_var = tk.StringVar()
pass_var = tk.StringVar()


def login():
    email = email_var.get()
    password = pass_var.get()

    if email == "shinghaniasumit@gmail.com" and password == "sumit@999":
        messagebox.showinfo("Success", "Login Successful")
        dashboard()
    else:
        messagebox.showerror("Error", "Invalid Credentials")


def register():
    email = email_var.get()
    password = pass_var.get()

    if email == "" or password == "":
        messagebox.showerror("Error", "All fields are required")
        return

    try:
        cursor.execute(
            "INSERT INTO users (email, password) VALUES (?, ?)",
            (email, password)
        )
        conn.commit()
        messagebox.showinfo("Success", "Account Created")
    except:
        messagebox.showerror("Error", "User already exists")


def dashboard():
    dash = tk.Toplevel()
    dash.title("Dashboard")
    dash.geometry("450x450")

    tk.Label(dash, text="Dashboard", font=("Arial", 18, "bold")).pack(pady=10)

    cursor.execute("SELECT COUNT(*) FROM contacts")
    total_contacts = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM meetings WHERE date >= ?",
        (datetime.now().strftime('%Y-%m-%d'),)
    )
    upcoming_meetings = cursor.fetchone()[0]

    stats_frame = tk.Frame(dash)
    stats_frame.pack(pady=10)

    tk.Label(stats_frame, text=f"Total Contacts: {total_contacts}", font=("Arial", 12)).pack(pady=5)
    tk.Label(stats_frame, text=f"Upcoming Meetings: {upcoming_meetings}", font=("Arial", 12)).pack(pady=5)

    tk.Button(dash, text="Add Contact", width=25, command=add_contact).pack(pady=5)
    tk.Button(dash, text="View Contacts", width=25, command=view_contacts).pack(pady=5)
    tk.Button(dash, text="Schedule Meeting", width=25, command=schedule_meeting).pack(pady=5)
    tk.Button(dash, text="View Meetings", width=25, command=view_meetings).pack(pady=5)


def add_contact():
    win = tk.Toplevel()
    win.title("Add Contact")

    name = tk.Entry(win)
    phone = tk.Entry(win)
    email = tk.Entry(win)
    company = tk.Entry(win)

    labels = ["Name", "Phone", "Email", "Company"]
    fields = [name, phone, email, company]

    for l, f in zip(labels, fields):
        tk.Label(win, text=l).pack()
        f.pack()

    def save():
        cursor.execute(
            "INSERT INTO contacts VALUES (NULL, ?, ?, ?, ?)",
            (name.get(), phone.get(), email.get(), company.get())
        )
        conn.commit()
        messagebox.showinfo("Saved", "Contact Added")
        win.destroy()

    tk.Button(win, text="Save", command=save).pack(pady=10)


def view_contacts():
    win = tk.Toplevel()
    win.title("Contacts")

    cursor.execute("SELECT name, phone FROM contacts")
    for c in cursor.fetchall():
        tk.Label(win, text=f"{c[0]} - {c[1]}").pack()


def schedule_meeting():
    win = tk.Toplevel()
    win.title("Schedule Meeting")

    contact = tk.Entry(win)
    date = tk.Entry(win)
    start = tk.Entry(win)
    end = tk.Entry(win)
    title = tk.Entry(win)
    notes = tk.Entry(win)

    fields = [contact, date, start, end, title, notes]
    labels = ["Contact Name", "Date (YYYY-MM-DD)", "Start Time", "End Time", "Title", "Notes"]

    for l, f in zip(labels, fields):
        tk.Label(win, text=l).pack()
        f.pack()

    def save_meeting():
        cursor.execute(
            "INSERT INTO meetings VALUES (NULL, ?, ?, ?, ?, ?, ?)",
            (contact.get(), date.get(), start.get(),
             end.get(), title.get(), notes.get())
        )
        conn.commit()
        messagebox.showinfo("Saved", "Meeting Scheduled")
        win.destroy()

    tk.Button(win, text="Save Meeting", command=save_meeting).pack(pady=10)


def view_meetings():
    win = tk.Toplevel()
    win.title("Meetings")

    cursor.execute("SELECT contact_name, date, title FROM meetings")
    for m in cursor.fetchall():
        tk.Label(win, text=f"{m[0]} | {m[1]} | {m[2]}").pack()


# ---------------- UI ----------------
tk.Label(root, text="Login", font=("Arial", 18)).pack(pady=10)

tk.Label(root, text="Email").pack()
tk.Entry(root, textvariable=email_var).pack()

tk.Label(root, text="Password").pack()
tk.Entry(root, textvariable=pass_var, show='*').pack()

tk.Button(root, text="Login", command=login).pack(pady=5)
tk.Button(root, text="Create Account", command=register).pack()

root.mainloop()
