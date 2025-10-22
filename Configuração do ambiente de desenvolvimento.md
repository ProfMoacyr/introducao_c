# Configuração do ambiente de desenvolvimento ESP32

## PlatformIO

1. No vscode, instale a extensão PlatformIO IDE

## Emulador

Na raiz do projeto:

```bash
md \espressif
cd downloads
tar -xzvf qemu-xtensa-softmmu-esp_develop_9.2.2_20250817-x86_64-w64-mingw32.tar.xz qemu.tar.gz -C c:\espressif
copy libiconv-2.dll c:\espressif\qemu\bin\
```

<!-- 1. Baixe os arquivos [qemu-riscv32](https://github.com/espressif/qemu/releases/download/esp-develop-9.2.2-20250817/qemu-riscv32-softmmu-esp_develop_9.2.2_20250817-x86_64-w64-mingw32.tar.xz) e [qemu-xtensa](https://github.com/espressif/qemu/releases/download/esp-develop-9.2.2-20250817/qemu-xtensa-softmmu-esp_develop_9.2.2_20250817-x86_64-w64-mingw32.tar.xz) e descompacte-os na pasta c:\espressif -->
- Inclua a pasta `c:\espressif\qemu\bin` no path
- Copie o arquivo `c:\libiconv-2.dll` para a pasta `c:\espressif\qemu\bin`

## Comandos úteis

> `C:\Users\moacy\.platformio\penv\Scripts\platformio.exe run --target menuconfig --environment esp32doit-devkit-v1`

esptool.py --chip esp32 merge_bin -o qemu_flash.bin --flash_mode dio --flash_freq 40m --flash_size 4MB 0x1000 build/bootloader/bootloader.bin 0x8000 build/partition_table/partition-table.bin 0x10000 build/firmware.bin
