class Evaluator:
    # Hằng số quy định trạng thái ô cờ
    EMPTY = 0
    PLAYER = 1   # MIN (Người chơi đánh X)
    MACHINE = 2  # MAX (Máy đánh O)

    def __init__(self):
        pass

    def evaluate_local(self, board, last_r, last_c):
        """
        Đánh giá điểm số cục bộ tại tọa độ vừa đánh (last_r, last_c)
        sử dụng phương pháp cửa sổ trượt tối ưu (High Performance).
        """
        player = board[last_r][last_c]
        if player == self.EMPTY:
            return 0
            
        opponent = self.MACHINE if player == self.PLAYER else self.PLAYER
        # Điểm số trả về sẽ cộng dương nếu là MACHINE, âm nếu là PLAYER
        sign = 1 if player == self.MACHINE else -1
        
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        total_score = 0
        rows = len(board)
        cols = len(board[0])
        
        for dr, dc in directions:
            # Xét 4 cửa sổ kích thước 4 có chứa quân cờ vừa đánh (vị trí step = 0)
            # Cửa sổ bắt đầu từ start_step: -3, -2, -1, 0
            for start_step in range(-3, 1):
                player_count = 0
                is_blocked = False
                
                # Kiểm tra 4 ô trong cửa sổ hiện tại
                for step in range(start_step, start_step + 4):
                    r = last_r + step * dr
                    c = last_c + step * dc
                    
                    # Nếu ra ngoài biên hoặc gặp quân đối thủ -> Cửa sổ này vô dụng
                    if r < 0 or r >= rows or c < 0 or c >= cols:
                        is_blocked = True
                        break
                        
                    cell = board[r][c]
                    if cell == opponent:
                        is_blocked = True
                        break
                    elif cell == player:
                        player_count += 1
                        # Thưởng điểm cho các quân cờ nằm liên tiếp nhau (Tăng mạnh)
                        total_score += 100 * sign 
                
                # Chỉ cộng điểm nếu cửa sổ có khả năng thắng (không bị chặn)
                if not is_blocked:
                    if player_count == 4:
                        total_score += 100000000 * sign 
                    elif player_count == 3:
                        total_score += 200000 * sign   # 200 Ngàn
                    elif player_count == 2:
                        total_score += 20000 * sign    # 20 Ngàn
                    
        # Thưởng điểm áp sát (Proximity bonus)
        # Nếu nước đi nằm ngay sát (radius 1) một quân cờ bất kỳ, cộng thêm điểm
        # Điều này giúp AI đánh bám sát hơn thay vì nhảy ra xa
        for dr in range(-1, 2):
            for dc in range(-1, 2):
                if dr == 0 and dc == 0: continue
                nr, nc = last_r + dr, last_c + dc
                if 0 <= nr < rows and 0 <= nc < cols:
                    if board[nr][nc] != self.EMPTY:
                        total_score += 100 * sign
                        
        return total_score
