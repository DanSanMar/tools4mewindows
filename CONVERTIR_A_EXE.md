# Convertir T4MW a `.exe`

Este documento explica cómo transformar `t4mw.py` en un ejecutable independiente para Windows, de modo que puedas compartirlo y usarlo sin necesidad de tener Python instalado en el equipo destino.

## ⚠️ Requisitos previos

Antes de comenzar, asegúrate de tener:

1. **Windows 10 u 11**. El ejecutable debe compilarse en Windows: PyInstaller no genera `.exe` desde Linux o macOS, y el script llama a herramientas del sistema (`winget`, `sfc`, `dism`, `powershell`).
2. **Python 3.8 o superior**.
3. **Git** (opcional, para clonar el repositorio).

---

## 📋 Paso 1: Preparar el entorno

1. Clona el repositorio (o descarga el código):

   ```bash
   git clone https://github.com/DanSanMar/tools4mewindows.git
   cd tools4mewindows
   ```

2. Instala las dependencias:

   ```bash
   pip install -r requirements.txt
   ```

   Esto instala **Pillow** (para manejar la imagen) y **PyInstaller** (para compilar). Aunque el script intenta instalar Pillow automáticamente, conviene hacerlo antes de compilar para asegurar que la dependencia quede incluida en el ejecutable.

---

## 📦 Paso 2: Comprobar los recursos

El proyecto incluye dos recursos que deben estar en la raíz:

- `LogoALL4meW.png`: imagen de la cabecera de la interfaz.
- `LogoALL4meW.ico`: icono del ejecutable.

La especificación `Tools4MeW.spec` ya se encarga de embeber el PNG y de asignar el icono.

---

## 🚀 Paso 3: Compilar

### Método recomendado: usar la especificación

Desde la carpeta del proyecto:

```bash
pyinstaller Tools4MeW.spec
```

La especificación genera un ejecutable único (`--onefile`), con el icono personalizado, el PNG embebido y `console=True`. Mantener la consola es intencionado: ahí se ve el progreso de SFC y DISM.

### Método manual

Si prefieres no usar la especificación:

```bash
pyinstaller --onefile --name "Tools4MeW" --icon "LogoALL4meW.ico" --add-data "LogoALL4meW.png;." t4mw.py
```

Si el comando falla, prueba la variante con módulo:

```bash
python -m PyInstaller --onefile --name "Tools4MeW" --icon "LogoALL4meW.ico" --add-data "LogoALL4meW.png;." t4mw.py
```

Notas:

- En Windows, el separador de `--add-data` es `;`. En Linux/macOS sería `:`.
- Si añades `--noconsole` o `--windowed`, el ejecutable no mostrará la salida de SFC/DISM. El log seguirá escribiéndose en `%TEMP%\t4mw.log`.

---

## 📂 Paso 4: Obtener el ejecutable

Una vez finalizado el proceso (puede tardar unos minutos):

- Ve a la carpeta `dist`.
- Encontrarás `Tools4MeW.exe`.
- Haz doble clic para probarlo.

**Nota importante:** el script incluye una comprobación de administrador. Al ejecutar el `.exe`, Windows pedirá permiso de administrador (UAC). Acéptalo para que SFC, DISM y el resto de herramientas funcionen correctamente.

---

## 🔧 Solución de problemas

| Problema | Solución |
|----------|----------|
| `No module named 'PIL'` | Ejecuta `pip install -r requirements.txt` antes de compilar. |
| La imagen no carga en el `.exe` | Usa `Tools4MeW.spec` o añade `--add-data "LogoALL4meW.png;."` al comando manual. |
| El antivirus bloquea el `.exe` | Es habitual que marque como falso positivo herramientas que ejecutan comandos del sistema. Añade una exclusión temporal para probar. |
| El script pide permisos de administrador | Es intencionado: se reinicia con privilegios elevados si no se ejecuta como admin. |
| No se ve la salida de SFC o DISM | Compila con `console=True` (la especificación ya lo hace) o revisa `%TEMP%\t4mw.log`. |
| `winget` no se reconoce | Actualiza **App Installer** desde Microsoft Store. |

---

## 🩺 Log

T4MW escribe su actividad en `%TEMP%\t4mw.log`. Si algo falla al ejecutar el `.exe`, revisa ese archivo antes de abrir una incidencia.

---

Generado para el proyecto **Tools4MeW - All4me Group**.
