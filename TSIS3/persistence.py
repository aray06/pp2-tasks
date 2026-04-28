import json
import os

def load_data(filename, default):
    if not os.path.exists(filename):
        with open(filename, 'w') as f:
            json.dump(default, f)
        return default
    with open(filename, 'r') as f:
        return json.load(f)

def save_data(filename, data):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

def update_leaderboard(name, score):
    lb = load_data('leaderboard.json', [])
    lb.append({"name": name, "score": int(score)})
    lb = sorted(lb, key=lambda x: x['score'], reverse=True)[:10]
    save_data('leaderboard.json', lb)