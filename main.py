def my_agent(obs, config):
    """
    四子棋 AI Agent - 使用 Minimax 演算法與 Alpha-Beta 剪枝
    
    參數:
        obs: 觀察對象，包含當前棋盤狀態 (obs.board) 和玩家標記 (obs.mark)
        config: 配置對象，包含棋盤尺寸 (rows, columns) 和連子數 (inarow)
    
    返回:
        int: AI 選擇的列索引 (0 到 columns-1)
    """
    ################################
    # Imports and helper functions #
    ################################
    import numpy as np
    import random
    
    def check_window(window, num_discs, piece, config):
        """
        檢查一個窗口（連續的格子）是否符合特定條件
        
        參數:
            window: 一個包含 config.inarow 個格子的列表
            num_discs: 需要包含的指定棋子數量
            piece: 要檢查的棋子標記 (1 或 2)
            config: 配置對象
        
        返回:
            bool: 如果窗口中有 num_discs 個指定棋子，且其餘為空位，返回 True
        """
        return (window.count(piece) == num_discs and window.count(0) == config.inarow - num_discs)
    
    def count_windows(grid, num_discs, piece, config):
        """
        統計棋盤上符合條件的窗口數量（用於評估棋形）
        
        參數:
            grid: 2D numpy 數組，表示棋盤狀態
            num_discs: 要統計的棋子數量（2=二連、3=三連、4=四連）
            piece: 要統計的棋子標記 (1 或 2)
            config: 配置對象
        
        返回:
            int: 符合條件的窗口總數（水平、垂直、對角線）
        """
        num_windows = 0
        
        # 水平方向：檢查每一行的所有可能的連續窗口
        for row in range(config.rows):
            for col in range(config.columns - (config.inarow - 1)):
                window = list(grid[row, col:col + config.inarow])
                if check_window(window, num_discs, piece, config):
                    num_windows += 1
        
        # 垂直方向：檢查每一列的所有可能的連續窗口
        for row in range(config.rows - (config.inarow - 1)):
            for col in range(config.columns):
                window = list(grid[row:row + config.inarow, col])
                if check_window(window, num_discs, piece, config):
                    num_windows += 1
        
        # 正對角線（從左上到右下）：檢查所有可能的對角線窗口
        for row in range(config.rows - (config.inarow - 1)):
            for col in range(config.columns - (config.inarow - 1)):
                # 使用 numpy 的高級索引提取對角線元素
                window = list(grid[range(row, row + config.inarow), range(col, col + config.inarow)])
                if check_window(window, num_discs, piece, config):
                    num_windows += 1
        
        # 負對角線（從右上到左下）：檢查所有可能的對角線窗口
        for row in range(config.inarow - 1, config.rows):
            for col in range(config.columns - (config.inarow - 1)):
                # 行索引遞減，列索引遞增
                window = list(grid[range(row, row - config.inarow, -1), range(col, col + config.inarow)])
                if check_window(window, num_discs, piece, config):
                    num_windows += 1
        
        return num_windows
    
    def evaluate_board(grid, mark, config):
        """
        評估棋盤狀態的分數（用於 minimax 演算法的葉節點評估）
        
        這個函數使用啟發式方法來評估當前棋盤對當前玩家（mark）的有利程度。
        分數越高表示對當前玩家越有利。
        
        參數:
            grid: 2D numpy 數組，表示棋盤狀態
            mark: 當前玩家的標記 (1 或 2)
            config: 配置對象
        
        返回:
            int: 評估分數（正數表示對當前玩家有利，負數表示不利）
        """
        # 權重設定：不同棋形的分數權重
        # 這些權重決定了 AI 對不同情況的重視程度
        A_WIN       = 1_000_000  # 四連（勝利）的權重
        B_THREE     = 1_000      # 三連的權重（接近勝利）
        C_TWO       = 10         # 二連的權重（潛在威脅）
        D_TWO_OPP   = -50        # 對手二連的負權重（需要防守）
        E_THREE_OPP = -10_000    # 對手三連的負權重（緊急防守）
        
        # 計算當前玩家的棋形數量
        num_twos      = count_windows(grid, 2, mark, config)  # 二連數量
        num_threes    = count_windows(grid, 3, mark, config)  # 三連數量
        num_fours     = count_windows(grid, 4, mark, config)  # 四連數量（勝利）
        
        # 計算對手的棋形數量
        # 對手標記：如果我是 1，對手是 2；如果我是 2，對手是 1
        opponent = 3 - mark
        num_twos_opp  = count_windows(grid, 2, opponent, config)  # 對手二連
        num_threes_opp= count_windows(grid, 3, opponent, config)  # 對手三連
        num_fours_opp = count_windows(grid, 4, opponent, config)  # 對手四連（失敗）
        
        # 直接勝/敗判定（優先級最高）
        if num_fours_opp > 0:
            # 對手已經四連，當前玩家失敗
            return -A_WIN
        if num_fours > 0:
            # 當前玩家已經四連，勝利
            return A_WIN
        
        # 啟發式評分：綜合考慮各種棋形
        # 公式：自己的優勢 - 對手的威脅
        score = (
            A_WIN      * num_fours +        # 自己的四連（雖然上面已處理，但保留以確保邏輯完整）
            B_THREE    * num_threes +       # 自己的三連（進攻優勢）
            C_TWO      * num_twos +         # 自己的二連（潛在優勢）
            D_TWO_OPP  * num_twos_opp +     # 對手的二連（輕微威脅）
            E_THREE_OPP* num_threes_opp     # 對手的三連（嚴重威脅，需要立即防守）
        )
        return score
    
    def drop_piece(grid, col, mark, config):
        """
        模擬在指定列落子（用於 minimax 演算法的棋盤狀態模擬）
        
        參數:
            grid: 2D numpy 數組，當前棋盤狀態
            col: 要落子的列索引 (0 到 columns-1)
            mark: 落子的玩家標記 (1 或 2)
            config: 配置對象
        
        返回:
            numpy.ndarray: 落子後的新棋盤狀態（複製），如果列已滿則返回 None
        """
        next_grid = grid.copy()  # 複製棋盤，避免修改原始狀態
        # 從底部向上尋找第一個空位（四子棋的規則：棋子會落在該列最下方的空位）
        for row in range(config.rows - 1, -1, -1):
            if next_grid[row][col] == 0:  # 找到空位
                next_grid[row][col] = mark  # 放置棋子
                return next_grid
        return None  # 該列已滿，無法落子
    
    def is_valid_move(grid, col, config):
        """
        檢查指定列是否還有空位可以落子
        
        參數:
            grid: 2D numpy 數組，棋盤狀態
            col: 要檢查的列索引
            config: 配置對象
        
        返回:
            bool: 如果該列頂部（第0行）為空，返回 True；否則返回 False
        """
        # 如果頂部為空，說明該列還有空間
        return grid[0][col] == 0
    
    def get_valid_moves(grid, config):
        """
        取得所有可以落子的列索引
        
        參數:
            grid: 2D numpy 數組，棋盤狀態
            config: 配置對象
        
        返回:
            list: 所有合法列索引的列表
        """
        return [c for c in range(config.columns) if is_valid_move(grid, c, config)]
    
    def minimax(grid, depth, is_maximizing, mark, config, alpha=float('-inf'), beta=float('inf')):
        """
        Minimax 演算法配合 Alpha-Beta 剪枝
        
        這是一個對抗性搜尋演算法，用於在零和遊戲中找到最佳移動。
        - Max 層：模擬當前玩家的回合，選擇分數最高的移動
        - Min 層：模擬對手的回合，選擇分數最低的移動（對當前玩家最不利）
        - Alpha-Beta 剪枝：剪掉不可能影響最終決策的分支，提高搜尋效率
        
        參數:
            grid: 2D numpy 數組，當前棋盤狀態
            depth: 搜尋深度（剩餘層數）
                例如 depth=3 表示：當前玩家走 1 步 → 對手走 1 步 → 當前玩家走 1 步
            is_maximizing: bool，True 表示當前是 Max 層（當前玩家回合），False 表示 Min 層（對手回合）
            mark: 當前玩家的標記 (1 或 2)，用於評估分數
            config: 配置對象
            alpha: Alpha 值（Alpha-Beta 剪枝用），表示當前已知的最佳分數（對 Max 層）
            beta: Beta 值（Alpha-Beta 剪枝用），表示當前已知的最佳分數（對 Min 層）
        
        返回:
            tuple: (分數, 最佳移動列索引)
                分數：從當前玩家角度評估的棋盤分數
                最佳移動：如果是最底層則為 None，否則為最佳列索引
        """
        valid_moves = get_valid_moves(grid, config)
        
        # 終止條件 1：到達搜尋深度或沒有合法移動
        # 此時直接評估當前棋盤狀態，不再繼續搜尋
        if depth == 0 or not valid_moves:
            return evaluate_board(grid, mark, config), None
        
        if is_maximizing:
            # ===== Max 層（當前玩家的回合，尋找最高分數的移動）=====
            max_score = float('-inf')  # 初始化為負無窮，確保任何合法移動都會更新它
            best_move = None
            
            # 嘗試所有合法的移動
            for col in valid_moves:
                next_grid = drop_piece(grid, col, mark, config)
                if next_grid is None:  # 該列已滿，跳過
                    continue
                
                # 終止條件 2：檢查當前玩家是否直接獲勝
                # 如果獲勝，立即返回（不需要繼續搜尋）
                if evaluate_board(next_grid, mark, config) >= 1_000_000:
                    return 1_000_000, col
                
                # 遞迴進入 Min 層（對手的回合）
                # 對手會選擇對當前玩家最不利的移動
                score, _ = minimax(next_grid, depth - 1, False, mark, config, alpha, beta)
                
                # 更新最佳分數和最佳移動
                if score > max_score:
                    max_score = score
                    best_move = col
                
                # Alpha-Beta 剪枝
                # alpha 記錄當前已知的最佳分數（對 Max 層）
                alpha = max(alpha, score)
                # 如果 beta <= alpha，說明對手（Min 層）不會選擇這個分支
                # 因為對手可以選擇一個更好的（對當前玩家更不利的）選項
                if beta <= alpha:
                    break  # 剪枝：不需要繼續搜尋這個分支的其他選項
            
            return max_score, best_move
        
        else:
            # ===== Min 層（對手的回合，尋找最低分數的移動）=====
            min_score = float('inf')  # 初始化為正無窮
            best_move = None
            opponent = 3 - mark  # 計算對手的標記
            
            # 嘗試所有合法的移動（從對手角度）
            for col in valid_moves:
                next_grid = drop_piece(grid, col, opponent, config)
                if next_grid is None:  # 該列已滿，跳過
                    continue
                
                # 終止條件 2：檢查對手是否直接獲勝
                # 如果對手獲勝，對當前玩家來說是最壞情況
                if evaluate_board(next_grid, mark, config) <= -1_000_000:
                    return -1_000_000, col
                
                # 遞迴進入 Max 層（當前玩家的回合）
                score, _ = minimax(next_grid, depth - 1, True, mark, config, alpha, beta)
                
                # 更新最低分數（對當前玩家最不利的情況）
                if score < min_score:
                    min_score = score
                    best_move = col
                
                # Alpha-Beta 剪枝
                # beta 記錄當前已知的最佳分數（對 Min 層，即對當前玩家最不利的分數）
                beta = min(beta, score)
                # 如果 beta <= alpha，說明當前玩家（Max 層）不會選擇這個分支
                # 因為當前玩家可以選擇一個更好的選項
                if beta <= alpha:
                    break  # 剪枝：不需要繼續搜尋這個分支的其他選項
            
            return min_score, best_move
    
    #########################
    # Agent makes selection #
    #########################
    
    # 轉換盤面格式：將一維數組重塑為二維棋盤
    # obs.board 是一維數組，需要轉換為 rows x columns 的二維數組
    grid = np.asarray(obs.board).reshape(config.rows, config.columns)
    
    # 執行 Minimax 演算法（搜尋深度為 3）
    # depth=3 意味著：AI 考慮自己走 1 步 → 對手走 1 步 → 自己再走 1 步
    # is_maximizing=True 表示從當前玩家（AI）的角度開始搜尋
    score, best_move = minimax(grid, depth=3, is_maximizing=True, mark=obs.mark, config=config)
    
    # 安全檢查：如果 minimax 返回 None（理論上不應該發生），使用隨機選擇作為備選
    # 這通常發生在所有列都已滿的情況（遊戲已結束）
    if best_move is None:
        # 從所有合法移動中隨機選擇一個
        # 這裡使用 obs.board 直接檢查（一維數組格式）
        valid_moves = [c for c in range(config.columns) if obs.board[c] == 0]
        if valid_moves:  # 確保有合法移動
            best_move = random.choice(valid_moves)
        else:
            # 如果完全沒有合法移動，返回 0（雖然遊戲應該已經結束）
            best_move = 0
    
    return best_move