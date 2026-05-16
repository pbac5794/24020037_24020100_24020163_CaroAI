import time

class MinimaxAgent:
    def __init__(self, depth, evaluator):
        self.max_depth = depth
        self.evaluator = evaluator
        self.PLAYER = 1   # X (MIN)
        self.MACHINE = 2  # O (MAX)
        self.node_count = 0

    def get_move(self, board, game_logic):
        start_time = time.time()
        self.node_count = 0
        
        best_score = -float('inf')
        best_move = None
        
        # Chỉ xét các ô trống trong bán kính 2 để đảm bảo bám sát
        moves = board.get_empty_cells(radius=2)
        if not moves: return None, 0

        for r, c in moves:
            board.make_move(r, c, self.MACHINE)
            # Dùng Alpha-Beta đơn giản hoặc Minimax thuần để tìm điểm tốt nhất
            score = self._minimax_rec(board, self.max_depth - 1, False, game_logic)
            board.undo_move(r, c)
            
            if score > best_score:
                best_score = score
                best_move = (r, c)
                
        execution_time = time.time() - start_time
        print(f"[Minimax] Độ sâu: {self.max_depth} | Trạng thái: {self.node_count} "
              f"| Thời gian: {execution_time:.4f}s | Chọn: {best_move}")
              
        return best_move, best_score

    def _minimax_rec(self, board, depth, is_maximizing, game_logic):
        self.node_count += 1
        
        # Kiểm tra thắng thua thực tế
        winner, _ = game_logic.check_winner(board)
        if winner == self.MACHINE:
            return 100000000 + depth 
        elif winner == self.PLAYER:
            return -100000000 - depth 
            
        if board.is_full() or depth == 0:
            # Chỉ tính toán điểm Heuristic tại nút lá
            return self._evaluate_board(board)
            
        moves = board.get_empty_cells(radius=2)
        
        if is_maximizing:
            max_eval = -float('inf')
            for r, c in moves:
                board.make_move(r, c, self.MACHINE)
                eval_score = self._minimax_rec(board, depth - 1, False, game_logic)
                board.undo_move(r, c)
                max_eval = max(max_eval, eval_score)
            return max_eval
        else:
            min_eval = float('inf')
            for r, c in moves:
                board.make_move(r, c, self.PLAYER)
                eval_score = self._minimax_rec(board, depth - 1, True, game_logic)
                board.undo_move(r, c)
                min_eval = min(min_eval, eval_score)
            return min_eval

    def _evaluate_board(self, board):
        """
        Đánh giá điểm số của toàn bộ bàn cờ.
        """
        total_score = 0
        # Chỉ quét những ô có quân cờ để tính điểm
        for r in range(board.size):
            for c in range(board.size):
                if board.grid[r][c] != 0:
                    # evaluate_local sẽ trả về điểm dương cho MACHINE, âm cho PLAYER
                    total_score += self.evaluator.evaluate_local(board.grid, r, c)
        return total_score
