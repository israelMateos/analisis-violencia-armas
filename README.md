# Análisis de incidentes violentos con armas

Proyecto de prácticas de Minería de Datos (Grupo 4). El objetivo de este proyecto es analizar datos relacionados con incidentes violentos con armas en Estados Unidos.

## Configuración del entorno de desarrollo

Las dependencias del proyecto se encuentran en la carpeta `requirements` y están divididas según la aplicación. Para instalar las dependencias del proyecto de Minería de Datos, ejecuta el siguiente comando desde el directorio principal:

```console
$ pip install -r requirements/data_mining/requirements.txt
```

Las dependencias para las demás aplicaciones se instalan automáticamente al construir la infraestructura con Docker Compose.

El proyecto necesita **Python 3.11**: Python 3.12 no es compatible con el paquete `ydata_profiling`, y no se ha comprobado si en versiones anteriores de Python funciona).

Además, los ficheros de gran tamaño han sido almacenados utilizando **Git LFS**, por lo que debes instalarlo para poder acceder a ellos. Puedes descargarlo desde [git-lfs.com](https://git-lfs.com/). Una vez descargado, ejecuta el siguiente comando desde el directorio principal para asegurarte de que tienes los ficheros completos:

```console
$ git lfs pull
```

## Descarga de _datasets_ (Sistemas Multigentes)

Para descargar uno de los conjuntos de datos, es necesario proporcionar un _token_ de autenticación en Kaggle. Para ello, inicia sesión con tu cuenta en la web de Kaggle. Dirígete a la pestaña 'Account' de tu perfil de usuario y selecciona 'Create New Token'. Se descargará un fichero `kaggle.json`, que contiene tus credenciales para la API. Para que el _script_ de descarga de conjuntos de datos pueda leerlo, crea un fichero `.env` en el directorio principal de este repositorio, con el siguiente contenido:

```console
KAGGLE_CONFIG_DIR="el directorio donde esté contenido kaggle.json"
```

## Levantar la infraestructura (Sistemas Multigentes)

La infraestructura está construida con **Docker**, por lo que será necesario que lo instales siguiendo las instrucciones en [docs.docker.com/get-docker](https://docs.docker.com/get-docker/).

Dirígete al directorio `db` y ejecuta el siguiente comando desde el mismo:

```console
$ docker compose up --build -d
```

Este comando construirá las imágenes de Docker y levantará toda la infraestructura, procesando y cargando los datos en los distintos esquemas de la base de datos. Este comando es para la primera ejecución. Para posteriores, al ya estar construidas las imágenes, ejecuta el siguiente comando desde `db`:

```console
$ docker compose -d
```

## Integrantes
- Darío Andrés Fallavollita Figueroa
- Israel Mateos Aparicio Ruiz Santa Quiteria (junto con Sistemas Multiagentes)
- Fernando Potenciano Santiago
- Adrián Julián Ramos Romero
- Ignacio Rozas López (junto con Sistemas Multiagentes)
- Laurentiu Gheorghe Zlatar (junto con Sistemas Multiagentes)
