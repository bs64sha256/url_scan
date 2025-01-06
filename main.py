import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import whois
import requests
import socket

def get_whois_info(url):
    try:
        domain = url.replace("http://", "").replace("https://", "").replace("www.", "")
        if "/" in domain:
            domain = domain.split("/")[0]

        w = whois.whois(domain)
        ip = socket.gethostbyname(domain)

        return {
            "domain": 'Домен: '+domain,
            "registrar": w.registrar or "N/A",
            "ip": "IP сервера: "+ip,
            "creation_date": w.creation_date or "N/A",
        }

    except whois.parser.PywhoisError as e:
        return {"error": f"Ошибка Whois: {e}"}
    except requests.exceptions.RequestException as e:
        return {"error": f"Ошибка сети: {e}"}
    except socket.gaierror:
        return {"error": "Не удалось разрешить имя хоста."}
    except Exception as e:
        return {"error": f"Неизвестная ошибка: {e}"}


def process_url():
    url = url_entry.get()
    if not url:
        messagebox.showerror("Ошибка", "Пожалуйста, введите URL-адрес.")
        return

    result = get_whois_info(url)
    if "error" in result:
        clear_results()  # Очистка результатов при ошибке
    else:
        domain_label.config(text=result['domain'])
        registrar_label.config(text="Регистратор: "+result['registrar'])
        ip_label.config(text=result['ip'])
        creation_date_label.config(text='Дата регистрации: '+str(result['creation_date']))


def clear_results():
    domain_label.config(text="N/A")
    registrar_label.config(text="N/A")
    ip_label.config(text="N/A")
    creation_date_label.config(text="N/A")

root = tk.Tk()
root.title("Whois Информация")
root.geometry('500x195+0+0')

url_label = ttk.Label(root, text="Введите URL-адрес:")
url_label.place(x=10, y=10)

url_entry = ttk.Entry(root, width=49)
url_entry.place(x=140, y=10)

process_button = ttk.Button(root, text="Получить информацию", command=process_url, cursor='hand2', width=67)
process_button.place(x=10, y=40)

domain_label = ttk.Label(root, text="Домен: ")
domain_label.place(x=10, y =70)

registrar_label = ttk.Label(root, text="Регистратор: ")
registrar_label.place(x=10, y=100)

ip_label = ttk.Label(root, text="IP сервера: ")
ip_label.place(x=10, y=130)

creation_date_label = ttk.Label(root, text="Дата регистрации: ")
creation_date_label.place(x=10, y=160)

root.mainloop()
