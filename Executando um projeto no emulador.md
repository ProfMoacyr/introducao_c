# Executando um projeto no emulador

## Configuração do projeto

Na pasta raiz do projeto:

```bash
C:\Users\Aula\.platformio\penv\Scripts\platformio.exe run --target menuconfig --environment esp32doit-devkit-v1
```

## Compile o projeto

```bash
C:\Users\Aula\.platformio\penv\Scripts\platformio.exe run --environment esp32doit-devkit-v1
```

## Altera o tamanho da imagem para 4MB

```bash
python qemu_4mb.py
```

```bash
qemu-system-xtensa -nographic -machine esp32 -serial mon:stdio -drive file=qemu_flash.bin,if=mtd,format=raw,id=flash
```
