# Pruebas de T4MW V.5.1

Checklist para validar la versión **V.5.1** en Windows 10/11 antes de compilar y distribuir el `.exe`.

Marca cada casilla cuando el resultado coincida con lo esperado. Si algo falla, anota el paso, el mensaje y la hora para revisar `%TEMP%\t4mw.log`.

## Preparación

- [ ] `git pull origin main`
- [ ] `pip install -r requirements.txt`
- [ ] Probar primero en **modo normal** y después en **modo administrador**.
- [ ] Cerrar aplicaciones importantes antes de las pruebas de limpieza.
- [ ] No ejecutar dos acciones largas a la vez; esperar a que termine cada consola.
- [ ] Anotar la hora de inicio para localizar la sesión en el log.

## 1. Arranque, modos y menú

- [ ] Ejecutar `python t4mw.py` sin administrador: **no debe aparecer UAC** y la ventana debe abrirse directamente.
- [ ] Bajo el título aparece el chip `● Modo normal` y, debajo, `UAC solo al usar acciones que lo requieren`.
- [ ] El título de la ventana muestra `T4MW - All4me Group (V.5.1)`.
- [ ] La cabecera muestra `T O O L S 4 M E W` y debajo `Versión V.5.1`.
- [ ] Se ven el icono y el logo.
- [ ] El menú principal tiene exactamente cinco botones: **Actualizar Todo el Software**, **Abrir Windows Update**, **Limpiar Sistema**, **Diagnóstico** y **Reparar Windows**.
- [ ] No aparecen las acciones antiguas de RAM ni de reiniciar Explorer.
- [ ] La barra superior ocupa todo el ancho y muestra cinco pestañas iguales: **Modo auto**, **Sistema**, **Más herramientas**, **Acerca de T4MW** y **Ayuda**, con **Ayuda** en el extremo derecho.
- [ ] Las pestañas tienen fondo azul suave y una línea inferior de acento; el texto se lee bien.
- [ ] **Sistema** contiene Administrador de tareas, Servicios, Monitor de recursos y Visor de eventos.
- [ ] **Más herramientas** contiene punto de restauración, análisis de Defender, Administrador de dispositivos, Administración de discos y Programador de tareas.
- [ ] **Ayuda** contiene **Cómo funcionan los modos**, Abrir log y Ayuda de Windows.
- [ ] No hay botón inferior de herramientas.
- [ ] El pie muestra los botones redondeados **CAMBIAR A MODO ADMINISTRADOR**, **ℹ️ MODOS** y **MODO OSCURO**, sin recortes.
- [ ] Pulsar **ℹ️ MODOS** y **Ayuda → Cómo funcionan los modos**: explican la diferencia entre los dos modos.
- [ ] La ventana muestra los cinco botones, las cinco pestañas y el pie sin recortes.
- [ ] Los cinco botones tienen esquinas redondeadas, fondo azul suave y borde fino, sin que el texto pierda legibilidad.
- [ ] Al pasar el ratón por un botón cambia el tono y aparece un tooltip redondeado con la explicación.
- [ ] En Windows 11, la ventana y los diálogos muestran esquinas redondeadas y la barra de título sigue al tema. En Windows 10 se ve el estilo clásico sin errores.
- [ ] Cambiar entre modo claro y oscuro: las pestañas pasan a azul oscuro suave y los botones mantienen el contraste; no deben quedar marcos oscuros ni esquinas del color del contenedor en modo claro.
- [ ] Abrir los diálogos de **Limpiar Sistema**, **Modo auto** y **Acerca de T4MW** en modo oscuro y en modo claro: deben usar los colores del tema.
- [ ] Cerrar y volver a abrir la aplicación.

### Cambio a modo administrador

- [ ] Pulsar **CAMBIAR A MODO ADMINISTRADOR**: pide confirmación y después UAC.
- [ ] Aceptar el UAC: T4MW se cierra y vuelve a abrirse con el chip `● Administrador` en verde y el botón pasa a **VOLVER A MODO NORMAL**.
- [ ] Al pulsar **Diagnóstico** en modo administrador **no** aparece aviso de UAC.
- [ ] Pulsar **VOLVER A MODO NORMAL**: se reinicia sin privilegios y vuelve a mostrar el chip `● Modo normal`.
- [ ] Cancelar el UAC al cambiar de modo: aparece el aviso **Permisos cancelados** y T4MW sigue abierto en el modo anterior.

## 2. Actualizar todo el software

- [ ] Pulsar **Actualizar Todo el Software**: se abre una consola nueva.
- [ ] En modo normal, abrir la consola **no** pide UAC; durante la actualización puede pedirse UAC por cada instalador que lo requiera.
- [ ] La consola muestra el banner `### Tools4meW - V.5.1 ###`.
- [ ] Se ejecuta `winget upgrade --all ...` y lista las actualizaciones disponibles.
- [ ] Al terminar, la consola se queda en `pause`.
- [ ] El comando aparece en `%TEMP%\t4mw.log`.
- [ ] Probar en un equipo sin *App Installer* o sin `winget` en el PATH: debe salir el diálogo **Winget no disponible**, no una consola rota.
- [ ] Pulsar **Abrir Windows Update**: abre la página de Windows Update en Configuración. No debe ejecutar `winget` ni modificar nada.

## 3. Limpieza rápida

- [ ] Pulsar **Limpiar Sistema**: aparece un diálogo con **Limpieza rápida**, **Limpieza completa**, la casilla **Incluir papelera de reciclaje** y **Cancelar**.
- [ ] La casilla de la papelera está desmarcada por defecto.
- [ ] Pulsar **Cancelar** o cerrar el diálogo con Escape: no se ejecuta nada.
- [ ] Elegir **Limpieza rápida** sin marcar la papelera: se abre una consola sin pedir UAC.
- [ ] En modo normal la consola tiene **un solo paso**: limpia los temporales del usuario.
- [ ] En modo administrador la consola tiene **tres pasos**: temporales del usuario, temporales de Windows y `ipconfig /flushdns`.
- [ ] Los archivos en uso se omiten sin romper la consola.
- [ ] El log `%TEMP%\t4mw.log` sigue existiendo después de la limpieza.
- [ ] Los pasos aparecen en el log.

### Limpieza con papelera (opcional)

- [ ] Envía un archivo de prueba a la papelera. No uses archivos personales.
- [ ] Abre **Limpiar Sistema**, marca **Incluir papelera de reciclaje** y elige **Limpieza rápida**.
- [ ] El diálogo muestra el aviso de que el borrado es permanente.
- [ ] La consola muestra un cuarto paso, `Vaciando papelera de reciclaje`, y la papelera queda vacía.
- [ ] La consola muestra `Papelera vaciada.` o un aviso legible si la papelera ya estaba vacía.
- [ ] Al volver a abrir el diálogo, la casilla vuelve a estar desmarcada.
- [ ] La acción de papelera queda registrada en el log.

## 4. Limpieza completa

- [ ] Pulsar **Limpiar Sistema** → **Limpieza completa** sin marcar la papelera.
- [ ] En modo normal, antes de abrir la consola aparece la confirmación **Permisos de administrador** y después el UAC.
- [ ] La consola muestra cuatro pasos e incluye `dism /online /cleanup-image /startcomponentcleanup`.
- [ ] La consola permanece abierta al terminar, aunque DISM tarde.
- [ ] Los pasos aparecen en el log.
- [ ] Antes de la limpieza, envía un archivo de prueba a la papelera.
- [ ] Comprobar que no se ha vaciado la papelera de reciclaje ni se han tocado documentos personales.

## 5. Diagnóstico

- [ ] Pulsar **Diagnóstico**: aparece un diálogo con **Diagnóstico rápido**, **Diagnóstico completo** y **Cancelar**.
- [ ] Pulsar **Cancelar** o cerrar el diálogo con Escape: no se ejecuta nada.
- [ ] En modo normal, al elegir un diagnóstico aparece la confirmación **Permisos de administrador** y después el UAC; en modo administrador se abre directamente.
- [ ] **Diagnóstico rápido**: ejecuta `DISM /CheckHealth`, consulta discos/espacio y estado de Defender.
- [ ] **Diagnóstico completo**: añade `DISM /AnalyzeComponentStore` y `chkdsk C: /scan`.
- [ ] La salida es legible y la consola queda en `pause`.
- [ ] El diagnóstico no modifica nada y no pide reinicio.
- [ ] Los pasos aparecen en el log.

## 6. Reparar Windows

- [ ] Pulsar **Reparar Windows**: aparece una confirmación con el aviso de duración.
- [ ] El botón predeterminado de la confirmación es **No**: pulsar Enter no ejecuta la reparación.
- [ ] Pulsar **No**: no se ejecuta nada.
- [ ] Aceptar: se ejecuta primero `DISM /Online /Cleanup-Image /RestoreHealth` y después `SFC /scannow`.
- [ ] En modo normal, tras aceptar la confirmación aparece el aviso de UAC para elevar solo esta reparación.
- [ ] La interfaz no se congela y la consola permanece abierta al terminar.
- [ ] Los dos comandos aparecen en el log.

## 7. Modo auto

- [ ] Pulsar **Modo auto** (barra superior): aparece un diálogo con las casillas **Actualizar software con Winget**, **Limpieza rápida** y **Diagnóstico rápido** marcadas por defecto.
- [ ] En modo normal la casilla de limpieza dice **Limpieza rápida (temporales del usuario)**; en modo administrador, **(temporales y DNS)**.
- [ ] El diálogo avisa de que no incluye reparación, papelera, limpieza completa ni diagnóstico completo.
- [ ] Pulsar **Cancelar** o cerrar con Escape: no se ejecuta nada.
- [ ] Desmarcar las tres casillas y pulsar **Ejecutar modo automático**: muestra un aviso y no abre ninguna consola.
- [ ] Con las tres casillas marcadas, ejecutar: se abre **una sola consola** con siete pasos en este orden: Winget, tres de limpieza y tres de diagnóstico rápido.
- [ ] En modo normal, esa ejecución pide UAC una vez antes de abrir la consola.
- [ ] La consola muestra el banner `### Tools4meW - V.5.1 ###` y termina en `pause`.
- [ ] El modo auto no vacía la papelera, no ejecuta `DISM /StartComponentCleanup` ni repara Windows.
- [ ] Desmarcar **Actualizar software** y ejecutar: la consola no llama a `winget` y mantiene el orden limpieza → diagnóstico.
- [ ] En modo normal, dejar solo **Limpieza rápida** y ejecutar: un único paso, sin UAC.
- [ ] En modo administrador, dejar solo **Limpieza rápida** y ejecutar: tres pasos, sin UAC.
- [ ] En un equipo sin `winget`, dejar marcada la actualización y ejecutar: muestra **Winget no disponible** y no abre la consola.
- [ ] En ese mismo equipo, desmarcar la actualización y ejecutar limpieza + diagnóstico: funciona sin `winget`.
- [ ] El log registra las tareas seleccionadas, el título `Mantenimiento automatico` y cada paso.

## 8. Sistema, Más herramientas, Acerca de y Ayuda

- [ ] **Sistema → Administrador de tareas**: abre el Administrador de tareas de Windows.
- [ ] **Sistema → Servicios**: abre la consola de Servicios con permisos de administrador.
- [ ] **Sistema → Monitor de recursos / Visor de eventos**: abre cada herramienta integrada.
- [ ] **Más herramientas → Crear punto de restauración**: pide confirmación, después UAC en modo normal, y ejecuta `Checkpoint-Computer`. Si la Protección del sistema está desactivada, muestra el error en la consola sin cerrarla.
- [ ] **Más herramientas → Análisis rápido de Defender**: pide confirmación, después UAC en modo normal, actualiza firmas y lanza un análisis rápido. Si hay otro antivirus, muestra el error en la consola.
- [ ] **Más herramientas → Administrador de dispositivos / Administración de discos / Programador de tareas**: abre cada herramienta integrada.
- [ ] Si alguna herramienta no está disponible, muestra un error legible y T4MW sigue abierto.
- [ ] **Acerca de T4MW** (barra superior): muestra la versión V.5.1, el autor, la licencia MIT y los botones **Abrir repositorio** y **Abrir perfil de GitHub**.
- [ ] **Abrir repositorio** abre `https://github.com/DanSanMar/tools4mewindows` en el navegador.
- [ ] **Abrir perfil de GitHub** abre `https://github.com/DanSanMar` en el navegador.
- [ ] **Ayuda → Abrir log**: abre `%TEMP%\t4mw.log` en el editor predeterminado.
- [ ] Si el log no existe, muestra un aviso en lugar de fallar.
- [ ] **Ayuda → Ayuda de Windows**: abre el navegador en la página de ayuda de Windows.

## 9. Log

- [ ] `%TEMP%\t4mw.log` contiene `Iniciando T4MW V.5.1`.
- [ ] Contiene `Ejecutando en modo normal en ...` o `Ejecutando en modo administrador en ...`.
- [ ] Contiene una línea `Ejecutando: ... (requiere_admin=..., modo_admin=...)` por cada secuencia y una línea por cada paso.
- [ ] Contiene `Consola lanzada: ...` o `Consola elevada lanzada: ...` con la ruta del `.bat` temporal.
- [ ] Las herramientas de **Sistema** y **Más herramientas** dejan una línea `Abriendo ...` en el log.

## 10. Compilación y `.exe`

- [ ] `pyinstaller Tools4MeW.spec` termina sin errores.
- [ ] `dist\Tools4MeW.exe` arranca en un Windows sin Python instalado.
- [ ] El `.exe` **no pide UAC al abrirse**: arranca en modo normal, muestra el logo de cabecera, el icono de la ventana y la versión V.5.1.
- [ ] En el `.exe`, **CAMBIAR A MODO ADMINISTRADOR** reinicia elevado y **VOLVER A MODO NORMAL** vuelve a abrir sin privilegios.
- [ ] Al usar **Diagnóstico** en modo normal, el `.exe` pide UAC y lanza la consola elevada.
- [ ] Los `.bat` temporales se crean en una carpeta propia (`%PUBLIC%\T4MW` o `%LOCALAPPDATA%\T4MW`) y se borran al terminar la consola.
- [ ] El archivo `Tools4MeW.exe` muestra el icono personalizado en el Explorador.
- [ ] Los cinco botones, los diálogos de modo, el Modo auto, las pestañas **Sistema** y **Más herramientas**, la barra superior y los menús funcionan igual que con Python.
- [ ] La limpieza rápida no rompe el `.exe` desinstalado: el directorio `_MEI*` de PyInstaller se conserva.
- [ ] El `.exe` no intenta instalar Pillow con `pip` si falta la dependencia.

## Registro de resultados

| Fecha | Equipo | Resultado | Notas |
|-------|--------|-----------|-------|
| 2026-10-27 | Windows de pruebas | Correcto | `.exe` compilado con `pyinstaller Tools4MeW.spec` y probado sin Python; arranque, interfaz, pestañas y menús correctos. |
