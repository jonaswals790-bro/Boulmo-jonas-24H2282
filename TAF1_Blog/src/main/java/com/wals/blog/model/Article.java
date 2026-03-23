package com.wals.blog.model;

import java.time.LocalDateTime;
import java.util.List;

public class Article {
    private Long id;
    private String titre;
    private String contenu;
    private String auteur;
    private LocalDateTime date;
    private String categorie;
    private List<String> tags;

    // Constructeur par défaut (Obligatoire pour Spring Boot)
    public Article() {
        this.date = LocalDateTime.now();
    }

    // Getters et Setters
    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }
    public String getTitre() { return titre; }
    public void setTitre(String titre) { this.titre = titre; }
    public String getContenu() { return contenu; }
    public void setContenu(String contenu) { this.contenu = contenu; }
    public String getAuteur() { return auteur; }
    public void setAuteur(String auteur) { this.auteur = auteur; }
    public String getCategorie() { return categorie; }
    public void setCategorie(String categorie) { this.categorie = categorie; }
    public List<String> getTags() { return tags; }
    public void setTags(List<String> tags) { this.tags = tags; }
}
