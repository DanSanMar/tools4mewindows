# Pruebas de T4MW V.3 — Fase 3

Checklist para validar la versión **V.3** en Windows 10/11 antes de compilar y distribuir el `.exe`.

Marca cada casilla cuando el resultado coincida con lo esperado. Si algo falla, anota el paso, el mensaje y la hora para revisar `%TEMP%\t4mw.log`.

## Preparación

- [ ] `git pull origin mejora-fase1`
- [ ] `pip install -r requirements.txt`
- [ ] Cerrar aplicaciones importantes antes de las pruebas de limpieza.
- [ ] No ejecutar dos acciones largas a la vez; esperar a que termine cada consola.
- [ ] Anotar la hora de inicio para localizar la sesión en el log.

## 1. Arranque y menú

- [ ] Ejecutar `python t4mw.py` sin administrador: debe aparecer el UAC y relanzarse elevado.
- [ ] Cancelar el UAC: la consola muestra `Error crítico al elevar privilegios` y espera a que pulses Enter; no se queda colgada.
- [ ] El título de la ventana muestra `T4MW - All4me Group (V.3)`.
- [ ] La cabecera muestra `T O O L S 4 M E W - V.3`.
- [ ] Se ven el icono y el logo.
- [ ] El menú principal tiene exactamente cinco botones: **Actualizar Todo el Software**, **Abrir Windows Update**, **Limpiar Sistema**, **Diagnóstico** y **Reparar Windows**.
- [ ] No aparecen las acciones antiguas de RAM ni de reiniciar Explorer.
- [ ] La barra superior está alineada a la derecha y muestra **Más herramientas**, **Acerca de T4MW** y **Ayuda**.
- [ ] **Más herramientas** contiene punto de restauración y análisis de Defender.
- [ ] **Ayuda** contiene Abrir log y Ayuda de Windows.
- [ ] No hay botón inferior de herramientas.
- [ ] La ventana muestra los cinco botones y el botón de tema sin recortes.
- [ ] Cambiar entre modo claro y oscuro: no deben quedar marcos oscuros en modo claro.
- [ ] Abrir el diálogo de **Limpiar Sistema** en modo oscuro y en modo claro: debe usar los colores del tema.
- [ ] Cerrar y volver a abrir la aplicación.

## 2. Actualizar todo el software

- [ ] Pulsar **Actualizar Todo el Software**: se abre una consola nueva.
- [ ] La consola muestra el banner `### Tools4meW - V.3 ###`.
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

## 7. Más herramientas, Ayuda y Acerca de

- [ ] **Más herramientas → Crear punto de restauración**: pide confirmación y ejecuta `Checkpoint-Computer`. Si la Protección del sistema está desactivada, muestra el error en la consola sin cerrarla.
- [ ] **Más herramientas → Análisis rápido de Defender**: pide confirmación, actualiza firmas y lanza un análisis rápido. Si hay otro antivirus, muestra el error en la consola.
- [ ] **Acerca de T4MW** (barra superior): muestra la versión, el autor, GitHub y la licencia MIT.
- [ ] **Ayuda → Abrir log**: abre `%TEMP%\t4mw.log` en el editor predeterminado.
- [ ] Si el log no existe, muestra un aviso en lugar de fallar.
- [ ] **Ayuda → Ayuda de Windows**: abre el navegador en la página de ayuda de Windows.

## 8. Log

- [ ] `%TEMP%\t4mw.log` contiene `Iniciando T4MW V.3`.
- [ ] Contiene `Ejecutando como administrador en ...`.
- [ ] Contiene una línea `Ejecutando: ...` por cada secuencia y una línea por cada paso.

## 9. Compilación y `.exe` (Fase 4)

- [ ] `pyinstaller Tools4MeW.spec` termina sin errores.
- [ ] `dist\Tools4MeW.exe` arranca en un Windows sin Python instalado.
- [ ] El `.exe` pide UAC, muestra el logo de cabecera, el icono de la ventana y la versión V.3.
- [ ] El archivo `Tools4MeW.exe` muestra el icono personalizado en el Explorador.
- [ ] Los cinco botones, los diálogos de modo, la barra superior y los menús funcionan igual que con Python.
- [ ] La limpieza rápida no rompe el `.exe` desinstalado: el directorio `_MEI*` de PyInstaller se conserva.
- [ ] El `.exe` no intenta instalar Pillow con `pip` si falta la dependencia.

## Registro de resultados

| Fecha | Equipo | Resultado | Notas |
|-------|--------|-----------|-------|
|       |        |           |       |
