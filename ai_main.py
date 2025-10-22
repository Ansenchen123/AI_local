import os
import time
import json
import threading
import queue
import google.generativeai as genai
from dotenv import load_dotenv

import tkinter as tk
from tkinter import scrolledtext,simpledialog,messagebox
from PIL import Image, ImageTk

def load_api_key():
    load_dotenv()
    api_key = os.getenv("GOOGLE_API_KEY")
    genai.configure(api_key=api_key)

def create_model(model_name = "gemini-2.5-flash", history = []):
    model = genai.GenerativeModel(model_name)
    chat = model.start_chat(history=history)
    return chat

def chat_with_model(chat, prompt):
    response = chat.send_message(prompt)
    return response.text, chat.history

def change_history_to_json(history):
    history_json = []
    for entry in history:
        history_json.append({
            "role": entry.role,
            "content": entry.parts[0].text
        })
    return history_json

def save_conversation(history, filename="conversation"):
    if not filename.endswith(".json"):
        filename += ".json"
    filename =  os.path.join("history",filename)
    history = change_history_to_json(history)
    with open(filename, 'w') as f:
        json.dump(history, f, indent=4)
    print(f"Conversation saved to {filename}")

def read_json_history(filename="conversation"):
    if not filename.endswith(".json"):
        filename += ".json"
    filename =  os.path.join("history",filename)
    try:
        with open(filename, 'r') as f:
            history_json = json.load(f)
    except FileNotFoundError:
        history_json = []
    return [
        {
            "role": entry["role"],
            "parts": [entry["content"]]
        }
        for entry in history_json
    ]

def set_history(chat,filename):
    if not filename.endswith('.json'):
            filename += '.json'
    history = read_json_history(filename)
    chat.history=history
    
def find_history():
    return os.listdir("history")

def delete_file(filename):
    if not filename.endswith('.json'):
            filename += '.json'
    path = os.path.join("history",filename)
    os.remove(path)

def tkinter_thread(chat):
    q = queue.Queue()
    filename = os.listdir('history')[0].split('.')[0]
    def run_chat_btn_t(event=None):
        prompt = text_area.get()
        if prompt:
            chat_btn.config(text='wait',state="disabled")
            msnscroll.insert(tk.END,f"user:{prompt}\n")
            threading.Thread(target=run_chat_btn,args=(prompt,)).start()

    def run_chat_btn(prompt):
        try:
            response = chat_with_model(chat, prompt) 
            q.put(response)
        except:
            q.put(None)
        
    def check_queue():
        try:
            response= q.get_nowait()
            if response is None:
                msnscroll.insert(tk.END, "AI Error\n")
            else:
                response_text = response[0]
                response_history = response[1]
                msnscroll.insert(tk.END,f"model:{response_text}\n")
                save_conversation(response_history,filename)
                text_area.delete(0, tk.END)
            chat_btn.config(text='send',state="normal")
        except queue.Empty:
            pass
        finally:
            root.after(100,check_queue)

    def history_text(history):
        msnscroll.delete('1.0',tk.END)
        for entry in history:
            role = entry.role
            text = entry.parts[0].text
            if role == 'model':
                msnscroll.insert(tk.END,f"model:{text}\n")
            elif role == 'user':
                msnscroll.insert(tk.END,f"user:{text}\n")
    
    def set_btn_list():
        model_choice.delete(0, tk.END)
        for text in find_history():
            btn = text.split('.')
            model_choice.insert(tk.END,btn[0])

    def on_history_choice(event):
        nonlocal filename
        widget = event.widget
        select = widget.curselection()
        if not select:
            return
        index = select[0]
        value = widget.get(index)
        save_conversation(chat.history,filename)
        filename = value
        msn.config(text=filename)
        set_history(chat,value)
        history_text(chat.history)


    def add_chat():
        filename_input = simpledialog.askstring(
            title='filecreat',
            prompt='new filename:'
        )
        if filename_input:
            nonlocal filename
            filename = filename_input
            msn.config(text=filename)
            chat.history = []
            history_text(chat.history)
            save_conversation(chat.history,filename)
            set_btn_list()

    def del_chat():
        filename_input = simpledialog.askstring(
            title='filedelete',
            prompt='del filename:'
        )
        if filename_input:
            nonlocal filename
            file_list = find_history()
            if not filename_input.endswith('.json'):
                filename_input += '.json'

            if not(filename_input in file_list):
                messagebox.showinfo(
                    title="Error", 
                    message="file no found "
                )
            elif len(file_list) <= 1:
                messagebox.showinfo(
                    title="Error", 
                    message="you must need 1 chat"
                )
            else:      
                delete_file(filename_input)
                if filename == filename_input:
                    filename = find_history()[0]
                    chat.history = read_json_history(filename)
                    msn.config(text=filename.split('.')[0])
                    history_text(chat.history)
                set_btn_list()

        
    root = tk.Tk()
    root.title("AI Chat Interface")
    root.geometry("600x400")

    label = tk.Label(root, text="Enter your message:",anchor="w")
    label.place(
        relx=0.35,
        rely=0.8,
        relwidth=0.65,
        relheight=0.1,
    )

    text_area = tk.Entry(root, width=70)
    text_area.bind("<Return>", run_chat_btn_t)
    text_area.place(
        relx=0.35,
        rely=0.9,
        relwidth=0.55,
        relheight=0.1,
    )

    chat_btn = tk.Button(root, text="send", command=run_chat_btn_t)
    chat_btn.place(
        relx=0.9,
        rely=0.9,
        relwidth=0.1,
        relheight=0.1,
    )

    msnscroll = scrolledtext.ScrolledText()
    msnscroll.place(
        relx=0.35,
        rely=0.1,
        relwidth=0.65,
        relheight=0.8,
    )

    model_choice = tk.Listbox(root)
    model_choice.place(
        relx=0.0,
        rely=0.2,
        relwidth=0.33,
        relheight=0.8,
    )

    add_chat_btn = tk.Button(root,text="add file",command=add_chat)
    add_chat_btn.place(
        relx=0.065,
        rely=0.025,
        relwidth=0.2,
        relheight=0.05,
    )

    del_chat_btn = tk.Button(root,text="delete file",command=del_chat)
    del_chat_btn.place(
        relx=0.065,
        rely=0.125,
        relwidth=0.2,
        relheight=0.05,
    )
    
    msn = tk.Label(root, text=filename, font=("Arial", 16))
    msn.place(
        relx=0.3,
        rely=0.0,
        relwidth=0.6,
        relheight=0.1,
    )

    root.after(100,check_queue)
    set_btn_list()
    set_history(chat,filename)
    history_text(chat.history)
    model_choice.bind('<<ListboxSelect>>', on_history_choice)
    return root



def main():
    load_api_key()
    chat = create_model()
    #response_text, history = chat_with_model(chat, "Hello, how can I assist you today?")
    #print("Model Response:", response_text)
    root = tkinter_thread(chat)
    root.mainloop()

if __name__ == "__main__":
    main()