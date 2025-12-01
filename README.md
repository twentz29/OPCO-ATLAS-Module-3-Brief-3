### Data
Dossier data
- `data_all.csv` : les données du module 2
- 
### Gérer les valeurs manquantes dans un réseau de neurones

Lorsque l’on travaille avec des données réelles, notamment issues de sources multiples (comme dans les modules précédents), il est fréquent de rencontrer de nombreuses valeurs manquantes. Dans le cadre d’un entraînement de réseau de neurones, ces valeurs ne peuvent pas être laissées telles quelles (avec des `NaN` ou des champs vides), car cela provoquerait des erreurs de traitement et rendrait le modèle instable.

La stratégie la plus simple consiste à supprimer les lignes incomplètes. Toutefois, cette méthode est généralement inefficace, car elle mène à une perte importante d'information. Une meilleure approche consiste à **imputer** les données manquantes avec une valeur calculée (comme la moyenne, la médiane ou un indicateur constant). Mais cela pose un autre problème : le modèle ne fait plus la différence entre une vraie donnée mesurée et une donnée estimée.

Pour pallier ce problème, une solution efficace et très utilisée dans les pipelines industriels consiste à **ajouter une colonne indicatrice pour chaque variable imputée**. Cela permet au modèle de savoir que la valeur a été imputée, et potentiellement d'ajuster son comportement en conséquence.

---

### Stratégie d’imputation + indicateurs

Prenons un exemple avec trois variables : `taille`, `age` et `poids`. Supposons que certaines valeurs soient manquantes. Nous pouvons remplir ces champs avec une valeur moyenne (par exemple), et en parallèle, créer une nouvelle colonne binaire par variable, indiquant si la valeur originale était manquante (`1`) ou non (`0`).

Ce type d’encodage donne au réseau une capacité supplémentaire : il peut **apprendre à détecter les schémas cachés derrière l’absence d’information**, ce qui est souvent révélateur (par exemple : une personne qui ne donne jamais son âge ou son poids peut correspondre à un profil particulier).

---

### Exemple après imputation + indicateurs

| taille | taille\_ismissing | age | age\_ismissing | poids | poids\_ismissing |
| ------ | ----------------- | --- | -------------- | ----- | ---------------- |
| 180.0  | 0                 | 35  | 0              | 75.0  | 0                |
| 165.0  | 0                 | 32  | 1              | 58.0  | 0                |
| 172.5  | 1                 | 28  | 0              | 66.5  | 1                |

*(avec des imputations par moyenne par exemple : taille → 172.5, age → 32, poids → 66.5)*

---

Cette méthode permet donc de **préserver un maximum d’information**, tout en rendant le modèle plus robuste et plus conscient des limites de ses données d’entrée. C’est une bonne pratique recommandée dans tous les projets d’IA sur données hétérogènes ou incomplètes.
