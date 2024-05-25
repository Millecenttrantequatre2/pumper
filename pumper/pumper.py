import tkinter as tk
from tkinter import filedialog, messagebox
import hashlib

def getmd5(fileName):
    hash_md5 = hashlib.md5()
    with open(fileName, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def pump_file():
    filePath = file_path.get()
    pumpSize = size_entry.get()
    unitType = unit_var.get()

    if not filePath:
        messagebox.showerror("Error", "Please select a file")
        return

    if not pumpSize.isdigit():
        messagebox.showerror("Error", "Please enter a valid size")
        return

    pumpSize = int(pumpSize)
    oldMD5 = getmd5(filePath)
    pumpFile = open(filePath, 'ab')

    b_fSize = 0

    if unitType == "KB":
        b_fSize = pumpSize * 1024

    elif unitType == "MB":
        b_fSize = pumpSize * pow(1024, 2)

    elif unitType == "GB":
        b_fSize = pumpSize * pow(1024, 3)

    else:
        messagebox.showerror("Erreur", "Invalid!")
        return

    buffer = 256
    for i in range(int(b_fSize / buffer)):
        pumpFile.write(b"0" * buffer)

    newMD5 = getmd5(filePath)

    pumpFile.close()

    messagebox.showinfo("Success", f"pump fini!!\nOriginal MD5: {oldMD5}\nPumped MD5: {newMD5}")

def select_file():
    file = filedialog.askopenfilename()
    file_path.set(file)

root = tk.Tk()
root.title("1134 pumper")

window_width = 400
window_height = 300
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
position_top = int(screen_height / 2 - window_height / 2)
position_right = int(screen_width / 2 - window_width / 2)
root.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')

file_path = tk.StringVar()
tk.Label(root, text="Select File:").pack(pady=5)
file_frame = tk.Frame(root)
file_frame.pack(pady=5)
tk.Entry(file_frame, textvariable=file_path, width=40).pack(side=tk.LEFT, padx=5)
tk.Button(file_frame, text="Browse", command=select_file).pack(side=tk.LEFT)

tk.Label(root, text="Enter Size:").pack(pady=5)
size_entry = tk.Entry(root)
size_entry.pack(pady=5)

tk.Label(root, text="Select Unit:").pack(pady=5)
unit_frame = tk.Frame(root)
unit_frame.pack(pady=5)
unit_var = tk.StringVar(value="KB")
units = [("KB", "KB"), ("MB", "MB"), ("GB", "GB")]
for (text, value) in units:
    tk.Radiobutton(unit_frame, text=text, variable=unit_var, value=value, indicatoron=0, width=10, height=2).pack(side=tk.LEFT, padx=5)

tk.Button(root, text="EXECUTE", command=pump_file, bg="green", fg="white", width=15, height=2).pack(pady=20)

root.mainloop()