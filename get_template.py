import subprocess
import pandas as pd

def get_template(problem_number):
    command1 = f"leetcode show -c {problem_number} -l python"
    command2 = f"leetcode show -c {problem_number} -l c"
    result1 = subprocess.run(command1, stdout=subprocess.PIPE, shell=True, text=True)
    result2 = subprocess.run(command2, stdout=subprocess.PIPE, shell=True, text=True)
    return result1.stdout, result2.stdout

def extract_template(text):
    start_index = text.find("@lc code=start")
    end_index = text.find("@lc code=end", start_index)
    
    if start_index != -1 and end_index != -1:
        extracted_template = text[start_index + 14:end_index - 3].strip()
        if extracted_template.startswith("/**"):
            end_comment_index = extracted_template.find("*/")
            if end_comment_index != -1:
                extracted_template = extracted_template[end_comment_index + 2:].strip()
        return extracted_template
    else:
        return None

def update_python_dataset(dataset, problem_number, python_template):
    index_to_update = dataset[dataset['id'] == problem_number].index
    if not index_to_update.empty:
        index_to_update = index_to_update[0]
        dataset.at[index_to_update, 'python_template'] = python_template

def update_c_dataset(dataset, problem_number, c_template):
    index_to_update = dataset[dataset['id'] == problem_number].index
    if not index_to_update.empty:
        index_to_update = index_to_update[0]
        dataset.at[index_to_update, 'c_template'] = c_template

if __name__ == "__main__":
    csv_filename = "leetcode_dataset.csv"
    leetcode_dataset = pd.read_csv(csv_filename)
    
    leetcode_dataset['python_template'] = ""
    leetcode_dataset['c_template'] = ""

    for problem_number in range(1, 101):
        python_template, c_template = get_template(problem_number)
        extracted_python_template = extract_template(python_template)
        extracted_c_template = extract_template(c_template)
        update_python_dataset(leetcode_dataset, problem_number, extracted_python_template)
        update_c_dataset(leetcode_dataset, problem_number, extracted_c_template)

    leetcode_dataset.to_csv(csv_filename, index=False, encoding='utf-8-sig')
    
    print(f"업데이트된 내용을 {csv_filename}에 저장했습니다.")