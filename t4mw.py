import os
import sys
import ctypes
import tkinter as tk
from tkinter import messagebox
import subprocess

os.chdir(os.path.dirname(os.path.abspath(__file__)))
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
        label = tk.Label(tw, text=self.texto, justify='left',
                         background="#2d3436", foreground="#ffffff",
                         relief='solid', borderwidth=1,
                         font=("Segoe UI", "15", "normal"), padx=5, pady=3)
        label.pack()
        
        # Programar la destrucción automática si el ratón se queda quieto mucho tiempo (opcional, pero ayuda a evitar glitches)
        # No es estrictamente necesario para el parpadeo, pero mejora la UX.

    def ocultar_tip(self, event=None):
        if self.tip_window:
            self.tip_window.destroy()
            self.tip_window = None
            
# --- VERIFICACIÓN DE ADMINISTRADOR ---
# Casi todas las tareas de mantenimiento de Windows requieren permisos elevados.
def es_admin():
    try:
        # Intenta verificar si el usuario actual tiene privilegios de Admin
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

# Si no somos administradores, el script se re-lanza a sí mismo pidiendo permisos.
if not es_admin():
    try:
        # "runas" lanza el proceso pidiendo elevación de privilegios (UAC)
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        sys.exit()
    except Exception as e:
        messagebox.showerror("Error de Permisos", f"No se pudo obtener permisos de administrador: {e}")
        sys.exit()

# --- LÓGICA DE LAS HERRAMIENTAS (BACKEND) ---

# Función maestra para ejecutar comandos en el CMD de Windows de forma externa
def ejecutar_externo(titulo, comando):
    # Usamos shell=True solo para comandos internos de CMD como 'del' o 'ipconfig'
    # 'start' invoca una nueva ventana de forma limpia
    proceso = f'title {titulo} && {comando} && pause'
    subprocess.Popen(['start', 'cmd', '/c', proceso], shell=True)

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
        lbl_logo_icon.config(bg=bg_main, fg=accent)
        lbl_logo_text.config(bg=bg_main, fg=fg_primary)
        lbl_sub.config(bg=bg_main, fg=fg_secondary)
        container.config(bg=bg_main)
        
        # Bucle para actualizar cada botón creado
        for btn in botones:
            btn.config(bg=btn_bg, fg=fg_primary, activebackground=btn_hover, activeforeground=fg_primary)
            # CORRECCIÓN: Se eliminaron los bind manuales aquí para no interferir con el Tooltip
            # Los eventos de hover los maneja ahora exclusivamente la clase Tooltip
            
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

    lbl_logo_icon = tk.Label(logo_frame, text="⚡", font=("Segoe UI", 32))
    lbl_logo_icon.pack()
    
    lbl_logo_text = tk.Label(logo_frame, text="T O O L S 4 M E W", font=("Segoe UI", 22, "bold"))
    lbl_logo_text.pack()

    lbl_sub = tk.Label(app, text="All4me Windows • V1.5", font=("Segoe UI", 9, "bold"))
    lbl_sub.pack(pady=(0, 20))

    # Contenedor para los botones
    container = tk.Frame(app)
    container.pack(fill="both", expand=True, padx=40)

    botones = []

    # Función auxiliar para crear botones con un estilo unificado y tooltip
    def crear_boton_moderno(texto, comando, descripcion, icono):
        frame_btn = tk.Frame(container, bg="#0f172a") 
        frame_btn.pack(fill="x", pady=5)
        
        full_text = f"  {icono}   {texto}"
        btn = tk.Button(frame_btn, text=full_text, font=("Segoe UI Semibold", 15), 
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