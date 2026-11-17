"""Construye el video del anexo técnico a partir de video/escenas.py.

1. Narra cada escena con la voz de marca (Laomedeia, Gemini TTS) -> video/trabajo/audio/*.wav
2. Renderiza cada diapositiva HTML con Edge headless -> video/trabajo/png/*.png
3. Une imagen + audio por escena y concatena -> video/demo_diagnostico_ia.mp4

Uso:  python video/construir_video.py            (reutiliza audios ya generados)
"""
import html
import os
import subprocess
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
RAIZ = Path(__file__).parent
sys.path.insert(0, str(RAIZ))
# voz_marca.py es la herramienta de narración (Gemini TTS, voz Laomedeia) del portafolio del autor.
# Indica su carpeta con la variable de entorno VOZ_MARCA_DIR.
sys.path.insert(0, os.environ.get("VOZ_MARCA_DIR", str(RAIZ)))

from escenas import ESCENAS  # noqa: E402
from voz_marca import narrar  # noqa: E402

TRABAJO = RAIZ / "trabajo"
EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
SALIDA = RAIZ / "demo_diagnostico_ia.mp4"
PAUSA_INICIO, PAUSA_FIN = 0.4, 0.8

CSS = """
*{margin:0;box-sizing:border-box}
body{width:1920px;height:1080px;background:#0d0f13;color:#eef0f3;font-family:'Segoe UI',sans-serif;
 padding:90px 120px;position:relative;overflow:hidden}
body:before{content:'';position:absolute;right:-300px;top:-300px;width:900px;height:900px;border-radius:50%;
 background:radial-gradient(circle,rgba(232,163,61,.18),transparent 65%)}
.k{color:#e8a33d;font-size:26px;letter-spacing:4px;text-transform:uppercase;font-weight:600}
h1{font-size:72px;font-weight:700;margin:18px 0 50px;line-height:1.1}
li{font-size:40px;margin:0 0 30px 0;list-style:none;padding-left:46px;position:relative;line-height:1.3}
li:before{content:'';position:absolute;left:0;top:18px;width:18px;height:18px;background:#e8a33d;border-radius:4px}
pre{background:#161a21;border:1px solid #2a303b;border-radius:18px;padding:40px 46px;font:31px/1.55 'Cascadia Code',Consolas,monospace;color:#d6dbe3;white-space:pre;font-variant-ligatures:none}
.f{font:24px Consolas,monospace;color:#8a93a3;margin-bottom:14px}
.pie{position:absolute;left:120px;right:120px;bottom:44px;display:flex;justify-content:space-between;color:#6b7381;font-size:22px}
table{border-collapse:collapse;width:100%}td{font-size:36px;padding:22px 26px;border-bottom:1px solid #2a303b}
td:first-child{color:#e8a33d;width:42%}
.term{background:#0a0c0f;border:1px solid #2a303b;border-radius:18px;padding:34px 44px;font:29px/1.5 'Cascadia Code',Consolas,monospace}
.ok{color:#5fd38d}.cmd{color:#e8a33d}
.dos{display:flex;gap:50px}.dos>div{flex:1;background:#161a21;border:1px solid #2a303b;border-radius:18px;padding:40px}
.dos h3{font-size:30px;color:#e8a33d;margin-bottom:24px;letter-spacing:2px}
.dos p{font-size:34px;line-height:1.45;color:#c9ced6;font-style:italic}
.dos li{font-size:34px}
.flujo{display:flex;align-items:center;justify-content:space-between;margin-top:70px}
.caja{width:250px;height:190px;border-radius:20px;background:#161a21;border:2px solid #2a303b;display:flex;
 flex-direction:column;align-items:center;justify-content:center;text-align:center;font-size:30px;font-weight:600}
.caja span{font-size:56px;margin-bottom:10px}.caja small{font-size:21px;color:#8a93a3;font-weight:400;margin-top:6px}
.caja.d{border-color:#e8a33d}
.fl{font-size:44px;color:#e8a33d}
.nota{margin-top:70px;font-size:32px;color:#aab2bf;line-height:1.6}
.caps{display:flex;gap:30px;height:620px}
.cap{flex:1;border-radius:16px;overflow:hidden;border:2px solid #e8a33d;background:#fff}
.cap img{width:100%;height:100%;object-fit:contain}
.portada{display:flex;flex-direction:column;justify-content:center;height:100%}
.portada h1{font-size:104px}.portada p{font-size:40px;color:#aab2bf}
"""


def _pie() -> str:
    return ('<div class="pie"><span>Henry Taborda · Challenge ONE G11 — Taranis Black</span>'
            '<span>Voz generada con IA</span></div>')


def _html(e: dict) -> str:
    t, esc = e["tipo"], html.escape
    cab = f'<div class="k">Diagnóstico IA de Pre-Ventas</div><h1>{esc(e["titulo"])}</h1>'
    if t == "portada":
        cuerpo = (f'<div class="portada"><div class="k">Anexo técnico · Python + Gemini + Pipedrive</div>'
                  f'<h1>{esc(e["titulo"])}</h1><p>{esc(e["subtitulo"])}</p></div>')
    elif t in ("puntos", "cierre"):
        cuerpo = cab + "<ul>" + "".join(f"<li>{esc(p)}</li>" for p in e["puntos"]) + "</ul>"
    elif t == "codigo":
        cuerpo = cab + f'<div class="f">{esc(e["archivo"])}</div><pre>{esc(chr(10).join(e["codigo"]))}</pre>'
    elif t == "tabla":
        cuerpo = cab + "<table>" + "".join(f"<tr><td>{esc(a)}</td><td>{esc(b)}</td></tr>"
                                           for a, b in e["filas"]) + "</table>"
    elif t == "terminal":
        lineas = []
        for l in e["lineas"]:
            clase = "cmd" if l.startswith("PS>") else "ok" if "✔" in l or l.startswith("Listo") else ""
            lineas.append(f'<div class="{clase}">{esc(l)}</div>')
        cuerpo = cab.replace("<h1>", '<h1 style="margin-bottom:30px">') + '<div class="term">' + "".join(lineas) + "</div>"
    elif t == "antes_despues":
        cuerpo = cab + (f'<div class="dos"><div><h3>ENTRA · nota del vendedor</h3><p>{esc(e["antes"])}</p></div>'
                        '<div><h3>SALE · nota en Pipedrive</h3><ul>'
                        + "".join(f"<li>{esc(p)}</li>" for p in e["despues"]) + "</ul></div></div>")
    elif t == "diagrama":
        cajas = [("👤", "Vendedor", "crea el deal"), ("📇", "Pipedrive", "webhook create.deal"),
                 ("🔒", "ngrok", "túnel HTTPS"), ("⚡", "FastAPI", "200 OK + 2.º plano"),
                 ("✨", "Gemini", "rol Pre-Ventas")]
        fila = ' <div class="fl">→</div> '.join(
            f'<div class="caja{" d" if n == "FastAPI" else ""}"><span>{i}</span>{n}<small>{s}</small></div>'
            for i, n, s in cajas)
        cuerpo = cab + f'<div class="flujo">{fila}</div>' + (
            '<div class="nota">↩ El diagnóstico vuelve a Pipedrive como <b>nota fijada</b> en el mismo deal '
            '(POST /api/v1/notes).<br>Sin relato → no se llama a la IA: nota «Diagnóstico no generado».</div>')
    elif t == "capturas":
        carpeta = RAIZ / "capturas"
        imgs = "".join(
            f'<div class="cap"><img src="{(carpeta / n).as_uri()}"></div>' for n in e["imagenes"])
        cuerpo = cab.replace("<h1>", '<h1 style="margin-bottom:34px">') + f'<div class="caps">{imgs}</div>'
    else:
        raise ValueError(t)
    return f'<!doctype html><meta charset="utf-8"><style>{CSS}</style><body>{cuerpo}{_pie() if t != "portada" else _pie()}</body>'


def _duracion(wav: Path) -> float:
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(wav)],
                       capture_output=True, text=True, check=True)
    return float(r.stdout.strip())


def main() -> None:
    for d in ("audio", "png", "html", "clips"):
        (TRABAJO / d).mkdir(parents=True, exist_ok=True)
    perfil = TRABAJO / "edge_perfil"
    clips = []
    for e in ESCENAS:
        print(f"▶ {e['id']}")
        wav = narrar(e["narracion"], TRABAJO / "audio" / f"{e['id']}.wav")
        pagina = TRABAJO / "html" / f"{e['id']}.html"
        pagina.write_text(_html(e), encoding="utf-8")
        png = TRABAJO / "png" / f"{e['id']}.png"
        for intento in range(3):  # Edge headless a veces se cuelga: límite de 60 s y reintento
            try:
                subprocess.run([EDGE, "--headless=new", "--disable-gpu", "--hide-scrollbars",
                                f"--user-data-dir={perfil}", "--force-device-scale-factor=1",
                                "--allow-file-access-from-files",
                                "--window-size=1920,1080", f"--screenshot={png}", pagina.as_uri()],
                               check=True, capture_output=True, timeout=60)
                break
            except subprocess.TimeoutExpired:
                print(f"  Edge no respondió; reintento {intento + 1}/3")
                subprocess.run(["powershell", "-NoProfile", "-Command",
                                "Get-CimInstance Win32_Process -Filter \"Name='msedge.exe'\" | "
                                "Where-Object { $_.CommandLine -like '*edge_perfil*' } | "
                                "ForEach-Object { Stop-Process -Id $_.ProcessId -Force }"])
        else:
            raise SystemExit(f"Edge no pudo capturar {pagina.name}")
        dur = _duracion(wav) + PAUSA_INICIO + PAUSA_FIN
        clip = TRABAJO / "clips" / f"{e['id']}.mp4"
        retraso = int(PAUSA_INICIO * 1000)
        subprocess.run([
            "ffmpeg", "-v", "error", "-y", "-loop", "1", "-framerate", "30", "-i", str(png), "-i", str(wav),
            "-filter_complex",
            f"[0:v]scale=1920:1080,"
            f"fade=t=in:st=0:d=0.35,fade=t=out:st={dur - 0.35:.2f}:d=0.35,format=yuv420p[v];"
            f"[1:a]adelay={retraso}|{retraso},apad,atrim=0:{dur:.2f},aresample=44100[a]",
            "-map", "[v]", "-map", "[a]", "-t", f"{dur:.2f}", "-c:v", "libx264", "-preset", "medium",
            "-crf", "20", "-c:a", "aac", "-b:a", "160k", "-ac", "2", str(clip)], check=True)
        clips.append(clip)
        print(f"  {dur:.1f} s")

    lista = TRABAJO / "lista.txt"
    lista.write_text("".join(f"file '{c.as_posix()}'\n" for c in clips), encoding="utf-8")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(lista),
                    "-c", "copy", "-movflags", "+faststart", str(SALIDA)], check=True)
    print(f"\nVideo: {SALIDA}  ({_duracion(SALIDA):.0f} s)")


if __name__ == "__main__":
    main()
