MTV Lebanon Scraper

A lightweight web-scraping project that extracts the latest news articles from MTV Lebanon, including titles, dates, categories, article text, and image/video content.

This project includes:
Full backend API (FastAPI) + Supabase DB
Frontend demo → view scraped articles
Deployed version (Render + Vercel)

Features

FastAPI backend with endpoints:

Endpoint	Description
GET /articles	Get all stored articles
POST /scrape	Trigger live scraping


Database: Supabase PostgreSQL
Frontend: Static HTML/CSS
Deployment: FastAPI on Render, frontend on Vercel
