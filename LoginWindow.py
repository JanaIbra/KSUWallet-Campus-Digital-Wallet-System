import tkinter as tk
import tkinter.messagebox as msg
from db import session, Wallet



class LoginWindow(tk.Frame):

    def __init__(self, master):
        super().__init__(master)
        self.master = master

        title_label = tk.Label(self, text="KSUWallet - Login", font=("Arial", 20, "bold"))
        title_label.pack(pady=10)

        form_frame = tk.Frame(self)
        form_frame.pack(pady=10)

        tk.Label(form_frame, text="Student / Admin ID:", anchor="w", width=20) \
            .grid(row=0, column=0, pady=5, padx=5, sticky="w")
        self.id_entry = tk.Entry(form_frame, width=25)
        self.id_entry.grid(row=0, column=1, pady=5, padx=5)

        tk.Label(form_frame, text="Password:", anchor="w", width=20) \
            .grid(row=1, column=0, pady=5, padx=5, sticky="w")
        self.pw_entry = tk.Entry(form_frame, width=25, show="*")
        self.pw_entry.grid(row=1, column=1, pady=5, padx=5)
        
        
        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=15)

        self.login_btn = tk.Button(btn_frame, text="Login", width=12, command=self.login_action)
        self.login_btn.grid(row=0, column=0, padx=5)

        self.back_btn = tk.Button(btn_frame, text="Back", width=12, command=self.go_back)
        self.back_btn.grid(row=0, column=1, padx=5)

        

    def login_action(self):
        sid = self.id_entry.get().strip()
        pw = self.pw_entry.get().strip()

        # Validation 
        if not sid.isdigit() or len(sid) != 10:
            msg.showerror("Error", "ID must be 10 digits.")
            return

        if len(pw) == 0:
            msg.showerror("Error", "Password cannot be empty.")
            return

        # Query DB 
        user = session.query(Wallet).filter(Wallet.student_id == sid).first()

        if user is None:
            msg.showerror("Error", "User not found.")
            return

        if user.password != pw:
            msg.showerror("Error", "Incorrect password.")
            return

        # Redirect 
        if user.wallet_type == "admin":
            from AdminWindow import AdminWindow  # open admin dashboard
            msg.showinfo("Success", "Welcome Admin!")
            self.destroy()
            admin_window = AdminWindow(self.master, user)
            admin_window.pack(fill="both", expand=True)
        else:
            from StudentWalletWindow import StudentWalletWindow # open student page
            msg.showinfo("Success", f"Welcome {user.name}!")
            self.destroy()
            student_window = StudentWalletWindow(self.master, user)
            student_window.pack(fill="both", expand=True)
        


    def go_back(self):
        self.destroy()
        from SignUpWindow import SignUpWindow
        signup = SignUpWindow(self.master)
        signup.pack(fill="both", expand=True)
