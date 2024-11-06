def favorite_film():
    films = []
    print("What is your favorite film?")
    film = input("Enter films: ")
    films.append(film)
    for x in films:
        print(f"One of your favorite films is: {x}")

favorite_film()

## Call the function, making sure to include a film title 
## as an argument in the function call. Ask for user input 
## for the name of the film