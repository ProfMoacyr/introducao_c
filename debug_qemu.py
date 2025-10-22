import subprocess
import os
from pathlib import Path

BUILD_DIR = Path(".pio/build/esp32doit-devkit-v1")
FLASH_BIN = BUILD_DIR / "qemu_flash.bin"
ELF_FILE = BUILD_DIR / "firmware.elf"

# Comando para iniciar QEMU com GDB remoto
qemu_cmd = [
    "qemu-system-xtensa",
    "-nographic",
    "-machine",
    "esp32",
    "-serial",
    "mon:stdio",
    "-drive",
    f"file={FLASH_BIN},if=mtd,format=raw,id=flash",
    "-s",
    "-S",
]

# Comando para iniciar GDB e conectar ao QEMU
gdb_cmd = [
    "xtensa-esp32-elf-gdb",
    str(ELF_FILE),
    "-ex",
    "target remote :1234",
    "-ex",
    "monitor reset halt",
    "-ex",
    "break app_main",
    "-ex",
    "continue",
]

print("[QEMU] Iniciando emulador...")
qemu_proc = subprocess.Popen(qemu_cmd)

print("[GDB] Conectando ao QEMU...")
subprocess.run(gdb_cmd)

# Finaliza QEMU após GDB encerrar
qemu_proc.terminate()
