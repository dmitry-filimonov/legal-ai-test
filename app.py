import streamlit as st
import openai

# Инициализация OpenAI API
openai.api_key = st.secrets["openai"]["api_key"]

# Функция для загрузки данных из документов
def load_data(theme):
    if theme == "Налоговое право":
        with open("FAQ по вопросам налогового права.txt", "r", encoding="cp1251") as f:
            return f.read()
    elif theme == "Корпоративное право":
        with open("FAQ_по_вопросам_корпоративного_права.txt", "r", encoding="cp1251") as f:
            return f.read()
    elif theme == "Общие вопросы":
        with open("Текст обучения.txt", "r", encoding="cp1251") as f:
            return f.read()
    else:
        return ""

theme = st.selectbox("Выберите тему вопросов:", ["Налоговое право", "Корпоративное право", "Общие вопросы"])

# Функция для получения ответа от OpenAI GPT
def get_answer(question, context):
    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Ты юрист, специализирующийся на лизинге автомобилей. Твоя задача - отвечать на вопросы пользователей используя информацию из контекста. "},
            {"role": "user", "content": f"Context: {context}\n\nQuestion: {question}\n\nAnswer:"}
        ]
    )
    answer = response.choices[0].message.content.strip()
    return answer

# Интерфейс Streamlit
st.title("Legal FAQ Chatbot")

st.write("Этот чат-бот отвечает на вопросы, используя информацию из загруженных документов по выбранной теме.")

question = st.text_input("Введите ваш вопрос:")

if question:
    context = load_data(theme)
    answer = get_answer(question, context)
    st.write("Ответ:", answer)
