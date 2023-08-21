import time
import json
import subprocess
import re

def test_save(filename):    
    result = subprocess.run("leetcode submit {}".format(filename), shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)    
    return result.stdout.decode("utf-8")

def clean_filename(title):
    return title.replace(" ", "-")

def parse_message(message):
    parsed_data = {}
    
    # Extracting "Accepted" or "Runtime Error" or "Wrong Answer"
    match = re.search(r"([^\n]+)\n", message)
    if match:
        parsed_data["result"] = match.group(1).replace("\u00d7", "").strip()
    
    # Extracting numbers (987, 987)
    numbers = re.findall(r"\d+", message)
    if len(numbers) >= 2:
        parsed_data["passed_test"] = int(numbers[0])
        parsed_data["total_test"] = int(numbers[1])
    
    # Extracting runtime information (41 ms)
    runtime_match = re.search(r"\(([\d\.]+ \w+)\)", message)
    if runtime_match:
        parsed_data["runtime"] = runtime_match.group(1)
    
    # Check if the status is "Accepted"
    if "Accepted" in parsed_data.get("result", ""):
        accepted_match = re.search(r"passed \(([\d\.]+ \w+)\)\n(.+)", message, re.DOTALL)
        if accepted_match:
            etc_content = accepted_match.group(2)
            
            # Cleaning up leading/trailing whitespace and newlines
            etc_content = etc_content.strip()
            
            parsed_data["etc"] = etc_content
    else:
        # Extracting the content after the "passed" information
        passed_match = re.search(r"passed \(N/A\)\n(.+)", message, re.DOTALL)
        if passed_match:
            etc_content = passed_match.group(1)
            
            # Cleaning up leading/trailing whitespace and newlines
            etc_content = etc_content.strip()
            
            parsed_data["etc"] = etc_content
    
    return parsed_data

def run_tests(results_name, entry):
    results = entry.get(results_name, [])
    title = entry.get("title", "Untitled") 
    cleaned_title = clean_filename(title.lower())
    try_results = []

    if results and len(results) > 0:
        for idx, line in enumerate(results, start=1):
            filename = "Compile/{}.py".format(cleaned_title)
            print(filename)
            with open(filename, "w") as pyfile:
                pyfile.write(line)
            print(f"Python file '{filename}' ({results_name} line {idx}) has been created and saved.")

            while True:
                test_result = test_save(filename)
                time.sleep(40)
                if test_result == "[ERROR] http error [code=429]\n":
                    print("429 error encountered. Waiting for 10 seconds before retrying.")
                else:
                    break

            # Parse the test_result using parse_message function
            parsed_result = parse_message(test_result)
            parsed_result["try"] = idx  # Add "try" value to the parsed_result
            
            try_results.append(parsed_result)

    return try_results


with open("python-results.json", encoding="utf-8-sig") as file:
    json_data = json.load(file)

all_results = []
for entry in json_data:
    num = entry.get("num")
    archive_date=entry.get("archive_date","null")
    title = entry.get("title", "Untitled") 
    first_results = run_tests("first_result", entry)
    second_results = run_tests("second_result", entry)
    third_results = run_tests("third_result", entry)

    result_obj = {
        "num": num,
        "title": title,
        "first_result": first_results,
        "second_result": second_results,
        "third_result": third_results
    }
    all_results.append(result_obj)

with open("python submit-result.json", "w", encoding="utf-8") as result_file:
    json.dump(all_results, result_file, indent=2)

print("All test results have been saved.")
