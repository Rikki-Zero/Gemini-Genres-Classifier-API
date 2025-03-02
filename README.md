# 音乐风格分类API

基于Gemini的音频文件音乐风格分类服务

## 快速开始

1. 进入开发环境：
```bash
nix develop
```

2. 启动API服务：
```bash
python src/api.py
```

3. 使用示例：
```bash
curl -X POST "http://localhost:8000/classify" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@/path/to/audio.mp3"
```

## API文档

访问 `http://localhost:8000/docs` 查看交互式API文档

## 参数说明

- file: 音频文件 (支持格式: mp3, wav等)
- genres_lang: 流派名称语言 (默认: en-us)
- reason_lang: 分类原因语言 (默认: zh-cn)

## 返回示例
```json
{
  "genres": ["Pop", "Electronic"],
  "reason": "这首歌的旋律和节奏都比较流行，同时使用了电子乐器进行编曲，因此被归类为流行和电子音乐。"
}
```
