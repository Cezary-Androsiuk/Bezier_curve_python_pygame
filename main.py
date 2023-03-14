import random
import pygame
from pygame.locals import *
import numpy as np
import copy

visible_control_points = False

# NOT EFFICIENT but scalable
# def nck(n, k):
#     return np.math.factorial(n) / (np.math.factorial(k) * np.math.factorial(n-k))
#
# def B(n, i, step):
#     # 0 ≤ step ≤ 1
#     return nck(n, i) * ((1-step) ** (n-i)) * step ** i
#
# def computePointFunctions(control_points, step):
#     x = 0
#     y = 0
#     i = 0
#     n = len(control_points)-1
#     for P in control_points:
#         x += B(n, i, step) * P[0]
#         y += B(n, i, step) * P[1]
#         i += 1
#     return x,y

def computePointFunction(control_points, step):
    point = [0,0]
    
    rev_step_p3 = ((1-step)**3)
    rev_step_p2 = ((1-step)**2)
    rev_step_p1 = ((1-step))

    step_p3 = ((step)**3)
    step_p2 = ((step)**2)
    step_p1 = ((step))

    for i in range(0,2):
        point[i] = \
            control_points[0][i] * (    rev_step_p3)             + \
            control_points[1][i] * (3 * rev_step_p2) * (step_p1) + \
            control_points[2][i] * (3 * rev_step_p1) * (step_p2) + \
            control_points[3][i]                     * (step_p3)

    return point



def drawBezierCurve(points, pointsColor = (255, 65, 65), curveColor = (170, 170, 170)):
    # draw single curve
    for step in np.arange(0, 1, 0.001):
        stepPoint = computePointFunction(points, step)
        pygame.draw.circle(screen, curveColor, stepPoint, 1)

    # draw control points
    if visible_control_points:
        for point in points:
            pygame.draw.circle(screen, pointsColor, [point[0],point[1]], 4)


def updatePoints(object, target):
    for (object_group, points_group) in zip(object, target):
        for (real, expected) in zip(object_group, points_group):
            x_error = expected[0] - real[0]
            y_error = expected[1] - real[1]

            real[2] += x_error / 50
            real[3] += y_error / 50


            real[0] += real[2] + x_error / 10
            real[1] += real[3] + y_error / 10


if __name__=='__main__':
    # Cezary Androsiuk
    pygame.init()
    pygame.font.init()
    font = pygame.font.SysFont('lato', 25)
    screen = pygame.display.set_mode((1200, 720))
    clock = pygame.time.Clock()

    # [ x_po, y_pos, x_velocity, y_velocity]
    points_C = [
        [ # curveOutline
            [450, 125, 0, 0], [190, 125, 0, 0], [190, 500, 0, 0], [450, 500, 0, 0],
        ],
        [ # curveInline
            [450, 175, 0, 0], [260, 175, 0, 0], [260, 450, 0, 0], [450, 450, 0, 0]
        ],
        [ # topPlug
            [450, 125, 0, 0], [500, 125, 0, 0], [500, 175, 0, 0], [450, 175, 0, 0]
        ],
        [ # bottomPlug
            [450, 500, 0, 0], [500, 500, 0, 0], [500, 450, 0, 0], [450, 450, 0, 0]
        ]
    ]
    points_A = [
        [ # outer left side
            [650, 470, 0, 0], [650, 470, 0, 0], [750, 150, 0, 0], [750, 150, 0, 0]
        ],
        [ # outer right side
            [900, 470, 0, 0], [900, 470, 0, 0], [800, 150, 0, 0], [800, 150, 0, 0]
        ],
        [ # top plug
            [750, 150, 0, 0], [760, 120, 0, 0], [790, 120, 0, 0], [800, 150, 0, 0]
        ],
        [ # bottom left plug
            [650, 470, 0, 0], [640, 500, 0, 0], [695, 505, 0, 0], [700, 470, 0, 0]
        ],
        [ # bottom right plug
            [900, 470, 0, 0], [910, 500, 0, 0], [855, 505, 0, 0], [850, 470, 0, 0]
        ],
        [ # inner left side
            [700, 470, 0, 0], [725, 375, 0, 0], [725, 375, 0, 0], [775, 375, 0, 0]
        ],
        [ # inner right side
            [850, 470, 0, 0], [825, 375, 0, 0], [825, 375, 0, 0], [775, 375, 0, 0]
        ],
        [ # inside left side
            [757, 290, 0, 0], [745, 325, 0, 0], [745, 325, 0, 0], [775, 325, 0, 0]
        ],
        [ # inside right side
            [793, 290, 0, 0], [805, 325, 0, 0], [805, 325, 0, 0], [775, 325, 0, 0]
        ],
        [ # inside top side
            [757, 290, 0, 0], [775, 230, 0, 0], [775, 230, 0, 0], [793, 290, 0, 0]
        ]
    ]
    object_letter_A = copy.deepcopy(points_A)
    object_letter_C = copy.deepcopy(points_C)
    velocity = 0

    text1 = font.render("press 'p' to show control points", False, (170, 170, 170))
    text2 = font.render("press SPACE to give each control point random value on screen (they are constantly attracted "
                        "to the start position)", False, (170, 170, 170))
    text3 = font.render("you can hold space for +/- 2s to have nice results", False, (170, 170, 170))

    run = True
    while run:
        clock.tick(30)

        if visible_control_points:
            control_points_text = font.render("(True)", False, (65, 255, 65))
            control_points_text.set_alpha(80)
        else:
            control_points_text = font.render("(False)", False, (255, 65, 65))
            control_points_text.set_alpha(100)

        for event in pygame.event.get():
            if event.type == QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    if visible_control_points:
                        visible_control_points = False
                    else:
                        visible_control_points = True
                if event.key == pygame.K_ESCAPE:
                    run = False

        key = pygame.key.get_pressed()
        if key[pygame.K_SPACE]:
            for group in object_letter_C:
                for point in group:
                    point[0] = random.randint(0, 1200)
                    point[1] = random.randint(0, 600)
            for group in object_letter_A:
                for point in group:
                    point[0] = random.randint(0, 1200)
                    point[1] = random.randint(0, 600)

        updatePoints(object_letter_C, points_C)
        updatePoints(object_letter_A, points_A)

        screen.fill((30, 30, 30))

        drawBezierCurve(object_letter_C[0])
        drawBezierCurve(object_letter_C[1])
        drawBezierCurve(object_letter_C[2])
        drawBezierCurve(object_letter_C[3])

        drawBezierCurve(object_letter_A[0])
        drawBezierCurve(object_letter_A[1])
        drawBezierCurve(object_letter_A[2])
        drawBezierCurve(object_letter_A[3])
        drawBezierCurve(object_letter_A[4])
        drawBezierCurve(object_letter_A[5])
        drawBezierCurve(object_letter_A[6])
        drawBezierCurve(object_letter_A[7])
        drawBezierCurve(object_letter_A[8])
        drawBezierCurve(object_letter_A[9])

        # align_line = [
        #     [
        #         # line top
        #         [0, 125],
        #         [0, 125],
        #         [1200, 125],
        #         [1200, 125]
        #     ],
        #     [
        #         # line bottom
        #         [0, 500],
        #         [0, 500],
        #         [1200, 500],
        #         [1200, 500]
        #     ]
        # ]
        # drawBezierCurve(align_line[0], (255, 0, 0), (100, 0, 0))
        # drawBezierCurve(align_line[1], (255, 0, 0), (100, 0, 0))

        screen.blit(text1, (10, 720 - 20 - 5 - 20 - 5 - 20 - 10))
        screen.blit(control_points_text, (280, 720 - 20 - 5 - 20 - 5 - 20 - 10))

        screen.blit(text2, (10, 720 - 20 - 5 - 20 - 10))

        screen.blit(text3, (10, 720 - 20 - 10))
        pygame.display.update()
    pygame.quit()
    exit()
