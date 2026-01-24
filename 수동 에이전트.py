import re
import subprocess
import os
import urllib.parse
import glob

def run_agent():
    print("Gemini Code Agent 대체 툴을 시작합니다. (종료하려면 'quit' 입력)")
    
    while True:
        user_input = input("> ").strip()
        
        if user_input == "quit":
            break
            
        # 명령어 추출: {명령(인자)}
        commands = re.findall(r'\{(\w+)\((.*?)\)\}', user_input, re.DOTALL)
        
        if not commands:
            continue

        for cmd_name, args_str in commands:
            try:
                # 개선된 인자 파싱: key="value" 형태를 더 정확하게 추출
                args = {}
                # 세미콜론(;)으로 구분된 인자들을 찾되, 값 내부의 세미콜론은 무시하도록 로직 변경
                raw_pairs = re.findall(r'(\w+)\s*=\s*"(.*?)"(?=;|$|\s)', args_str, re.DOTALL)
                for k, v in raw_pairs:
                    args[k] = v.replace('\\n', '\n')

                # 1. search
                if cmd_name == "search":
                    query = args.get('query', '')
                    url = f"https://www.google.com/search?q={urllib.parse.quote(query)}"
                    result = subprocess.run(['curl', '-s', url], capture_output=True, text=True, shell=True)
                    print(result.stdout)

                # 2. shell
                elif cmd_name == "shell":
                    command = args.get('command', '')
                    result = subprocess.run(['powershell', '-Command', command], capture_output=True, text=True)
                    print(result.stdout if result.stdout else result.stderr)

                # 3. readfolder
                elif cmd_name == "readfolder":
                    folder = args.get('file') or args.get('name') or "."
                    result = subprocess.run(['powershell', 'ls', folder], capture_output=True, text=True)
                    print(result.stdout)

                # 4. edit
                elif cmd_name == "edit":
                    target = args.get('target')
                    old_str = args.get('oldstring')
                    new_str = args.get('newstring')
                    
                    with open(target, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    if content.count(old_str) == 0:
                        print("오류: 기존 문자열을 찾을 수 없습니다.")
                    elif content.count(old_str) > 1:
                        print("오류: 일치하는 내용이 여러 개입니다.")
                    else:
                        new_content = content.replace(old_str, new_str)
                        with open(target, 'w', encoding='utf-8') as f:
                            f.write(new_content)
                        print("완료")

                # 5. readfile
                elif cmd_name == "readfile":
                    name = args.get('file')
                    start = int(args.get('start', 1))
                    end = int(args.get('end', -1))
                    with open(name, 'r', encoding='utf-8') as f:
                        lines = f.readlines()
                        if end == -1: end = len(lines)
                        print("".join(lines[start-1:end]))

                # 6. writefile
                elif cmd_name == "writefile":
                    name = args.get('name')
                    content = args.get('content')
                    if content is None:
                        print("오류: content 내용을 읽지 못했습니다. 형식을 확인하세요.")
                        continue
                    if os.path.exists(name):
                        print(f"오류: '{name}' 파일이 이미 존재합니다.")
                    else:
                        with open(name, 'w', encoding='utf-8') as f:
                            f.write(content)
                        print("완료")

                # 7. glob
                elif cmd_name == "glob":
                    pattern = args.get('pattern', '*')
                    files = glob.glob(pattern)
                    print("\n".join(files))

            except Exception as e:
                print(f"오류: {str(e)}")

if __name__ == "__main__":
    run_agent()
