import tkinter as tk
from fonctions import charger, undo, not_undo, fen_sauver, callback_vert, callback_gris, callback_luminosite, callback_constraste, callback_flou, callback_flou_de_gauss, callback_detection_bord, callback_fusion

# Création de la fenêtre principale
fenetre_principale = tk.Tk()
fenetre_principale.title("UVSQolor")

# crée unn menubar
menubar = tk.Menu(fenetre_principale)
fenetre_principale.config(menu=menubar)


# crée un menu
file_menu1 = tk.Menu(menubar, tearoff=False)
file_menu2 = tk.Menu(menubar, tearoff=False)
file_menu_filtre_couleur = tk.Menu(menubar, tearoff=False)

# Bouton revenir en arrière
button_not_undo = tk.Button(fenetre_principale, text="🔜", command= lambda: not_undo(fenetre_principale))
button_not_undo.pack(side=tk.RIGHT, padx=2, pady=2)

button_undo = tk.Button(fenetre_principale, text="🔙", command=lambda: undo(fenetre_principale))
button_undo.pack(side=tk.RIGHT, padx=2, pady=2)

# Rajouter l'onglet Fichier
menubar.add_cascade(
    label="File",
    menu=file_menu1
)

# Rajouter le sous onglet Ouvrir de File
file_menu1.add_command(
    label='Ouvrir',
    command=lambda : charger(fenetre_principale)
)

file_menu1.add_command(
    label='Enregitrer',
    command= fen_sauver
)

# Rajouter l'onglet Effets
menubar.add_cascade(
    label="Effets",
    menu=file_menu2
)

file_menu2.add_cascade(
    label="Filtres de Couleurs",
    menu=file_menu_filtre_couleur
)

file_menu_filtre_couleur.add_command(
    label='Filtre Vert',
    command=lambda : callback_vert(fenetre_principale)
)

file_menu_filtre_couleur.add_command(
    label='Filtre Gris',
    command=lambda : callback_gris(fenetre_principale)
)

file_menu2.add_command(
    label='Luminosité',
    command=lambda : callback_luminosite(fenetre_principale)
)

file_menu2.add_command(
    label='Constraste',
    command=lambda : callback_constraste(fenetre_principale)
)

file_menu2.add_command(
    label='Flou',
    command=lambda : callback_flou(fenetre_principale)
)

file_menu2.add_command(
    label='Flou de Gauss',
    command= lambda : callback_flou_de_gauss(fenetre_principale)
)

file_menu2.add_command(
    label='Flou Detection de bord',
    command= lambda : callback_detection_bord(fenetre_principale)
)

file_menu2.add_command(
    label='Flou fusion',
    command= lambda : callback_fusion(fenetre_principale)
)

fenetre_principale.mainloop()
