import tkinter as tk
import tkinter.messagebox as msg
import random, datetime
from db import session, Wallet


class AdminWindow(tk.Frame):
    def __init__(self, master, user):
        super().__init__(master)
        self.master = master
        self.user = user

        # Window Title 
        title_label = tk.Label(self, text="KSUWallet - Admin Dashboard", font=("Arial", 18, "bold"))
        title_label.pack(pady=10)

        #Navigation buttons (tabs)
        tab_frame = tk.Frame(self)
        tab_frame.pack(pady=10)
        tk.Button(tab_frame, text="View Entities", width=15, command=self.show_view_tab).grid(row=0, column=0, padx=5)
        tk.Button(tab_frame, text="Add KSU Entity", width=15, command=self.show_add_tab).grid(row=0, column=1, padx=5)
        tk.Button(tab_frame, text="Manage", width=15, command=self.show_manage_tab).grid(row=0, column=2, padx=5)

        #Frames for tabs
        self.view_frame = tk.Frame(self)
        self.add_frame = tk.Frame(self)
        self.manage_frame = tk.Frame(self)

        for f in (self.view_frame, self.add_frame, self.manage_frame):
            f.pack_propagate(False)

        #Build tabs content
        self.build_view_tab()
        self.build_add_tab()
        self.build_manage_tab()

        #Show default tab
        self.show_view_tab()

        #Back button to Sign Up window
        back_btn = tk.Button(self, text="Back", width=15, command=self.go_back)
        back_btn.pack(pady=20)
    
    
    def build_view_tab(self):
        #Tab for viewing KSU entities
        wrapper = tk.Frame(self.view_frame)
        wrapper.pack(fill="both", expand=True, pady=10)

        tk.Label(wrapper, text="Entities:", font=("Arial", 14, "bold")).pack(pady=10)

        # List of KSU entities
        self.entity_listbox = tk.Listbox(wrapper, width=40, height=12)
        self.entity_listbox.pack(pady=5)

        tk.Button(wrapper, text="View balance", width=20, command=self.view_details_action).pack(pady=10)
    
    
    def refresh_entities(self):
        #Refresh listbox content from DB
        session.expire_all()
        self.entity_listbox.delete(0, tk.END)
        
        all_entities = session.query(Wallet).filter(Wallet.wallet_type == "KSU" ).all()
        
        for e in all_entities:
            self.entity_listbox.insert(tk.END, e.name)
    
    
    def view_details_action(self):
        #Show selected entity details
        session.expire_all()
        sel = self.entity_listbox.curselection()
        if not sel:
            msg.showerror("Error", "Please select an entity.")
            return

        name = self.entity_listbox.get(sel[0])
        entity = session.query(Wallet).filter(Wallet.name == name).first()

        if not entity:
            msg.showerror("Error", "Entity not found.")
            return

        # Display entity info
        msg.showinfo(
            "Entity Details",
            f"Name: {entity.name}\n"
            f"Type: {entity.wallet_type}\n"
            f"Entity ID: {entity.student_id}\n"
            f"Wallet Number: {entity.wallet_number}\n"
            f"Balance: {entity.balance} SR\n"
        )
    
    
    def build_add_tab(self):
        #Tab to create new entity
        wrapper = tk.Frame(self.add_frame)
        wrapper.pack(fill="both", expand=True, pady=10)

        tk.Label(wrapper, text="Add New KSU Entity", font=("Arial", 14, "bold")).pack(pady=10)

        # Form input
        form = tk.Frame(wrapper)
        form.pack(pady=10)

        tk.Label(form, text="Entity Name:", width=20, anchor="w").grid(row=0, column=0, pady=5)
        self.entry_entity_name = tk.Entry(form, width=25)
        self.entry_entity_name.grid(row=0, column=1, pady=5)

        tk.Button(wrapper, text="Create Entity", width=18,command=self.add_entity_action).pack(pady=15)
    
    
    def add_entity_action(self):
        #Create new KSU entity wallet
        name = self.entry_entity_name.get().strip()

        if len(name) == 0:
            msg.showerror("Error", "Entity name cannot be empty.")
            return

        # Prevent duplicate names
        existing = session.query(Wallet).filter(Wallet.name == name,  Wallet.wallet_type == "KSU").first()
        if existing:
            msg.showerror("Error", "KSU entity with this name already exists.")
            return

        # Generate unique IDs
        while True:
            dummy_sid = str(random.randint(10**9, 10**10 - 1))
            if not session.query(Wallet).filter(Wallet.student_id == dummy_sid).first():
                break

        while True:
            wallet_number = str(random.randint(10**9, 10**10 - 1))
            if not session.query(Wallet).filter(Wallet.wallet_number == wallet_number).first():
                break

        # Save to DB
        new_entity = Wallet(
            student_id=dummy_sid,
            name=name,
            password="none",
            email="none",
            phone="none",
            wallet_number=wallet_number,
            wallet_type="KSU",
            balance=0.0,
            created_at=datetime.datetime.now()
        )
        session.add(new_entity)
        session.commit()
        session.expire_all()

        # Show confirmation
        msg.showinfo(
            "KSU Entity Created",
            f"KSU entity successfully created!\n\n"
            f"Name: {name}\n"
            f"Wallet Number: {wallet_number}\n"
        )

        self.entry_entity_name.delete(0, tk.END)
        self.refresh_entities()
    
    
    def build_manage_tab(self):
        #Tab for admin actions
        wrapper = tk.Frame(self.manage_frame)
        wrapper.pack(fill="both", expand=True, pady=10)
        tk.Label(wrapper, text="Manage System", font=("Arial", 14, "bold")).pack(pady=15)
        tk.Button(wrapper, text="Pay Stipends", width=30,command=self.pay_stipends_action).pack(pady=10)
        tk.Button(wrapper, text="Cash Out", width=30, command=self.cash_out_action).pack(pady=10)
    
    
    def pay_stipends_action(self):
        #Add 1000 SR to all student wallets
        session.rollback()
        students = session.query(Wallet).filter(Wallet.wallet_type == "student").all()

        if not students:
            msg.showinfo("Info", "No student wallets found.")
            return

        for s in students:
            s.balance += 1000.0

        session.commit()
        session.expire_all()
        msg.showinfo("Success", "1000 SR deposited to all student wallets.")
        self.refresh_entities()
    
    
    def cash_out_action(self):
        #Set all KSU entity balances to zero
        session.rollback()
        
        entities = session.query(Wallet).filter( Wallet.wallet_type == "KSU" ).all()
        
        if not entities:
            msg.showinfo("Info", "No KSU wallets found.")
            return

        for e in entities:
            e.balance = 0.0

        session.commit()
        session.expire_all()
        msg.showinfo("Success", "All KSU entity balances cleared.")
        self.refresh_entities()
        
    
    def show_view_tab(self):
        #Switch to View tab
        session.expire_all()
        self.refresh_entities()
        self.add_frame.pack_forget()
        self.manage_frame.pack_forget()
        self.view_frame.pack(fill="both", expand=True)
    
    
    def show_add_tab(self):
        #Switch to Add tab
        self.view_frame.pack_forget()
        self.manage_frame.pack_forget()
        self.add_frame.pack(fill="both", expand=True)
    
    
    def show_manage_tab(self):
        # Switch to Manage tab
        self.view_frame.pack_forget()
        self.add_frame.pack_forget()
        self.manage_frame.pack(fill="both", expand=True)
    
    
    def go_back(self):
        #Go back to SignUp window
        self.destroy()
        from SignUpWindow import SignUpWindow
        win = SignUpWindow(self.master)
        win.pack(fill="both", expand=True)
