# Whisper Mobile Transcriber

Aplicativo web com layout mobile-first para:
- enviar áudio;
- transcrever usando Whisper;
- copiar o texto;
- baixar a transcrição em `.txt`.

## Como rodar

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Abra em: `http://localhost:8000`

## Observações
- Na primeira execução, o Whisper baixa o modelo `base`.
- É necessário ter `ffmpeg` instalado no sistema para processar diversos formatos de áudio.
