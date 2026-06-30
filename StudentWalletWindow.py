import tkinter as tk
from tkinter import messagebox
from db import session, Wallet

class StudentWalletWindow(tk.Frame):

    def __init__(self, master, user):
        super().__init__(master)
        self.master = master
        self.user = user

        # Title
        title_label = tk.Label(self, text="KSUWallet - Student Dashboard", font=("Arial", 20, "bold"))
        title_label.pack(pady=10)

        # Info Section
        info_frame = tk.Frame(self, borderwidth=1, relief="solid", padx=20, pady=20)
        info_frame.pack(pady=10, padx=20, fill="x")

        tk.Label(info_frame, text="Your Wallet Details", font=("Arial", 14, "bold")).pack(pady=(0, 10))
        
        tk.Label(info_frame, text=f"Wallet Number: {self.user.wallet_number}", font=("Arial", 12)).pack(anchor="w")
        
        self.lbl_balance = tk.Label(info_frame, text=f"Current Balance: {self.user.balance} SR", font=("Arial", 12, "bold"))
        self.lbl_balance.pack(anchor="w", pady=5)

        # Payment Form
        form_frame = tk.Frame(self)
        form_frame.pack(pady=20)

        tk.Label(form_frame, text="Target Wallet Number:", width=20, anchor="w").grid(row=0, column=0, pady=5, sticky="w")
        self.entry_target = tk.Entry(form_frame, width=25)
        self.entry_target.grid(row=0, column=1, pady=5)

        tk.Label(form_frame, text="Amount (SR):", width=20, anchor="w").grid(row=1, column=0, pady=5, sticky="w")
        self.entry_amount = tk.Entry(form_frame, width=25)
        self.entry_amount.grid(row=1, column=1, pady=5)

        # Buttons
        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=20)

        self.btn_pay = tk.Button(btn_frame, text="Pay", width=15, command=self.pay_action)
        self.btn_pay.grid(row=0, column=0, padx=10)

        self.btn_back = tk.Button(btn_frame, text="Back", width=15, command=self.go_back)
        self.btn_back.grid(row=0, column=1, padx=10)


    def pay_action(self):
        target_num = self.entry_target.get().strip()
        amount_txt = self.entry_amount.get().strip()

        if not target_num:
            messagebox.showerror("Error", "Please enter target wallet number")
            return

        if target_num == self.user.wallet_number:
            messagebox.showerror("Error", "You cannot pay to yourself")
            return

        try:
            amount = float(amount_txt)
        except:
            messagebox.showerror("Error", "Invalid amount format")
            return

        if amount <= 0:
            messagebox.showerror("Error", "Amount must be positive")
            return

        # Check balance from DB to be sure
        student_wallet = session.query(Wallet).filter(Wallet.id == self.user.id).first()

        if student_wallet.balance < amount:
            messagebox.showerror("Error", "There is not enough money")
            return

        # Check if target exists
        target_wallet = session.query(Wallet).filter(Wallet.wallet_number == target_num).first()
        
        if not target_wallet:
            messagebox.showerror("Error", "Target wallet number does not exist")
            return

        # Do transaction
        student_wallet.balance -= amount
        target_wallet.balance += amount
        session.commit()

        # Update UI
        self.user.balance = student_wallet.balance
        self.lbl_balance.config(text=f"Current Balance: {self.user.balance} SR")

        messagebox.showinfo("Success", "Transaction completed successfully")
        
        # Clear fields
        self.entry_target.delete(0, tk.END)
        self.entry_amount.delete(0, tk.END)


    def go_back(self):
        self.destroy()
        from SignUpWindow import SignUpWindow
        win = SignUpWindow(self.master)
        win.pack(fill="both", expand=True)