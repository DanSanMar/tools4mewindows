# AGENTS.md

## Repo
Single-file Python Tkinter GUI for Windows system maintenance. The only source file is `t4mw.py`; the docs are `README.md` and `CONVERTIR_A_EXE.md`. There are no packages, tests, CI, lint, or typecheck. Dependencies are listed by name in `requirements.txt` (`pillow`, `pyinstaller`); there are no pins. Do not invent test/lint/build-tool commands.

## Run
- `python t4mw.py` — Windows 10/11 only. It calls Windows-only tools (`winget`, `cmd.exe`, `sfc`, `dism`, `powershell`, `taskkill`) and is not meaningful on Linux/macOS.
- Requires Administrator; the script auto-elevates via UAC (`ctypes.shell32.ShellExecuteW` with `runas`), then `os.chdir`s to the script directory.
- Dependency: `pillow` (PIL). The script auto-installs it at runtime via `pip install pillow` if missing — requires network. Pre-install with `pip install -r requirements.txt` (this also installs PyInstaller).
- Logs to `%TEMP%\t4mw.log`.

## Build `.exe`
- Canonical: `pyinstaller Tools4MeW.spec` (icon `LogoALL4meW.ico`, `console=True`, embeds `LogoALL4meW.png`, output name `Tools4MeW`).
- Alternative: `pyinstaller --onefile --name "Tools4MeW" --icon "LogoALL4meW.ico" --add-data "LogoALL4meW.png;." t4mw.py` (keeps the console window).
- Output lands in `dist/`; `build/` and `dist/` are gitignored.
- Build on Windows: PyInstaller does not cross-compile, and the app calls Windows tools.
- Images are loaded through `resource_path()`, which supports PyInstaller's `_MEIPASS`.
- `--add-data` uses `;` on Windows and `:` on Linux/macOS.

## Docs
- `README.md` covers features and installation; `CONVERTIR_A_EXE.md` covers packaging. Keep both in sync when behavior changes.
- The version is defined once in `VERSION` (`t4mw.py`) and used in the window title, header, and console banner. Keep the README badge in sync.

## Gotchas
- `LogoALL4meW.png` is tracked in git even though `.gitignore` lists it; `.gitignore` does not affect already-tracked files.
- Admin elevation restarts the process with `runas` using `sys.argv[0]`; paths resolved after elevation are relative to the script file.
- The Pillow auto-install is not reliable inside a PyInstaller `.exe`; PyInstaller bundles the dependency at build time, so install it before building.
- SFC/DISM can take several minutes; the launched console stays open with `pause`.
