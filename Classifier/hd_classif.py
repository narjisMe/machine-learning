import csv
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from sklearn.base import BaseEstimator, ClassifierMixin
from sklearn.linear_model import RidgeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier

class HeartDiseaseDataset:
    def __init__(self, chemin):
        self.donnees = []
        with chemin.open() as fichier:
            for ligne in csv.reader(fichier):
                valeurs = []
                for valeur in ligne:
                    if valeur == "?":
                        valeurs.append(None)
                    else:
                        valeurs.append(float(valeur))
                self.donnees.append(valeurs)

    def as_array(self):
        lignes = []
        for ligne in self.donnees:
            if None not in ligne:
                lignes.append(ligne)
        return np.array(lignes)


def manual_classifier(patient):
    points = 0
    if patient[2] == 4:
        points += 2
    if patient[8] == 1:
        points += 1
    if patient[10] == 2:
        points += 1
    if patient[12] == 7:
        points += 2
    return points >= 3

class ManualClassifier(ClassifierMixin, BaseEstimator):
    classes_ = np.array([False, True])

    def fit(self, X, y):
        return self

    def predict(self, X):
        return np.array([manual_classifier(patient) for patient in X])


def afficher_graphiques(X, y, sortie):
    noms = ["age", "sex", "cp", "trestbps", "chol", "fbs", "restecg",
             "thalach", "exang", "oldpeak", "slope", "ca", "thal"]
    numeriques = [0, 3, 4, 7, 9, 11]
    categories = [1, 2, 5, 6, 8, 10, 12]

    plt.figure(figsize=(10, 7))
    for i, colonne in enumerate(numeriques):
        plt.subplot(2, 3, i + 1)
        plt.boxplot([X[~y, colonne], X[y, colonne]],
                    tick_labels=["Non malade", "Malade"])
        plt.title(noms[colonne])
    plt.tight_layout()
    plt.savefig(sortie / "numeriques.png")

    plt.figure(figsize=(12, 8))
    for i, colonne in enumerate(categories):
        valeurs = np.unique(X[:, colonne])
        non_malades = []
        malades = []
        for valeur in valeurs:
            non_malades.append(np.sum((X[:, colonne] == valeur) & ~y))
            malades.append(np.sum((X[:, colonne] == valeur) & y))
        positions = np.arange(len(valeurs))
        plt.subplot(3, 3, i + 1)
        plt.bar(positions - 0.2, non_malades, width=0.4, label="Non malade")
        plt.bar(positions + 0.2, malades, width=0.4, label="Malade")
        plt.xticks(positions, valeurs.astype(int))
        plt.ylabel("patients")
        plt.title(noms[colonne])
        if i == 0:
            plt.legend()
    plt.tight_layout()
    plt.savefig(sortie / "categories.png")

    plt.figure(figsize=(12, 4))
    paires = [(0, 7), (0, 9), (7, 9)]
    for i, (a, b) in enumerate(paires):
        plt.subplot(1, 3, i + 1)
        plt.scatter(X[~y, a], X[~y, b], label="Non malade", alpha=0.6)
        plt.scatter(X[y, a], X[y, b], label="Malade", alpha=0.6)
        plt.xlabel(noms[a])
        plt.ylabel(noms[b])
        if i == 0:
            plt.legend()
    plt.tight_layout()
    plt.savefig(sortie / "points.png")


def tester(nom, modele, X, y):
    modele.fit(X, y)
    predictions = modele.predict(X)
    score = np.mean(predictions == y)
    resultat = f"{nom} : {score:.1%}"
    if isinstance(modele, RidgeClassifier):
        resultat += f" | norme : {np.linalg.norm(modele.coef_):.3f}"
    print(resultat, flush=True)


def main():
    dossier = Path(__file__).resolve().parent
    dataset = HeartDiseaseDataset(dossier / "heart+disease" / "processed.cleveland.data")
    donnees = dataset.as_array()
    X = donnees[:, :-1]
    y = donnees[:, -1] > 0

    sortie = dossier / "graphiques"
    sortie.mkdir(exist_ok=True)

    tester("manuel", ManualClassifier(), X, y)

    for alpha in [0, 0.1, 1, 10, 100, 1000, 5000]:
        modele = RidgeClassifier(alpha=alpha)
        tester(f"ridge alpha={alpha}", modele, X, y)
        if alpha == 1:
            ridge = modele

    for profondeur in [2, 5, None]:
        for feuille in [1, 5]:
            modele = DecisionTreeClassifier(
                max_depth=profondeur, min_samples_leaf=feuille, random_state=42
            )
            tester(f"arbre profondeur={profondeur} feuille={feuille}", modele, X, y)

    modele = make_pipeline(StandardScaler(), KNeighborsClassifier(n_neighbors=5))
    tester("KNN k=5", modele, X, y)

    print("coefficients (de 0 à 12) :", np.round(ridge.coef_, 3))
    print("intercept :", round(ridge.intercept_[0], 3))
    afficher_graphiques(X, y, sortie)
    plt.show(block=True)


if __name__ == "__main__":
    main()
