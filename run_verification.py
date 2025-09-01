import subprocess
import os
import json

def run_command(command):
    """
    运行一个shell命令。
    如果命令成功执行，返回True；如果失败，打印错误并返回False。
    """
    print(f"--- Running command: {' '.join(command)} ---")
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"!!! ERROR: Command failed with return code {result.returncode}")
        print("--- stderr ---\n" + result.stderr)
        return False
    else:
        print("--- Command executed successfully ---")
        return True

def build_and_test():
    """
    封装了构建和测试C++项目的逻辑。
    返回测试程序的退出代码（0代表成功，非0代表失败）。
    """
    build_dir = "build"
    # 创建构建目录
    if not run_command(["mkdir", "-p", build_dir]): return -1 
    # 运行CMake来配置项目
    if not run_command(["cmake", "-S", ".", "-B", build_dir]): return -1 
    # 编译项目
    if not run_command(["cmake", "--build", build_dir]): return -1 
    
    test_executable = os.path.join(build_dir, "run_tests")
    print(f"--- Running tests: {test_executable} ---")
    test_result = subprocess.run([test_executable], capture_output=True, text=True)
    print("--- Test Output ---\n" + test_result.stdout)
    return test_result.returncode

def main():
    """主逻辑函数"""
    # [修改] 问题五：明确FAIL_TO_PASS和PASS_TO_PASS的逻辑
    report = {
        "FAIL_TO_PASS": {"status": "PENDING", "details": ""},
        "PASS_TO_PASS": {"status": "SKIPPED", "details": "PASS_TO_PASS test not implemented in this scenario."}
    }

    # --- FAIL_TO_PASS 阶段 ---
    print("\n=== STAGE: FAIL_TO_PASS Verification ===\n")
    
    # 1. 应用测试补丁
    # [修改] 问题三：使用 git apply
    if not run_command(["git", "apply", "/testbed/test.patch"]):
        report["FAIL_TO_PASS"]["status"] = "ERROR"
        report["FAIL_TO_PASS"]["details"] = "Failed to apply test.patch"
        return report

    # 2. 运行测试，预期失败 (FAIL)
    if build_and_test() == 0:
        report["FAIL_TO_PASS"]["status"] = "FAILED"
        report["FAIL_TO_PASS"]["details"] = "Test passed unexpectedly before applying the code fix."
        return report
        
    print("\n--- Correctly FAILED before fix ---")

    # 3. 应用代码修复补丁
    if not run_command(["git", "apply", "/testbed/code.patch"]):
        report["FAIL_TO_PASS"]["status"] = "ERROR"
        report["FAIL_TO_PASS"]["details"] = "Failed to apply code.patch"
        return report

    # 4. 运行测试，预期成功 (PASS)
    if build_and_test() != 0:
        report["FAIL_TO_PASS"]["status"] = "FAILED"
        report["FAIL_TO_PASS"]["details"] = "Test still failed after applying the code fix."
        return report

    print("\n--- Correctly PASSED after fix ---")
    
    report["FAIL_TO_PASS"]["status"] = "SUCCESS"
    report["FAIL_TO_PASS"]["details"] = "Test correctly failed before the fix and passed after the fix."
    
    return report

if __name__ == "__main__":
    # 关于问题四的说明：
    # 这里的 code.patch 和 test.patch 是我们为演示而制作的。
    # 在实际任务中，应使用项目方提供的、真实的标注文件。
    final_report = main()
    # [修改] 将报告文件也输出到 /testbed 目录，这样我们在本地才能看到它
    with open("/testbed/report.json", "w") as f:
        json.dump(final_report, f, indent=4)
    
    print("\n--- Final Report ---")
    print(json.dumps(final_report, indent=4))