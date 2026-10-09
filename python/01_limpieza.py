"""Limpia el CSV de Spotify (TidyTuesday, 2020-01-21) y guarda data/canciones.csv."""
import pandas as pd, pathlib
RAIZ = pathlib.Path(__file__).resolve().parent.parent
d = pd.read_csv(RAIZ / "data" / "spotify_songs_raw.csv")
n0 = len(d)

# 1) Quitar filas sin nombre o artista
d = d.dropna(subset=["track_name", "track_artist"])
n_sin_nombre = n0 - len(d)

# 2) La misma canción aparece en varias listas: nos quedamos con una fila por track_id
n1 = len(d)
d = d.drop_duplicates("track_id")
n_dup_id = n1 - len(d)

# 3) Misma canción y artista con distinto id (versiones del álbum, reediciones): la de más popularidad
n2 = len(d)
d = d.sort_values("track_popularity", ascending=False).drop_duplicates(["track_name", "track_artist"])
n_dup_nombre = n2 - len(d)

# 4) Fecha de lanzamiento: algunas vienen solo con el año
d["fecha"] = pd.to_datetime(d["track_album_release_date"], format="mixed", errors="coerce")
d["anio"] = d["fecha"].dt.year
assert d["anio"].notna().all()

d["duracion_min"] = d["duration_ms"] / 60000
d = d.rename(columns={"track_artist": "artista", "track_name": "cancion", "track_popularity": "popularidad",
                      "playlist_genre": "genero", "danceability": "bailable", "energy": "energia",
                      "valence": "positividad", "acousticness": "acustica", "loudness": "volumen_db",
                      "speechiness": "habla", "tempo": "tempo"})
cols = ["cancion", "artista", "anio", "genero", "popularidad", "duracion_min", "bailable", "energia",
        "positividad", "acustica", "volumen_db", "habla", "tempo"]
d[cols].sort_values(["anio", "artista", "cancion"]).to_csv(RAIZ / "data" / "canciones.csv", index=False)
print(f"filas originales {n0} · sin nombre {n_sin_nombre} · duplicadas por id {n_dup_id} · "
      f"duplicadas por nombre+artista {n_dup_nombre} · canciones únicas {len(d)}")
