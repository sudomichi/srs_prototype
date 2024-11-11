import sqlite3
import os
from tkinter import Tk, Label, Entry, Button, filedialog, messagebox, StringVar, PhotoImage, Toplevel
from tkinter.ttk import Treeview, Frame
from PIL import Image, ImageTk  # Requires the Pillow library

# Ensure you install the Pillow library
# pip install pillow

# Define the database file
DB_FILE = 'students.db'

# Connect to the SQLite database (it will be created if it doesn't exist) 
conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()

# Create the students table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        student_id TEXT NOT NULL UNIQUE,
        semester TEXT NOT NULL,
        picture_path TEXT NOT NULL
    )
''')
conn.commit()

# Function to add a student to the database
def add_student(name, student_id, semester, picture_path):
    try:
        cursor.execute('''
            INSERT INTO students (name, student_id, semester, picture_path)
            VALUES (?, ?, ?, ?)
        ''', (name, student_id, semester, picture_path))
        conn.commit()
        messagebox.showinfo("Success", "Student information saved successfully!")
        display_data()  # Refresh the table after saving
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "A student with this ID already exists.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

# Function to select an image file
def select_image_file():
    file_path = filedialog.askopenfilename(
        title="Select an image",
        filetypes=[("Image Files", "*.jpg;*.jpeg;*.png;*.gif;*.bmp")]
    )
    picture_path_var.set(file_path)  # Set the selected file path in the UI

# Function to open a full-size image
def open_full_image(image_path):
    top = Toplevel(root)
    top.title("Full Image")
    img = Image.open(image_path)
    img = img.resize((300, 300))  # Resize for display
    img = ImageTk.PhotoImage(img)
    Label(top, image=img).pack()
    top.mainloop()

# Function to display data in the Treeview table
def display_data():
    # Clear existing rows
    for row in data_tree.get_children():
        data_tree.delete(row)
    
    # Fetch data from the database
    cursor.execute("SELECT name, student_id, semester, picture_path FROM students")
    for row in cursor.fetchall():
        name, student_id, semester, picture_path = row
        img = Image.open(picture_path)
        img = img.resize((25, 25))  # Thumbnail size
        img = ImageTk.PhotoImage(img)
        data_tree.insert('', 'end', values=(name, student_id, semester, "Click to View"), tags=(picture_path,))
        data_tree.tag_bind(picture_path, '<Button-1>', lambda e, path=picture_path: open_full_image(path))

# Set up the main application window
root = Tk()
root.title("Student Database")
root.geometry("600x600")
root.configure(bg='#F0F0F0')

# UI variables
name_var = StringVar()
id_var = StringVar()
semester_var = StringVar()
picture_path_var = StringVar()

# Form Frame
form_frame = Frame(root, padding="10")
form_frame.pack(pady=20)

# Name field
Label(form_frame, text="Name:", background='#F0F0F0', font=("Arial", 12)).grid(row=0, column=0, sticky="w")
Entry(form_frame, textvariable=name_var, width=30).grid(row=0, column=1)

# ID field
Label(form_frame, text="ID:", background='#F0F0F0', font=("Arial", 12)).grid(row=1, column=0, sticky="w")
Entry(form_frame, textvariable=id_var, width=30).grid(row=1, column=1)

# Semester field
Label(form_frame, text="Semester:", background='#F0F0F0', font=("Arial", 12)).grid(row=2, column=0, sticky="w")
Entry(form_frame, textvariable=semester_var, width=30).grid(row=2, column=1)

# Picture Upload
Label(form_frame, text="Picture:", background='#F0F0F0', font=("Arial", 12)).grid(row=3, column=0, sticky="w")
Button(form_frame, text="Upload", command=select_image_file, bg="#007ACC", fg="white").grid(row=3, column=1, sticky="w")
Label(form_frame, textvariable=picture_path_var, background='#F0F0F0', font=("Arial", 10)).grid(row=3, column=1, sticky="e")

# Save button
def save_data():
    name = name_var.get()
    student_id = id_var.get()
    semester = semester_var.get()
    picture_path = picture_path_var.get()
    
    if not name or not student_id or not semester or not picture_path:
        messagebox.showwarning("Warning", "All fields must be filled out.")
        return
    
    add_student(name, student_id, semester, picture_path)

Button(form_frame, text="Save", command=save_data, bg="#007ACC", fg="white", width=10).grid(row=4, columnspan=2, pady=10)

# Display section
Label(root, text="Saved Records:", background='#F0F0F0', font=("Arial Bold", 14)).pack()

# Treeview to display data
columns = ("Name", "ID", "Semester", "Picture")
data_tree = Treeview(root, columns=columns, show="headings")
data_tree.heading("Name", text="Name")
data_tree.heading("ID", text="ID")
data_tree.heading("Semester", text="Semester")
data_tree.heading("Picture", text="Picture")
data_tree.pack(fill="both", expand=True, padx=10, pady=10)

display_data()  # Load initial data

root.mainloop()

# Close the database connection when done
conn.close()


