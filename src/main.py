from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from GenresClassifier import GenresClassifier
import os

app = FastAPI(
    title="音乐风格分类API",
    description="基于Gemini的音频文件音乐风格分类服务",
    version="1.0.0",
)

classifier = GenresClassifier()

@app.post("/classify")
async def classify_music(
    file: UploadFile = File(...),
    genres_lang: str = "en-us",
    reason_lang: str = "zh-cn"
):
    try:
        # 保存临时文件
        temp_path = f"/tmp/{file.filename}"
        with open(temp_path, "wb") as buffer:
            buffer.write(await file.read())
        
        # 上传并分类
        classifier.upload_to_gemini(temp_path, file.content_type)
        result = classifier.request(genres_lang, reason_lang)
        
        # 清理临时文件
        os.remove(temp_path)
        
        return JSONResponse(content=result)
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"分类失败: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
