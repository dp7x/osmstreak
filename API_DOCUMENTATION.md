# OSM Streak API Documentation

Questa documentazione descrive come ottenere i dati del tuo profilo OSM Streak e integrarli nel tuo profilo OpenStreetMap.

## API Endpoints

### 1. API JSON - Ottieni dati utente in JSON

**Endpoint:** `GET /api/user/<username>`

**Descrizione:** Restituisce i dati pubblici dell'utente in formato JSON (score, level, streak).

**Parametri:**
- `<username>` - Il nome utente OSM (case-sensitive)

**Esempio di richiesta:**
```
GET /api/user/MapperName
```

**Risposta (200 OK):**
```json
{
  "name": "MapperName",
  "score": 1250,
  "level": 3,
  "streak": 45,
  "uid": 123456
}
```

**Errori:**
- `404 Not Found` - L'utente non esiste

**Caso d'uso:**
- Integrare i dati in applicazioni custom
- Creare dashboard personali
- Sincronizzare dati con altri sistemi

---

### 2. Widget HTML - Embed nel profilo OSM

**Endpoint:** `GET /widget/<username>`

**Descrizione:** Restituisce un widget HTML embeddabile che mostra score, level e streak dell'utente con uno stile elegante.

**Parametri:**
- `<username>` - Il nome utente OSM (case-sensitive)

**Come usare:**

Nel tuo profilo OpenStreetMap, aggiungi un iframe nella sezione "About" o "Description":

```html
<iframe src="https://streak.osmz.ru/widget/MapperName" 
        width="340" 
        height="200" 
        style="border:none; border-radius: 8px;">
</iframe>
```

**Caratteristiche:**
- ✅ Responsive e mobile-friendly
- ✅ Gradient viola elegante
- ✅ Mostra Score, Level, Days di streak
- ✅ Link al sito ufficiale di OSM Streak
- ✅ Si aggiorna automaticamente dal database

**Errori:**
- `404 Not Found` - L'utente non esiste

---

### 3. Badge SVG - Usa nei README/Profili

**Endpoint:** `GET /badge/<username>`

**Descrizione:** Restituisce un badge SVG dinamico con i dati dell'utente. Perfetto per README di GitHub, profili, etc.

**Parametri:**
- `<username>` - Il nome utente OSM (case-sensitive)

**Come usare:**

**In Markdown (GitHub README, etc.):**
```markdown
![OSM Streak Badge](https://streak.osmz.ru/badge/MapperName)
```

**In HTML:**
```html
<img src="https://streak.osmz.ru/badge/MapperName" alt="OSM Streak Badge" />
```

**Nel profilo OpenStreetMap:**
```html
<img src="https://streak.osmz.ru/badge/MapperName" alt="OSM Streak" style="max-width: 350px;" />
```

**Caratteristiche:**
- ✅ SVG dinamico (si aggiorna in tempo reale)
- ✅ Mostra nome utente, score, level e streak
- ✅ Design elegante con gradient
- ✅ Funziona ovunque supporti immagini

**Errori:**
- `404 Not Found` - L'utente non esiste

---

## Esempi di utilizzo

### Esempio 1: Aggiungere il widget al profilo OSM

1. Vai su [openstreetmap.org](https://www.openstreetmap.org)
2. Accedi al tuo profilo
3. Clicca su "Edit Profile"
4. Nella sezione "About me", aggiungi:
```html
<h3>🎯 My OSM Streak Stats</h3>
<iframe src="https://streak.osmz.ru/widget/TuoNomeUtente" 
        width="340" 
        height="200" 
        style="border:none; border-radius: 8px;">
</iframe>
```
5. Salva le modifiche

### Esempio 2: Aggiungere il badge a GitHub

Nel tuo README.md di GitHub:
```markdown
# My OSM Contributions

![OSM Streak](https://streak.osmz.ru/badge/TuoNomeUtente)

Sto mappando ogni giorno con OSM Streak!
```

### Esempio 3: Usare l'API JSON in JavaScript

```javascript
async function getStreakData(username) {
  try {
    const response = await fetch(`https://streak.osmz.ru/api/user/${username}`);
    
    if (!response.ok) {
      throw new Error('User not found');
    }
    
    const data = await response.json();
    
    console.log(`${data.name} - Level ${data.level}, Score: ${data.score}`);
    console.log(`🔥 Streak: ${data.streak} days`);
    
    return data;
  } catch (error) {
    console.error('Error fetching streak data:', error);
  }
}

// Uso
getStreakData('MapperName');
```

---

## Note Importanti

### Case Sensitivity
- I nomi utente **sono case-sensitive**
- `mapper` e `Mapper` sono utenti diversi
- Controlla il capitalization nel tuo nome OSM

### Privacy
- Tutti gli endpoint sono **pubblici**
- Non è necessaria autenticazione
- I dati mostrati sono gli stessi visibili nel profilo pubblico

### Rate Limiting
- Nessun limite di rate ufficiale per ora
- Per uso massivo, contatta gli amministratori

### CORS
- Gli endpoint supportano CORS per richieste da browser

---

## Troubleshooting

**D: Ottengo 404 Not Found**
- Controlla che il nome utente sia corretto e con il capitalization giusto
- Verifica che l'utente abbia completato almeno una sfida in OSM Streak

**D: Il widget non si carica**
- Controlla che l'URL sia corretto
- Verifica che il dominio sia accessibile
- Controlla la console del browser per errori

**D: Il badge SVG non si aggiorna**
- Il badge è dinamico e si aggiorna quando visiti l'URL
- I browser e i servizi potrebbero cachare l'immagine
- Se usi servizi CDN, potrebbero cachetrare per più tempo

---

## Support

Per problemi o suggerimenti, apri un issue su GitHub:
[dp7x/osmstreak/issues](https://github.com/dp7x/osmstreak/issues)

Oppure contatta l'amministratore di OSM Streak.
