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
        print("--- stderr ---")
        print(result.stderr)
        print("--- stdout ---")
        print(result.stdout)
        return False
    else:
        print("--- Command executed successfully ---")
        # print(result.stdout) # 如果需要，可以取消这行注释来查看成功命令的输出
        return True

def build_and_test():
    """
    封装了构建和测试C++项目的逻辑。
    返回测试程序的退出代码（0代表成功，非0代表失败）。
    """
    build_dir = "build"
    # 创建构建目录，-p选项表示如果目录已存在也不会报错
    if not run_command(["mkdir", "-p", build_dir]): return -1 
    
    # 运行CMake来配置项目
    if not run_command(["cmake", "-S", ".", "-B", build_dir]): return -1 
    
    # 运行make（或等效的构建命令）来编译项目
    if not run_command(["cmake", "--build", build_dir]): return -1 
    
    # 运行编译出的测试程序
    test_executable = os.path.join(build_dir, "run_tests")
    print(f"--- Running tests: {test_executable} ---")
    test_result = subprocess.run([test_executable], capture_output=True, text=True)
    
    # 打印测试结果
    print("--- Test Output ---")
    print(test_result.stdout)
    if test_result.returncode != 0:
        print("--- Tests FAILED ---")
    else:
        print("--- ALL Tests PASSED ---")
        
    return test_result.returncode

def main():
    """主逻辑函数"""
    report = {
        "project": "C++ Calculator Sample",
        "verification_status": "PENDING",
        "steps": []
    }

    # --- 阶段1: 应用测试补丁并验证测试是否如预期般失败 ---
    print("\n=== STAGE 1: Applying test.patch and expecting failure ===\n")
    if not run_command(["patch", "main.cpp", "test.patch"]):
        report["verification_status"] = "ERROR: Failed to apply test.patch"
        return report
    
    report["steps"].append("Applied test.patch successfully.")
    
    test_return_code_before_fix = build_and_test()
    if test_return_code_before_fix == 0:
        report["verification_status"] = "FAILED: Tests passed BEFORE the code fix. The test patch is likely ineffective."
        return report
    
    report["steps"].append("Tests correctly FAILED before the code fix.")

    # --- 阶段2: 应用代码修复补丁并验证测试是否通过 ---
    print("\n=== STAGE 2: Applying code.patch and expecting success ===\n")
    if not run_command(["patch", "calculator.cpp", "code.patch"]):
        report["verification_status"] = "ERROR: Failed to apply code.patch"
        return report
        
    report["steps"].append("Applied code.patch successfully.")
    
    test_return_code_after_fix = build_and_test()
    if test_return_code_after_fix != 0:
        report["verification_status"] = "FAILED: Tests still failed AFTER the code fix."
        return report

    report["steps"].append("Tests correctly PASSED after the code fix.")
    
    # --- 结论 ---
    print("\n=== Verification successful! ===\n")
    report["verification_status"] = "SUCCESS"
    return report

if __name__ == "__main__":
    final_report = main()
    # 将最终报告写入JSON文件
    with open("report.json", "w") as f:
        json.dump(final_report, f, indent=4)
    
    print("\n--- Final Report ---")
    print(json.dumps(final_report, indent=4))