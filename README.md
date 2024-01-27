# SpardaUpdater

![imagen](https://github.com/SpardaHunter/SpardaUpdater/assets/155873668/9da8d587-de58-4c7c-9bee-7ae8474b03dd)


Programa para realizar acciones a una unidad

¿Como funciona?

Edita un archivo .txt y podrás utilizar los siguientes comandos por líneas

Comandos:

```
eliminar
copiar
mover
```

**Comando Eliminar:**

Uso: eliminar ruta
    Descripción: Este comando se utiliza para eliminar un archivo o directorio en el dispositivo seleccionado.
    Variables:
        ruta: Ruta del archivo o directorio que se eliminará. 
		
Ejemplos:
```
eliminar "UPDATE B/File.mp4"
eliminar "UPDATE A/New Folder"
```


**Comando Copiar:**

Uso: copiar origen destino
    Descripción: Este comando se utiliza para copiar un archivo o directorio desde la ubicación de origen a la ubicación de destino en el dispositivo seleccionado reemplazando archivos si fuese necesario. Si no existe la carpeta, la creará.
    Variables:
        origen: Ruta del archivo o directorio que se copiará. Puede ser una ruta relativa o absoluta en el dispositivo.
        destino: Ruta del directorio de destino para la operación de copia. 

Ejemplos:
```
copiar "Carpeta 2/images" "BACKUP 2/images"
copiar "Archivos/1.txt" "BACKUP/archivos/copia1.txt"
copiar "./UPDATE/images" "CARPETA/images"
copiar "./UPDATE/images/FOTO.png" "CARPETA/images/FOTO.png"
```


**Comando Mover:**

Uso: mover origen destino
    Descripción: Este comando se utiliza para mover un archivo o directorio desde la ubicación de origen a la ubicación de destino en el dispositivo seleccionado reemplazando archivos si fuese necesario. Si no existe la carpeta, la creará.
    Variables:
        origen: Ruta del archivo o directorio que se moverá. 
        destino: Ruta del directorio de destino para la operación de movimiento.
		
```
mover "Carpeta/images" "BACKUP/images"
mover "Archivos/1.txt" "BACKUP/archivos/copia1.txt"
```

--------

# SpardaUpdater

![imagen](https://github.com/SpardaHunter/SpardaUpdater/assets/155873668/9da8d587-de58-4c7c-9bee-7ae8474b03dd)

Program to perform actions on a unit

How does it work?

Edit a .txt file and you can use the following commands in lines

Commands:

```
eliminar
copiar
mover
```

**eliminar Command:**

Usage: delete route
     Description: This command is used to delete a file or directory on the selected device.
     Variables:
         path: Path of the file or directory to be deleted.

Examples:
```
eliminar "UPDATE B/File.mp4"
eliminar "UPDATE A/New Folder"
```


**copiar Command:**

Usage: copy source destination
     Description: This command is used to copy a file or directory from the source location to the destination location on the selected device, replacing files if necessary. If the folder does not exist, it will create it.
     Variables:
         origin: Path of the file or directory to be copied. It can be a relative or absolute path on the device.
         destination: Path of the destination directory for the copy operation.

Examples:
```
copiar "Folder 2/images" "BACKUP 2/images"
copiar "Files/1.txt" "BACKUP/files/copy1.txt"
copiar "./UPDATE/images" "FOLDER/images"
copiar "./UPDATE/images/FOTO.png" "FOLDER/images/FOTO.png"
```


**mover Command:**

Usage: move origin destination
     Description: This command is used to move a file or directory from the source location to the destination location on the selected device, replacing files if necessary. If the folder does not exist, it will create it.
     Variables:
         origin: Path of the file or directory to be moved.
         destination: Path of the destination directory for the move operation.


```
mover "Folder/images" "BACKUP/images"
mover "Files/1.txt" "BACKUP/files/copy1.txt"
```


