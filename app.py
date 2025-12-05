import redis
import os
from dotenv import load_dotenv
from datetime import datetime

# 載入 .env 檔案中的環境變數
load_dotenv()

# --- 1. 連線設定 ---
try:
    r = redis.Redis(
        host=os.getenv("REDIS_HOST"),       # 讀取環境變數
        port=int(os.getenv("REDIS_PORT")),  # 讀取環境變數 (轉成整數)
        decode_responses=True,
        username="default",
        password=os.getenv("REDIS_PASSWORD"), # 讀取環境變數
        ssl=False
    )
    r.ping()
    print("✅ 成功連線到 Redis！(已啟用 Pipeline 功能)")
except Exception as e:
    print("❌ 無法連線到 Redis！")
    print("錯誤內容:", e)
    exit()

# --- 2. 功能函數定義 (必須放在主程式上面！) ---

def show_leaderboard():
    key = "test_leaderboard"
    
    # --- 顯示 Top 10 ---
    print("\n🥇 目前排名 (Top 10)")
    leaderboard_data = r.zrevrange(key, 0, 9, withscores=True)
    
    if leaderboard_data:
        for i, (name, score) in enumerate(leaderboard_data, start=1):
            print(f"{i}. {name} - {int(score)} 分")
    else:
        print("目前還沒有人有成績，快去登記！")
    
    print("---")
    
    # --- 查詢自己的排名 ---
    player_name = input("輸入您的暱稱以查看您的排名 (留白跳過): ").strip()
    
    if player_name:
        # 使用 ZREVRANK 查詢倒序排名 (從 0 開始)
        rank_index = r.zrevrank(key, player_name)
        
        if rank_index is not None:
            actual_rank = rank_index + 1 # 實際排名是索引 + 1
            score = r.zscore(key, player_name) # 取得分數
            
            print(f"\n✨ 您的個人排名:")
            print(f"> 玩家: {player_name}")
            print(f"> 排名: 第 {actual_rank} 名")
            print(f"> 分數: {int(score)} 分")
            
            # 給予 Top 10 以外的玩家一些額外的回饋(鼓勵)
            if actual_rank > 10:
                 print("> 離 Top 10 只差一點點，繼續加油！")
            
        else:
            print(f"\n⚠️ 找不到玩家 '{player_name}' 的成績。")

def show_activity():
    print("\n📢 最新動態")
    logs = r.lrange("test_activity", 0, -1)
    if logs:
        for log in logs:
            print(log)
    else:
        print("目前沒有最新動態。")

def add_score():
    # 這就是你要的 Pipeline 加分版本
    name = input("請輸入玩家暱稱: ").strip()
    if not name:
        print("⚠️ 玩家名字不可空白")
        return
    try:
        score = int(input("請輸入分數 (0~10000): "))
    except ValueError:
        print("⚠️ 分數必須是數字")
        return
    if score <= 0:
        print("⚠️ 分數必須大於 0")
        return
    
    # --- 使用 Pipeline 打包指令  ---
    pipe = r.pipeline() 
    pipe.zadd("test_leaderboard", {name: score})
    
    time_str = datetime.now().strftime("%H:%M:%S")
    log_msg = f"[{time_str}] 玩家 {name} 獲得了 {score} 分！"
    pipe.lpush("test_activity", log_msg)
    pipe.ltrim("test_activity", 0, 9)
    
    pipe.execute() # 一次發送
    # -------------------------------------
    
    print(f"✅ {name} 的成績已上傳！(Pipeline 傳輸完成)")

def reset_data():
    confirm = input("⚠️ 確定要重置所有資料嗎？ (yes/no): ").lower()
    if confirm == "yes":
        r.delete("test_leaderboard", "test_activity")
        print("✅ 所有資料已重置！")
    else:
        print("取消重置。")

# --- 3. 主程式迴圈 (一定要放在最下面) ---
while True:
    print("\n==== Redis 極速遊戲排行榜 ====")
    print("1. 顯示排行榜")
    print("2. 顯示最新動態")
    print("3. 登記成績 (Pipeline 加速版)")
    print("4. 重置所有資料")
    print("0. 離開")
    choice = input("請選擇操作: ").strip()
    
    if choice == "1":
        show_leaderboard()
    elif choice == "2":
        show_activity()
    elif choice == "3":
        add_score()  # 這裡會去呼叫上面的 def add_score()
    elif choice == "4":
        reset_data()
    elif choice == "0":
        print("👋 掰掰！")
        break
    else:
        print("⚠️ 請輸入有效選項")