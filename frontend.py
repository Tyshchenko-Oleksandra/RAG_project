import requests
import streamlit as st

API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="University Notes RAG",
    page_icon="📚",
    layout="centered"
)

st.title("📚 University Notes RAG")
st.write("Постав питання по своїх університетських конспектах.")

# --- Load subjects ---
try:
    subjects_response = requests.get(f"{API_URL}/subjects")
    subjects_response.raise_for_status()
    subjects = subjects_response.json().get("subjects", [])
except Exception:
    subjects = []
    st.error("Не вдалося підключитися до backend. Перевір, чи запущений FastAPI сервер.")

if subjects:
    subject = st.selectbox("Обери предмет:", subjects)

    question = st.text_area(
        "Твоє питання:",
        placeholder="Наприклад: Що в конспекті сказано про числові ряди?"
    )

    if st.button("Отримати відповідь"):
        if not question.strip():
            st.warning("Введи питання.")
        else:
            with st.spinner("Шукаю відповідь у конспектах..."):
                try:
                    response = requests.post(
                        f"{API_URL}/ask",
                        json={
                            "subject": subject,
                            "question": question
                        },
                        timeout=60
                    )
                    response.raise_for_status()
                    result = response.json()

                    st.subheader("Відповідь")
                    st.write(result.get("answer", "Відповідь не знайдена."))

                    sources = result.get("sources", [])

                    if sources:
                        st.subheader("Джерела")
                        for source in sources:
                            label = source.get(
                                "label",
                                source.get("source", "Unknown source")
                            )
                            st.write(f"- {label}")

                except Exception as error:
                    st.error(f"Помилка під час запиту: {error}")
else:
    st.info("Поки немає доступних предметів. Спочатку запусти `python3 ingest.py`.")