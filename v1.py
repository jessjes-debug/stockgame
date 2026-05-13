# !pip -q install gradio pandas  <-- 이 줄을 삭제하거나 주석 처리하세요.

# Google Colab용 하나모아 모의투자 게임 코드
import base64, zlib, json, math
import pandas as pd
import gradio as gr

# ... 이하 동일 ...
SCENARIO_DATA = [
  {
    "stage": 1,
    "period": "2018 Q2",
    "title": "미중 무역전쟁의 서막",
    "desc": "트럼프 행정부가 중국산 수입품에 고율 관세를 부과하며 글로벌 공급망 긴장이 고조됩니다.",
    "round_news": [
      [
        "미국이 중국산 수입품에 고율 관세 부과를 예고했습니다.",
        "글로벌 교역 위축 가능성이 커지고 있습니다.",
        "수출 비중이 큰 기업들의 실적 우려가 제기됩니다."
      ],
      [
        "무역 갈등이 반도체와 제조업 공급망 전반으로 확산되고 있습니다.",
        "안전 자산 선호로 달러 관련 상품에 관심이 몰립니다.",
        "자동차·항공 등 경기민감 업종의 부담이 커지고 있습니다."
      ],
      [
        "관세 충격이 실제 기업 실적 전망에 반영되기 시작했습니다.",
        "반도체 수요 둔화 우려가 커집니다.",
        "방어적 자산과 환율 관련 상품의 상대적 강세가 나타납니다."
      ]
    ],
    "stocks": [
      {"name":"삼성전자","type":"주식","price":51000,"change_rate":-3.2,"intro":"국내 대표 반도체·전자 기업입니다.","hint":"수출 비중이 큰 반도체 기업은 무역분쟁 시 부담을 받을 수 있습니다."},
      {"name":"SK하이닉스","type":"주식","price":88000,"change_rate":-4.5,"intro":"메모리 반도체 중심 기업으로 경기와 반도체 업황의 영향을 크게 받습니다.","hint":"반도체 업황 둔화 뉴스가 나오면 부정적 영향을 받을 수 있습니다."},
      {"name":"LG화학","type":"주식","price":340000,"change_rate":-1.5,"intro":"배터리·석유화학 관련 기업입니다.","hint":"글로벌 경기 둔화 우려는 소재·화학주에 부담이 될 수 있습니다."},
      {"name":"NAVER","type":"주식","price":155000,"change_rate":0.8,"intro":"검색·플랫폼·콘텐츠 사업을 하는 인터넷 기업입니다.","hint":"플랫폼주는 제조업보다 무역분쟁 직접 영향이 작을 수 있습니다."},
      {"name":"현대차","type":"주식","price":150000,"change_rate":-5.2,"intro":"국내 대표 자동차 기업으로 수출과 경기 흐름의 영향을 받습니다.","hint":"관세와 수출 둔화 우려는 자동차주에 부담입니다."},
      {"name":"카카오","type":"주식","price":110000,"change_rate":1.2,"intro":"메신저·플랫폼·콘텐츠 사업을 하는 인터넷 기업입니다.","hint":"내수 플랫폼 성격이 있어 상대적으로 방어적일 수 있습니다."},
      {"name":"KODEX 200","type":"ETF","price":31000,"change_rate":-2.1,"intro":"코스피200 지수를 따라가는 대표 ETF입니다.","hint":"시장 전체가 흔들리면 지수형 ETF도 같이 영향을 받습니다."},
      {"name":"TIGER 2차전지테마","type":"ETF","price":14000,"change_rate":-1.0,"intro":"2차전지 관련 기업들을 묶어 투자하는 ETF입니다.","hint":"성장 테마 ETF는 시장 불안 시 변동성이 커질 수 있습니다."},
      {"name":"KODEX 미국달러선물","type":"ETF","price":11000,"change_rate":4.5,"intro":"달러 가치 상승에 투자하는 ETF입니다.","hint":"위기 국면에서는 달러 강세가 나타날 수 있습니다."},
      {"name":"S-Oil","type":"주식","price":95000,"change_rate":2.3,"intro":"정유 기업으로 유가와 정제마진의 영향을 받습니다.","hint":"유가 상승은 정유주에 긍정적으로 작용할 수 있습니다."},
      {"name":"대한항공","type":"주식","price":28000,"change_rate":-6.1,"intro":"항공 기업으로 유가와 여행 수요의 영향을 받습니다.","hint":"유가 상승과 여행 수요 둔화는 항공주에 부담입니다."},
      {"name":"포스코홀딩스","type":"주식","price":320000,"change_rate":-3.5,"intro":"철강 기업으로 원자재와 글로벌 경기 영향을 받습니다.","hint":"글로벌 교역 둔화는 철강 수요에 부담이 될 수 있습니다."}
    ]
  },
  {
    "stage": 2,
    "period": "2019 Q4",
    "title": "미중 1차 합의 기대감",
    "desc": "장기화된 무역 갈등이 해소될 기미를 보이면서 IT 대형주 중심의 랠리가 시작됩니다.",
    "round_news": [
      ["미중 1차 무역합의 가능성이 언급되기 시작했습니다.","투자심리가 점차 회복되고 있습니다.","반도체 업황 바닥 통과론이 나오고 있습니다."],
      ["무역분쟁 완화 기대감이 IT 대형주로 확산되고 있습니다.","코스피 회복 기대가 커지고 있습니다.","위험자산 선호 심리가 살아나고 있습니다."],
      ["합의 기대감이 강해지며 반도체·성장주 중심의 매수세가 유입됩니다.","바이오와 플랫폼주에도 긍정적 분위기가 이어집니다.","지수형 ETF와 레버리지 상품의 변동성이 커집니다."]
    ],
    "stocks": [
      {"name":"삼성전자","type":"주식","price":55800,"change_rate":4.5,"intro":"국내 대표 반도체·전자 기업입니다.","hint":"무역갈등 완화와 반도체 회복 기대는 긍정적일 수 있습니다."},
      {"name":"SK하이닉스","type":"주식","price":94100,"change_rate":6.2,"intro":"메모리 반도체 대표 기업입니다.","hint":"반도체 업황 회복 뉴스에 민감하게 반응할 수 있습니다."},
      {"name":"LG화학","type":"주식","price":317000,"change_rate":2.1,"intro":"배터리·석유화학 관련 기업입니다.","hint":"위험자산 선호 회복 시 성장산업에 관심이 생길 수 있습니다."},
      {"name":"NAVER","type":"주식","price":186000,"change_rate":3.5,"intro":"인터넷 플랫폼 기업입니다.","hint":"플랫폼주는 투자심리 회복 시 강세를 보일 수 있습니다."},
      {"name":"삼성바이오로직스","type":"주식","price":433000,"change_rate":5.0,"intro":"바이오의약품 위탁생산 기업입니다.","hint":"바이오 대형주는 안정적 성장 기대를 받을 수 있습니다."},
      {"name":"셀트리온","type":"주식","price":181000,"change_rate":1.8,"intro":"바이오 의약품 기업입니다.","hint":"바이오 업종은 시장 회복기에 관심을 받을 수 있습니다."},
      {"name":"KODEX 레버리지","type":"ETF","price":12500,"change_rate":8.2,"intro":"코스피 상승폭의 약 2배를 추종하는 ETF입니다.","hint":"시장이 오를 때 수익률이 커질 수 있지만 하락 시 위험도 큽니다."},
      {"name":"TIGER 반도체","type":"ETF","price":22000,"change_rate":7.5,"intro":"반도체 관련 종목에 투자하는 ETF입니다.","hint":"반도체 업황 개선 기대가 핵심입니다."},
      {"name":"KODEX 200","type":"ETF","price":29500,"change_rate":3.1,"intro":"코스피200 지수를 추종하는 ETF입니다.","hint":"시장 전체 회복에 투자하는 선택지입니다."},
      {"name":"SK이노베이션","type":"주식","price":150000,"change_rate":-0.5,"intro":"정유·배터리 관련 기업입니다.","hint":"정유와 배터리 이슈가 엇갈릴 수 있습니다."},
      {"name":"KB금융","type":"주식","price":47000,"change_rate":1.2,"intro":"금융지주회사로 금리와 경기 영향을 받습니다.","hint":"경기 회복 기대는 금융주에 일부 긍정적일 수 있습니다."},
      {"name":"LG전자","type":"주식","price":72000,"change_rate":2.8,"intro":"가전·전자제품 중심 기업입니다.","hint":"소비 회복과 전자 수요 개선 기대가 작용할 수 있습니다."}
    ]
  }
]

# 3~10스테이지도 자동 생성
EXTRA_STAGES = [
  ("2020 Q1","코로나19 팬데믹 충격","전 세계적인 전염병 확산으로 글로벌 증시가 역사적인 폭락장을 경험합니다.",
   ["중국에서 시작된 감염병 확산이 글로벌 이슈로 번지고 있습니다.","WHO가 팬데믹을 선언하며 글로벌 증시가 급락합니다.","각국 봉쇄 조치로 실물경제 충격이 커집니다."],
   [("삼성전자","주식",42300,-20.5),("SK하이닉스","주식",69000,-25.0),("LG화학","주식",230000,-18.0),("NAVER","주식",143000,-12.5),("씨젠","주식",110000,150.0),("현대차","주식",65000,-35.2),("KODEX 200선물인버스2X","ETF",12000,45.0),("KODEX 골드선물","ETF",13000,5.2),("TIGER 미국S&P500","ETF",11000,-15.5),("신한지주","주식",22000,-30.0),("대한항공","주식",13000,-45.0),("넷마블","주식",90000,-5.5)]),
  ("2020 Q3","BBIG 랠리의 시작","비대면 경제와 친환경 정책으로 바이오, 배터리, 인터넷, 게임주가 급등합니다.",
   ["코로나 이후 비대면 경제가 빠르게 확산되고 있습니다.","정부가 K-뉴딜 정책을 강조하며 성장산업에 관심이 몰립니다.","언택트와 친환경 테마가 강하게 상승합니다."],
   [("카카오","주식",350000,25.0),("LG화학","주식",700000,30.0),("삼성SDI","주식",450000,22.0),("NAVER","주식",300000,15.0),("엔씨소프트","주식",800000,10.0),("셀트리온","주식",320000,12.0),("KODEX BBIG","ETF",12000,24.0),("TIGER 2차전지테마","ETF",18000,28.0)]),
  ("2021 Q1","반도체 슈퍼사이클과 코스피 3000","코스피 지수가 역사상 처음으로 3000포인트를 돌파하며 반도체 대형주가 시장을 견인합니다.",
   ["코스피가 3000선 돌파를 시도하며 투자 열기가 강해집니다.","차량용 반도체 부족 이슈가 부각됩니다.","시장 전반의 상승 분위기가 레버리지 상품까지 자극합니다."],
   [("삼성전자","주식",91000,15.0),("SK하이닉스","주식",145000,12.0),("DB하이텍","주식",60000,20.0),("KODEX 레버리지","ETF",25000,28.0),("HMM","주식",35000,50.0),("현대차","주식",240000,18.0),("기아","주식",88000,15.0),("TIGER 반도체","ETF",31000,16.0)]),
  ("2021 Q4","인플레이션 공포와 테이퍼링","물가 상승 압력이 커지며 연준의 금리 인상 속도가 빨라질 것이라는 우려가 확산됩니다.",
   ["미국 물가 상승률이 높게 나오며 인플레이션 우려가 커집니다.","테이퍼링 가속화 가능성이 언급됩니다.","금리 인상 우려가 본격화되며 투자자들이 방어적으로 움직입니다."],
   [("KB금융","주식",55000,8.0),("하나금융지주","주식",42000,7.5),("신한지주","주식",38000,6.5),("삼성전자","주식",70000,-10.0),("카카오","주식",120000,-15.0),("NAVER","주식",360000,-12.0),("KODEX 인버스","ETF",4000,12.0),("SK이노베이션","주식",220000,-5.0)]),
  ("2022 Q1","러시아-우크라이나 전쟁 발발","지정학적 리스크로 유가와 원자재 가격이 폭등하며 전 세계 증시가 위축됩니다.",
   ["러시아와 우크라이나 간 긴장이 고조되고 있습니다.","전쟁 발발로 글로벌 금융시장이 충격을 받습니다.","지정학적 리스크가 장기화될 가능성이 제기됩니다."],
   [("한화에어로스페이스","주식",55000,20.0),("한국항공우주","주식",40000,18.0),("S-Oil","주식",110000,15.0),("LIG넥스원","주식",75000,25.0),("TIGER 원유선물","ETF",5000,30.0),("대한항공","주식",27000,-10.0),("KODEX 200","ETF",36000,-8.0),("포스코홀딩스","주식",290000,7.0)]),
  ("2022 Q3","금리 급등과 킹달러의 시대","미 연준의 자이언트 스텝 단행으로 달러 가치가 폭등하고 자산 가격이 급락합니다.",
   ["미국의 강한 금리 인상 가능성이 커지고 있습니다.","연준이 자이언트 스텝을 단행하며 시장이 흔들립니다.","킹달러 현상이 이어지며 글로벌 자금이 미국으로 이동합니다."],
   [("KODEX 미국달러선물레버리지","ETF",12000,15.0),("삼성전자","주식",55000,-8.0),("카카오","주식",50000,-25.0),("NAVER","주식",160000,-22.0),("LG에너지솔루션","주식",450000,5.0),("KODEX 인버스","ETF",5000,10.0),("KB금융","주식",48000,3.0),("TIGER 미국S&P500","ETF",13000,-12.0)]),
  ("2023 Q1","AI 혁명과 ChatGPT 열풍","생성형 AI 기술의 충격으로 AI 반도체와 HBM 관련주가 급반등합니다.",
   ["ChatGPT가 전 세계적으로 화제가 되고 있습니다.","AI 연산에 필요한 고성능 반도체 수요가 부각됩니다.","AI 산업 성장 기대가 관련 종목으로 확산됩니다."],
   [("SK하이닉스","주식",85000,12.0),("한미반도체","주식",25000,35.0),("이수페타시스","주식",15000,40.0),("삼성전자","주식",62000,5.0),("TIGER 미국나스닥100","ETF",13000,10.0),("NAVER","주식",210000,8.0),("카카오","주식",65000,5.0),("DB하이텍","주식",52000,11.0)]),
  ("2023 Q4","2차전지 조정과 온디바이스 AI","급등했던 2차전지주가 조정을 받는 가운데 온디바이스 AI 관련주가 부각됩니다.",
   ["2차전지 급등주에 대한 고평가 논란이 커지고 있습니다.","스마트폰과 기기 안에서 AI를 구동하는 온디바이스 AI가 부각됩니다.","금리 동결 기대감으로 성장주 투자심리가 일부 회복됩니다."],
   [("에코프로","주식",700000,-15.0),("에코프로비엠","주식",250000,-12.0),("제주반도체","주식",15000,45.0),("가온칩스","주식",45000,30.0),("포스코DX","주식",55000,8.0),("삼성전자","주식",73000,6.0),("SK하이닉스","주식",135000,12.0),("TIGER 2차전지테마","ETF",28000,-10.0)])
]

for idx, item in enumerate(EXTRA_STAGES, start=3):
    period, title, desc, news, stocks = item
    SCENARIO_DATA.append({
        "stage": idx,
        "period": period,
        "title": title,
        "desc": desc,
        "round_news": [
            [news[0], "관련 업종의 주가 변동성이 확대되고 있습니다.", "투자자들의 관심이 특정 테마로 이동하고 있습니다."],
            [news[1], "시장 분위기가 빠르게 변하고 있습니다.", "종목별 차별화가 나타나고 있습니다."],
            [news[2], "이전 라운드보다 가격 변화가 더 크게 반영됩니다.", "직전 라운드 결과를 보고 전략을 조정해야 합니다."]
        ],
        "stocks": [
            {
                "name": n,
                "type": t,
                "price": p,
                "change_rate": cr,
                "intro": f"{n} 관련 투자 자산입니다.",
                "hint": f"{title} 국면에서 {n}의 수익률 변화를 참고해보세요."
            }
            for n, t, p, cr in stocks
        ]
    })

START_CASH = 10_000_000

def format_krw(x):
    try:
        x = 0 if pd.isna(x) else float(x)
    except Exception:
        x = 0
    return f"{round(x):,}원"

def safe_qty(x):
    try:
        x = float(x)
    except Exception:
        return 0
    if math.isnan(x) or x < 0:
        return 0
    return int(math.floor(x))

def stocks_to_df(stage):
    df = pd.DataFrame(stage["stocks"])
    return df[["name", "type", "price", "change_rate", "intro", "hint"]].copy()

def empty_portfolio():
    return pd.DataFrame(columns=["name", "type", "qty", "avg_price", "last_price"])

def empty_history():
    return pd.DataFrame([{
        "stage": 1,
        "round": 1,
        "event": "게임 시작",
        "cash": START_CASH,
        "stock_value": 0,
        "total_asset": START_CASH,
    }])

def new_state(difficulty="초급"):
    state = {
        "cash": START_CASH,
        "portfolio": empty_portfolio(),
        "market": pd.DataFrame(),
        "stage_idx": 0,
        "round_idx": 0,
        "difficulty": difficulty,
        "last_round_result": pd.DataFrame(),
        "history": empty_history(),
        "notice": "게임이 시작되었습니다.",
    }
    add_or_update_stage_assets(state, 0)
    return state

def current_stage(state):
    return SCENARIO_DATA[state["stage_idx"]]

def current_stocks(state):
    return state.get("market", pd.DataFrame()).copy()

def add_or_update_stage_assets(state, stage_idx):
    st = SCENARIO_DATA[stage_idx]
    new_assets = stocks_to_df(st)
    new_assets["base_price"] = new_assets["price"]
    new_assets["current_price"] = new_assets["price"]
    new_assets["source_stage"] = stage_idx + 1
    new_assets["status"] = "초기 종목" if stage_idx == 0 else "신규 종목"

    if state["market"] is None or state["market"].empty:
        state["market"] = new_assets.reset_index(drop=True)
        return

    market = state["market"].copy()
    for _, asset in new_assets.iterrows():
        if asset["name"] in market["name"].values:
            row_idx = market.index[market["name"] == asset["name"]][0]
            for col in ["type", "price", "change_rate", "intro", "hint", "base_price", "current_price", "source_stage"]:
                market.at[row_idx, col] = asset[col]
            market.at[row_idx, "status"] = "기존 종목 갱신"
        else:
            market = pd.concat([market, pd.DataFrame([asset])], ignore_index=True)

    market.loc[market["source_stage"] < stage_idx + 1, "status"] = "이전 스테이지 누적"
    state["market"] = market.reset_index(drop=True)

def calc_assets(state):
    pf = state["portfolio"].copy()
    if pf.empty:
        return pf, 0, state["cash"]

    cs = current_stocks(state)
    pf["current_price"] = pf["last_price"]

    for i, row in pf.iterrows():
        matched = cs[cs["name"] == row["name"]]
        if not matched.empty:
            pf.at[i, "current_price"] = matched.iloc[0]["current_price"]

    pf["eval_amount"] = pf["qty"] * pf["current_price"]
    pf["buy_amount"] = pf["qty"] * pf["avg_price"]
    pf["profit_loss"] = pf["eval_amount"] - pf["buy_amount"]
    pf["return_rate"] = pf.apply(
        lambda r: (r["profit_loss"] / r["buy_amount"] * 100) if r["buy_amount"] > 0 else 0,
        axis=1,
    )

    stock_value = float(pf["eval_amount"].sum())
    total_asset = state["cash"] + stock_value
    return pf, stock_value, total_asset

def add_history(state, event_text):
    _, stock_value, total_asset = calc_assets(state)
    row = {
        "stage": state["stage_idx"] + 1,
        "round": state["round_idx"] + 1,
        "event": event_text,
        "cash": state["cash"],
        "stock_value": stock_value,
        "total_asset": total_asset,
    }
    state["history"] = pd.concat([state["history"], pd.DataFrame([row])], ignore_index=True)

def apply_round_price_change(state, to_round_1based):
    old_market = state["market"].copy()
    market = state["market"].copy()
    st = current_stage(state)
    stage_df = stocks_to_df(st)
    stage_names = set(stage_df["name"].tolist())

    progress_map = {1: 0, 2: 0.5, 3: 1}
    next_progress = progress_map.get(to_round_1based, 1)

    for i, row in market.iterrows():
        nm = row["name"]
        if nm in stage_names:
            stage_row = stage_df[stage_df["name"] == nm].iloc[0]
            next_price = round(stage_row["price"] * (1 + stage_row["change_rate"] / 100 * next_progress))
            market.at[i, "current_price"] = next_price

    state["market"] = market

    result = old_market.copy()
    result["new_price"] = market["current_price"]
    result["old_price"] = old_market["current_price"]
    result["round_return"] = result.apply(
        lambda r: round((r["new_price"] / r["old_price"] - 1) * 100, 2) if r["old_price"] > 0 else 0,
        axis=1,
    )
    result["is_current_stage"] = result["name"].apply(lambda x: 1 if x in stage_names else 0)
    result["abs_return"] = result["round_return"].abs()
    result = result.sort_values(["is_current_stage", "abs_return"], ascending=[False, False])

    view = result[["name", "type", "old_price", "new_price", "round_return", "status"]].copy()
    view.columns = ["종목명", "구분", "이전가격", "현재가격", "라운드수익률", "상태"]
    state["last_round_result"] = view
    return view

def account_summary_md(state):
    _, stock_value, total_asset = calc_assets(state)
    return f"""
### 나의 자산
- 현금 잔액: **{format_krw(state['cash'])}**
- 주식 평가액: **{format_krw(stock_value)}**
- 총 자산: <span style='color:#00A86B; font-weight:900; font-size:26px'>{format_krw(total_asset)}</span>

<span style='color:#607d8b'>수익률은 라운드 종료 후 결과 화면에서만 공개됩니다.</span>
"""

def round_info_md(state):
    st = current_stage(state)
    return f"""
### 게임 진행
- 현재 난이도: **{state['difficulty']}**
- 현재 스테이지: **Stage {state['stage_idx'] + 1} / {len(SCENARIO_DATA)}**
- 스테이지명: **{st['title']}**
- 현재 라운드: **{state['round_idx'] + 1} / 3**
"""

def market_info_html(state):
    st = current_stage(state)
    news_now = st["round_news"][state["round_idx"]]
    news_cards = "".join([
        f"""
        <div style='background:#eef9f4; border:1px solid #d6efe4; border-radius:12px; padding:12px; flex:1; min-height:95px;'>
          <span style='background:#00A86B; color:white; padding:3px 8px; border-radius:999px; font-size:12px; font-weight:700;'>NEWS</span>
          <p style='margin-top:10px;'>{x}</p>
        </div>
        """ for x in news_now
    ])
    return f"""
    <div style='background:white; border-radius:14px; padding:20px; box-shadow:0 4px 12px rgba(0,0,0,0.06);'>
      <div style='display:flex; justify-content:space-between; align-items:center; gap:10px; flex-wrap:wrap;'>
        <h2 style='margin:0;'>{st['period']} 시장 상황</h2>
        <span style='background:#263238; color:white; padding:5px 10px; border-radius:999px;'>Stage {state['stage_idx'] + 1} · Round {state['round_idx'] + 1}</span>
      </div>
      <p>{st['desc']}</p>
      <div style='display:flex; gap:12px; flex-wrap:wrap;'>{news_cards}</div>
    </div>
    """

def stock_choices(state):
    stocks = current_stocks(state)
    choices = []
    for i, row in stocks.iterrows():
        label = f"{row['name']} ({row['type']}) ｜ 현재가 {format_krw(row['current_price'])} ｜ {row['status']}"
        choices.append((label, int(i)))
    return choices

def selected_stock_info_md(state, stock_idx, qty):
    stocks = current_stocks(state)
    if stocks.empty or stock_idx is None:
        return "게임 시작 후 거래 종목이 표시됩니다."

    stock_idx = int(stock_idx)
    if stock_idx < 0 or stock_idx >= len(stocks):
        stock_idx = 0

    s = stocks.iloc[stock_idx]
    qty = safe_qty(qty)
    buy_amount = qty * s["current_price"]
    max_buy = int(state["cash"] // s["current_price"]) if s["current_price"] > 0 else 0

    own_qty = 0
    pf = state["portfolio"]
    if not pf.empty and s["name"] in pf["name"].values:
        own_qty = int(pf[pf["name"] == s["name"]].iloc[0]["qty"])

    extra = ""
    if state["difficulty"] == "초급":
        extra = f"\n- 자산 소개: {s['intro']}"
    elif state["difficulty"] == "중급":
        extra = f"\n- 투자 힌트: {s['hint']}"

    return f"""
### 선택 종목 정보
- 종목명: **{s['name']}**
- 현재가: **{format_krw(s['current_price'])}**
- 수익률: **라운드 종료 후 공개**{extra}
- 최대 매수 가능 수량: **{max_buy:,}주**
- 현재 보유 수량: **{own_qty:,}주**
- 입력 수량 기준 거래금액: **{format_krw(buy_amount)}**
"""

def stock_table_df(state):
    stocks = current_stocks(state)
    if stocks.empty:
        return pd.DataFrame({"안내": ["게임 시작 후 투자 가능 종목이 표시됩니다."]})

    stocks = stocks.sort_values(["source_stage", "name"], ascending=[False, True]).copy()

    if state["difficulty"] == "초급":
        view = stocks[["name", "type", "current_price", "status", "intro"]].copy()
        view.insert(3, "공개수익률", "라운드 종료 후 공개")
        view.columns = ["종목명", "구분", "현재가", "공개수익률", "상태", "자산소개"]
    elif state["difficulty"] == "중급":
        view = stocks[["name", "type", "current_price", "status", "hint"]].copy()
        view.insert(3, "공개수익률", "라운드 종료 후 공개")
        view.columns = ["종목명", "구분", "현재가", "공개수익률", "상태", "투자힌트"]
    else:
        view = stocks[["name", "type", "current_price", "status"]].copy()
        view.insert(3, "공개수익률", "라운드 종료 후 공개")
        view.columns = ["종목명", "구분", "현재가", "공개수익률", "상태"]

    view["현재가"] = view["현재가"].apply(lambda x: f"{int(round(x)):,}")
    return view.reset_index(drop=True)

def portfolio_table_df(state):
    pf, _, _ = calc_assets(state)
    if pf.empty:
        return pd.DataFrame({"안내": ["현재 보유 중인 종목이 없습니다."]})

    view = pd.DataFrame({
        "종목명": pf["name"],
        "구분": pf["type"],
        "보유수량": pf["qty"].astype(int),
        "평균단가": pf["avg_price"].round(0).astype(int),
        "현재가": pf["current_price"].round(0).astype(int),
        "매입금액": pf["buy_amount"].round(0).astype(int),
        "평가금액": pf["eval_amount"].round(0).astype(int),
        "평가손익": pf["profit_loss"].round(0).astype(int),
        "현재수익률": pf["return_rate"].apply(lambda x: f"{x:+.2f}%"),
    })

    for col in ["평균단가", "현재가", "매입금액", "평가금액", "평가손익"]:
        view[col] = view[col].apply(lambda x: f"{x:,}")

    return view.reset_index(drop=True)

def history_table_df(state):
    h = state["history"].copy()
    view = pd.DataFrame({
        "Stage": h["stage"],
        "Round": h["round"],
        "이벤트": h["event"],
        "현금": h["cash"].round(0).astype(int),
        "주식평가액": h["stock_value"].round(0).astype(int),
        "총자산": h["total_asset"].round(0).astype(int),
    })

    for col in ["현금", "주식평가액", "총자산"]:
        view[col] = view[col].apply(lambda x: f"{x:,}")

    return view.reset_index(drop=True)

def round_result_df(state):
    result = state.get("last_round_result", pd.DataFrame())
    if result is None or result.empty:
        return pd.DataFrame({"안내": ["아직 종료된 라운드가 없습니다."]})

    view = result.copy()
    view["이전가격"] = view["이전가격"].apply(lambda x: f"{int(round(x)):,}")
    view["현재가격"] = view["현재가격"].apply(lambda x: f"{int(round(x)):,}")
    view["라운드수익률"] = view["라운드수익률"].apply(lambda x: f"{x:+.2f}%")
    return view.reset_index(drop=True)

def all_outputs(state, selected_idx=None, qty=0):
    choices = stock_choices(state)

    if selected_idx is None and choices:
        selected_idx = choices[0][1]

    valid_values = [v for _, v in choices]
    if choices and selected_idx not in valid_values:
        selected_idx = choices[0][1]

    return (
        state,
        account_summary_md(state),
        round_info_md(state),
        market_info_html(state),
        gr.update(choices=choices, value=selected_idx),
        selected_stock_info_md(state, selected_idx, qty),
        stock_table_df(state),
        portfolio_table_df(state),
        history_table_df(state),
        round_result_df(state),
        state.get("notice", ""),
    )

def start_game(difficulty):
    state = new_state(difficulty)
    return all_outputs(state, None, 0)

def refresh_selected_info(state, stock_idx, qty):
    if state is None:
        state = new_state("초급")
    return selected_stock_info_md(state, stock_idx, qty)

def buy_stock(state, stock_idx, qty):
    if state is None:
        state = new_state("초급")

    stocks = current_stocks(state)
    if stocks.empty or stock_idx is None:
        state["notice"] = "거래 가능한 종목이 없습니다."
        return all_outputs(state, stock_idx, qty)

    stock_idx = int(stock_idx)
    s = stocks.iloc[stock_idx]
    qty = safe_qty(qty)

    if qty <= 0:
        state["notice"] = "거래 수량을 1주 이상 입력해주세요."
        return all_outputs(state, stock_idx, qty)

    total_cost = qty * s["current_price"]

    if state["cash"] < total_cost:
        state["notice"] = "현금 잔액이 부족합니다."
        return all_outputs(state, stock_idx, qty)

    state["cash"] -= total_cost
    pf = state["portfolio"].copy()

    if not pf.empty and s["name"] in pf["name"].values:
        row_idx = pf.index[pf["name"] == s["name"]][0]
        old_qty = pf.at[row_idx, "qty"]
        old_avg = pf.at[row_idx, "avg_price"]
        new_qty = old_qty + qty
        pf.at[row_idx, "avg_price"] = ((old_qty * old_avg) + total_cost) / new_qty
        pf.at[row_idx, "qty"] = new_qty
        pf.at[row_idx, "last_price"] = s["current_price"]
    else:
        pf = pd.concat([pf, pd.DataFrame([{
            "name": s["name"],
            "type": s["type"],
            "qty": qty,
            "avg_price": s["current_price"],
            "last_price": s["current_price"],
        }])], ignore_index=True)

    state["portfolio"] = pf
    add_history(state, f"{s['name']} {qty:,}주 매수")
    state["notice"] = f"{s['name']} {qty:,}주 매수 완료"
    return all_outputs(state, stock_idx, 0)

def sell_stock(state, stock_idx, qty):
    if state is None:
        state = new_state("초급")

    stocks = current_stocks(state)
    if stocks.empty or stock_idx is None:
        state["notice"] = "거래 가능한 종목이 없습니다."
        return all_outputs(state, stock_idx, qty)

    stock_idx = int(stock_idx)
    s = stocks.iloc[stock_idx]
    qty = safe_qty(qty)

    if qty <= 0:
        state["notice"] = "거래 수량을 1주 이상 입력해주세요."
        return all_outputs(state, stock_idx, qty)

    pf = state["portfolio"].copy()

    if pf.empty or s["name"] not in pf["name"].values:
        state["notice"] = "해당 종목을 보유하고 있지 않습니다."
        return all_outputs(state, stock_idx, qty)

    row_idx = pf.index[pf["name"] == s["name"]][0]
    own_qty = pf.at[row_idx, "qty"]

    if own_qty < qty:
        state["notice"] = "보유 수량이 부족합니다."
        return all_outputs(state, stock_idx, qty)

    sell_amount = qty * s["current_price"]
    state["cash"] += sell_amount
    pf.at[row_idx, "qty"] = own_qty - qty
    pf.at[row_idx, "last_price"] = s["current_price"]

    if pf.at[row_idx, "qty"] <= 0:
        pf = pf.drop(index=row_idx).reset_index(drop=True)

    state["portfolio"] = pf
    add_history(state, f"{s['name']} {qty:,}주 매도")
    state["notice"] = f"{s['name']} {qty:,}주 매도 완료"
    return all_outputs(state, stock_idx, 0)

def next_round(state, stock_idx, qty):
    if state is None:
        state = new_state("초급")

    current_stage_idx = state["stage_idx"]
    current_round_idx = state["round_idx"]
    current_round_1 = current_round_idx + 1

    if current_round_1 < 3:
        apply_round_price_change(state, current_round_1 + 1)
        state["round_idx"] = current_round_idx + 1
        add_history(
            state,
            f"Stage {current_stage_idx + 1} Round {current_round_1} 종료 / Round {state['round_idx'] + 1} 진입",
        )
        state["notice"] = f"Stage {current_stage_idx + 1} - Round {current_round_1} 결과가 공개되었습니다."

    else:
        apply_round_price_change(state, 3)
        add_history(
            state,
            f"Stage {current_stage_idx + 1} Round {current_round_1} 종료 / Stage {current_stage_idx + 1} 종료",
        )

        if current_stage_idx < len(SCENARIO_DATA) - 1:
            next_stage_idx = current_stage_idx + 1
            state["stage_idx"] = next_stage_idx
            state["round_idx"] = 0
            add_or_update_stage_assets(state, next_stage_idx)
            add_history(state, f"Stage {next_stage_idx + 1} 진입")
            state["notice"] = f"Stage {current_stage_idx + 1} - Round {current_round_1} 결과 공개 / 다음 스테이지: {SCENARIO_DATA[next_stage_idx]['title']}"

        else:
            _, _, total_asset = calc_assets(state)
            state["notice"] = f"게임 종료: 최종 자산 {format_krw(total_asset)}"

    return all_outputs(state, stock_idx, qty)

custom_css = """
body { background:#f5f7f8; }
.gradio-container { font-family: 'Noto Sans KR', sans-serif; }
#title { color:#00A86B; font-weight:900; }
"""

with gr.Blocks(css=custom_css, title="하나모아 모의투자 게임") as demo:
    gr.Markdown("# 하나모아 모의투자 게임", elem_id="title")
    gr.Markdown("Colab용 버전입니다. 난이도를 선택한 뒤 게임 시작을 누르면 진행됩니다.")

    state_box = gr.State(new_state("초급"))

    with gr.Row():
        difficulty = gr.Radio(
            choices=["초급", "중급", "고급"],
            value="초급",
            label="게임 난이도",
            info="초급: 자산 소개 / 중급: 투자 힌트 / 고급: 힌트 없음",
        )
        start_btn = gr.Button("게임 시작 / 초기화", variant="primary")

    notice = gr.Textbox(label="알림", interactive=False)

    with gr.Row():
        with gr.Column(scale=1):
            account_md = gr.Markdown()
            round_md = gr.Markdown()
            next_btn = gr.Button("다음 라운드로", variant="primary")

        with gr.Column(scale=3):
            market_html = gr.HTML()
            gr.Markdown("## 거래하기")
            trade_stock = gr.Dropdown(label="거래 종목 선택", choices=[], value=None)
            trade_qty = gr.Number(label="거래 수량", value=0, precision=0)
            selected_info = gr.Markdown()

            with gr.Row():
                buy_btn = gr.Button("매수", variant="primary")
                sell_btn = gr.Button("매도")

    with gr.Tabs():
        with gr.Tab("투자 가능 종목"):
            stock_table = gr.Dataframe(label="투자 가능 종목", interactive=False, wrap=True)

        with gr.Tab("포트폴리오"):
            portfolio_table = gr.Dataframe(label="내 보유 자산 상세", interactive=False, wrap=True)

        with gr.Tab("라운드 결과"):
            round_result_table = gr.Dataframe(label="직전 라운드 수익률", interactive=False, wrap=True)

        with gr.Tab("게임 결과"):
            history_table = gr.Dataframe(label="자산 변화", interactive=False, wrap=True)

        with gr.Tab("게임방법"):
            gr.Markdown("""
### 1. 게임의 목적
각 스테이지별 경제 상황과 시황 뉴스를 보고 주식 또는 ETF를 매수·매도하여 최종 자산을 최대화하는 게임입니다.

### 2. 기본 진행 방식
- 처음 시작 자산은 10,000,000원입니다.
- 게임은 총 10개 스테이지로 구성되어 있습니다.
- 각 스테이지는 3개 라운드로 진행됩니다.
- 라운드가 넘어갈수록 해당 시기의 시장 변화가 가격에 반영됩니다.
- 매수와 매도는 거래하기 영역에서 진행합니다.
- 스테이지가 넘어가면 이전 종목은 유지되고, 새로운 종목이 누적됩니다.

### 3. 수익률 공개 방식
- 라운드 진행 중에는 전체 공개 수익률이 보이지 않습니다.
- [다음 라운드로] 버튼을 눌러 라운드를 종료하면, 방금 끝난 라운드의 수익률 표가 공개됩니다.
- [포트폴리오]에서는 현재 보유 자산의 현재 수익률을 확인할 수 있습니다.

### 4. 난이도
- 초급: 각 자산이 어떤 종목인지 한 줄 소개가 제공됩니다.
- 중급: 시장 배경을 바탕으로 한 투자 힌트가 제공됩니다.
- 고급: 별도 힌트 없이 뉴스와 가격만 보고 판단합니다.

### 5. 유의사항
이 게임은 교육용 모의투자 게임이며, 실제 투자 수익을 보장하지 않습니다.
""")

    outputs = [
        state_box,
        account_md,
        round_md,
        market_html,
        trade_stock,
        selected_info,
        stock_table,
        portfolio_table,
        history_table,
        round_result_table,
        notice,
    ]

    start_btn.click(start_game, inputs=[difficulty], outputs=outputs)
    trade_stock.change(refresh_selected_info, inputs=[state_box, trade_stock, trade_qty], outputs=[selected_info])
    trade_qty.change(refresh_selected_info, inputs=[state_box, trade_stock, trade_qty], outputs=[selected_info])
    buy_btn.click(buy_stock, inputs=[state_box, trade_stock, trade_qty], outputs=outputs).then(lambda: 0, outputs=[trade_qty])
    sell_btn.click(sell_stock, inputs=[state_box, trade_stock, trade_qty], outputs=outputs).then(lambda: 0, outputs=[trade_qty])
    next_btn.click(next_round, inputs=[state_box, trade_stock, trade_qty], outputs=outputs)
    demo.load(start_game, inputs=[difficulty], outputs=outputs)

demo.launch(share=True, debug=False)
