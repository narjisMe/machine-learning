# Réponses

1. Les malades ont souvent un oldpeak plus élevé et un thalach plus bas. L'âge peut aussi aider. La tension et le cholestérol séparent moins clairement les groupes. ca est un nombre entier limité à quelques valeurs.

Pour les catégories, on compare les nombres de malades et de non-malades. cp=4, exang=1, slope=2 et thal=7 semblent utiles. Le classificateur manuel donne respectivement 2, 1, 1 et 2 points. À partir de 3 points sur 6, il prédit malade et obtient 79,5 % de bonnes réponses.

2. Ridge obtient 85,2 % avec alpha=0, 0.1 ou 1, 85,5 % avec alpha=10, puis 73,7 % avec alpha=5000. La norme des coefficients passe de 0,586 à 0,050 : les coefficients se rapprochent de zéro lorsque la régularisation augmente.

Les coefficients multiplient les 13 variables. L'intercept est la constante ajoutée à la fin. Un coefficient positif fait augmenter le score vers la classe malade quand la variable augmente ; un coefficient négatif fait diminuer ce score. Le score calculé est une somme pondérée, pas une probabilité. Les valeurs des coefficients dépendent aussi des unités des variables.

Avec alpha=1, le coefficient de sex est positif (environ 0,286), celui de thalach est négatif (environ -0,005), et l'intercept vaut environ -1,753.

3. On teste max_depth et min_samples_leaf. L'arbre atteint de 77,1 % à 100 % sur ces données. L'arbre sans limite avec des feuilles de taille minimale 1 atteint 100 %, car il peut mémoriser l'entraînement. On peut aussi modifier criterion et min_samples_split.

4. KNN avec 5 voisins obtient 88,6 %. On standardise ses variables pour éviter que les grandes valeurs dominent les distances.

5. Tous les modèles utilisent fit, predict et score. tester entraîne et évalue chaque modèle de la même manière. Le fit manuel retourne seulement self, sans apprentissage.

Les paramètres sont appris pendant fit, par exemple coef_ et intercept_ de Ridge ou les seuils de l'arbre. Les hyperparamètres sont choisis avant fit : alpha, max_depth, min_samples_leaf ou n_neighbors.

Les 6 lignes incomplètes sont supprimées : il reste 297 patients. num=0 devient False et num>0 devient True. Comme dans cette séance, les modèles sont entraînés et évalués sur les mêmes données. Ces scores ne mesurent donc pas leurs performances sur de nouveaux patients. La séparation entraînement/test viendra à la prochaine séance.
