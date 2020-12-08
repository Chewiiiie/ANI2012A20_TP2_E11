import sys
import maya.cmds as cmds
import pymel.core as pm
pm.loadPlugin("fbxmaya") # Charger le plugin d'export

# Definition des constantes
prefix = "Snowman_"

# Vider le buffer de selection
cmds.select(clear=True)

# Selectionner tous les bonhommes de neige present et stocker les IDs trouves
cmds.select(prefix+'*', noExpand=True, visible=True)
allSnowIds = list(set([n.split('_')[1] for n in cmds.ls(s=True, v=True)]))

# Exporter chaque model dans un fichier fbx
if len(allSnowIds) == 0:
    sys.exit()
    
for snowman in [prefix + id for id in allSnowIds]:
    cmds.select(snowman)
    pm.mel.FBXExport(f=snowman, s=True)