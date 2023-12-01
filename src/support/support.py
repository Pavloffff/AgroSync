from os import walk

import pygame.image


def import_image(path, size: tuple[int, int]):
    return pygame.transform.scale(pygame.image.load(path).convert_alpha(), size)


def import_folder(path, size: tuple[int, int]):
    surface_list = []

    for _, _, img_files in walk(path):
        for image in img_files:
            full_path = path + "/" + image
            image_surf = import_image(full_path, size)
            surface_list.append(image_surf)

    return surface_list


