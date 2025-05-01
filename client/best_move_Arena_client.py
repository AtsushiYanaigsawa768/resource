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
        self.int_remained_cards = 36 
        self.history_card_info = [] #1ターン前のカード情報を保持するリスト
    
    def reset_card_info(self):
        # カードのデッキを初期化：数値×枚数の形式でリストに追加
        self.remained_cards = []
        for value, count in [
            (1, 4), (2, 4), (3, 4), (4, 4), (5, 4),
            (10, 3), (15, 2), (20, 1),
            (0, 3), (-5, 2), (-10, 1)
        ]:
            self.remained_cards.extend([value] * count)
        self.int_remained_cards = 36


    def AI_player_action(self,others_info, current_sum, log, actions):
        print(f"[SampleClient] AI deciding action based on sum: {current_sum}, log: {log}, actions: {actions},others_info: {others_info}")

        # Extract card_info from others_info
        drawn_cards = [player['card_info'] for player in others_info]
        if self.history_card_info != drawn_cards:
            # カードの情報が異なる場合、新たなターンが始まったとみなす。
            self.history_card_info = drawn_cards
            self.int_remained_cards -= len(drawn_cards) + 1  # 残りのカード枚数を減少 (1は自分のカード)
            if self.int_remained_cards < 0:
                self.reset_card_info()  # 残りのカードが0未満になった場合、カード情報をリセット
                self.int_remained_cards -= len(drawn_cards) + 1

        print(log)
        time.sleep(3)
        
        # 以下は、期待値を計算するためのロジック
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

        # coyote絶対に宣言したくない場合、以下のコードを有効にする
        # If log exists, find the maximum action from it
        # if log:
        #     max_action_from_log = max(entry['action'] for entry in log)
        #     # Use the maximum action from the log if it's greater than our calculated action
        #     if max_action_from_log > current_sum+1:
        #         action = max_action_from_log +1
        print(f"[SampleClient] AI selected action: {action}")
        print(f"Game Drawn Cards: {self.game_drawn_cards}")  # ゲーム全体のドローしたカードを表示
        return action