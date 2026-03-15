import json
import os

def build_display():
    json_path = "internal_core_data.json"
    
    # データの読み込み
    if not os.path.exists(json_path):
        print("⚠️ 待機中: 演算データ(JSON)がまだ着弾していません。")
        # データがない場合の仮画面
        content_html = "<h1>📡 帝国データ同期待機中...</h1>"
    else:
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        # 司令官の演算結果から抽出
        metrics = data.get('metrics', {})
        revenue = data.get('revenue', {})
        ts = data.get('timestamp', 'N/A')
        
        # 黄金のダッシュボード HTML構成
        content_html = f"""
            <h1>🏰 AAU EMPIRE DASHBOARD</h1>
            <p style="color:#00ff00;">SYSTEM STATUS: ACTIVE (LOGISTICS OPEN)</p>
            <div class="stat-grid">
                <div class="stat-card">
                    <div class="label">RISK LEVEL (VaR 99%)</div>
                    <div class="val">{metrics.get('var_99', 0):.2%}</div>
                </div>
                <div class="stat-card">
                    <div class="label">TOTAL REVENUE</div>
                    <div class="val">¥{revenue.get('total', 0):,}</div>
                </div>
            </div>
            <div class="footer">Last Core Sync: {ts}</div>
        """

    # HTMLファイルの書き出し
    full_html = f"""
    <!DOCTYPE html>
    <html lang="ja">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>AAU EMPIRE DASHBOARD</title>
        <style>
            body {{ background: #05070a; color: #d4af37; font-family: 'Courier New', monospace; text-align: center; margin: 0; padding: 0; }}
            .container {{ border: 2px solid #d4af37; display: inline-block; padding: 40px; margin-top: 50px; background: #0a0e14; box-shadow: 0 0 30px rgba(212, 175, 55, 0.3); min-width: 350px; }}
            h1 {{ border-bottom: 1px solid #d4af37; padding-bottom: 10px; margin-bottom: 20px; }}
            .stat-grid {{ display: grid; grid-template-columns: 1fr; gap: 20px; margin-top: 20px; }}
            .stat-card {{ border: 1px solid #d4af37; padding: 20px; background: #111; }}
            .label {{ font-size: 12px; color: #888; margin-bottom: 10px; text-transform: uppercase; }}
            .val {{ color: #fff; font-size: 32px; font-weight: bold; }}
            .footer {{ margin-top: 30px; font-size: 11px; color: #555; }}
        </style>
    </head>
    <body>
        <div class="container">
            {content_html}
        </div>
    </body>
    </html>
    """
    
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(full_html)
    print("✅ index.html の生成が完了しました。")

if __name__ == "__main__":
    build_display()
