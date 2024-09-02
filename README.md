Documentación de Prueba Técnica: Sistema de Recomendación de Películas. 
Exploración y Preparación de datos:
El código utiliza la función pd.read_csv para leer dos archivos: 
ratings_path: Contiene las calificaciones que los usuarios dieron a las películas.
movies_path: Contiene información sobre las películas, incluyendo sus géneros.

Estructura de los DataFrames:
ratings: Contiene columnas como user_id, item_id, rating (calificación dada), y timestamp (marca de tiempo de la calificación).
movies: Contiene información sobre las películas, con columnas como item_id (identificador de la película), title (título), release_date (fecha de lanzamiento), y una serie de columnas binarias para indicar los géneros a los que pertenece cada película.
El filtrado y selección de columnas se llevó a cabo de la siguiente manera:
Selección de géneros: Se seleccionan solo las columnas que representan los géneros de las películas. Esto es importante porque estas columnas se utilizarán para calcular la similitud entre películas.
Filtrado del DataFrame: Se crea un nuevo DataFrame movies_gen que contiene solo las columnas seleccionadas. Este DataFrame tiene valores binarios (0 o 1) indicando si una película pertenece o no a un determinado género.

2. Desarrollo del Sistema de Recomendación
Generación de la matriz de similitud:
Similitud de cosenos: La función generate_cosine_similarity calcula la similitud entre las películas en términos de sus géneros usando la similitud de coseno. Esto genera una matriz donde cada elemento (i, j) indica cuán similares son la película i y la película j basándose en los géneros a los que pertenecen.
Mapeo de títulos de películas a índices:

movie_idx = dict(zip(movies['title'], list(movies.index)))
Diccionario de índices: Se crea un diccionario movie_idx que mapea cada título de película a su índice correspondiente en el DataFrame movies. Esto facilita la búsqueda de películas en la matriz de similitud.
Lo siguiente es hacer recomendaciones basadas en contenido mediante la función: 
get_content_based_recommendations
En donde se encuentran los siguientes procedimientos:
Búsqueda del título más cercano: La función movie_finder se utiliza para encontrar el título de película más cercano al que el usuario ingresa. Esto se hace utilizando la coincidencia difusa (fuzzy matching), que permite corregir errores de escritura o coincidencias aproximadas.
Índice de la película: Se obtiene el índice de la película correspondiente al título encontrado en el DataFrame movies.
Cálculo de similitud: Se recupera la fila correspondiente a esta película en la matriz de similitud (cosine_sim[idx]), y se ordenan las películas según su similitud con la película de referencia.
Selección de recomendaciones: Se seleccionan las n_recommendations películas más similares (excluyendo la película de referencia) y se devuelven sus títulos.


API de Flask
Definición de la Ruta:
@app.route('/'): Define la ruta principal (la página de inicio) de la aplicación cuando un usuario visita la raíz del sitio web ( http://localhost:5000/).
methods=['GET', 'POST']: Indica que esta ruta puede manejar tanto solicitudes GET como POST.
Si un usuario simplemente visita la página (http://localhost:5000/), Flask recibe una solicitud GET.
La función index() se ejecuta para manejar la solicitud, mostrando normalmente la página index.html.
Si hay un formulario en la página que se envía (como cuando el usuario ingresa un título de película y presiona "Buscar"), Flask recibe una solicitud POST. De nuevo, la función index() se ejecuta, pero esta vez manejará los datos enviados por el formulario, generando recomendaciones de películas en tu caso.

Función index:
Inicialización de variables: Se inicializa la variable recommendations como None. Esto servirá para almacenar las recomendaciones que se generen.
Manejo de solicitud POST:
Obtención del título de película: Si el usuario envía un formulario (solicitud POST), se extrae el nombre de la película que el usuario ingresó usando request.form['moviename'].
Generación de recomendaciones: Se llama a la función get_content_based_recommendations con el nombre de la película proporcionada por el usuario y otros parámetros necesarios. Esto genera una lista de películas recomendadas.
Conversión a lista: Las recomendaciones se convierten a una lista con .tolist() para que puedan ser fácilmente manipuladas en la plantilla HTML.
Renderización de la plantilla:
render_template('index.html', recommendations=recommendations): Renderiza la plantilla index.html y pasa la lista de recomendaciones a la plantilla para que pueda mostrarse en la página web.
Plantilla HTML (index.html)
Aunque el código específico de la plantilla index.html no se muestra, sabemos que es un archivo HTML que se encuentra en el directorio de plantillas de Flask (normalmente templates/). En esta plantilla:
Formulario de Entrada: Contiene un formulario donde el usuario puede ingresar el título de una película.
Muestra de Recomendaciones: Si hay recomendaciones generadas, estas se muestran en la página web utilizando las variables pasadas desde Flask (recommendations).
INSTRUCCIONES PARA LA EJECUCIÓN DEL SISTEMA:

Estructura del proyecto:

/Sistema de Recomendación
│
├── app.py                   # Archivo principal de Flask 
├── cosine_similarity.pkl    # Archivo pickle generado  
├── ml-100k                  # Carpeta con los archivos de MovieLens
│   ├── u.data               # Archivo de calificaciones
│   └── u.item               # Archivo de información de películas
│
└── templates
    └── index.html           # Plantilla HTML para la interfaz

Es necesario crear un ambiente virtual (venv) e instalar las librerías que alberga el documento de texto requirements.txt.

Una vez cumplidos estos pasos, en la terminal ubicada en el directorio del proyecto, ejecutamos el comando:

>> python3 app.py



