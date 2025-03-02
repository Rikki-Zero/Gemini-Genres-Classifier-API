import requests

def main():
    try:
        url = "http://localhost:8000/classify"
        files = {"file": open("/home/rikki/下载/tokyo blue weeps - Sundaland of mind.mp3", "rb")}
        response = requests.post(url, files=files)
        print(response.json())
    except Exception as e:
        print(f"发生错误: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
