import json
import re

# 删除src src\s*=\s*(?:"([^"]+)"|'([^']+)'|([^\s>]+))

# --- 配置 ---
TARGET_CHARACTER_NAME = "索拉"
INPUT_HTML_FILE = "module\conversation\dialogue_raw.html"
OUTPUT_JSON_FILE = "module\conversation\dialogue.json"

def parse_with_regex(html_content):
    """
    使用正则表达式解析HTML内容。
    这种方法比纯字符串操作更健壮，能更好地应对微小的格式变化。
    """
    conversations = []
    
    # 定义正则表达式模式
    # - (.*?) 是一个非贪婪捕获组，用于抓取我们需要的内容。
    # - re.DOTALL 标志让 . (点号) 可以匹配包括换行符在内的任意字符。
    pattern = re.compile(
        r'class="list-title">.*?<span.*?>(.*?)</span>.*?'  # 捕获组 1: question
        r'class="dialogue-100">.*?<span.*?>(.*?)</span>.*?' # 捕获组 2: false_answer
        r'class="dialogue-120">.*?<span.*?>(.*?)</span>',   # 捕获组 3: true_answer
        re.DOTALL
    )
    
    # 查找所有匹配项
    # findall会返回一个元组（tuple）的列表，每个元组包含所有捕获组的内容
    matches = pattern.findall(html_content)
    
    for match in matches:
        # match[0] 是问题, match[1] 是 false 答案, match[2] 是 true 答案
        question = match[0].strip()
        false_answer = match[1].strip()
        true_answer = match[2].strip()
        
        conversations.append({
            "question": question,
            "answer": {
                "false": false_answer,
                "true": true_answer
            }
        })
        
    return conversations

# (下方的 update_json_file 和 main 函数与之前的版本相同，这里不再重复)
def update_json_file(character_name, data_list):
    existing_data = {}
    try:
        with open(OUTPUT_JSON_FILE, 'r', encoding='utf-8') as f:
            existing_data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        pass

    updated_data = {character_name: data_list}
    for key, value in existing_data.items():
        if key != character_name:
            updated_data[key] = value
            
    with open(OUTPUT_JSON_FILE, 'w', encoding='utf-8') as f:
        json.dump(updated_data, f, ensure_ascii=False, indent=2)

def main():
    try:
        with open(INPUT_HTML_FILE, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"错误: 输入文件 '{INPUT_HTML_FILE}' 未找到。")
        return
        
    character_name_from_file = lines[0].strip()
    html_content = "".join(lines[1:])
    
    if character_name_from_file == TARGET_CHARACTER_NAME:
        print(f"找到目标角色 '{TARGET_CHARACTER_NAME}'，使用正则表达式处理...")
        extracted_data = parse_with_regex(html_content)
        if extracted_data:
            update_json_file(TARGET_CHARACTER_NAME, extracted_data)
            print(f"处理完成！数据已成功保存或更新到 '{OUTPUT_JSON_FILE}'。")
        else:
            print("警告: 未从HTML中提取到任何有效数据。")
    else:
        print(f"文件中的角色 '{character_name_from_file}' 不是目标角色 '{TARGET_CHARACTER_NAME}'，已跳过。")

if __name__ == '__main__':
    main()