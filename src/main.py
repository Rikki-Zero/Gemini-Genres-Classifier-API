from GenresClassifier import GenresClassifier

def main():
    try:
        ai = GenresClassifier()
        # （1m）freecompress-可不,雄之助,攻 - 花となれ.mp3
        ai.upload_to_gemini("/home/rikki/下载/tokyo blue weeps - Sundaland of mind.mp3", mime_type="audio/mpeg")
        x = ai.request()
        print(x)
    except Exception as e:
        print(f"发生错误: {str(e)}")
        # 打印完整的异常堆栈信息
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
