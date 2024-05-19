from fastapi import APIRouter, Depends, HTTPException
from app.backend.auth import get_current_user
from app.models.models import User, Movie
from app.backend.movies import *

routerMovie = APIRouter()

@routerMovie.post("/save_movie/")
def save_movie(movie: Movie, current_user: User = Depends(get_current_user)):
    try:
        if guardar_pelicula(movie, current_user.username):
            return {"status": "success", "message": "Movie saved"}
        else:
            raise HTTPException(status_code=400, detail="Error saving movie")
    except:
        raise HTTPException(status_code=400, detail="Error saving movie")
    
@routerMovie.get("/search_movie/")
def search_movie(movie: Movie, current_user: User = Depends(get_current_user)):
    try:
        results = search_movieDB(movie.title)
        if results:
            return results
        else:
            raise HTTPException(status_code=400, detail="No movies found")
    except:
        raise HTTPException(status_code=400, detail="Error searching movie")
    
@routerMovie.get("/movies/all")
def read_movies_me(current_user: User = Depends(get_current_user)):
    try:
        movies = get_all_movies(current_user.username)
        if movies:
            return movies
        else:
            raise HTTPException(status_code=400, detail="No movies found")
    except:
        raise HTTPException(status_code=400, detail="Error reading movies")
    
@routerMovie.get("/movies/all/tvseries/")
def read_tvseries(current_user: User = Depends(get_current_user)):
    try:
        movies = get_tvseries(current_user.username)
        if movies:
            return movies
        else:
            raise HTTPException(status_code=400, detail="No movies found")
    except:
        raise HTTPException(status_code=400, detail="Error reading movies")
    
@routerMovie.get("/movies/all/movies/")
def read_movies(current_user: User = Depends(get_current_user)):
    try:
        movies = get_movies(current_user.username)
        if movies:
            return movies
        else:
            raise HTTPException(status_code=400, detail="No movies found")
    except:
        raise HTTPException(status_code=400, detail="Error reading movies")
    
@routerMovie.get("/movies/all/by_genre/")
def read_movies_by_genre(movie: Movie, current_user: User = Depends(get_current_user)):
    try:
        movies = get_movie_by_genre(movie.genre, current_user.username)
        if movies:
            return movies
        else:
            raise HTTPException(status_code=400, detail="No movies found")
    except:
        raise HTTPException(status_code=400, detail="Error reading movies")
    
@routerMovie.get("/movies/random/")
def read_random_movie(current_user: User = Depends(get_current_user)):
    try:
        movie = get_random_movie(current_user.username)
        if movie:
            return movie
        else:
            raise HTTPException(status_code=400, detail="No movie found")
    except:
        raise HTTPException(status_code=400, detail="Error reading movie")
    
@routerMovie.get("/movies/random/tvseries/")
def read_random_tvseries(current_user: User = Depends(get_current_user)):
    try:
        movie = get_random_tvseries(current_user.username)
        if movie:
            return movie
        else:
            raise HTTPException(status_code=400, detail="No movie found")
    except:
        raise HTTPException(status_code=400, detail="Error reading movie")
    
@routerMovie.get("/movies/random/movies/")
def read_random_movies(current_user: User = Depends(get_current_user)):
    try:
        movie = get_random_movie(current_user.username)
        if movie:
            return movie
        else:
            raise HTTPException(status_code=400, detail="No movie found")
    except:
        raise HTTPException(status_code=400, detail="Error reading movie")
    
@routerMovie.get("/movies/random/by_genre/")
def read_random_movie_by_genre(movie: Movie, current_user: User = Depends(get_current_user)):
    try:
        movie = get_random_movie_by_genre(movie.genre, current_user.username)
        if movie:
            return movie
        else:
            raise HTTPException(status_code=400, detail="No movie found")
    except:
        raise HTTPException(status_code=400, detail="Error reading movie")
    
@routerMovie.get("/movies/random/by_genre_and_type/")
def read_random_movie_by_genre_and_type(data: Movie, current_user: User = Depends(get_current_user)):
    try:
        movie = get_random_movie_by_genre_and_type(data, current_user.username)
        if movie:
            return movie
        else:
            raise HTTPException(status_code=400, detail="No movie found")
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail="Error reading movie")

@routerMovie.get("/movies/byID/")
def read_movie_byID(movie: Movie, current_user: User = Depends(get_current_user)):
    try:
        movie = get_movie_by_id(movie.id, current_user.username)
        if movie:
            return movie
        else:
            raise HTTPException(status_code=400, detail="No movie found")
    except:
        raise HTTPException(status_code=400, detail="Error reading movie")
    
@routerMovie.get("/movies/byTitle/")
def read_movie_byTitle(movie: Movie, current_user: User = Depends(get_current_user)):
    try:
        movie = search_movie_by_title_DB(movie.title, current_user.username)
        if movie:
            return movie
        else:
            raise HTTPException(status_code=400, detail="No movie found")
    except:
        raise HTTPException(status_code=400, detail="Error reading movie")
    
@routerMovie.get("/movies/byType/")
def read_movie_byType(movie: Movie, current_user: User = Depends(get_current_user)):
    try:
        movie = get_movie_by_type(movie.type, current_user.username)
        if movie:
            return movie
        else:
            raise HTTPException(status_code=400, detail="No movie found")
    except:
        raise HTTPException(status_code=400, detail="Error reading movie")
    
@routerMovie.get("/movies/random/byType/")
def read_random_movie_byType(movie: Movie, current_user: User = Depends(get_current_user)):
    try:
        movie = get_random_movie_by_type(movie.type, current_user.username)
        if movie:
            return movie
        else:
            raise HTTPException(status_code=400, detail="No movie found")
    except:
        raise HTTPException(status_code=400, detail="Error reading movie")

@routerMovie.put("/update_movie/{id}/")
def update_movie(id: int, movie: Movie, current_user: User = Depends(get_current_user)):
    try:
        if update_movie(id, movie, current_user.username):
            return {"status": "success", "message": "Movie updated"}
        else:
            raise HTTPException(status_code=400, detail="Error updating movie")
    except:
        raise HTTPException(status_code=400, detail="Error updating movie")
    
@routerMovie.delete("/delete_movie/{id}/")
def delete_movie(id: int, current_user: User = Depends(get_current_user)):
    try:
        if borrar_pelicula(id):
            return {"status": "success", "message": "Movie deleted"}
        else:
            raise HTTPException(status_code=400, detail="Error deleting movie")
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail="Error deleting movie")
    
