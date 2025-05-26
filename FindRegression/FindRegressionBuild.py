import os
import subprocess
import shlex
from datetime import datetime

# ==== Configuration ====
sub_path = r"xxx"
include_subpath = r"xxx"
source_file = "test.cpp"
log_file = "build_test_log.txt"
# Your base compiler flags (easy to modify!)
base_compile_options = '/c /EHsc /std:c++latest'
# =======================

def is_valid_version_dir(name):
    return len(name) == 11 and name[:8].isdigit() and name[8] == '.' and name[9:].isdigit()

def log_to_file(message):
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(message + "\n")

def compile_with_cl(cl_path, version, base_dir):
    version_dir = os.path.join(base_dir, version)
    include_path = os.path.join(version_dir, include_subpath)

    #compile_options = f'{base_compile_options} /I"{include_path}"'
    compile_options = f'{base_compile_options}'
    include_path_new = f'-I{include_path}'
    command = [cl_path] + [include_path_new] + shlex.split(compile_options) + [source_file]

    try:
        result = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=60,
            check=False,
        )
        success = result.returncode == 0
        log_entry = (
            f"=== Version: {version} ===\n"
            f"Command: {' '.join(command)}\n"
            f"Return Code: {result.returncode}\n"
            f"--- STDOUT ---\n{result.stdout.decode(errors='ignore')}\n"
            f"--- STDERR ---\n{result.stderr.decode(errors='ignore')}\n"
            f"Result: {'SUCCESS' if success else 'FAILURE'}\n"
            f"{'-'*40}\n"
        )
        log_to_file(log_entry)
        return success
    except Exception as e:
        log_to_file(f"Exception for {version}: {e}")
        return False

def binary_search_regression_build(base_dir):
    print(f"\n🔍 Searching in: {base_dir}")
    log_to_file(f"\n===== Searching in: {base_dir} =====")

    try:
        version_dirs = [
            d for d in os.listdir(base_dir)
            if is_valid_version_dir(d) and os.path.isdir(os.path.join(base_dir, d))
        ]
    except Exception as e:
        print(f"❌ Cannot access directory: {base_dir}, error: {e}")
        log_to_file(f"Cannot access directory: {base_dir}, error: {e}")
        return None, None

    version_dirs.sort()
    left = 0
    right = len(version_dirs) - 1
    regression_index = None

    while left <= right:
        mid = (left + right) // 2
        version = version_dirs[mid]
        cl_path = os.path.join(base_dir, version, sub_path)

        if not os.path.isfile(cl_path):
            print(f"[Skipped] cl.exe not found: {version}")
            log_to_file(f"[Skipped] cl.exe not found: {version}")
            mid += 1
            continue

        print(f"🧪 Testing version: {version}")
        success = compile_with_cl(cl_path, version, base_dir)

        if (not success):
            regression_index = mid
            right = mid - 1
        else:
            left = mid + 1

    if regression_index is not None and regression_index > 0:
        regression_version = version_dirs[regression_index]
        prev_version = version_dirs[regression_index - 1]
        regression_cl = os.path.join(base_dir, regression_version, sub_path)
        include_path = os.path.join(base_dir, regression_version, include_subpath)
        compile_cmd = f'"{regression_cl}" /I"{include_path}" {source_file} {base_compile_options}'

        print(f"\n✅ Regression build found: {regression_version}")
        print(f"⬅️ Previous failing version: {prev_version}")
        print(f"\n👉 Full command to compile:")
        print(compile_cmd)

        log_to_file(f"\n✅ Regression build found: {regression_version}")
        log_to_file(f"⬅️ Previous failing version: {prev_version}")
        log_to_file(f"Full compile command: {compile_cmd}")
        return regression_version, regression_cl
    else:
        print("🚫 No regression build found in this path.")
        log_to_file("🚫 No regression build found in this path.")
        return None, None

def find_regression_build_with_fallback():
    log_to_file(f"\n===== Regression Build Search Started at {datetime.now()} =====")

    # First try in Builds path
    primary_base = r"xxx"
    version, cl_path = binary_search_regression_build(primary_base)
    if version:
        return version

    # If not found, fallback to Archive path
    archive_base = r"xxx"
    return binary_search_regression_build(archive_base)

if __name__ == "__main__":
    find_regression_build_with_fallback()
