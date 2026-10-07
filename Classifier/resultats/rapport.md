# Résultats de l'activité

Données : `processed.cleveland.data`. 303 patients, dont 139 malades ; 6 mesures manquantes conservées puis imputées dans les pipelines.

Séparation stratifiée reproductible (random_state=42) : 227 patients d'entraînement et 76 de test. Les hyperparamètres sont choisis par validation croisée à 5 plis sur l'entraînement uniquement. Les transformations sont réajustées dans chaque pli, sans fuite du jeu de validation ou de test.

## 1. Classificateur manuel

Les boxplots et le scatter explorent uniquement l'entraînement. Les variables catégorielles doivent aussi être lues à l'aide de leurs codes UCI, pas comme des mesures continues. Les variables retenues sont cp (col. 2), exang (8), oldpeak (9), ca (11) et thal (12). thalach (7) est aussi intéressante sur le scatter. Sur ces graphiques, les malades ont généralement oldpeak et ca plus élevés, une fréquence thalach plus basse, et davantage de codes cp=4 et thal=7. Les distributions de trestbps, chol et fbs se recouvrent davantage : ces variables isolées séparent moins clairement les groupes.

La règle fixe prédit malade si au moins deux signes sont présents : cp=4, exang=1, oldpeak>=1.5, ca>=1, thal dans {6,7}. Les seuils sont heuristiques ; ils ne sont ni appris par fit ni ajustés aux scores du test.

## Comparaison sur le même jeu de test

| Modèle | Accuracy entraînement | Accuracy test | Précision | Rappel | F1 |
|---|---:|---:|---:|---:|---:|
| Manuel | 0.797 | 0.829 | 0.750 | 0.943 | 0.835 |
| Ridge | 0.846 | 0.895 | 0.886 | 0.886 | 0.886 |
| Arbre | 0.894 | 0.697 | 0.636 | 0.800 | 0.709 |
| KNN | 0.859 | 0.882 | 0.882 | 0.857 | 0.870 |

La classe positive est « malade ». Le rappel mesure la part des malades détectés ; la précision la part de malades parmi les prédictions positives. comparaison.csv contient aussi TN, FP, FN et TP (matrice [[TN, FP], [FN, TP]]).

## 2. Ridge et alpha

alpha est un hyperparamètre de régularisation : plus il augmente, plus les coefficients sont pénalisés. Une pénalisation très forte peut provoquer du sous-apprentissage ; l'accuracy ne varie pas forcément de façon monotone. Les coefficients peuvent changer sans que les classes prédites changent.

| alpha | Accuracy validation moyenne | Écart-type |
|---:|---:|---:|
| 0.01 | 0.824 | 0.037 |
| 0.1 | 0.824 | 0.037 |
| 1 | 0.824 | 0.040 |
| 10 | 0.815 | 0.043 |
| 100 | 0.837 | 0.047 |
| 1000 | 0.802 | 0.039 |

## 3. Arbre de décision

On compare max_depth (profondeur), min_samples_leaf (taille minimale d'une feuille) et criterion (gini ou entropy). On peut aussi modifier min_samples_split, max_features, class_weight ou ccp_alpha. Limiter la profondeur et augmenter la taille minimale des feuilles réduit la complexité. Un arbre non limité peut très bien mémoriser l'entraînement sans bien généraliser.

## 4. K plus proches voisins

KNeighborsClassifier prédit selon les voisins du patient. On compare k=3,5,9,15 et une pondération uniforme ou selon la distance. Les variables numériques sont standardisées et les catégories encodées en one-hot pour Ridge et KNN. Un petit k peut être sensible au bruit ; un grand k lisse davantage les décisions.

## Hyperparamètres retenus et impact observé

- Ridge : `{'classifier__alpha': 100}`, accuracy CV = 0.837. Selon les réglages, l'accuracy CV varie de 0.802 à 0.837.
- Arbre : `{'decisiontreeclassifier__criterion': 'entropy', 'decisiontreeclassifier__max_depth': 5, 'decisiontreeclassifier__min_samples_leaf': 5}`, accuracy CV = 0.833. Selon les réglages, l'accuracy CV varie de 0.718 à 0.833.
- KNN : `{'classifier__n_neighbors': 5, 'classifier__weights': 'uniform'}`, accuracy CV = 0.820. Selon les réglages, l'accuracy CV varie de 0.797 à 0.820.

Les détails de chaque combinaison sont dans hyperparametres.csv. Ces petits échantillons donnent des estimations variables ; un classement sur une seule séparation ne démontre pas qu'un modèle est toujours supérieur.

## 5. Refactorisation et paramètres

ManualClassifier expose fit, predict et score via ClassifierMixin/BaseEstimator. fit retourne self sans apprentissage. make_models centralise les modèles et leurs grilles ; evaluate les entraîne et calcule les mêmes métriques.

Les paramètres appris sont les coefficients et l'interception de Ridge, les variables et seuils des nœuds de l'arbre, ou les exemples mémorisés par KNN. Les hyperparamètres sont choisis avant fit : alpha, max_depth, min_samples_leaf, criterion, n_neighbors et weights. Bien que scikit-learn les appelle aussi parameters dans get_params(), ils ne sont pas appris par fit.

Documentation : [Ridge](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.RidgeClassifier.html), [arbre](https://scikit-learn.org/stable/modules/generated/sklearn.tree.DecisionTreeClassifier.html), [KNN](https://scikit-learn.org/stable/modules/generated/sklearn.neighbors.KNeighborsClassifier.html).
