import tkinter as tk
import socket
import serial
import threading

client_socket = None
arduino_port = None


def accept_connections():
    while True:
        try:
            client, addr = server_socket.accept()
            clients.append((client, addr))
            client_thread = threading.Thread(target=handle_client, args=(client, addr))
            client_thread.start()
            update_chat(f"{addr} se ha conectado.")
        except OSError:
            break

def handle_client(client, addr):
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message:
                if message == "/exit":
                    remove_client(client, addr)
                else:
                    update_chat(f"Cliente {addr}: {message}")
                    broadcast_message(f"Cliente {addr}: {message}", client)
        except OSError:
            break

def update_chat(message):
    chat_box.config(state=tk.NORMAL)
    chat_box.insert(tk.END, f"{message}\n")
    chat_box.config(state=tk.DISABLED)
    chat_box.see(tk.END)

def broadcast_message(message, sender_client):
    for client, addr in clients:
        if client != sender_client:
            try:
                client.send(bytes(message, 'utf-8'))
            except OSError:
                remove_client(client, addr)

def remove_client(client, addr):
    for c, a in clients:
        if c == client:
            clients.remove((c, a))
            c.close()
            update_chat(f"{a} se ha desconectado.")
            break

def send_server_message(event=None):
    message = server_message.get()
    server_message.set("")
    update_chat(f"Servidor: {message}")
    broadcast_message(f"Servidor: {message}", None)

def start_server():
    global server_socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('192.168.69.54', 5555))  # Replace with your server's IP and port
    server_socket.listen(5)
    server_status.set("Servidor iniciado")
    start_button.config(state=tk.DISABLED)
    stop_button.config(state=tk.NORMAL)
    accept_thread = threading.Thread(target=accept_connections)
    accept_thread.start()

def stop_server():
    global server_socket
    server_socket.close()
    server_status.set("Servidor apagado")
    start_button.config(state=tk.NORMAL)
    stop_button.config(state=tk.DISABLED)



# Funciones de control del Arduino
def connect_to_arduino():
    global arduino_port
    
    try:
        arduino_port = serial.Serial('COM3', 9600)  # Reemplaza 'COMX' con tu puerto COM asignado
        update_interface("Conectado al Arduino")
    except serial.SerialException:
        update_interface("Error al conectar con Arduino")

def disconnect_from_arduino():
    global arduino_port
    
    if arduino_port:
        arduino_port.close()
        update_interface("Desconectado del Arduino")
    else:
        update_interface("No hay conexión activa con Arduino")

def toggle_fan_motor():
    if arduino_port:
        arduino_port.write(b'FAN_TOGGLE\n')  # Envia el comando al Arduino
        update_interface("Motor del Ventilador Toggled")
    else:
        update_interface("No hay conexión con Arduino para controlar el motor")

# Función para ajustar la velocidad del motor del ventilador
def set_fan_speed():
    speed = fan_speed_slider.get()
    if arduino_port:
        arduino_port.write(f'FAN_SPEED {speed}\n'.encode())  # Envia el comando al Arduino
        update_interface(f"Velocidad del Motor del Ventilador ajustada a {speed}")
    else:
        update_interface("No hay conexión con Arduino para controlar la velocidad del motor del ventilador")

# Funciones de control adicional

def toggle_water_pump():
    if arduino_port:
        arduino_port.write(b'WATER_TOGGLE\n')  # Envia el comando al Arduino
        update_interface("Bomba de Agua Toggled")
    else:
        update_interface("No hay conexión con Arduino para controlar la bomba de agua")

def set_led_intensity():
    intensity = led_intensity_slider.get()
    if arduino_port:
        arduino_port.write(f'LED {intensity}\n'.encode())  # Envia el comando al Arduino
        update_interface(f"Luces LED ajustadas a intensidad {intensity}")
    else:
        update_interface("No hay conexión con Arduino para controlar las luces LED")
        
# Función para actualizar la interfaz con el mensaje recibido
def update_interface(message):
    messages_text.config(state=tk.NORMAL)
    messages_text.insert(tk.END, message + '\n')
    messages_text.see(tk.END)
    messages_text.config(state=tk.DISABLED)

# Crear la interfaz gráfica
root = tk.Tk()
root.title("servidor")

#controles servidor 
frame = tk.Frame(root)
frame.pack()

scrollbar = tk.Scrollbar(frame)
chat_box = tk.Text(frame, height=15, width=50, yscrollcommand=scrollbar.set)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
chat_box.pack(side=tk.LEFT, fill=tk.BOTH)
chat_box.config(state=tk.DISABLED)

server_status = tk.StringVar()
server_status.set("Servidor apagado")
status_label = tk.Label(root, textvariable=server_status)
status_label.pack()

start_button = tk.Button(root, text="Iniciar Servidor", command=start_server)
start_button.pack()

stop_button = tk.Button(root, text="Detener Servidor", command=stop_server, state=tk.DISABLED)
stop_button.pack()

server_message = tk.StringVar()
message_entry = tk.Entry(root, textvariable=server_message)
message_entry.bind("<Return>", send_server_message)
message_entry.pack()
message_entry.focus()

send_button = tk.Button(root, text="Enviar a Clientes", command=send_server_message)
send_button.pack()

clients = []

# Controles para el Arduino
arduino_connect_button = tk.Button(root, text="Conectar Arduino", command=connect_to_arduino)
arduino_connect_button.pack()

arduino_disconnect_button = tk.Button(root, text="Desconectar Arduino", command=disconnect_from_arduino)
arduino_disconnect_button.pack()

fan_motor_button = tk.Button(root, text="Encender/Apagar Motor del Ventilador", command=toggle_fan_motor)
fan_motor_button.pack()

# Controles adicionales
fan_frame = tk.Frame(root)
fan_frame.pack(padx=20, pady=10)
tk.Label(fan_frame, text="Control de Ventilador").pack()
fan_speed_slider = tk.Scale(fan_frame, from_=0, to=255, orient=tk.HORIZONTAL, length=200)
fan_speed_slider.set(50)
fan_speed_slider.pack()
tk.Button(fan_frame, text="Aplicar", command=set_fan_speed).pack()

water_frame = tk.Frame(root)
water_frame.pack(padx=20, pady=10)
tk.Label(water_frame, text="Control de Motor de Agua").pack()
tk.Button(water_frame, text="Encender/Apagar", command=toggle_water_pump).pack()

led_frame = tk.Frame(root)
led_frame.pack(padx=20, pady=10)
tk.Label(led_frame, text="Control de Luces LED").pack()
led_intensity_slider = tk.Scale(led_frame, from_=0, to=100, orient=tk.HORIZONTAL, length=200)
led_intensity_slider.set(50)
led_intensity_slider.pack()
tk.Button(led_frame, text="Aplicar", command=set_led_intensity).pack()

# Ventana de mensajes
messages_frame = tk.Frame(root)
messages_frame.pack(padx=20, pady=10)
messages_label = tk.Label(messages_frame, text="Mensajes")
messages_label.pack()
messages_text = tk.Text(messages_frame, height=10, width=50, state=tk.DISABLED)
messages_text.pack()

root.mainloop()