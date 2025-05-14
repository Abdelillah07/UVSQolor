import numpy as np
import tkinter as tk
from tkinter import filedialog
from PIL import Image
from PIL import ImageTk 
import PIL as pil
from scipy.signal import convolve2d
import copy

# Définition des variables globales
nom_fichier = None
photo = None
canvas = None
matrices_pixels = None
matrice_affichage = None
historique = []
historique_undo = []

# Gestion de l'affichage
def charger(fenetre_principale):
    global nom_fichier, photo, canvas, matrices_pixels, historique

    nom_fichier = str(filedialog.askopenfilename(title="Ouvrir une image"))

    # On vérifie si l'utilisateur n'a pas annulé l'ouverture
    if nom_fichier is not None:
        # On crée une image Pillow puis on la convertit au format TkInter 
        img = pil.Image.open(nom_fichier)
        matrices_pixels = np.array(img)
        historique.append(copy.deepcopy(matrices_pixels))
        photo = ImageTk.PhotoImage(img)

        if canvas is None:
            # Si c'est la première fois qu'on affiche l'image, on crée le canvas
            canvas = tk.Canvas(fenetre_principale, width = img.size[0], height = img.size[1])
            canvas.create_image(0, 0, anchor=tk.NW, image=photo)
            canvas.pack()
        rafraichir(fenetre_principale)

def rafraichir(fenetre_principale):
    global photo
    img = Image.fromarray(matrices_pixels)
    photo = ImageTk.PhotoImage(img)
    canvas.delete("all")
    canvas.config(width=img.size[0], height=img.size[1])
    canvas.create_image(0, 0, anchor=tk.NW, image=photo)
    fenetre_principale.pack_propagate(True)

def rafraichir_affichage(img):
    global photo

    photo = ImageTk.PhotoImage(img)
    canvas.delete("all")
    canvas.config(width=img.size[0], height=img.size[1])
    canvas.create_image(0, 0, anchor=tk.NW, image=photo)

# Gestion des effets
def applique_effet():
    global dialogue_effet, matrices_pixels, matrice_affichage, historique, historique_undo
    matrices_pixels = copy.deepcopy(matrice_affichage)
    historique.append(matrices_pixels)
    historique_undo = []
    dialogue_effet.destroy()

def annule_effet(fenetre_principale):
    global dialogue_effet
    rafraichir(fenetre_principale)
    dialogue_effet.destroy()

def boutons(dialogue_effet, fenetre_principale):
    frame_boutons = tk.Frame(dialogue_effet)
    frame_boutons.pack(side=tk.BOTTOM, pady=10)

    bouton_appliquer = tk.Button(frame_boutons, text="Appliquer",
                                 command=applique_effet)
    bouton_appliquer.pack(side=tk.LEFT, padx=10)

    bouton_annuler = tk.Button(frame_boutons, text="Annuler",
                               command=lambda :annule_effet(fenetre_principale))
    bouton_annuler.pack(side=tk.LEFT, padx=10)

# Revenir en arrière et en avant
def undo(fenetre_principale):
    """ Supprimer le dernier élément de la liste historique"""
    global matrices_pixels, historique, historique_undo
    if len(historique) > 1:
        historique_undo.append(historique.pop())
        matrices_pixels = copy.deepcopy(historique[-1])
    rafraichir(fenetre_principale)

def not_undo(fenetre_principale):
    """ Revenir sur l'élément suppirmer de historique tant qu'il n'y pas eu de nouvelles modifications dans l'image"""
    global matrices_pixels, historique, historique_undo
    if historique_undo != []:
        matrices_pixels = copy.deepcopy(historique_undo[-1])
        historique.append(historique_undo.pop())
    rafraichir(fenetre_principale)

# Savegarder les modifiactions autant qu'image
def fen_sauver():
    global matrices_pixels, fen

    """ Fenêtre pour enregistrer l'image"""
    fen = tk.Toplevel()
    fen.title("Enregistrer les modifications")

    texte = tk.Label(fen, text = "Choisis le nom du fichier")
    nom_fichier = tk.Entry(fen)
    bouton_sauver = tk.Button(fen, text="Enregistrer", command=lambda: sauver(matrices_pixels, nom_fichier.get()))

    # Emplacement des widgets
    texte.grid(row=0, column=0)
    nom_fichier.grid(row=0, column=1)
    bouton_sauver.grid(row=1, column=0)

def sauver(matPix, nom_fichier):
    """ Sauvegarder l'image sous format .png"""
    global fen
    nom_fichier += ".png"
    Image.fromarray(matPix).save(nom_fichier)
    fen.destroy()

#Filtre Vert
def filtre_vert():
    global matrices_pixels, historique, historique_undo
    matrices_pixels[:,:,[0,2]] = 0
    historique.append(matrices_pixels)
    historique_undo = []

def callback_vert(fenetre_principale):
    filtre_vert()
    rafraichir(fenetre_principale)

#Filtre Gris
def filtre_gris():
    global matrices_pixels, historique, historique_undo
    matrices_pixels = np.dot(matrices_pixels, np.array([0.2126, 0.7152, 0.0722]))
    historique.append(matrices_pixels)
    historique_undo = []

def callback_gris(fenetre_principale):
    filtre_gris()
    rafraichir(fenetre_principale)

#Filtre Luminosité
def filtre_luminosite(fenetre_principale):
    global dialogue_effet
    dialogue_effet = tk.Toplevel(fenetre_principale)
    dialogue_effet.title("Luminosité")
    dialogue_effet.geometry("300x150")
    dialogue_effet.grab_set()
    slider = tk.Scale(dialogue_effet, from_=-1.0, to=1.0,
                      orient=tk.HORIZONTAL, length=200,
                      resolution=0.1, digits=2,
                      command=correction_gamma)
    slider.set(0.0)
    slider.pack(pady=20)

    boutons(dialogue_effet, fenetre_principale)

def correction_gamma(facteur):
    global matrices_pixels, matrice_affichage, photo

    facteur = float(facteur)

    # Normalisation (diviser par 255 pour avoir des valeurs entre 0 et 1)
    max_value = float(np.iinfo(matrices_pixels.dtype).max)
    matrice_normalisee = matrices_pixels / max_value
    
    # Appliquer le facteur de correction gamma
    gamma = 1.0 - facteur

    # Appliquer la correction gamma
    matrice_gamma = np.clip(matrice_normalisee**gamma, 0, 1)

    # Remettre à l'échelle les valeurs de 0 à 255
    matrice_gamma = np.uint8(matrice_gamma * max_value)
    matrice_affichage = copy.deepcopy(matrice_gamma)

    # Créer une image à partir de la matrice corrigée
    img_ajustee = Image.fromarray(matrice_gamma)

    rafraichir_affichage(img_ajustee)

def callback_luminosite(fenetre_principale):
    filtre_luminosite(fenetre_principale)


#Filtre Contraste
def filtre_contraste(fenetre_principale):
    global dialogue_effet
    dialogue_effet = tk.Toplevel(fenetre_principale)
    dialogue_effet.title("Contraste")
    dialogue_effet.geometry("250x300")
    dialogue_effet.grab_set()

    slider1 = tk.Scale(dialogue_effet, from_=-1.0, to=1.0,
                      orient=tk.HORIZONTAL, length=200,
                      resolution=0.1, digits=2,
                      command=lambda x: correctionn_sigoide(slider1.get(), slider2.get()))
    
    slider2 = tk.Scale(dialogue_effet, from_=-1.0, to=1.0,
                      orient=tk.HORIZONTAL, length=200,
                      resolution=0.1, digits=2,
                      command=lambda y: correctionn_sigoide(slider1.get(), slider2.get()))
    slider1.set(0.0)
    slider1.pack(pady=20)

    slider2.set(0.0)
    slider2.pack(pady=20)

    boutons(dialogue_effet, fenetre_principale)

def correctionn_sigoide(contraste, pente):
    global matrices_pixels, matrice_affichage, photo

    pente = 1.0 +float(pente)
    contraste = 1.0 + float(contraste)
    max_value = float(np.iinfo(matrices_pixels.dtype).max)
    
    # Normalisation (diviser par 255 pour avoir des valeurs entre 0 et 1)
    matrice_normalisee = matrices_pixels / max_value
    matrice_normalisee -= 0.5
    matrice_normalisee *= contraste
    matrice_normalisee *= pente
    matrice_normalisee = np.exp(-(matrice_normalisee))
    matrice_normalisee += 1
    matrice_normalisee = 1/matrice_normalisee

    # Remettre à l'échelle les valeurs de 0 à 255
    matrice_normalisee = np.uint8(matrice_normalisee *255)
    matrice_affichage = copy.deepcopy(matrice_normalisee)

    # Créer une image à partir de la matrice corrigée
    img_ajustee = Image.fromarray(matrice_normalisee)

    rafraichir_affichage(img_ajustee)

def callback_constraste(fenetre_principale):
    filtre_contraste(fenetre_principale)

#Filtre Flou
def filtre_flou(fenetre_principale):
    global dialogue_effet
    dialogue_effet = tk.Toplevel(fenetre_principale)
    dialogue_effet.title("Flou")
    dialogue_effet.geometry("250x300")
    dialogue_effet.grab_set()

    slider1 = tk.Scale(dialogue_effet, from_=0, to=10,
                      orient=tk.HORIZONTAL, length=200,
                      resolution=0.1, digits=2,
                      command=correction_flou)
    
    slider1.set(1.0)
    slider1.pack(pady=20)

    boutons(dialogue_effet, fenetre_principale)

def correction_flou(facteur):
    global matrices_pixels, matrice_affichage

    facteur = int(facteur)
    facteur =2*facteur +1
    matrice = copy.deepcopy(matrices_pixels)
    kernel = np.ones((facteur, facteur), dtype=int) #On crée un noyau rempli de 1 de taille facteur 
    kernel = (1/(facteur*facteur)) * kernel #On normalise le noyau par la moyenne

    # Appliquer la convolution sur chaque canal et mettre à jour la matrice
    for i in range(3):  # Itérer sur les canaux RGB
        matrice[:, :, i] = convolve2d(matrice[:, :, i].astype(np.uint8), kernel, boundary='symm', mode='same')

    matrice = np.uint8(matrice)
    matrice_affichage = copy.deepcopy(matrice)
    img_ajustee = Image.fromarray(matrice)
    rafraichir_affichage(img_ajustee)

def callback_flou(fenetre_principale):
    filtre_flou(fenetre_principale)
    rafraichir(fenetre_principale)

# Filtre Flou Gaussien
def filtre_flou_gaussien(fenetre_principale):
    global dialogue_effet
    dialogue_effet = tk.Toplevel(fenetre_principale)
    dialogue_effet.title("Flou")
    dialogue_effet.geometry("250x300")
    dialogue_effet.grab_set()
    slider1 = tk.Scale(dialogue_effet, from_=0, to=10,
                      orient=tk.HORIZONTAL, length=200,
                      resolution=0.1, digits=2,
                      command=correction_flou_gaussien)
    
    slider1.set(1.0)
    slider1.pack(pady=20)

    boutons(dialogue_effet, fenetre_principale)

def correction_flou_gaussien(facteur):
    global matrices_pixels, matrice_affichage

    facteur = int(facteur)
    matrice = copy.deepcopy(matrices_pixels)
    kernel = noyau_gaussien(facteur, sigma=facteur / 3)

    # Appliquer la convolution sur chaque canal et mettre à jour la matrice
    for i in range(3):  # Itérer sur les canaux RGB
        matrice[:, :, i] = convolve2d(matrice[:, :, i].astype(np.uint8), kernel, boundary='symm', mode='same')

    matrice = np.uint8(matrice)
    matrice_affichage = copy.deepcopy(matrice)
    img_ajustee = Image.fromarray(matrice)
    rafraichir_affichage(img_ajustee)

def noyau_gaussien(size, sigma=None):
    size = int(size) // 2
    x, y = np.mgrid[-size:size+1, -size:size+1]
    normal = 1 / (2.0 * np.pi * sigma**2)
    kernel_g = np.exp(-((x**2 + y**2) / (2.0*sigma**2))) * normal
    return kernel_g / np.sum(kernel_g)

def callback_flou_de_gauss(fenetre_principale):
    filtre_flou_gaussien(fenetre_principale)
    rafraichir(fenetre_principale)

#Filtre de détection de bord
def filtre_bord(fenetre_principale):
    global dialogue_effet
    dialogue_effet = tk.Toplevel(fenetre_principale)
    dialogue_effet.title("Flou")
    dialogue_effet.geometry("250x300")
    dialogue_effet.grab_set()
    slider1 = tk.Scale(dialogue_effet, from_=1, to=10,
                      orient=tk.HORIZONTAL, length=200,
                      resolution=0.1, digits=2,
                      command=correction_bord)
    
    slider1.set(0)
    slider1.pack(pady=20)

    boutons(dialogue_effet, fenetre_principale)

def correction_bord(facteur):
    global matrices_pixels, matrice_affichage

    facteur = int(facteur)
    matrice_X = np.dot(matrices_pixels, np.array([0.2126, 0.7152, 0.0722]))
    matrice_Y = copy.deepcopy(matrice_X)
    kernel_X = noyau_bord_X(facteur)
    kernel_Y = noyau_bord_Y(facteur)
    # Appliquer la convolution sur la matrice et la met à jour
    matrice_X = convolve2d(matrice_X.astype(np.uint8), kernel_X, boundary='symm', mode='same')
    matrice_Y = convolve2d(matrice_Y.astype(np.uint8), kernel_Y, boundary='symm', mode='same')
    
    matrice = np.sqrt(matrice_X**2 + matrice_Y**2)
    matrice = np.clip(matrice, 0, 255)
    matrice = np.uint8(matrice)
    matrice_affichage = copy.deepcopy(matrice)
    img_ajustee = Image.fromarray(matrice)
    rafraichir_affichage(img_ajustee)

def noyau_bord_X(facteur):
    kernel = np.zeros((facteur, facteur), dtype=float)
    for i in range(kernel.shape[0]):
        kernel[i][0] = i+1
        kernel[i][facteur-1] = -(i+1)
    return kernel

def noyau_bord_Y(facteur):
    kernel = np.zeros((facteur, facteur), dtype=float)
    for i in range(kernel.shape[0]):
        kernel[0][i] = i+1
        kernel[facteur-1][i] = -(i+1)
    return kernel

def callback_detection_bord(fenetre_principale):
    filtre_bord(fenetre_principale)
