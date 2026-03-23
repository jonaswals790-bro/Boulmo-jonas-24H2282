package com.wals.blog.controller;

import com.wals.blog.model.Article;
import org.springframework.web.bind.annotation.*;
import java.util.ArrayList;
import java.util.List;

@RestController
@RequestMapping("/api/articles")
public class ArticleController {

    private List<Article> articles = new ArrayList<>();

    // GET /api/articles : Lister tous les articles
    @GetMapping
    public List<Article> list() {
        return articles;
    }

    // POST /api/articles : Ajouter un nouvel article
    @PostMapping
    public Article create(@RequestBody Article article) {
        articles.add(article);
        return article;
    }
}
