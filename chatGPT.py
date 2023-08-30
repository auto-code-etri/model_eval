# leetcode_dataset.csv 파일 불러오기 및 수정
import warnings
warnings.filterwarnings("ignore")
import pandas as pd
data=pd.read_csv('leetcode_dataset.csv')
data.info()

#인덱스 추출
leetcode = data[['id','title','description','related_topics','python_template','c_template']]
leetcode.head(10)


# chat GPT에게 input할 데이터 파싱
# 각 행(문제)마다 description열의 내용에서 d, e, c를 추출하여 저장할 변수 초기화
d = []
e = []
c = []
pcode = []
ccode=[]

# 각 행(문제)을 순회하며 d, e, c 값을 추출하여 저장
for index, row in data.iterrows():
    description = row['description']
    example_start_index = description.find("Example 1")
    constraints_start_index = description.find("Constraints")
    
    # "Example 1" 문자열이 나오기 전까지 description에서 d 값 추출
    if example_start_index != -1:
        d.append(description[:example_start_index])
    else:
        d.append(description)
    
    # "Example 1" 문자열이 나오기 시작해서 "Constraints" 문자열이 나오기 전까지 description에서 e 값 추출
    if example_start_index != -1 and constraints_start_index != -1:
        e.append(description[example_start_index:constraints_start_index])
    else:
        e.append("")
    
    # "Constraints" 문자열이 나오기 시작하는 내용부터 description에서 c 값 추출
    if constraints_start_index != -1:
        c.append(description[constraints_start_index:])
    else:
        c.append("")
    
    # python_template의 내용은 변수 pcode에 저장
    pcode.append(row['python_template'])

    #c_template의 내용은 변수 ccode에 저장
    ccode.append(row['c_template'])


# chat GPT와 통신
# python 코드 생성
import os
import openai
import json
import time

openai.api_key = "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"

results = []

def count_tokens(text):
    return len(openai.Completion.create(prompt=text, max_tokens=1)["usage"]["total_tokens"])

# ChatGPT가 생성한 코드에서 특정 템플릿 부분을 추출하는 함수
def extract_class_code(result):
    start_index = result.find("class")
    if start_index == -1:
        return result
    end_index = result.find("```", start_index) if '```' in result else len(result)
    return result[start_index:end_index]

# ChatGPT를 사용하여 코드를 생성하고 추출하는 함수
def fetch_code(messages, max_retries=3, delay=60):
    retries = 0
    while retries < max_retries:
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages
            )
            code = response["choices"][0]["message"]["content"]
            class_code = extract_class_code(code)
            
            token_count = response["usage"]["total_tokens"]
            if token_count >= 4000:
                time.sleep(60)
            elif "class Solution" in class_code:
                return class_code
            else:
                time.sleep(40)
        except Exception as e:
            print(f"Error occurred: {e}. Retrying in {delay} seconds.")
            retries += 1
            time.sleep(delay)
    
    raise Exception("Failed to fetch code after multiple retries.")

# 문제별로 ChatGPT를 사용하여 코드를 생성하고 추출하는 과정을 반복
for i in range(100):
    first_results = []
    second_results = []
    third_results = []

    messages = [
        {"role": "user", "content": "Please implement the following code. I don't need an explanation."},
        {"role": "user", "content": f"Description: {d[i]}"},
        {"role": "user", "content": f"Code outline: {pcode[i]}"}
    ]

    for _ in range(10):
        first_results.append(fetch_code(messages))
        
        messages_second = messages + [{"role": "user", "content": f"Constraints: {c[i]}"}]
        second_results.append(fetch_code(messages_second))
        
        messages_third = messages_second + [{"role": "user", "content": f"Example: {e[i]}"}]
        third_results.append(fetch_code(messages_third))

    result_obj = {
        "num": i + 1,
        "title":leetcode['title'][i],
        "description":d[i],
        "constraints":c[i],
        "category":leetcode['related_topics'][i],
        "python_template": leetcode['python_template'][i],
        "first_result": first_results,
        "second_result": second_results,
        "third_result": third_results
    }
    results.append(result_obj)
    print(i+1,"저장")

filename = "python-results.json"
with open(filename, mode='w', encoding="utf-8-sig") as file:
    json.dump(results, file, ensure_ascii=False, indent=2)

print(f"모든 문제의 결과가 JSON 파일로 저장되었습니다.")


# c코드 생성
import os
import openai
import json
import time

# OpenAI API 키 설정
openai.api_key = "1234"

# 결과를 저장할 리스트 초기화
results = []

# ChatGPT가 생성한 코드에 특정 템플릿이 포함되었는지 확인하는 함수
def contains_c_template(code, template):
    template_start = template.split("(")[0]  # "(" 이전 부분을 추출
    return template_start in code

# ChatGPT가 생성한 코드에서 특정 템플릿 부분을 추출하는 함수
def extract_code(result, template):
    template_start = template.split("(")[0]
    start_index = result.find(template_start)
    if start_index == -1:
        return result
    end_index = result.rfind("}")
    if end_index == -1:
        return result
    return result[start_index:end_index+1]

# ChatGPT를 사용하여 코드를 생성하고 추출하는 함수
def fetch_code(messages, template, max_retries=3, delay=60):
    retries = 0
    while retries < max_retries:
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages
            )
            code = response["choices"][0]["message"]["content"]
            
            token_count = response["usage"]["total_tokens"]
            if token_count >= 4000:
                time.sleep(60)
            elif contains_c_template(code, template):
                code = extract_code(code, template)
                return code
            else:
                time.sleep(40)
        except Exception as e:
            print(f"Error occurred: {e}. Retrying in {delay} seconds.")
            retries += 1
            time.sleep(delay)
    
    raise Exception("Multiple retries failed. Failed to fetch code.")

# 문제별로 ChatGPT를 사용하여 코드를 생성하고 추출하는 과정을 반복
for i in range(100):
    first_results = []
    second_results = []
    third_results = []

    template = ccode[i]  # 현재 문제에 해당하는 C 템플릿 가져오기

    messages = [
        {"role": "user", "content": "Please implement the following code. I don't need an explanation."},
        {"role": "user", "content": f"Description: {d[i]}"},
        {"role": "user", "content": f"Code outline: {ccode[i]}"}
    ]

    for _ in range(10):
        first_results.append(fetch_code(messages, template))
        
        messages_second = messages + [{"role": "user", "content": f"Constraints: {c[i]}"}]
        second_results.append(fetch_code(messages_second, template))
        
        messages_third = messages_second + [{"role": "user", "content": f"Example: {e[i]}"}]
        third_results.append(fetch_code(messages_third, template))

    result_obj = {
        "num": i + 1,
        "title": leetcode['title'][i],
        "description": d[i],
        "constraints": c[i],
        "category": leetcode['related_topics'][i],
        "python_template": template,
        "first_result": first_results,
        "second_result": second_results,
        "third_result": third_results
    }
    results.append(result_obj)
    print(i+1, "저장")

filename = "c-results.json"
with open(filename, mode='w', encoding="utf-8-sig") as file:
    json.dump(results, file, ensure_ascii=False, indent=2)

print(f"모든 문제의 결과가 JSON 파일로 저장되었습니다.")
