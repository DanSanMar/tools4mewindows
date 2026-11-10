# T4MW - Utility Suite ⚡
### Herramienta de mantenimiento integral para Windows (All4me Windows)

**T4MW (Tools4me Windows)** es una suite de mantenimiento ligera y potente escrita en Python. Está diseñada para centralizar las tareas de optimización más comunes de Windows en una interfaz gráfica moderna, intuitiva y fácil de usar, eliminando la necesidad de recordar comandos complejos de la terminal.

![Versión](https://img.shields.io/badge/Versi%C3%B3n-V.5.1-blue)
![Python](https://img.shields.io/badge/Python-3.x-green)
![OS](https://img.shields.io/badge/OS-Windows-informational)
![Licencia](https://img.shields.io/badge/Licencia-MIT-yellow)

---

## ✨ Características principales

El menú principal tiene cinco acciones claras:

* **📦 Actualizar todo el software**: usa el gestor `winget` para buscar y aplicar actualizaciones de todas tus aplicaciones instaladas de forma masiva.
* **🔄 Abrir Windows Update**: abre la página de Windows Update en Configuración. `winget` actualiza aplicaciones, no Windows.
* **🧹 Limpiar sistema**: dos modos. La **rápida** borra temporales del usuario y, en modo administrador, también los de Windows y la caché DNS. La **completa** añade la limpieza de componentes de Windows con `DISM`. La papelera de reciclaje se puede incluir como opción; si se marca, el borrado es permanente.
* **🩺 Diagnóstico**: solo lectura. Comprueba la imagen de Windows, los discos y Defender; el modo completo añade análisis del almacén de componentes y `chkdsk`.
* **🛠 Reparar Windows**: ejecuta `DISM /RestoreHealth` y después `SFC /scannow` en una sola consola.

La barra superior ocupa todo el ancho y contiene cinco pestañas con fondo azul claro:

- **Modo auto**: ejecuta en una sola consola la actualización con `winget`, la limpieza rápida y el diagnóstico rápido. Puedes marcar o desmarcar cada tarea; no incluye reparación, papelera, limpieza completa ni diagnóstico completo.
- **Sistema**: abre el Administrador de tareas, Servicios, Monitor de recursos y Visor de eventos.
- **Más herramientas**: crear un punto de restauración, análisis rápido con Windows Defender, Administrador de dispositivos, Administración de discos y Programador de tareas.
- **Acerca de T4MW**: versión, autor, repositorio, perfil de GitHub y licencia.
- **Ayuda**: explicación de los modos de ejecución, abrir el log y abrir la ayuda de Windows.

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

## 🎛️ Modos de ejecución (V.5.1)

T4MW arranca en **modo normal** y solo pide permisos de administrador cuando hacen falta. La aplicación muestra el modo actual bajo el título y lo registra en el log.

### Modo normal (por defecto)

- La aplicación se abre **sin UAC**.
- **Actualizar todo el software** funciona sin elevar la aplicación: Windows pedirá UAC solo por cada instalador que lo requiera, y el resto se actualizará sin avisos.
- **Limpiar sistema → rápida** borra únicamente los temporales de tu usuario.
- **Reparar Windows**, **Diagnóstico**, **Más herramientas → punto de restauración**, **análisis de Defender** y la **limpieza completa** piden UAC solo al pulsarlos.
- Si el **Modo auto** incluye el diagnóstico, se pide UAC una vez y la limpieza aprovecha esos permisos.

### Modo administrador

- El botón **CAMBIAR A MODO ADMINISTRADOR** reinicia T4MW solicitando UAC una sola vez.
- Todas las herramientas funcionan sin avisos adicionales.
- La limpieza rápida incluye los temporales de Windows y la caché DNS.
- Recomendado para reparaciones profundas (**SFC**, **DISM**) y para la limpieza completa.

### Cómo cambiar de modo

Usa los botones del pie de la ventana:

- **CAMBIAR A MODO ADMINISTRADOR** / **VOLVER A MODO NORMAL**: relanza la aplicación con el modo elegido. Al volver al modo normal, T4MW se reinicia sin privilegios usando `explorer.exe`; si Windows no lo permite, ciérralo y ábrelo de nuevo normalmente.
- **ℹ️ MODOS** y **Ayuda → Cómo funcionan los modos**: muestran esta misma explicación dentro de la aplicación.

> **Nota:** si abres T4MW con «Ejecutar como administrador», arrancará directamente en modo administrador.

---

## 🎨 Interfaz personalizable

T4MW incluye un **sistema de temas dinámico**:

- **Modo oscuro**: paleta oscura suave, sin azules saturados, para reducir la fatiga visual.
- **Modo claro**: fondo blanco roto y azules suaves, con aspecto limpio y actual.
- **Botones redondeados**: las acciones principales se dibujan con esquinas suaves y un borde fino, con efecto de resaltado al pasar el ratón.
- **Chip de modo**: bajo la versión se muestra el modo actual con un punto de color (azul en modo normal, verde en administrador).
- **Ventana redondeada**: en Windows 11 la ventana y los diálogos usan esquinas redondeadas y la barra de título sigue al tema claro u oscuro. En Windows 10 se mantiene el estilo del sistema.
- **Tooltips informativos**: cada botón muestra una breve explicación de lo que hace al pasar el ratón.
- **Barra superior de ancho completo**: cinco pestañas iguales con fondo azul suave y línea inferior de acento.

---

## 🚀 Requisitos e instalación

### Requisitos previos

- **Sistema operativo**: Windows 10 u 11.
- **Python**: [Python 3.8 o superior](https://www.python.org/).
- **Permisos**: no se requieren privilegios de administrador al iniciar. Se solicitan bajo demanda o al activar el **modo administrador** desde el pie de la ventana.
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

## 🆕 Novedades V.5.1

- Nueva estética: botones y chips con **esquinas redondeadas** y paleta más suave.
- **Ventana y diálogos redondeados** en Windows 11, con barra de título acorde al tema.
- Cabecera reorganizada: título, **versión** y **chip del modo** con indicador de color.
- Tooltips rediseñados y con esquinas suaves.
- Sin cambios de funcionamiento: mismos comandos, modos y confirmaciones que en V.5.

### Novedades V.5

- Arranque en **modo normal** sin UAC automático.
- Nuevo **selector de modo** en el pie: administrador ↔ normal.
- **Elevación bajo demanda**: cada tarea administrativa pide UAC solo al usarse.
- `winget` sigue funcionando en modo normal, con UAC por aplicación cuando corresponde.
- Limpieza adaptada al modo: temporales del usuario en normal; completa en administrador.
- Explicación de los modos integrada en **ℹ️ MODOS** y en **Ayuda**.
- Los lanzadores se ejecutan desde `.bat` temporales propios y se borran al terminar.
- Versión unificada en **V.5**.

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
- 🧹 La limpieza de temporales no toca documentos personales. En modo normal solo borra los temporales de tu usuario; la papelera solo se vacía si marcas la opción **Incluir papelera de reciclaje** en el diálogo de limpieza, y esa acción es irreversible.
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
