import tkinter as tk
import random

SIZE = 500
history = []

import redis
import json

REDIS_HOST = 'de.futoke.ru'
REDIS_PORT = 6379
PIPE_NAME = 'itmo'


def init_chat():
    conn = redis.StrictRedis(host=REDIS_HOST,
                      port=REDIS_PORT,
                      db=0,
                      username='default',
                      password='dark_chat',
                      decode_responses=True)
    reader = conn.pubsub()
    reader.subscribe(PIPE_NAME)
    return conn, reader

def send_message(msg):
    conn.publish(PIPE_NAME, json.dumps(msg))
    print(msg)

def read_msgs(callback, frame_msgs):
    print('In read')
    for msg in reader.listen():
        if type(msg['data']) is int:
            continue
        print(msg)
        msg = json.loads(msg['data'])
        callback(frame_msgs, msg)
        # callback(frame_msgs,
        #          f'{msg["nickname"]}:\n{msg["text"]}')

conn, reader = init_chat()

def render_frames(parent):
    header = tk.Frame(parent, bg="blue")
    footer = tk.Frame(parent, bg="purple")
    body = tk.Frame(parent)

    header.pack(side=tk.TOP, fill=tk.X)
    footer.pack(side=tk.BOTTOM, fill=tk.X)
    body.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
    entry_name = render_header(header)
    render_footer(footer, body, entry_name)

def render_header(parent):
    lbl_name = tk.Label(parent, text="Name: ", font=("",14))
    lbl_name.pack(side=tk.LEFT)
    entry_name = tk.Entry(parent)
    entry_name.pack(side=tk.LEFT)
    name_default = f"Kotik -{random.randint(1,1000)}"
    entry_name.insert(0, name_default)
    return entry_name

def send_msg(body, entry_msg, entry_name):
    msg_text = entry_msg.get()
    name = entry_name.get()
    msg = f"{name}:\n{msg_text}"
    entry_msg.delete(0, tk.END)
    # send via network
    render_msg(body, msg)

def render_msg(body, msg):
    lbl_msg = tk.Label(body, text=msg, bg="Gray",
                       padx=2, pady=2,
                       font=("",14),
                       wraplength=400,
                       justify=tk.LEFT)
    lbl_msg.pack(side=tk.TOP, ANCHOR=tk.NE, pady=2)
    history.append(lbl_msg)

    height = 0
    for msg in history:
        msg_height = msg.winfo_reqheight()
        height += (msg_height + 2*2)

    if height >body.winfo_height():
        old_msg = history.pop(0)
        height -= old_msg.winfo_reqheight() - 2
        old_msg.destroy()
        root.update_idletasks()

def render_footer(parent, body):
    entry_msg = tk.Entry(parent)
    entry_msg.pack(side=tk.LEFT, fill=tk.X, expand=True)
    btn_send = tk.Button(parent, text = "Send",
                         command=lambda: send_msg(body, entry_msg, entry_name))
    btn_send.pack(side=tk.RIGHT)

if __name__ == '__main__':
    root = tk.Tk()
    root.geometry(f"{SIZE}x{SIZE}")
    root.title("Viber")
    render_frames(root)
    root.mainloop()