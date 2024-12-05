## Características del Dataset

- **MesListing**: Mes en que se listó la propiedad.
- **year**: Año en que se listó la propiedad.
- **precio_pesos_constantes**: Precio de la propiedad ajustado a pesos constantes. Target.

## Caracteristica de id y localización:
- **id_grid**: ID del polígono.
- **LONGITUDE**: Longitud del centroide del polígono asignado a la propiedad.
- **LATITUDE**: Latitud del centroide del polígono asignado a la propiedad.
- **ITE_ADD_CITY_NAME**: Nombre de la ciudad donde se encuentra la propiedad.
- **ITE_ADD_STATE_NAME**: Nombre de la provincia donde se encuentra la propiedad.
- **ITE_ADD_NEIGHBORHOOD_NAME**: Nombre del barrio donde se encuentra la propiedad.

##Caracteristicas estructurales:
- **TIPOPROPIEDAD**: Tipo de propiedad (ej. departamento, casa, etc.).
- **STotalM2**: Superficie total de la propiedad en metros cuadrados.
- **SConstrM2**: Superficie construida de la propiedad en metros cuadrados.
- **Dormitorios**: Cantidad de dormitorios en la propiedad.
- **Banos**: Cantidad de baños en la propiedad.
- **Ambientes**: Cantidad de ambientes en la propiedad.
- **Amoblado**: Indica si la propiedad está amoblada.
- **Antiguedad**: Antigüedad de la propiedad en años.
- **ITE_TIPO_PROD**: Estado de la propiedad; los valores posibles son 'U' (usado), 'N' (nuevo), y 'S' (sin clasificación).

## Caracteristicas no estructurales:
- **Cisterna**: Indica si la propiedad tiene cisterna.
- **AccesoInternet**: Indica si hay acceso a Internet en la propiedad.
- **Calefaccion**: Indica si hay calefacción en la propiedad.
- **AireAC**: Indica si hay aire acondicionado.
- **Estacionamiento**: Indica si hay estacionamiento.
- **Chimenea**: Indica si hay chimenea.
- **Cocheras**: Indica si hay cocheras. (NO one hot encoding)
- **SistContraIncendios**: Indica si hay sistema contra incendios.

## Caracteristicas de contexto de la propiedad:

- **Gimnasio**: Indica si hay gimnasio en la propiedad.
- **Laundry**: Indica si hay lavandería en la propiedad.
- **Recepcion**: Indica si hay recepción en la propiedad.
- **AreaParrillas**: Indica si hay área de parrillas.
- **CanchaTennis**: Indica si hay cancha de tenis.
- **AreaCine**: Indica si hay área de cine.
- **LocalesComerciales**: Indica si hay locales comerciales en la propiedad.
- **Ascensor**: Indica si hay ascensor en la propiedad.
- **SalonFiestas**: Indica si hay salón de fiestas.
- **Seguridad**: Indica si hay seguridad en la propiedad.
- **Pileta**: Indica si hay pileta.
- **Jacuzzi**: Indica si hay jacuzzi.
- **AreaJuegosInfantiles**: Indica si hay área de juegos infantiles.
- **BusinessCenter**: Indica si hay un centro de negocios en la propiedad.
- **SalonDeUsosMul**: Indica si hay salón de usos múltiples.
- **PistaJogging**: Indica si hay pista de jogging.
- **EstacionamientoVisitas**: Indica si hay estacionamiento para visitas.
- **Lobby**: Indica si hay lobby en la propiedad.
- **LocalesComerciales**: Indica si hay locales comerciales en la propiedad.

## Fuera de uso

- **SitioOrigen**: Origen del anuncio (ej. sitio web, aplicación).