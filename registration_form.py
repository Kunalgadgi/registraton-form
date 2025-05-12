import tkinter as tk
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk
from db_config import get_connection
import os

uploaded_photo_data = None

def upload_photo():
    global uploaded_photo_data, photo_label
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
    if file_path:
        with open(file_path, 'rb') as file:
            uploaded_photo_data = file.read()
        img = Image.open(file_path)
        img = img.resize((100, 100))
        photo = ImageTk.PhotoImage(img)
        photo_label.configure(image=photo)
        photo_label.image = photo

def submit_form():
    global uploaded_photo_data

    data = {
        "first_name": first_name.get(),
        "last_name": last_name.get(),
        "username": username.get(),
        "email": email.get(),
        "phone": phone.get(),
        "password": password.get(),
        "confirm_password": confirm_password.get()
    }

    if not all(data.values()) or uploaded_photo_data is None:
        messagebox.showerror("Error", "All fields and photo are required!")
        return
    if data["password"] != data["confirm_password"]:
        messagebox.showerror("Error", "Passwords do not match!")
        return

    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO users 
            (first_name, last_name, username, email, phone, password, photo)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (
            data["first_name"], data["last_name"], data["username"],
            data["email"], data["phone"], data["password"], uploaded_photo_data
        ))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Registration successful!")
        clear_form()
    except Exception as e:
        messagebox.showerror("Database Error", str(e))

def clear_form():
    global uploaded_photo_data
    for entry in [first_name, last_name, username, email, phone, password, confirm_password]:
        entry.delete(0, tk.END)
    
    uploaded_photo_data = None

    # Restore placeholder image
    placeholder_path = os.path.join("assets", "upload_placeholder.jpg")
    if os.path.exists(placeholder_path):
        upload_img = Image.open(placeholder_path)
        upload_img = upload_img.resize((100, 100))
        upload_photo_img = ImageTk.PhotoImage(upload_img)
        photo_label.configure(image=upload_photo_img)
        photo_label.image = upload_photo_img

# ---------------- UI ----------------
root = tk.Tk()
root.title("Modern Registration")
root.geometry("750x600")

# Background image
bg_path = os.path.join("assets", "background.jpg")
if os.path.exists(bg_path):
    bg_img = Image.open(bg_path)
    bg_img = bg_img.resize((750, 600))
    bg_photo = ImageTk.PhotoImage(bg_img)
    background_label = tk.Label(root, image=bg_photo)
    background_label.image = bg_photo
    background_label.place(x=0, y=0, relwidth=1, relheight=1)

# Main form frame
main = tk.Frame(root, bg="white", bd=2, relief="ridge")
main.place(relx=0.5, rely=0.5, anchor="center", width=600, height=550)

# Upload photo
placeholder_path = os.path.join("assets", "upload_placeholder.jpg")
upload_img = Image.open(placeholder_path)
upload_img = upload_img.resize((100, 100))
upload_photo_img = ImageTk.PhotoImage(upload_img)

photo_label = tk.Label(main, image=upload_photo_img, bg="white")
photo_label.image = upload_photo_img
photo_label.place(x=30, y=30)

upload_btn = tk.Button(main, text="Upload Photo", command=upload_photo, bg="white", fg="blue", bd=0)
upload_btn.place(x=40, y=140)

# Title
tk.Label(main, text="REGISTRATION", font=("Arial", 18, "bold"), fg="#008cba", bg="white").place(x=220, y=30)

# Fields
label_font = ("Arial", 10)
entry_width = 25

tk.Label(main, text="FIRST NAME", bg="white", font=label_font).place(x=160, y=80)
first_name = tk.Entry(main, width=entry_width)
first_name.place(x=160, y=100)

tk.Label(main, text="LAST NAME", bg="white", font=label_font).place(x=350, y=80)
last_name = tk.Entry(main, width=entry_width)
last_name.place(x=350, y=100)

tk.Label(main, text="USERNAME", bg="white", font=label_font).place(x=160, y=140)
username = tk.Entry(main, width=entry_width)
username.place(x=160, y=160)

tk.Label(main, text="EMAIL", bg="white", font=label_font).place(x=350, y=140)
email = tk.Entry(main, width=entry_width)
email.place(x=350, y=160)

tk.Label(main, text="PH. NUMBER", bg="white", font=label_font).place(x=160, y=200)
phone = tk.Entry(main, width=entry_width)
phone.place(x=160, y=220)

tk.Label(main, text="PASSWORD", bg="white", font=label_font).place(x=350, y=200)
password = tk.Entry(main, width=entry_width, show="*")
password.place(x=350, y=220)

tk.Label(main, text="CONFIRM PASSWORD", bg="white", font=label_font).place(x=160, y=260)
confirm_password = tk.Entry(main, width=entry_width, show="*")
confirm_password.place(x=160, y=280)

# Submit Button
submit_btn = tk.Button(main, text="SUBMIT", command=submit_form, bg="#008cba", fg="white", font=("Arial", 12), width=20)
submit_btn.place(x=200, y=330)

# Optional Decorative Image
left_img_path = os.path.join("assets", "left_image.jpg")
if os.path.exists(left_img_path):
    left_img = Image.open(left_img_path)
    left_img = left_img.resize((100, 100))
    left_image_tk = ImageTk.PhotoImage(left_img)
    tk.Label(main, image=left_image_tk, bg="white").place(x=30, y=400)

root.mainloop()
