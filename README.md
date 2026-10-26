# T4MW - Utility Suite ⚡
### Herramienta de mantenimiento integral para Windows (All4me Windows)

**T4MW (Tools4me Windows)** es una suite de mantenimiento ligera y potente escrita en Python. Está diseñada para centralizar las tareas de optimización más comunes de Windows en una interfaz gráfica moderna, intuitiva y fácil de usar, eliminando la necesidad de recordar comandos complejos de la terminal.

![Versión](https://img.shields.io/badge/Versi%C3%B3n-V.3-blue)
![Python](https://img.shields.io/badge/Python-3.x-green)
![OS](https://img.shields.io/badge/OS-Windows-informational)
![Licencia](https://img.shields.io/badge/Licencia-MIT-yellow)

---

## ✨ Características principales

El menú principal tiene cinco acciones claras:

* **📦 Actualizar todo el software**: usa el gestor `winget` para buscar y aplicar actualizaciones de todas tus aplicaciones instaladas de forma masiva.
* **🔄 Abrir Windows Update**: abre la página de Windows Update en Configuración. `winget` actualiza aplicaciones, no Windows.
* **🧹 Limpiar sistema**: dos modos. La **rápida** borra temporales del usuario y de Windows y vacía la caché DNS. La **completa** añade la limpieza de componentes de Windows con `DISM`. La papelera de reciclaje se puede incluir como opción; si se marca, el borrado es permanente.
* **🩺 Diagnóstico**: solo lectura. Comprueba la imagen de Windows, los discos y Defender; el modo completo añade análisis del almacén de componentes y `chkdsk`.
* **🛠 Reparar Windows**: ejecuta `DISM /RestoreHealth` y después `SFC /scannow` en una sola consola.

La barra superior, alineada a la derecha, contiene:

- **Modo auto**: ejecuta en una sola consola la actualización con `winget`, la limpieza rápida y el diagnóstico rápido. Puedes marcar o desmarcar cada tarea; no incluye reparación, papelera, limpieza completa ni diagnóstico completo.
- **Más herramientas**: crear un punto de restauración y análisis rápido con Windows Defender.
- **Acerca de T4MW**: versión, autor, repositorio, perfil de GitHub y licencia.
- **Ayuda**: abrir el log y abrir la ayuda de Windows.

Las acciones largas piden confirmación antes de ejecutarse; el **Modo auto** se configura y se lanza desde su propio diálogo. La limpieza y el diagnóstico permiten elegir entre modo rápido y completo. Si `winget` no está disponible, la aplicación avisa en lugar de fallar.

### Tiempos orientativos

| Acción | Tiempo |
|--------|--------|
| Limpieza rápida | 1-2 minutos |
| Limpieza completa | 10-30 minutos |
| Diagnóstico rápido | 1-3 minutos |
| Diagnóstico completo | 5-20 minutos |
| Reparar Windows | 20-60 minutos |
| Actualizar software | Depende de las actualizaciones |
| Modo auto | Depende de la actualización + 2-5 minutos |
| Abrir Windows Update | Inmediato |

---

## 🎨 Interfaz personalizable

T4MW incluye un **sistema de temas dinámico**:

- **Modo oscuro**: para reducir la fatiga visual (estética slate/azul).
- **Modo claro**: interfaz limpia y profesional.
- **Tooltips informativos**: cada botón muestra una breve explicación de lo que hace al pasar el ratón.
- **Barra superior alineada a la derecha**: Modo auto, Más herramientas, Acerca de T4MW y Ayuda.

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

El método recomendado usa la especificación incluida, que embebe el logo y el icono de la ventana, y asigna el icono del ejecutable:

```bash
pyinstaller Tools4MeW.spec
```

El ejecutable aparece en `dist/Tools4MeW.exe`. Para el método manual y la solución de problemas, consulta [CONVERTIR_A_EXE.md](CONVERTIR_A_EXE.md).

---

## 🧪 Pruebas

Antes de compilar o distribuir una versión, sigue la checklist de [PRUEBAS.md](PRUEBAS.md). Recoge el resultado de cada acción y revisa el log si algo falla.

---

## 🩺 Registro (log)

La actividad se registra en `%TEMP%\t4mw.log`. Es útil cuando se ejecuta el `.exe` y no queda claro por qué falló un comando.

---

## ⚠️ Nota de seguridad

Este script ejecuta comandos que modifican archivos del sistema y registros de actualización. Se recomienda:

- ✅ Cerrar aplicaciones importantes antes de usar las herramientas de limpieza.
- 🚦 No ejecutes dos acciones largas a la vez: espera a que termine la consola.
- 💾 Crear un punto de restauración antes de usar **Reparar Windows**.
- ⏱️ Tener paciencia durante SFC, DISM y `chkdsk`; pueden tardar varios minutos y la consola no debe cerrarse.
- 🧹 La limpieza de temporales no toca documentos personales. La papelera solo se vacía si marcas la opción **Incluir papelera de reciclaje** en el diálogo de limpieza; esa acción es irreversible.
- ⚙️ **Modo auto** solo ejecuta actualización con `winget`, limpieza rápida y diagnóstico rápido. No repara Windows, no vacía la papelera y no usa los modos completos.
- ℹ️ La limpieza completa elimina componentes de actualizaciones anteriores y puede impedir desinstalar algunas actualizaciones.
- ⚖️ **Responsabilidad**: el autor no se hace responsable de un uso indebido de las herramientas.

---

## 👤 Autor

Desarrollado por **DanSanMar**.

- GitHub: [@DanSanMar](https://github.com/DanSanMar)
- Repositorio: [tools4mewindows](https://github.com/DanSanMar/tools4mewindows)

---

## 📄 Licencia

Este proyecto se distribuye bajo la licencia **MIT**. Consulta [LICENSE](LICENSE).
