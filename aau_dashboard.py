import json
import os

def build_display():
    json_path = "internal_core_data.json"
    
    if not os.path.exists(json_path):
        print("⚠️ 待機中: 演算データがまだ届いていません。")
        return

    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # データの抽出（心臓部から届いた中身）
    m = data.get('metrics', {})
    r = data.get('revenue', {})
    ts = data.get('timestamp', 'N/A')

    # 黄金の帝国ダッシュボード HTML
    html_content = f"""
    <!DOCTYPE html>
    <html lang="ja">
    <head>
        <meta charset="UTF-8">
        <title>AAU EMPIRE DASHBOARD</title>
        <style>
            body {{ background: #05070a; color: #d4af37; font-family: 'Courier New', monospace; text-align: center; margin: 0; padding: 0; }}
            .container {{ border: 2px solid #d4af37; display: inline-block; padding: 40px; margin-top: 50px; background: #0a0e14; box-shadow: 0 0 30px rgba(212, 175, 55, 0.3); }}
            h1 {{ border-bottom: 1px solid #d4af37; padding-bottom: 10px; }}
            .stat-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 30px; margin-top: 30px; }}
            .stat-card {{ border: 1px solid #d4af37; padding: 20px; background: #111; }}
            .label {{ font-size: 12px; color: #888; margin-bottom: 10px; }}
            .val {{ color: #fff; font-size: 28px; font-weight: bold; }}
            .footer {{ margin-top: 30px; font-size: 11px; color: #555; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🏰 AAU EMPIRE DASHBOARD</h1>
            <p style="color:#00ff00;">SYSTEM STATUS: ONLINE (CONNECTED TO CORE)</p>
            <div class="stat-grid">
                <div class="stat-card"><div class="label">RISK LEVEL (VaR 99%)</div><div class="val">{m.get('var_99', 0):.2%}</div></div>
                <div class="stat-card"><div class="label">TOTAL REVENUE</div><div class="val">¥{r.get('total', 0):,}</div></div>
            </div>
            <div class="footer">Last Core Sync: {ts} | Repository: aau-main</div>
        </div>
    </body>
    </html>
    """
    
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    print("✅ Dashboard: 最新の資産状況をHTMLに反映しました。")

if __name__ == "__main__":
    build_display()
