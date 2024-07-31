import streamlit as st
import openai

# Инициализация OpenAI API
openai.api_key = st.secrets["openai"]["api_key"]

# Функция для загрузки данных из документов
def load_data():
    options = ["Налоговое право", "Корпоративное право", "Общие вопросы"]
    selected_options = st.multiselect("Выберите документы для загрузки:", options)
    
    data = {}
    for option in selected_options:
        if option == "Налоговое право":
            with open("FAQ по вопросам налогового права.txt", "r", encoding="cp1251") as f:
                data[option] = f.read()
        elif option == "Корпоративное право":
            with open("FAQ_по_вопросам_корпоративного_права.txt", "r", encoding="cp1251") as f:
                data[option] = f.read()
        elif option == "Общие вопросы":
            with open("Текст обучения.txt", "r", encoding="cp1251") as f:
                data[option] = f.read()
    
    return data

data = load_data()

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

st.write("Этот чат-бот отвечает на вопросы, используя информацию из загруженных документов по налоговому и корпоративному праву.")

question = st.text_input("Введите ваш вопрос:")

if question:
    context = ""
    for doc_name, content in data.items():
        context += content + "\n\n"
    answer = get_answer(question, context)
    st.write("Ответ:", answer)
