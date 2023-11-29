from os import walk

import pygame.image


def import_folder(path):
    surface_list = []

    for _, _, img_files in walk(path):
        for image in img_files:
            full_path = path + "/" + image
            image_surf = pygame.transform.scale(pygame.image.load(full_path).convert_alpha(), (100, 100))
            surface_list.append(image_surf)

    print(surface_list)

    return surface_list
