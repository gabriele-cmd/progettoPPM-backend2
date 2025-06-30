# 🎧 Vinyl Shop Backend - Progetto PPM

Backend REST API per un e-commerce di vinili, sviluppato con Django REST Framework.  
Progetto universitario per il corso di **Progettazione e Programmazione del Software (PPM)**.  
Collegato a un frontend HTML/JavaScript minimale.

---

## 🚀 Funzionalità principali

- Autenticazione e registrazione con token
- Gestione utenti con permessi e ruoli
- CRUD prodotti con sconti e disponibilità
- Carrello e gestione ordini
- Checkout e pagamento (simulato)
- Admin panel Django (`/admin`)
- Database PostgreSQL (tramite Supabase)
- Deploy serverless su **Vercel**

---

## 🧩 Tecnologie utilizzate

- Python 3.13
- Django 5.x
- Django REST Framework
- PostgreSQL (Supabase)
- Vercel (deploy backend)
- GitHub Actions (versionamento e CI/CD)

---

## 👥 Tipi di utenti e permessi

| Ruolo                   | Permessi                                                                 | Group       |
|-------------------------|--------------------------------------------------------------------------|-------------|
| 🧑‍💻 Cliente           | - Registrazione/login/logout<br>- Visualizza prodotti<br>- Aggiunge al carrello<br>- Checkout | user |
| 🛠 Moderatore           | - Tutti i permessi del cliente<br>- Visualizza ordini di tutti gli utenti<br>- Visualizza e gestisce utenti | user, moderator |
| 📦 Product Manager     | - Tutti i permessi del cliente<br>- Crea/modifica/elimina prodotti | user, product_manager |
| 👑 Superuser (Admin)   | - Accesso completo a tutto via Django Admin | n/a |

---

## 🛠 Moderatore 
Si occupa della gestione dei Clienti e dei loro Ordini, offrendo assistenza qualora un ordine risulti non pagato o voglia venir modificato o cancellato (rimborsato).<br>
Inoltre, può modificare le informazioni personali dei Clienti qualora ci fossero stati errori di inserimento o negargli l'accesso al sito in caso di abusi o violazioni attraverso l'opzione di Ban.

---

## 📦 Product Manager 
Si occupa della gestione catalogo del negozio. Gestisce i prodotti modificandone le informazioni, la disponibilità o gli sconti, oppure aggiungendone di nuovi o rimuovendone qualora il negozio ne cessi la vendita.<br>
Inoltre, può visualizzare i prodotti comprati accedendo alla lista degli OrderItems (read-only), per valutare così quale prodotto è più richiesto e quale meno in modo da organizzare i rifornimenti del magazzino.

---

## 🔐 Credenziali di test

| Ruolo              | Username     | Password       |
|--------------------|--------------|----------------|
| Cliente 1     | `LocalBuyer`   | `testpassword1`  |
| Cliente 2    | `ForeignBuyer`   | `testpassword2`  |
| Moderatore         | `Moderator`  | `testpassword3`  |
| Product Manager    | `Manager`    | `testpassword4`  |
| Superuser (admin)  | `Gab`      | `superpassword` |

---

## 🌐 Endpoint principali

| Metodo | Endpoint                             | Descrizione                          |
|--------|--------------------------------------|--------------------------------------|
| POST   | `/api/users/register/`               | Registrazione                        |
| POST   | `/api/users/login/`                  | Login (ritorna token)                |
| GET    | `/api/products/`                     | Lista prodotti                       |
| POST   | `/api/orders/cart/items/`            | Aggiunge prodotto al carrello        |
| GET    | `/api/orders/cart/`                  | Visualizza carrello attivo           |
| POST   | `/api/orders/checkout/`              | Esegue checkout                      |

⚠️ Tutti gli endpoint `/orders/` e `/products/` richiedono autenticazione tramite token.

Le funzioni sopra indicate possono essere testate da frontend (e quindi accessibili agli Utenti normali.

Le seguenti funzioni necessitano invece di un accesso minimo da Staff User (gruppo moderator o manager, o superuser):

| Azione                               | Gruppo                              |
|--------------------------------------|-------------------------------------|
| Aggiunta/rimozione/modifica Utente   | Super User / moderator (in parte)   |
| Aggiunta/rimozione/modifica Prodotto | Staff User / product_manager        |
| Aggiunta/rimozione/modifica Ordine   | Super User / moderator              |
| Ban/unBan Utente                     | Super User / moderator              |
| Gestione permessi e gruppi           | Super User                          |
| altro (...)                          | Super User                          |

---

## 🛠️ Tecnologie Utilizzate

- **Backend:** realizzato con **Django** e **Python**, per gestire logica applicativa, API REST, autenticazione e interazione con il database.
- **Frontend:** sviluppato interamente in **HTML** con **JavaScript** integrato, per garantire un’interfaccia minimale, essenziale e facilmente estendibile senza framework esterni.

## ☁️ Database, Deploy e Avvio

### Database

Il database utilizzato nel progetto è ospitato su **Supabase**, una piattaforma backend-as-a-service che fornisce un database PostgreSQL gestito con autenticazione, storage e API integrate.

Per la configurazione locale e di produzione, sono utilizzate variabili d’ambiente contenute nel file `.env`, in particolare:

- `DATABASE_URL`: URL di connessione al database Supabase, con le credenziali criptate.
- Altre variabili di configurazione sensibili (come `SECRET_KEY` o `DB_NAME/HOST/PORT/PASSWORD`) sono mantenute in `.env` per sicurezza.

### Deploy

Il backend Django è stato deployato su **Vercel**, che ospita l’app e la rende accessibile via web.

- L’URL pubblico da visitare per la visualizzazione del sito è:  
  `https://progetto-ppm-backend2.vercel.app/`
  è possibile, tramite lo stesso link, visitare il backend aggiungendo /admin in fondo al link.

- Le variabili d’ambiente configurate su Vercel puntano al database Supabase, garantendo sincronizzazione con il backend.

Il deploy su Vercel è stato configurato per aggiornarsi automaticamente ad ogni push sul branch principale, assicurando che l’app sia sempre aggiornata con l’ultima versione del codice.

