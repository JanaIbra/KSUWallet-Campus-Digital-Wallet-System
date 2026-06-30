import tkinter as tk
from tkinter import messagebox
import re, datetime, random

from db import session, Wallet


class SignUpWindow(tk.Frame):
    
    def __init__(self, master):
        
        super().__init__(master)
        self.master = master


        title_label = tk.Label(self, text="KSUWallet - Sign Up", font=("Arial", 20, "bold"))
        title_label.pack(pady=10)       
        
        form_frame = tk.Frame(self)
        form_frame.pack(pady=10)

        tk.Label(form_frame, text="First Name:", anchor="w", width=25).grid(row=0, column=0, pady=3, sticky="w")
        self.entry_first = tk.Entry(form_frame, width=25)
        self.entry_first.grid(row=0, column=1, pady=3)

        tk.Label(form_frame, text="Last Name:", anchor="w", width=25).grid(row=1, column=0, pady=3, sticky="w")
        self.entry_last = tk.Entry(form_frame, width=25)
        self.entry_last.grid(row=1, column=1, pady=3)

        tk.Label(form_frame, text="Student ID (10 digits):", anchor="w", width=25).grid(row=2, column=0, pady=3, sticky="w")
        self.entry_sid = tk.Entry(form_frame, width=25)
        self.entry_sid.grid(row=2, column=1, pady=3)

        tk.Label(form_frame, text="Email (@student.ksu.edu.sa):", anchor="w", width=25).grid(row=3, column=0, pady=3, sticky="w")
        self.entry_email = tk.Entry(form_frame, width=25)
        self.entry_email.grid(row=3, column=1, pady=3)

        tk.Label(form_frame, text="Phone (05XXXXXXXX):", anchor="w", width=25).grid(row=4, column=0, pady=3, sticky="w")
        self.entry_phone = tk.Entry(form_frame, width=25)
        self.entry_phone.grid(row=4, column=1, pady=3)

        tk.Label(form_frame, text="Password (>= 6):", anchor="w", width=25).grid(row=5, column=0, pady=3, sticky="w")
        self.entry_pw = tk.Entry(form_frame, width=25, show="*")
        self.entry_pw.grid(row=5, column=1, pady=3)


        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=10)

        self.submit_btn = tk.Button(btn_frame, text="Submit", width=15, command=self.on_submit)
        self.submit_btn.grid(row=0, column=0, padx=5)

        self.login_btn = tk.Button(btn_frame, text="Login", width=15, command=self.go_to_login)
        self.login_btn.grid(row=0, column=1, padx=5)

    
    
    def validate_inputs(self):
            
            first = str(self.entry_first.get()).strip()
            last = str(self.entry_last.get()).strip()
            sid = str(self.entry_sid.get()).strip()
            email = str(self.entry_email.get()).strip()
            phone = str(self.entry_phone.get()).strip()
            pw = str(self.entry_pw.get()).strip()

            #First / Last name
            if not first:
                messagebox.showinfo("Invalid name", "First name can't be empty")
                return None
            if not last:
                messagebox.showinfo("Invalid name", "Last name can't be empty")
                return None

            #Student ID: 10 digits
            reg = "^[0-9]{10}$"
            pat = re.compile(reg)
            x = re.search(pat, sid)
            if not x:
                messagebox.showinfo("Invalid Student ID", "Student ID must consist of 10 digits")
                return None

            #Password: at least 6 letters/digits
            reg = "^[a-zA-Z0-9]{6,}$" #There is no upper limit
            pat = re.compile(reg)
            x = re.search(pat, pw)
            if not x:
                messagebox.showinfo("Invalid Password", "Password must be at least 6 characters (letters or digits)")
                return None

            #Email: xxxxxxxx@student.ksu.edu.sa
            reg = r"^([a-zA-Z0-9\._-]+)(@student\.ksu\.edu\.sa)$"
            pat = re.compile(reg)
            x = re.search(pat, email)
            if not x:
                messagebox.showinfo("Invalid Email", "Email must be in this format: xxxxxxxx@student.ksu.edu.sa")
                return None

            #Phone: 05XXXXXXXX
            reg = r"^(05)[0-9]{8}$"
            pat = re.compile(reg)
            x = re.search(pat, phone)
            if not x:
                messagebox.showinfo("Invalid Phone Number", "Phone Number must start with 05 and consist of 10 digits")
                return None

        
            return first, last, sid, email, phone, pw
    
    
    def on_submit(self):

        result = self.validate_inputs()
        if result is None:
            return

        first, last, sid, email, phone, pw = result

        existing = session.query(Wallet).filter(Wallet.student_id == sid,
            Wallet.wallet_type == "student").first()

        if existing:
            messagebox.showerror("Error", "Student already registered with this ID.")
            return

        wallet_number = str(random.randint(10**9, 10**10 - 1))
        full_name = f"{first} {last}"

        new_wallet = Wallet(
            student_id=sid,
            name=full_name,
            password=pw,  
            email=email,
            phone=phone,
            wallet_number=wallet_number,
            wallet_type="student",
            balance=1000.0,
            created_at=datetime.datetime.now()
        )

        session.add(new_wallet)
        session.commit()

        messagebox.showinfo("Success", f"Student registered successfully.\nWallet Number: {wallet_number}")

        

    
    def go_to_login(self):
        self.destroy()
        from LoginWindow import LoginWindow
        login_window = LoginWindow(self.master)
        login_window.pack(fill="both", expand=True)



if __name__ == "__main__":
    root = tk.Tk()
    root.title("KSUWallet")
    root.geometry("550x550")

    signup = SignUpWindow(root)
    signup.pack(fill="both", expand=True)

    root.mainloop()