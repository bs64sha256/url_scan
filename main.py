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
            "ip": "IP адрес: "+ip,
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
        creation_date_label.config(text='Дата регистрации: '+str(result['creation_date'][0]))


def clear_results():
    domain_label.config(text="N/A")
    registrar_label.config(text="N/A")
    ip_label.config(text="N/A")
    creation_date_label.config(text="N/A")

root = tk.Tk()
root.title("Whois Информация")
root.geometry('6000x600+0+0')

url_label = ttk.Label(root, text="Введите URL-адрес:")
url_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)

url_entry = ttk.Entry(root, width=40)
url_entry.grid(row=0, column=1, padx=5, pady=5)

process_button = ttk.Button(root, text="Получить информацию", command=process_url)
process_button.grid(row=1, column=0, columnspan=2, pady=10)

domain_label = ttk.Label(root, text="Домен: ")
domain_label.grid(row=2, column=0, columnspan=2, pady=5, sticky=tk.W)

registrar_label = ttk.Label(root, text="Регистратор: ")
registrar_label.grid(row=3, column=0, columnspan=2, pady=5, sticky=tk.W)

ip_label = ttk.Label(root, text="IP сервера: ")
ip_label.grid(row=4, column=0, columnspan=2, pady=5, sticky=tk.W)

creation_date_label = ttk.Label(root, text="Дата регистрации: ")
creation_date_label.grid(row=5, column=0, columnspan=2, pady=5, sticky=tk.W)

root.mainloop()
