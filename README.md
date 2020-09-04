# python-movie-collection-checker


[![Build Status](https://drone.mateusz.ovh/api/badges/mateusz/python-movie-collection-checker/status.svg)](https://drone.mateusz.ovh/mateusz/python-movie-collection-checker)


A python script that will check existing movies and will tell you if you are missing any movies from collections you already have.

## Usage

```python
python3 src/python-movie-collection-checker/get-list-of-movies.py
```

# Configuration:
You need to edit file config.py accordingly.


# Info
Script will produce file missing-movies.txt with the output.

Script will skip movies that are not released yet or don't have release date in TMDB.
