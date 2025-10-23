import os

# Tamanho desejado: 4MB
TARGET_SIZE = 4 * 1024 * 1024

with open(".pio/build/esp32doit-devkit-v1/firmware.bin", "rb") as f:
    data = f.read()

# Verifica se o firmware é menor que 4MB
if len(data) > TARGET_SIZE:
    raise ValueError("Firmware maior que 4MB!")

# Preenche com zeros até 4MB
padded_data = data + b"\x00" * (TARGET_SIZE - len(data))

with open("qemu_flash.bin", "wb") as f:
    f.write(padded_data)

print("Arquivo qemu_flash.bin gerado com 4MB exatos.")
