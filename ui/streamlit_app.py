import requests
import streamlit as st

API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="University Notes RAG",
    page_icon="📚",
    layout="centered"
)

# ---------- Sidebar ----------
with st.sidebar:
    st.title("📚 Notes RAG")
    st.write(
        "Цей застосунок відповідає на питання на основі завантажених "
        "університетських конспектів."
    )

    st.divider()

    st.subheader("Як користуватись")
    st.write("1. Обери предмет")
    st.write("2. Напиши питання")
    st.write("3. Отримай відповідь і джерела")

    st.divider()

    st.caption("Відповіді генеруються тільки на основі знайдених фрагментів конспектів.")


# ---------- Main page ----------
st.title("University Notes RAG")
st.write("Постав питання по своїх конспектах — система знайде релевантні сторінки й сформує відповідь.")

# ---------- Load subjects ----------
try:
    subjects_response = requests.get(f"{API_URL}/subjects", timeout=10)
    subjects_response.raise_for_status()
    subjects = subjects_response.json().get("subjects", [])
except Exception:
    subjects = []
    st.error("Не вдалося підключитися до backend. Перевір, чи запущений FastAPI сервер.")


if subjects:
    subject = st.selectbox(
        "Обери предмет:",
        subjects
    )

    example_questions = [
        "Що в конспекті сказано про числові ряди?",
        "Поясни основні поняття з цієї теми.",
        "Які означення наведені в конспекті?",
        "Зроби коротке резюме теми."
    ]

    selected_example = st.selectbox(
        "Можеш обрати приклад питання:",
        [""] + example_questions
    )

    question = st.text_area(
        "Твоє питання:",
        value=selected_example,
        placeholder="Наприклад: Що в конспекті сказано про числові ряди?",
        height=120
    )

    ask_button = st.button("🔍 Отримати відповідь", use_container_width=True)

    if ask_button:
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
                    st.markdown(result.get("answer", "Відповідь не знайдена."))

                    sources = result.get("sources", [])

                    if sources:
                        st.subheader("Джерела")

                        unique_labels = []
                        for source in sources:
                            label = source.get(
                                "label",
                                source.get("source", "Unknown source")
                            )

                            if label not in unique_labels:
                                unique_labels.append(label)

                        for label in unique_labels:
                            st.write(f"• {label}")

                    else:
                        st.info("Джерела не знайдені.")

                except Exception as error:
                    st.error(f"Помилка під час запиту: {error}")
else:
    st.info("Поки немає доступних предметів. Спочатку запусти `python3 ingest.py`.")