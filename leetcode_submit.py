import time
import json
import subprocess

def test_save(filename):    
    result = subprocess.run("leetcode submit {}".format(filename), shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)    
    return result.stdout.decode("utf-8")

def clean_filename(title):
    return title.replace(" ", "-")

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

            try_results.append({"try": idx, "test": test_result})

    return try_results

with open("1-25 python-results.json", encoding="utf-8-sig") as file:
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

with open("1-25 submit_result.json", "w", encoding="utf-8") as result_file:
    json.dump(all_results, result_file, indent=2)

print("All test results have been saved in compile_result.json.")
