import tkinter as tk
import random
import string
import pygame

def generate_key():
    hex_val = entry.get().strip()
    if len(hex_val) != 5:
        lbl_res.config(text="Ошибка: нужно 5 символов")
        return
    try:
        dec_val = str(int(hex_val, 16))
    except ValueError:
        lbl_res.config(text="Ошибка: это не HEX")
        return

    d1, d2, d3 = dec_val[0], dec_val[1], dec_val[2]
    tail = dec_val[-2:]

    blocks = []
    for d in (d1, d2, d3):
        chars = [random.choice(string.ascii_uppercase + string.digits) for _ in range(4)]
        chars.insert(random.randint(0, 4), d)
        blocks.append("".join(chars))

    key = f"{blocks[0]}-{blocks[1]}-{blocks[2]} {tail}"
    lbl_res.config(text=key)

def animate():
    colors = ["lime", "yellow", "cyan", "magenta"]
    lbl_title.config(fg=random.choice(colors))
    root.after(500, animate)

root = tk.Tk()
root.geometry("600x400")

try:
    pygame.mixer.init()
    pygame.mixer.music.load("music.mp3")
    pygame.mixer.music.play(-1)
except:
    pass

try:
    bg = tk.PhotoImage(file="background.png")
    tk.Label(root, image=bg).place(x=0, y=0, relwidth=1, relheight=1)
except:
    pass

lbl_title = tk.Label(root, text="KEYGEN", font=("Arial", 20, "bold"))
lbl_title.pack(pady=20)
animate()

entry = tk.Entry(root, font=("Arial", 14))
entry.pack(pady=10)
tk.Button(root, text="Сгенерировать", command=generate_key).pack(pady=10)
lbl_res = tk.Label(root, text="", font=("Courier", 16, "bold"))
lbl_res.pack(pady=20)

root.mainloop()