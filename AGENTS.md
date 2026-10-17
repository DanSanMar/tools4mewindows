# AGENTS.md

## Repo
Single-file Python Tkinter GUI for Windows system maintenance. The only source file is `t4mw.py`; there are no other packages, no tests, no CI, no lint, no typecheck, and no `requirements.txt`. Do not invent test/lint/build-tool commands.

## Run
- `python t4mw.py` — Windows 10/11 only. It calls Windows-only tools (`winget`, `cmd.exe`, `sfc`, `dism`, `powershell`, `taskkill`) and is not meaningful on Linux/macOS.
- Requires Administrator; the script auto-elevates via UAC (`ctypes.shell32.ShellExecuteW` with `runas`), then `os.chdir`s to the script directory.
- Dependency: `pillow` (PIL). The script auto-installs it at runtime via `pip install pillow` if missing — requires network. Pre-install manually to avoid the runtime prompt.

## Build `.exe`
- Canonical: `pyinstaller Tools4MeW.spec` (spec sets icon from `LogoALL4meW.ico`, `console=True`, output name `Tools4MeW`).
- Alternative: `pyinstaller --onefile --name "Tools4MeW" t4mw.py` (keeps console window).
- Output lands in `dist/`; `build/` and `dist/` are gitignored.
- To embed the logo image in a onefile build add `--add-data "LogoALL4meW.png;."` (Windows `;` separator). Images are loaded through `resource_path()`, which supports PyInstaller's `_MEIPASS`.

## Gotchas
- `LogoALL4meW.png` is listed in `.gitignore` and is not tracked; don't assume it is committed.
- Admin elevation restarts the process with `runas` using `sys.argv[0]`; paths resolved after elevation are relative to the script file.
- Version badges in the README (v1.5) and window title (V.2) disagree; the code is the source of truth, not the badges.