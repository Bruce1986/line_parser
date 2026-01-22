"""
Project: Line Chat Parser
Authors: Bruce & Antigravity
Date: 2026-01-22

Description:
    This script parses LINE chat log text files and converts them into a readable HTML format.
    It handles message filtering, special name parsing, and visual styling for a better reading experience.

Usage:
    1. Place your LINE chat history .txt files in the same directory as this script.
    2. Run the script directly to process all .txt files in the directory:
       $ python line_parser.py
    3. Or run with a specific file argument:
       $ python line_parser.py specific_chat_log.txt

    The script will generate corresponding .html files in the same directory.

描述：
    此腳本用於解析 LINE 對話紀錄文字檔 (.txt)，並將其轉換為易於閱讀的 HTML 格式。
    它具備訊息過濾、特殊名稱解析以及最佳化閱讀體驗的視覺樣式功能。

使用說明：
    1. 將您的 LINE 對話紀錄 .txt 檔案放在此腳本所在的同一個目錄下。
    2. 直接執行腳本以處理目錄下的所有 .txt 檔案：
       $ python line_parser.py
    3. 或者透過參數指定特定的檔案：
       $ python line_parser.py specific_chat_log.txt

    腳本將在相同目錄下生成對應的 .html 檔案。
"""
import os
import sys
import re
import html
from datetime import datetime

# ================= 設定區 =================
# 指定您的 txt 檔案所在的資料夾路徑
SOURCE_DIR = os.path.dirname(os.path.abspath(__file__))
# OUTPUT_FILE = os.path.join(SOURCE_DIR, 'line_chat_viewer.html')
MAX_LINES = 7
MAX_DISPLAY_MSGS = 5000 # 限制顯示最近的 N 則訊息，避免瀏覽器崩潰

# ================= 樣式與 HTML 模板 =================
HTML_TEMPLATE_START = """
<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Line 對話紀錄整理 (已過濾長訊)</title>
    <style>
        body { font-family: "Microsoft JhengHei", "Helvetica Neue", sans-serif; background-color: #f0f2f5; margin: 0; padding: 20px; }
        .container { max-width: 800px; margin: 0 auto; background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
        h1 { text-align: center; color: #00B900; }
        .file-header { background-color: #eee; padding: 10px; margin-top: 30px; border-radius: 5px; font-weight: bold; color: #555; border-left: 5px solid #00B900; }
        .date-divider { text-align: center; margin: 20px 0; position: -webkit-sticky; position: sticky; top: 10px; z-index: 1000; pointer-events: none; }
        .date-divider span { background-color: #dcf8c6; padding: 5px 15px; border-radius: 15px; font-size: 0.8em; color: #555; box-shadow: 0 1px 2px rgba(0,0,0,0.1); display: inline-block; }
        .message { display: flex; margin-bottom: 15px; align-items: flex-start; }
        .avatar { width: 40px; height: 40px; background-color: #ddd; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: bold; color: #fff; margin-right: 10px; flex-shrink: 0; font-size: 14px;}
        .content-wrapper { max-width: 80%; }
        .sender-name { font-size: 0.8em; color: #888; margin-bottom: 2px; }
        .bubble { background-color: #e9e9eb; padding: 10px 15px; border-radius: 15px; position: relative; line-height: 1.5; white-space: pre-wrap; word-break: break-all;}
        .bubble.filtered { background-color: #ffebee; color: #c62828; font-style: italic; }
        .time { font-size: 0.7em; color: #aaa; margin-top: 5px; text-align: right; }
        
        /* 簡單的顏色生成邏輯 */
        .color-0 { background-color: #FF5722; }
        .color-1 { background-color: #2196F3; }
        .color-2 { background-color: #9C27B0; }
        .color-3 { background-color: #4CAF50; }
        .color-4 { background-color: #FFC107; text-color: #333;}
    </style>
</head>
<body>
    <div class="container">
        <h1>Line 對話紀錄閱覽器 (近期訊息)</h1>
        <p style="text-align:center; color: #666;">
            過濾條件：忽略超過 {max_lines} 行的訊息 | 
            顯示限制：最新的 {max_msgs} 則
        </p>
"""

HTML_TEMPLATE_END = """
    </div>
</body>
</html>
"""

SPECIAL_NAMES = [
    'Kevin 侯Belong to GOD',
    'Bruce 布魯斯張 🥉',
    '林立皋 Eric',
    'Lan 重元',
    "山姆．奧特曼AI 顧問 × 北科大 凱文 from 'AI小幫手'",
    "gpt-4o-mini from 'AI小幫手'",
    'Edwin Yang 楊聰榮Taiwan',
    'Arthur 蔣紀綱 （方德背客故事長）',
    '陳泳睿(Antoine 安東尼）線束加工',
    'Morris Lu - AI Robot',
    '黃世昌 AI晶片 算法 算力 光達 雷達',
    '渤浚/Bogi AI自動化顧問、天使投資',
    '王進忠-赫曼咖啡 （沒有速度⋯沒有進度）',
    'Shang-Yu Scott Huang',
    '林國平Kevin 建築•室內•設計施工',
    'Edwin Yang 聰榮（Vinh）',
    '黃武章 Wu-Jang Huang',
    'Yung-Pin Cheng(鄭）',
    'Leo 俊志 立鋒Mixcore',
    'Shui Shou, Wang',
    '林家振Jonathan Lin',
    '周宏雋 David Chou',
    '翁昕瑀 Christine',
    '林彥廷 Roy（古書男子）',
    'Johnason Chen',
    'Giselle Wang',
    '陳凱爾Kyle ไคล์',
    'M. Human 陳護木',
    'Morris Sun 孫',
    'Watson Tsai',
    'Richard 廖冠傑',
    'daniel weng',
    'Willy Ruan',
    'Jordan Lin',
    'Yvonne Hsu',
    'Kevin Tsai',
    '卡斯 ▵ Lucas',
    'Robert Wu',
    'Miss Yang',
    'john吳 吳震廷',
    'Bruce Lin',
    '高振軒 Kazen',
    '余紹銘 Brian',
    'Kai (亞馬遜)',
    '正道 M Chen',
    'Rick Chen',
    'Jazz Wang',
    '羅鴻陞 Alan',
    'Alan 陳議添',
    '鵬 steven',
    'Aha Lin',
    'Niel 若庠',
    'James Shih',
    "AI 論文導讀 X 北科大EMBA侯凱文 from 'AI小幫手'",
    "會議錄音 from 'AI小幫手'",
    "巴菲特ROE企業分析 from 'AI小幫手'",
    "grok-4-fast from 'AI小幫手'",
]

def get_avatar_color(name):
    """根據名字生成固定的顏色 class"""
    hash_val = sum(ord(c) for c in name)
    return f"color-{hash_val % 5}"

def auto_detect_names(lines):
    """
    分析整個檔案，找出可能是名字的字串。
    邏輯：
    1. 抓取所有時間開頭的行
    2. 取得去除時間後的內容
    3. 統計前綴詞出現的頻率 (例如 "Kevin", "Kevin 侯", "Kevin 侯Belong"...)
    4. 如果長的前綴詞出現頻率很高，且經常後面接不同的內容，則視為名字
    """
    print("正在自動分析對話中的名字...")
    from collections import Counter
    
    time_pattern = re.compile(r'^(\d{1,2}:\d{2}|上午 \d{1,2}:\d{2}|下午 \d{1,2}:\d{2})')
    
    # 候選名字計數器
    candidate_counts = Counter()
    # 記錄每個候選名字後面接的"不同內容"的數量 (用來判斷這是否為名字)
    # 例如 "Dave" 後面接 "Hi", "Dave" 後面接 "早安" -> diversity = 2
    candidate_diversity = {} 

    for line in lines:
        line = line.strip('\n')
        if not line: continue
        
        match = time_pattern.match(line)
        if match:
            # 取得時間後面的內容
            content = line[match.end():].strip()
            
            # 如果有 Tab，Tab 前面通常就是名字 (這是 Line 電腦版最穩定的格式)
            if '\t' in content:
                name = content.split('\t')[0]
                candidate_counts[name] += 100 # 給予高權重
                continue

            # --- 新增：從系統訊息"偷"名字 ---
            # 模式 1: XXX已加入群組
            # 模式 2: XXX已退出群組
            # 模式 3: XXX邀請YYY加入群組
            # 模式 4: XXX已將YYY退出群組
            
            sys_match_1 = re.match(r'^(.*)已加入群組。$', content)
            if sys_match_1:
                name = sys_match_1.group(1).strip()
                if name: candidate_counts[name] += 200 # 最高權重，系統保證
                continue

            sys_match_2 = re.match(r'^(.*)已退出群組。$', content)
            if sys_match_2:
                name = sys_match_2.group(1).strip()
                if name: candidate_counts[name] += 200
                continue
                
            sys_match_3 = re.match(r'^(.*)邀請(.*)加入群組。$', content)
            if sys_match_3:
                inviter = sys_match_3.group(1).strip()
                invitee = sys_match_3.group(2).strip()
                if inviter: candidate_counts[inviter] += 200
                if invitee: candidate_counts[invitee] += 200
                continue

            sys_match_4 = re.match(r'^(.*)已將(.*)退出群組。$', content)
            if sys_match_4:
                admin = sys_match_4.group(1).strip()
                victim = sys_match_4.group(2).strip()
                if admin: candidate_counts[admin] += 200
                if victim: candidate_counts[victim] += 200
                continue
            # ---------------------------------
                
            # 如果有雙空格，通常也是名字分隔
            if '  ' in content:
                name = re.split(r'\s{2,}', content)[0]
                candidate_counts[name] += 50
                continue
            
            # 如果只有單空格，情況較複雜 (例如 "Bruce Lin 早安")
            # 我們嘗試切分出前 1~3 個 token 作為潛在名字
            parts = content.split(' ')
            max_tokens = min(len(parts), 4) # 最多假設名字有 4 個詞 (例如 "Kevin 侯 Belong to GOD")
            
            for i in range(1, max_tokens + 1):
                potential_name = " ".join(parts[:i])
                # 排除太長的名字 (例如超過 30 字元)
                if len(potential_name) > 30: continue
                
                # 簡單過濾掉明顯不是名字的 (例如由純數字組成，或包含奇怪符號)
                # 這裡先不做太嚴格過濾
                
                candidate_counts[potential_name] += 1
                
                # 記錄這個潛在名字後面的內容 (用來計算多樣性)
                remainder = " ".join(parts[i:])
                if potential_name not in candidate_diversity:
                    candidate_diversity[potential_name] = set()
                if len(candidate_diversity[potential_name]) < 10: # 只需存前 10 個不同的就好，省記憶體
                    candidate_diversity[potential_name].add(remainder)

    # 篩選階段
    detected_names = []
    
    # 建立候選名單集合，方便查找
    all_candidates = set(candidate_counts.keys())
    
    # helper: 檢查是否為強連結 (Strong Binding)
    # 例如 "林立皋" (count=10) 與 "林立皋 Eric" (count=9)
    # 代表 "林立皋" 有 90% 的機率後面接 "Eric"，這時候應該視 "林立皋 Eric" 為完整名字
    def is_strong_binding(base_name, count):
        # 尋找是否有開頭為 base_name + space 的更長候選人
        best_extension = None
        max_ext_count = 0
        
        for cand in all_candidates:
            if cand != base_name and cand.startswith(base_name + " "):
                c_count = candidate_counts[cand]
                if c_count > max_ext_count:
                    max_ext_count = c_count
                    best_extension = cand
        
        # 如果延伸版本的出現頻率佔原本的 70% 以上，且延伸版本本身也夠多 (>2)
        if best_extension and max_ext_count > 0 and (max_ext_count / count) > 0.7 and max_ext_count > 2:
            return best_extension
        return None

    # 1. 優先加入 Tab/雙空格 識別出的 (權重 > 20)
    for name, count in candidate_counts.items():
        if count > 20 and name not in SPECIAL_NAMES:
            detected_names.append(name)
            
    # 2. 加入單空格推測的
    for name, count in candidate_counts.items():
        if count > 5: # 出現超過 5 次 (基本門檻)
            diversity = len(candidate_diversity.get(name, []))
            
            # 檢查是否有更 "強" 的長名字版本
            strong_extension = is_strong_binding(name, count)
            if strong_extension:
                # 如果有強連結 (例如 林立皋 -> 林立皋 Eric)，優先加入長版本
                if strong_extension not in SPECIAL_NAMES and strong_extension not in detected_names:
                    detected_names.append(strong_extension)
                # 短版本通常就略過，或者是也加入但排序在後 (parse_line_log 會自動 sort by len)
                continue
            
            # 一般多樣性檢查
            if diversity >= 3 and name not in SPECIAL_NAMES and name not in detected_names:
                detected_names.append(name)
                
    # 額外補強：針對 "Name EngName" 類似 "林立皋 Eric" 這種組合
    # 如果 "林立皋 Eric" 被上面的 strong_binding 抓到了，那很好
    # 如果沒抓到 (可能比例不到 80%)，但它的 diversity 夠高，原本的邏輯也會抓到
    # 所以上述邏輯應該足夠處理大部分 "固定後綴" 的情況

    print(f"自動偵測到 {len(detected_names)} 個新名字 (例如: {detected_names[:5]})...")
    return detected_names

def parse_line_log(file_path):
    """解析單個 txt 檔案"""
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # --- 自動分析階段 ---
    # 動態擴充 SPECIAL_NAMES
    global SPECIAL_NAMES
    new_names = auto_detect_names(lines)
    if new_names:
        # 將新舊名單合併
        combined_names = set(SPECIAL_NAMES + new_names)
        # 轉回 List 並依長度排序 (長的優先匹配)
        SPECIAL_NAMES = sorted(list(combined_names), key=len, reverse=True)
    # -------------------


    parsed_msgs = []
    current_date = ""
    
    # 正則表達式：匹配時間 (e.g., 22:05, 上午 10:00)
    time_pattern = re.compile(r'^(\d{1,2}:\d{2}|上午 \d{1,2}:\d{2}|下午 \d{1,2}:\d{2})')
    # 支援 YYYY/MM/DD 或 YYYY.MM.DD (Line 電腦版與手機版匯出格式可能不同)
    date_pattern = re.compile(r'^\d{4}[/.][\d]{2}[/.][\d]{2}')

    # 暫存變數
    temp_msg = None 
    current_msg_lines = [] 

    for line in lines:
        line = line.strip('\n') # 保留行內的空格，只去尾端換行
        if not line: continue

        # 1. 檢查是否為日期分隔線
        if date_pattern.match(line):
            current_date = line
            continue

        # 2. 檢查是否為新訊息的開頭 (以時間開頭)
        time_match = time_pattern.match(line)
        if time_match:
            # 如果有前一則訊息，先存起來
            if temp_msg:
                temp_msg['content'] = '\n'.join(current_msg_lines)
                parsed_msgs.append(temp_msg)
                temp_msg = None # 重置
                current_msg_lines = []
            
            # 取得時間字串與剩餘內容
            time_str = time_match.group(0)
            rest_line = line[len(time_str):].strip()
            
            name = ""
            content = ""
            
            # 優先檢查特殊名單
            is_special_name = False
            for special_name in SPECIAL_NAMES:
                if rest_line.startswith(special_name):
                    name = special_name
                    content = rest_line[len(special_name):].strip()
                    is_special_name = True
                    break
            
            # Checks for system event patterns (Join/Leave group)
            # 放在特殊名單之後，但在一般分割之前
            # 如果整行符合特定結尾，視為系統訊息
            system_suffixes = ['已退出群組。', '已加入群組。', '邀請.*加入群組。', '已將.*退出群組。']
            is_system_msg = False
            for suffix in system_suffixes:
                 if re.search(suffix + '$', rest_line):
                     is_system_msg = True
                     break
            
            if is_system_msg:
                # 系統訊息：沒有名字，內容為整行
                name = ""
                content = rest_line
                # 這裡不需切分
            elif not is_special_name:
                # 嘗試切分名字與內容
                if '\t' in rest_line:
                    parts = rest_line.split('\t', 1)
                    name = parts[0]
                    content = parts[1] if len(parts) > 1 else ""
                elif '  ' in rest_line:
                     parts = re.split(r'\s{2,}', rest_line, maxsplit=1)
                     name = parts[0]
                     content = parts[1] if len(parts) > 1 else ""
                elif ' ' in rest_line:
                    parts = rest_line.split(' ', 1)
                    name = parts[0]
                    content = parts[1] if len(parts) > 1 else ""
                else:
                    # 無法切分，假設整行是名字? 或整行是內容? 
                    # 通常視為內容，名字留空 (或視為系統訊息)
                    content = rest_line
                
            temp_msg = {
                'date': current_date,
                'time': time_str,
                'name': name,
                'content': content if 'content' in locals() else "", # Ensure content exists
                'lines_count': 1,
                'type': 'system' if is_system_msg else 'user'
            }
            if content:
                current_msg_lines = [content]
            else:
                current_msg_lines = []
        else:
            # 3. 這行沒有時間開頭，屬於上一則訊息的換行內容
            if temp_msg:
                current_msg_lines.append(line)
                temp_msg['lines_count'] += 1

    # 加入最後一則
    if temp_msg:
        temp_msg['content'] = '\n'.join(current_msg_lines)
        parsed_msgs.append(temp_msg)
        
    return parsed_msgs

def generate_html(target_file=None):
    full_paths = []
    
    if target_file:
        # 如果有指定檔案，只處理該檔案
        if os.path.exists(target_file):
            full_paths = [target_file]
        else:
            print(f"找不到指定檔案: {target_file}")
            return
    else:
        # 否則搜尋 SOURCE_DIR 下所有 txt 檔案
        files = [f for f in os.listdir(SOURCE_DIR) if f.endswith('.txt')]
        if not files:
            print("未找到任何 .txt 檔案！")
            return
        full_paths = [os.path.join(SOURCE_DIR, f) for f in files]

    for file_path in full_paths:
        filename = os.path.basename(file_path)
        print(f"正在處理: {filename}...")
        
        # 決定輸出檔名 (同目錄，副檔名改為 .html)
        file_dir = os.path.dirname(file_path)
        base_name = os.path.splitext(filename)[0]
        output_path = os.path.join(file_dir, f"{base_name}.html")
        
        try:
            msgs = parse_line_log(file_path)
            # 反轉訊息列表，讓最新的在最上面
            msgs.reverse()
            
            with open(output_path, 'w', encoding='utf-8') as f:
                # 寫入檔頭 (直接寫入檔案，取代記憶體堆疊)
                f.write(HTML_TEMPLATE_START.replace("{max_lines}", str(MAX_LINES)).replace("{max_msgs}", str(MAX_DISPLAY_MSGS)))
                f.write(f'<div class="file-header">檔案：{filename}</div>')
                
                last_date = ""
                valid_msg_count = 0
                
                for msg in msgs:
                    # ================= 過濾區 =================
                    name = msg.get('name', '')
                    content = msg.get('content', '').strip()
                    msg_type = msg.get('type', 'user')

                    # 1. 過濾 AI 與機器人
                    if 'AI小幫手' in name or 'gpt-4o-mini' in name or '麥肯錫AI' in name:
                        continue
                        
                    # 2. 過濾特定系統訊息/圖片/貼圖/記事本
                    system_keywords = [
                        '圖片',
                        '影片',
                        '貼圖',
                        '已新增新的記事本。',
                        '已分享記事本。',
                        'GOD已設定<u>公告</u>',
                        '聯絡資訊',
                        '!切換角色',
                        '!重置角色',
                        '!清空對話',
                        '!56cf61af-bca7-4d4f-a0ab-2ba7844012ab',
                        '!8f279bfe-37c2-4734-bedf-e17f256096ad',
                        '!e9e2b097-2db4-4c97-9dab-52aaaf6fc74b',
                        ]
                    
                    # 精確匹配
                    if content in system_keywords:
                        continue
                    
                    # 模糊匹配 (處理名字被誤判進內容的情況，例如 "Kevin 圖片")
                    is_suffix_system = False
                    for kw in system_keywords:
                        if content.endswith(' ' + kw):
                             is_suffix_system = True
                             break
                    if is_suffix_system:
                        continue

                    if '已收回訊息' in content: 
                        continue

                    # 3. 過濾過長訊息 (直接跳過)
                    if msg['lines_count'] > MAX_LINES:
                        continue
                    # ========================================

                    # 4. 檢查是否達到顯示上限 (避免 HTML 過大導致瀏覽器崩潰)
                    if valid_msg_count >= MAX_DISPLAY_MSGS:
                        f.write(f'<div style="text-align:center; padding: 20px; color: #888; background: #f9f9f9; margin: 20px 0; border-radius: 10px;">--- 已顯示最新的 {MAX_DISPLAY_MSGS} 則訊息 (為了效能其餘已省略) ---</div>')
                        break

                    # 日期分隔線
                    if msg['date'] != last_date:
                        f.write(f'<div class="date-divider"><span>{msg["date"]}</span></div>')
                        last_date = msg['date']
                    
                    display_content = html.escape(content)
                    
                    # 將網址轉換為超連結
                    # 簡單匹配 https:// 或 http:// 開頭，直到遇到空白或結尾
                    url_pattern = re.compile(r'(https?://\S+)')
                    display_content = url_pattern.sub(r'<a href="\1" target="_blank" style="color: #007bff; text-decoration: none;">\1</a>', display_content)

                    # 渲染訊息
                    if msg_type == 'system':
                        # 系統訊息樣式
                         f.write(f"""
                <div class="message" style="justify-content: center;">
                    <div style="background-color: #f0f0f0; color: #888; padding: 5px 15px; border-radius: 15px; font-size: 0.85em;">
                        {display_content} <span style="font-size: 0.8em; margin-left: 5px;">{msg['time']}</span>
                    </div>
                </div>
                """)
                    else:
                        # 一般使用者訊息
                        avatar_text = name[0] if name else "?"
                        avatar_color = get_avatar_color(name)
                        bubble_class = "bubble"
                        
                        f.write(f"""
                <div class="message">
                    <div class="avatar {avatar_color}">{avatar_text}</div>
                    <div class="content-wrapper">
                        <div class="sender-name">{html.escape(name)}</div>
                        <div class="{bubble_class}">{display_content}</div>
                        <div class="time">{msg['time']}</div>
                    </div>
                </div>
                """)
                    
                    valid_msg_count += 1
                
                f.write(HTML_TEMPLATE_END)
            
            print(f"完成！已輸出至: {output_path}")

        except Exception as e:
            print(f"處理失敗 {filename}: {e}")

    print("所有檔案處理完畢。")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # 如果有傳入參數，例如 python line_parser.py chat.txt
        generate_html(sys.argv[1])
    else:
        generate_html()
