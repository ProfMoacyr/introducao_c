# extra_script.py
Import("env")
import os
import subprocess

# Define o nome do arquivo de saída de 4MB para o QEMU
QEMU_FIRMWARE = "qemu_firmware_4MB.bin"
FLASH_SIZE = "4MB"

def merge_qemu_firmware(source, target, env):
    print("Iniciando a criação da imagem de 4MB para QEMU...")
    
    # Caminhos para os arquivos gerados pelo build
    bootloader_bin = os.path.join(".pio/build", "bootloader", "bootloader.bin")
    partitions_bin = os.path.join(".pio/build", "partition_table", "partitions.bin")
    app_bin = os.path.join(".pio/build", "firmware.bin")
    output_path = os.path.join(".", QEMU_FIRMWARE)

    # Verifica se os arquivos necessários existem
    if not all(os.path.exists(f) for f in [bootloader_bin, partitions_bin, app_bin]):
        print("Erro: Arquivos binários essenciais não encontrados. Compilação falhou?")
        return

    # Comando esptool.py merge_bin
    # --fill-flash-size: preenche o restante do arquivo de 4MB com 0xFF
    # Endereços: 0x1000 para bootloader, 0x8000 para partitions, 0x10000 para a aplicação
    command = [
        "esptool.py",
        "merge_bin",
        "--output", output_path,
        "--flash_mode", env.GetBuildOption("board_build.flash_mode"),
        "--flash_size", FLASH_SIZE,
        "--fill-flash-size", FLASH_SIZE,
        "0x1000", bootloader_bin,
        "0x8000", partitions_bin,
        "0x10000", app_bin
    ]

    try:
        # Usa o esptool.py do ambiente PlatformIO
        subprocess.check_call(command, env=env['ENV'])
        print(f"\n✅ Imagem de firmware de 4MB para QEMU criada com sucesso em: {output_path}")
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Erro ao executar esptool.py: {e}")

# Adiciona a função ao hook de pós-compilação
env.AddPostAction("buildprog", merge_qemu_firmware)