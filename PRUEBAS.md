# Pruebas de T4MW V.4

Checklist para validar la versión **V.4** en Windows 10/11 antes de compilar y distribuir el `.exe`.

Marca cada casilla cuando el resultado coincida con lo esperado. Si algo falla, anota el paso, el mensaje y la hora para revisar `%TEMP%\t4mw.log`.

## Preparación

- [ ] `git pull origin main`
- [ ] `pip install -r requirements.txt`
- [ ] Cerrar aplicaciones importantes antes de las pruebas de limpieza.
- [ ] No ejecutar dos acciones largas a la vez; esperar a que termine cada consola.
- [ ] Anotar la hora de inicio para localizar la sesión en el log.

## 1. Arranque y menú

- [ ] Ejecutar `python t4mw.py` sin administrador: debe aparecer el UAC y relanzarse elevado.
- [ ] Cancelar el UAC: la consola muestra `Error crítico al elevar privilegios` y espera a que pulses Enter; no se queda colgada.
- [ ] El título de la ventana muestra `T4MW - All4me Group (V.4)`.
- [ ] La cabecera muestra `T O O L S 4 M E W - V.4`.
- [ ] Se ven el icono y el logo.
- [ ] El menú principal tiene exactamente cinco botones: **Actualizar Todo el Software**, **Abrir Windows Update**, **Limpiar Sistema**, **Diagnóstico** y **Reparar Windows**.
- [ ] No aparecen las acciones antiguas de RAM ni de reiniciar Explorer.
- [ ] La barra superior ocupa todo el ancho y muestra cuatro pestañas iguales: **Modo auto**, **Más herramientas**, **Acerca de T4MW** y **Ayuda**, con **Ayuda** en el extremo derecho.
- [ ] Las pestañas tienen fondo azul claro y una línea inferior de acento; el texto se lee bien.
- [ ] **Más herramientas** contiene punto de restauración y análisis de Defender.
- [ ] **Ayuda** contiene Abrir log y Ayuda de Windows.
- [ ] No hay botón inferior de herramientas.
- [ ] La ventana muestra los cinco botones, las pestañas y el botón de tema sin recortes.
- [ ] Los cinco botones tienen un fondo azul suave y un borde fino, sin que el texto pierda legibilidad.
- [ ] Cambiar entre modo claro y oscuro: las pestañas pasan a azul oscuro y los botones mantienen el contraste; no deben quedar marcos oscuros en modo claro.
- [ ] Abrir los diálogos de **Limpiar Sistema**, **Modo auto** y **Acerca de T4MW** en modo oscuro y en modo claro: deben usar los colores del tema.
- [ ] Cerrar y volver a abrir la aplicación.

## 2. Actualizar todo el software

- [ ] Pulsar **Actualizar Todo el Software**: se abre una consola nueva.
- [ ] La consola muestra el banner `### Tools4meW - V.4 ###`.
- [ ] Se ejecuta `winget upgrade --all ...` y lista las actualizaciones disponibles.
- [ ] Al terminar, la consola se queda en `pause`.
- [ ] El comando aparece en `%TEMP%\t4mw.log`.
- [ ] Probar en un equipo sin *App Installer* o sin `winget` en el PATH: debe salir el diálogo **Winget no disponible**, no una consola rota.
- [ ] Pulsar **Abrir Windows Update**: abre la página de Windows Update en Configuración. No debe ejecutar `winget` ni modificar nada.

## 3. Limpieza rápida

- [ ] Pulsar **Limpiar Sistema**: aparece un diálogo con **Limpieza rápida**, **Limpieza completa**, la casilla **Incluir papelera de reciclaje** y **Cancelar**.
- [ ] La casilla de la papelera está desmarcada por defecto.
- [ ] Pulsar **Cancelar** o cerrar el diálogo con Escape: no se ejecuta nada.
- [ ] Elegir **Limpieza rápida** sin marcar la papelera: se abre una consola con tres pasos.
- [ ] Se limpian los temporales del usuario y de Windows, y se ejecuta `ipconfig /flushdns`.
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
- [ ] La consola muestra cuatro pasos e incluye `dism /online /cleanup-image /startcomponentcleanup`.
- [ ] La consola permanece abierta al terminar, aunque DISM tarde.
- [ ] Los pasos aparecen en el log.
- [ ] Antes de la limpieza, envía un archivo de prueba a la papelera.
- [ ] Comprobar que no se ha vaciado la papelera de reciclaje ni se han tocado documentos personales.

## 5. Diagnóstico

- [ ] Pulsar **Diagnóstico**: aparece un diálogo con **Diagnóstico rápido**, **Diagnóstico completo** y **Cancelar**.
- [ ] Pulsar **Cancelar** o cerrar el diálogo con Escape: no se ejecuta nada.
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
- [ ] La interfaz no se congela y la consola permanece abierta al terminar.
- [ ] Los dos comandos aparecen en el log.

## 7. Modo auto

- [ ] Pulsar **Modo auto** (barra superior): aparece un diálogo con las casillas **Actualizar software con Winget**, **Limpieza rápida** y **Diagnóstico rápido** marcadas por defecto.
- [ ] El diálogo avisa de que no incluye reparación, papelera, limpieza completa ni diagnóstico completo.
- [ ] Pulsar **Cancelar** o cerrar con Escape: no se ejecuta nada.
- [ ] Desmarcar las tres casillas y pulsar **Ejecutar modo automático**: muestra un aviso y no abre ninguna consola.
- [ ] Con las tres casillas marcadas, ejecutar: se abre **una sola consola** con siete pasos en este orden: Winget, tres de limpieza rápida y tres de diagnóstico rápido.
- [ ] La consola muestra el banner `### Tools4meW - V.4 ###` y termina en `pause`.
- [ ] El modo auto no vacía la papelera, no ejecuta `DISM /StartComponentCleanup` ni repara Windows.
- [ ] Desmarcar **Actualizar software** y ejecutar: la consola no llama a `winget` y mantiene el orden limpieza → diagnóstico.
- [ ] En un equipo sin `winget`, dejar marcada la actualización y ejecutar: muestra **Winget no disponible** y no abre la consola.
- [ ] En ese mismo equipo, desmarcar la actualización y ejecutar limpieza + diagnóstico: funciona sin `winget`.
- [ ] El log registra las tareas seleccionadas, el título `Mantenimiento automatico` y cada paso.

## 8. Más herramientas, Ayuda y Acerca de

- [ ] **Más herramientas → Crear punto de restauración**: pide confirmación y ejecuta `Checkpoint-Computer`. Si la Protección del sistema está desactivada, muestra el error en la consola sin cerrarla.
- [ ] **Más herramientas → Análisis rápido de Defender**: pide confirmación, actualiza firmas y lanza un análisis rápido. Si hay otro antivirus, muestra el error en la consola.
- [ ] **Acerca de T4MW** (barra superior): muestra la versión V.4, el autor, la licencia MIT y los botones **Abrir repositorio** y **Abrir perfil de GitHub**.
- [ ] **Abrir repositorio** abre `https://github.com/DanSanMar/tools4mewindows` en el navegador.
- [ ] **Abrir perfil de GitHub** abre `https://github.com/DanSanMar` en el navegador.
- [ ] **Ayuda → Abrir log**: abre `%TEMP%\t4mw.log` en el editor predeterminado.
- [ ] Si el log no existe, muestra un aviso en lugar de fallar.
- [ ] **Ayuda → Ayuda de Windows**: abre el navegador en la página de ayuda de Windows.

## 9. Log

- [ ] `%TEMP%\t4mw.log` contiene `Iniciando T4MW V.4`.
- [ ] Contiene `Ejecutando como administrador en ...`.
- [ ] Contiene una línea `Ejecutando: ...` por cada secuencia y una línea por cada paso.

## 10. Compilación y `.exe`

- [ ] `pyinstaller Tools4MeW.spec` termina sin errores.
- [ ] `dist\Tools4MeW.exe` arranca en un Windows sin Python instalado.
- [ ] El `.exe` pide UAC, muestra el logo de cabecera, el icono de la ventana y la versión V.4.
- [ ] El archivo `Tools4MeW.exe` muestra el icono personalizado en el Explorador.
- [ ] Los cinco botones, los diálogos de modo, el Modo auto, la barra superior y los menús funcionan igual que con Python.
- [ ] La limpieza rápida no rompe el `.exe` desinstalado: el directorio `_MEI*` de PyInstaller se conserva.
- [ ] El `.exe` no intenta instalar Pillow con `pip` si falta la dependencia.

## Registro de resultados

| Fecha | Equipo | Resultado | Notas |
|-------|--------|-----------|-------|
|       |        |           |       |
