import re
import subprocess
import os
import urllib.parse
import glob

def run_agent():
    print("Gemini Code Agent v2.3 (Context Search) 시작. (종료: 'quit')")
    
    while True:
        user_input = input("> ").strip()
        if user_input == "quit": break
            
        commands = re.findall(r'\{(\w+)\((.*?)\)\}', user_input, re.DOTALL)
        if not commands: continue

        for cmd_name, args_str in commands:
            try:
                args = {}
                raw_pairs = re.findall(r'(\w+)\s*=\s*"(.*?)"(?=;|$|\s)', args_str, re.DOTALL)
                for k, v in raw_pairs:
                    args[k] = v.replace('\\n', '\n').replace('\\t', '    ')

                if cmd_name == "writefile":
                    name, content = args.get('name'), args.get('content')
                    if os.path.exists(name):
                        print(f"오류: '{name}' 파일이 이미 존재함")
                    else:
                        with open(name, 'w', encoding='utf-8') as f:
                            f.write(content)
                        print("완료")

                elif cmd_name == "edit":
                    target, old_str, new_str = args.get('target'), args.get('oldstring'), args.get('newstring')
                    with open(target, 'r', encoding='utf-8') as f: content = f.read()
                    if content.count(old_str) != 1:
                        print(f"오류: 일치 개수 {content.count(old_str)}개 (1개여야 함)")
                    else:
                        with open(target, 'w', encoding='utf-8') as f: f.write(content.replace(old_str, new_str))
                        print("완료")

                elif cmd_name == "shell":
                    result = subprocess.run(['powershell', '-Command', args.get('command', '')], capture_output=True, text=True)
                    print(result.stdout if result.stdout else result.stderr)

                elif cmd_name == "readfile":
                    with open(args.get('file'), 'r', encoding='utf-8') as f:
                        lines = f.readlines()
                        start, end = int(args.get('start', 1)), int(args.get('end', -1))
                        if end == -1: end = len(lines)
                        print("".join(lines[start-1:end]))

                elif cmd_name == "readfolder":
                    folder = args.get('file') or args.get('name') or "."
                    print(subprocess.run(['powershell', 'ls', folder], capture_output=True, text=True).stdout)

                elif cmd_name == "glob":
                    print("\n".join(glob.glob(args.get('pattern', '*'))))

                # --- 업그레이드된 searchtext 기능 ---
                elif cmd_name == "searchtext":
                    query = args.get('query')
                    print(f"🔍 '{query}' 주변 맥락 검색 결과:")
                    for file_path in glob.glob('*'):
                        if os.path.isfile(file_path):
                            try:
                                with open(file_path, 'r', encoding='utf-8') as f:
                                    content = f.read()
                                    idx = content.find(query)
                                    if idx != -1:
                                        # 앞뒤 30글자 추출 로직
                                        start = max(0, idx - 30)
                                        end = min(idx + len(query) + 30, len(content))
                                        snippet = content[start:end].replace('\n', ' ') # 가독성 위해 줄바꿈 제거
                                        print(f"📄 {file_path}: ...{snippet}...")
                            except:
                                pass

            except Exception as e:
                print(f"오류: {str(e)}")

if __name__ == "__main__":
    run_agent()
