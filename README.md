# paste-agent

paste-agent는 ChatGPT, Claude, Gemini 등 원하는 AI와 연동하여 코드를 수정할 수 있는 **자율 코딩 에이전트**입니다.  
API 연동 없이, 웹상에서 AI가 출력한 명령어를 복사해서 붙여넣는 것만으로 코드를 수정할 수 있습니다.


## 사용 가능 명령어
- writefolder - 폴더를 생성합니다.  
- writefile - 파일을 생성합니다.  
- edit - 파일의 기존 내용을 새 문자열로 대치합니다.  
- readfolder - 폴더의 내용을 읽습니다.  
- readfile - 파일의 내용을 읽습니다.  
- searchtext - 현재 폴더에서 특정 문자열을 검색합니다.  
- glob - 현재 폴더에서 패턴과 일치하는 파일을 찾습니다.  
- shell - powershell 명령을 실행합니다.

## 장점
- 코드의 수정 위치를 몰라도 코드를 쉽게 수정할 수 있습니다.
- AI로 코드를 보여주기만 하지 않고 코드를 실제로 작성할 수 있습니다

## 단점
- 복사 후 붙여넣기 과정이 필요해 복잡한 프로젝트는 번거로울 수 있습니다.



## 사용방법
1. 소스 코드를 다운받은 후 압축을 해제하세요.
2. AI 모델에게 prompts.txt의 내용을 보내세요. AI 모델이 "알겠습니다." 라고 답합니다.
3. agent.exe를 실행하세요.
4. 요청한 후 AI 모델이 응답을 출력하면 복사 버튼 (<img width="17" height="19" alt="image" src="https://github.com/user-attachments/assets/4e3d428b-b7f6-4a8c-aab2-d7dfc93b0f84" />)을 눌러서 출력을 복사하세요.
5. agent.exe에 Ctrl+V로 붙여넣기 한 후 엔터를 누르세요.
6. 출력 결과를 AI 모델에게 입력 후 전송하세요.
7. 위 과정을 반복하세요.
