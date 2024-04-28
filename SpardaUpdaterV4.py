import tkinter as tk
from tkinter import filedialog, ttk, simpledialog, messagebox
import shutil
import os
import re
import threading
import sys

class MoveFilesApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sparda Updater")

        # Obtener la ubicación del script actual
        if getattr(sys, 'frozen', False):
            self.script_dir = os.path.dirname(sys.executable)
        else:
            self.script_dir = os.path.dirname(__file__)

        self.device_label = tk.Label(root, text="Seleccionar dispositivo:")
        self.device_label.pack(pady=5)

        device_frame = tk.Frame(root)
        device_frame.pack(pady=5)

        self.device_var = tk.StringVar(root)
        self.devices_dropdown = tk.OptionMenu(device_frame, self.device_var, *self.get_connected_devices())
        self.devices_dropdown.pack(side="left")

        self.refresh_button = tk.Button(device_frame, text="Refrescar Dispositivos", command=self.refresh_devices)
        self.refresh_button.pack(side="left")

        entry_frame = tk.Frame(root)
        entry_frame.pack(pady=5)

        self.config_label = tk.Label(entry_frame, text="Archivo de configuración:")
        self.config_label.pack(side="top")

        self.config_var = tk.StringVar(root)
        self.config_entry = tk.Entry(entry_frame, textvariable=self.config_var, state='normal', width=47)
        self.config_entry.pack(side="left")

        self.config_button = tk.Button(entry_frame, text="...", command=self.select_config_file)
        self.config_button.pack(side="left")

        self.move_button = tk.Button(root, text="Iniciar", command=self.execute_commands)
        self.move_button.pack(pady=10)

        self.progressbar = ttk.Progressbar(root, mode="determinate", length=300)
        self.progressbar.pack(pady=10)

        self.success_messages = []  # Lista para almacenar los mensajes de éxito

    def get_connected_devices(self):
        # Devuelve una lista de letras de unidades (C:, D:, etc.) disponibles
        return [f"{c}:" for c in "CDEFGHIJKLMNOPQRSTUVWXYZ" if os.path.exists(f"{c}:")]

    def refresh_devices(self):
        # Actualiza el menú desplegable de dispositivos con las unidades disponibles
        self.devices_dropdown['menu'].delete(0, 'end')
        devices = self.get_connected_devices()
        if not devices:
            self.show_error("No se encontraron dispositivos conectados.")
            return

        for device in devices:
            self.devices_dropdown['menu'].add_command(label=device, command=tk._setit(self.device_var, device))

    def get_full_path(self, device, path):
        # Combina el dispositivo y la ruta para obtener la ruta completa
        return os.path.join(device, path)

    def select_config_file(self):
        # Abre un cuadro de diálogo para seleccionar el archivo de configuración
        file_path = filedialog.askopenfilename(title="Seleccionar archivo de configuración", filetypes=[("Archivos de texto", "*.txt")], initialdir=self.script_dir)
        if file_path:
            self.config_var.set(file_path)

    def execute_commands(self):
        # Ejecuta los comandos especificados en el archivo de configuración
        if not self.config_var.get():
            self.show_error("Por favor, selecciona un archivo de configuración primero.")
            return

        selected_device = self.device_var.get()
        if not selected_device:
            self.show_error("Por favor, selecciona un dispositivo.")
            return

        if not os.path.exists(selected_device):
            self.show_error(f"No se encuentra el dispositivo {selected_device}.")
            return

        config_file_path = self.config_var.get()

        # Crear un hilo para ejecutar las operaciones de archivos en segundo plano
        thread = threading.Thread(target=self.execute_commands_in_thread, args=(config_file_path, selected_device))
        thread.start()

    def execute_commands_in_thread(self, config_file_path, selected_device):
        # Ejecuta los comandos de manera asíncrona en un hilo separado
        try:
            with open(config_file_path, 'r') as file:
                total_lines = sum(1 for _ in file)
                file.seek(0)  # Reiniciar el cursor del archivo

                for line_number, line in enumerate(file, start=1):
                    # Divide la línea del archivo de configuración en partes
                    parts = re.split(r'"', line.strip())
                    parts = [part.strip() for part in parts if part.strip()]  # Eliminar elementos vacíos

                    if len(parts) < 2:
                        self.show_error(f"Error en el formato de la línea {line_number} del archivo de configuración.")
                        return

                    command, argument = parts[0].lower(), parts[1]

                    if command == 'mover':
                        if len(parts) == 3:
                            destination = parts[2].strip()
                        else:
                            self.show_error(f"Error en el formato de la línea {line_number} del archivo de configuración.")
                            return
                        self.move_files(selected_device, argument, destination)
                    elif command == 'eliminar':
                        self.delete_item(selected_device, argument)
                    elif command == 'copiar':
                        if len(parts) == 3:
                            destination = parts[2].strip()
                        else:
                            destination = argument
                        self.copy_files(selected_device, argument, destination)
                    else:
                        self.show_error(f"Comando no reconocido en la línea {line_number} del archivo de configuración.")

                    # Actualizar la barra de progreso
                    progress_value = int((line_number / total_lines) * 100)
                    self.progressbar['value'] = progress_value
                    self.root.update_idletasks()

                # Reiniciar la barra de progreso después de completar las operaciones
                self.progressbar['value'] = 0
                # Mostrar el mensaje de éxito acumulado
                self.show_success_dialog()
        except Exception as e:
            self.show_error(f"Error durante la ejecución de comandos: {e}")

    def move_files(self, selected_device, argument, destination):
        # Mueve archivos o carpetas de origen a destino
        source = argument.strip('\"')
        source_path = os.path.join(selected_device, source)
        destination_path = os.path.join(selected_device, destination)

        try:
            if os.path.exists(source_path):
                if os.path.isfile(source_path):
                    # Verificar si la carpeta de destino existe y crearla si no
                    os.makedirs(os.path.dirname(destination_path), exist_ok=True)
                    shutil.move(source_path, destination_path)  # Mover el archivo
                    self.success_messages.append(f"Archivo {source_path} movido a {destination_path} correctamente.")
                elif os.path.isdir(source_path):
                    self.copy_and_delete_folder(source_path, destination_path)
                    self.success_messages.append(f"Directorio {source_path} movido a {destination_path} correctamente.")
                else:
                    self.success_messages.append(f"La ruta {source_path} no es ni un archivo ni un directorio válido.")
            else:
                self.success_messages.append(f"No se encontró el archivo o directorio de origen {source_path}.")
        except Exception as e:
            self.success_messages.append(f"Error al mover {source_path}: {e}")

    def copy_and_delete_folder(self, source, destination):
        # Copia y elimina una carpeta
        try:
            if os.path.exists(destination):
                # Si la carpeta de destino ya existe, copiar y reemplazar archivos
                for root, dirs, files in os.walk(source):
                    rel_path = os.path.relpath(root, source)
                    dest_root = os.path.join(destination, rel_path)

                    # Crear subdirectorios en el destino si no existen
                    os.makedirs(dest_root, exist_ok=True)

                    for file in files:
                        src_file = os.path.join(root, file)
                        dest_file = os.path.join(dest_root, file)

                        # Copiar y reemplazar archivos individualmente
                        shutil.copy2(src_file, dest_file)

            else:
                # Si la carpeta de destino no existe, copiar archivos y crear la carpeta de destino
                os.makedirs(destination, exist_ok=True)

                for root, _, files in os.walk(source):
                    rel_path = os.path.relpath(root, source)
                    dest_root = os.path.join(destination, rel_path)

                    # Crear subdirectorios en el destino si no existen
                    os.makedirs(dest_root, exist_ok=True)

                    for file in files:
                        src_file = os.path.join(root, file)
                        dest_file = os.path.join(dest_root, file)

                        # Copiar y reemplazar archivos individualmente
                        shutil.copy2(src_file, dest_file)

                # Eliminar la carpeta de origen después de la copia exitosa
                shutil.rmtree(source)

                self.success_messages.append(f"Carpeta {source} movida a {destination} correctamente.")
        except Exception as e:
            raise RuntimeError(f"Error al copiar y eliminar la carpeta: {e}")

    def delete_item(self, selected_device, argument):
        # Elimina un archivo o carpeta
        item_path = os.path.join(selected_device, argument)

        try:
            if os.path.exists(item_path):
                if os.path.isdir(item_path):
                    shutil.rmtree(item_path)  # Eliminar el directorio y su contenido
                    self.success_messages.append(f"Directorio {item_path} eliminado correctamente.")
                elif os.path.isfile(item_path):
                    os.remove(item_path)  # Eliminar el archivo
                    self.success_messages.append(f"Archivo {item_path} eliminado correctamente.")
                else:
                    self.success_messages.append(f"La ruta {item_path} no es ni un archivo ni un directorio válido.")
            else:
                self.success_messages.append(f"No se encontró el archivo o directorio {item_path}.")
        except Exception as e:
            self.success_messages.append(f"Error al eliminar {item_path}: {e}")

    def copy_files(self, selected_device, source, destination):
        # Copia archivos o carpetas de origen a destino
        source_path = self.get_full_path(selected_device, source)

        # Verificar si la ruta de origen comienza con "./" para interpretarla como relativa
        if source.startswith("./"):
            # Eliminar "./" y usar la ruta relativa
            source_path = os.path.join(self.script_dir, source[2:])

        destination_path = self.get_full_path(selected_device, destination)

        try:
            if os.path.exists(source_path):
                if os.path.isfile(source_path):
                    # Verificar si la carpeta de destino existe y crearla si no
                    destination_directory = os.path.dirname(destination_path)
                    os.makedirs(destination_directory, exist_ok=True)

                    # Copiar el archivo
                    shutil.copy(source_path, destination_path)
                    self.success_messages.append(f"Archivo {source_path} copiado a {destination_path} correctamente.")
                elif os.path.isdir(source_path):
                    self.copiar_carpeta(source_path, destination_path)  # Usar tu método para copiar carpetas
                    self.success_messages.append(f"Directorio {source_path} copiado a {destination_path} correctamente.")
                else:
                    self.success_messages.append(f"La ruta {source_path} no es ni un archivo ni un directorio válido.")
            else:
                self.success_messages.append(f"No se encontró el archivo o directorio de origen {source_path}.")
        except Exception as e:
            self.success_messages.append(f"Error al copiar {source_path}: {e}")

    def copiar_carpeta(self, origen, destino):
        # Copia una carpeta con archivos y subcarpetas
        origen = self.get_full_path(".", origen)  # Convertir la ruta a relativa si comienza con "./"
        destino = self.get_full_path(".", destino)  # Convertir la ruta a relativa si comienza con "./"

        # Verificar si el destino existe
        if os.path.exists(destino):
            # Copiar archivos y carpetas al destino reescribiendo si es necesario
            for root, _, files in os.walk(origen):
                for file in files:
                    origen_archivo = os.path.join(root, file)
                    destino_archivo = os.path.join(destino, os.path.relpath(origen_archivo, origen))
                    os.makedirs(os.path.dirname(destino_archivo), exist_ok=True)  # Crear subdirectorios si no existen
                    self.copiar_archivo(origen_archivo, destino_archivo)
        else:
            # Crear la carpeta de destino si no existe
            os.makedirs(destino, exist_ok=True)

            # Copiar archivos y carpetas al destino reescribiendo si es necesario
            for root, _, files in os.walk(origen):
                for file in files:
                    origen_archivo = os.path.join(root, file)
                    destino_archivo = os.path.join(destino, os.path.relpath(origen_archivo, origen))
                    os.makedirs(os.path.dirname(destino_archivo), exist_ok=True)  # Crear subdirectorios si no existen
                    self.copiar_archivo(origen_archivo, destino_archivo)

    def copiar_archivo(self, origen, destino):
        # Copia un archivo desde el origen hasta el destino
        origen = self.get_full_path(".", origen)  # Convertir la ruta a relativa si comienza con "./"
        destino = self.get_full_path(".", destino)  # Convertir la ruta a relativa si comienza con "./"

        try:
            # Copiar el archivo
            shutil.copy2(origen, destino)
        except Exception as e:
            # Mostrar un mensaje de error
            self.success_messages.append(f"Error al copiar {origen} a {destino}: {e}")

            # Verificar si el directorio de destino existe, y si no, crearlo
            destino_directorio = os.path.dirname(destino)
            os.makedirs(destino_directorio, exist_ok=True)

            try:
                # Intentar copiar el archivo nuevamente después de crear el directorio
                shutil.copy2(origen, destino)
            except Exception as e:
                # Mostrar otro mensaje de error si la segunda copia también falla
                self.success_messages.append(f"Fallo al copiar {origen} a {destino} incluso después de crear el directorio: {e}")

    def show_success_dialog(self):
        if self.success_messages:
            success_message = "\n".join(self.success_messages)
            messagebox.showinfo("Proceso finalizado", success_message)
            # Limpiar la lista después de mostrar el mensaje
            self.success_messages = []

    def show_error(self, message):
        messagebox.showerror("Error", message)


if __name__ == "__main__":
    root = tk.Tk()
    app = MoveFilesApp(root)
    root.geometry("400x250")
    root.resizable(False, False)
    root.mainloop()
