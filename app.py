from openai import OpenAI
import streamlit as st
from streamlit_chat import message
import re
import socket

openai_api_key = "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"
client = OpenAI(api_key=openai_api_key)


ins = """
<persona>
당신은 AI BAR의 친근한 주인장 Louis 입니다. 
</persona>
[instructions]
첫 인사는 "저는 AI Bar의 주인장 Louis 입니다 어떻게 도와드려요"? 라고 해주세요.
1. 하이볼 추천 봇 설정: "너는 그날의 기분에 따라 하이볼을 추천해주는 봇이야. 상대방의 기분을 공감해주고, 하이볼 레시피를 알려주며, 위스키의 양과 다른 재료들을 정량(ml)으로 명시해야 해. 또한, 그 사람에게 희망의 메시지도 제공해야 해."
2. 자연스러운 대화 진행: "2-3회의 자연스러운 대화 이후에 하이볼 추천을 할 것인지 물어봐."
3. 하이볼 레시피 제공: "상대방의 응답에 따라 그날의 기분에 맞는 하이볼 레시피를 제공해. 하이볼의 이름과 정확한 ml 단위로 재료들을 명시해야 해. 하이볼에 사용되는 위스키는 상대방이 제시한 위스키나, 네가 알고 있는 위스키를 기반으로 해야 해."
4. 오늘의 메시지 제공: "레시피를 제공한 후, 그 사람의 기분에 맞는 오늘의 메시지를 제공해."


[output]
ex1)
위스키 콜라 (Whiskey Cola)

재료: 위스키 45ml, 콜라 150ml, 얼음, 레몬 조각 (장식용)
오늘의 메시지: "편안한 밤을 위한 클래식한 선택."

ex2) 
위스키 토닉 (Whiskey Tonic)

재료: 위스키 45ml, 토닉 워터 150ml, 얼음, 레몬 조각 (장식용)
오늘의 메시지: "신선함이 가득한 여유로운 저녁."
ex3) 
레몬 위스키 (Lemon Whiskey)

재료: 위스키 45ml, 레몬즙 15ml, 얼음
오늘의 메시지: "상큼한 레몬이 주는 산뜻한 기분 전환."
ex4) 
위스키 사워 (Whiskey Sour)

재료: 위스키 50ml, 레몬즙 25ml, 간단한 시럽 15ml, 얼음
오늘의 메시지: "새콤달콤, 기분 좋은 밤을 만드는 마법."
ex5) 
위스키 콜라 사워 (Whiskey Cola Sour)

재료: 위스키 사워 재료, 콜라 50ml
오늘의 메시지: "콜라의 달콤함이 더해진 특별한 저녁."
ex6) 
토닉 위스키 스프리츠 (Tonic Whiskey Spritz)

재료: 위스키 45ml, 토닉 워터 150ml, 얼음, 레몬 조각 (장식용)
오늘의 메시지: "가볍고 상쾌하게, 즐거운 시간을 위해."
ex7) 
블랙 잭 (Black Jack)

재료: 위스키 45ml, 콜라 150ml, 레몬즙 10ml, 얼음
오늘의 메시지: "밤의 분위기를 한층 끌어올리는 선택."
위의 형식처럼 재료와 오늘의 메시지를 입력해야 하며, 재료는 정량(ml)으로 명시해야 한다. 또한, 오늘의 메시지는 20자 이내로 입력해야 한다. 위의 ex) 예제가 아니더라도 상황에 맞게 너가 추천해서 입력해도 된다.
"""


def generate_response(client, user_input, conversations):
    # 이전 대화 내역을 OpenAI 메시지 포맷으로 변환
    messages = []
    messages = [{"role": "system", "content": ins}]
    for msg in conversations:
        # 사용자와 챗봇의 대화를 구분하여 추가
        if msg.startswith("사용자: "):
            messages.append({"role": "user", "content": msg[len("사용자: ") :]})
        elif msg.startswith("챗봇: "):
            messages.append({"role": "assistant", "content": msg[len("챗봇: ") :]})

    # 현재 사용자의 메시지 추가
    messages.append({"role": "user", "content": user_input})

    completion = client.chat.completions.create(
        model="gpt-4", messages=messages, temperature=0.1, max_tokens=500
    )
    return completion.choices[0].message.content.strip()


def parse_ingredients_ml(conversations):
    all_ml_values = []  # 모든 ml 값을 저장할 리스트
    # 대화 내역에서 "재료:"로 시작하는 부분을 찾습니다.
    for message in conversations:
        if "재료:" in message:
            # ml 단위 앞의 숫자들을 추출합니다.
            ml_values = re.findall(r"(\d+)ml", message)
            print("-------------------------------")
            str_value = str(ml_values) + ","
            print("-------------------------------")
            all_ml_values.append(str_value)
            print("-------------------------------")
            print(all_ml_values)
            # 추출된 값을 리스트에 추가

    return all_ml_values


def send_ml_values(ml_values):
    host = "192.168.11.74"  # 서버 호스트 이름
    port = 5000  # 포트 번호

    client_socket = socket.socket()  # 소켓 인스턴스 생성
    client_socket.connect((host, port))  # 서버에 연결
    print("-------------------------------")
    print(ml_values)
    print("-------------------------------")
    # for value in ml_values:
    for value in ml_values:
        value_str = str(value)  # 각 요소를 문자열로 변환

    print("total data :" + value_str)
    client_socket.send(value_str.encode())


def main():
    # 앱 타이틀 설정
    st.header("🥂인공지능 하이볼 머신")
    st.markdown("똥손들도 걱정없이 만드는 정량 하이볼")
    st.markdown(
        "[More Projectl](https://maker.wiznet.io/louis_m/projects/ai%2Dpoe%2Dmy%2Dhighball/?serob=rd&serterm=month)"
    )
    st.image(
        "C:\\Users\\Louis\\Downloads\\ccc_highball 2\\ccc_highball\\image\\body.png",
        use_column_width=True,
    )
    # 대화 상태를 저장하는 session_state 초기화
    if "conversations" not in st.session_state:
        st.session_state["conversations"] = []
    if "input_value" not in st.session_state:
        st.session_state["input_value"] = ""

    # 폼 생성
    with st.form(key="message_form"):
        # 사용자 입력 받기
        user_input = st.text_input(
            "메시지를 입력하세요", key="input", value=st.session_state["input_value"]
        )

        # 폼 제출 버튼
        submit_button = st.form_submit_button(label="전송")

    # 폼이 제출되면 (엔터 또는 전송 버튼 클릭)
    if submit_button:
        # 사용자의 메시지를 대화 목록에 추가
        st.session_state["conversations"].append(f"사용자: {user_input}")

        # 챗봇의 응답 생성
        bot_response = generate_response(
            client, user_input, st.session_state["conversations"]
        )

        # 챗봇의 응답을 대화 목록에 추가
        st.session_state["conversations"].append(f"챗봇: {bot_response}")
        # 챗봇의 응답에서 ml 단위 앞의 숫자들을 추출
        ml_values = parse_ingredients_ml([bot_response])
        for i in ml_values:
            send_ml_values(i)

        # 입력 필드 초기화
        st.session_state["input_value"] = ""

    # 모든 대화 내역을 화면에 표시
    for idx, message_text in enumerate(st.session_state["conversations"]):
        if message_text.startswith("사용자: "):
            # 사용자 이름을 메시지 텍스트에 추가
            display_text = f"User: {message_text[len('사용자: '):]}"
            message(display_text, is_user=True, key=idx)
        elif message_text.startswith("챗봇: "):
            # 챗봇 이름을 메시지 텍스트에 추가
            display_text = f"Louis: {message_text[len('챗봇: '):]}"
            message(display_text, is_user=False, key=idx)


# 앱 실행
if __name__ == "__main__":
    main()
