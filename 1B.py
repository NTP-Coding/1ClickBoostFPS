import tkinter as tk
import winreg
import ctypes
import sys
import webbrowser
import os

MODES = {
    "ลดความล่าช้าขาเข้า + บูสต์อัตราเฟรม": 0x26,
    "สมูทอัตราเฟรม & เสถียร": 0x3A,
    "สมรรถนะปีศาจ": 0xfa332a,
    "ค่าดั้งเดิม": 0x2A
}

def apply_mode(hex_value):
    try:
        key_path = r"SYSTEM\\CurrentControlSet\\Control\\PriorityControl"
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path, 0, winreg.KEY_SET_VALUE) as key:
            winreg.SetValueEx(key, "Win32PrioritySeparation", 0, winreg.REG_DWORD, hex_value)
        show_success_popup()
    except PermissionError:
        show_error_popup("⛔ ต้องใช้สิทธิ์แอดมิน")
    except Exception as e:
        show_error_popup(f"⚠️ Error: {str(e)}")

def show_success_popup():
    popup = tk.Toplevel(root)
    popup.title("เสร็จสิ้น")
    popup.geometry("250x130")
    popup.resizable(False, False)
    popup.configure(bg="#1a1a1a")

    label = tk.Label(popup, text="✅ บูสFPS เสร็จสิ้น", font=("Segoe UI", 10, "bold"), fg="#00ff88", bg="#1a1a1a")
    label.pack(pady=(20, 5))

    restart_btn = tk.Button(popup, text="🔁 Restart เครื่อง", command=restart_computer)
    style_button(restart_btn, bg="#cc3333", hover_bg="#aa2222")
    restart_btn.pack(pady=10)

def show_error_popup(msg):
    popup = tk.Toplevel(root)
    popup.title("ข้อผิดพลาด")
    popup.geometry("260x110")
    popup.resizable(False, False)
    popup.configure(bg="#1a1a1a")

    label = tk.Label(popup, text=msg, font=("Segoe UI", 10), fg="red", bg="#1a1a1a", wraplength=240)
    label.pack(pady=20)

def restart_computer():
    os.system("shutdown /r /t 1")

def open_discord():
    webbrowser.open("https://discord.gg/7e45EpwXVz")

def style_button(btn, bg="#2c2c2c", fg="white", font=("Segoe UI", 10, "bold"), hover_bg="#444"):
    btn.config(
        bg=bg,
        fg=fg,
        activebackground=hover_bg,
        activeforeground="white",
        relief="flat",
        borderwidth=0,
        font=font,
        cursor="hand2"
    )
    def on_enter(e): btn['background'] = hover_bg
    def on_leave(e): btn['background'] = bg
    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)

def resource_path(relative_path):
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)    

if not ctypes.windll.shell32.IsUserAnAdmin():
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, ' '.join(sys.argv), None, 1)
    sys.exit()

root = tk.Tk()
root.title("บูสต์เฟรมเรต ปรับแต่ง")
root.geometry("300x360")
root.iconbitmap(resource_path("icons.ico"))
root.resizable(False, False)

canvas = tk.Canvas(root, width=300, height=360, bg="#1a1a1a", highlightthickness=0)
canvas.pack(fill="both", expand=True)

canvas.create_text(150, 30, text="เลือกโหมดเพื่อบูสต์เฟรมเรต", font=("Segoe UI", 12, "bold"), fill="#ff0000")

y = 70
for mode, hex_val in MODES.items():
    btn = tk.Button(root, text=mode, width=28, command=lambda val=hex_val: apply_mode(val))
    style_button(btn)
    canvas.create_window(150, y, window=btn)
    y += 42

discord_btn = tk.Button(root, text="เข้าร่วม Discord", command=open_discord)
style_button(discord_btn, bg="#5865F2", hover_bg="#4752C4")
canvas.create_window(150, y, window=discord_btn)
y += 25

canvas.create_text(150, y+10, text="Ver 1.0.1", font=("Segoe UI", 8), fill="#666")
canvas.create_text(150, y+25, text="แจกฟรีห้ามจำหน่าย", font=("Segoe UI", 8), fill="#666")
canvas.create_text(150, y+40, text="Build By Nattaphat", font=("Segoe UI", 8), fill="#666")

root.mainloop()
