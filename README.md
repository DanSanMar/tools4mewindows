# T4MW - Utility Suite ⚡
### Herramienta de mantenimiento integral para Windows (All4me Windows)

**T4MW (Tools4me Windows)** es una suite de mantenimiento ligera y potente escrita en Python. Está diseñada para centralizar las tareas de optimización más comunes de Windows en una interfaz gráfica moderna, intuitiva y fácil de usar, eliminando la necesidad de recordar comandos complejos de la terminal.

![Versión](https://img.shields.io/badge/Versión-1.5-blue)
![Python](https://img.shields.io/badge/Python-3.x-green)
![OS](https://img.shields.io/badge/OS-Windows-informational)

---

## ✨ Características principales

El script integra las herramientas más eficaces de diagnóstico y limpieza de Windows:

* **📦 Actualizar Todo el Software**: Utiliza el gestor `Winget` para buscar y aplicar actualizaciones de todas tus aplicaciones instaladas de forma masiva.
* **🧹 Limpiar Archivos Basura**: Elimina archivos temporales del usuario/sistema y limpia la caché DNS para resolver problemas de red.
* **🛠 Reparar Archivos del Sistema**: Ejecuta el comando `SFC /scannow` para verificar la integridad de los archivos de Windows.
* **♻️ Eliminar Residuos de Update**: Usa `DISM` para limpiar versiones antiguas y redundantes de Windows Update, liberando gigabytes de espacio.
* **🩺 Restaurar Imagen de Sistema**: Repara errores graves del sistema comparando tu instalación local con la imagen oficial de Microsoft.
* **🚀 Optimizar Memoria RAM**: Fuerza el recolector de basura del sistema para liberar memoria retenida innecesariamente.
* **🔄 Reiniciar Windows Explorer**: Refresca la barra de tareas y el escritorio de forma rápida si la interfaz se queda congelada.

---

## 🎨 Interfaz Personalizable
T4MW incluye un **sistema de temas dinámico**:
- **Modo Oscuro**: Para reducir la fatiga visual (estética Slate/Azul).
- **Modo Claro**: Interfaz limpia y profesional.
- **Tooltips Informativos**: Cada botón muestra una breve explicación de lo que hace al pasar el ratón.

---

## 🚀 Requisitos e Instalación

### Requisitos previos
- **Sistema Operativo**: Windows 10 u 11.
- **Python**: Tener instalado [Python 3.x](https://www.python.org/).
- **Permisos**: El script requiere privilegios de **Administrador** (el propio programa solicitará el permiso UAC al iniciarse).

### Instalación
1. Clona este repositorio:
   ```bash
   git clone [https://github.com/DanSanMar/tools4mewindows.git](https://github.com/DanSanMar/tools4mewindows.git)
   Entra en el directorio:

### 🚀 Instalación y Ejecución

```bash
cd tools4mewindows
python t4mw.py```

🛠️ Tecnologías Utilizadas
Componente	Tecnología
Lenguaje	Python
Interfaz Gráfica	Tkinter
Llamadas de Sistema	Librería ctypes y os para ejecución de comandos CMD y PowerShell
⚠️ Nota de Seguridad
Este script ejecuta comandos que modifican archivos del sistema y registros de actualización. Se recomienda:

✅ Cerrar aplicaciones importantes antes de usar las herramientas de limpieza.
⏱️ Tener paciencia durante los procesos de SFC y DISM, ya que pueden tardar varios minutos.
⚖️ Responsabilidad: El autor no se hace responsable de un uso indebido de las herramientas.
👤 Autor
Desarrollado por DanSanMar.

GitHub: @DanSanMar
Repositorio: tools4mewindows
