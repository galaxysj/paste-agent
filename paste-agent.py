ㅇimport re
import subprocess
import os
import urllib.parse
import glob

def run_agent():
    
    while True:
        user_input = input("> ").strip()
        if user_input == "quit": break
            
        commands = re.findall(r'\{(\w+)\((.*?)\)\}', user_input, re.DOTALL)
        if not commands: continue

        for cmd_name, args_str in commands:
            try:
                # 더 정교한 인자 파싱 (값 내부에 ;가 있어도 동작하도록)
                args = {}
                raw_pairs = re.findall(r'(\w+)\s*=\s*"(.*?)"(?=;|$|\s)', args_str, re.DOTALL)
                for k, v in raw_pairs:
                    # \n은 줄바꿈으로, \t는 공백 4칸으로 변환하여 들여쓰기 유지
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

            except Exception as e:
                print(f"오류: {str(e)}")

if __name__ == "__main__":
    run_agent()
