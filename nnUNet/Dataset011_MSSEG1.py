import os
import shutil
from glob import glob

# Définition des chemins
data_dir = '../MSSEG-1-preprocessed-2/MSSEG-1-preprocessed-2'
output_dir = 'nnUNet_raw/Dataset011_MSSEG1'
images_tr_dir = os.path.join(output_dir, 'imagesTr')
images_ts_dir = os.path.join(output_dir, 'imagesTs')
labels_tr_dir = os.path.join(output_dir, 'labelsTr')

# Création du répertoire de sortie
os.makedirs(output_dir, exist_ok=True)

# Suppression des répertoires de sortie s'ils existent
if os.path.exists(images_tr_dir):
    shutil.rmtree(images_tr_dir)

if os.path.exists(images_ts_dir):
    shutil.rmtree(images_ts_dir)

if os.path.exists(labels_tr_dir):
    shutil.rmtree(labels_tr_dir)

# Création des dossiers de sortie
os.makedirs(images_tr_dir, exist_ok=True)
os.makedirs(images_ts_dir, exist_ok=True)
os.makedirs(labels_tr_dir, exist_ok=True)

# Récupération et tri des fichiers
flair_files = sorted(glob(os.path.join(data_dir, '*_flair_0.nii.gz')))
consensus_files = sorted(glob(os.path.join(data_dir, '*_consensus.nii.gz')))

# Print files names avec saut de ligne
print("\n".join(flair_files))
print("\n".join(consensus_files))

# Calcul des indices pour 80% d'entraînement
nb_train = int(len(flair_files) * 0.8)

# Copie des fichiers dans les répertoires correspondants avec renommage
for i, flair_file in enumerate(flair_files):
    consensus_file = consensus_files[i]
    flair_new_name = f"msseg1_{i+1:03d}_0000.nii.gz"
    consensus_new_name = f"msseg1_{i+1:03d}.nii.gz"
    if i < nb_train:
        shutil.copy(flair_file, os.path.join(images_tr_dir, flair_new_name))
        shutil.copy(consensus_file, os.path.join(labels_tr_dir, consensus_new_name))
    else:
        shutil.copy(flair_file, os.path.join(images_ts_dir, flair_new_name))

print("Organisation terminée avec succès !")
