# Prima che sia tardi

Sito di informazione sviluppato in Django nel 2023 e pubblicato in produzione su primachesiatardi.com. Il repository contiene solo il codice: articoli, immagini e dati degli utenti non ne fanno parte.

## Funzionalità

- **Articoli e sezioni**: editor CKEditor con caricamento di immagini e video YouTube, URL leggibili basati sullo slug, ricerca nel testo.
- **Telegram**: ogni nuovo articolo viene pubblicato automaticamente su un canale tramite la Bot API.
- **SEO**: sitemap XML generata automaticamente, `robots.txt` e analisi delle pagine con django-check-seo.
- **Utenti**: registrazione, login e recupero password; gli utenti registrati possono commentare e mettere "mi piace", mentre gli articoli li pubblica solo lo staff.
- **Statistiche**: contatore delle visite per articolo con django-hitcount.
- **Calendario eventi**: FullCalendar con creazione, modifica ed eliminazione degli eventi direttamente dal calendario.
- **Form contatti**: reCAPTCHA v2, allegati con estensioni consentite, e-mail di conferma a chi scrive e avviso alla redazione. L'IP e lo user agent di ogni richiesta vengono salvati, e dall'area amministrativa si può mettere un IP in blacklist per bloccarne gli invii.
- **Privacy**: banner dei cookie e pagina della Cookie Policy.

## Tecnologie

Python, Django 4.2, PostgreSQL (SQLite in sviluppo), Bootstrap 5 con django-crispy-forms, CKEditor, FullCalendar, django-recaptcha.

## Struttura

| App | Contenuto |
|---|---|
| `blog` | Configurazione del progetto, URL principali e sitemap |
| `core` | Homepage, ricerca, manifesto e pagine statiche |
| `news` | Sezioni, articoli, commenti e "mi piace" |
| `accounts` | Registrazione degli utenti |
| `calendario` | Calendario degli eventi |
| `contatto` | Form contatti e blacklist degli IP |

## Avvio in locale

Serve Python 3.11 o 3.12: alcune dipendenze del 2023 non supportano le versioni più recenti.

```bash
python -m venv .venv
source .venv/bin/activate        # su Windows: .venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
DJANGO_DEBUG=True python manage.py runserver
```

Su Windows (PowerShell) imposta la variabile prima di avviare il server: `$env:DJANGO_DEBUG="True"`.

Senza altre variabili il progetto usa SQLite, stampa le e-mail in console e usa le chiavi di test di reCAPTCHA.

## Configurazione

I valori sensibili non sono nel codice: arrivano da variabili d'ambiente. Copia `.env.example` in `.env` nella cartella del progetto e compila i valori: database PostgreSQL, SMTP, chiavi reCAPTCHA e una `DJANGO_SECRET_KEY` nuova. Il file `.env` viene letto all'avvio ed è escluso da Git. Per generare una chiave:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```
