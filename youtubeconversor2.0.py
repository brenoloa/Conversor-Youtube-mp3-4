import tkinter as tk
from tkinter import messagebox, filedialog, ttk
from pytube import YouTube
import threading

def choose_directory():
    directory = filedialog.askdirectory()
    if directory:
        directory_entry.delete(0, tk.END)
        directory_entry.insert(0, directory)

def start_download_audio():
    thread = threading.Thread(target=download_audio)
    thread.start()

def start_download_video():
    thread = threading.Thread(target=download_video)
    thread.start()

def download_audio():
    url = url_entry.get()
    download_directory = directory_entry.get()

    if not url:
        messagebox.showwarning("URL necessária", "Por favor, insira a URL do vídeo do YouTube.")
        return
    if not download_directory:
        messagebox.showwarning("Diretório necessário", "Por favor, escolha um diretório para salvar o arquivo.")
        return

    try:
        yt = YouTube(url, on_progress_callback=progress_function)
        stream = yt.streams.filter(only_audio=True).first()
        if stream:
            progress_bar['value'] = 0
            status_label.config(text="Baixando áudio...")
            root.update_idletasks()
            stream.download(output_path=download_directory)
            status_label.config(text="Download Completo")
            messagebox.showinfo("Download Completo", f"Áudio baixado com sucesso em: {download_directory}")
        else:
            messagebox.showwarning("Erro", "Não foi possível encontrar um stream de áudio.")
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao baixar o áudio: {e}")

def download_video():
    url = url_entry.get()
    download_directory = directory_entry.get()

    if not url:
        messagebox.showwarning("URL necessária", "Por favor, insira a URL do vídeo do YouTube.")
        return
    if not download_directory:
        messagebox.showwarning("Diretório necessário", "Por favor, escolha um diretório para salvar o arquivo.")
        return

    try:
        yt = YouTube(url, on_progress_callback=progress_function)
        stream = yt.streams.filter(file_extension='mp4', progressive=True).first()
        if stream:
            progress_bar['value'] = 0
            status_label.config(text="Baixando vídeo...")
            root.update_idletasks()
            stream.download(output_path=download_directory)
            status_label.config(text="Download Completo")
            messagebox.showinfo("Download Completo", f"Vídeo baixado com sucesso em: {download_directory}")
        else:
            messagebox.showwarning("Erro", "Não foi possível encontrar um stream de vídeo.")
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao baixar o vídeo: {e}")

def progress_function(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    percentage_of_completion = (bytes_downloaded / total_size) * 100
    progress_bar['value'] = percentage_of_completion
    progress_label.config(text=f"{percentage_of_completion:.2f}%")
    root.update_idletasks()

# Criação da interface gráfica
root = tk.Tk()
root.title("brenoloa | YouTube Download")

# Estilo da barra de progresso
style = ttk.Style()
style.theme_use('clam')
style.configure("TProgressbar", thickness=30, troughcolor='#d9d9d9', background='#4caf50', troughrelief='flat')

# Criação dos componentes da interface
url_label = tk.Label(root, text="URL do vídeo do YouTube:")
url_label.pack(pady=5)

url_entry = tk.Entry(root, width=50)
url_entry.pack(pady=5)

directory_label = tk.Label(root, text="Pasta para salvar o arquivo:")
directory_label.pack(pady=5)

directory_frame = tk.Frame(root)
directory_frame.pack(pady=5)

directory_entry = tk.Entry(directory_frame, width=40)
directory_entry.pack(side=tk.LEFT, padx=5)

choose_button = tk.Button(directory_frame, text="Escolher", command=choose_directory)
choose_button.pack(side=tk.LEFT)

button_frame = tk.Frame(root)
button_frame.pack(pady=20)

download_audio_button = tk.Button(button_frame, text="Baixar Áudio", command=start_download_audio)
download_audio_button.pack(side=tk.LEFT, padx=10)

download_video_button = tk.Button(button_frame, text="Baixar Vídeo", command=start_download_video)
download_video_button.pack(side=tk.LEFT, padx=10)

progress_bar = ttk.Progressbar(root, orient="horizontal", length=400, mode="determinate", style="TProgressbar")
progress_bar.pack(pady=10)

progress_label = tk.Label(root, text="0%")
progress_label.pack(pady=5)

status_label = tk.Label(root, text="")
status_label.pack(pady=5)

# Execução do aplicativo
root.mainloop()
