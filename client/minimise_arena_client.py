from .not_websocket_client import Client
import random
import time 
class SampleClient(Client):
    def AI_player_action(self,others_info, sum, log, actions, round_num):
        # カスタムロジックを実装
        print(f"[A SampleClient] AI deciding action based on sum: {sum}, log: {log}, actions: {actions},others_info: {others_info}, round_num: {round_num}" )
        # 例: ランダムにアクションを選択
        # action = random.choice(actions)
        # 例：最小値を選択
        if len(actions) != 1:
            action = min([a for a in actions if a > -1])
        else:
            action = actions[0]
        print(f"[A SampleClient] AI selected action: {action}")
        time.sleep(1)
        return action