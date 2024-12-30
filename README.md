## **Implémentation des Algorithmes de Réduction de Maillage (Vertex Clustering et Edge Collapse)**

le travail réalisé concernant l'implémentation de deux algorithmes de réduction de maillage 3D : Vertex Clustering et Edge Collapse. L'objectif principal était de développer des algorithmes capables de diminuer le nombre de sommets et de faces d'un modèle 3D tout en s'efforçant de préserver sa qualité visuelle et les détails importants. Le travail a consisté en la lecture et l'interprétation du format de fichier .obj, la conception de structures de données adéquates, l'implémentation des deux algorithmes en Python, et enfin, la comparaison des résultats obtenus sur des modèles 3D.

**1. Introduction**

La réduction de maillage est une technique essentielle dans le domaine de la modélisation 3D, permettant d'optimiser les modèles pour diverses applications telles que les jeux vidéo, la réalité virtuelle, ou encore la visualisation scientifique. Un maillage réduit permet une manipulation plus fluide, une transmission plus rapide des données et une complexité de calcul diminuée. Ce projet s'est concentré sur deux méthodes populaires de réduction : le Vertex Clustering et l'Edge Collapse.

**2. Décodage du Format OBJ et Structures de Données**

La première étape cruciale a été de comprendre et d'implémenter la lecture du format de fichier .obj. Une classe `Mesh` a été définie pour stocker les informations essentielles du maillage :

* `self.vertices`: Une liste de tuples représentant les coordonnées (x, y, z) des sommets.
* `self.normals`: Une liste de tuples représentant les vecteurs normaux.
* `self.tex_coords`: Une liste de tuples représentant les coordonnées de texture (u, v).
* `self.faces`: Une liste de listes, chaque liste interne représentant une face et contenant des tuples d'indices `(vertex_index, tex_coord_index, normal_index)`.

La fonction `load_obj` a été développée pour parser un fichier .obj et remplir les attributs de l'objet `Mesh`. Cette fonction gère les différents types de lignes du fichier .obj (vertices, normales, textures, faces) et convertit les données en types Python appropriés. Une gestion d'erreur basique a été incluse pour le cas où le fichier n'est pas trouvé.

**3. Implémentation de l'Algorithme Vertex Clustering**

L'algorithme de Vertex Clustering a été implémenté à travers la fonction `vertex_clustering`. Les étapes principales sont les suivantes :

1. **Création d'une Grille:** L'espace 3D du maillage est divisé en cellules d'une taille spécifiée par le paramètre `grid_size`.
2. **Clustering des Sommets:** Chaque sommet du maillage est assigné à une cellule de la grille en fonction de ses coordonnées. Un dictionnaire `clusters` est utilisé pour regrouper les indices des sommets appartenant à chaque cellule.
3. **Calcul des Sommets Représentatifs:** Pour chaque cellule contenant des sommets, un sommet représentatif est calculé en prenant la moyenne des positions des sommets du cluster (le centroïde).
4. **Reconstruction du Maillage Simplifié:** Un nouveau maillage est créé. Les sommets du maillage simplifié sont les centroïdes calculés. Les faces du maillage original sont reconstruites en utilisant les indices des sommets représentatifs correspondants. Les faces dégénérées (avec moins de 3 sommets uniques après le clustering) sont ignorées.

**4. Implémentation de l'Algorithme Edge Collapse**

L'algorithme Edge Collapse a été implémenté via la fonction `edge_collapse`. Les étapes clés sont :

1. **Calcul des Arêtes et des Faces Adjacentes:** Une structure est créée pour stocker les arêtes du maillage et les faces adjacentes à chaque arête.
2. **Calcul du Coût de Collapse:** Pour chaque arête, un coût de collapse est calculé. Dans cette implémentation, un coût simple basé sur la distance euclidienne entre les deux sommets de l'arête est utilisé.
3. **Utilisation d'une File de Priorité:** Les arêtes sont insérées dans une file de priorité (`heapq`) en fonction de leur coût de collapse.
4. **Collapsus Itératif des Arêtes:** Tant que le nombre de sommets à supprimer n'est pas atteint, l'arête avec le coût de collapse le plus faible est extraite de la file de priorité.
5. **Fusion des Sommets:** Les deux sommets de l'arête sélectionnée sont fusionnés en un nouveau sommet, dont la position est la moyenne des positions des sommets originaux.
6. **Mise à Jour des Faces:** Les faces adjacentes à l'arête collapsée sont mises à jour pour utiliser le nouvel indice du sommet fusionné. Les faces dégénérées sont supprimées.
7. **Gestion des Sommets Collapsés:** Un tableau `collapsed_vertices` est utilisé pour suivre les sommets qui ont été fusionnés.
8. **Finalisation du Maillage Simplifié:** Un nouveau maillage est créé avec les sommets restants. Les indices des faces sont mis à jour pour correspondre aux nouveaux indices des sommets.

**5. Comparaison des Résultats**

La fonction `compare_meshes` a été implémentée pour afficher le nombre de sommets et de faces des maillages originaux et simplifiés. Des fonctions utilisant les librairies `trimesh` et `pyvista` ont également été intégrées pour une comparaison visuelle des maillages dans un notebook Jupyter. Ces fonctions permettent de charger les maillages et de les afficher côte à côte, facilitant l'évaluation de la qualité de la simplification. Les pourcentages de réduction des sommets et des faces sont calculés et affichés.

**6. Sauvegarde des Résultats**

La fonction `save_obj` permet de sauvegarder un objet `Mesh` dans un nouveau fichier .obj. Elle itère sur les sommets, les normales et les coordonnées de texture, puis sur les faces, en formatant correctement les lignes du fichier .obj.

**7. Mise en Œuvre et Tests**

Un script principal a été développé pour parcourir les fichiers .obj du dossier "DVI2_simpl", appliquer les deux algorithmes de réduction avec des paramètres ajustables (taille de la grille pour Vertex Clustering, taux de réduction pour Edge Collapse), sauvegarder les maillages simplifiés et afficher les comparaisons numériques et visuelles. Des fichiers de test ont été inclus pour s'assurer du bon fonctionnement du code en l'absence de données réelles.

**8. Discussion et Observations**

* **Vertex Clustering:** Cet algorithme est relativement simple à implémenter et rapide à exécuter. Le paramètre `grid_size` contrôle directement le niveau de simplification. Une valeur plus élevée entraîne une réduction plus importante, mais peut aussi conduire à une perte de détails plus significative.
* **Edge Collapse:** L'implémentation de l'Edge Collapse est plus complexe, notamment en raison de la gestion de la file de priorité et de la mise à jour des faces. Cependant, il offre potentiellement un meilleur contrôle sur la qualité de la simplification, surtout si des métriques de coût plus avancées étaient utilisées (comme les Quadric Error Metrics, qui n'ont pas été implémentées dans ce travail). Le taux de réduction (`target_ratio`) permet de définir précisément le niveau de simplification souhaité.

**9. Défis Rencontrés**

* **Gestion des Indices:** La manipulation correcte des indices des sommets, des normales et des coordonnées de texture lors de la reconstruction des faces a nécessité une attention particulière.
* **Gestion des Faces Dégénérées:** S'assurer que les faces dégénérées sont correctement identifiées et ignorées après la simplification a été un défi.
* **Efficacité de l'Edge Collapse:** L'implémentation actuelle de l'Edge Collapse, bien que fonctionnelle, pourrait être optimisée en utilisant des structures de données plus performantes pour la recherche des faces adjacentes.



**11. Conclusion**

Le Vertex Clustering se révèle simple et rapide pour une simplification globale, tandis que l'Edge Collapse, bien que plus complexe, offre un meilleur potentiel de préservation de la qualité visuelle, en particulier si des métriques de coût plus sophistiquées sont utilisées. Les résultats obtenus et les pistes d'amélioration identifiées constituent une base solide pour des développements futurs dans le domaine de la réduction de maillage 3D.
