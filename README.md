#  Trending Products Scraper API & Dashboard

A full-stack educational project demonstrating **web scraping automation**, **API development**, and **data visualization**.  
This project fetches trending product data from **Amazon** and **Product Hunt**, exposing it through a RESTful API and displaying it on a simple dashboard interface.

> Note: The data collected from **Product Hunt** includes mock examples, since the website employs strong anti-bot measures.  
> This choice is intentional — showcasing both the limits of scraping and best practices for safe, ethical automation.

---

## Features

- **Amazon Trending Products Scraper** (Selenium-based)
- **Product Hunt Mock Integration** (educational demonstration)
- **REST API built with Express.js**
- **Dashboard Frontend** displaying fetched results
- **Auto-Updater** for periodic scraping tasks
- **Selector configuration file** for flexible HTML parsing
- Clean separation between **data collection**, **API serving**, and **frontend visualization**

---

## Technologies Used

### Backend & Automation
- **Python 3.12+**
- **Selenium** — for dynamic web scraping
- **Requests / JSON / Time** — for lightweight automation and data handling

### API & Server
- **Node.js**
- **Express.js**
- **CORS / Body-Parser** middleware
- **JSON file-based datastore**

### Frontend
- **HTML + Vanilla JS**
- **Fetch API** to consume the Express backend
- Simple, responsive dashboard layout

## How to Run Locally

- nstall dependencies
Make sure you have **Node.js** and **Python 3.12+** installed.
npm install
pip install selenium

## The API will run at: http://localhost:3000/api/trending


OBS:
Ethical & Educational Purpose

This project is developed strictly for learning purposes.
It demonstrates:

How scraping works technically.

Why certain websites (like Product Hunt) implement anti-bot measures.

The importance of using public APIs whenever available.

⚠️ Always respect websites’ Terms of Service and robots.txt guidelines.
Do not use scraping for commercial or unauthorized purposes.

