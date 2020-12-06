import maya.cmds as cmds
import sys

body = []
division = 20
radius = [2, 1.7, 1.3]
pos = [0, 2.4, 4.8]

def body_instantiate():
    """Fonction pour créer les différents éléments du corp"""

    if len(pos) != len(radius):
        print("<ERROR (body_instantiate): Nombre d'éléments non concordant [{} rayons pour {} positions]>".format(len(radius), len(pos)))
        sys.exit()

    for i, r in enumerate(radius):
        name = "body_sphere_{}".format(i)

        print "<Création de la sphère: {} de rayon {}>".format(name, r)
        body.append(cmds.polySphere(n=name, sx=division, sy=division, r=r))


if __name__ == "__main__":
    body_instantiate()