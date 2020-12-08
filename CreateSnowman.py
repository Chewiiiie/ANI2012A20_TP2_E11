import sys
import random
import maya.cmds as cmds

# Definition des constantes
prefix = "Snowman_"
subDivisionsX = 13
subDivisionsY = 13
subDivisionsZ = 13
offset = [0, 2, 0]
snowmanID = random.randint(235, 846)
sets = []

# Definition des parties du corps
bodyParts = []
bodyRadius = [2, 1.7, 1.3]
bodyPositions = [(0, 0, 0), (0, 2.4, 0), (0, 4.8, 0)]

# Definition des boutons
buttons = []
buttonsRadius = [0.178, 0.178, 0.178]
buttonsPositions = [(1.42, 3.13, 0), (1.58, 2.5, 0), (1.5, 1.86, 0)]

# Definition des yeux
eyes = []
eyesRadius = [0.23, 0.23]
eyesPositions = [(1.1, 5.08, 0.472), (1.1, 5.08, -0.472)]

# Definition du chapeau
hatParts = []
hatDimensions = [(1, 2), (1.5, 0.25)]
hatPositions = [(0, 6.66, 0.6), (0, 5.7, 0.34)]
hatRotations = [(15, 0, 0), (15, 0, 0)]

# Definition des bras
arms = []
armDimensions = [(0.1, 2), (0.1, 2)]
armPositions = [(0, 1.8, 2), (0, 1.8, -2)]
armRotations = [(-27, 0, 0), (27, 0, 0)]

# Definition du nez
nose = []
noseDimensions = [(0.3, 1.65)]
nosePositions = [(1.87, 4.5, 0)]
noseRotations = [(0, 0, -90)]

# Definition de l'echarpe
scarf = []
scarfDimensions = [(1, 0.5)]
scarfPositions = [(0, 3.7, 0)]
scarfRotations = [(0, 0, 0)]


def attribute_has(node_name, attribute_name):
    """fonction qui valide l'existence d'un attribut sur un noeud"""

    # valider si le noeud possede l'attribut
    if cmds.objExists("%s.%s" % (node_name, attribute_name)):
        print("<Le noeud '{}' possede l'attribut '{}'>".format(node_name, attribute_name))
        return True
    else:
        print("<Le noeud '{}' ne possede pas l'attribut '{}'>".format(node_name, attribute_name))
        return False


def attribute_add(node_name, attribute_name):
    """fonction pour ajouter d'un nouvel attribut numerique sur un noeud"""

    # valider si le noeud possede l'attribut
    if not attribute_has(node_name, attribute_name):
        # ajouter un attribut sur le noeud
        cmds.addAttr(node_name, longName=attribute_name)
        print("<Le noeud '{}' possede maintenant l'attribut '{}'>".format(node_name, attribute_name))
    else:
        print("<Fonction 'attribute_add' annulee, car l'attribut '{}' existe deja pas sur le noeud '{}'>".format(
            attribute_name, node_name))


def attribute_remove(node_name, attribute_name):
    """fonction pour supprimer un attribut assigne �  un noeud"""

    # valider si l'attribut existe dej�  sur le noeud
    if attribute_has(node_name, attribute_name):
        # supprimer l'attribut
        cmds.deleteAttr(node_name, attribute=attribute_name)
        print("<L'attribut '{}' a bien ete enleve du noeud '{}'>".format(node_name, attribute_name))
    else:
        print("<fonction 'attribute_remove' annulee, car l'attribut '{}' n'existe pas sur le noeud '{}'>".format(
            attribute_name, node_name))


def attribute_read(node_name, attribute_name):
    """fonction de lecture d'une valeur d'un attribut assigne �  un noeud"""

    # valider si le noeud possede l'attribut
    if attribute_has(node_name, attribute_name):
        # extraire et retourner la valeur de l'attribut
        return cmds.getAttr("%s.%s" % (node_name, attribute_name))
    else:
        print("<fonction 'attribute_read' annulee, car l'attribut '{}' n'existe pas sur le noeud '{}'>".format(
            attribute_name, node_name))
        return None


def attribute_write(node_name, attribute_name, attribute_value):
    """fonction d'ecriture d'une valeur dans un attribut assigne �  un noeud"""

    # Si le noeud ne possede pas l'attribut, alors, le creer
    if not attribute_has(node_name, attribute_name):
        attribute_add(node_name, attribute_name)

    cmds.setAttr("%s.%s" % (node_name, attribute_name), attribute_value)
    print("<L'attribut '{}' du noeud '{}' a bien ete mis a jour>".format(node_name, attribute_name))


def attribute_connect(node_name1, attribute_name1, node_name2, attribute_name2):
    """fonction pour creer une connexion entre deux attributs de deux noeuds differents"""

    # valider l'existence de l'attribut sur les deux noeuds
    if not attribute_has(node_name1, attribute_name1):
        attribute_add(node_name1, attribute_name1)
    if not attribute_has(node_name2, attribute_name2):
        attribute_add(node_name2, attribute_name2)

    # creation d'une connexion entre les deux attributs
    cmds.connectAttr("%s.%s" % (node_name1, attribute_name1), "%s.%s" % (node_name2, attribute_name2))
    print("<L'attribut '{}' du noeud '{}' a ete connecte a l'attribut '{}' du noeud '{}'>".format(node_name1,
                                                                                                  attribute_name1,
                                                                                                  node_name2,
                                                                                                  attribute_name2))


def spheres_instantiate(part, rads, dest):
    """Fonction pour creer des spheres en serie"""

    names = []

    for i, r in enumerate(rads):
        n = "{}_sphere_{}".format(part, i)
        names.append(n)

        print("\t\t<Creation de la sphere : {} de rayon {}>".format(n, r))
        dest.append(cmds.polySphere(n=n, sx=subDivisionsX, sy=subDivisionsY, r=r))

    sets.append(cmds.sets(names, n=part))


def cylinders_instantiate(part, dims, dest):
    """Fonction pour creer des cylindres en serie"""

    names = []

    for i, d in enumerate(dims):
        n = "{}_cylinder_{}".format(part, i)
        names.append(n)

        print("\t\t<Creation du cylindre : {} de dimension {}>".format(n, d))
        dest.append(cmds.polyCylinder(n=n, sx=subDivisionsX, sy=subDivisionsY, sz=subDivisionsZ, r=d[0], h=d[1]))

    sets.append(cmds.sets(names, n=part))


def cone_instantiate(part, dims, dest):
    """Fonction pour creer des cones en serie"""

    names = []

    for i, d in enumerate(dims):
        n = "{}_cone_{}".format(part, i)
        names.append(n)

        print("\t\t<Creation du cone : {} de dimension {}>".format(n, d))
        dest.append(cmds.polyCone(n=n, sx=subDivisionsX, sy=subDivisionsY, sz=subDivisionsZ, r=d[0], h=d[1]))

    sets.append(cmds.sets(names, n=part))


def torus_instantiate(part, dims, dest):
    """Fonction pour creer des anneaux en serie"""

    names = []

    for i, d in enumerate(dims):
        n = "{}_torus_{}".format(part, i)
        names.append(n)

        print("\t\t<Creation de l'anneau : {} de dimension {}>".format(n, d))
        dest.append(cmds.polyTorus(n=n, sx=subDivisionsX, sy=subDivisionsY, r=d[0], sr=d[1]))

    sets.append(cmds.sets(names, n=part))


def validate_pools(dims, pos):
    n_dim = len(dims)
    n_pos = len(pos)
    if n_pos != n_dim:
        print("<ERROR: Nombre d'elements non concordant [{} dimensions pour {} positions]>".format(
            n_dim, n_pos))
        sys.exit()


def instantiate(part, type, dimensions, positions, destination):
    """Fonction generale d'instantiation"""
    o_id = part + "_" + str(snowmanID)

    print("\t<{}: Debut de l'instantiation>".format(o_id))

    validate_pools(dimensions, positions)

    if type == "sphere":
        spheres_instantiate(o_id, dimensions, destination)
    elif type == "cylinder":
        cylinders_instantiate(o_id, dimensions, destination)
    elif type == "cone":
        cone_instantiate(o_id, dimensions, destination)
    elif type == "torus":
        torus_instantiate(o_id, dimensions, destination)
    else:
        print("\t<ERROR: No function found>")

    print("\t<{}: Instantiation terminee>\n".format(o_id))


def objects_place(objs, pos):
    """Fonction pour deplacer des objets"""
    print("\t<Debut du placement>")

    for elem, p in zip(objs, pos):
        print("\n\t\t<Placement de {}>".format(elem[0]))
        attribute_write(elem[0], "translateX", p[0] + offset[0])
        attribute_write(elem[0], "translateY", p[1] + offset[1])
        attribute_write(elem[0], "translateZ", p[2] + offset[2])

    print("\t<Placement termine>\n")


def objects_rotate(objs, rot):
    """Fonction pour orienter des objets"""
    print("\t<Debut de la rotation>")

    for elem, r in zip(objs, rot):
        print("\n\t\t<Rotation de {}>".format(elem[0]))
        attribute_write(elem[0], "rotateX", r[0])
        attribute_write(elem[0], "rotateY", r[1])
        attribute_write(elem[0], "rotateZ", r[2])

    print("\t<Rotation terminee>\n")


def identify(elements):
    """Fonction pour ajouter un 'tag' aux parties du corps"""
    print("\t<Debut de l'identification'>")

    for elem in elements:
        attribute_write(elem[0], "snwomanPart", True)

    print("\t<Identification terminee>\n")


if __name__ == "__main__":
    name = prefix + str(snowmanID)

    # Creation du corps
    print("\n\n\n<Debut de la creation du corps>\n====\n")
    instantiate("body", "sphere", bodyRadius, bodyPositions, bodyParts)
    objects_place(bodyParts, bodyPositions)
    identify(bodyParts)
    print("====\n<Fin de la creation du corps>\n")

    # Creation des boutons
    print("\n\n\n====\n<Debut de la creation des boutons>\n")
    instantiate("button", "sphere", buttonsRadius, buttonsPositions, buttons)
    objects_place(buttons, buttonsPositions)
    identify(buttons)
    print("<Fin de la creation des boutons>\n====\n")

    # Creation des yeux
    print("\n\n\n====\n<Debut de la creation des yeux>\n")
    instantiate("eye", "sphere", eyesRadius, eyesPositions, eyes)
    objects_place(eyes, eyesPositions)
    identify(eyes)
    print("<Fin de la creation des yeux>\n====\n")

    # Creation du chapeau
    print("\n\n\n====\n<Debut de la creation du chapeau>\n")
    instantiate("hat", "cylinder", hatDimensions, hatPositions, hatParts)
    objects_place(hatParts, hatPositions)
    objects_rotate(hatParts, hatRotations)
    identify(hatParts)
    print("<Fin de la creation du chapeau>\n====\n")

    # Creation des bras
    print("\n\n\n====\n<Debut de la creation des bras>\n")
    instantiate("arm", "cylinder", armDimensions, armPositions, arms)
    objects_place(arms, armPositions)
    objects_rotate(arms, armRotations)
    identify(arms)
    print("<Fin de la creation des bras>\n====\n")

    # Creation du nez
    print("\n\n\n====\n<Debut de la creation du nez>\n")
    instantiate("nose", "cone", noseDimensions, nosePositions, nose)
    objects_place(nose, nosePositions)
    objects_rotate(nose, noseRotations)
    identify(nose)
    print("<Fin de la creation du nez>\n====\n")

    # Creation de l'echarpe
    print("\n\n\n====\n<Debut de la creation de l'echarpe>\n")
    instantiate("scarf", "torus", scarfDimensions, scarfPositions, scarf)
    objects_place(scarf, scarfPositions)
    objects_rotate(scarf, scarfRotations)
    identify(scarf)
    print("<Fin de la creation de l'echarpe>\n====\n")

    cmds.sets(sets, n=name)
