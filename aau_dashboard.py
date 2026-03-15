import json
import os
from datetime import datetime

def build_display():
    json_path = "internal_core_data.json"
    
    # --- 1. データ抽出プロトコル ---
    # デフォルト値の設定（データが欠損していても表示を維持する）
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

    # 脳(-)から届いたリアルな数字を抽出
    m = core_data.get('metrics', default_data['metrics'])
    r = core_data.get('revenue', default_data['revenue'])
    ts = core_data.get('timestamp', default_data['timestamp'])

    # --- 2. 帝国デザイン構築 ---
    html_template = f"""
    <!DOCTYPE html>
    <html lang="ja">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>AAU EMPIRE CONTROL CENTER</title>
        <style>
            :root {{
                --gold: #d4af37;
                --bg: #05070a;
                --panel: #0a1018;
                --text: #e0e0e0;
                --active: #00ff00;
                --dim-gold: rgba(212, 175, 55, 0.4);
            }}
            body {{
                background: var(--bg);
                color: var(--text);
                font-family: 'Courier New', monospace;
                margin: 0;
                padding: 20px;
                display: flex;
                justify-content: center;
            }}
            .empire-frame {{
                border: 2px solid var(--gold);
                max-width: 1000px;
                width: 100%;
                padding: 30px;
                background: linear-gradient(145deg, #05070a 0%, #0a0e14 100%);
                box-shadow: 0 0 50px rgba(212, 175, 55, 0.15);
                position: relative;
            }}
            .header {{
                text-align: center;
                border-bottom: 3px double var(--gold);
                margin-bottom: 30px;
                padding-bottom: 15px;
            }}
            .header h1 {{
                margin: 0;
                font-size: 2.2em;
                letter-spacing: 8px;
                color: var(--gold);
                text-shadow: 0 0 10px var(--gold);
            }}
            .system-status {{
                position: absolute;
                top: 10px;
                right: 20px;
                font-size: 10px;
                color: var(--active);
                animation: blink 2s infinite;
            }}
            @keyframes blink {{ 0% {{ opacity: 1; }} 50% {{ opacity: 0.3; }} 100% {{ opacity: 1; }} }}
            
            .grid {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
                gap: 20px;
            }}
            .panel {{
                background: var(--panel);
                border: 1px solid var(--dim-gold);
                padding: 20px;
                position: relative;
                overflow: hidden;
            }}
            .panel::before {{
                content: "AAU-SECURED";
                position: absolute;
                top: -5px;
                right: -5px;
                font-size: 8px;
                background: var(--gold);
                color: #000;
                padding: 2px 10px;
                transform: rotate(45deg);
            }}
            .label {{
                font-size: 11px;
                color: var(--gold);
                text-transform: uppercase;
                border-left: 3px solid var(--gold);
                padding-left: 10px;
                margin-bottom: 15px;
            }}
            .value {{
                font-size: 32px;
                font-weight: bold;
                color: #ffffff;
                text-shadow: 0 0 5px rgba(255,255,255,0.2);
            }}
            
            /* 8エージェントリスト */
            .agent-grid {{
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 8px;
                font-size: 12px;
            }}
            .agent-item {{
                color: var(--active);
                background: rgba(0, 255, 0, 0.05);
                padding: 4px;
                border: 1px solid rgba(0, 255, 0, 0.2);
            }}

            /* 物理拠点ステータス */
            .node-status {{
                margin-top: 10px;
                font-size: 12px;
            }}
            .node-item {{
                margin-bottom: 5px;
                display: flex;
                justify-content: space-between;
            }}
            .online {{ color: var(--active); font-weight: bold; }}

            .footer {{
                margin-top: 40px;
                text-align: center;
                font-size: 10px;
                color: #555;
                border-top: 1px solid #222;
                padding-top: 10px;
            }}
        </style>
    </head>
    <body>
        <div class="empire-frame">
            <div class="system-status">● AAU-PRIMARY-01 STATUS: ACTIVE</div>
            <div class="header">
                <h1>AAU EMPIRE CONTROL</h1>
                <div style="font-size: 10px; color: var(--gold); margin-top: 5px;">ASSET MANAGEMENT & FINTECH INTELLIGENCE</div>
            </div>

            <div class="grid">
                <div class="panel">
                    <div class="label">Empire Total Revenue</div>
                    <div class="value">¥{r.get('total', 0):,}</div>
                    <div style="font-size: 10px; margin-top: 10px; color: #888;">
                        Fintech Sub: 3 Shields & Tax-Auto Mode
                    </div>
                </div>

                <div class="panel">
                    <div class="label">Risk Analysis (VaR 99%)</div>
                    <div class="value">{m.get('var_99', 0):.4%}</div>
                    <div style="font-size: 10px; margin-top: 10px; color: #888;">
                        Security: Backtest Lab Synthetic Data
                    </div>
                </div>

                <div class="panel" style="grid-row: span 2;">
                    <div class="label">8-Agent Deployment</div>
                    <div class="agent-grid">
                        <div class="agent-item">▣ RESEARCH</div>
                        <div class="agent-item">▣ QUANTS</div>
                        <div class="agent-item">▣ DEV-AGNT</div>
                        <div class="agent-item">▣ EXECUTE</div>
                        <div class="agent-item">▣ RISK-MGR</div>
                        <div class="agent-item">▣ CRITIC</div>
                        <div class="agent-item">▣ CODE-OPT</div>
                        <div class="agent-item">▣ TAX-AGNT</div>
                    </div>
                    <div style="font-size: 9px; margin-top: 15px; color: var(--gold);">
                        *All Agents synchronized with Core IP
                    </div>
                </div>

                <div class="panel">
                    <div class="label">Infras Node Status</div>
                    <div class="node-status">
                        <div class="node-item"><span>ISHIKARI-CHITOSE</span><span class="online">ONLINE</span></div>
                        <div class="node-item"><span>NAGANO-MATSUMOTO</span><span class="online">ONLINE</span></div>
                        <div class="node-item"><span>OKAYAMA-CENTRAL</span><span class="online">ONLINE</span></div>
                    </div>
                </div>
            </div>

            <div class="footer">
                COMMANDER AUTHENTICATED | SYNC_TIMESTAMP: {ts} | © 2026 AAU EMPIRE
            </div>
        </div>
    </body>
    </html>
    """
    
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_template)
    print("✅ 帝国ダッシュボード・最終統合完了。")

if __name__ == "__main__":
    build_display()
