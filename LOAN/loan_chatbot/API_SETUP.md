# 🔑 API 키 설정 가이드

## Google Gemini API 키 발급

1. [Google AI Studio](https://makersuite.google.com/app/apikey) 접속
2. 새 API 키 생성
3. API 키 복사

## 설정 방법

### 1. config.yaml 파일 생성
```bash
cp config_template.yaml config.yaml
```

### 2. API 키 입력
`config.yaml` 파일을 열고 다음 부분을 수정:
```yaml
gemini:
  api_key: "여기에_실제_API_키_입력"
```

### 3. 보안 주의사항
- ⚠️ **절대** config.yaml 파일을 GitHub에 업로드하지 마세요
- .gitignore에 config.yaml이 포함되어 있는지 확인하세요
- API 키는 개인 정보이므로 공유하지 마세요

## 환경변수 설정 (대안)

config.yaml 대신 환경변수로도 설정 가능합니다:

```bash
# Windows
set GEMINI_API_KEY=your_api_key_here

# Linux/Mac
export GEMINI_API_KEY=your_api_key_here
```