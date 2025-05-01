from server.arena import Arena
if __name__ == "__main__":
    # -- Example usage --
    #
    # もし事前に定義したクライアントを渡したい場合:
    #
    from client.sample_arena_client import SampleClient as SampleClient
    from client.gemini_client import GeminiSampleClient as GeminiSampleClient
    
    predefs = [
        [SampleClient(player_name="PreAI1", is_ai=True), "PreAI1"],
        [SampleClient(player_name="PreAI2", is_ai=True), "PreAI2"],
        [GeminiSampleClient(player_name="PreAI3", is_ai=True), "PreAI3"],
    ]
    
    arena = Arena(total_matches=5, predefined_clients=predefs)
    arena.run()
    #
    
    # 事前クライアントを指定せずに起動
    
    # arena = Arena()
    # arena.run()