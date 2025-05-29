<h1>The Weekly Space Gazette</h1><br>
<p>A fully automated Python-based newsletter system that scrapes latest space news, formats it into an email, and sends it weekly to subscribers via a web-managed mailing list.</p><br>

 ## Features

-  Scrapes latest space news from trusted sources  
-  Stores articles in a centralized database  
-  Sends automated, formatted email digests  
-  Offers an easy-to-use interface to subscribe or unsubscribe  
-  Web-hosted and publicly accessible  
-  Executes weekly via scheduled automation

##  Tech Stack

### Backend
- **Python** (Flask, Requests, SQLAlchemy)
- **BeautifulSoup** for web scraping
- **Jinja2** for email templating
- **SMTP** for sending emails

### Frontend
- **HTML/CSS** for email and web templates

### Database
- **PostgreSQL** (hosted on Render)

### Automation & Deployment
- **GitHub Actions** for scheduled automation
- **Render** for hosting web app and database

