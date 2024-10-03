import requests
import os
from dotenv import load_dotenv
from app.models.models import Movie, User, UserInDB
from app.database.databaseConn import databaseConn 
from app.backend.users import obtener_usuario_por_username
from googletrans import Translator

def translate_to_english(text):
  """
  Translates text to English if it's not already in English.

  Args:
    text (str): The text to be translated.

  Returns:
    str: The translated text (English).
  """
  translator = Translator()

  # Detect the language of the input text
  detected_lang = translator.detect(text).lang

  # If the language is not English, translate to English
  if detected_lang != 'en':
    translation = translator.translate(text, dest='en').text
    return translation
  # If the language is English, return the text as-is
  else:
    return text
  
def search_movieDB(title):
    load_dotenv("dev.env")
    apikey = os.getenv("MOVIESAPIKEY")
    
    url = "https://imdb146.p.rapidapi.com/v1/find/"

    #translatedTitle = translate_to_english(title)

    querystring = {"query": title}

    headers = {
        "X-RapidAPI-Key": apikey,
        "X-RapidAPI-Host": "imdb146.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)
    response = response.json()

    results = response['titleResults']['results']
    return results

def guardar_pelicula(movie: Movie, username: str):
    # Crear conexión a la base de datos
    conn, cursor = databaseConn()

    # Obtener datos del usuario que está guardando la película
    try:
        user = obtener_usuario_por_username(username)
    except:
        return False
    
    # Verificar si la película ya existe en la base de datos
    try:
        cursor.execute("SELECT * FROM movies WHERE title = %s AND (user1 = %s OR user2 = %s)", (movie.title, user.username, user.relatedto))
        existing_movie = cursor.fetchone()
        if existing_movie:
            print("La película ya se encuentra en la base de datos.")
            return False
    except Exception as e:
        print(f"Error: {str(e)}")
        return False
    
    # Ejecutar la consulta SQL para guardar la película
    try:
        cursor.execute("INSERT INTO movies (title, release_date, type, genre, image_url, user1, user2) VALUES (%s, %s, %s, %s, %s, %s, %s)", (movie.title, movie.release, movie.type, movie.genre, movie.imageurl, user.username, user.relatedto))
        conn.commit()
        return True
    except Exception as e:
        print(f"Error: {str(e)}")
        return False

def get_all_movies(username: str):
    #crear conexión a la base de datos
    conn, cursor = databaseConn()

    # obtener datos del usuario
    try:
        user = obtener_usuario_por_username(username)
    except:
        return False

    # ejecutar la consulta SQL para obtener las películas
    try:
        cursor.execute("SELECT * FROM movies WHERE (user1 = %s OR user2 = %s)", (user.username, user.username,))
        movies = cursor.fetchall()
        return [Movie(id=movie[0], title=movie[1], release=movie[2], type=movie[3],genre=movie[4], imageurl=movie[5]) for movie in movies]
    except Exception as e:
        print(f"Error: {str(e)}")
        return False
    finally:
        conn.close()

def get_tvseries(username: str):
    #crear conexión a la base de datos
    conn, cursor = databaseConn()

    # obtener datos del usuario
    try:
        user = obtener_usuario_por_username(username)
    except:
        return False
    
    # ejecutar la consulta SQL para obtener las series de televisión
    try:
        cursor.execute("SELECT * FROM movies WHERE type = 'tvSeries' AND user1 = %s OR user2 = %s", (user.username, user.username))
        tvseries = cursor.fetchall()
        print(tvseries)
        return [Movie(id=tvserie[0], title=tvserie[1], release=tvserie[2], type=tvserie[3],genre=tvserie[4], imageurl=tvserie[5]) for tvserie in tvseries]
    except Exception as e:
        print(f"Error: {str(e)}")
        return False
    finally:
        conn.close()

def get_movies(username: str):
    #crear conexión a la base de datos
    conn, cursor = databaseConn()

    # obtener datos del usuario
    try:
        user = obtener_usuario_por_username(username)
    except:
        return False
    
    # ejecutar la consulta SQL para obtener las películas
    try:
        cursor.execute("SELECT * FROM movies WHERE (user1 = %s OR user2 = %s) AND type = 'movie'", (user.username, user.username,))
        movies = cursor.fetchall()
        return [Movie(id=movie[0], title=movie[1], release=movie[2], type=movie[3],genre=movie[4], imageurl=movie[5]) for movie in movies]
    except Exception as e:
        print(f"Error: {str(e)}")
        return False
    finally:
        conn.close()

def get_movie_by_id(id, username: str):
    #crear conexión a la base de datos
    conn, cursor = databaseConn()

    # obtener datos del usuario
    try:
        user = obtener_usuario_por_username(username)
    except:
        return False
    
    # ejecutar la consulta SQL para obtener la película por id
    try:
        cursor.execute("SELECT * FROM movies WHERE id = %s AND (user1 = %s OR user2 = %s)", (id, user.username, user.username))
        movie = cursor.fetchone()
        return Movie(id=movie[0], title=movie[1], release=movie[2], type=movie[3],genre=movie[4], imageurl=movie[5])
    except Exception as e:
        print(f"Error: {str(e)}")
        return False
    finally:
        conn.close()

def get_movie_by_genre(genre: str, username: str):
    #crear conexión a la base de datos
    conn, cursor = databaseConn()

    # obtener datos del usuario
    try:
        user = obtener_usuario_por_username(username)
    except:
        return False
    
    # ejecutar la consulta SQL para obtener la película por género
    try:
        cursor.execute("SELECT * FROM movies WHERE genre = %s AND (user1 = %s OR user2 = %s)", (genre, user.username, user.username))
        movies = cursor.fetchall()
        return [Movie(id=movie[0], title=movie[1], release=movie[2], type=movie[3],genre=movie[4], imageurl=movie[5]) for movie in movies]
    except Exception as e:
        print(f"Error: {str(e)}")
        return False
    finally:
        conn.close()

def get_random_movie(username: str):
    #crear conexión a la base de datos
    conn, cursor = databaseConn()

    # obtener datos del usuario
    try:
        user = obtener_usuario_por_username(username)
    except:
        return False
    
    # ejecutar la consulta SQL para obtener una película aleatoria
    try:
        cursor.execute("SELECT * FROM movies WHERE user1 = %s OR user2 = %s ORDER BY RANDOM() LIMIT 1", (user.username, user.username))
        movie = cursor.fetchone()
        return Movie(id=movie[0], title=movie[1], release=movie[2], type=movie[3],genre=movie[4], imageurl=movie[5])
    except Exception as e:
        print(f"Error: {str(e)}")
        return False
    finally:
        conn.close()

def get_random_movie_by_genre(genre: str, username: str):
    #crear conexión a la base de datos
    conn, cursor = databaseConn()

    # obtener datos del usuario
    try:
        user = obtener_usuario_por_username(username)
    except:
        return False
    
    # ejecutar la consulta SQL para obtener una película aleatoria por género
    try:
        cursor.execute("SELECT * FROM movies WHERE genre = %s AND (user1 = %s OR user2 = %s) ORDER BY RANDOM() LIMIT 1", (genre, user.username, user.username))
        movie = cursor.fetchone()
        return Movie(id=movie[0], title=movie[1], release=movie[2], type=movie[3],genre=movie[4], imageurl=movie[5])
    except Exception as e:
        print(f"Error: {str(e)}")
        return False
    finally:
        conn.close()

def get_random_tvseries(username: str):
    #crear conexión a la base de datos
    conn, cursor = databaseConn()

    # obtener datos del usuario
    try:
        user = obtener_usuario_por_username(username)
    except:
        return False
    
    # ejecutar la consulta SQL para obtener una serie de televisión aleatoria
    try:
        cursor.execute("SELECT * FROM movies WHERE user1 = %s OR user2 = %s AND type = 'tvSeries' ORDER BY RANDOM() LIMIT 1", (user.username, user.username))
        tvserie = cursor.fetchone()
        return Movie(id=tvserie[0], title=tvserie[1], release=tvserie[2], type=tvserie[3],genre=tvserie[4], imageurl=tvserie[5])
    except Exception as e:
        print(f"Error: {str(e)}")
        return False
    finally:
        conn.close()

def get_random_movie(username: str):
    #crear conexión a la base de datos
    conn, cursor = databaseConn()

    # obtener datos del usuario
    try:
        user = obtener_usuario_por_username(username)
    except:
        return False
    
    # ejecutar la consulta SQL para obtener una película aleatoria
    try:
        cursor.execute("SELECT * FROM movies WHERE user1 = %s OR user2 = %s AND type = 'movie' ORDER BY RANDOM() LIMIT 1", (user.username, user.username))
        movie = cursor.fetchone()
        return Movie(id=movie[0], title=movie[1], release=movie[2], type=movie[3],genre=movie[4], imageurl=movie[5])
    except Exception as e:
        print(f"Error: {str(e)}")
        return False
    finally:
        conn.close()

def get_random_movie_by_genre_and_type(movie: Movie, username: str):
    #crear conexión a la base de datos
    conn, cursor = databaseConn()

    # obtener datos del usuario
    try:
        user = obtener_usuario_por_username(username)
    except:
        return False
    
    # ejecutar la consulta SQL para obtener una película aleatoria por género y tipo
    try:
        cursor.execute("SELECT * FROM movies WHERE genre = %s AND type = %s AND (user1 = %s OR user2 = %s) ORDER BY RANDOM() LIMIT 1", (movie.genre, movie.type, user.username, user.username))
        movie = cursor.fetchone()
        return Movie(id=movie[0], title=movie[1], release=movie[2], type=movie[3],genre=movie[4], imageurl=movie[5])
    except Exception as e:
        print(f"Error: {str(e)}")
        return False
    finally:
        conn.close()

def search_movie_by_title_DB(title: str, username: str):
    #crear conexión a la base de datos
    conn, cursor = databaseConn()

    # obtener datos del usuario
    try:
        user = obtener_usuario_por_username(username)
    except:
        return False
    
    # ejecutar la consulta SQL para buscar una película por título
    try:
        cursor.execute("SELECT * FROM movies WHERE title LIKE %s AND (user1 = %s OR user2 = %s)", ('%' + title + '%', user.username, user.username))
        movie = cursor.fetchall()
        return [Movie(id=movie[0], title=movie[1], release=movie[2], type=movie[3],genre=movie[4], imageurl=movie[5]) for movie in movie]
    except Exception as e:
        print(f"Error: {str(e)}")
        return False
    finally:
        conn.close()

def update_movie_db(id: str, movie: Movie, username: str):
    #crear conexión a la base de datos
    conn, cursor = databaseConn()

    try:
        movie.id = None
    except:
        pass

    # obtener datos del usuario
    try:
        user = obtener_usuario_por_username(username)
    except:
        return False
    
    # validar que la película exista en la base de datos y que el usuario tenga permisos para actualizarla
    try:
        cursor.execute("SELECT * FROM movies WHERE id = %s AND (user1 = %s OR user2 = %s)", (id, user.username, user.username))
        existing_movie = cursor.fetchone()
        if not existing_movie:
            print("La película no existe en la base de datos o no tienes permisos para actualizarla.")
            return False
    except Exception as e:
        print(f"Error: {str(e)}")
        return False
    
    # ejecutar la consulta SQL para actualizar la película
    try:
        # buscar los datos del modelo que no sean None
        for data in movie.dict().items():
            if data[1] is not None:
                cursor.execute(f"UPDATE movies SET {data[0]} = %s WHERE id = %s", (data[1], id))
        conn.commit()
        return True


    except Exception as e:
        print(f"Error: {str(e)}")
        return False
    finally:
        conn.close()

def borrar_pelicula(id: str, user: str):
    #crear conexión a la base de datos
    conn, cursor = databaseConn()

    # validar que la película exista en la base de datos y que el usuario tenga permisos para eliminarla
    try:
        cursor.execute("SELECT * FROM movies WHERE id = %s AND (user1 = %s OR user2 = %s)", (id, user.username, user.username))
        existing_movie = cursor.fetchone()
        if not existing_movie:
            print("La película no existe en la base de datos o no tienes permisos para actualizarla.")
            return False
    except Exception as e:
        print(f"Error: {str(e)}")
        return False

    try:
        #eliminar datos de la base de datos
        cursor.execute("DELETE FROM movies WHERE id = %s", (id,))
        conn.commit()
        return True
    except Exception as e:
        print(f"Error: {str(e)}")
        return False
    finally:
        conn.close()

def get_movie_by_type(type: str, username: str):
    #crear conexión a la base de datos
    conn, cursor = databaseConn()

    # obtener datos del usuario
    try:
        user = obtener_usuario_por_username(username)
    except:
        return False
    
    # ejecutar la consulta SQL para obtener la película por tipo
    try:
        cursor.execute("SELECT * FROM movies WHERE type = %s AND (user1 = %s OR user2 = %s)", (type, user.username, user.username))
        movies = cursor.fetchall()
        return [Movie(id=movie[0], title=movie[1], release=movie[2], type=movie[3],genre=movie[4], imageurl=movie[5]) for movie in movies]
    except Exception as e:
        print(f"Error: {str(e)}")
        return False
    finally:
        conn.close()

def get_random_movie_by_type(type: str, username: str):
    #crear conexión a la base de datos
    conn, cursor = databaseConn()

    # obtener datos del usuario
    try:
        user = obtener_usuario_por_username(username)
    except:
        return False
    
    # ejecutar la consulta SQL para obtener una película aleatoria por tipo
    try:
        cursor.execute("SELECT * FROM movies WHERE type = %s AND (user1 = %s OR user2 = %s) ORDER BY RANDOM() LIMIT 1", (type, user.username, user.username))
        movie = cursor.fetchone()
        return Movie(id=movie[0], title=movie[1], release=movie[2], type=movie[3],genre=movie[4], imageurl=movie[5])
    except Exception as e:
        print(f"Error: {str(e)}")
        return False
    finally:
        conn.close()

