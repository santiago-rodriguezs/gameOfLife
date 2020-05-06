#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May  1 16:44:44 2020

@author: santiago
"""

import pygame
import numpy as np
import time

pygame.init()

#screen set
width, height = 1000, 1000
screen = pygame.display.set_mode((height, width))

#color de fondo
bg = 25, 25, 25
screen.fill(bg)

#número de celdas
nxC, nyC = 25, 25
#dimensión de celdas
dimCW = width/nxC
dimCH = height/nyC

#estado de celdas: viva: 1, muerta: 0.
gameState = np.zeros((nxC, nyC))

#autómata palo
gameState[5, 3] = 1
gameState[5, 4] = 1
gameState[5, 5] = 1

#autómata movil
gameState[21, 21] = 1
gameState[22, 22] = 1
gameState[22, 23] = 1
gameState[21, 23] = 1
gameState[20, 23] = 1

#control de la ejecución del juego
pauseExect = False

#bucle de ejecución
while True:

    newGameState = np.copy(gameState)

    #actualización de fondo
    screen.fill(bg)
    time.sleep(0.1)

    #registro de eventos de teclado y mouse
    ev = pygame.event.get()

    for event in ev:

        #detecta si se persiona una tecla
        if event.type == pygame.KEYDOWN:
            pauseExect = not pauseExect

        #detecta si se presiona el mouse
        mouseClick = pygame.mouse.get_pressed()

        #cambia estado en lugar presionado
        if sum(mouseClick) > 0:
            posX, posY = pygame.mouse.get_pos()
            celX, celY = int(np.floor(posX/dimCW)), int(np.floor(posY/dimCH))
            newGameState[celX, celY] = not mouseClick[2]
    
    for y in range(0, nxC):
        for x in range(0, nyC):

            if not pauseExect:
            
                #calculo de numero de vecinos cercanos
                n_neigh = gameState[(x-1) % nxC, (y-1) % nyC] + \
                        gameState[(x) % nxC, (y-1) % nyC] + \
                        gameState[(x+1) % nxC, (y-1) % nyC] + \
                        gameState[(x-1) % nxC, (y) % nyC] + \
                        gameState[(x+1) % nxC, (y) % nyC] + \
                        gameState[(x-1) % nxC, (y+1) % nyC] + \
                        gameState[(x) % nxC, (y+1) % nyC] + \
                        gameState[(x+1) % nxC, (y+1) % nyC] 

                #regla 1: si una célula muerta tiene 3 vecinas vivas, revive.
                if gameState[x, y] == 0 and n_neigh == 3:
                    newGameState[x, y] = 1

                #regla2: si una célula viva tiene menos de 2 o mas de 3 vecinas vivas, muere.
                elif gameState[x, y] == 1 and (n_neigh < 2 or n_neigh > 3):
                    newGameState[x, y] = 0

            #creación de polígono de cada celda a dibujar
            poly = [((x) * dimCW, (y) * dimCH),
                    ((x+1) * dimCW, (y) * dimCH),
                    ((x+1) * dimCW, (y+1) * dimCH),
                    ((x) * dimCW, (y+1) * dimCH)]
            
            #dibuja la celda para cada par xy
            if newGameState[x, y] == 0:
                pygame.draw.polygon(screen, (128, 128, 128), poly, 1)
            else:
                pygame.draw.polygon(screen, (255, 255, 255), poly, 0)
    
    #actualización del estado del juego
    gameState = np.copy(newGameState)

    #actualización de pantalla
    pygame.display.flip()