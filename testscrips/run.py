import sys
import subprocess
sys.path.append('../../')
# 判断是否是windows系统，是True,否False
WIN = sys.platform.startswith('win')

def main():
   """主函数"""

   steps = [
       # 激活虚拟环境，暂时不考虑
       # "venv\\Script\\activate" if WIN else "source venv/bin/activate",

       # 生成allure原始报告到指定目录下，使用generate命令导出HTML报告到新的目录
       # --alluredir file_path 指定存储目录
       # --clean-alluredir 清除allure-results历史数据
       # 程序核心入口
       "pytest -l  --alluredir ../allure-results --clean-alluredir",
       "copy ..\etc\environment.properties ..\\results\environment.properties",
       # 使用generate命令导出HTML报告到新的目录
       "allure generate ../allure-results -c -o ../allure-report",
       # 使用open命令在浏览器中打开HTML报告
       "allure open ../allure-report"
   ]
   n = 0
   for step in steps:
       n += 1
       print(n)
       '''
       subprocess是Python与系统交互的一个库，该模块允许生成新进程，连接到它们的输入/输出/错误管道，并获取它们的返回代码
       call命令：从一个批处理程序调用另一个批处理程序，并且不终止父批处理程序，后面接 执行脚本的路径和名称
       args：表示要执行的命令。必须是一个字符串，字符串参数列表
       shell：如果该参数为 True，将通过操作系统的 shell 执行指定的命令
       '''
       subprocess.run("call " + step if WIN else step, shell=True)



if __name__ == "__main__":
   main()