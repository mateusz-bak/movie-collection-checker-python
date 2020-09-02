import os


def get_list_of_movies(movies_location):
    subfolders = [f.path for f in os.scandir(movies_location) if f.is_dir()]

    for x in range(0, len(subfolders)):
        subfolders[x] = subfolders[x].replace("./movies/", "")

    return subfolders


def separate_titles_and_years(subfolders):
    for x in range(0, len(subfolders)):
        subfolders[x] = subfolders[x].split("(")
        subfolders[x][1] = subfolders[x][1][:-1]

    return subfolders


if __name__ == '__main__':

    movies_location = "./movies"

    subfolders = get_list_of_movies(movies_location)

    separate_titles_and_years(subfolders)

    for x in subfolders:
        print(x)
