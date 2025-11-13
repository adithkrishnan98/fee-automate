# Building Fee Tracker

This guide explains how to build Fee Tracker for distribution.

## ⚠️ Important: When to Rebuild

**YES, you need to rebuild after EVERY code change!** The DMG/EXE packages contain compiled Python bytecode, not the source files. Changes to `fee_tracker.py` or other Python files won't be reflected in already-built packages.

## Quick Build Commands

### macOS (One Command)
```bash
chmod +x build_and_package.sh
./build_and_package.sh
```

This will:
- Clean previous builds
- Build `FeeTracker.app`
- Create `FeeTracker-1.0.0-macOS.dmg`
- Show file sizes and next steps

**Output:** `dist/FeeTracker-1.0.0-macOS.dmg` (ready to distribute)

### Windows (One Command)
```cmd
build_windows.bat
```

This will:
- Clean previous builds
- Build `FeeTracker.exe`
- Create standalone executable

**Output:** `dist/FeeTracker.exe` (ready to distribute)

## Cross-Platform Builds

**❌ You CANNOT build Windows executables on macOS** (or vice versa).

PyInstaller builds are platform-specific:
- **macOS builds** → `.app` bundles and `.dmg` installers (macOS only)
- **Windows builds** → `.exe` executables (Windows only)

### To build for both platforms:

1. **On macOS**: Run `./build_and_package.sh`
2. **On Windows**: Run `build_windows.bat`

OR use a CI/CD service like GitHub Actions to build for both platforms automatically.

## Individual Build Steps (Manual)

If you need more control, you can run steps individually:

### macOS - Manual Steps
```bash
# 1. Build the app
./build_app.sh

# 2. Create DMG (optional)
./create_dmg.sh
```

### Windows - Manual Steps
```cmd
REM 1. Build the executable
.venv\Scripts\pyinstaller.exe fee_tracker_windows.spec --clean --noconfirm
```

## Development Workflow

### During Development
Run directly with Python (no rebuilding needed):
```bash
# macOS/Linux
.venv/bin/python fee_tracker.py

# Windows
.venv\Scripts\python.exe fee_tracker.py
```

### Before Distribution
1. Make your code changes
2. Test with Python directly (above)
3. **Run the build script** (`build_and_package.sh` or `build_windows.bat`)
4. Test the built app/exe
5. Distribute the DMG or EXE

## Build Outputs

### macOS
- `dist/FeeTracker.app` - Standalone app bundle
- `dist/FeeTracker-1.0.0-macOS.dmg` - Installer for distribution

### Windows
- `dist/FeeTracker.exe` - Standalone executable
- `dist/` folder contains all dependencies

## Troubleshooting

### "Module not found" errors in built app
Add missing module to `hiddenimports` in the `.spec` file:
```python
hiddenimports=[
    'PySide6.QtCore',
    'missing_module_name',  # Add here
],
```

### Build is too large
PyInstaller includes many dependencies. To reduce size:
- Use `--exclude-module` for unused modules
- Enable UPX compression (already enabled)

### Changes not reflected in built app
**You forgot to rebuild!** Run the build script again.

## File Sizes (Approximate)

- **macOS DMG**: ~40 MB
- **Windows EXE**: ~50-60 MB (includes Qt framework)

These sizes are normal for PyQt/PySide applications with bundled dependencies.
