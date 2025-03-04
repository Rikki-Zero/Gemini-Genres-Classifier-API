import requests

def main():
    try:
        url = "http://localhost:8000/classify"
        files = {"file": open("/home/rikki/下载/25.最終舞曲 I.m4a", "rb")}
        response = requests.post(url, files=files)
        print(response.json())
    except Exception as e:
        print(f"发生错误: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
