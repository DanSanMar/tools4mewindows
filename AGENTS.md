# AGENTS.md

## Repo
Single-file Python Tkinter GUI for Windows system maintenance. The only source file is `t4mw.py`; the docs are `README.md`, `CONVERTIR_A_EXE.md`, and `PRUEBAS.md`. There are no packages, automated tests, CI, lint, or typecheck. Dependencies are listed by name in `requirements.txt` (`pillow`, `pyinstaller`); there are no pins. Do not invent test/lint/build-tool commands.

## Run
- `python t4mw.py` — Windows 10/11 only. It calls Windows-only tools (`winget`, `cmd.exe`, `sfc`, `dism`, `chkdsk`, `powershell`) and is not meaningful on Linux/macOS.
- Requires Administrator; the script auto-elevates via UAC (`ctypes.shell32.ShellExecuteW` with `runas`), then `os.chdir`s to the script directory.
- Dependency: `pillow` (PIL). The script auto-installs it at runtime via `pip install pillow` if missing — requires network. Pre-install with `pip install -r requirements.txt` (this also installs PyInstaller).
- Logs to `%TEMP%\t4mw.log`.
- Main actions: update (winget), open Windows Update (Settings), clean (quick/complete, optional recycle bin), diagnose (quick/complete), repair (DISM + SFC). The full-width top bar has five equal-width tabs: "Modo auto" (runs update + quick cleanup + quick diagnostic in one console), "Más herramientas" (restore point, Defender), "Sistema" (Task Manager, Services, Resource Monitor, Event Viewer, Device Manager, Disk Management, Task Scheduler), "Acerca de T4MW" (version, repo/profile links, license), and "Ayuda" (log, Windows support link).

## Build `.exe`
- Canonical: `pyinstaller Tools4MeW.spec` (icon `LogoALL4meW.ico`, `console=True`, embeds `LogoALL4meW.png` and `LogoALL4meW.ico`, output name `Tools4MeW`).
- Alternative: `pyinstaller --onefile --name "Tools4MeW" --icon "LogoALL4meW.ico" --add-data "LogoALL4meW.png;." --add-data "LogoALL4meW.ico;." t4mw.py` (keeps the console window).
- Output lands in `dist/`; `build/` and `dist/` are gitignored.
- Build on Windows: PyInstaller does not cross-compile, and the app calls Windows tools.
- Images are loaded through `resource_path()`, which supports PyInstaller's `_MEIPASS`.
- `--add-data` uses `;` on Windows and `:` on Linux/macOS.

## Docs
- `README.md` covers features and installation; `CONVERTIR_A_EXE.md` covers packaging; `PRUEBAS.md` is the manual checklist for validating a release on Windows. Keep them in sync when behavior changes.
- The version is defined once in `VERSION` (`t4mw.py`) and used in the window title, header, and console banner. Current version: V.4. Keep the README badge in sync.

## Gotchas
- `LogoALL4meW.png` is tracked in git even though `.gitignore` lists it; `.gitignore` does not affect already-tracked files.
- Admin elevation restarts the process with `runas` using `sys.argv[0]`; paths resolved after elevation are relative to the script file.
- The Pillow auto-install is not reliable inside a PyInstaller `.exe`; PyInstaller bundles the dependency at build time, so install it before building.
- The temp-cleanup step must keep excluding `_MEI*` and `t4mw.log`: `_MEI*` is the running onefile bundle, and the log is open. Do not replace it with a blanket `del "%TEMP%\*"`.
- Emptying the recycle bin is an explicit opt-in checkbox in the cleanup dialog (`Clear-RecycleBin -Force`), default off; it permanently deletes personal files. Keep the checkbox opt-in and its permanent-deletion warning; do not make it part of routine cleanup by default.
- Destructive confirmations (repair, restore point, Defender) use `default=messagebox.NO`; keep that default so Enter does not trigger an irreversible action. The recycle-bin option is an explicit checkbox, default off.
- The top menu bar is a custom full-width grid with five equal-width tabs: Menubuttons for "Más herramientas"/"Sistema"/"Ayuda" plus top-level "Modo auto"/"Acerca de T4MW" buttons. Visual order is Modo auto, Más herramientas, Sistema, Acerca de T4MW, Ayuda; Ayuda stays rightmost. Tabs use a blue bar background with a 2px accent line. The native Tk menubar cannot align cascades to the right; do not reintroduce the footer tools button.
- "Sistema" only launches built-in Windows utilities (`taskmgr`, `mmc` snap-ins, `resmon`) through `abrir_utilidad_windows()` using argument lists and no shell. Do not add registry editor or destructive commands there.
- Main action buttons use a soft blue background plus a 1px frame border. `aplicar_tema()` must update both `frames_botones` (border) and `botones` (fill); keep light/dark contrast readable.
- "Modo auto" must stay limited to Winget update, quick cleanup, and quick diagnostic in one console; reuse `pasos_limpieza_rapida()` and `pasos_diagnostico_rapido()`. Do not add repair, recycle bin, complete cleanup, or complete diagnostic to it.
- The About dialog is a custom modal with buttons for the repository (`https://github.com/DanSanMar/tools4mewindows`) and the author profile (`https://github.com/DanSanMar`); both use `abrir_enlace()`. Keep both links and the MIT license text.
- The main-window "Abrir Windows Update" button only opens Settings (`ms-settings:windowsupdate`); it does not install updates. Winget handles apps, not Windows.
- `DISM /StartComponentCleanup` removes superseded components; do not add `/ResetBase`, which would prevent uninstalling all updates.
- The RAM GC and Explorer restart actions were removed on purpose. Do not reintroduce them without a concrete reason.
- SFC/DISM/chkdsk can take several minutes; the launched console stays open with `pause`.
