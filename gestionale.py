
import streamlit as st
import pandas as pd
from datetime import datetime
from openai import OpenAI
import json 
st.set_page_config(page_title="Gestionale Ristorante", layout="wide")

st.title("📋 Agenda Prenotazioni")
audio_file = st.sidebar.audio_input("Prenota a voce")
if audio_file:
    transcript = client.audio.transcriptions.create(model="whisper-1", file=audio_file)
    testo = transcript.text
    st.sidebar.write(f"Ho capito: {testo}")
    
    # Chiediamo all'IA di estrarre i dati
    prompt = f"Estrai dati da: '{testo}' in JSON con chiavi: Nome, Persone, Telefono, Turno, Note."
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        response_format={ "type": "json_object" }
    )
    dati = json.loads(response.choices[0].message.content)
    
    # Salviamo automaticamente
    nuova_p = pd.DataFrame([[datetime.now().date(), dati.get('Turno'), dati.get('Nome'), dati.get('Persone'), dati.get('Telefono'), dati.get('Note')]], columns=df.columns)
    df = pd.concat([df, nuova_p], ignore_index=True)
    df.to_csv("prenotazioni.csv", index=False)
    st.rerun()
# Simulazione Database
try:
    df = pd.read_csv("prenotazioni.csv")
except:
    df = pd.DataFrame(columns=["Data", "Turno", "Nome", "Persone", "Telefono", "Note"])

# Sidebar per inserimento manuale veloce
with st.sidebar:
    st.header("Nuova Prenotazione")
    nome = st.text_input("Nome Cliente")
    tel = st.text_input("Telefono")
    persone = st.number_input("Numero Persone", min_value=1, step=1)
    turno = st.radio("Turno", ["Pranzo", "Cena"])
    data = st.date_input("Data", datetime.now())
    note = st.text_area("Note")
    
    if st.button("Salva Prenotazione"):
        nuova = pd.DataFrame([[data, turno, nome, persone, tel, note]], columns=df.columns)
        df = pd.concat([df, nuova], ignore_index=True)
        df.to_csv("prenotazioni.csv", index=False)
        st.success("Salvato!")

# Visualizzazione con colori
def colora_turni(row):
    return ['background-color: #FFF4E0' if row.Turno == 'Pranzo' else 'background-color: #E0F0FF'] * len(row)

st.dataframe(df.style.apply(colora_turni, axis=1), use_container_width=True)