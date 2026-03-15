import json
import os

def build_display():
    json_path = "internal_core_data.json"
    
    # デフォルト値（データがない場合）
    metrics = {"var_99": 0.0}
    revenue = {"total": 0}
    ts = "データ同期待機中..."
    status_color = "#ff0000" # 赤（待機）
    status_text = "WAITING FOR CORE DATA..."

    # データの読み込みに挑戦
    if os.path.exists(json_path):
        try:
            with open(json_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                # 脳（-）からのデータを抽出
                metrics = data.get('metrics', metrics)
                revenue = data.get('revenue', revenue)
                ts = data.get('timestamp', ts)
                status_color = "#00ff00" # 緑（稼働）
                status_text = "AAU-PRIMARY-01 Status: ACTIVE"
        except Exception as e:
            status_text = f"DATA ERROR: {str(e)}"

    # 黄金のダッシュボード HTML
    full_html = f"""
    <!DOCTYPE html>
    <html lang="ja">
    <head>
        <meta charset="UTF-8">
        <title>AAU EMPIRE DASHBOARD</title>
        <style>
            body {{ background: #05070a; color: #d4af37; font-family: 'Courier New', monospace; text-align: center; padding-top: 50px; }}
            .container {{ border: 2px solid #d4af37; display: inline-block; padding: 40px; background: #0a0e14; box-shadow: 0 0 30px rgba(212, 175, 55, 0.3); min-width: 400px; }}
            .status {{ color: {status_color}; font-weight: bold; margin-bottom: 20px; font-size: 1.2em; }}
            .stat-box {{ border: 1px solid #d4af37; margin: 15px 0; padding: 20px; background: #111; }}
            .label {{ color: #888; font-size: 0.8em; text-transform: uppercase; }}
            .value {{ color: #fff; font-size: 2.5em; font-weight: bold; display: block; }}
            .footer {{ margin-top: 30px; font-size: 0.7em; color: #444; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🏰 AAU EMPIRE</h1>
            <div class="status">{status_text}</div>
            
            <div class="stat-box">
                <span class="label">Total Revenue</span>
                <span class="value">¥{revenue.get('total', 0):,}</span>
            </div>

            <div class="stat-box">
                <span class="label">Risk Level (VaR 99%)</span>
                <span class="value">{metrics.get('var_99', 0):.2%}</span>
            </div>

            <div class="footer">LAST UPDATE: {ts}</div>
        </div>
    </body>
    </html>
    """
    
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(full_html)

if __name__ == "__main__":
    build_display()
