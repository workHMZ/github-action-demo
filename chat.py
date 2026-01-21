from openai import OpenAI
import os


# .envファイルの読み込みを試行（存在する場合）
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # python-dotenvがインストールされていない場合、システム環境変数を使用
    pass


def main():
    # OpenAIクライアントの初期化
    client = OpenAI()
    
    # 対話ID、サーバー側の対話状態を維持するために使用
    conversation_id = None
    print("'quit'または'exit'を入力してプログラムを終了")
    print("'new'を入力して新しい対話を開始")
    print("-" * 50)
    
    while True:
        try:
            # ユーザー入力の取得
            user_input = input("\nあなた: ").strip()
            
            # 終了コマンドの確認
            if user_input.lower() in ['quit', 'exit', '終了']:
                print("さようなら！")
                break
            
            # 新しい対話コマンドの確認
            if user_input.lower() in ['new', '新しい対話']:
                conversation_id = None
                print("新しい対話を開始")
                continue
            
            # 空の入力の場合はスキップ
            if not user_input:
                continue
            
            # APIリクエストパラメータの構築
            request_params = {
                "model": "gpt-5-mini",
                "input": [
                    {
                        "role": "user",
                        "content": user_input
                    }
                ]
            }
            
            # 対話IDがある場合、対話を継続するためにリクエストに追加
            if conversation_id:
                request_params["previous_response_id"] = conversation_id
            
            # OpenAI API呼び出し
            print("AIが考えています...")
            
            response = client.responses.create(**request_params)
            
            
            # AI応答と対話IDの取得
            ai_response = response.output_text
            
            print(response)
            print(type(response))
            
            conversation_id = response.id
            model = response.model
            print(f"使用モデル: {model}")                
            print(f"対話ID: {conversation_id}")
            
            # AI応答の表示
            print(f"\nAI: {ai_response}")
            
        except KeyboardInterrupt:
            print("\n\nプログラムがユーザーによって中断されました")
            break
        except Exception as e:
            print(f"\nエラーが発生しました: {e}")
            print("APIキーとネットワーク接続を確認してください")
            
            # 継続するかどうかの確認
            continue_chat = input("続行しますか？(y/n): ").strip().lower()
            if continue_chat not in ['y', 'yes', 'はい']:
                break


def check_api_key():
    """APIキーが設定されているかを確認"""
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("エラー: OPENAI_API_KEY環境変数が見つかりません")
        print("OpenAI APIキーを設定してください:")
        print("方法1 - 環境変数:")
        print("  Linux/Mac: export OPENAI_API_KEY='your-api-key-here'")
        print("  Windows: set OPENAI_API_KEY=your-api-key-here")
        print("方法2 - .envファイル:")
        print("  .envファイルを作成し追加: OPENAI_API_KEY=your-api-key-here")
        print("  （.envファイルが.gitignoreに含まれていることを確認）")
        return False
    return True


if __name__ == "__main__":
    # APIキーの確認
    if check_api_key():
        main()
    else:
        print("プログラムを終了")
