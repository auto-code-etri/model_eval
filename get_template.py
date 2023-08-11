import subprocess
import pandas as pd

def get_template(problem_number):
    # 실행할 명령어
    command1 = f"leetcode show -c {problem_number} -l python"
    command2 = f"leetcode show -c {problem_number} -l c"
    # 명령어 실행
    result1 = subprocess.run(command1, stdout=subprocess.PIPE, shell=True, text=True)
    result2 = subprocess.run(command2, stdout=subprocess.PIPE, shell=True, text=True)
    # 템플릿 추출
    return result1.stdout, result2.stdout

def extract_template(text):
    start_index = text.find("@lc code=start")  # "class"로 시작하는 인덱스 찾기
    end_index = text.find("@lc code=end", start_index)  # "# @lc code=end"로 끝나는 인덱스 찾기
    
    if start_index != -1 and end_index != -1:
        return text[start_index+14:end_index-3].strip()
    else:
        return None

def update_python_dataset(dataset, problem_number, python_template):
    index_to_update = dataset[dataset['id'] == problem_number].index
    if not index_to_update.empty:
        index_to_update = index_to_update[0]
        python_template_with_info = f"Create Python code based on outline below.\n{python_template}"
        dataset.at[index_to_update, 'python_template'] = python_template_with_info + dataset.at[index_to_update, 'python_template']

def update_c_dataset(dataset, problem_number, c_template):
    index_to_update = dataset[dataset['id'] == problem_number].index
    if not index_to_update.empty:
        index_to_update = index_to_update[0]
        c_template_with_info = f"Create c code based on outline below.\n{c_template}"
        dataset.at[index_to_update, 'c_template'] = c_template_with_info + dataset.at[index_to_update, 'c_template']


if __name__ == "__main__":
    # 기존 CSV 파일 불러오기
    csv_filename = "leetcode_dataset.csv"
    leetcode_dataset = pd.read_csv(csv_filename)
    
    # 'python_template', 'c_template'열 추가
    leetcode_dataset['python_template'] = ""
    leetcode_dataset['c_template'] = ""

    # 1부터 100까지의 문제 템플릿을 가져와서 leetcode_dataset에 추가
    for problem_number in range(1, 101):
        python_template,c_template = get_template(problem_number)
        extracted_python_template = extract_template(python_template)
        extracted_c_template = extract_template(c_template)
        update_python_dataset(leetcode_dataset, problem_number, extracted_python_template)
        update_c_dataset(leetcode_dataset, problem_number, extracted_c_template)

    # 업데이트된 데이터를 기존 CSV 파일에 추가하여 저장
    leetcode_dataset.to_csv(csv_filename, index=False, encoding='utf-8-sig')
    
    print(f"업데이트된 내용을 {csv_filename}에 저장했습니다.")
