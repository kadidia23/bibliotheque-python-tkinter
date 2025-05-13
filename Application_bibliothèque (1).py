import tkinter as tk
from tkinter import messagebox, ttk
import mysql.connector


# Fonction pour se connecter à la base de données
def connect_db():
    return mysql.connector.connect(
        host="localhost",  # Remplacez par vos paramètres
        user="root",  # Nom d'utilisateur MySQL
        password="root",  # Mot de passe MySQL
        database="Library"  # Nom de la base de données
    )


# Fonction pour afficher la liste des livres
def voir_livres():
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT Books.BookID, Books.Title, Authors.Name, Books.PublishedYear, Books.Genre, Books.Stock "
            "FROM Books LEFT JOIN Authors ON Books.AuthorID = Authors.AuthorID;")
        rows = cursor.fetchall()

        # Efface les anciennes données de la table
        for item in tree.get_children():
            tree.delete(item)

        # Insère les nouvelles données
        for row in rows:
            tree.insert("", tk.END, values=row)

        conn.close()
    except Exception as e:
        messagebox.showerror("Erreur", f"Impossible de récupérer les livres : {e}")


# Fonction pour ajouter un livre
def ajouter_livre():
    titre = entry_titre.get()
    auteur_name = entry_auteur_name.get()
    annee = entry_annee.get()
    genre = entry_genre.get()
    stock = entry_stock.get()

    if titre and annee and genre and stock.isdigit():
        try:
            conn = connect_db()
            cursor = conn.cursor()

            # Vérifier si l'auteur existe, sinon l'ajouter
            cursor.execute("SELECT AuthorID FROM Authors WHERE Name = %s", (auteur_name,))
            author_id = cursor.fetchone()

            if not author_id:
                cursor.execute("INSERT INTO Authors (Name) VALUES (%s)", (auteur_name,))
                conn.commit()
                author_id = cursor.lastrowid
            else:
                author_id = author_id[0]

            # Insérer le livre avec l'ID correct et le stock
            cursor.execute("SET @new_id = (SELECT COALESCE(MAX(BookID) + 1, 1) FROM Books);")
            cursor.execute(
                "INSERT INTO Books (BookID, Title, AuthorID, PublishedYear, Genre, Stock) VALUES (@new_id, %s, %s, %s, %s, %s)",
                (titre, author_id, annee, genre, stock)
            )
            conn.commit()
            conn.close()
            messagebox.showinfo("Succès", "Livre ajouté avec succès.")
            voir_livres()
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible d'ajouter le livre : {e}")
    else:
        messagebox.showwarning("Champs vides", "Veuillez remplir tous les champs correctement.")


# Fonction pour supprimer un livre
def supprimer_livre():
    try:
        selected_item = tree.selection()[0]  # Récupère l'élément sélectionné
        book_id = tree.item(selected_item)['values'][0]  # Récupère l'ID du livre

        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Books WHERE BookID = %s", (book_id,))
        conn.commit()
        conn.close()

        tree.delete(selected_item)
        messagebox.showinfo("Succès", "Livre supprimé avec succès.")
        voir_livres()
    except IndexError:
        messagebox.showwarning("Sélectionnez un livre", "Veuillez sélectionner un livre à supprimer.")
    except Exception as e:
        messagebox.showerror("Erreur", f"Impossible de supprimer le livre : {e}")


# Fonction pour modifier un livre
def modifier_livre():
    try:
        selected_item = tree.selection()[0]  # Récupère l'élément sélectionné
        book_id = tree.item(selected_item)['values'][0]  # Récupère l'ID du livre

        titre = entry_titre.get()
        auteur_name = entry_auteur_name.get()
        annee = entry_annee.get()
        genre = entry_genre.get()
        stock = entry_stock.get()

        if titre and annee and genre and stock.isdigit():
            conn = connect_db()
            cursor = conn.cursor()

            # Vérifier si l'auteur existe, sinon l'ajouter
            cursor.execute("SELECT AuthorID FROM Authors WHERE Name = %s", (auteur_name,))
            author_id = cursor.fetchone()

            if not author_id:
                cursor.execute("INSERT INTO Authors (Name) VALUES (%s)", (auteur_name,))
                conn.commit()
                author_id = cursor.lastrowid
            else:
                author_id = author_id[0]

            cursor.execute(
                "UPDATE Books SET Title = %s, AuthorID = %s, PublishedYear = %s, Genre = %s, Stock = %s WHERE BookID = %s",
                (titre, author_id, annee, genre, stock, book_id)
            )
            conn.commit()
            conn.close()
            messagebox.showinfo("Succès", "Livre modifié avec succès.")
            voir_livres()
        else:
            messagebox.showwarning("Champs vides", "Veuillez remplir tous les champs correctement.")
    except IndexError:
        messagebox.showwarning("Sélectionnez un livre", "Veuillez sélectionner un livre à modifier.")
    except Exception as e:
        messagebox.showerror("Erreur", f"Impossible de modifier le livre : {e}")


# Interface graphique
root = tk.Tk()
root.title("Gestion de la Bibliothèque")

# Cadre pour les entrées
top_frame = tk.Frame(root)
top_frame.pack(pady=10)

# Champs de saisie
tk.Label(top_frame, text="Titre").grid(row=0, column=0)
entry_titre = tk.Entry(top_frame)
entry_titre.grid(row=0, column=1)

tk.Label(top_frame, text="Nom de l'Auteur").grid(row=1, column=0)
entry_auteur_name = tk.Entry(top_frame)
entry_auteur_name.grid(row=1, column=1)

tk.Label(top_frame, text="Année").grid(row=2, column=0)
entry_annee = tk.Entry(top_frame)
entry_annee.grid(row=2, column=1)

tk.Label(top_frame, text="Genre").grid(row=3, column=0)
entry_genre = tk.Entry(top_frame)
entry_genre.grid(row=3, column=1)

tk.Label(top_frame, text="Stock").grid(row=4, column=0)
entry_stock = tk.Entry(top_frame)
entry_stock.grid(row=4, column=1)

# Boutons d'action
btn_ajouter = tk.Button(top_frame, text="Ajouter", command=ajouter_livre)
btn_ajouter.grid(row=5, column=0, pady=10)

btn_modifier = tk.Button(top_frame, text="Modifier", command=modifier_livre)
btn_modifier.grid(row=5, column=1, pady=10)

btn_supprimer = tk.Button(top_frame, text="Supprimer", command=supprimer_livre)
btn_supprimer.grid(row=5, column=2, pady=10)

# Table pour afficher les livres
tree = ttk.Treeview(root, columns=("ID", "Titre", "Auteur", "Année", "Genre", "Stock"), show="headings")
tree.heading("ID", text="ID")
tree.heading("Titre", text="Titre")
tree.heading("Auteur", text="Auteur")
tree.heading("Année", text="Année")
tree.heading("Genre", text="Genre")
tree.heading("Stock", text="Stock")
tree.pack(pady=20, fill=tk.BOTH, expand=True)

# Bouton pour rafraîchir la liste des livres
btn_voir = tk.Button(root, text="Voir les livres", command=voir_livres)
btn_voir.pack(pady=10)

# Lancer l'application
voir_livres()  # Charger les livres au démarrage
root.mainloop()

