/**
 * API 客戶端 - 封裝與後端的通信
 */

// 後端 API 基礎 URL
// 開發環境：http://localhost:5000
// 生產環境：需要替換為實際的後端 URL
const API_BASE_URL = 'http://localhost:5000';

/**
 * 獲取 AI 的下一步移動
 * @param {number[]} board - 扁平化棋盤數組 (0=空, 1=玩家1, 2=玩家2)
 * @param {number} mark - AI 的玩家標記 (1 或 2)
 * @param {Object} options - 可選配置
 * @returns {Promise<number>} AI 選擇的列索引
 */
async function getAIMove(board, mark, options = {}) {
    const {
        rows = 6,
        columns = 7,
        inarow = 4,
        depth = 3
    } = options;

    try {
        const response = await fetch(`${API_BASE_URL}/api/move`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                board,
                mark,
                rows,
                columns,
                inarow,
                depth
            })
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || `HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        
        if (data.status === 'success' && typeof data.column === 'number') {
            return data.column;
        } else {
            throw new Error('Invalid response from server');
        }
    } catch (error) {
        console.error('Error getting AI move:', error);
        throw error;
    }
}

/**
 * 檢查 API 健康狀態
 * @returns {Promise<boolean>} API 是否可用
 */
async function checkAPIHealth() {
    try {
        const response = await fetch(`${API_BASE_URL}/api/health`);
        if (response.ok) {
            const data = await response.json();
            return data.status === 'ok';
        }
        return false;
    } catch (error) {
        console.error('API health check failed:', error);
        return false;
    }
}
