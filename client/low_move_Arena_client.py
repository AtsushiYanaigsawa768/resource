from .not_websocket_client import Client
import random
import time

class SampleClient(Client):
    def AI_player_action(self,others_info, sum, log, actions):
        # カスタムロジックを実装
        print(f"[SampleClient] AI deciding action based on sum: {sum}, log: {log}, actions: {actions},others_info: {others_info}")
        # 例: ランダムにアクションを選択
        action = max(min(actions),sum+1)
        print(f"[SampleClient] AI selected action: {action}")
        return action