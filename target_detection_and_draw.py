import requests
from PIL import Image, ImageDraw
import json
import re
import config
url = "https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation"
api_key =config.aliyuncs_API_KEY

# 构造请求头
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"  
}

# 构造请求体
payload1 = {
    "model": "qwen-vl-max",
    "input": {
        "messages": [
            {
                "role": "system",
                "content": [
                    {
                        "type": "text",
                        "text": "You are an intelligent assistant capable of accurately identifying dogs from pictures., Definition: A dog refers to a dog in the biological sense. Therefore, other items like clouds or fragments that resemble a dog are not considered dogs."
                    }
                ]
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "image": "https://images.pexels.com/photos/247522/pexels-photo-247522.jpeg"
                        
                        
                    },
                    {
                        "type": "text",
                        "text": r""" Describe this picture in detail in chinese"""
                    }
                ]
            }
        ]
    }
}
response = requests.post(url, headers=headers, json=payload1)  
if response.status_code == 200:
    result = response.json()
    print(result["output"]["choices"][0]["message"]["content"][0]["text"])
else:
    print(f"请求失败，状态码: {response.status_code}")
    print("错误信息:", response.text)
payload2 = {
    "model": "qwen-vl-max",
    "input": {
        "messages": [
            {
                "role": "system",
                "content": [
                    {
                        "type": "text",
                        "text": "You are an intelligent assistant capable of accurately identifying dogs from pictures., Definition: A dog refers to a dog in the biological sense. Therefore, other items like clouds or fragments that resemble a dog are not considered dogs."
                    }
                ]
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "image": "https://images.pexels.com/photos/247522/pexels-photo-247522.jpeg"
                        
                        
                    },
                    {
                        "type": "text",
                        "text": r""" analyze this image and determine whether there is a dog within it. Just identify the presence of the dog. If the dog is
                                    identified, only return the result in JSON without Markdown: {"result": "yes", "bounding_boxes": [[xmin, ymin, xmax, ymax], ...] }; 
                                    otherwise, return: {"result": "no"}."""
                    }
                ]
            }
        ]
    }
}
# 发送请求
response = requests.post(url, headers=headers, json=payload2)  
if response.status_code == 200:
    result = response.json()
    #提取AI返回的坐标数据
    Coordinate=result["output"]["choices"][0]["message"]["content"][0]["text"]
    #由于返回的数据被。```jaon ````包裹，使用正则表达式提取其中间的数据
    json_match = re.search(r'```json\n(.*?)\n```', Coordinate, re.DOTALL)
    json_str = json_match.group(1)
    #此时其任然为一个字符串，将其转化为字典
    data_dict = json.loads(json_str)
    Coordinates = data_dict["bounding_boxes"][0]
    print("坐标提取完毕")
else:
    print(f"请求失败，状态码: {response.status_code}")
    print("错误信息:", response.text)
#根据提取到的坐标绘制出相应的区域
with Image.open("C:/Users/wxx/Desktop/test5/dog_picture.png") as img:
    #由于ai无法读取图片大小，也无法强制要求使用提供的图片大小数据，所以只能更改图片大小使之与AI估计的大小相吻合
    img_process = img.resize((1311,737))
    draw = ImageDraw.Draw(img_process)
    draw.rectangle(Coordinates, outline="red", width=3)
    img_process.save("C:/Users/wxx/Desktop/test5/processed_dog_picture.png")
    print("图片绘制完毕")