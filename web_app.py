import streamlit as st
import redis
import pandas as pd
import os
from dotenv import load_dotenv
from datetime import datetime

# 載入 .env 檔案
load_dotenv()

# --- 1. 設定網頁標題 ---
st.set_page_config(page_title="Redis 極速排行榜", page_icon="🏆")
st.title("🏆 Redis 極速遊戲排行榜")
st.write("這是使用 Python + Streamlit + Redis Cloud 打造的即時系統～✨")

# --- 2. 連線到 Redis (不使用 cache 避免報錯) ---
def get_redis_connection():
    try:
        return redis.Redis(
            host=os.getenv("REDIS_HOST"),       # 改成讀取環境變數
            port=int(os.getenv("REDIS_PORT")),  # 改成讀取環境變數
            decode_responses=True,
            username="default",
            password=os.getenv("REDIS_PASSWORD"), # 改成讀取環境變數
            ssl=False
        )
    except Exception as e:
        st.error(f"無法連線到 Redis: {e}")
        return None

r = get_redis_connection()
# --- 3. 側邊欄：輸入成績 ---
with st.sidebar:
    st.header("📝 登記成績")
    name_input = st.text_input("玩家暱稱")
    score_input = st.number_input("分數", min_value=0, max_value=100000, step=10)
    
    if st.button("送出成績"):
        if name_input and score_input > 0:
            
            # --- 🔥 新增功能：檢查是否破紀錄 🔥 ---
            key = "test_leaderboard"
            old_score = r.zscore(key, name_input) # 先去 Redis 查舊分數
            
            is_new_record = False
            msg_title = ""
            msg_body = ""

            if old_score is None:
                # 從來沒玩過
                is_new_record = True
                msg_title = "🎉 歡迎新玩家！"
                msg_body = f"首度登錄成績：{score_input} 分"
            elif score_input > old_score:
                # 破紀錄了
                is_new_record = True
                msg_title = "🎉 太神啦！打破個人紀錄！"
                msg_body = f"舊分數：{int(old_score)} → 新分數：{score_input}"
            else:
                # 沒破紀錄
                msg_title = "💪 再接再厲！"
                msg_body = f"這次獲得 {score_input} 分 (您的最高紀錄是 {int(old_score)} 分)"

            # --- 使用 Pipeline ---
            pipe = r.pipeline()
            pipe.zadd(key, {name_input: score_input}) 
            
            time_str = datetime.now().strftime("%H:%M:%S")
            log_msg = f"[{time_str}] 玩家 {name_input} 獲得了 {score_input} 分！"
            pipe.lpush("test_activity", log_msg)
            pipe.ltrim("test_activity", 0, 9)
            pipe.execute()
            
            # --- 顯示結果 (使用 Toast 或 Success) ---
            if is_new_record:
                st.balloons() # 🎈 放氣球特效！
                # 這裡不加 time.sleep 或 rerun，讓訊息和特效自然停留！
                st.success(f"{msg_title} {msg_body}") 
            else:
                st.info(f"{msg_title} {msg_body}")
                
            # st.rerun() / time.sleep(1.5) 這兩行都刪除！讓 Streamlit 自己處理顯示。
        else:
            st.warning("⚠️ 請輸入名字並確認分數大於 0")

# 舊版分隔線寫法
st.markdown("---")

# 移除 type="primary" 避免舊版報錯
st.subheader("🗑️ 系統管理")

if st.button("重置所有資料", key="reset_main"):
    r.delete("test_leaderboard", "test_activity")
    st.success("所有資料已重置！")
    st.experimental_rerun()# <--  新版指令 st.rerun()，改用舊版 st.experimental_rerun()

# --- 4. 主畫面：顯示排行榜與動態 ---

col1, col2 = st.columns(2)

with col1:
    st.subheader("👑 榮耀名人堂 (Top 10排行)")
    leaderboard_data = r.zrevrange("test_leaderboard", 0, 9, withscores=True)
    
    # 顯示 Top 10 表格
    if leaderboard_data:
        df = pd.DataFrame(leaderboard_data, columns=["玩家", "分數"])
        df.index += 1
        df["分數"] = df["分數"].astype(int) 
        st.table(df)
        
        # --- 🔥 11/25 新增圖表區塊 🔥 ---
        st.markdown("---")
        st.subheader("📊 分數視覺分析")
        st.caption("即時戰況分佈圖")
        
        # 將玩家名稱設為索引，然後只顯示分數欄位
        df_chart = df.set_index('玩家') 
        # 使用 Streamlit 內建的柱狀圖功能
        st.bar_chart(df_chart[['分數']])
        # ----------------------------------
        
    else:
        st.info("目前還沒有排名資料")
    
    st.markdown("---") # 分隔線
    
    # --- 🔥 11/25 新增個人查詢 🔥 ---
    st.subheader("🔍 查詢您的排名")
    # 使用 Streamlit 的輸入框讓使用者輸入暱稱
    player_name_query = st.text_input("輸入您的暱稱", key="player_rank_query")
    
    if player_name_query:
        key = "test_leaderboard"
        
        # 1. 使用 ZREVRANK 查詢倒序排名 (從 0 開始)
        rank_index = r.zrevrank(key, player_name_query)
        
        if rank_index is not None:
            actual_rank = rank_index + 1 # 實際排名是索引 + 1
            score = r.zscore(key, player_name_query) # 取得分數
            
            st.success(f"**玩家：{player_name_query}**")
            st.metric(label="您的目前排名", value=f"第 {actual_rank} 名")
            st.metric(label="您的分數", value=f"{int(score)} 分")

            if actual_rank > 10:
                st.info("🔥 雖然不在 Top 10，但您已經超越了許多玩家！繼續努力！")
            
        else:
            st.warning(f"⚠️ 找不到玩家 **{player_name_query}** 的成績。")

with col2:
    st.subheader("📢 最新動態牆")
    logs = r.lrange("test_activity", 0, -1)
    
    if logs:
        for log in logs:
            st.text(log)
    else:
        st.info("目前沒有最新動態")