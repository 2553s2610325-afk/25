import streamlit as st
from google import genai
from google.genai import types

# 페이지 설정
st.set_page_config(
    page_title="연애상담 챗봇",
    page_icon="💌",
)

st.title("💌 연애상담 챗봇")
st.caption("Gemini 2.5 Flash Lite 기반")

# -----------------------------
# API KEY 불러오기
# -----------------------------
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
except Exception:
    st.error("Secrets에 GOOGLE_API_KEY가 설정되지 않았습니다.")
    st.stop()

# Gemini 클라이언트 생성
try:
    client = genai.Client(api_key=api_key)
except Exception as e:
    st.error(f"Gemini 클라이언트 생성 실패: {e}")
    st.stop()

# -----------------------------
# 채팅 기록 저장
# -----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "model",
            "content": "안녕하세요 😊 연애 고민을 편하게 이야기해 주세요!"
        }
    ]

# 기존 메시지 출력
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# -----------------------------
# 사용자 입력
# -----------------------------
user_input = st.chat_input("연애 고민을 입력하세요...")

if user_input:
    # 사용자 메시지 저장
    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )

    # 사용자 메시지 출력
    with st.chat_message("user"):
        st.markdown(user_input)

    # Gemini 호출
    with st.chat_message("model"):
        with st.spinner("생각 중..."):

            try:
                # Gemini 형식으로 변환
                history = []

                for msg in st.session_state.messages:
                    role = "user" if msg["role"] == "user" else "model"

                    history.append(
                        types.Content(
                            role=role,
                            parts=[types.Part(text=msg["content"])]
                        )
                    )

                response = client.models.generate_content(
                    model="gemini-2.5-flash-lite",
                    contents=history,
                    config=types.GenerateContentConfig(
                        temperature=0.8,
                        max_output_tokens=500,
                        system_instruction="""
너는 공감 능력이 뛰어난 연애상담 전문가다.
사용자의 감정을 존중하고,
현실적이고 따뜻한 조언을 제공해라.
"""
                    )
                )

                reply = response.text

                st.markdown(reply)

                # 응답 저장
                st.session_state.messages.append(
                    {
                        "role": "model",
                        "content": reply
                    }
                )

            except Exception as e:
                error_msg = f"오류가 발생했습니다: {e}"

                st.error(error_msg)

                st.session_state.messages.append(
                    {
                        "role": "model",
                        "content": error_msg
                    }
                )
