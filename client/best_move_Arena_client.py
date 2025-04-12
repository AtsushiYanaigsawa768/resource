from .not_websocket_client import Client
import random
import time

class GameTrackingClient(Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # ゲーム全体で各ターンにドローしたカード（自分および他のプレイヤー）の記録を保持するリスト
        self.game_drawn_cards = []  # 各ターンの記録を累積
        self.remained_cards = []  # 残りのカードを保持するリスト
        # カードのデッキを初期化：数値×枚数の形式でリストに追加
        for value, count in [
            (1, 4), (2, 4), (3, 4), (4, 4), (5, 4),
            (10, 3), (15, 2), (20, 1),
            (0, 3), (-5, 2), (-10, 1)
        ]:
            self.remained_cards.extend([value] * count)

    def AI_player_action(self,others_info, current_sum, log, actions):
        # カスタムロジックを実装
        print(f"[SampleClient] AI deciding action based on sum: {current_sum}, log: {log}, actions: {actions},others_info: {others_info}")
        # 例: ランダムにアクションを選択
        # Extract card_info from others_info
        drawn_cards = [player['card_info'] for player in others_info]
        self.game_drawn_cards.append(drawn_cards)  # Record cards drawn in the current turn
        # Remove drawn cards from remained_cards
        for card in drawn_cards:
            if card in self.remained_cards:
                self.remained_cards.remove(card)
        
        # Calculate expected value of the remaining cards
        if self.remained_cards:
            expected_value = sum(self.remained_cards) / len(self.remained_cards)
        else:
            expected_value = 0
        action = current_sum+int(expected_value)
        # If log exists, find the maximum action from it
        # if log:
        #     max_action_from_log = max(entry['action'] for entry in log)
        #     # Use the maximum action from the log if it's greater than our calculated action
        #     if max_action_from_log > current_sum+1:
        #         action = max_action_from_log +1
        print(f"[SampleClient] AI selected action: {action}")
        print(f"Game Drawn Cards: {self.game_drawn_cards}")  # ゲーム全体のドローしたカードを表示
        return action