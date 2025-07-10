# 🎧 Vinyl Shop Backend - Progetto PPM

Backend REST API per un e-commerce di vinili, sviluppato con Django REST Framework.  
Progetto universitario per il corso di **Progettazione e Programmazione del Software (PPM)**.  
Collegato a un frontend HTML/JavaScript minimale.


## 🚀 Funzionalità principali

- Autenticazione e registrazione con token
- Gestione utenti con permessi e ruoli
- CRUD prodotti con sconti e disponibilità
- Carrello e gestione ordini
- Checkout e pagamento (simulato)
- Admin panel Django (`/admin`)
- Database PostgreSQL (tramite Supabase)
- Deploy serverless su **Vercel**


## 🧩 Tecnologie utilizzate

- Python 3.13
- Django 5.x
- Django REST Framework
- PostgreSQL (Supabase)
- Vercel (deploy backend)
- GitHub Actions (versionamento e CI/CD)


## 👥 Tipi di utenti e permessi

| Ruolo                   | Permessi                                                                 | Group       |
|-------------------------|--------------------------------------------------------------------------|-------------|
| 🧑‍💻 Cliente           | - Registrazione/login/logout<br>- Visualizza prodotti<br>- Aggiunge al carrello<br>- Checkout | user |
| 🛠 Moderatore           | - Tutti i permessi del cliente<br>- Visualizza ordini di tutti gli utenti<br>- Visualizza e gestisce utenti | user, moderator |
| 📦 Product Manager     | - Tutti i permessi del cliente<br>- Crea/modifica/elimina prodotti | user, product_manager |
| 👑 Superuser (Admin)   | - Accesso completo a tutto via Django Admin | n/a |


## 🛠 Moderatore 
Si occupa della gestione dei Clienti e dei loro Ordini, offrendo assistenza qualora un ordine risulti non pagato o voglia venir modificato o cancellato (rimborsato).<br>
Inoltre, può modificare le informazioni personali dei Clienti qualora ci fossero stati errori di inserimento o negargli l'accesso al sito in caso di abusi o violazioni attraverso l'opzione di Ban.


## 📦 Product Manager 
Si occupa della gestione catalogo del negozio. Gestisce i prodotti modificandone le informazioni, la disponibilità o gli sconti, oppure aggiungendone di nuovi o rimuovendone qualora il negozio ne cessi la vendita.<br>
Inoltre, può visualizzare i prodotti comprati accedendo alla lista degli OrderItems (read-only), per valutare così quale prodotto è più richiesto e quale meno in modo da organizzare i rifornimenti del magazzino.


## 🔐 Credenziali di test

| Ruolo              | Username     | Password       | Token |
|--------------------|--------------|----------------|------|
| Cliente 1     | `LocalBuyer`   | `testpassword1`  | 0dad42abec6d8bf3658d450107f8bda59e99e08e |
| Cliente 2    | `ForeignBuyer`   | `testpassword2`  | f977df01f22f54fb76e122b8ac99143c11ce7c96 |
| Moderatore         | `Moderator`  | `testpassword3`  | d9774a67f7611b7ca7713285badf8e676c8fd976 |
| Product Manager    | `Manager`    | `testpassword4`  | 7ed6652024cbe4bc931697fbaee5457f0e62cb72 |
| Superuser (admin)  | `Gab`      | `superpassword` | 392789baec81fd2583650e1fe7a3a4ea4cacb8a4 |


## 📚 Elenco Endpoint Principali

| Metodo | Endpoint                                 | Descrizione                                 | Autenticazione |
|--------|------------------------------------------|---------------------------------------------|----------------|
| POST   | `/api/users/register/`                   | Registra un nuovo utente                    | ❌ No          |
| POST   | `/api/users/login/`                      | Login e ottiene token                       | ❌ No          |
| GET    | `/api/users/me/`                         | Info sull’utente loggato                    | ✅ Sì          |
| GET    | `/api/products/`                         | Elenco prodotti disponibili                 | ✅ Sì          |
| POST   | `/api/orders/cart/items/`                | Aggiunge prodotto al carrello               | ✅ Sì          |
| PATCH  | `/api/orders/cart/items/<item_id>/`      | Modifica quantità di un prodotto nel carrello | ✅ Sì        |
| DELETE | `/api/orders/cart/items/<item_id>/`      | Rimuove un prodotto dal carrello            | ✅ Sì          |
| GET    | `/api/orders/cart/`                      | Visualizza carrello attivo                  | ✅ Sì          |
| POST   | `/api/orders/checkout/`                  | Conclude l’ordine (checkout)                | ✅ Sì          |
| GET    | `/api/orders/orders/`                    | Storico ordini dell’utente loggato          | ✅ Sì          |


Le funzioni sopra indicate possono essere testate da frontend (e quindi accessibili agli Utenti normali).

Le seguenti funzioni necessitano invece di un accesso minimo da Staff User (gruppo moderator o manager, o superuser):

| Metodo | Endpoint                                 | Descrizione                                         | Accesso richiesto       |
|--------|------------------------------------------|-----------------------------------------------------|--------------------------|
| POST   | `/api/users/ban/<user_id>/`              | Banna un utente                                     | Superuser / Moderator    |
| GET    | `/admin/`                                | Admin panel completo Django                         | Superuser                |
| POST   | `/api/products/`                         | Crea un nuovo prodotto                              | Product Manager / Staff  |
| PUT    | `/api/products/<product_id>/`            | Aggiorna un prodotto esistente                      | Product Manager / Staff  |
| DELETE | `/api/products/<product_id>/`            | Rimuove un prodotto                                 | Product Manager / Staff  |
| GET    | `/api/orders/orders/`                    | Visualizza tutti gli ordini (solo per staff)        | Moderator / Superuser    |
| PUT    | `/api/orders/orders/<order_id>/`         | Modifica stato di un ordine                         | Moderator / Superuser    |
| DELETE | `/api/orders/orders/<order_id>/`         | Elimina un ordine                                   | Superuser                |
| PATCH  | `/api/users/<user_id>/`                  | Modifica informazioni utente                        | Moderator / Superuser    |
| GET/POST | `/admin/auth/group/` e relazioni       | Gestione permessi, gruppi e ruoli                   | Superuser                |

### 📤 Payload JSON per endpoint

Di seguito sono riportati esempi di payload da utilizzare per testare alcuni degli endpoint sopra citati.

#### 🆕 `POST /api/products/` — Crea un nuovo prodotto

```json
{
  "name": "The Dark Side of the Moon - Pink Floyd",
  "description": "50th Anniversary Edition, rimasterizzato.",
  "price": 35.00,
  "stock": 10,
  "discount_percentage": 15
}
```

---

#### ✏️ `PUT /api/products/<product_id>/` — Modifica un prodotto esistente

```json
{
  "name": "Because The Internet - Childish Gambino",
  "description": "Corretto typo in 'Childish'.",
  "price": 24.00,
  "stock": 5,
  "discount_percentage": 5
}
```

---

#### ✅ `PUT /api/orders/orders/<order_id>/` — Modifica stato di un ordine

```json
{
  "is_paid": true
}
```

> Esempio: puoi usare `order_id = 3` per testare con un ordine non pagato di `LocalBuyer`.

---

#### 👤 `PATCH /api/users/<user_id>/` — Modifica dati di un utente

```json
{
  "first_name": "Mario",
  "last_name": "Rossi",
  "email": "mario.rossi@example.com"
}
```

> Esempio: `user_id = 2` corrisponde a `LocalBuyer`.


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


### NOTA

Il supporto fornito da Vercel e Supabase potrebbe rendere il sito occasionalmente lento nel caricare le richieste. Il sito funziona ma si abbia cura di aspettare la risposta del server ed evitare dove possibile di inviare molteplici richieste tutte insieme.
