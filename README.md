# PRJIAV : Segmentation de lesions SEP

La sclérose en plaques (SEP) est une maladie neurodégénérative chronique qui provoque
des lésions inflammatoires au niveau de la substance blanche du cerveau. L'identification
et la segmentation des nouvelles lésions sont cruciales pour le suivi clinique des patients.

## Objectifs :

- Développer un algorithme de segmentation capable d'identifier les nouvelles lésions à partir de deux images IRM
  cérébrales séparée dans le temps.
- Comparer les performances de différents algorithmes.

## Données :

Les données disponibles pour la réalisation de ce projet sont les bases de données MSSEG-1 et MSSEG-2.

- MSSEG-1 : 53 patients, segmentation par sept experts avec un consensus contenant l'ensemble des lésions identifiées.
- MSSEG-2 : 40 patients différents de MSSEG-1, 2 IRM par patient séparé d'un certain temps, segmentation par quatre
  experts avec un consensus contenant uniquement les nouvelles lésions du second IRM.

L'ensemble des IRM sont fournis en format NIfTI (.nii ou .nii.gz). Il s'agit de données volumétriques 3D.
Les données étant volumineuses, SaturnCloud a été utilisé pour leur traitement et l'entrainement des algorithmes. Les
scripts utilisés sont donc écrits pour fonctionner en priorité avec cette plateforme.

L'ensemble des dépendances pour les scripts et programme utilisés peuvent être installées avec la commande :
```bash
pip install -r requirements.txt
```

## Prétraitement :

Afin de faciliter l'entrainement des algorithmes, il a été nécessaire de pré-traiter les données. Pour cela, nous avons
réalisé les étapes suivantes :

0. Normaliser l'arborescence des dossiers : les données ont été fournis dans trois dossiers d'arborescence différente
- ```
  MSSEG-1
  ├── 01016SACH
  │   ├── 3DFLAIR.nii
  │   ├── 3DT1GADO.nii
  │   ├── 3DT1.nii
  │   ├── Consensus.nii
  │   ├── DP.nii
  │   ├── elastix.log
  │   ├── IterationInfo.0.R0.txt
  │   ├── IterationInfo.0.R1.txt
  │   ├── IterationInfo.0.R2.txt
  │   ├── IterationInfo.0.R3.txt
  │   ├── ManualSegmentation_1.nii
  │   ├── ManualSegmentation_2.nii
  │   ├── ManualSegmentation_3.nii
  │   ├── ManualSegmentation_4.nii
  │   ├── ManualSegmentation_5.nii
  │   ├── ManualSegmentation_6.nii
  │   ├── ManualSegmentation_7.nii
  │   ├── T2.nii
  │   ├── transformix.log
  │   └── TransformParameters.0.txt
  └── ...
  ```
- ```
  MSSEG-1 test
  ├── 01045BRPO_1
  │   ├── 3DFLAIR.nii.gz
  │   ├── 3DT1GADO.nii.gz
  │   ├── 3DT1.nii.gz
  │   ├── Consensus.nii.gz
  │   ├── DP.nii.gz
  │   ├── input.json
  │   ├── ManualSegmentation_1.nii.gz
  │   ├── ManualSegmentation_2.nii.gz
  │   ├── ManualSegmentation_3.nii.gz
  │   ├── ManualSegmentation_4.nii.gz
  │   ├── ManualSegmentation_5.nii.gz
  │   ├── ManualSegmentation_6.nii.gz
  │   ├── ManualSegmentation_7.nii.gz
  │   └── T2.nii.gz
  └── ...
  ```
- ```
  MSSEG-2
  ├── 013
  │   ├── flair_time01_on_middle_space.nii.gz
  │   ├── flair_time02_on_middle_space.nii.gz
  │   ├── ground_truth_expert1.nii.gz
  │   ├── ground_truth_expert2.nii.gz
  │   ├── ground_truth_expert3.nii.gz
  │   ├── ground_truth_expert4.nii.gz
  │   └── ground_truth.nii.gz
  └── ...
  ```
Les données utiles conservées sont le consensus des experts (`idpatient_consensus.nii.gz`) et le ou les deux IRM (`idpatient_flair_0.nii.gz` + `idpatient_flair_1.nii.gz` uniquement pour MSSEG-2). On obtient la structure suivante (pour MSSEG-1) :
```
  MSSEG-1-preprocessed-0
  ├── 01016_consensus.nii.gz
  ├── 01016_flair_0.nii.gz
  ├── 01038_consensus.nii.gz
  ├── 01038_flair_0.nii.gz
  └── ...
  ```
Cette arborescence peut être obtenue avec la commande suivante :
```bash
python scripts/0_create_file_tree.py --input $HOME/workspace/MSSEG-1 --output $HOME/workspace/MSSEG-1-preprocessed-0 --database-type MSSEG-1
```

1. Extraction du cerveau : Chaque IRM contient l'ensemble de la tête du patient, pour simplifier la compréhension des données par les modèles, nous avons utilisé HD-BET pour extraire le cerveau de chaque IRM. Le script suivant permet d'extraire le cerveau des IRM dans un dossier :
```bash
python scripts/1_extract_brain.py --input $HOME/workspace/MSSEG-1-preprocessed-0 --output $HOME/workspace/MSSEG-1-preprocessed-1
```

2. Redimensionnement des images à une taille constante :
```bash
python scripts/2_crop_brain.py --input $HOME/workspace/MSSEG-1-preprocessed-1 --output $HOME/workspace/MSSEG-1-preprocessed-2
```

Les images fournies étaient déjà normalisées, il n'a donc pas été nécessaire de réaliser cette étape.

