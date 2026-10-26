import os
import sys
import ctypes
import logging
import tkinter as tk
from tkinter import messagebox
import subprocess
import shutil

VERSION = "V.4"

# --- LOGGING A ARCHIVO TEMPORAL (útil cuando se ejecuta como .exe sin consola) ---
log_path = os.path.join(os.environ.get("TEMP", "."), "t4mw.log")
logging.basicConfig(
    filename=log_path,
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)
logging.info("Iniciando T4MW %s", VERSION)

# --- VERIFICACIÓN E INSTALACIÓN AUTOMÁTICA DE LIBRERÍAS ---
# Comprueba si Pillow (para manejar JPG) está instalada. Si no, la instala sola.
try:
    from PIL import Image, ImageTk
except ImportError:
    if getattr(sys, "frozen", False):
        # Dentro de un .exe no se puede instalar Pillow: debe venir empaquetada
        root_err = tk.Tk()
        root_err.withdraw()
        messagebox.showerror(
            "Error de Dependencias",
            "El ejecutable no incluye Pillow. Recompílalo con 'pyinstaller Tools4MeW.spec'.",
        )
        sys.exit()

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
    # PyInstaller crea una carpeta temporal y guarda la ruta en _MEIPASS
    base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

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
    except Exception:
        return False

if not es_admin():
    try:
        # Obtenemos la ruta absoluta del script actual
        script_path = os.path.abspath(sys.argv[0])
        # Intentamos elevar privilegios. ShellExecuteW devuelve <= 32 si falla.
        resultado = ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, f'"{script_path}"', None, 1
        )
        if resultado <= 32:
            raise OSError(f"ShellExecuteW devolvió {resultado}")
        sys.exit()
    except Exception as e:
        print(f"Error crítico al elevar privilegios: {e}")
        input("Presiona Enter para salir...") # Esto evita que la consola se cierre
        sys.exit()

# CAMBIO DE DIRECTORIO: Hazlo DESPUÉS de ser admin
os.chdir(os.path.dirname(os.path.abspath(__file__)))
logging.info("Ejecutando como administrador en %s", os.getcwd())

# --- LÓGICA DE LAS HERRAMIENTAS (BACKEND) ---

# Paleta del tema actual, para que los diálogos hereden los colores
TEMA_ACTUAL = {}

def comando_powershell(codigo):
    """Envuelve código PowerShell en un comando de una línea para CMD."""
    # El código no debe contener comillas dobles; usa comillas simples dentro.
    if '"' in codigo:
        raise ValueError("El código PowerShell no debe contener comillas dobles")
    return f'powershell -NoProfile -Command "{codigo}"'

COMANDO_ACTUALIZAR_WINGET = (
    "winget upgrade --all --include-unknown "
    "--accept-package-agreements --accept-source-agreements"
)

def pasos_limpieza_rapida():
    """Pasos comunes de la limpieza rápida, sin papelera ni DISM."""
    return [
        (
            "Limpiando temporales del usuario",
            comando_powershell(
                "Get-ChildItem -LiteralPath $env:TEMP -Force -ErrorAction SilentlyContinue | "
                "Where-Object { $_.Name -notlike '_MEI*' -and $_.Name -ne 't4mw.log' } | "
                "Remove-Item -Recurse -Force -ErrorAction SilentlyContinue"
            ),
        ),
        (
            "Limpiando temporales de Windows",
            comando_powershell(
                "Get-ChildItem -LiteralPath (Join-Path $env:WINDIR 'Temp') -Force -ErrorAction SilentlyContinue | "
                "Where-Object { $_.Name -notlike '_MEI*' -and $_.Name -ne 't4mw.log' } | "
                "Remove-Item -Recurse -Force -ErrorAction SilentlyContinue"
            ),
        ),
        ("Vaciando cache DNS", "ipconfig /flushdns"),
    ]

def pasos_diagnostico_rapido():
    """Pasos de diagnóstico de solo lectura."""
    return [
        (
            "Comprobando la imagen de Windows con DISM",
            "dism /online /cleanup-image /checkhealth",
        ),
        (
            "Consultando discos y espacio",
            comando_powershell(
                "Get-PhysicalDisk | Format-List FriendlyName,HealthStatus,OperationalStatus; "
                "Get-Volume | Select-Object DriveLetter,FileSystemLabel,"
                "@{n='LibreGB';e={[math]::Round($_.SizeRemaining/1GB,1)}},"
                "@{n='TotalGB';e={[math]::Round($_.Size/1GB,1)}} | Format-Table -AutoSize"
            ),
        ),
        (
            "Consultando estado de Defender",
            comando_powershell(
                "try { Get-MpComputerStatus | Format-List "
                "AntivirusEnabled,RealTimeProtectionEnabled,AntivirusSignatureLastUpdated } "
                "catch { Write-Host 'Defender no disponible' }"
            ),
        ),
    ]

def elegir_opcion(titulo, mensaje, opciones):
    """Muestra un diálogo modal con varias opciones y devuelve el valor elegido."""
    ventana = tk.Toplevel(app)
    ventana.title(titulo)
    try:
        ventana.iconbitmap(resource_path("LogoALL4meW.ico"))
    except Exception:
        pass
    ventana.transient(app)
    ventana.resizable(False, False)

    bg = TEMA_ACTUAL.get("bg", "#f1f5f9")
    fg = TEMA_ACTUAL.get("fg", "#0f172a")
    btn_bg = TEMA_ACTUAL.get("btn", "#e2e8f0")
    btn_hover = TEMA_ACTUAL.get("btn_hover", "#cbd5e1")
    ventana.config(bg=bg)

    contenido = tk.Frame(ventana, bg=bg, padx=20, pady=20)
    contenido.pack(fill="both", expand=True)

    tk.Label(
        contenido, text=mensaje, bg=bg, fg=fg, justify="left",
        wraplength=430, font=("Segoe UI", 11),
    ).pack(pady=(0, 15))

    resultado = {"valor": None}

    def elegir(valor):
        resultado["valor"] = valor
        ventana.destroy()

    for texto, valor in opciones:
        tk.Button(
            contenido, text=texto, command=lambda v=valor: elegir(v),
            font=("Segoe UI Semibold", 11), anchor="w", padx=12, pady=8,
            bg=btn_bg, fg=fg, activebackground=btn_hover, activeforeground=fg,
            relief="flat", cursor="hand2",
        ).pack(fill="x", pady=3)

    ventana.bind("<Escape>", lambda e: ventana.destroy())
    ventana.protocol("WM_DELETE_WINDOW", ventana.destroy)

    ventana.update_idletasks()
    x = app.winfo_rootx() + (app.winfo_width() - ventana.winfo_reqwidth()) // 2
    y = app.winfo_rooty() + (app.winfo_height() - ventana.winfo_reqheight()) // 2
    ventana.geometry(f"+{max(x, 0)}+{max(y, 0)}")

    # El grab necesita que la ventana ya esté visible.
    ventana.wait_visibility()
    ventana.grab_set()
    ventana.focus_set()
    ventana.wait_window()
    return resultado["valor"]

def elegir_limpieza():
    """Diálogo de limpieza con modos rápido/completo y papelera opcional."""
    ventana = tk.Toplevel(app)
    ventana.title("Limpiar sistema")
    try:
        ventana.iconbitmap(resource_path("LogoALL4meW.ico"))
    except Exception:
        pass
    ventana.transient(app)
    ventana.resizable(False, False)

    bg = TEMA_ACTUAL.get("bg", "#f1f5f9")
    fg = TEMA_ACTUAL.get("fg", "#0f172a")
    btn_bg = TEMA_ACTUAL.get("btn", "#e2e8f0")
    btn_hover = TEMA_ACTUAL.get("btn_hover", "#cbd5e1")
    ventana.config(bg=bg)

    contenido = tk.Frame(ventana, bg=bg, padx=20, pady=20)
    contenido.pack(fill="both", expand=True)

    tk.Label(
        contenido,
        text=(
            "Elige el tipo de limpieza:\n\n"
            "• Rápida: temporales del usuario y de Windows, y caché DNS (1-2 min).\n"
            "• Completa: añade la limpieza de componentes de Windows con DISM (10-30 min).\n\n"
            "La papelera de reciclaje solo se vacía si marcas la casilla inferior."
        ),
        bg=bg, fg=fg, justify="left", wraplength=430, font=("Segoe UI", 11),
    ).pack(pady=(0, 10))

    var_papelera = tk.BooleanVar(value=False)
    tk.Checkbutton(
        contenido,
        text="Incluir papelera de reciclaje (borrado permanente)",
        variable=var_papelera,
        bg=bg, fg=fg, selectcolor=btn_bg,
        activebackground=bg, activeforeground=fg,
        font=("Segoe UI", 10), anchor="w", justify="left",
        wraplength=430, cursor="hand2", highlightthickness=0, bd=0,
    ).pack(fill="x", pady=(0, 2))

    tk.Label(
        contenido,
        text="Si la marcas, los archivos de la papelera se eliminarán de forma permanente.",
        bg=bg, fg="#dc2626", justify="left", wraplength=430,
        font=("Segoe UI", 9),
    ).pack(fill="x", pady=(0, 12))

    resultado = {"modo": None, "papelera": False}

    def elegir(modo):
        resultado["modo"] = modo
        resultado["papelera"] = bool(var_papelera.get())
        ventana.destroy()

    for texto, valor in (
        ("Limpieza rápida", "rapida"),
        ("Limpieza completa", "completa"),
        ("Cancelar", None),
    ):
        tk.Button(
            contenido, text=texto, command=lambda v=valor: elegir(v),
            font=("Segoe UI Semibold", 11), anchor="w", padx=12, pady=8,
            bg=btn_bg, fg=fg, activebackground=btn_hover, activeforeground=fg,
            relief="flat", cursor="hand2",
        ).pack(fill="x", pady=3)

    ventana.bind("<Escape>", lambda e: elegir(None))
    ventana.protocol("WM_DELETE_WINDOW", lambda: elegir(None))

    ventana.update_idletasks()
    x = app.winfo_rootx() + (app.winfo_width() - ventana.winfo_reqwidth()) // 2
    y = app.winfo_rooty() + (app.winfo_height() - ventana.winfo_reqheight()) // 2
    ventana.geometry(f"+{max(x, 0)}+{max(y, 0)}")

    ventana.wait_visibility()
    ventana.grab_set()
    ventana.focus_set()
    ventana.wait_window()
    return resultado["modo"], resultado["papelera"]

def elegir_modo_auto():
    """Diálogo para seleccionar las tareas del modo automático."""
    ventana = tk.Toplevel(app)
    ventana.title("Modo automático")
    try:
        ventana.iconbitmap(resource_path("LogoALL4meW.ico"))
    except Exception:
        pass
    ventana.transient(app)
    ventana.resizable(False, False)

    bg = TEMA_ACTUAL.get("bg", "#f1f5f9")
    fg = TEMA_ACTUAL.get("fg", "#0f172a")
    btn_bg = TEMA_ACTUAL.get("btn", "#e2e8f0")
    btn_hover = TEMA_ACTUAL.get("btn_hover", "#cbd5e1")
    ventana.config(bg=bg)

    contenido = tk.Frame(ventana, bg=bg, padx=20, pady=20)
    contenido.pack(fill="both", expand=True)

    tk.Label(
        contenido,
        text=(
            "Selecciona las tareas que quieres ejecutar seguidas.\n\n"
            "Las tareas marcadas se ejecutarán en este orden: actualización, "
            "limpieza rápida y diagnóstico rápido. Se abrirá una sola consola. "
            "La actualización puede tardar varios minutos."
        ),
        bg=bg, fg=fg, justify="left", wraplength=430, font=("Segoe UI", 11),
    ).pack(pady=(0, 10))

    var_actualizar = tk.BooleanVar(value=True)
    var_limpiar = tk.BooleanVar(value=True)
    var_diagnostico = tk.BooleanVar(value=True)

    for texto, variable in (
        ("Actualizar software con Winget", var_actualizar),
        ("Limpieza rápida (temporales y DNS)", var_limpiar),
        ("Diagnóstico rápido (solo lectura)", var_diagnostico),
    ):
        tk.Checkbutton(
            contenido,
            text=texto,
            variable=variable,
            bg=bg, fg=fg, selectcolor=btn_bg,
            activebackground=bg, activeforeground=fg,
            font=("Segoe UI", 10), anchor="w", justify="left",
            cursor="hand2", highlightthickness=0, bd=0,
        ).pack(fill="x", pady=2)

    tk.Label(
        contenido,
        text=(
            "No incluye reparación, papelera, limpieza completa ni diagnóstico completo."
        ),
        bg=bg, fg="#dc2626", justify="left", wraplength=430,
        font=("Segoe UI", 9),
    ).pack(fill="x", pady=(8, 12))

    resultado = {"seleccion": None}

    def ejecutar():
        seleccion = {
            "actualizar": bool(var_actualizar.get()),
            "limpiar": bool(var_limpiar.get()),
            "diagnostico": bool(var_diagnostico.get()),
        }
        if not any(seleccion.values()):
            messagebox.showwarning(
                "Modo automático",
                "Selecciona al menos una tarea.",
                parent=ventana,
            )
            return
        resultado["seleccion"] = seleccion
        ventana.destroy()

    def cancelar():
        ventana.destroy()

    tk.Button(
        contenido, text="Ejecutar modo automático", command=ejecutar,
        font=("Segoe UI Semibold", 11), anchor="w", padx=12, pady=8,
        bg=btn_bg, fg=fg, activebackground=btn_hover, activeforeground=fg,
        relief="flat", cursor="hand2",
    ).pack(fill="x", pady=3)

    tk.Button(
        contenido, text="Cancelar", command=cancelar,
        font=("Segoe UI Semibold", 11), anchor="w", padx=12, pady=8,
        bg=btn_bg, fg=fg, activebackground=btn_hover, activeforeground=fg,
        relief="flat", cursor="hand2",
    ).pack(fill="x", pady=3)

    ventana.bind("<Escape>", lambda e: cancelar())
    ventana.protocol("WM_DELETE_WINDOW", cancelar)

    ventana.update_idletasks()
    x = app.winfo_rootx() + (app.winfo_width() - ventana.winfo_reqwidth()) // 2
    y = app.winfo_rooty() + (app.winfo_height() - ventana.winfo_reqheight()) // 2
    ventana.geometry(f"+{max(x, 0)}+{max(y, 0)}")

    ventana.wait_visibility()
    ventana.grab_set()
    ventana.focus_set()
    ventana.wait_window()
    return resultado["seleccion"]

def construir_script(titulo, pasos):
    """Construye una línea de CMD con varios pasos numerados."""
    logo_ascii = f"### Tools4meW - {VERSION} ###"
    partes = [
        f"title {titulo}",
        "color 0b",
        f"echo {logo_ascii}",
        "echo -----------------------------------------",
    ]

    total = len(pasos)
    for indice, (etiqueta, comando) in enumerate(pasos, 1):
        partes.append(f"echo [{indice}/{total}] {etiqueta}...")
        partes.append(comando)
        partes.append("echo.")

    partes.extend([
        "echo -----------------------------------------",
        "echo [!] Tarea finalizada.",
        "pause",
    ])
    return " & ".join(partes)

def ejecutar_secuencia(titulo, pasos):
    """Abre una consola nueva y ejecuta los pasos en orden."""
    script_cmd = construir_script(titulo, pasos)

    logging.info("Ejecutando: %s", titulo)
    for etiqueta, comando in pasos:
        logging.info("  [%s] %s", etiqueta, comando)

    try:
        # Una sola cadena para que CMD interprete bien las comillas internas.
        # /d evita AutoRun y CREATE_NEW_CONSOLE da una ventana independiente.
        subprocess.Popen(
            f'cmd.exe /d /c {script_cmd}',
            creationflags=subprocess.CREATE_NEW_CONSOLE
        )
    except Exception as e:
        logging.exception("Error ejecutando %s", titulo)
        messagebox.showerror("Error de Ejecución", f"No se pudo abrir la consola: {e}")

def ejecutar_externo(titulo, comando):
    """Atajo para lanzar un único comando en una consola."""
    ejecutar_secuencia(titulo, [(titulo, comando)])

def confirmar(titulo, mensaje):
    # Pide confirmación antes de una acción larga o destructiva.
    # El foco por defecto queda en "No" para evitar ejecuciones accidentales.
    return messagebox.askyesno(titulo, mensaje, icon="warning", default=messagebox.NO)

def comprobar_winget():
    """Comprueba si Winget está disponible y avisa si no lo está."""
    if shutil.which("winget") is not None:
        return True

    logging.error("winget no encontrado en PATH")
    messagebox.showerror(
        "Winget no disponible",
        "No se encontró 'winget' en el PATH.\n\n"
        "Instala o actualiza 'App Installer' desde Microsoft Store y vuelve a intentarlo.",
    )
    return False

def actualizar_winget():
    # Usa el gestor de paquetes nativo de Windows para actualizar todas las apps instaladas
    if not comprobar_winget():
        return
    ejecutar_externo("Actualizando Software con Winget", COMANDO_ACTUALIZAR_WINGET)

def limpiar_sistema():
    modo, incluir_papelera = elegir_limpieza()
    if modo is None:
        logging.info("Limpieza cancelada por el usuario")
        return

    logging.info("Modo de limpieza: %s; papelera: %s", modo, incluir_papelera)
    pasos = pasos_limpieza_rapida()

    if incluir_papelera:
        pasos.append((
            "Vaciando papelera de reciclaje",
            comando_powershell(
                "try { Clear-RecycleBin -Force -ErrorAction Stop; "
                "Write-Host 'Papelera vaciada.' } "
                "catch { Write-Host ('Aviso: ' + $_.Exception.Message) }"
            ),
        ))

    if modo == "completa":
        pasos.append((
            "Limpiando componentes de Windows con DISM",
            "dism /online /cleanup-image /startcomponentcleanup",
        ))

    titulo = "Limpieza rapida" if modo == "rapida" else "Limpieza completa"
    if incluir_papelera:
        titulo += " + papelera"
    ejecutar_secuencia(titulo, pasos)

def reparar_windows():
    if not confirmar(
        "Reparar Windows",
        "Se ejecutará DISM /RestoreHealth y después SFC /scannow.\n\n"
        "Puede tardar entre 20 y 60 minutos, conviene tener conexión a Internet "
        "y no se debe cerrar la consola. Si quieres, crea antes un punto de "
        "restauración desde Más herramientas.\n\n¿Quieres continuar?",
    ):
        return

    ejecutar_secuencia("Reparar Windows", [
        ("Reparando la imagen del sistema con DISM", "dism /online /cleanup-image /restorehealth"),
        ("Comprobando archivos del sistema con SFC", "sfc /scannow"),
    ])

def diagnostico():
    modo = elegir_opcion(
        "Diagnóstico",
        "Elige el nivel de diagnóstico:\n\n"
        "• Rápido: estado de la imagen de Windows, discos y Defender (1-3 min).\n"
        "• Completo: añade análisis del almacén de componentes y escaneo del disco C: (5-20 min).\n\n"
        "Solo lectura: no modifica nada.",
        [
            ("Diagnóstico rápido", "rapido"),
            ("Diagnóstico completo", "completo"),
            ("Cancelar", None),
        ],
    )
    if modo is None:
        logging.info("Diagnostico cancelado por el usuario")
        return

    logging.info("Modo de diagnostico: %s", modo)
    pasos = pasos_diagnostico_rapido()

    if modo == "completo":
        pasos.insert(1, (
            "Analizando el almacen de componentes con DISM",
            "dism /online /cleanup-image /analyzecomponentstore",
        ))
        pasos.append((
            "Escaneando el disco C: con chkdsk",
            "chkdsk C: /scan",
        ))

    titulo = "Diagnostico rapido" if modo == "rapido" else "Diagnostico completo"
    ejecutar_secuencia(titulo, pasos)

def modo_auto():
    """Ejecuta en una sola consola las tareas seleccionadas del modo automático."""
    seleccion = elegir_modo_auto()
    if seleccion is None:
        logging.info("Modo automatico cancelado por el usuario")
        return

    if not any(seleccion.values()):
        logging.warning("Modo automatico sin tareas seleccionadas")
        return

    if seleccion["actualizar"] and not comprobar_winget():
        return

    logging.info(
        "Modo automatico: actualizar=%s; limpiar=%s; diagnostico=%s",
        seleccion["actualizar"], seleccion["limpiar"], seleccion["diagnostico"],
    )

    pasos = []
    if seleccion["actualizar"]:
        pasos.append(("Actualizando software con Winget", COMANDO_ACTUALIZAR_WINGET))
    if seleccion["limpiar"]:
        pasos.extend(pasos_limpieza_rapida())
    if seleccion["diagnostico"]:
        pasos.extend(pasos_diagnostico_rapido())

    ejecutar_secuencia("Mantenimiento automatico", pasos)

def crear_punto_restauracion():
    if not confirmar(
        "Crear punto de restauración",
        "Se creará un punto de restauración de Windows. Requiere que la "
        "Protección del sistema esté activada; Windows puede limitar la "
        "frecuencia a un punto cada 24 horas.\n\n¿Quieres continuar?",
    ):
        return

    ejecutar_externo(
        "Punto de restauracion",
        comando_powershell(
            "Checkpoint-Computer -Description 'T4MW - mantenimiento' "
            "-RestorePointType MODIFY_SETTINGS"
        ),
    )

def analizar_defender():
    if not confirmar(
        "Análisis rápido de Defender",
        "Se actualizarán las firmas y se ejecutará un análisis rápido de "
        "Windows Defender. Si usas otro antivirus, puede no estar disponible.\n\n"
        "¿Quieres continuar?",
    ):
        return

    ejecutar_secuencia("Analisis rapido de Defender", [
        ("Actualizando firmas de Defender", comando_powershell("Update-MpSignature")),
        ("Ejecutando analisis rapido", comando_powershell("Start-MpScan -ScanType QuickScan")),
    ])

def abrir_windows_update():
    try:
        os.startfile("ms-settings:windowsupdate")
        logging.info("Abriendo Windows Update")
    except Exception as e:
        logging.exception("No se pudo abrir Windows Update")
        messagebox.showerror(
            "Windows Update",
            f"No se pudo abrir la configuración de Windows Update:\n\n{e}",
        )

def abrir_log():
    if not os.path.exists(log_path):
        messagebox.showinfo("Log", "Todavía no hay ningún registro.")
        return

    try:
        os.startfile(log_path)
        logging.info("Abriendo el log: %s", log_path)
    except Exception as e:
        logging.exception("No se pudo abrir el log")
        messagebox.showerror("Log", f"No se pudo abrir el archivo de log:\n\n{e}")

def abrir_enlace(url, titulo):
    """Abre un enlace en el navegador y avisa si no se puede."""
    try:
        os.startfile(url)
        logging.info("Abriendo enlace (%s): %s", titulo, url)
    except Exception as e:
        logging.exception("No se pudo abrir el enlace: %s", url)
        messagebox.showerror(titulo, f"No se pudo abrir el enlace:\n\n{e}")

def abrir_ayuda_windows():
    abrir_enlace("https://support.microsoft.com/es-es/windows", "Ayuda de Windows")

def acerca_de():
    """Muestra la información del proyecto con enlaces al repositorio y al perfil."""
    ventana = tk.Toplevel(app)
    ventana.title("Acerca de T4MW")
    try:
        ventana.iconbitmap(resource_path("LogoALL4meW.ico"))
    except Exception:
        pass
    ventana.transient(app)
    ventana.resizable(False, False)

    bg = TEMA_ACTUAL.get("bg", "#f1f5f9")
    fg = TEMA_ACTUAL.get("fg", "#0f172a")
    btn_bg = TEMA_ACTUAL.get("btn", "#e2e8f0")
    btn_hover = TEMA_ACTUAL.get("btn_hover", "#cbd5e1")
    ventana.config(bg=bg)

    contenido = tk.Frame(ventana, bg=bg, padx=24, pady=20)
    contenido.pack(fill="both", expand=True)

    tk.Label(
        contenido, text="T4MW - All4me Group",
        bg=bg, fg=fg, font=("Segoe UI", 16, "bold"),
    ).pack(pady=(0, 2))

    tk.Label(
        contenido, text=f"Versión {VERSION}",
        bg=bg, fg=fg, font=("Segoe UI", 11),
    ).pack(pady=(0, 12))

    tk.Label(
        contenido,
        text=(
            "Herramientas de mantenimiento para Windows 10/11.\n\n"
            "Desarrollado por DanSanMar.\n"
            "Licencia MIT."
        ),
        bg=bg, fg=fg, justify="center", font=("Segoe UI", 10),
    ).pack(pady=(0, 15))

    def abrir_repositorio():
        abrir_enlace(
            "https://github.com/DanSanMar/tools4mewindows",
            "Repositorio T4MW",
        )

    def abrir_perfil():
        abrir_enlace("https://github.com/DanSanMar", "Perfil de GitHub")

    for texto, comando in (
        ("Abrir repositorio", abrir_repositorio),
        ("Abrir perfil de GitHub", abrir_perfil),
        ("Cerrar", ventana.destroy),
    ):
        tk.Button(
            contenido, text=texto, command=comando,
            font=("Segoe UI Semibold", 11), anchor="w", padx=12, pady=8,
            bg=btn_bg, fg=fg, activebackground=btn_hover, activeforeground=fg,
            relief="flat", cursor="hand2",
        ).pack(fill="x", pady=3)

    ventana.bind("<Escape>", lambda e: ventana.destroy())
    ventana.protocol("WM_DELETE_WINDOW", ventana.destroy)

    ventana.update_idletasks()
    x = app.winfo_rootx() + (app.winfo_width() - ventana.winfo_reqwidth()) // 2
    y = app.winfo_rooty() + (app.winfo_height() - ventana.winfo_reqheight()) // 2
    ventana.geometry(f"+{max(x, 0)}+{max(y, 0)}")

    ventana.wait_visibility()
    ventana.grab_set()
    ventana.focus_set()
    ventana.wait_window()

# --- INTERFAZ GRÁFICA (FRONTEND) ---
try:
    app = tk.Tk()
    app.title(f"T4MW - All4me Group ({VERSION})")
    app.geometry("600x650+500+20")
    app.resizable(True, True)

    # Icono de la ventana (el .exe ya lo lleva, pero así también se ve al ejecutar el .py)
    try:
        app.iconbitmap(resource_path("LogoALL4meW.ico"))
    except Exception as e:
        logging.warning("No se pudo cargar el icono: %s", e)

    # --- BARRA SUPERIOR DE MENÚS ---
    def poblar_menu_mas(menu):
        menu.add_command(label="Crear punto de restauración", command=crear_punto_restauracion)
        menu.add_command(label="Análisis rápido de Defender", command=analizar_defender)

    def poblar_menu_ayuda(menu):
        menu.add_command(label="Abrir log", command=abrir_log)
        menu.add_command(label="Ayuda de Windows", command=abrir_ayuda_windows)

    barra_menus = tk.Frame(app, bd=0, highlightthickness=0)
    barra_menus.pack(fill="x", side="top")
    for columna in range(4):
        barra_menus.grid_columnconfigure(columna, weight=1, uniform="pestanas")

    # Cuatro pestañas de ancho uniforme: Modo auto, Más, Acerca y Ayuda.
    btn_menu_ayuda = tk.Menubutton(
        barra_menus, text="Ayuda",
        font=("Segoe UI Semibold", 10), relief="flat", bd=0,
        padx=8, pady=6, highlightthickness=0, cursor="hand2",
    )
    menu_ayuda = tk.Menu(btn_menu_ayuda, tearoff=0)
    poblar_menu_ayuda(menu_ayuda)
    btn_menu_ayuda.config(menu=menu_ayuda)
    btn_menu_ayuda.grid(row=0, column=3, sticky="ew", padx=1, pady=2)

    btn_menu_acerca = tk.Button(
        barra_menus, text="Acerca de T4MW", command=acerca_de,
        font=("Segoe UI Semibold", 10), relief="flat", bd=0,
        padx=8, pady=6, highlightthickness=0, cursor="hand2",
    )
    btn_menu_acerca.grid(row=0, column=2, sticky="ew", padx=1, pady=2)

    btn_menu_mas = tk.Menubutton(
        barra_menus, text="Más herramientas",
        font=("Segoe UI Semibold", 10), relief="flat", bd=0,
        padx=8, pady=6, highlightthickness=0, cursor="hand2",
    )
    menu_mas = tk.Menu(btn_menu_mas, tearoff=0)
    poblar_menu_mas(menu_mas)
    btn_menu_mas.config(menu=menu_mas)
    btn_menu_mas.grid(row=0, column=1, sticky="ew", padx=1, pady=2)

    btn_modo_auto = tk.Button(
        barra_menus, text="Modo auto", command=modo_auto,
        font=("Segoe UI Semibold", 10), relief="flat", bd=0,
        padx=8, pady=6, highlightthickness=0, cursor="hand2",
    )
    btn_modo_auto.grid(row=0, column=0, sticky="ew", padx=1, pady=2)

    linea_menus = tk.Frame(app, height=2)
    linea_menus.pack(fill="x")

    # --- CARGA DEL LOGO ALL4MEW ---
    try:
        img_path = resource_path("LogoALL4meW.png")
        img_open = Image.open(img_path)
        # Redimensionamos la imagen para que encaje bien en la cabecera
        img_open = img_open.resize((230, 160), Image.Resampling.LANCZOS)
        logo_img = ImageTk.PhotoImage(img_open)
    except Exception as e:
        logo_img = None
        logging.warning("No se pudo cargar la imagen: %s", e)

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
            barra_bg = "#172554"    # Azul muy oscuro para las pestañas
            barra_hover = "#1e3a8a"
            barra_borde = "#38bdf8"
            btn_accion_bg = "#1e3a8a"
            btn_accion_hover = "#1e40af"
            btn_accion_borde = "#0ea5e9"
        else:
            bg_main = "#f1f5f9"     # Colores claros/grises
            fg_primary = "#0f172a"
            fg_secondary = "#64748b"
            accent = "#0284c7"
            btn_bg = "#e2e8f0"
            btn_hover = "#cbd5e1"
            barra_bg = "#dbeafe"    # Azul claro para las pestañas
            barra_hover = "#bfdbfe"
            barra_borde = "#93c5fd"
            btn_accion_bg = "#e0f2fe"
            btn_accion_hover = "#bae6fd"
            btn_accion_borde = "#7dd3fc"

        # Guardamos la paleta para que los diálogos modales la usen
        TEMA_ACTUAL.update({
            "bg": bg_main,
            "fg": fg_primary,
            "btn": btn_bg,
            "btn_hover": btn_hover,
            "accent": accent,
            "barra": barra_bg,
            "barra_hover": barra_hover,
            "barra_borde": barra_borde,
            "btn_accion": btn_accion_bg,
            "btn_accion_hover": btn_accion_hover,
            "btn_accion_borde": btn_accion_borde,
        })

        # Aplicación de los colores a cada componente
        app.config(bg=bg_main)
        barra_menus.config(bg=barra_bg)
        linea_menus.config(bg=barra_borde)
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
        for frame in frames_botones:
            frame.config(bg=btn_accion_borde)
        for btn in botones:
            btn.config(
                bg=btn_accion_bg, fg=fg_primary,
                activebackground=btn_accion_hover, activeforeground=fg_primary,
            )

        for btn_menu in (btn_modo_auto, btn_menu_mas, btn_menu_acerca, btn_menu_ayuda):
            btn_menu.config(
                bg=barra_bg, fg=fg_primary,
                activebackground=barra_hover, activeforeground=fg_primary,
            )

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
    logo_frame = tk.Frame(app, pady=20)
    logo_frame.pack(fill="x")

    # Contenedor del icono/logo
    lbl_logo_icon = tk.Label(logo_frame)
    lbl_logo_icon.pack()
    
    lbl_logo_text = tk.Label(logo_frame, text=f"T O O L S 4 M E W - {VERSION}", font=("Segoe UI", 22, "bold"))
    lbl_logo_text.pack()


    # Contenedor para los botones
    container = tk.Frame(app)
    container.pack(fill="both", expand=True, padx=40)

    botones = []
    frames_botones = []

    # Función auxiliar para crear botones con un estilo unificado y tooltip
    def crear_boton_moderno(texto, comando, descripcion, icono):
        frame_btn = tk.Frame(container, bg="#0f172a") 
        frame_btn.pack(fill="x", pady=3)
        frames_botones.append(frame_btn)
        
        full_text = f"  {icono}   {texto}"
        btn = tk.Button(frame_btn, text=full_text, font=("Segoe UI Semibold", 14),
                       anchor="w", padx=20, pady=8,
                       relief="flat", bd=0, highlightthickness=0,
                       cursor="hand2", command=comando)
        btn.pack(fill="x", padx=1, pady=1)
        botones.append(btn)
        Tooltip(btn, descripcion) # Asigna la ayuda flotante

    # --- DEFINICIÓN DE BOTONES ---
    crear_boton_moderno("Actualizar Todo el Software", actualizar_winget, "Actualiza las aplicaciones instaladas con Winget.", "📦")
    crear_boton_moderno("Abrir Windows Update", abrir_windows_update, "Abre Configuración > Windows Update.\nNo instala actualizaciones automáticamente.", "🔄")
    crear_boton_moderno("Limpiar Sistema", limpiar_sistema, "Limpieza rápida o completa. Puedes incluir la papelera de reciclaje.", "🧹")
    crear_boton_moderno("Diagnóstico", diagnostico, "Comprueba Windows, los discos y Defender sin modificar nada.", "🩺")
    crear_boton_moderno("Reparar Windows", reparar_windows, "Ejecuta DISM /RestoreHealth y SFC /scannow.", "🛠")

    # --- PIE: TEMA ---
    btn_tema = tk.Button(app, font=("Segoe UI", 12, "bold"), relief="raised", cursor="hand2", command=alternar_tema)
    btn_tema.pack(pady=12)

    # Iniciar la interfaz con el tema configurado
    aplicar_tema()
    app.mainloop()

except Exception as e:
    # Captura cualquier error de inicio (como falta de fuentes o permisos) para que no se cierre sin avisar
    logging.exception("Error crítico al iniciar la aplicación")
    root_err = tk.Tk()
    root_err.withdraw()
    messagebox.showerror("Error Crítico", f"Se produjo un error al iniciar la aplicación:\n\n{e}")