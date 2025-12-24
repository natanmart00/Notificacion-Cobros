# Google Sheets → NTFY \| Sistema de Recordatorios de Pago

Este proyecto es una automatización desarrollada en Python que consume
datos desde una hoja de cálculo de Google Sheets, procesa información de
pagos mensuales de clientes y envía notificaciones inteligentes mediante
**ntfy** para recordar montos pendientes de pago.

El sistema está diseñado para ser simple, extensible y fácilmente
programable para ejecuciones periódicas.

------------------------------------------------------------------------

## Características

-   Lectura automática de datos desde Google Sheets en tiempo real
-   Identificación inteligente de clientes con pagos pendientes
-   Cálculo automático de deudas mensuales por cliente
-   Envío de notificaciones push mediante ntfy
-   Ejecución programable (diaria, semanal, etc.)
-   Gestión segura de credenciales mediante variables de entorno

------------------------------------------------------------------------

## Prerrequisitos

Antes de comenzar, asegúrate de contar con lo siguiente:

-   Python 3.11 o superior
-   Cuenta de Google con acceso a Google Sheets
-   Hoja de cálculo con la estructura esperada\
    (ver `doc_ejemplos/ejemplo_google_sheets`)
-   Una instancia de ntfy (ntfy.sh o servidor propio)
-   Conexión a internet para el acceso a APIs

------------------------------------------------------------------------

## Configuración inicial

### 1. Estructura de Google Sheets

La hoja de cálculo debe respetar **exactamente** la estructura definida
en:

    doc_ejemplos/ejemplo_google_sheets

Incluyendo nombres de pestañas y columnas.

------------------------------------------------------------------------

### 2. Configuración de la API´s de Google

1.  Accede a la Google Cloud Console
2.  Crea un proyecto nuevo o selecciona uno existente
3.  Habilita la **Google Sheets API** y la **Google Drive API**
4.  Crea una cuenta de servicio desde **APIs y Servicios →
    Credenciales**
5.  Asigna un nombre (ejemplo: `sheets-automation`)
6.  Otorga el rol **Editor** (o uno más restrictivo)

------------------------------------------------------------------------

### 3. Descarga de credenciales

1.  Selecciona la cuenta de servicio creada
2.  Accede a la pestaña **Claves**
3.  Crea una nueva clave en formato **JSON**
4.  Descarga el archivo y renómbralo como:

```
    credentials.json
```

------------------------------------------------------------------------

### 4. Configuración de ntfy

#### Opción A: ntfy.sh (recomendado)

-   Accede a https://ntfy.sh
-   Define un topic único (ejemplo: `recordatorios_pagos`)

#### Opción B: Servidor autoalojado

-   Sigue la documentación oficial de ntfy
-   Configura tu servidor y obtén la URL base

------------------------------------------------------------------------

## Instalación

1.  Clona el repositorio:

``` bash
git clone https://github.com/natanmart00/Notificacion-Cobros.git
```

2.  Instala las dependencias:

``` bash
pip install -r requirements.txt
```

3.  Configura las variables de entorno:

Renombra el archivo `.env_ejemplo` a `.env` y completa los valores.

### Variables de entorno

#### Google

``` env
GOOGLE_CREDENTIALS_PATH=ruta/al/archivo/credentials.json
SPREADSHEET_ID=id_de_tu_google_sheet
```

#### ntfy

``` env
NTFY_TEMA=nombre_de_tu_topic
```

4.  Archivos de configuración

-   Coloca `credentials.json` en la ruta indicada
-   Verifica que el archivo `.env` esté correctamente configurado

5.  Crea la hoja de calculo de google sheets tal y como está en el archivo Excel de ejemplo doc_ejemplos/ejemplo_google_sheets.xlsx

6. pega el codigo de doc_ejemplos/codigo_apps_script.txt en el menu extensiones -> Apps Scripts

7. en Apps Scripts ve al menu izquierdo y busca activadores -> agregar activador -> elegir que función ejecutar (selecciona AlEnviarFormulario) -> Tipo de evento(al enviar el formulario) -> Guardar

------------------------------------------------------------------------

## Uso

### Ejecución manual

``` bash
python -m src.main
```

------------------------------------------------------------------------

## Solución de problemas

### La hoja no es encontrada

**Error:** `La hoja no fue encontrada`

-   Verifica el nombre exacto de la pestaña en Google Sheets
-   Confirma que coincida con el valor configurado en `.env`

------------------------------------------------------------------------

### No llegan las notificaciones de ntfy

-   Verifica la conexión a internet
-   Confirma que el topic configurado sea correcto
-   Prueba acceder manualmente a:

```
    https://ntfy.sh/tu_topic
```

-   Revisa posibles bloqueos por firewall

------------------------------------------------------------------------

### No se detectan clientes con deuda

-   Verifica que la columna **Pagado** contenga valores `TRUE` o `FALSE`
-   Confirma que los nombres de las columnas sean correctos

------------------------------------------------------------------------

## Contribuciones

Si detectas un error o deseas proponer una mejora:

1.  Haz fork del proyecto
2.  Crea una rama: `git checkout -b feature/NuevaMejora`
3.  Realiza commit de tus cambios:
    `git commit -m "Descripción del cambio"`
4.  Sube la rama: `git push origin feature/NuevaMejora`
5.  Abre un Pull Request
