# Chroma Premium Website

Μία επαγγελματική ιστοσελίδα σε Flask για την εταιρεία βαφών Chroma Premium. Η εφαρμογή είναι έτοιμη για φιλοξενία στο [PythonAnywhere](https://www.pythonanywhere.com/).

## Δομή έργου

```
mysite/
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── email_utils.py
│   ├── routes.py
│   ├── static/
│   │   ├── css/main.css
│   │   ├── js/main.js
│   │   └── images/logo.png   # προσθέστε εδώ το λογότυπο
│   └── templates/
│       ├── base.html
│       ├── contact.html
│       ├── gallery.html
│       ├── home.html
│       ├── process.html
│       ├── quality.html
│       └── services.html
├── requirements.txt
└── wsgi.py
```

## Τοπική ανάπτυξη

1. Δημιουργήστε και ενεργοποιήστε ένα virtualenv:
   ```powershell
   py -m venv .venv
   .\.venv\Scripts\activate
   ```
2. Εγκαταστήστε εξαρτήσεις:
   ```powershell
   pip install -r requirements.txt
   ```
3. Ορίστε μεταβλητές περιβάλλοντος (προαιρετικά δημιουργήστε ένα `.env`):
   ```env
   FLASK_ENV=development
   SECRET_KEY=μια_τυχαία_αλφαριθμητική_τιμή
   CONTACT_RECIPIENT=info@chromapremium.gr
   SMTP_SERVER=smtp.yourprovider.gr
   SMTP_PORT=587
   SMTP_USERNAME=...
   SMTP_PASSWORD=...
   SMTP_USE_TLS=true
   ```
4. Εκτέλεση development server:
   ```powershell
   flask --app wsgi run --reload
   ```

## Φόρμα επικοινωνίας & email

Η αποστολή email πραγματοποιείται μέσω SMTP. Στο περιβάλλον φιλοξενίας ορίστε τα εξής environment variables:

- `CONTACT_RECIPIENT` – προεπιλογή `info@chromapremium.gr`
- `SMTP_SERVER`
- `SMTP_PORT` (προεπιλογή 587)
- `SMTP_USERNAME`
- `SMTP_PASSWORD`
- `SMTP_USE_TLS` (προεπιλογή `true`)
- `SMTP_USE_SSL` (προεπιλογή `false`)

Αν λείπει κάποιο από τα παραπάνω, η εφαρμογή εμφανίζει μήνυμα σφάλματος χωρίς να διακόπτεται.

## Ανέβασμα στο PythonAnywhere

1. Δημιουργήστε νέο Python 3.11 virtualenv και εγκαταστήστε τα requirements.
2. Αντιγράψτε τον φάκελο `mysite/` στο home directory σας στο PythonAnywhere.
3. Στο Web tab ορίστε:
   - Source code: `~/mysite`
   - Working directory: `~/mysite`
   - WSGI configuration file: `~/mysite/wsgi.py`
4. Στο ίδιο tab, ενεργοποιήστε το virtualenv σας.
5. Στις Static files προσθέστε mapping: URL `/static/` → `/home/<username>/mysite/app/static`.
6. Στις Environment Variables προσθέστε τις SMTP ρυθμίσεις και το `SECRET_KEY`.
7. Τοποθετήστε το αρχείο `logo.png` στο `app/static/images/`.
8. Κάντε reload την εφαρμογή.

## Επόμενα βήματα

- Προσθέστε φωτογραφίες στο `app/static/images/gallery/` και ενημερώστε το `gallery.html` με την τελική διάταξη.
- Συμπληρώστε τηλέφωνο/ωράριο στα templates.
- Σκεφτείτε μετάφραση στα αγγλικά εφόσον θέλετε διπλή γλώσσα.

