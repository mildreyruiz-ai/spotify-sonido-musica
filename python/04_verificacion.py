"""Recalcula con otro método (numpy, a mano) varias cifras de la página y las compara con resultados.json."""
import json, pathlib
import numpy as np, pandas as pd
R = pathlib.Path(__file__).resolve().parent.parent
res = json.loads((R / "data" / "resultados.json").read_text(encoding="utf-8"))
raw = pd.read_csv(R / "data" / "spotify_songs_raw.csv").dropna(subset=["track_name", "track_artist"])
raw = raw.drop_duplicates("track_id").sort_values("track_popularity", ascending=False)
raw = raw.drop_duplicates(["track_name", "track_artist"])
anio = pd.to_datetime(raw.track_album_release_date, format="mixed").dt.year.to_numpy()
dur = (raw.duration_ms / 60000).to_numpy(); val = raw.valence.to_numpy(); vol = raw.loudness.to_numpy()
assert len(raw) == res["n_total"], (len(raw), res["n_total"])
ok = True
for p in res["periodos"]:
    m = (anio >= p["periodo"]) & (anio <= p["periodo"] + 4)
    for nombre, arr, f in [("duración", dur, np.median), ("positividad", val, np.mean), ("volumen", vol, np.mean)]:
        esperado = {"duración": p["duracion_min"], "positividad": p["positividad"], "volumen": p["volumen_db"]}[nombre]
        bien = abs(round(float(f(arr[m])), 3) - esperado) < 0.0011
        ok &= bien
        if not bien: print("FALLA", p["etiqueta"], nombre)
    assert m.sum() == p["canciones"]
print("TODO CUADRA" if ok else "HAY DIFERENCIAS"); assert ok
