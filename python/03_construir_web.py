"""Inserta data/resultados.json en web/template.html y genera web/index.html."""
import json, pathlib
R = pathlib.Path(__file__).resolve().parent.parent
datos = json.loads((R / "data" / "resultados.json").read_text(encoding="utf-8"))
t = (R / "web" / "template.html").read_text(encoding="utf-8")
(R / "web" / "index.html").write_text(t.replace("__DATA__", json.dumps(datos, ensure_ascii=False)), encoding="utf-8")
print("web/index.html generado")
