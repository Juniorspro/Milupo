# Guion del tráiler: quién habla, qué dice y en qué segundo empieza.
GUION = {
  'en': [
    (0.35, 'narrador', 'Beyond the clouds... lies a sky without limits.'),
    (3.35, 'dragon',   'Hold on tight, little rider.'),
    (5.25, 'jinete',   'I was born for this!'),
    (8.75, 'narrador', 'Soar through canyons of stone and fire.'),
    (12.25, 'narrador', 'Burn the enemy fleet.'),
    (15.55, 'narrador', 'Dive at full speed.'),
    (14.95, 'jinete',  'Here we go!'),
    (18.35, 'narrador', 'Turn their arrows against them.'),
    (21.15, 'dragon',  "Is that all they've got?"),
    (22.75, 'jinete',  'Not even close!'),
    (24.55, 'narrador', 'Twenty levels. One legend.'),
    (27.55, 'narrador', 'Ride the dragon. Rule the sky.'),
    (30.55, 'narrador', 'Dragon Rider. Play now, on Rezona.'),
  ],
  'es': [
    (0.35, 'narrador', 'Más allá de las nubes... hay un cielo sin límites.'),
    (3.35, 'dragon',   'Sujétate fuerte, jinete.'),
    (5.2, 'jinete',    '¡Nací para esto!'),
    (8.75, 'narrador', 'Vuela entre cañones de piedra y fuego.'),
    (12.25, 'narrador', 'Quema la flota enemiga.'),
    (15.55, 'narrador', 'Ataca en picada.'),
    (14.85, 'jinete',  '¡Allá vamos!'),
    (18.25, 'narrador', 'Devuélveles sus propias flechas.'),
    (21.15, 'dragon',  '¿Eso es todo lo que tienen?'),
    (22.75, 'jinete',  '¡Ni de cerca!'),
    (24.55, 'narrador', 'Veinte niveles. Una leyenda.'),
    (27.55, 'narrador', 'Monta el dragón. Domina el cielo.'),
    (30.55, 'narrador', 'Dragon Rider. Juega ya en Rezona.'),
  ],
}
# Voz de Piper, velocidad (más alto = más lento) y procesamiento de cada personaje
VOCES = {
  'en': {'narrador': ('en_US-ryan-high', 1.12), 'dragon': ('en_GB-northern_english_male-medium', 1.15), 'jinete': ('en_US-hfc_female-medium', 0.95)},
  'es': {'narrador': ('es_MX-ald-medium', 1.08), 'dragon': ('es_ES-davefx-medium', 1.12), 'jinete': ('es_AR-daniela-high', 0.95)},
}
EFECTOS = {   # cadena de filtros de ffmpeg para cada personaje
  'narrador': {'en': 'rubberband=pitch=0.89:formant=preserved', 'es': 'rubberband=pitch=0.84:formant=preserved',
               'comun': 'highpass=f=60,equalizer=f=120:t=q:w=1:g=4,equalizer=f=3500:t=q:w=1.5:g=2,acompressor=threshold=-20dB:ratio=4:attack=5:release=120,aecho=0.8:0.5:40:0.12'},
  'dragon':   {'en': 'rubberband=pitch=0.72', 'es': 'rubberband=pitch=0.70',
               'comun': 'highpass=f=40,equalizer=f=90:t=q:w=1:g=7,lowpass=f=6000,acompressor=threshold=-22dB:ratio=5:attack=5:release=150,aecho=0.8:0.6:60|120:0.25|0.15'},
  'jinete':   {'en': 'anull', 'es': 'anull',
               'comun': 'highpass=f=120,equalizer=f=4000:t=q:w=1.5:g=3,acompressor=threshold=-20dB:ratio=3:attack=5:release=100,aecho=0.8:0.4:30:0.1'},
}
