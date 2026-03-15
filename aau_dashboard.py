import json
import os

def build_display():
    json_path = "internal_core_data.json"
    
    # データの読み込み（失敗しても止まらないように保護）
    try:
        if os.path.exists(json_path):
            with open(json_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                revenue = data.get('revenue', {}).get('total', '0')
                var = data.get('metrics', {}).get('var_99', '0')
        else:
            revenue, var = "待機中", "待機中"
    except:
        revenue, var = "エラー", "エラー"

    # 極限までシンプルにしたHTML（真っ白回避用）
    html_template = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            body {{ background-color: #000; color: #d4af37; font-family: sans-serif; text-align: center; padding: 50px; }}
            .box {{ border: 2px solid #d4af37; padding: 20px; display: inline-block; }}
            h1 {{ color: #fff; }}
            .val {{ font-size: 2em; font-weight: bold; color: #00ff00; }}
        </style>
    </head>
    <body>
        <div class="box">
            <h1>🏰 AAU EMPIRE DASHBOARD</h1>
            <p>STATUS: ACTIVE</p>
            <hr>
            <p>TOTAL REVENUE</p>
            <div class="val">¥{revenue}</div>
            <p>RISK LEVEL (VaR 99%)</p>
            <div class="val">{var}</div>
        </div>
    </body>
    </html>
    """
    
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_template)
    print("✅ index.html re-generated.")

if __name__ == "__main__":
    build_display()
