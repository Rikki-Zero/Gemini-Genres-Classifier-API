import os
import json
import google.generativeai as genai
from google.ai.generativelanguage_v1beta.types import content

class GenresClassifier:
  def __init__(self):
    genai.configure(api_key=os.environ["GEMINI_API_KEY"])
    self.prevUploadedFile = None

    # Create the model
    self.generation_config = {
      "temperature": 1,
      "top_p": 0.95,
      "top_k": 40,
      "max_output_tokens": 8192,
      "response_schema": content.Schema(
        type = content.Type.OBJECT,
        enum = [],
        required = ["genres", "reason"],
        properties = {
          "genres": content.Schema(
            type = content.Type.ARRAY,
            items = content.Schema(
              type = content.Type.STRING,
            ),
          ),
          "reason": content.Schema(
            type = content.Type.STRING,
          ),
        },
      ),
      "response_mime_type": "application/json",
    }

    self.model = genai.GenerativeModel(
      model_name="gemini-2.0-flash-exp",
      generation_config=self.generation_config,
      system_instruction="音乐流派的分类标准是**多维度**的，它们并非基于单一的标准划分，而是综合考虑了以下几个方面：\n\n1. 音乐形式和结构 (Musical Form and Structure):**\n\n*   **和声 (Harmony):** 不同流派使用不同的和弦进行、和声方式和音阶，如蓝调的蓝调音阶、古典音乐的复杂和声结构、爵士乐的和弦即兴等。\n*   **旋律 (Melody):** 不同流派的旋律走向、音高、节奏都不同，如摇滚乐的强烈节奏、流行乐的易于传唱的旋律等。\n*   **节奏 (Rhythm):** 不同流派的节奏模式不同，如雷鬼的切分节奏、嘻哈的鼓点节拍、放克的律动节奏等。\n*   **乐器 (Instrumentation):** 不同流派偏好的乐器不同，如古典音乐的管弦乐团、摇滚乐的电吉他、电子音乐的合成器等。\n*   **曲式结构 (Form):** 不同流派的歌曲结构也不同，如布鲁斯的 12 小节形式、流行乐的 Verse-Chorus 结构、古典音乐的奏鸣曲形式等。\n\n**2. 文化和历史渊源 (Cultural and Historical Origins):**\n\n*   **起源地 (Origin):** 许多流派都起源于特定的文化和地域，如蓝调起源于美国南方非裔社区、爵士乐起源于美国新奥尔良、拉丁音乐起源于拉丁美洲等。\n*   **历史时期 (Historical Period):** 不同流派流行于不同的历史时期，如古典音乐盛行于巴洛克和古典时期、摇滚乐兴起于 20 世纪 50 年代、嘻哈兴起于 20 世纪 70 年代等。\n*   **社会文化背景 (Social and Cultural Context):** 一些流派的兴起与特定的社会文化背景有关，如摇滚乐的叛逆精神、嘻哈的街头文化等。\n\n**3. 功能和用途 (Function and Purpose):**\n\n*   **娱乐 (Entertainment):** 大多数流派的主要功能是娱乐，如流行音乐、摇滚乐等。\n*   **舞蹈 (Dance):** 一些流派主要用于舞蹈，如放克、拉丁、雷鬼等。\n*   **仪式或宗教 (Ritual or Religious):** 一些流派与宗教或仪式有关，如一些民谣、世界音乐等。\n*   **戏剧和电影 (Drama and Film):** \"Stage & Screen\" 属于为戏剧或电影而创作的配乐。\n\n**4. 情感表达和氛围 (Emotional Expression and Atmosphere):**\n\n*   **情绪 (Mood):** 不同流派表达的情绪不同，如蓝调的忧郁、流行乐的欢快、古典音乐的庄严、摇滚乐的激情等。\n*   **氛围 (Atmosphere):** 不同流派营造的氛围不同，如电子音乐的未来感、民谣的淳朴感、爵士乐的慵懒感等。\n\n**具体到列表中：**\n\n*   **Blues:** 主要基于蓝调音阶和 12 小节形式，起源于美国非裔社区。\n*   **Brass & Military:** 使用铜管乐器为主，用于军事或仪式场合。\n*   **Children's:** 面向儿童的音乐，通常旋律简单、歌词易懂。\n*   **Classical:** 基于古典时期音乐的风格和结构，通常使用管弦乐团演奏。\n*   **Electronic:** 使用电子乐器和技术创作的音乐。\n*   **Folk, World, & Country:** 包含各种传统民俗音乐、世界各地音乐以及美国乡村音乐。\n*   **Funk/Soul:** 源于美国黑人音乐，强调节奏感和律动，多用于舞蹈。\n*   **Hip-Hop:** 以说唱为主，强调节奏和歌词表达，起源于美国街头文化。\n*   **Jazz:** 源于美国非裔社区，强调即兴演奏和独特的和弦进行。\n*   **Latin:** 包含来自拉丁美洲各地的音乐风格，节奏鲜明，多用于舞蹈。\n*   **Non-Music:** 非音乐性质的音频，如环境音效、广播剧等。\n*   **Pop:** 强调旋律朗朗上口，迎合大众口味。\n*   **Reggae:** 源于牙买加，以切分节奏为特点，常用于舞蹈。\n*   **Rock:** 以电吉他为主，强调节奏感和力量，通常表达叛逆或激情。\n*   **Stage & Screen:** 为舞台剧、电影、电视剧创作的配乐，烘托剧情和人物情绪。\n\n\n请根据音乐的以下特征，将其分类到以下音乐流派中：蓝调(Blues)、铜管与军乐(Brass & Military)、儿童音乐(Children's)、古典音乐(Classical)、电子音乐(Electronic)、民谣、世界音乐及乡村音乐(Folk, World, & Country)、放克/灵魂乐(Funk / Soul)、嘻哈音乐(Hip-Hop)、爵士乐(Jazz)、拉丁音乐(Latin)、非音乐(Non-Music)、流行音乐(Pop)、雷鬼音乐(Reggae)、摇滚乐(Rock)、舞台与银幕音乐(Stage & Screen)。\n\n请考虑以下特征进行分类：\n- 音乐形式和结构：包括和声、旋律、节奏、乐器使用、曲式结构等。\n- 文化和历史渊源：包括起源地、历史时期、社会文化背景等。\n- 功能和用途：包括娱乐、舞蹈、仪式、宗教、戏剧和电影等。\n- 情感表达和氛围：包括情绪、氛围等。\n\n如果音乐属于多个流派，请按照相关度排序输出，并简要说明分类依据。\n\n输入中如果附加区域代码，请使用该区域代码的本地化翻译返回分类结果\n\n样例输入：\n\n<音乐>\n\n```\ngenres: en-us\nreason: zh-cn\n```\n\n应该给出这样的返回\n```\n{\n   \"genres\": [\n      \"Pop\",\n      \"Electronic\"\n   ],\n   \"reason\": \"这首歌的旋律和节奏都比较流行，同时使用了电子乐器进行编曲，因此被归类为流行和电子音乐。\"\n}\n```\n\n但是，如果当前输入变成：\n\n```\ngenres: zh-cn\nreason: en-us\n```\n\n你需要输出：\n```\n{\n   \"genres\": [\n      \"流行音乐\",\n      \"电子音乐\"\n   ],\n   \"reason\": \"The song has a catchy rhythm and melody, and it uses electronic instruments in its arrangement, so it's categorized as both electronic and pop music.\"\n}\n```\n\n输入中的genres对应到输出genres的语言，输入中的reason字段同理\n其他语言以此类推\n请你注意检查输出语言是否和用户当前输入的要求相符。\n如果用户什么也没有输入，只输入了音乐，请按照：\n\n```\ngenres: en-us\nreason: zh-cn\n```\n\n理解。\n\n最终输出结果结构如下：\n```\n{\n   \"Genres\": [],\n   \"reason\": \"\"\n}\n```",
    )

    self.chat_session = None

  def upload_to_gemini(self, path, mime_type=None):
    file = genai.upload_file(path, mime_type=mime_type)

    print(f"Uploaded file '{file.display_name}' as: {file.uri}")

    self.prevUploadedFile = file

    # Initialize or update chat session
    if self.chat_session is None:
        self.chat_session = self.model.start_chat(
            history=[
                {
                    "role": "user",
                    "parts": [
                        self.prevUploadedFile,
                    ],
                },
            ]
        )
    else:
        self.chat_session.history = [
            {
                "role": "user",
                "parts": [
                    self.prevUploadedFile,
                ],
            },
        ]

    return file
  
  def request(self, genresLang = "en-us", reasonLang = "zh-cn"):
    if self.prevUploadedFile == None:
      raise SystemError("请先上传文件")
    
    settingStr = '''
      genres: {0}
      reason: {1}
    '''.format(genresLang,reasonLang)

    response = self.chat_session.send_message(settingStr)

    return json.loads(response.text)
