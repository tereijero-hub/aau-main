import json
import numpy as np
from datetime import datetime

def generate_visual_data():
    # 公開用に「100本の嵐」を生成するロジック
    n_paths = 100
    n_steps = 100
    initial_equity = 1000000
    
    # モンテカルロ生成（平均0.05%, 分散1.2%のランダムウォーク）
    returns = np.random.normal(0.0005, 0.012, (n_paths, n_steps))
    paths = (initial_equity * (1 + np.cumsum(returns, axis=1))).tolist()

    # ダミーのエージェント報告（見た目重視）
    agent_reports = {
        f"A{i}_Status": {"val": "ACTIVE", "ok": True} for i in range(1, 11)
    }

    output = {
        "metadata": {
            "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "judgment": "🟢 GRANTED",
            "active_agents": 10
        },
        "agent_intelligence": agent_reports,
        "visuals": {
            "monte_carlo_paths": paths,
            "mae_dist": np.random.normal(-0.01, 0.005, 50).tolist(),
            "mfe_dist": np.random.normal(0.02, 0.01, 50).tolist(),
            "latency": [145.2, 58.4, 162.1]
        }
    }

    with open("internal_core_data.json", "w", encoding="utf-8") as f:
        json.dump(output, f, indent=4)
    print("🚀 Data updated for Dashboard")

if __name__ == "__main__":
    generate_visual_data()
