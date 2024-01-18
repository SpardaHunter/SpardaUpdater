import shutil
import os
import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import re

def obtener_unidades_disponibles():
    unidades = []
    for unidad in range(ord('A'), ord('Z')+1):
        unidad = chr(unidad) + ":"
        if os.path.exists(unidad):
            unidades.append(unidad)
    return unidades

class App:
    def __init__(self, master):
        self.master = master
        self.master.title("Sparda SF2000 Updater")
        self.master.geometry("500x300")  # Ajustar el tamaño de la ventana

        self.label_unidad = tk.Label(master, text="Unidad de destino:")
        self.label_unidad.pack(pady=5)

        self.unidades = obtener_unidades_disponibles()
        self.unidad_seleccionada = tk.StringVar()
        self.unidad_combobox = ttk.Combobox(master, textvariable=self.unidad_seleccionada, values=self.unidades, state="readonly")
        self.unidad_combobox.pack(pady=5)

        self.refresh_button = tk.Button(master, text="Refrescar", command=self.refrescar_unidades)
        self.refresh_button.pack(pady=5)

        self.label_config = tk.Label(master, text="Archivo de configuración:")
        self.label_config.pack(pady=5)

        self.config_path_var = tk.StringVar()
        self.config_entry = tk.Entry(master, textvariable=self.config_path_var, state="readonly", width=40)
        self.config_entry.pack(pady=5)

        self.config_button = tk.Button(master, text="Seleccionar Configuración", command=self.seleccionar_archivo_config)
        self.config_button.pack(pady=5)

        self.progress_label = tk.Label(master, text="Progreso:")
        self.progress_label.pack(pady=5)

        self.progressbar = ttk.Progressbar(master, mode="determinate")
        self.progressbar.pack(pady=5)

        self.seleccionar_button = tk.Button(master, text="Ejecutar Acciones", command=self.ejecutar_acciones)
        self.seleccionar_button.pack(pady=10)

        self.refrescar_unidades()

    def refrescar_unidades(self):
        self.unidades = obtener_unidades_disponibles()
        self.unidad_combobox['values'] = self.unidades

    def seleccionar_archivo_config(self):
        archivo_config = filedialog.askopenfilename(title="Seleccione el archivo de configuración", filetypes=[("Archivos de texto", "*.txt")])
        self.config_path_var.set(archivo_config)

    def ejecutar_acciones(self):
        unidad_destino = self.unidad_seleccionada.get()
        archivo_config = self.config_path_var.get()

        if not unidad_destino or not archivo_config:
            self.mostrar_popup_error("Seleccione una unidad y un archivo de configuración antes de ejecutar las acciones.")
            return

        try:
            acciones_completadas = []
            errores = []

            with open(archivo_config, 'r') as file:
                lineas = file.readlines()

            total_acciones = len(lineas)
            progreso_actual = 0

            for linea in lineas:
                progreso_actual += 1
                self.progressbar['value'] = (progreso_actual / total_acciones) * 100
                self.master.update_idletasks()

                partes = re.split(r'"\s*|\s*"', linea.strip())
                partes = [parte for parte in partes if parte]

                accion = partes[0]

                try:
                    if accion == 'copiar':
                        origen = partes[1].replace("\\", "/")
                        destino = os.path.join(unidad_destino, partes[2].replace("\\", "/"))
                        self.copiar_archivo(origen, destino)
                        acciones_completadas.append(f'Se copió {origen} a {destino}')

                    elif accion == 'eliminar':
                        destino = os.path.join(unidad_destino, partes[1].replace("\\", "/"))
                        self.eliminar_archivo(destino)
                        acciones_completadas.append(f'Se eliminó {destino}')

                    elif accion == 'mover':
                        origen = os.path.join(unidad_destino, partes[1].replace("\\", "/"))
                        destino = os.path.join(unidad_destino, partes[2].replace("\\", "/"))
                        self.mover_archivo(origen, destino)
                        acciones_completadas.append(f'Se movió {origen} a {destino}')

                except Exception as e:
                    errores.append(f'Error al procesar la acción: {linea.strip()} - {str(e)}')

            mensaje_exito = "¡Actualización completada!\n" + "\n".join(acciones_completadas)
            
            if errores:
                mensaje_error = "\n\nArchivos con errores:\n" + "\n".join(errores)
                mensaje_exito += mensaje_error

            self.mostrar_popup_exito(mensaje_exito)

        except FileNotFoundError:
            self.mostrar_popup_error(f"Error: El archivo {archivo_config} no se encuentra.")
        except Exception as e:
            self.mostrar_popup_error(f"Error inesperado: {str(e)}")

    def copiar_archivo(self, origen, destino):
        shutil.copy(origen, destino)

    def eliminar_archivo(self, destino):
        os.remove(destino)

    def mover_archivo(self, origen, destino):
        shutil.move(origen, destino)

    def mostrar_popup_exito(self, mensaje):
        messagebox.showinfo("Éxito", mensaje)

    def mostrar_popup_error(self, mensaje):
        messagebox.showerror("Error", mensaje)

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
