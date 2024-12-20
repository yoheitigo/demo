from flask import Flask, request, jsonify
import threading

app = Flask(__name__)

def process_heavy_task(data):
    import time
    print("重い処理を開始")
    time.sleep(10)  # 10秒かかる重い処理
    print("重い処理が完了")

@app.route('/slack/events', methods=['POST'])
def slack_events():
    data = request.json
    
    # 1. すぐに200 OKを返す
    response = jsonify({'status': 'ok'})
    
    # 2. 重い処理はバックグラウンドスレッドで実行
    threading.Thread(target=process_heavy_task, args=(data,)).start()
    return response, 200

if __name__ == "__main__":
    app.run(port=3000)
