# Changelog

## [Unreleased]

## 0.3.0 - 18-03-2026
### Added
- Wireless connection dialog with Quick Connect and Android 11+ pairing-code flow
- Support for legacy TCP/IP wireless mode
- Automatic wireless connection prompt when no USB device detected
- Connection settings persistence in config
- Network scanner — auto-discovers ADB devices on the local subnet
- X11 window docking via `X11DockManager` using python-xlib reparenting
- `StatelessDockManager` as a no-op fallback for Wayland sessions
- Abstract `DockManager` base class — platform backends swapped in at runtime
- Swap screens toggle — switch which display is top/bottom, persisted to config
- Layout mode switching (`DUAL` / `TOP` / `BOTTOM`) with dynamic container resize
- Automatic `adb`/`scrcpy` installation via `pkexec` on first launch (pacman and apt-get supported)
- SIGINT / Ctrl+C signal handling with clean shutdown
- Platform-conditional requirements — `pywin32-ctypes` Windows-only, `python-xlib` Linux-only
### Changed
- `--window-borderless` scrcpy flag now only applied on Windows; Linux keeps window decorations
- Loading screen skipped on Linux to avoid Pygame display-init race condition
- Process force-kill falls back to `SIGKILL` on Linux instead of `taskkill`
- `show_fatal_error()` prints to console on Linux instead of Win32 MessageBox
- Windows binaries (`adb.exe`, `scrcpy.exe`, `.dll`, `.bat`) removed from repository
### Bugfixes
- Fixed issue where bottom screen displays incorrectly, causing non-transparency with screenshots
- Improved window handling to improve stability

## 0.2.0 - 31-01-2026
### Added
- Added ability to change Scrcpy Scale
- Better logging and error handling
### Bugfixes
- Fixed issue with Control Panel crashing on Windows 10 and improved Windows 10 Compatibility
- Updated codebase to become more refined
- Improved window management safeguards for Windows 10


## 0.1.1 - 28-01-2026
### Added
- Added incompatibility warning for Windows 10
- Add thread safety to window focus handling
- Improved dark mode support
### Bugfixes
- Fixed spacing on "DOCK WINDOWS" text 
- Debounce and throttle sync() calls


## 0.1.0 - 26-01-2026
### Added
- Dual-screen scrcpy docking
- Layout presets
- Screenshot capture
- Logging system
- PyInstaller build support
