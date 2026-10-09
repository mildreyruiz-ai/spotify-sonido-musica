# Cómo ha cambiado el sonido de la música en 50 años (Python)

Análisis de más de 26.000 canciones de Spotify, de 1970 a 2019, con las características de audio de la propia plataforma: duración, positividad, volumen, bailabilidad y más. Es un proyecto de **análisis exploratorio y narración con datos**: cada gráfico cuenta una cosa y la frase de debajo dice qué significa.

**Página con el análisis:** https://mildreyruiz-ai.github.io/spotify-sonido-musica/web/
**Portfolio:** [mildreyruiz.com](https://mildreyruiz.com)

## Lo que dicen los datos

- Las canciones duran más de un minuto menos que a finales de los 80: la mediana pasa de 4:25 (1985-89) a 3:22 (2015-19).
- La música suena menos alegre desde 2010: la positividad media se mantenía entre 0,59 y 0,63 hasta 2009 y baja a 0,47 en 2015-19.
- El volumen medio sube de -10,2 dB (1970-74) a -6,2 dB (2010-14) y se estabiliza después.
- El género latino es el más alegre (0,60) y el EDM el menos (0,40).
- Ninguna característica del sonido explica la popularidad: la correlación más alta es 0,14.

## Qué no pueden decir estos datos

- Vienen de listas de Spotify de 2019-2020. Las canciones antiguas que aparecen son las que aún se escuchan, no todo lo que se publicó.
- Más de la mitad de las canciones son de 2015-19, y los periodos antiguos tienen pocas.
- La positividad y el volumen los calcula Spotify con un algoritmo.
- Correlación no es causa: los datos no explican por qué cambia la música.

## Estructura

```
data/spotify_songs_raw.csv   datos originales (TidyTuesday, 2020-01-21)
data/canciones.csv           canciones únicas, ya limpias
data/resultados.json         cifras que usa la página
python/01_limpieza.py        limpieza y deduplicado
python/02_analisis.py        medias por periodo y género, correlaciones
python/03_construir_web.py   genera web/index.html
python/04_verificacion.py    recalcula con otro método y compara
web/                         página con el análisis
```

## Limpieza (resumen)

De 32.833 filas originales se quitaron 5 sin nombre, 4.476 repetidas por aparecer en varias listas y 2.123 versiones duplicadas de la misma canción y artista. Quedan 26.229 canciones únicas.

## Cómo reproducirlo

```
pip install pandas numpy
python python/01_limpieza.py
python python/02_analisis.py
python python/03_construir_web.py
python python/04_verificacion.py
```

## Notas de desarrollo

Proyecto realizado con un flujo de trabajo asistido por IA (Claude) para la programación y la revisión. La elección del tema, las preguntas, la interpretación y las conclusiones son mías.

## Licencia y fuente

Código © Mildrey Ruiz. Datos: [TidyTuesday, 21 de enero de 2020](https://github.com/rfordatascience/tidytuesday/tree/main/data/2020/2020-01-21), canciones de Spotify obtenidas con el paquete spotifyr.
