import yaml
import streamlit as st
import streamlit_authenticator as stauth
import bcrypt

def load_config():
    """
    YAML 설정 파일을 불러옵니다.
    """
    with open('config.yaml', encoding='utf-8') as file:
        config = yaml.load(file, Loader=yaml.SafeLoader)
    return config

def save_config(config):
    """
    설정을 YAML 파일에 저장합니다.
    """
    with open('config.yaml', 'w', encoding='utf-8') as file:
        yaml.dump(config, file, default_flow_style=False)

def register_user(username, name, email, password):
    """
    새 사용자를 등록합니다.
    
    Parameters:
    - username: 사용자 아이디
    - name: 사용자 이름
    - email: 이메일 주소
    - password: 비밀번호
    
    Returns:
    - success: 등록 성공 여부
    - message: 성공/실패 메시지
    """
    # 설정 파일 불러오기
    config = load_config()
    
    # 이미 존재하는 사용자인지 확인
    if username in config['credentials']['usernames']:
        return False, "이미 존재하는 사용자 아이디입니다."
    
    # 이메일 중복 확인
    for user_data in config['credentials']['usernames'].values():
        if user_data.get('email') == email:
            return False, "이미 등록된 이메일 주소입니다."
    
    # 사전 인증된 이메일인지 확인
    pre_authorized = email in config.get('preauthorized', {}).get('emails', [])
    
    # 비밀번호 해싱
    hashed_password = stauth.Hasher([password]).generate()[0]
    
    # 새 사용자 추가
    config['credentials']['usernames'][username] = {
        'email': email,
        'name': name,
        'password': hashed_password
    }
    
    # 설정 저장
    save_config(config)
    
    return True, "회원가입이 완료되었습니다! 이제 로그인할 수 있습니다."

def setup_authenticator():
    """
    인증 객체를 설정하고 반환합니다.
    """
    config = load_config()
    authenticator = stauth.Authenticate(
        config['credentials'],
        config['cookie']['name'],
        config['cookie']['key'],
        config['cookie']['expiry_days']
    )
    return authenticator

def get_user_info(username):
    """
    사용자 정보를 반환합니다.
    """
    config = load_config()
    if username in config['credentials']['usernames']:
        return config['credentials']['usernames'][username]
    return None

def check_authentication():
    """
    인증 상태를 확인합니다.
    """
    if 'authentication_status' not in st.session_state:
        return False, None, None
        
    if st.session_state.authentication_status:
        return True, st.session_state.username, st.session_state.name
    
    return False, None, None

def save_user_preferences(username, preferences):
    """
    사용자의 기본 설정을 저장합니다.
    
    Parameters:
    - username: 사용자 아이디
    - preferences: 저장할 설정(딕셔너리)
    """
    config = load_config()
    
    if 'preferences' not in config:
        config['preferences'] = {}
    
    config['preferences'][username] = preferences
    save_config(config)

def get_user_preferences(username):
    """
    사용자의 기본 설정을 불러옵니다.
    
    Parameters:
    - username: 사용자 아이디
    
    Returns:
    - preferences: 사용자 설정 딕셔너리 (없으면 빈 딕셔너리)
    """
    config = load_config()
    
    if 'preferences' not in config:
        return {}
    
    return config['preferences'].get(username, {}) 