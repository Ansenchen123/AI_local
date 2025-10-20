import os
import time
import json
import threading
import queue
import google.generativeai as genai
from dotenv import load_dotenv

import tkinter as tk
from tkinter import scrolledtext
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

def save_conversation(history, filename="conversation.json"):
    history = change_history_to_json(history)
    with open(filename, 'w') as f:
        json.dump(history, f, indent=4)
    print(f"Conversation saved to {filename}")

def read_json_history(filename="conversation.json"):
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

def tkinter_thread(model):
    q = queue.Queue()

    def run_chat_btn_t():
        prompt = text_area.get()
        if prompt:
            chat_btn.config(text='wait',state="disabled")
            threading.Thread(target=run_chat_btn,args=(prompt,)).start()

    def run_chat_btn(prompt):
        try:
            response_text, history = chat_with_model(model, prompt)
            response = [response_text,history]
            q.put(response)
        except:
            q.put(None)
        
    def check_queue():
        try:
            response= q.get_nowait()
            if response is None:
                msn.config(text=f"AI Error")
            else:
                msn.config(text=f"AI Response: {response[0]}")
                text_area.delete(0,tk.END)
            chat_btn.config(text='send',state="normal")
        except queue.Empty:
            pass
        finally:
            root.after(100,check_queue)
    root = tk.Tk()
    root.title("AI Chat Interface")
    root.geometry("600x400")

    label = tk.Label(root, text="Enter your message:",anchor="w")
    label.place(
        relx=0.5,
        rely=0.8,
        relwidth=0.5,
        relheight=0.1,
    )

    text_area = tk.Entry(root, width=70)
    text_area.place(
        relx=0.5,
        rely=0.9,
        relwidth=0.4,
        relheight=0.1,
    )

    chat_btn = tk.Button(root, text="send", command=run_chat_btn_t)
    chat_btn.place(
        relx=0.9,
        rely=0.9,
        relwidth=0.1,
        relheight=0.1,
    )

    msn = tk.Label(root, text="AI Chat Interface", font=("Arial", 16))
    msn.pack()

    root.after(100,check_queue)

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