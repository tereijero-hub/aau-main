import json
import os
from datetime import datetime

def build_display():
    json_path = "internal_core_data.json"
    
    # デフォルトデータ
    default_data = {
        "metrics": {"var_99": 0.0, "sharpe_ratio": 0.0},
        "revenue": {"total": 0, "tax_automated": 0},
        "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }

    try:
        if os.path.exists(json_path):
            with open(json_path, "r", encoding="utf-8") as f:
                core_data = json.load(f)
        else:
            core_data = default_data
    except:
        core_data = default_data

    m = core_data.get('metrics', default_data['metrics'])
    r = core_data.get('revenue', default_data['revenue'])
    ts = core_data.get('timestamp', default_data['timestamp'])

    # 黄金の帝国デザイン（末尾の閉じクォートを厳密に確認済み）
    html_template = f"""
    <!DOCTYPE html>
    <html lang="ja">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>AAU EMPIRE CONTROL CENTER</title>
        <style>
            :root {{ --gold: #d4af37; --bg: #05070a; --panel: #0a0e14; --text: #e0e0e0; }}
            body {{ background: var(--bg); color: var(--text); font-family: 'Courier New', monospace; margin: 0; padding: 20px; }}
            .border {{ border: 2px solid var(--gold); padding: 20px; box-shadow: 0 0 20px rgba(212, 175, 55, 0.2); }}
            h1 {{ color: var(--gold); text-align: center; border-bottom: 1px solid var(--gold); padding-bottom: 10px; letter-spacing: 5px; }}
            .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; margin-top: 20px; }}
            .panel {{ background: var(--panel); border: 1px solid rgba(212, 175, 55, 0.4); padding: 15px; position: relative; }}
            .label {{ font-size: 12px; color: var(--gold); text-transform: uppercase; margin-bottom: 5px; }}
            .value {{ font-size: 28px; font-weight: bold; color: #fff; }}
            .agent-list {{ display: grid; grid-template-columns: 1fr 1fr; gap: 5px; font-size: 11px; }}
            .agent-item {{ color: #00ff00; border-left: 2px solid #00ff00; padding-left: 5px; }}
            .location {{ font-size: 12px; margin-top: 10px; color: #888; }}
            .status-tag {{ background: #004400; color: #00ff00; padding: 2px 8px; font-size: 10px; border-radius: 3px; }}
            .footer {{ text-align: center; margin-top: 30px; font-size: 10px; color: #444; }}
        </style>
    </head>
    <body>
        <div class="border">
            <h1>🏰 AAU EMPIRE COMMAND</h1>
            <div style="text-align: right;"><span class="status-tag">SYSTEM: ACTIVE</span></div>
            <div class="grid">
                <div class="panel">
                    <div class="label">Total Managed Revenue</div>
                    <div class="val">¥{r.get('total', 0):,}</div>
                    <div class="location">Fintech Sub: 3 Shields Active</div>
                </div>
                <div class="panel">
                    <div class="label">Risk metrics (VaR 99%)</div>
                    <div class="val">{m.get('var_99', 0):.2%}</div>
                    <div class="location">Defense: Synthetic Data Shield</div>
                </div>
                <div class="panel">
                    <div class="label">8-Agent Status</div>
                    <div class="agent-list">
                        <div class="agent-item">Research: ON</div><div class="agent-item">Quants: ON</div>
                        <div class="agent-item">Dev: ON</div><div class="agent-item">Execute: ON</div>
                        <div class="agent-item">Risk: ON</div><div class="agent-item">Critic: ON</div>
                        <div class="agent-item">Optimize: ON</div><div class="agent-item">Tax: ON</div>
                    </div>
                </div>
                <div class="panel">
                    <div class="label">Infrastructure Nodes</div>
                    <div style="font-size: 12px;">
                        📍 ISHIKARI-CHITOSE: <span style="color:#00ff00;">ONLINE</span><br>
                        📍 MATSUMOTO: <span style="color:#00ff00;">ONLINE</span><br>
                        📍 OKAYAMA: <span style="color:#00ff00;">ONLINE</span>
                    </div>
                </div>
            </div>
            <div class="footer">AUTHENTICATED BY EMPIRE CORE | SYNC_TS: {ts}</div>
        </div>
    </body>
    </html>
    """
    
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_template)
    print("✅ 帝国ダッシュボード・最終形態の展開に成功しました。")

if __name__ == "__main__":
    build_display()
