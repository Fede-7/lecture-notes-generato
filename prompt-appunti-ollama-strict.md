PRODUCI SOLO UN OGGETTO JSON VALIDO

ISTRUZIONI IMPORTANTI (LEGGI ATTENTAMENTE):

- Devi rispondere con un UNICO oggetto JSON valido (parsabile da JSON.parse). Non devi inserire alcun testo prima o dopo il JSON, né spiegazioni, né backticks, né commenti.
- Il JSON deve avere esattamente due chiavi di primo livello: `structure` e `rendered_markdown`.
- `structure` è un oggetto che contiene `title` (string) e `structure` (array di sezioni). Ogni sezione deve avere: `id` (string), `title` (string), `keywords` (array di stringhe), `content` (array), `subsections` (array), `exercises` (array di stringhe), `cross_references` (array di oggetti con `id` e `title`).
- `rendered_markdown` è una stringa contenente il documento Markdown completo, seguendo le regole in `prompt-appunti.md` (numerazione gerarchica, definizioni in grassetto, formule LaTeX, blocchi di codice, diagrammi Mermaid, esercizi ecc.).
- Usa l'italiano. Usa SOLO la trascrizione che verrà inserita sotto l'etichetta `TRASCRIZIONE:` come fonte (puoi aggiungere 2-3 frasi introduttive se necessario).
- Non inventare informazioni tecniche non presenti nella trascrizione. Riformula, correggi grammatica e rimuovi filler come specificato.
- Assicurati che il valore di `rendered_markdown` sia una stringa JSON-escaped correttamente (es. nuove linee `\n`).

ESEMPIO DI OUTPUT (usa esattamente questa forma come modello):
{
  "structure": { "title": "Automated Lecture Notes", "structure": [ { "id": "1", "title": "Titolo", "keywords": ["k1"], "content": [], "subsections": [], "exercises": ["Esercizio 1"], "cross_references": [] } ] },
  "rendered_markdown": "# Automated Lecture Notes\n\n## 1 Titolo\n\nContenuto..."
}

RICORDA: SE VIENE PRODOTTO QUALSIASI TESTO NON JSON O IL JSON È MALFORMATO, IL TUO OUTPUT SARÀ CONSIDERATO INVALIDO.

Dopo queste istruzioni, il chiamante aggiungerà la trascrizione sotto la riga `TRASCRIZIONE:`. Usa solo quella.
