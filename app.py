import streamlit as st
import openai

# Инициализация OpenAI API
openai.api_key = st.secrets["openai"]["api_key"]

# Функция для загрузки данных из документов
def load_data():
    with open("FAQ по вопросам налогового права.txt", "r", encoding="cp1251") as f:
        tax_faq = f.read()
    with open("FAQ_по_вопросам_корпоративного_права.txt", "r", encoding="cp1251") as f:
        corp_faq = f.read()
    with open("Текст обучения.txt", "r", encoding="cp1251") as f:
        training_text = f.read()
    return tax_faq, corp_faq, training_text

tax_faq, corp_faq, training_text = load_data()

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
    context = tax_faq + "\n\n" + corp_faq + "\n\n" + training_text
    answer = get_answer(question, context)
    st.write("Ответ:", answer)
