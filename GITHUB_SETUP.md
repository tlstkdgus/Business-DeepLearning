# 🚀 GitHub 업로드 가이드

## 1. Git 저장소 초기화
```bash
cd "c:\Users\tlstk\Desktop\대학 수업\비즈니스 딥러닝"
git init
```

## 2. 원격 저장소 연결
```bash
git remote add origin https://github.com/tlstkdgus/Business-DeepLearning.git
```

## 3. 첫 번째 커밋
```bash
git add .
git commit -m "Initial commit: Business Deep Learning projects"
```

## 4. GitHub에 푸시
```bash
git branch -M main
git push -u origin main
```

## ⚠️ 주의사항

### 업로드 전 확인
- [ ] config.yaml 파일이 .gitignore에 포함되어 있는지 확인
- [ ] API 키가 포함된 파일들이 제외되어 있는지 확인
- [ ] 불필요한 파일들 (__pycache__, venv 등)이 제외되어 있는지 확인

### API 키 보안
- 실제 API 키는 절대 GitHub에 업로드하지 마세요
- config_template.yaml을 사용하여 다른 사용자가 설정할 수 있도록 안내하세요

## 📋 추가 명령어

### 새 변경사항 추가
```bash
git add .
git commit -m "Update: 설명"
git push
```

### 브랜치 생성 (선택사항)
```bash
git checkout -b feature/new-feature
git push -u origin feature/new-feature
```

### 상태 확인
```bash
git status
git log --oneline
```