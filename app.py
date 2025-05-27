import streamlit as st
import requests

API_KEY = 'f4a83c30b0011d4d51ac2028879177cd'
cidade = 'Fortaleza,BR'

url = f'https://api.openweathermap.org/data/2.5/weather?q={cidade}&appid={API_KEY}&lang=pt_br&units=metric'
resposta = requests.get(url)
dados = resposta.json()

if resposta.status_code != 200:
    st.error(f"Erro na requisição: {dados.get('message', 'Erro desconhecido')}")
else:
    st.title("☁️ Previsão do Tempo - Fortaleza")
    st.write(f"📍 Cidade: {dados['name']}")
    st.write(f"🌡️ Temperatura: {dados['main']['temp']}°C")
    st.write(f"☁️ Condição: {dados['weather'][0]['description']}")
    st.write(f"💧 Umidade: {dados['main']['humidity']}%")
    st.write(f"🌬️ Vento: {round(dados['wind']['speed'] * 3.6)} km/h")
    st.write(f"☔ Chuva: 0%")  # A API básica não dá esse dado direto
