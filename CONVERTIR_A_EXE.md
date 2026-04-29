Este documento explica cómo transformar el script `t4mw.py` en un archivo ejecutable independiente para Windows, de modo que puedas compartirlo y usarlo sin necesidad de tener Python instalado en el equipo destino.

## ⚠️ Requisitos Previos

Antes de comenzar, asegúrate de tener instalado:

1. Python (versión 3.8 o superior recomendada).
2. Git (para clonar el repositorio).

---

## 📋 Paso 1: Preparar el Entorno

1. Clona el repositorio (o descarga el script):

    git clone https://github.com/DanSanMar/tools4mewindows.git  
    cd tools4mewindows

2. Instala las dependencias necesarias:

El script utiliza Pillow para manejar imágenes. Aunque el script intenta instalarla automáticamente, es mejor hacerlo manualmente antes de compilar para asegurar que todo esté correcto.

    pip install pillow pyinstaller

---

## 📦 Paso 2: Preparar los Recursos (Icono)

El script intenta cargar una imagen llamada `LogoALL4meW.png`. Para que el ejecutable tenga el icono correcto y la imagen funcione dentro del `.exe`:

- Asegúrate de que el archivo `LogoALL4meW.png` esté en la misma carpeta donde ejecutarás el comando de compilación.
- Si deseas que el ejecutable tenga un icono personalizado en la barra de tareas, convierte tu imagen a formato `.ico` (ej. `logo.ico`).

---

## 🚀 Paso 3: Compilar a .exe

Abre una terminal (CMD o PowerShell) en la carpeta del proyecto y ejecuta uno de los siguientes comandos según tus necesidades:

### Opción A: Ejecutable Estándar (Con ventana negra de consola)

Esta opción muestra la ventana de comandos mientras se ejecutan las herramientas (útil para ver logs).

    pyinstaller --onefile --name "Tools4MeW" t4mw.py

### Opción B: Ejecutable Sin Ventana (Modo Oculto)

Si prefieres que el programa se ejecute en segundo plano sin mostrar la ventana negra de CMD (ideal para herramientas de sistema), añade el flag `--noconsole` (o `--windowed`).

**Nota:** Las herramientas internas abrirán sus propias ventanas de CMD, pero la ventana principal de Python no aparecerá.

    pyinstaller --onefile --noconsole --name "Tools4MeW" t4mw.py

### Opción C: Con Icono Personalizado (Recomendado)

Para asignar un icono al ejecutable final:

    pyinstaller --onefile --noconsole --icon="logo.ico" --name "Tools4MeW" t4mw.py

(Reemplaza `"logo.ico"` con la ruta real de tu archivo de icono).

---

## 📂 Paso 4: Obtener el Ejecutable

Una vez finalizado el proceso (puede tardar unos minutos):

- Ve a la carpeta generada llamada `dist`.
- Encontrarás el archivo `Tools4MeW.exe`.
- Prueba el ejecutable: haz doble clic para verificar que funciona correctamente.

**Nota Importante:**  
El script incluye una comprobación de administrador. Al ejecutar el `.exe`, es posible que Windows te pida permiso de administrador. Acepta para que las herramientas de sistema (SFC, DISM, etc.) funcionen correctamente.

---

## 🔧 Solución de Problemas Comunes

| Problema | Solución |
|----------|---------|
| Error: "No module named 'PIL'" | Asegúrate de haber ejecutado `pip install pillow` antes de compilar. |
| La imagen no carga en el `.exe` | PyInstaller a veces no detecta recursos dinámicos. Si usas `--onefile`, la imagen debe estar embebida. Si falla, considera usar `--add-data "LogoALL4meW.png;."` en el comando de compilación. |
| Antivirus bloquea el `.exe` | Es común que los antivirus marquen como falso positivo herramientas que ejecutan comandos de sistema. Puedes desactivarlo temporalmente para probar o añadir una excepción. |
| El script pide permisos de Admin | Esto es intencional. El script se reinicia automáticamente con privilegios elevados si no se ejecuta como administrador. |

---

## 📝 Comandos Avanzados (Opcional)

Si quieres incluir la imagen explícitamente para evitar errores de ruta en el ejecutable único:

    pyinstaller --onefile --noconsole --icon="logo.ico" --add-data "LogoALL4meW.png;." --name "Tools4MeW" t4mw.py

(En Windows, el separador es `;`. En Linux/Mac sería `:`).

---

Generado para el proyecto **Tools4MeW - All4me Group**

---

