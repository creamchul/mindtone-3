import streamlit as st
import random
import time
import yaml
from utils import analyze_emotion, clean_text, get_emotion_emoji, generate_breathing_exercise, generate_self_care_tip
from auth_utils import setup_authenticator, register_user, check_authentication, save_user_preferences, get_user_preferences

# 감정 치유 챗봇 - MindTone
# 사용자의 감정 상태를 인식하고 공감과 위로를 제공하는 챗봇 애플리케이션

# 감정별 응답 메시지 사전
responses = {
    "슬픔": [
        "당신의 슬픔을 이해합니다. 힘든 시간을 보내고 계시는군요.",
        "슬픔은 자연스러운 감정입니다. 당신의 감정을 온전히 느끼는 것이 중요해요.",
        "함께 이야기하다 보면 마음이 조금 가벼워질 수 있어요. 더 말씀해 주실래요?",
        "때로는 울어도 괜찮아요. 감정을 표현하는 것이 치유의 첫 단계입니다.",
        "지금 느끼는 감정이 영원히 지속되지는 않을 거예요. 조금씩 나아질 거예요."
    ],
    "불안": [
        "불안한 마음이 드는 것은 자연스러운 일이에요. 깊게 숨을 들이마시고 내쉬어 보세요.",
        "현재에 집중하는 것이 도움이 될 수 있어요. 지금 이 순간에 집중해 보세요.",
        "불확실함이 불안을 키울 수 있어요. 지금 할 수 있는 작은 일에 집중해 보는 건 어떨까요?",
        "불안할 때는 '지금, 여기'에 집중하는 명상이 도움이 됩니다.",
        "당신이 느끼는 감정은 유효합니다. 그 감정을 있는 그대로 받아들여 보세요."
    ],
    "분노": [
        "화가 나는 감정이 들 수 있어요. 그 감정을 인정하는 것이 중요합니다.",
        "분노는 우리에게 중요한 무언가가 침해받았다는 신호일 수 있어요.",
        "잠시 그 상황에서 벗어나 깊게 호흡해 보는 것이 도움이 될 수 있어요.",
        "당신의 감정은 정당합니다. 하지만 그 감정을 어떻게 표현할지 선택할 수 있어요.",
        "분노의 근원을 이해하면 그것을 더 잘 다룰 수 있게 됩니다."
    ],
    "스트레스": [
        "스트레스를 느끼는 것은 매우 자연스러운 반응입니다. 잠시 휴식을 취해보세요.",
        "자신을 돌보는 시간을 가지는 것이 중요해요. 오늘 자신을 위한 작은 행동을 해보세요.",
        "때로는 '아니오'라고 말하는 것도 자기 관리의 중요한 부분입니다.",
        "작은 성취에도 자신을 칭찬해 주세요. 모든 진전은 가치 있습니다.",
        "깊은 호흡과 가벼운 스트레칭이 긴장을 풀어줄 수 있어요."
    ],
    "행복": [
        "행복한 순간을 온전히 즐기세요. 그 기쁨을 충분히 느끼는 것이 중요합니다.",
        "행복한 순간들을 기록해두면 어려운 시간에 힘이 될 수 있어요.",
        "당신의 행복이 오래 지속되길 바랍니다. 그 감정을 즐겨보세요.",
        "행복은 우리 삶의 소중한 부분입니다. 그 순간을 소중히 여겨보세요.",
        "행복한 마음을 주변 사람들과 나누면 더 커질 수 있어요."
    ],
    "혼란": [
        "혼란스러운 상황이군요. 조금 정리할 시간을 가져보는 건 어떨까요?",
        "한 번에 한 가지씩 생각하면 혼란이 줄어들 수 있어요.",
        "때로는 잠시 물러서서 전체 그림을 보는 것이 도움이 됩니다.",
        "생각을 정리하기 위해 글로 적어보는 것도 좋은 방법입니다.",
        "혼란스러울 때는 믿을 수 있는 사람과 대화하는 것이 도움이 될 수 있어요."
    ],
    "피곤": [
        "충분한 휴식은 매우 중요합니다. 오늘 일찍 잠자리에 드는 건 어떨까요?",
        "잠시 눈을 감고 깊게 호흡하는 것만으로도 에너지를 회복할 수 있어요.",
        "자신의 신체가 보내는 신호에 귀 기울이는 것이 중요합니다.",
        "짧은 낮잠이나 명상이 피로를 줄이는 데 도움이 될 수 있어요.",
        "때로는 '아무것도 하지 않는 시간'이 필요합니다."
    ],
    "기타": [
        "당신의 감정을 더 자세히 이야기해 주시겠어요?",
        "지금 어떤 생각이 떠오르나요? 편안하게 나누어 보세요.",
        "더 구체적으로 이야기해 주시면 더 잘 이해할 수 있을 것 같아요.",
        "당신의 이야기를 듣고 있어요. 계속해서 말씀해 주세요.",
        "당신의 감정은 모두 유효합니다. 어떤 감정이든 표현해도 괜찮아요."
    ]
}

# 명상 가이드 메시지
meditation_guides = [
    "깊게 숨을 들이마시고 천천히 내쉬세요. 이 순간에 집중해 보세요.",
    "눈을 감고 호흡에 집중해 보세요. 들숨... 날숨... 마음이 점점 평온해집니다.",
    "몸의 긴장을 하나씩 풀어보세요. 발끝부터 머리까지, 모든 긴장이 녹아내립니다.",
    "마음속의 잡념들을 구름처럼 흘려보내세요. 그저 관찰만 하고 붙잡지 마세요.",
    "당신은 지금 안전합니다. 이 순간에 온전히 머물러보세요."
]

# 긍정적인 확언 메시지
affirmations = [
    "나는 충분히, 있는 그대로 가치 있는 사람입니다.",
    "나는 어떤 어려움도 이겨낼 수 있는 힘을 가지고 있습니다.",
    "나는 매일 조금씩 성장하고 있습니다.",
    "나는 나의 감정을 인정하고 사랑합니다.",
    "나는 행복할 자격이 있습니다.",
    "나는 내 삶의 주인입니다.",
    "오늘 하루도 최선을 다했습니다.",
    "나는 충분히 노력하고 있습니다.",
    "실패는 성장의 기회입니다.",
    "모든 것은 때가 되면 잘 풀릴 것입니다."
]

# 감사 연습 가이드
gratitude_guides = [
    "오늘 하루 중 감사한 순간 세 가지를 떠올려보세요.",
    "당신의 삶에서 당연하게 여겼던 것들 중 감사할 만한 것은 무엇인가요?",
    "주변 사람들 중 감사함을 느끼는 사람을 떠올려보세요. 그 이유는 무엇인가요?",
    "오늘 경험한 작은 기쁨은 무엇인가요?",
    "당신의 신체 중 건강하게 기능하는 부분에 감사해보세요."
]

def get_response(emotion):
    """선택된 감정에 맞는 응답을 랜덤하게 선택하여 반환합니다."""
    if emotion in responses:
        return random.choice(responses[emotion])
    return random.choice(responses["기타"])

def simulate_typing(text):
    """챗봇이 타이핑하는 효과를 시뮬레이션합니다."""
    message_placeholder = st.empty()
    full_text = ""
    
    for i in range(len(text)):
        full_text += text[i]
        message_placeholder.markdown(full_text + "▌")
        time.sleep(0.01)  # 타이핑 속도 조절
    
    message_placeholder.markdown(full_text)
    return message_placeholder

def registration_form():
    """사용자 등록 양식을 표시합니다."""
    st.subheader("회원가입")
    
    with st.form("registration_form"):
        username = st.text_input("사용자 아이디")
        name = st.text_input("이름")
        email = st.text_input("이메일")
        password = st.text_input("비밀번호", type="password")
        password_confirm = st.text_input("비밀번호 확인", type="password")
        
        submitted = st.form_submit_button("가입하기")
        
        if submitted:
            if not username or not name or not email or not password:
                st.error("모든 필드를 입력해주세요.")
            elif password != password_confirm:
                st.error("비밀번호가 일치하지 않습니다.")
            else:
                success, message = register_user(username, name, email, password)
                if success:
                    st.success(message)
                    st.session_state.show_login = True
                    st.session_state.show_registration = False
                else:
                    st.error(message)

def apply_theme(theme_name):
    """
    선택된 테마에 따라 CSS를 적용합니다.
    """
    themes = {
        "calm_blue": """
        <style>
        .stApp {
            background-color: #f0f5f9;
            color: #1e3d59;
        }
        .chat-message {
            padding: 1.5rem;
            border-radius: 0.8rem;
            margin-bottom: 1rem;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        .chat-message.user {
            background-color: #2e5c8a;
            color: white;
        }
        .chat-message.bot {
            background-color: #4d80b3;
            color: white;
        }
        .stButton button {
            background-color: #2e5c8a;
            color: white;
            border-radius: 20px;
        }
        .stTextInput input {
            border-radius: 20px;
            border: 1px solid #2e5c8a;
        }
        </style>
        """,
        
        "warm_beige": """
        <style>
        .stApp {
            background-color: #f9f5f0;
            color: #5d4037;
        }
        .chat-message {
            padding: 1.5rem;
            border-radius: 0.8rem;
            margin-bottom: 1rem;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        .chat-message.user {
            background-color: #8d6e63;
            color: white;
        }
        .chat-message.bot {
            background-color: #a1887f;
            color: white;
        }
        .stButton button {
            background-color: #8d6e63;
            color: white;
            border-radius: 20px;
        }
        .stTextInput input {
            border-radius: 20px;
            border: 1px solid #8d6e63;
        }
        </style>
        """,
        
        "soft_green": """
        <style>
        .stApp {
            background-color: #f0f9f5;
            color: #2e7d32;
        }
        .chat-message {
            padding: 1.5rem;
            border-radius: 0.8rem;
            margin-bottom: 1rem;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        .chat-message.user {
            background-color: #43a047;
            color: white;
        }
        .chat-message.bot {
            background-color: #66bb6a;
            color: white;
        }
        .stButton button {
            background-color: #43a047;
            color: white;
            border-radius: 20px;
        }
        .stTextInput input {
            border-radius: 20px;
            border: 1px solid #43a047;
        }
        </style>
        """,
        
        "lavender": """
        <style>
        .stApp {
            background-color: #f5f0f9;
            color: #5e35b1;
        }
        .chat-message {
            padding: 1.5rem;
            border-radius: 0.8rem;
            margin-bottom: 1rem;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        .chat-message.user {
            background-color: #7e57c2;
            color: white;
        }
        .chat-message.bot {
            background-color: #9575cd;
            color: white;
        }
        .stButton button {
            background-color: #7e57c2;
            color: white;
            border-radius: 20px;
        }
        .stTextInput input {
            border-radius: 20px;
            border: 1px solid #7e57c2;
        }
        </style>
        """
    }
    
    return themes.get(theme_name, themes["calm_blue"])

def show_chat_interface():
    """채팅 인터페이스를 표시합니다."""
    
    # 세션 상태 초기화
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    if "selected_emotion" not in st.session_state:
        st.session_state.selected_emotion = None
    
    # 사용자 선호 설정 저장
    if "preferences" not in st.session_state:
        st.session_state.preferences = get_user_preferences(st.session_state.username)
    
    # 헤더 및 소개
    st.header(f"💭 안녕하세요, {st.session_state.name}님!")
    st.markdown("""
    MindTone과 함께 당신의 감정을 이야기해 보세요.
    저는 당신의 마음에 귀 기울이고 함께 감정을 나누는 공간이 되고 싶습니다.
    """)
    
    # 사이드바 메뉴
    with st.sidebar:
        st.title("도움 메뉴")
        
        # 로그아웃 버튼
        st.session_state.authenticator.logout('로그아웃', 'sidebar')
        st.markdown("---")
        
        st.subheader("명상 가이드")
        if st.button("30초 명상 시작"):
            meditation = random.choice(meditation_guides)
            st.session_state.messages.append({"role": "assistant", "content": f"🧘 명상 가이드: {meditation}"})
            
        st.subheader("긍정적 확언")
        if st.button("긍정적 확언 보기"):
            affirmation = random.choice(affirmations)
            st.session_state.messages.append({"role": "assistant", "content": f"✨ 오늘의 확언: {affirmation}"})
            
        st.subheader("감사 연습")
        if st.button("감사 연습하기"):
            gratitude = random.choice(gratitude_guides)
            st.session_state.messages.append({"role": "assistant", "content": f"🙏 감사 연습: {gratitude}"})

        st.subheader("호흡 운동")
        if st.button("호흡 운동 가이드"):
            breathing = generate_breathing_exercise()
            st.session_state.messages.append({"role": "assistant", "content": f"🌬️ 호흡 운동: {breathing}"})
        
        st.subheader("자기 관리 팁")
        if st.button("자기 관리 팁 받기"):
            tip = generate_self_care_tip()
            st.session_state.messages.append({"role": "assistant", "content": f"💝 자기 관리 팁: {tip}"})
        
        # 사용자 설정
        st.markdown("---")
        st.subheader("환경 설정")
        
        # 테마 선택
        theme_options = {
            "calm_blue": "차분한 파랑",
            "warm_beige": "따뜻한 베이지",
            "soft_green": "부드러운 초록",
            "lavender": "라벤더"
        }
        
        selected_theme = st.selectbox(
            "테마 선택", 
            options=list(theme_options.keys()),
            format_func=lambda x: theme_options[x],
            index=list(theme_options.keys()).index(st.session_state.preferences.get("theme", "calm_blue"))
        )
        
        if st.button("설정 저장"):
            st.session_state.preferences["theme"] = selected_theme
            save_user_preferences(st.session_state.username, st.session_state.preferences)
            st.success("설정이 저장되었습니다.")
            st.experimental_rerun()
            
        st.markdown("---")
        st.caption("© 2023 MindTone. 이 챗봇은 전문적인 상담을 대체할 수 없습니다.")
    
    # 대화 기록 표시
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # 감정 선택 옵션
    emotion_options = ["슬픔", "불안", "분노", "스트레스", "행복", "혼란", "피곤", "기타"]
    
    # 사용자 입력 처리
    user_input = st.chat_input("오늘 어떤 감정을 느끼고 계신가요?")
    
    if user_input:
        # 사용자 메시지 표시
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)
        
        # 텍스트 정제 및 감정 분석
        cleaned_text = clean_text(user_input)
        detected_emotion = analyze_emotion(cleaned_text)
        emotion_emoji = get_emotion_emoji(detected_emotion)
        
        # 자동 감정 분석 결과와 수동 감정 선택 옵션 제공
        with st.chat_message("assistant"):
            st.markdown(f"제가 느끼기에 {emotion_emoji} '{detected_emotion}' 감정을 느끼고 계신 것 같아요. 맞나요?")
            st.markdown("정확한 감정을 선택해주시면 더 도움이 될 수 있어요:")
            
            # 감정 선택 버튼을 두 줄로 구성
            col1, col2 = st.columns(2)
            
            for i, emotion in enumerate(emotion_options[:4]):
                e_emoji = get_emotion_emoji(emotion)
                if col1.button(f"{e_emoji} {emotion}", key=f"emotion_{emotion}"):
                    st.session_state.selected_emotion = emotion
            
            for i, emotion in enumerate(emotion_options[4:]):
                e_emoji = get_emotion_emoji(emotion)
                if col2.button(f"{e_emoji} {emotion}", key=f"emotion_{emotion}"):
                    st.session_state.selected_emotion = emotion
        
        # 감정이 선택되면 응답 표시
        if st.session_state.selected_emotion:
            with st.chat_message("assistant"):
                response = get_response(st.session_state.selected_emotion)
                st.session_state.messages.append({"role": "assistant", "content": response})
                simulate_typing(response)
                
                # 필요에 따라 추가 지원 옵션 제공
                if st.session_state.selected_emotion in ["슬픔", "불안", "분노", "스트레스"]:
                    st.markdown("---")
                    st.markdown("도움이 될 만한 활동을 추천해 드릴게요:")
                    
                    col1, col2 = st.columns(2)
                    if col1.button("호흡 운동 가이드", key="breathing_btn"):
                        breathing = generate_breathing_exercise()
                        st.session_state.messages.append({"role": "assistant", "content": f"🌬️ 호흡 운동: {breathing}"})
                        simulate_typing(f"🌬️ 호흡 운동: {breathing}")
                    
                    if col2.button("긍정적 확언 보기", key="affirmation_btn"):
                        affirmation = random.choice(affirmations)
                        st.session_state.messages.append({"role": "assistant", "content": f"✨ 오늘의 확언: {affirmation}"})
                        simulate_typing(f"✨ 오늘의 확언: {affirmation}")
            
            # 감정 선택 후 상태 초기화
            st.session_state.selected_emotion = None

def main():
    """메인 함수"""
    # 앱 설정
    st.set_page_config(
        page_title="MindTone - 감정 치유 챗봇",
        page_icon="💭",
        layout="centered"
    )
    
    # 인증 설정
    if 'authenticator' not in st.session_state:
        st.session_state.authenticator = setup_authenticator()
    
    # 상태 변수 초기화
    if 'show_registration' not in st.session_state:
        st.session_state.show_registration = False
    
    if 'show_login' not in st.session_state:
        st.session_state.show_login = True
    
    # 인증 상태 확인
    is_authenticated, username, name = check_authentication()
    
    if is_authenticated:
        # 사용자 테마 적용
        user_preferences = get_user_preferences(username)
        theme = user_preferences.get("theme", "calm_blue")
        st.markdown(apply_theme(theme), unsafe_allow_html=True)
        
        # 채팅 인터페이스 표시
        show_chat_interface()
    else:
        # 로그인 및 회원가입 페이지
        st.markdown(apply_theme("calm_blue"), unsafe_allow_html=True)
        
        st.title("💭 MindTone - 감정 치유 챗봇")
        st.markdown("""
        당신의 마음에 귀 기울이고 함께 감정을 나누는 공간, MindTone에 오신 것을 환영합니다.
        시작하려면 로그인하거나 새 계정을 만들어주세요.
        """)
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("로그인", use_container_width=True):
                st.session_state.show_login = True
                st.session_state.show_registration = False
        
        with col2:
            if st.button("회원가입", use_container_width=True):
                st.session_state.show_registration = True
                st.session_state.show_login = False
        
        st.markdown("---")
        
        if st.session_state.show_registration:
            registration_form()
        
        if st.session_state.show_login:
            name, authentication_status, username = st.session_state.authenticator.login("로그인", "main")
            
            if authentication_status is False:
                st.error("사용자 이름 또는 비밀번호가 올바르지 않습니다.")
            
            elif authentication_status is None:
                st.warning("사용자 이름과 비밀번호를 입력하세요.")

def load_config():
    """
    YAML 설정 파일을 불러옵니다.
    """
    import os
    config_path = 'config.yaml'
    if not os.path.exists(config_path):
        # 기본 설정으로 config.yaml 파일 생성
        config = {
            'credentials': {'usernames': {'jsmith': {'email': 'jsmith@gmail.com', 'name': 'John Smith', 'password': '$2b$12$K3JNm5Rp0J0KgFdPL0nN1.N7ub/HF4Z8z9TQ6d1fLRIsC8MKJQHxK'}}},
            'cookie': {'expiry_days': 30, 'key': 'mindtone_auth_key', 'name': 'mindtone_auth'},
            'preauthorized': {'emails': ['example@gmail.com']}
        }
        with open(config_path, 'w') as file:
            yaml.dump(config, file, default_flow_style=False)
    
    with open(config_path) as file:
        config = yaml.load(file, Loader=yaml.SafeLoader)
    return config

if __name__ == "__main__":
    # 설정 파일 확인
    import os
    if not os.path.exists('config.yaml'):
        # 기본 설정으로 config.yaml 파일 생성
        config = {
            'credentials': {'usernames': {'jsmith': {'email': 'jsmith@gmail.com', 'name': 'John Smith', 'password': '$2b$12$K3JNm5Rp0J0KgFdPL0nN1.N7ub/HF4Z8z9TQ6d1fLRIsC8MKJQHxK'}}},
            'cookie': {'expiry_days': 30, 'key': 'mindtone_auth_key', 'name': 'mindtone_auth'},
            'preauthorized': {'emails': ['example@gmail.com']}
        }
        with open('config.yaml', 'w') as file:
            yaml.dump(config, file, default_flow_style=False)
            
    main() 