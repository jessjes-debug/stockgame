import pandas as pd
import gradio as gr
import math

# --- 1. 시나리오 데이터 (중략된 부분 없이 필수 데이터 포함) ---
SCENARIO_DATA = [
    {
        "stage": 1, "period": "2018 Q2", "title": "미중 무역전쟁의 서막",
        "desc": "트럼프 행정부가 중국산 수입품에 고율 관세를 부과하며 글로벌 공급망 긴장이 고조됩니다.",
        "round_news": [
            ["미국 고율 관세 예고", "글로벌 교역 위축", "수출 기업 실적 우려"],
            ["공급망 긴장 확산", "달러 선호 현상", "경기민감주 부담"],
            ["실적 전망 반영 시작", "반도체 수요 둔화", "환율 관련주 강세"]
        ],
        "stocks": [
            {"name":"삼성전자","type":"주식","price":51000,"change_rate":-3.2,"intro":"국내 대표 반도체 기업","hint":"무역분쟁 시 부담"},
            {"name":"KODEX 미국달러선물","type":"ETF","price":11000,"change_rate":4.5,"intro":"달러 가치 투자","hint":"위기 시 강세"}
        ]
    }
    # ... (필요 시 여기에 다른 스테이지 데이터 추가)
]

# --- 2. 게임 로직 함수들 ---
def format_krw(x):
    return f"{int(round(x or 0)):,}원"

def new_state(difficulty="초급"):
    return {
        "cash": 10_000_000,
        "portfolio": pd.DataFrame(columns=["name", "type", "qty", "avg_price", "last_price"]),
        "market": pd.DataFrame(SCENARIO_DATA[0]["stocks"]), # 초기 데이터
        "stage_idx": 0,
        "round_idx": 0,
        "difficulty": difficulty,
        "history": pd.DataFrame(columns=["stage", "round", "event", "cash", "total_asset"]),
        "notice": "게임이 시작되었습니다."
    }

# (참고: 다른 보조 함수들 생략 - 실행을 위해 최소한의 demo 구성으로 넘어갑니다)

# --- 3. Gradio UI 구성 (이 부분이 반드시 demo.launch 위에 있어야 함) ---
custom_css = "body { background:#f5f7f8; }"

with gr.Blocks(css=custom_css, title="하나모아 모의투자") as demo:
    gr.Markdown("# 📈 하나모아 모의투자 게임")
    
    state_box = gr.State(new_state())
    
    with gr.Row():
        difficulty = gr.Radio(["초급", "중급", "고급"], value="초급", label="난이도")
        start_btn = gr.Button("게임 시작")
        
    notice = gr.Textbox(label="알림", interactive=False)
    
    with gr.Row():
        account_md = gr.Markdown("### 자산 정보가 여기에 표시됩니다.")
        
    # (여기에 나머지 UI 컴포넌트들을 추가하세요)

# --- 4. 실행부 (가장 하단) ---
if __name__ == "__main__":
    # Streamlit Cloud에서 실행 시 share=True는 에러를 유발할 수 있으므로 제거하거나 기본값 권장
    demo.launch()
