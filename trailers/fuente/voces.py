import subprocess, json, os, wave
from guion import GUION, VOCES, EFECTOS
os.makedirs('vo', exist_ok=True)
info = {}
for idioma, lineas in GUION.items():
    info[idioma] = []
    for n, (inicio, quien, texto) in enumerate(lineas):
        modelo, lento = VOCES[idioma][quien]
        crudo, final = f'vo/{idioma}_{n:02d}_crudo.wav', f'vo/{idioma}_{n:02d}.wav'
        subprocess.run(['venv/bin/piper', '-m', f'voces/{modelo}.onnx', '-f', crudo, '--length_scale', str(lento), '--sentence_silence', '0.15'],
                       input=texto.encode(), check=True, capture_output=True)
        filtro = f"{EFECTOS[quien][idioma]},{EFECTOS[quien]['comun']},silenceremove=start_periods=1:start_threshold=-45dB,areverse,silenceremove=start_periods=1:start_threshold=-45dB,areverse,aresample=48000"
        subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', crudo, '-af', filtro, '-ac', '2', final], check=True)
        dur = float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', final]))
        info[idioma].append({'inicio': inicio, 'quien': quien, 'texto': texto, 'archivo': final, 'dur': round(dur, 2)})
        print(f'{idioma} {inicio:5.2f}s {quien:9s} {dur:4.2f}s  {texto}')
json.dump(info, open('vo/lineas.json', 'w'), ensure_ascii=False, indent=1)
