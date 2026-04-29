import os
import sys
import ctypes
import tkinter as tk
from tkinter import messagebox
import subprocess
import os
import sys

# --- VERIFICACIÓN E INSTALACIÓN AUTOMÁTICA DE LIBRERÍAS ---
# Comprueba si Pillow (para manejar JPG) está instalada. Si no, la instala sola.
try:
    from PIL import Image, ImageTk
except ImportError:
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pillow"])
        from PIL import Image, ImageTk
    except Exception as e:
        # Si falla por problemas de red o permisos, usa tkinter estándar para avisar
        root_err = tk.Tk()
        root_err.withdraw()
        messagebox.showerror("Error de Dependencias", f"Falta la librería 'pillow' para la imagen y no se pudo instalar automáticamente.\n\nError: {e}")
        sys.exit()

def resource_path(relative_path):
    """ Obtiene la ruta absoluta de los recursos, compatible con PyInstaller """
    try:
        # PyInstaller crea una carpeta temporal y guarda la ruta en _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# Ahora usa la función para cargar tu imagen
ruta_al_logo = resource_path("LogoALL4meW.png")
# Ejemplo: self.logo = PhotoImage(file=ruta_al_logo)

# --- CLASE PARA TOOLTIPS (EXPLICACIÓN) ---
# Esta clase crea pequeñas ventanas flotantes de ayuda cuando pasas el ratón 
# sobre un botón. Maneja eventos de entrada (<Enter>) y salida (<Leave>).
class Tooltip:
    def __init__(self, widget, texto):
        self.widget = widget
        self.texto = texto
        self.tip_window = None
        self.id = None
        
        # Bind de eventos
        widget.bind("<Enter>", self.mostrar_tip)
        widget.bind("<Leave>", self.ocultar_tip)
        widget.bind("<ButtonPress>", self.ocultar_tip) # Ocultar si se hace clic

    def mostrar_tip(self, event=None):
        # Si ya hay una ventana de tooltip o no hay texto, salir
        if self.tip_window or not self.texto:
            return
            
        # Calcular posición: Usamos winfo_rootx/y del widget
        # Añadimos un pequeño offset para que no tape el botón
        x = self.widget.winfo_rootx() + self.widget.winfo_width() + 10
        y = self.widget.winfo_rooty() + 10
        
        # Crear la ventana Toplevel
        self.tip_window = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        
        # Crear el contenido del tooltip
        label = tk.Label(tw, text=self.texto, justify='center',
                         background="#2d3436", foreground="#ffffff",
                         relief='solid', borderwidth=1,
                         font=("Segoe UI", "14", "normal"), padx=5, pady=3)
        label.pack()

    def ocultar_tip(self, event=None):
        if self.tip_window:
            self.tip_window.destroy()
            self.tip_window = None
            
# --- VERIFICACIÓN DE ADMINISTRADOR MEJORADA ---
def es_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if not es_admin():
    try:
        # Obtenemos la ruta absoluta del script actual
        script_path = os.path.abspath(sys.argv[0])
        # Intentamos elevar privilegios
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, f'"{script_path}"', None, 1)
        sys.exit()
    except Exception as e:
        print(f"Error crítico al elevar privilegios: {e}")
        input("Presiona Enter para salir...") # Esto evita que la consola se cierre
        sys.exit()

# CAMBIO DE DIRECTORIO: Hazlo DESPUÉS de ser admin
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# --- LÓGICA DE LAS HERRAMIENTAS (BACKEND) ---

# Función maestra para ejecutar comandos en el CMD de Windows de forma externa
def ejecutar_externo(titulo, comando):
    logo_ascii = "### Tools4meW - V.2 ###" # Versión simplificada para evitar errores de escape
    
    # Construimos el comando de forma que sea una sola línea limpia para el CMD
    # Usamos /K en lugar de /C si quieres que la ventana SE QUEDE ABIERTA aunque falle
    script_cmd = (
        f'title {titulo} && '
        f'color 0b && '
        f'echo {logo_ascii} && '
        f'echo [+] Ejecutando: {titulo}... && '
        f'echo ----------------------------------------- && '
        f'{comando} && '
        f'echo. && '
        f'echo ----------------------------------------- && '
        f'echo [!] Tarea finalizada. && '
        f'pause'
    )
    
    try:
        # Usamos shell=True y pasamos el string directamente. 
        # CREATE_NEW_CONSOLE es clave para que no herede la consola invisible (si existe)
        subprocess.Popen(
            ["cmd.exe", "/c", script_cmd],
            creationflags=subprocess.CREATE_NEW_CONSOLE
        )
    except Exception as e:
        messagebox.showerror("Error de Ejecución", f"No se pudo abrir la consola: {e}")

def actualizar_winget():
    # Usa el gestor de paquetes nativo de Windows para actualizar todas las apps instaladas
    ejecutar_externo("Actualizando Software (Winget)", "winget upgrade --all --include-unknown --accept-package-agreements --accept-source-agreements")

def limpiar_sistema():
    # flushdns: limpia la caché de red. del /q: borra archivos temporales del usuario y del sistema
    ejecutar_externo("Limpieza de Temporales y DNS", "ipconfig /flushdns & del /q /f /s %temp%\\* & del /q /f /s C:\\Windows\\Temp\\*")

def reparar_sfc():
    # System File Checker: busca y repara archivos corruptos de Windows
    ejecutar_externo("Escaneo y Reparacion (SFC)", "sfc /scannow")

def limpiar_updates():
    # DISM: Elimina archivos antiguos de actualizaciones de Windows que ya no son necesarios
    ejecutar_externo("Limpieza de Actualizaciones (DISM)", "dism /online /cleanup-image /startcomponentcleanup")

def optimizar_imagen():
    # Compara tu Windows con una copia en la nube de Microsoft para reparar errores graves
    ejecutar_externo("Reparar Imagen de Sistema (DISM)", "dism /online /cleanup-image /restorehealth")

def reiniciar_explorador():
    # Mata el proceso de la barra de tareas y carpetas, y lo vuelve a iniciar para refrescar el sistema
    ejecutar_externo("Reiniciando Explorador", "taskkill /f /im explorer.exe & start explorer.exe")

def liberar_ram():
    # Llama al "Garbage Collector" (Recolector de basura) del sistema para intentar liberar memoria
    ejecutar_externo("Liberando Memoria RAM", "powershell -command \"[System.GC]::Collect();\"")

# --- INTERFAZ GRÁFICA (FRONTEND) ---
try:
    app = tk.Tk()
    app.title("T4MW - All4me Group")
    app.geometry("600x850+500+20")
    app.resizable(True, True)

    # --- CARGA DEL LOGO ALL4MEW ---
    try:
        img_path = resource_path("LogoALL4meW.png")
        img_open = Image.open(img_path)
        # Redimensionamos la imagen para que encaje bien en la cabecera
        img_open = img_open.resize((230, 160), Image.Resampling.LANCZOS)
        logo_img = ImageTk.PhotoImage(img_open)
    except Exception as e:
        logo_img = None
        print(f"No se pudo cargar la imagen: {e}")

    tema_oscuro = False 

    # Función que cambia los colores de todos los elementos de la interfaz
    def aplicar_tema():
        if tema_oscuro:
            bg_main = "#0f172a"     # Colores tipo "Slate" oscuro
            fg_primary = "#f8fafc"
            fg_secondary = "#94a3b8"
            accent = "#38bdf8"      # Azul brillante
            btn_bg = "#334155"
            btn_hover = "#475569"
        else:
            bg_main = "#f1f5f9"     # Colores claros/grises
            fg_primary = "#0f172a"
            fg_secondary = "#64748b"
            accent = "#0284c7"
            btn_bg = "#e2e8f0"
            btn_hover = "#cbd5e1"

        # Aplicación de los colores a cada componente
        app.config(bg=bg_main)
        logo_frame.config(bg=bg_main)
        
        # Lógica de colores para el logo (por si falla la imagen, usa el rayo)
        if not logo_img:
            lbl_logo_icon.config(text="⚡", bg=bg_main, fg=accent)
        else:
            lbl_logo_icon.config(image=logo_img, bg=bg_main)
            lbl_logo_icon.image = logo_img # Referencia obligatoria en Tkinter

        lbl_logo_text.config(bg=bg_main, fg=fg_primary)
        
        container.config(bg=bg_main)
        
        # Bucle para actualizar cada botón creado
        for btn in botones:
            btn.config(bg=btn_bg, fg=fg_primary, activebackground=btn_hover, activeforeground=fg_primary)
            
        btn_tema.config(
            text="  MODO CLARO  " if tema_oscuro else "  MODO OSCURO  ",
            bg=accent,
            fg="#ffffff"
        )

    def alternar_tema():
        global tema_oscuro
        tema_oscuro = not tema_oscuro
        aplicar_tema()

    # --- DISEÑO DE CABECERA ---
    logo_frame = tk.Frame(app, pady=30)
    logo_frame.pack(fill="x")

    # Contenedor del icono/logo
    lbl_logo_icon = tk.Label(logo_frame)
    lbl_logo_icon.pack()
    
    lbl_logo_text = tk.Label(logo_frame, text="T O O L S 4 M E W - V.2", font=("Segoe UI", 22, "bold"))
    lbl_logo_text.pack()


    # Contenedor para los botones
    container = tk.Frame(app)
    container.pack(fill="both", expand=True, padx=40)

    botones = []

    # Función auxiliar para crear botones con un estilo unificado y tooltip
    def crear_boton_moderno(texto, comando, descripcion, icono):
        frame_btn = tk.Frame(container, bg="#0f172a") 
        frame_btn.pack(fill="x", pady=5)
        
        full_text = f"  {icono}   {texto}"
        btn = tk.Button(frame_btn, text=full_text, font=("Segoe UI Semibold", 14), 
                       anchor="w", padx=20, pady=10,
                       relief="flat", cursor="hand2", command=comando)
        btn.pack(fill="x")
        botones.append(btn)
        Tooltip(btn, descripcion) # Asigna la ayuda flotante

    # --- DEFINICIÓN DE BOTONES ---
    crear_boton_moderno("Actualizar Todo el Software", actualizar_winget, "Actualiza las aplicaciones con Winget.", "📦")
    crear_boton_moderno("Limpiar Archivos Basura", limpiar_sistema, "Borra archivos temporales y caché DNS.", "🧹")
    crear_boton_moderno("Reparar Archivos del Sistema", reparar_sfc, "Ejecuta SFC /scannow para comprobar que no haya errores en el sistema.", "🛠")
    crear_boton_moderno("Eliminar Residuos de Update", limpiar_updates, "Libera espacio de actualizaciones de Windows anteriores.", "♻️")
    crear_boton_moderno("Restaurar Imagen de Sistema", optimizar_imagen, "Comprueba y repara la salud de la imagen DISM.", "🩺")
    crear_boton_moderno("Optimizar Memoria RAM", liberar_ram, "Fuerza una limpieza de la memoria RAM.", "🚀")
    crear_boton_moderno("Reiniciar Windows Explorer", reiniciar_explorador, "Reinicia la interfaz de usuario para evitar acumulación de errores.", "🔄")

    # Botón inferior para cambiar el tema
    btn_tema = tk.Button(app, font=("Segoe UI", 12, "bold"), relief="raised", cursor="hand2", command=alternar_tema)
    btn_tema.pack(pady=20)

    # Iniciar la interfaz con el tema configurado
    aplicar_tema()
    app.mainloop()

except Exception as e:
    # Captura cualquier error de inicio (como falta de fuentes o permisos) para que no se cierre sin avisar
    root_err = tk.Tk()
    root_err.withdraw()
    messagebox.showerror("Error Crítico", f"Se produjo un error al iniciar la aplicación:\n\n{e}")