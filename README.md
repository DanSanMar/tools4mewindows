# T4MW - Utility Suite ⚡
### Herramienta de mantenimiento integral para Windows (All4me Windows)

**T4MW (Tools4me Windows)** es una suite de mantenimiento ligera y potente escrita en Python. Está diseñada para centralizar las tareas de optimización más comunes de Windows en una interfaz gráfica moderna, intuitiva y fácil de usar, eliminando la necesidad de recordar comandos complejos de la terminal.

![Versión](https://img.shields.io/badge/Versi%C3%B3n-V.2-blue)
![Python](https://img.shields.io/badge/Python-3.x-green)
![OS](https://img.shields.io/badge/OS-Windows-informational)
![Licencia](https://img.shields.io/badge/Licencia-MIT-yellow)

---

## ✨ Características principales

El script integra las herramientas más eficaces de diagnóstico y limpieza de Windows:

* **📦 Actualizar todo el software**: usa el gestor `winget` para buscar y aplicar actualizaciones de todas tus aplicaciones instaladas de forma masiva.
* **🧹 Limpiar archivos basura**: elimina archivos temporales del usuario y del sistema, y limpia la caché DNS para resolver problemas de red.
* **🛠 Reparar archivos del sistema**: ejecuta `sfc /scannow` para verificar la integridad de los archivos de Windows.
* **♻️ Eliminar residuos de Update**: usa `DISM` para limpiar versiones antiguas y redundantes de Windows Update, liberando gigabytes de espacio.
* **🩺 Restaurar imagen de sistema**: repara errores graves del sistema comparando tu instalación local con la imagen oficial de Microsoft.
* **🚀 Optimizar memoria RAM**: fuerza el recolector de basura del sistema para liberar memoria retenida innecesariamente.
* **🔄 Reiniciar Windows Explorer**: refresca la barra de tareas y el escritorio de forma rápida si la interfaz se queda congelada.

Las acciones largas o destructivas (limpieza, SFC, DISM y reinicio del Explorador) piden confirmación antes de ejecutarse. Si `winget` no está disponible, la aplicación avisa en lugar de fallar.

---

## 🎨 Interfaz personalizable

T4MW incluye un **sistema de temas dinámico**:

- **Modo oscuro**: para reducir la fatiga visual (estética slate/azul).
- **Modo claro**: interfaz limpia y profesional.
- **Tooltips informativos**: cada botón muestra una breve explicación de lo que hace al pasar el ratón.

---

## 🚀 Requisitos e instalación

### Requisitos previos

- **Sistema operativo**: Windows 10 u 11.
- **Python**: [Python 3.8 o superior](https://www.python.org/).
- **Permisos**: el script requiere privilegios de **Administrador** (el propio programa solicitará el permiso UAC al iniciarse).
- **Dependencias**: Pillow para cargar el logo. Se instala sola si falta, pero conviene instalarla antes.

### Instalación

```bash
git clone https://github.com/DanSanMar/tools4mewindows.git
cd tools4mewindows
pip install -r requirements.txt
python t4mw.py
```

`requirements.txt` incluye Pillow y PyInstaller; este último solo es necesario para compilar el `.exe`.

---

## 📦 Compilar a `.exe`

El método recomendado usa la especificación incluida, que embebe el logo y asigna el icono:

```bash
pyinstaller Tools4MeW.spec
```

El ejecutable aparece en `dist/Tools4MeW.exe`. Para el método manual y la solución de problemas, consulta [CONVERTIR_A_EXE.md](CONVERTIR_A_EXE.md).

---

## 🩺 Registro (log)

La actividad se registra en `%TEMP%\t4mw.log`. Es útil cuando se ejecuta el `.exe` y no queda claro por qué falló un comando.

---

## ⚠️ Nota de seguridad

Este script ejecuta comandos que modifican archivos del sistema y registros de actualización. Se recomienda:

- ✅ Cerrar aplicaciones importantes antes de usar las herramientas de limpieza.
- ⏱️ Tener paciencia durante los procesos de SFC y DISM, ya que pueden tardar varios minutos.
- ⚖️ **Responsabilidad**: el autor no se hace responsable de un uso indebido de las herramientas.

---

## 👤 Autor

Desarrollado por **DanSanMar**.

- GitHub: [@DanSanMar](https://github.com/DanSanMar)
- Repositorio: [tools4mewindows](https://github.com/DanSanMar/tools4mewindows)

---

## 📄 Licencia

Este proyecto se distribuye bajo la licencia **MIT**. Consulta [LICENSE](LICENSE).
