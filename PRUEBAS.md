# Pruebas de T4MW V.2.1 — Fase 2

Checklist para validar la versión **V.2.1** en Windows 10/11 antes de compilar y distribuir el `.exe`.

Marca cada casilla cuando el resultado coincida con lo esperado. Si algo falla, anota el paso, el mensaje y la hora para revisar `%TEMP%\t4mw.log`.

## Preparación

- [ ] `git pull origin mejora-fase1`
- [ ] `pip install -r requirements.txt`
- [ ] Cerrar aplicaciones importantes antes de las pruebas de limpieza.
- [ ] Anotar la hora de inicio para localizar la sesión en el log.

## 1. Arranque y permisos

- [ ] Ejecutar `python t4mw.py` sin administrador: debe aparecer el UAC y relanzarse elevado.
- [ ] El título de la ventana muestra `T4MW - All4me Group (V.2.1)`.
- [ ] La cabecera muestra `T O O L S 4 M E W - V.2.1`.
- [ ] Se ven el icono y el logo.
- [ ] Cambiar entre modo claro y oscuro: no deben quedar marcos oscuros en modo claro.
- [ ] Cerrar y volver a abrir la aplicación.

## 2. Actualizar todo el software (flujo principal)

- [ ] Pulsar **Actualizar Todo el Software**: se abre una consola nueva.
- [ ] La consola muestra el banner `### Tools4meW - V.2.1 ###`.
- [ ] Se ejecuta `winget upgrade --all ...` y lista las actualizaciones disponibles.
- [ ] Al terminar, la consola se queda en `pause`.
- [ ] El comando aparece en `%TEMP%\t4mw.log`.
- [ ] Probar en un equipo sin *App Installer* o sin `winget` en el PATH: debe salir el diálogo **Winget no disponible**, no una consola rota.

## 3. Limpiar archivos basura

- [ ] Pulsar el botón: aparece una confirmación.
- [ ] Pulsar **No**: no se ejecuta nada.
- [ ] Pulsar **Sí**: se ejecutan `ipconfig /flushdns` y la limpieza de `%temp%` y `C:\Windows\Temp`.
- [ ] Si algún archivo está bloqueado, la consola no se cierra y permite leer el error.
- [ ] El comando aparece en el log.

## 4. Reparar archivos del sistema (SFC)

- [ ] Pulsar el botón: aparece la confirmación con el aviso de duración.
- [ ] Aceptar: se ejecuta `sfc /scannow` y la interfaz no se congela.
- [ ] La consola permanece abierta al terminar.
- [ ] El comando aparece en el log.

## 5. Eliminar residuos de Update (DISM)

- [ ] Pulsar el botón: aparece la confirmación.
- [ ] Aceptar: se ejecuta `dism /online /cleanup-image /startcomponentcleanup`.
- [ ] La consola permanece abierta al terminar.
- [ ] El comando aparece en el log.

## 6. Restaurar imagen de sistema (DISM)

- [ ] Pulsar el botón: aparece la confirmación.
- [ ] Aceptar: se ejecuta `dism /online /cleanup-image /restorehealth`.
- [ ] La consola permanece abierta al terminar.
- [ ] El comando aparece en el log.

## 7. Reiniciar Windows Explorer

- [ ] Pulsar el botón: aparece la confirmación.
- [ ] Aceptar: la barra de tareas desaparece y vuelve.
- [ ] Las ventanas de carpetas abiertas se cierran.
- [ ] El comando aparece en el log.

## 8. Optimizar memoria RAM

- [ ] Pulsar el botón: no pide confirmación (la acción es rápida).
- [ ] Se ejecuta el comando de PowerShell y la consola queda en `pause`.
- [ ] El comando aparece en el log.

## 9. Log

- [ ] `%TEMP%\t4mw.log` contiene `Iniciando T4MW V.2.1`.
- [ ] Contiene `Ejecutando como administrador en ...`.
- [ ] Contiene una línea `Ejecutando: ... -> ...` por cada acción lanzada.

## 10. Compilación y `.exe` (Fase 3)

- [ ] `pyinstaller Tools4MeW.spec` termina sin errores.
- [ ] `dist\Tools4MeW.exe` arranca en un Windows sin Python instalado.
- [ ] El `.exe` pide UAC, muestra icono, logo y versión V.2.1.
- [ ] Los botones, las confirmaciones y el log funcionan igual que con Python.
- [ ] El `.exe` no intenta instalar Pillow con `pip` si falta la dependencia.

## Registro de resultados

| Fecha | Equipo | Resultado | Notas |
|-------|--------|-----------|-------|
|       |        |           |       |
