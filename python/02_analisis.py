"""Calcula las cifras del relato y las guarda en data/resultados.json."""
import json, pathlib
import pandas as pd
RAIZ = pathlib.Path(__file__).resolve().parent.parent
d = pd.read_csv(RAIZ / "data" / "canciones.csv")

# 2020 solo llega hasta enero: se deja fuera de las tendencias
t = d[(d.anio >= 1970) & (d.anio <= 2019)].copy()
t["periodo"] = (t.anio // 5 * 5)
t["etiqueta"] = t["periodo"].astype(str) + "-" + (t["periodo"] + 4).astype(str).str[-2:]
per = (t.groupby(["periodo", "etiqueta"])
         .agg(canciones=("cancion", "size"), duracion_min=("duracion_min", "median"),
              positividad=("positividad", "mean"), volumen_db=("volumen_db", "mean"),
              bailable=("bailable", "mean"), energia=("energia", "mean"), acustica=("acustica", "mean"))
         .round(3).reset_index())

gen = (d.groupby("genero")
         .agg(canciones=("cancion", "size"), duracion_min=("duracion_min", "median"),
              positividad=("positividad", "mean"), bailable=("bailable", "mean"),
              energia=("energia", "mean"), tempo=("tempo", "median"), popularidad=("popularidad", "mean"))
         .round(3).reset_index().sort_values("positividad", ascending=False))

# Correlación de Spearman con la popularidad (canciones desde 2010, popularidad > 0)
rec = d[(d.anio >= 2010) & (d.popularidad > 0)]
vars_ = {"duracion_min": "Duración", "bailable": "Bailable", "energia": "Energía", "positividad": "Positividad",
         "acustica": "Acústica", "volumen_db": "Volumen", "habla": "Parte hablada", "tempo": "Tempo"}
corr = rec[list(vars_) + ["popularidad"]].corr(method="spearman")["popularidad"].drop("popularidad")
corr = [{"variable": vars_[k], "rho": round(float(v), 3)} for k, v in corr.sort_values().items()]

res = {"periodos": per.to_dict("records"), "generos": gen.to_dict("records"), "correlaciones": corr,
       "n_total": int(len(d)), "n_tendencias": int(len(t)), "n_corr": int(len(rec)),
       "anio_min": int(d.anio.min()), "anio_max": int(d.anio.max()),
       "sin_popularidad": int((d.popularidad == 0).sum())}
(RAIZ / "data" / "resultados.json").write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")

# Comprobaciones
assert per.canciones.sum() == len(t)
assert (per.canciones >= 250).all(), "algún periodo tiene muy pocas canciones"
assert gen.canciones.sum() == len(d)
print(per[["etiqueta", "canciones", "duracion_min", "positividad", "volumen_db"]].to_string(index=False))
print(corr)
