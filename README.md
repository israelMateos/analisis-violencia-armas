# Análisis de incidentes violentos con armas

Proyecto de prácticas de Minería de Datos (Grupo 4). El objetivo de este proyecto es analizar datos relacionados con incidentes violentos con armas en Estados Unidos.

## Configuración del entorno de desarrollo

Las dependencias del proyecto se encuentran en el fichero `requirements.txt`. Para instalarlas, ejecuta el siguiente comando desde el directorio principal:

```console
pip install -r requirements.txt
```

Además, los ficheros de gran tamaño han sido almacenados utilizando **Git LFS**, por lo que debes instalarlo para poder acceder a ellos. Puedes descargarlo desde [https://git-lfs.com/](https://git-lfs.com/).
## Descarga de _datasets_

Para descargar uno de los conjuntos de datos, es necesario proporcionar un _token_ de autenticación en Kaggle. Para ello, inicia sesión con tu cuenta en la web de Kaggle. Dirígete a la pestaña 'Account' de tu perfil de usuario y selecciona 'Create New Token'. Se descargará un fichero `kaggle.json`, que contiene tus credenciales para la API. Para que el _script_ de descarga de conjuntos de datos pueda leerlo, crea un fichero `.env` en el directorio principal de este repositorio, con el siguiente contenido:

```console
KAGGLE_CONFIG_DIR="el directorio donde esté contenido kaggle.json"
```

## Integrantes
- Darío Andrés Fallavollita Figueroa
- Israel Mateos Aparicio Ruiz Santa Quiteria
- Fernando Potenciano Santiago
- Adrián Julián Ramos Romero
- Ignacio Rozas López
- Laurentiu Gheorghe Zlatar
