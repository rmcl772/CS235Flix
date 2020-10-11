from CS235Flix.domainmodel import actor, director


def grid_layout(data: list, column_count: int):
    grid = []

    for row in range(len(data) // column_count + 1):
        grid.append(data[row * column_count: (row * column_count) + column_count])

    return grid


def alphabetical_list(data: list, grid: int = False):
    alpha_list = {}

    for item in data:
        if type(item) == actor.Actor:
            name = item.actor_full_name
        elif type(item) == director.Director:
            name = item.director_full_name
        else:
            continue

        letter = name[0].lower()

        if letter not in alpha_list:
            alpha_list[letter] = []

        alpha_list[letter].append(item)

    if grid:
        for letter in alpha_list:
            alpha_list[letter] = grid_layout(alpha_list[letter], grid)

    return alpha_list
