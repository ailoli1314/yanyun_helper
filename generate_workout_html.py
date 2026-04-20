# -*- coding: utf-8 -*-
"""
健身计划HTML生成器
根据当天是周几，自动读取 workout_config.json 并生成当日训练计划 HTML
"""

import json
import os
from datetime import datetime

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "workout_config.json")
OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "workout_today.html")

# 部位emoji映射
PART_EMOJI = {
    "胸": "💪",
    "胸大肌": "💪🫁",
    "胸肌": "💪",
    "胸肌上部": "💪⬆️",
    "三角肌": "🦴",
    "三角肌中束": "🤷",
    "三角肌后束": "🤦",
    "三角肌前束": "🦴",
    "肱三头肌": "🦾",
    "肱二头肌": "💪🦾",
    "背阔肌": "⬇️",
    "斜方肌": "🦴",
    "菱形肌": "🦴",
    "腹肌": "🔥",
    "股四头肌": "🦵",
    "臀大肌": "🍑",
    "腘绳肌": "🦵",
    "小腿三头肌": "🦶",
}

def get_day_key():
    """获取今天是周几，返回对应的 day key"""
    weekday = datetime.now().isoweekday()  # 1=Monday, 7=Sunday
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        config = json.load(f)
    
    # 适配配置中的weekdays映射
    # config里 0=rest, 1=day1... 所以直接用 weekday % 7
    day_map = {0: "rest", 1: "day1", 2: "day2", 3: "day3", 4: "rest", 5: "day1", 6: "day2", 7: "day3"}
    
    # 也支持自定义weekdays配置
    if "weekdays" in config:
        weekday_index = datetime.now().weekday()  # 0=Monday
        return config["weekdays"].get(str(weekday_index), "rest")
    
    return day_map.get(weekday, "rest")


def get_part_emoji(primary):
    """根据主要部位获取emoji"""
    for key, emoji in PART_EMOJI.items():
        if key in primary:
            return emoji
    return "💪"


def generate_html(config, day_key):
    """生成HTML内容"""
    day_data = config["days"].get(day_key, config["days"]["rest"])
    day_name = day_data["name"]
    day_emoji = day_data.get("emoji", "🏋️")
    day_desc = day_data.get("description", "")
    exercises = day_data.get("exercises", [])
    
    today_date = datetime.now().strftime("%Y年%m月%d日")
    weekday_name = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"][datetime.now().weekday()]
    
    # 生成动作卡片
    exercise_cards = ""
    for ex in exercises:
        part_emoji = get_part_emoji(ex["primary"])
        
        # 生成步骤HTML
        steps_html = ""
        for i, step in enumerate(ex["steps"], 1):
            steps_html += f'<div class="step"><span class="step-num">{i}</span><span>{step}</span></div>\n'
        
        # 生成注意事项HTML
        tips_html = ""
        for tip in ex["tips"]:
            tips_html += f'<div class="tip">⚠️ {tip}</div>\n'
        
        # 主要+次要部位
        parts_html = f'<div class="part-badge">{part_emoji} {ex["primary"]}</div>'
        if ex.get("secondary"):
            parts_html += f'<div class="part-badge secondary">{ex["secondary"]}</div>'
        
        # 组数次数标签
        sets_label = f'<div class="sets-label">📊 {ex["sets_reps"]} | 休息{ex.get("rest","60")}秒</div>'
        
        # 家用替代
        home_alt = f'<div class="home-alt">🏠 家用替代：{ex["home_alternative"]}</div>'
        
        card = f"""
        <div class="exercise-card">
            <div class="card-header">
                <div class="card-title-row">
                    <span class="card-emoji">{part_emoji}</span>
                    <h3 class="card-title">{ex["name"]}</h3>
                </div>
                <div class="card-en">{ex.get("name_en","")}</div>
                {sets_label}
            </div>
            <div class="card-body">
                <div class="parts-row">
                    {parts_html}
                </div>
                <div class="section-title">📋 动作步骤</div>
                <div class="steps">{steps_html}</div>
                <div class="section-title">⚡ 注意事项</div>
                <div class="tips">{tips_html}</div>
                {home_alt}
            </div>
        </div>
        """
        exercise_cards += card
    
    # 如果是休息日
    rest_content = ""
    if day_key == "rest" or not exercises:
        exercise_cards = f"""
        <div class="rest-day">
            <div class="rest-emoji">😴🛌💤</div>
            <h2>今日休息</h2>
            <p>好好休息，让肌肉恢复！</p>
            <p>可以做轻度的拉伸或散步</p>
            <div class="tip" style="text-align:center;max-width:400px;margin:20px auto">
                💡 休息也是训练的一部分，肌肉在休息时生长
            </div>
        </div>
        """
    
    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>{day_name} - 健身计划</title>
    <style>
        :root {{
            --bg: #f5f6fa;
            --card-bg: #ffffff;
            --text: #2d3436;
            --text-secondary: #636e72;
            --accent: #0984e3;
            --accent-light: #dfe6e9;
            --success: #00b894;
            --warning: #fdcb6e;
            --shadow: 0 2px 12px rgba(0,0,0,0.08);
            --radius: 16px;
        }}
        
        [data-theme="dark"] {{
            --bg: #1a1a2e;
            --card-bg: #16213e;
            --text: #eaeaea;
            --text-secondary: #a0a0a0;
            --accent: #4cc9f0;
            --accent-light: #2a3f5f;
            --shadow: 0 2px 12px rgba(0,0,0,0.4);
        }}
        
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            -webkit-tap-highlight-color: transparent;
        }}
        
        body {{
            font-family: -apple-system, "PingFang SC", "Microsoft YaHei", sans-serif;
            background: var(--bg);
            color: var(--text);
            padding: 16px;
            padding-bottom: 80px;
            transition: background 0.3s, color 0.3s;
            min-height: 100vh;
        }}
        
        .theme-toggle {{
            position: fixed;
            top: 16px;
            right: 16px;
            z-index: 999;
            background: var(--card-bg);
            border: none;
            border-radius: 50%;
            width: 44px;
            height: 44px;
            font-size: 20px;
            cursor: pointer;
            box-shadow: var(--shadow);
            display: flex;
            align-items: center;
            justify-content: center;
        }}
        
        .header {{
            text-align: center;
            margin: 30px 0 20px;
        }}
        
        .date-info {{
            font-size: 14px;
            color: var(--text-secondary);
            margin-bottom: 6px;
        }}
        
        .day-title {{
            font-size: 26px;
            font-weight: 700;
            color: var(--accent);
            margin-bottom: 6px;
        }}
        
        .day-desc {{
            font-size: 15px;
            color: var(--text-secondary);
            margin-bottom: 4px;
        }}
        
        .day-summary {{
            background: var(--card-bg);
            border-radius: var(--radius);
            padding: 14px 18px;
            margin: 14px 0;
            box-shadow: var(--shadow);
            display: flex;
            justify-content: space-around;
            text-align: center;
        }}
        
        .summary-item {{
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 4px;
        }}
        
        .summary-num {{
            font-size: 24px;
            font-weight: 700;
            color: var(--accent);
        }}
        
        .summary-label {{
            font-size: 12px;
            color: var(--text-secondary);
        }}
        
        .divider {{
            text-align: center;
            color: var(--text-secondary);
            font-size: 13px;
            margin: 24px 0 16px;
            display: flex;
            align-items: center;
            gap: 12px;
        }}
        
        .divider::before, .divider::after {{
            content: '';
            flex: 1;
            height: 1px;
            background: var(--accent-light);
        }}
        
        .exercise-card {{
            background: var(--card-bg);
            border-radius: var(--radius);
            margin-bottom: 16px;
            box-shadow: var(--shadow);
            overflow: hidden;
            transition: transform 0.2s;
        }}
        
        .exercise-card:active {{
            transform: scale(0.98);
        }}
        
        .card-header {{
            padding: 16px 18px 12px;
            border-bottom: 1px solid var(--accent-light);
        }}
        
        .card-title-row {{
            display: flex;
            align-items: center;
            gap: 10px;
            margin-bottom: 4px;
        }}
        
        .card-emoji {{
            font-size: 28px;
        }}
        
        .card-title {{
            font-size: 18px;
            font-weight: 700;
        }}
        
        .card-en {{
            font-size: 12px;
            color: var(--text-secondary);
            margin-left: 38px;
            font-style: italic;
        }}
        
        .sets-label {{
            display: inline-block;
            background: var(--accent-light);
            color: var(--accent);
            font-size: 13px;
            font-weight: 600;
            padding: 4px 12px;
            border-radius: 20px;
            margin-top: 8px;
        }}
        
        .card-body {{
            padding: 14px 18px 16px;
        }}
        
        .parts-row {{
            display: flex;
            flex-wrap: wrap;
            gap: 6px;
            margin-bottom: 14px;
        }}
        
        .part-badge {{
            background: linear-gradient(135deg, #ff6b6b, #ee5a5a);
            color: white;
            font-size: 12px;
            font-weight: 600;
            padding: 4px 10px;
            border-radius: 12px;
        }}
        
        .part-badge.secondary {{
            background: linear-gradient(135deg, #74b9ff, #0984e3);
        }}
        
        .section-title {{
            font-size: 13px;
            font-weight: 700;
            color: var(--accent);
            margin-bottom: 8px;
            margin-top: 12px;
        }}
        
        .steps {{
            display: flex;
            flex-direction: column;
            gap: 8px;
        }}
        
        .step {{
            display: flex;
            align-items: flex-start;
            gap: 10px;
            font-size: 14px;
            line-height: 1.5;
        }}
        
        .step-num {{
            background: var(--accent-light);
            color: var(--accent);
            font-size: 11px;
            font-weight: 700;
            width: 20px;
            height: 20px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            flex-shrink: 0;
            margin-top: 2px;
        }}
        
        .tips {{
            display: flex;
            flex-direction: column;
            gap: 6px;
        }}
        
        .tip {{
            background: var(--accent-light);
            color: var(--text);
            font-size: 13px;
            padding: 8px 12px;
            border-radius: 10px;
            line-height: 1.5;
            border-left: 3px solid var(--warning);
        }}
        
        .home-alt {{
            background: #e8f5e9;
            color: #2e7d32;
            font-size: 13px;
            padding: 10px 14px;
            border-radius: 10px;
            margin-top: 14px;
            line-height: 1.5;
        }}
        
        [data-theme="dark"] .home-alt {{
            background: #1b3a2a;
            color: #81c784;
        }}
        
        .rest-day {{
            text-align: center;
            padding: 60px 20px;
            color: var(--text-secondary);
        }}
        
        .rest-emoji {{
            font-size: 64px;
            margin-bottom: 20px;
        }}
        
        .rest-day h2 {{
            font-size: 28px;
            color: var(--text);
            margin-bottom: 12px;
        }}
        
        .rest-day p {{
            font-size: 16px;
            line-height: 1.8;
        }}
        
        .footer {{
            text-align: center;
            margin-top: 40px;
            padding: 20px;
            color: var(--text-secondary);
            font-size: 12px;
            border-top: 1px solid var(--accent-light);
        }}
        
        /* 进度条 */
        .progress-bar {{
            position: fixed;
            bottom: 0;
            left: 0;
            right: 0;
            background: var(--card-bg);
            padding: 12px 20px 16px;
            box-shadow: 0 -2px 12px rgba(0,0,0,0.1);
            z-index: 100;
        }}
        
        .progress-label {{
            font-size: 12px;
            color: var(--text-secondary);
            margin-bottom: 6px;
        }}
        
        .progress-track {{
            background: var(--accent-light);
            border-radius: 6px;
            height: 6px;
            overflow: hidden;
        }}
        
        .progress-fill {{
            background: linear-gradient(90deg, var(--accent), var(--success));
            height: 100%;
            border-radius: 6px;
            transition: width 0.5s;
        }}
        
        /* 深色主题适配 */
        [data-theme="dark"] .sets-label {{
            background: var(--accent-light);
        }}
        
        [data-theme="dark"] .step-num {{
            background: var(--accent-light);
        }}
        
        [data-theme="dark"] .tip {{
            background: #2a2a3a;
            border-left-color: #f39c12;
        }}
        
        [data-theme="dark"] .progress-track {{
            background: #2a2a3a;
        }}
    </style>
</head>
<body>
    <button class="theme-toggle" onclick="toggleTheme()" id="themeBtn">☀️</button>
    
    <div class="header">
        <div class="date-info">{today_date} {weekday_name}</div>
        <div class="day-title">{day_emoji} {day_name}</div>
        <div class="day-desc">{day_desc}</div>
    </div>
    
    <div class="day-summary">
        <div class="summary-item">
            <span class="summary-num">{len(exercises)}</span>
            <span class="summary-label">训练动作</span>
        </div>
        <div class="summary-item">
            <span class="summary-num">{sum(int(ex.get('sets_reps','').split('×')[0].strip()) for ex in exercises if '×' in ex.get('sets_reps',''))}</span>
            <span class="summary-label">总组数</span>
        </div>
        <div class="summary-item">
            <span class="summary-num">{len(exercises) * 4 if exercises else 0}</span>
            <span class="summary-label">预计分钟</span>
        </div>
    </div>
    
    <div class="divider">💪 训练动作 💪</div>
    
    {exercise_cards}
    
    <div class="footer">
        <p>💡 编辑 <code>workout_config.json</code> 即可修改训练计划</p>
        <p style="margin-top:6px">由 OpenClaw 自动生成 · {today_date}</p>
    </div>
    
    <div class="progress-bar">
        <div class="progress-label">今日训练完成进度</div>
        <div class="progress-track">
            <div class="progress-fill" id="progressFill" style="width: 0%"></div>
        </div>
    </div>
    
    <script>
        // 深色/浅色主题切换
        function toggleTheme() {{
            const body = document.body;
            const btn = document.getElementById('themeBtn');
            if (body.getAttribute('data-theme') === 'dark') {{
                body.removeAttribute('data-theme');
                btn.textContent = '☀️';
                localStorage.setItem('theme', 'light');
            }} else {{
                body.setAttribute('data-theme', 'dark');
                btn.textContent = '🌙';
                localStorage.setItem('theme', 'dark');
            }}
        }}
        
        // 读取保存的主题
        if (localStorage.getItem('theme') === 'dark') {{
            document.body.setAttribute('data-theme', 'dark');
            document.getElementById('themeBtn').textContent = '🌙';
        }}
        
        // 进度跟踪
        let completed = 0;
        const total = {len(exercises)};
        
        function markDone() {{
            if (completed < total) {{
                completed++;
                updateProgress();
            }}
        }}
        
        function updateProgress() {{
            const pct = total > 0 ? Math.round((completed / total) * 100) : 0;
            document.getElementById('progressFill').style.width = pct + '%';
        }}
        
        // 点击卡片标记完成
        document.querySelectorAll('.exercise-card').forEach(card => {{
            card.addEventListener('click', function(e) {{
                if (e.target.closest('.home-alt') || e.target.closest('button')) return;
                this.style.opacity = this.style.opacity === '0.5' ? '1' : '0.5';
                markDone();
            }});
        }});
    </script>
</body>
</html>
"""
    return html


def main():
    """主函数：读取配置并生成HTML"""
    # 读取配置
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        config = json.load(f)
    
    # 获取今天是周几，对应什么训练日
    day_key = get_day_key()
    
    # 生成HTML
    html_content = generate_html(config, day_key)
    
    # 写入文件
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write(html_content)
    
    print(f"✅ 健身计划已生成: {OUTPUT_PATH}")
    print(f"📅 今天是: {config['days'][day_key]['name']}")
    print(f"🏋️ 共 {len(config['days'][day_key]['exercises'])} 个动作")
    print(f"📝 主题: {day_key}")
    
    return day_key, config['days'][day_key]


if __name__ == "__main__":
    main()
