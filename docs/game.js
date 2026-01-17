/**
 * 四子棋遊戲邏輯
 */

// 遊戲配置
const ROWS = 6;
const COLUMNS = 7;
const INAROW = 4;

// 遊戲狀態
let gameState = {
    board: Array(ROWS * COLUMNS).fill(0), // 扁平化棋盤
    currentPlayer: 1, // 1 = 玩家1 (紅色), 2 = 玩家2 (黃色)
    gameMode: 'human', // 'human' 或 'ai'
    gameOver: false,
    winner: null,
    winningCells: []
};

// DOM 元素
let boardElement, statusElement, loadingElement, resultElement, resultTitleElement;

/**
 * 初始化遊戲
 */
function initGame() {
    // 獲取 DOM 元素
    boardElement = document.getElementById('board');
    statusElement = document.getElementById('status');
    loadingElement = document.getElementById('loading');
    resultElement = document.getElementById('result');
    resultTitleElement = document.getElementById('result-title');

    // 綁定事件
    document.getElementById('new-game-btn').addEventListener('click', startNewGame);
    document.getElementById('play-again-btn').addEventListener('click', startNewGame);
    document.getElementById('mode-human').addEventListener('click', () => setGameMode('human'));
    document.getElementById('mode-ai').addEventListener('click', () => setGameMode('ai'));

    // 創建棋盤
    createBoard();
    
    // 開始新遊戲
    startNewGame();
}

/**
 * 創建棋盤 DOM
 */
function createBoard() {
    boardElement.innerHTML = '';
    
    for (let col = 0; col < COLUMNS; col++) {
        const column = document.createElement('div');
        column.className = 'column';
        column.dataset.column = col;
        column.addEventListener('click', () => handleColumnClick(col));
        
        for (let row = 0; row < ROWS; row++) {
            const cell = document.createElement('div');
            cell.className = 'cell empty';
            cell.dataset.row = row;
            cell.dataset.col = col;
            column.appendChild(cell);
        }
        
        boardElement.appendChild(column);
    }
}

/**
 * 開始新遊戲
 */
function startNewGame() {
    gameState = {
        board: Array(ROWS * COLUMNS).fill(0),
        currentPlayer: 1,
        gameMode: gameState.gameMode, // 保持當前模式
        gameOver: false,
        winner: null,
        winningCells: []
    };
    
    updateBoard();
    updateStatus();
    hideResult();
    enableBoard();
}

/**
 * 設置遊戲模式
 */
function setGameMode(mode) {
    if (gameState.gameOver || gameState.board.every(cell => cell === 0)) {
        gameState.gameMode = mode;
        document.getElementById('mode-human').classList.toggle('active', mode === 'human');
        document.getElementById('mode-ai').classList.toggle('active', mode === 'ai');
        startNewGame();
    }
}

/**
 * 處理列點擊
 */
async function handleColumnClick(col) {
    if (gameState.gameOver) return;
    
    // 檢查列是否已滿
    if (!isValidMove(col)) return;
    
    // 落子
    makeMove(col, gameState.currentPlayer);
    
    // 檢查勝利
    const winResult = checkWin();
    if (winResult.winner) {
        gameState.gameOver = true;
        gameState.winner = winResult.winner;
        gameState.winningCells = winResult.cells;
        updateBoard();
        showResult(winResult.winner);
        return;
    }
    
    // 檢查平局
    if (isBoardFull()) {
        gameState.gameOver = true;
        showResult(null);
        return;
    }
    
    // 切換玩家
    gameState.currentPlayer = gameState.currentPlayer === 1 ? 2 : 1;
    updateStatus();
    updateBoard();
    
    // AI 模式：如果是 AI 的回合，獲取 AI 移動
    if (gameState.gameMode === 'ai' && gameState.currentPlayer === 2 && !gameState.gameOver) {
        await makeAIMove();
    }
}

/**
 * 檢查移動是否合法
 */
function isValidMove(col) {
    return gameState.board[col] === 0; // 檢查頂部是否為空
}

/**
 * 執行移動
 */
function makeMove(col, player) {
    // 從底部向上找到第一個空位
    for (let row = ROWS - 1; row >= 0; row--) {
        const index = row * COLUMNS + col;
        if (gameState.board[index] === 0) {
            gameState.board[index] = player;
            return;
        }
    }
}

/**
 * 檢查勝利條件
 */
function checkWin() {
    const board2D = getBoard2D();
    
    // 檢查所有方向
    for (let row = 0; row < ROWS; row++) {
        for (let col = 0; col < COLUMNS; col++) {
            const player = board2D[row][col];
            if (player === 0) continue;
            
            // 檢查水平
            if (col <= COLUMNS - INAROW) {
                const cells = [];
                let count = 0;
                for (let i = 0; i < INAROW; i++) {
                    if (board2D[row][col + i] === player) {
                        count++;
                        cells.push({ row, col: col + i });
                    }
                }
                if (count === INAROW) {
                    return { winner: player, cells };
                }
            }
            
            // 檢查垂直
            if (row <= ROWS - INAROW) {
                const cells = [];
                let count = 0;
                for (let i = 0; i < INAROW; i++) {
                    if (board2D[row + i][col] === player) {
                        count++;
                        cells.push({ row: row + i, col });
                    }
                }
                if (count === INAROW) {
                    return { winner: player, cells };
                }
            }
            
            // 檢查正對角線（左上到右下）
            if (row <= ROWS - INAROW && col <= COLUMNS - INAROW) {
                const cells = [];
                let count = 0;
                for (let i = 0; i < INAROW; i++) {
                    if (board2D[row + i][col + i] === player) {
                        count++;
                        cells.push({ row: row + i, col: col + i });
                    }
                }
                if (count === INAROW) {
                    return { winner: player, cells };
                }
            }
            
            // 檢查負對角線（右上到左下）
            if (row <= ROWS - INAROW && col >= INAROW - 1) {
                const cells = [];
                let count = 0;
                for (let i = 0; i < INAROW; i++) {
                    if (board2D[row + i][col - i] === player) {
                        count++;
                        cells.push({ row: row + i, col: col - i });
                    }
                }
                if (count === INAROW) {
                    return { winner: player, cells };
                }
            }
        }
    }
    
    return { winner: null, cells: [] };
}

/**
 * 檢查棋盤是否已滿
 */
function isBoardFull() {
    return gameState.board.slice(0, COLUMNS).every(cell => cell !== 0);
}

/**
 * 獲取 2D 棋盤表示
 */
function getBoard2D() {
    const board2D = [];
    for (let row = 0; row < ROWS; row++) {
        board2D[row] = [];
        for (let col = 0; col < COLUMNS; col++) {
            const index = row * COLUMNS + col;
            board2D[row][col] = gameState.board[index];
        }
    }
    return board2D;
}

/**
 * AI 移動
 */
async function makeAIMove() {
    if (gameState.gameOver) return;
    
    showLoading();
    disableBoard();
    
    try {
        // 調用 API 獲取 AI 移動
        const aiColumn = await getAIMove(
            [...gameState.board], // 複製棋盤
            gameState.currentPlayer,
            {
                rows: ROWS,
                columns: COLUMNS,
                inarow: INAROW,
                depth: 3
            }
        );
        
        hideLoading();
        enableBoard();
        
        // 執行 AI 移動
        if (isValidMove(aiColumn)) {
            makeMove(aiColumn, gameState.currentPlayer);
            
            // 檢查勝利
            const winResult = checkWin();
            if (winResult.winner) {
                gameState.gameOver = true;
                gameState.winner = winResult.winner;
                gameState.winningCells = winResult.cells;
                updateBoard();
                showResult(winResult.winner);
                return;
            }
            
            // 檢查平局
            if (isBoardFull()) {
                gameState.gameOver = true;
                showResult(null);
                return;
            }
            
            // 切換回玩家
            gameState.currentPlayer = 1;
            updateStatus();
            updateBoard();
        }
    } catch (error) {
        hideLoading();
        enableBoard();
        alert('無法連接到 AI 服務器。請確保後端服務正在運行。\n錯誤：' + error.message);
        console.error('AI move error:', error);
    }
}

/**
 * 更新棋盤顯示
 */
function updateBoard() {
    const cells = boardElement.querySelectorAll('.cell');
    cells.forEach(cell => {
        const row = parseInt(cell.dataset.row);
        const col = parseInt(cell.dataset.col);
        const index = row * COLUMNS + col;
        const player = gameState.board[index];
        
        cell.className = 'cell';
        if (player === 0) {
            cell.className += ' empty';
        } else if (player === 1) {
            cell.className += ' player1';
        } else {
            cell.className += ' player2';
        }
        
        // 標記獲勝的棋子
        if (gameState.winningCells.some(c => c.row === row && c.col === col)) {
            cell.className += ' winning';
        }
    });
    
    // 禁用已滿的列
    const columns = boardElement.querySelectorAll('.column');
    columns.forEach((column, col) => {
        if (!isValidMove(col) || gameState.gameOver) {
            column.classList.add('disabled');
        } else {
            column.classList.remove('disabled');
        }
    });
}

/**
 * 更新狀態顯示
 */
function updateStatus() {
    if (gameState.gameOver) {
        if (gameState.winner) {
            statusElement.textContent = `玩家 ${gameState.winner} 獲勝！`;
        } else {
            statusElement.textContent = '平局！';
        }
    } else {
        if (gameState.gameMode === 'ai' && gameState.currentPlayer === 2) {
            statusElement.textContent = 'AI 思考中...';
        } else {
            const playerName = gameState.currentPlayer === 1 ? '玩家 1（紅色）' : '玩家 2（黃色）';
            statusElement.textContent = `${playerName} 的回合`;
        }
    }
}

/**
 * 顯示/隱藏加載動畫
 */
function showLoading() {
    loadingElement.style.display = 'flex';
    statusElement.style.display = 'none';
}

function hideLoading() {
    loadingElement.style.display = 'none';
    statusElement.style.display = 'block';
}

/**
 * 啟用/禁用棋盤
 */
function enableBoard() {
    boardElement.querySelectorAll('.column').forEach(col => {
        if (isValidMove(parseInt(col.dataset.column)) && !gameState.gameOver) {
            col.classList.remove('disabled');
        }
    });
}

function disableBoard() {
    boardElement.querySelectorAll('.column').forEach(col => {
        col.classList.add('disabled');
    });
}

/**
 * 顯示遊戲結果
 */
function showResult(winner) {
    if (winner === 1) {
        resultTitleElement.textContent = '玩家 1 獲勝！';
    } else if (winner === 2) {
        if (gameState.gameMode === 'ai') {
            resultTitleElement.textContent = 'AI 獲勝！';
        } else {
            resultTitleElement.textContent = '玩家 2 獲勝！';
        }
    } else {
        resultTitleElement.textContent = '平局！';
    }
    resultElement.style.display = 'flex';
}

function hideResult() {
    resultElement.style.display = 'none';
}

// 頁面加載完成後初始化遊戲
document.addEventListener('DOMContentLoaded', initGame);
