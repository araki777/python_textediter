import tkinter as tk
from tkinter import filedialog, messagebox

current_file = None

# ファイルの作成
def new_file():
    global current_file
    text_widget.delete("1.0", tk.END)
    current_file = None

# ファイルを開く
def open_file():
    global current_file
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if file_path:
        with open(file_path, "r") as file:
            text_widget.delete("1.0", tk.END)
            text_widget.insert(tk.END, file.read())
            current_file = file_path
            update_status_bar()

# ファイルの保存
def save_file():
    global current_file
    if current_file:
        with open(current_file, "w") as file:
            file.write(text_widget.get("1.0", tk.END))
    else:
        save_file_as()


# ファイルに名前を付けて保存
def save_file_as():
    global current_file
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
    if file_path:
        with open(file_path, "w") as file:
            file.write(text_widget.get("1.0", tk.END))
            current_file = file_path
            update_status_bar()

# エディタを閉じる
def exit_editor():
    if messagebox.askokcancel("Exit", "本当に閉じますか？"):
        window.destroy()

# 切り取りコマンド
def cut_text():
    selected_text = text_widget.get(tk.SEL_FIRST, tk.SEL_LAST)
    text_widget.delete(tk.SEL_FIRST, tk.SEL_LAST)
    window.clipboard_clear()
    window.clipboard_append(selected_text)

# コピーコマンド
def copy_text():
    selected_text = text_widget.get(tk.SEL_FIRST, tk.SEL_LAST)
    window.clipboard_clear()
    window.clipboard_append(selected_text)

# 貼り付けコマンド
def paste_text():
    text_to_paste = window.clipboard_get()
    text_widget.insert(tk.INSERT, text_to_paste)

def update_status_bar(event=None):
    line, column = map(int, text_widget.index(tk.INSERT).split('.'))
    char_count = len(text_widget.get("1.0", tk.END)) - 1
    status_bar.config(text=f"{line}行, {column}列, {char_count}文字")

# メインウインドウを作成
window = tk.Tk()

# ウインドウのタイトルを設定
window.title("エディタ")

# メニューを作成
menu_bar = tk.Menu(window)
file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label="New", command=new_file)
file_menu.add_command(label="Open", command=open_file)
file_menu.add_command(label="Save", command=save_file)
file_menu.add_command(label="Save As", command=save_file_as)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=exit_editor)
menu_bar.add_cascade(label="File", menu=file_menu)
edit_menu = tk.Menu(menu_bar, tearoff=0)
edit_menu.add_command(label="Cut", command=cut_text, accelerator="Ctrl+X")
edit_menu.add_command(label="Copy", command=copy_text, accelerator="Ctrl+C")
edit_menu.add_command(label="Paste", command=paste_text, accelerator="Ctrl+V")
menu_bar.add_cascade(label="Edit", menu=edit_menu)

window.config(menu=menu_bar)

text_widget = tk.Text(window, font=("Arial", 12), bg="white", fg="black", wrap=tk.WORD)
text_widget.pack(fill=tk.BOTH, expand=True)
text_widget.bind("<Control-t>", update_status_bar)

status_bar = tk.Label(window, text="", bd=1, relief=tk.SUNKEN, anchor=tk.W)
status_bar.pack(side=tk.BOTTOM, fill=tk.X)

window.bind("<Control-x>", cut_text)
window.bind("<Control-c>", copy_text)
window.bind("<Control-v>", paste_text)

update_status_bar()

text_widget.config(height=10, width=40)

# イベントループを開始
window.mainloop()