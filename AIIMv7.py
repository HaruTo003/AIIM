import openai
import pandas as pd
import datetime
import streamlit as st
from datetime import datetime

# Impostazioni API di OpenAI (devi inserire la tua API Key)
openai.api_key = "Your_OpenAI_API_Key"

# Funzione per generare una risposta tramite OpenAI (GPT)
def generate_response(prompt):
    response = openai.Completion.create(
        model="gpt-4",
        prompt=prompt,
        max_tokens=150,
        temperature=0.7
    )
    return response.choices[0].text.strip()

class AIIM:
    def __init__(self):
        self.ingredients = []
        self.allergies = []
        self.recipes = []
        self.weekly_menu = []
        self.conversation_history = []

    def add_ingredients(self, ingredient_name, expiry_date, nutritional_info):
        try:
            expiry_date = datetime.strptime(expiry_date, "%Y-%m-%d")
            self.ingredients.append({
                'ingredient': ingredient_name,
                'expiry_date': expiry_date,
                'nutritional_info': nutritional_info
            })
            return "Ingrediente aggiunto!"
        except ValueError:
            return "Data non valida per la scadenza!"

    def generate_weekly_menu(self):
        prompt = f"Genera un menù settimanale per una persona con questi ingredienti: {', '.join([i['ingredient'] for i in self.ingredients])}. Considera le allergie: {', '.join(self.allergies)}."
        weekly_menu_response = generate_response(prompt)
        self.weekly_menu = weekly_menu_response
        return f"Ecco il tuo menù settimanale: {weekly_menu_response}"

    def generate_recipes(self):
        ingredients_list = [i['ingredient'] for i in self.ingredients]
        prompt = f"Trova ricette che usano gli ingredienti seguenti: {', '.join(ingredients_list)}. Considera le allergie: {', '.join(self.allergies)}."
        recipe_response = generate_response(prompt)
        self.recipes = recipe_response
        return f"Ricette trovate: {recipe_response}"

    def process_user_input(self, user_input):
        """Elabora l'input dell'utente e agisce in base al comando."""
        # Converte tutto in minuscolo per facilitare la comprensione
        user_input = user_input.lower()

        # Gestisce i comandi in base alle parole chiave
        if "aggiungere ingrediente" in user_input:
            return "Quale ingrediente vuoi aggiungere?"
        elif "menù settimanale" in user_input:
            return self.generate_weekly_menu()
        elif "ricette" in user_input:
            return self.generate_recipes()
        else:
            return "Non sono sicuro di come rispondere. Puoi chiedere di aggiungere ingredienti, generare un menù settimanale o cercare ricette."

    def run(self):
        st.title("AIIM - AI for Intelligent Meals")
        st.markdown("Benvenuto! Iniziamo la tua pianificazione dei pasti.")

        # Inizializzazione della conversazione
        if 'conversation_history' not in st.session_state:
            st.session_state.conversation_history = []

        # Mostra la conversazione passata
        for message in st.session_state.conversation_history:
            if message['role'] == 'user':
                st.markdown(f"**Tu:** {message['content']}")
            else:
                st.markdown(f"**AIIM:** {message['content']}")

        # Input dell'utente
        user_input = st.text_input("Scrivi un messaggio:", "")

        if user_input:
            # Aggiungi messaggio dell'utente alla conversazione
            st.session_state.conversation_history.append({'role': 'user', 'content': user_input})

            # Risposta dell'AIIM
            response = self.process_user_input(user_input)

            # Se l'utente sta aggiungendo un ingrediente, raccogli le informazioni necessarie
            if "aggiungere ingrediente" in user_input.lower():
                ingredient_name = st.text_input("Quale ingrediente vuoi aggiungere?", key="ingredient_name")
                expiry_date = st.text_input("Quando scade l'ingrediente? (YYYY-MM-DD)", key="expiry_date")
                nutritional_info = st.text_input("Inserisci le informazioni nutrizionali:", key="nutritional_info")
                if ingredient_name and expiry_date and nutritional_info:
                    response = self.add_ingredients(ingredient_name, expiry_date, nutritional_info)

            # Aggiungi la risposta dell'AIIM alla conversazione
            st.session_state.conversation_history.append({'role': 'aiim', 'content': response})

        # Mostra l'aggiornamento della conversazione
        for message in st.session_state.conversation_history:
            if message['role'] == 'user':
                st.markdown(f"**Tu:** {message['content']}")
            else:
                st.markdown(f"**AIIM:** {message['content']}")

if __name__ == "__main__":
    aiim = AIIM()
    aiim.run()
