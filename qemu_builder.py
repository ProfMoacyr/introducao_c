Import("env")
import os
import subprocess

# --- Configurações ---
# Tamanho da Flash em MB que o QEMU suporta.
FLASH_SIZE_MB = "4"
# O nome do arquivo final de flash para o QEMU
QEMU_FLASH_BIN = "qemu_flash.bin"

# Caminhos dos binários gerados pelo PlatformIO/ESP-IDF
BUILD_DIR = env.subst("$BUILD_DIR")
BOOTLOADER_BIN = os.path.join(BUILD_DIR, "bootloader.bin")
PARTITIONS_BIN = os.path.join(BUILD_DIR, "partitions.bin")
FIRMWARE_BIN = os.path.join(BUILD_DIR, "firmware.bin")
QEMU_FLASH_PATH = os.path.join(BUILD_DIR, QEMU_FLASH_BIN)

# Caminho para o esptool.py (fornecido pelo PlatformIO)
ESPTOOL_PY = env.subst("$PYTHONEXE") + " " + os.path.join(
    env.PioPlatform().get_package_dir("tool-esptoolpy"), "esptool.py"
)

# Caminho para o QEMU (fornecido pelo PlatformIO/ESP-IDF Tools)
QEMU_BIN = "qemu-system-xtensa"

# Offsets padrão do ESP32
FLASH_OFFSETS = [
    ("0x1000", BOOTLOADER_BIN),
    ("0x8000", PARTITIONS_BIN),
    ("0x10000", FIRMWARE_BIN)
]

# ------------------ 1. Cria a Imagem de Flash de 4MB ------------------
def merge_qemu_flash(*args, **kwargs):
    print("--- Gerando imagem de flash de 4MB para QEMU ---")

    # Monta o comando merge_bin
    cmd = [
        ESPTOOL_PY,
        "--chip", "esp32",
        "merge_bin",
        "-o", QEMU_FLASH_PATH,
        "--flash_mode", env.GetEffectiveFlashMode(),
        "--flash_freq", env.GetEffectiveFlashFreq(),
        "--flash_size", FLASH_SIZE_MB + "MB"
    ]

    for offset, path in FLASH_OFFSETS:
        if os.path.exists(path):
            cmd.extend([offset, path])
        else:
            print(f"AVISO: Arquivo não encontrado: {path}")

    try:
        # Executa o comando de mesclagem
        subprocess.check_call(cmd, shell=True)
        print(f"Sucesso: Imagem de QEMU criada em: {QEMU_FLASH_PATH}")
        print(f"Tamanho do arquivo: {os.path.getsize(QEMU_FLASH_PATH)} bytes.")
    except Exception as e:
        print(f"ERRO ao gerar imagem de QEMU: {e}")


# ------------------ 2. Define o Target (Alvo) de Emulação QEMU ------------------
def run_qemu(*args, **kwargs):
    print("\n--- Iniciando Emulação QEMU ---")

    # Comando QEMU
    qemu_cmd = [
        QEMU_BIN,
        "-nographic",
        "-machine", "esp32",
        "-serial", "mon:stdio",
        # Usamos if=mtd, pois é a interface de memória flash correta
        "-drive", f"file={QEMU_FLASH_PATH},if=mtd,format=raw"
    ]

    if not os.path.exists(QEMU_FLASH_PATH):
        print("ERRO: Imagem de flash QEMU não encontrada. Execute 'pio run' primeiro.")
        return

    try:
        # Executa o QEMU
        subprocess.run(qemu_cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"QEMU encerrou com erro: {e}")
    except FileNotFoundError:
        print(f"ERRO: O executável QEMU não foi encontrado em: {QEMU_BIN}")
        print("Certifique-se de que o PlatformIO instalou o pacote 'tool-qemu-xtensa-esp'.")


# Adiciona a função de mesclagem para ser executada após o build
env.AddPostAction("build", merge_qemu_flash)

# Adiciona um novo Target (Alvo) chamado "qemu" que pode ser chamado via CLI
# Define um comando que executa a função run_qemu (sem a variável de ambiente)
qemu_command = env.Command(
    target=QEMU_FLASH_PATH,  # Define a dependência do comando
    source=None,
    action=run_qemu  # Aqui o 'action' é aceito dentro de Command
)

# Cria um ALIAS (qemu) que executa o comando definido acima
env.AddAlias("qemu", qemu_command)
env.AlwaysBuild("qemu") # Garante que ele sempre execute

# Adiciona a função de mesclagem para ser executada após o build
env.AddPostAction("build", merge_qemu_flash)