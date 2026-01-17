"""
Flask API 服務器 - 提供四子棋 AI 移動接口
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
from agent import get_ai_move

app = Flask(__name__)
# 允許所有來源的跨域請求（生產環境可以限制特定域名）
CORS(app)


@app.route('/api/health', methods=['GET'])
def health_check():
    """健康檢查端點"""
    return jsonify({
        'status': 'ok',
        'message': 'Connect 4 AI API is running'
    })


@app.route('/api/move', methods=['POST'])
def get_move():
    """
    獲取 AI 的下一步移動
    
    請求格式:
    {
        "board": [0,0,1,2,...],  # 扁平化棋盤，0=空，1=玩家1，2=玩家2
        "mark": 1,                # AI 的玩家標記 (1 或 2)
        "rows": 6,                # 可選，默認 6
        "columns": 7,             # 可選，默認 7
        "inarow": 4,              # 可選，默認 4
        "depth": 3                # 可選，默認 3
    }
    
    響應格式:
    {
        "column": 3,              # AI 選擇的列索引 (0-6)
        "status": "success"
    }
    """
    try:
        data = request.get_json()
        
        # 驗證必需參數
        if 'board' not in data:
            return jsonify({'error': 'Missing required parameter: board'}), 400
        if 'mark' not in data:
            return jsonify({'error': 'Missing required parameter: mark'}), 400
        
        board = data['board']
        mark = int(data['mark'])
        
        # 可選參數，設置默認值
        rows = int(data.get('rows', 6))
        columns = int(data.get('columns', 7))
        inarow = int(data.get('inarow', 4))
        depth = int(data.get('depth', 3))
        
        # 驗證參數範圍
        if mark not in [1, 2]:
            return jsonify({'error': 'mark must be 1 or 2'}), 400
        if len(board) != rows * columns:
            return jsonify({'error': f'board length must be {rows * columns}'}), 400
        
        # 調用 AI 獲取移動
        column = get_ai_move(
            board=board,
            mark=mark,
            rows=rows,
            columns=columns,
            inarow=inarow,
            depth=depth
        )
        
        return jsonify({
            'column': column,
            'status': 'success'
        })
    
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500


if __name__ == '__main__':
    # 開發模式運行
    app.run(debug=True, host='0.0.0.0', port=5000)
