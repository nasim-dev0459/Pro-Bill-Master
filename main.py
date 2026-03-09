import sqlite3
from tkinter import *
from tkinter import messagebox, ttk
from datetime import datetime

# --- Database setup ---
def init_db():
    conn = sqlite3.connect("shop_data.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sales (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            items TEXT,
            total REAL
        )
    """)
    conn.commit()
    conn.close()

init_db()

class BillMaster:
    def __init__(self, root):
        self.root = root
        self.root.title("Pro Bill Master - Login")
        self.root.geometry("400x550")
        self.root.config(bg="#1a1a2e")
        self.root.resizable(False, False)

        self.username = StringVar()
        self.password = StringVar()

        # UI
        Label(root, text="🚀", font=("Arial", 60), bg="#1a1a2e", fg="#e94560").pack(pady=30)
        Label(root, text="ADMIN LOGIN", font=("Segoe UI", 24, "bold"), bg="#1a1a2e", fg="white").pack()

        f = Frame(root, bg="#1a1a2e")
        f.pack(pady=30)

        Label(f, text="Username", font=("Arial", 10), bg="#1a1a2e", fg="#a2a2a2").grid(row=0, column=0, sticky="w")
        Entry(f, textvariable=self.username, font=("Arial", 12), width=28, bd=0, highlightthickness=1).grid(row=1, column=0, pady=(5, 15))

        Label(f, text="Password", font=("Arial", 10), bg="#1a1a2e", fg="#a2a2a2").grid(row=2, column=0, sticky="w")
        Entry(f, textvariable=self.password, show="*", font=("Arial", 12), width=28, bd=0, highlightthickness=1).grid(row=3, column=0, pady=5)

        btn = Button(root, text="LOG IN", command=self.login, bg="#e94560", fg="white", 
                     font=("Arial", 12, "bold"), width=22, bd=0, cursor="hand2", activebackground="#cf304a")
        btn.pack(pady=20)

    def login(self):
        if self.username.get().strip() == "admin" and self.password.get().strip() == "1234":
            self.new_win = Toplevel(self.root)
            self.app = Dashboard(self.new_win)
            self.root.withdraw()
        else:
            messagebox.showerror("Error", "Invalid credentials!")

class Dashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Bill Master Dashboard")
        self.root.geometry("1100x700")
        self.root.config(bg="#f0f2f5")

        # Variables
        self.menu = {"Samosa": 25, "Roll": 40, "Pakora": 15, "Coffee": 100, "Milkshake": 120, "Meatbox": 150}
        self.vars = {item: IntVar(value=0) for item in self.menu}
        self.total_var = StringVar(value="0.00")

        self.setup_ui()

    def setup_ui(self):
        # Header
        header = Frame(self.root, bg="#1a1a2e", height=80)
        header.pack(side=TOP, fill=X)
        Label(header, text="💎 PRO BILLING MASTER", font=("Segoe UI", 26, "bold"), bg="#1a1a2e", fg="white").pack(pady=15)

        # Main Body
        container = Frame(self.root, bg="#f0f2f5")
        container.pack(fill=BOTH, expand=True, padx=30, pady=30)

        # --- LEFT: MENU CARD ---
        left_f = LabelFrame(container, text=" SELECT ITEMS ", font=("Arial", 12, "bold"), bg="white", padx=20, pady=20)
        left_f.pack(side=LEFT, fill=Y, padx=10)

        for item, price in self.menu.items():
            row = Frame(left_f, bg="white")
            row.pack(fill=X, pady=10)
            
            Label(row, text=f"{item}", font=("Arial", 11), bg="white", width=12, anchor="w").pack(side=LEFT)
            Label(row, text=f"Tk.{price}", font=("Arial", 9), fg="#666", bg="white", width=8).pack(side=LEFT)
            
            Button(row, text="-", width=3, bg="#f0f2f5", command=lambda x=item: self.update_qty(x, -1)).pack(side=LEFT, padx=2)
            Entry(row, textvariable=self.vars[item], width=5, justify="center", font=("Arial", 10, "bold")).pack(side=LEFT, padx=2)
            Button(row, text="+", width=3, bg="#f0f2f5", command=lambda x=item: self.update_qty(x, 1)).pack(side=LEFT, padx=2)

        # --- RIGHT: BILLING ---
        right_f = Frame(container, bg="#f0f2f5")
        right_f.pack(side=LEFT, fill=BOTH, expand=True, padx=10)

        # Bill Summary Box
        summary_f = LabelFrame(right_f, text=" BILL SUMMARY ", font=("Arial", 12, "bold"), bg="white", padx=20, pady=20)
        summary_f.pack(fill=X)

        Label(summary_f, text="TOTAL AMOUNT", font=("Arial", 14), bg="white", fg="#1a1a2e").pack()
        Label(summary_f, textvariable=self.total_var, font=("Segoe UI", 50, "bold"), bg="white", fg="#27ae60").pack(pady=10)
        Label(summary_f, text="Taka", font=("Arial", 12), bg="white", fg="#666").pack()

        # Action Buttons
        btn_f = Frame(right_f, bg="#f0f2f5")
        btn_f.pack(pady=30)

        btn_style = {"font": ("Arial", 12, "bold"), "width": 25, "height": 2, "fg": "white", "bd": 0, "cursor": "hand2"}
        
        Button(btn_f, text="✅ SAVE & PRINT BILL", bg="#27ae60", command=self.save_bill, **btn_style).pack(pady=10)
        Button(btn_f, text="📜 VIEW SALES HISTORY", bg="#1a1a2e", command=self.show_history, **btn_style).pack(pady=5)
        Button(btn_f, text="🔄 RESET ALL", bg="#e94560", command=self.reset, **btn_style).pack(pady=5)
        Button(btn_f, text="🚪 LOGOUT", bg="#95a5a6", command=self.logout, **btn_style).pack(pady=20)

    def update_qty(self, item, val):
        current = self.vars[item].get()
        self.vars[item].set(max(0, current + val))
        total = sum(self.menu[i] * self.vars[i].get() for i in self.menu)
        self.total_var.set(f"{total:.2f}")

    def save_bill(self):
        total = float(self.total_var.get())
        if total <= 0:
            messagebox.showwarning("Empty Bill", "Please select some items first!")
            return
        
        items_sold = [f"{i} (x{self.vars[i].get()})" for i in self.menu if self.vars[i].get() > 0]
        
        conn = sqlite3.connect("shop_data.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO sales (date, items, total) VALUES (?, ?, ?)",
                       (datetime.now().strftime("%Y-%m-%d %H:%M"), ", ".join(items_sold), total))
        conn.commit()
        conn.close()
        
        messagebox.showinfo("Success", f"Bill of Tk.{total} saved successfully!")
        self.reset()

    def show_history(self):
        h_win = Toplevel(self.root)
        h_win.title("Sales History")
        h_win.geometry("800x500")
        
        tree = ttk.Treeview(h_win, columns=("ID", "Date", "Items", "Total"), show='headings')
        for col in ("ID", "Date", "Items", "Total"):
            tree.heading(col, text=col)
            tree.column(col, anchor=CENTER)
        tree.column("Items", width=400)
        tree.pack(fill=BOTH, expand=True)

        conn = sqlite3.connect("shop_data.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM sales ORDER BY id DESC")
        for row in cursor.fetchall():
            tree.insert("", END, values=row)
        conn.close()

    def reset(self):
        for i in self.menu: self.vars[i].set(0)
        self.total_var.set("0.00")

    def logout(self):
        self.root.master.deiconify()
        self.root.destroy()

if __name__ == "__main__":
    root = Tk()
    BillMaster(root)
    root.mainloop()