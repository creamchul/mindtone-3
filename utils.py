import re
import random

# 간단한 감정 키워드 사전 (실제 감정 분석에는 자연어 처리 라이브러리를 사용하는 것이 좋습니다)
emotion_keywords = {
    "슬픔": ["슬프", "우울", "눈물", "속상", "그리움", "외로움", "상실", "아프", "괴로움", "그리워", "서럽"],
    "불안": ["불안", "걱정", "두려움", "무서움", "긴장", "초조", "스트레스", "조마조마", "떨림", "공포"],
    "분노": ["화가 나", "짜증", "분노", "화남", "미움", "증오", "억울", "답답", "속상", "분개", "열받"],
    "스트레스": ["스트레스", "부담", "압박", "힘들", "버거움", "벅참", "과로", "지침", "피곤", "부담"],
    "행복": ["행복", "기쁨", "즐거움", "좋음", "감사", "사랑", "감동", "따뜻", "뿌듯", "만족", "웃음"],
    "혼란": ["혼란", "헷갈림", "복잡", "모르겠", "혼동", "갈팡질팡", "고민", "결정", "선택", "갈등", "혼란스러"],
    "피곤": ["피곤", "지침", "졸림", "나른", "무기력", "에너지", "지침", "탈진", "지친", "피로", "잠"]
}

def analyze_emotion(text):
    """
    사용자의 텍스트에서 감정을 분석하여 가장 가능성 높은 감정을 반환합니다.
    매우 기본적인 키워드 매칭 방식을 사용합니다.
    
    실제 애플리케이션에서는 자연어 처리 라이브러리나 API를 사용하는 것이 좋습니다.
    """
    text = text.lower()
    emotion_scores = {}
    
    # 각 감정 카테고리별 키워드 매칭 점수 계산
    for emotion, keywords in emotion_keywords.items():
        score = 0
        for keyword in keywords:
            if keyword in text:
                score += 1
        emotion_scores[emotion] = score
    
    # 가장 높은 점수의 감정 반환
    max_score = max(emotion_scores.values()) if emotion_scores else 0
    
    # 점수가 0이면 감정을 감지하지 못한 것으로 간주
    if max_score == 0:
        return "기타"
    
    # 최고 점수를 가진 감정들 중에서 랜덤하게 선택 (동점일 경우)
    max_emotions = [e for e, s in emotion_scores.items() if s == max_score]
    return random.choice(max_emotions)

def clean_text(text):
    """
    텍스트를 정제하는 함수
    """
    # 특수 문자 제거 (이모티콘 등은 유지)
    text = re.sub(r'[^\w\s\uAC00-\uD7A3가-힣ㄱ-ㅎㅏ-ㅣ]', ' ', text)
    # 여러 공백을 하나로 치환
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def get_emotion_emoji(emotion):
    """
    감정에 해당하는 이모티콘을 반환합니다.
    """
    emotion_emojis = {
        "슬픔": "😢",
        "불안": "😰",
        "분노": "😠",
        "스트레스": "😫",
        "행복": "😊",
        "혼란": "😕",
        "피곤": "😴",
        "기타": "🤔"
    }
    return emotion_emojis.get(emotion, "🤔")

def generate_breathing_exercise():
    """
    호흡 운동 가이드를 생성합니다.
    """
    exercises = [
        "4-7-8 호흡법: 4초 동안 숨을 들이마시고, 7초 동안 숨을 참고, 8초 동안 천천히 내쉬세요.",
        "복식 호흡: 배에 손을 올리고 숨을 들이마실 때 배가 부풀어 오르는 것을 느껴보세요. 천천히 깊게 숨을 쉬세요.",
        "교대 콧구멍 호흡: 오른쪽 콧구멍을 막고 왼쪽으로 숨을 들이마신 후, 왼쪽을 막고 오른쪽으로 내쉬세요.",
        "상자 호흡법: 4초 들이마시고, 4초 참고, 4초 내쉬고, 4초 참는 패턴을 반복하세요.",
        "호흡 집중: 그냥 편안하게 호흡하면서 숨이 들어오고 나가는 감각에만 집중해 보세요."
    ]
    return random.choice(exercises)

def generate_self_care_tip():
    """
    자기 관리 팁을 생성합니다.
    """
    tips = [
        "오늘 물을 충분히 마셨나요? 수분 섭취는 신체와 정신 건강에 중요합니다.",
        "5분만이라도 스트레칭을 해보세요. 몸의 긴장을 풀어주는 데 도움이 됩니다.",
        "창문을 열고 깊게 숨을 들이마셔보세요. 신선한 공기가 기분을 전환시켜 줄 수 있어요.",
        "잠시 전자기기에서 벗어나 눈을 쉬게 해주세요.",
        "좋아하는 음악을 들으며 잠시 휴식을 취해보세요.",
        "오늘 한 가지 작은 성취를 떠올리고 자신을 칭찬해보세요.",
        "가까운 사람에게 안부 메시지를 보내보세요. 관계를 유지하는 것도 자기 관리의 일부입니다.",
        "5분 동안 아무 생각도 하지 않고 그냥 존재하는 시간을 가져보세요."
    ]
    return random.choice(tips) 