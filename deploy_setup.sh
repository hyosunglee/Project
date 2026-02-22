#!/bin/bash
# ================================================================
#  Self-Learning API — MacOS 자동 배포 스크립트
#  사용법: chmod +x deploy_setup.sh && ./deploy_setup.sh
# ================================================================

set -e  # 에러 발생 시 즉시 중단

# ── 색상 출력 헬퍼 ──────────────────────────────────────────────
RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'
BLUE='\033[0;34m'; BOLD='\033[1m'; NC='\033[0m'

info()    { echo -e "${BLUE}[INFO]${NC} $1"; }
success() { echo -e "${GREEN}[✅]${NC} $1"; }
warn()    { echo -e "${YELLOW}[⚠️]${NC} $1"; }
error()   { echo -e "${RED}[❌]${NC} $1"; exit 1; }
step()    { echo -e "\n${BOLD}━━━ $1 ━━━${NC}"; }

# ── 프로젝트 경로 설정 ──────────────────────────────────────────
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="${1:-$SCRIPT_DIR}"  # 인수로 경로 전달 가능

echo -e "${BOLD}"
echo "╔════════════════════════════════════════╗"
echo "║   Self-Learning API 자동 배포 스크립트  ║"
echo "║   MacOS 전용                            ║"
echo "╚════════════════════════════════════════╝"
echo -e "${NC}"
info "프로젝트 경로: $PROJECT_DIR"


# ================================================================
# STEP 0 — 필수 도구 확인 및 자동 설치
# ================================================================
step "STEP 0: 필수 도구 확인"

# Homebrew
if ! command -v brew &>/dev/null; then
    info "Homebrew 설치 중..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    success "Homebrew 설치 완료"
else
    success "Homebrew 확인됨"
fi

# Git
if ! command -v git &>/dev/null; then
    info "Git 설치 중..."
    brew install git
fi
success "Git: $(git --version)"

# GitHub CLI
if ! command -v gh &>/dev/null; then
    info "GitHub CLI 설치 중..."
    brew install gh
    success "GitHub CLI 설치 완료"
else
    success "GitHub CLI: $(gh --version | head -1)"
fi

# Render CLI
if ! command -v render &>/dev/null; then
    info "Render CLI 설치 중..."
    brew install render
    success "Render CLI 설치 완료"
else
    success "Render CLI 확인됨"
fi

# Docker Desktop 확인 (설치는 수동 안내)
if ! command -v docker &>/dev/null; then
    warn "Docker Desktop이 없습니다."
    warn "https://www.docker.com/products/docker-desktop/ 에서 설치 후 재실행하세요."
    open "https://www.docker.com/products/docker-desktop/"
    exit 1
else
    success "Docker: $(docker --version)"
fi

# jq (JSON 파싱용)
if ! command -v jq &>/dev/null; then
    brew install jq
fi
success "jq 확인됨"


# ================================================================
# STEP 1 — GitHub 로그인 확인
# ================================================================
step "STEP 1: GitHub 로그인"

if ! gh auth status &>/dev/null; then
    info "GitHub 로그인이 필요합니다..."
    gh auth login
fi
GITHUB_USER=$(gh api user --jq '.login')
success "GitHub 로그인됨: $GITHUB_USER"


# ================================================================
# STEP 2 — 프로젝트 디렉토리로 이동 및 배포 파일 복사
# ================================================================
step "STEP 2: 배포 파일 설치"

cd "$PROJECT_DIR"

# .github/workflows 폴더 생성
mkdir -p .github/workflows

# 이 스크립트와 같은 폴더에 있는 배포 파일들 복사
DEPLOY_FILES_DIR="$SCRIPT_DIR"

files_to_copy=(
    "Dockerfile"
    "Dockerfile.worker"
    "render.yaml"
    "requirements.txt"
)

for f in "${files_to_copy[@]}"; do
    if [ -f "$DEPLOY_FILES_DIR/$f" ]; then
        cp "$DEPLOY_FILES_DIR/$f" "$PROJECT_DIR/$f"
        success "$f 복사 완료"
    else
        warn "$f 파일이 없습니다 — 스킵"
    fi
done

# GitHub Actions workflow
if [ -f "$DEPLOY_FILES_DIR/.github/workflows/deploy.yml" ]; then
    cp "$DEPLOY_FILES_DIR/.github/workflows/deploy.yml" \
       "$PROJECT_DIR/.github/workflows/deploy.yml"
    success "deploy.yml 복사 완료"
fi


# ================================================================
# STEP 3 — Git push
# ================================================================
step "STEP 3: GitHub push"

cd "$PROJECT_DIR"

git add .
git status --short

read -rp "위 변경사항을 push하시겠습니까? (y/n): " CONFIRM
if [[ "$CONFIRM" =~ ^[Yy]$ ]]; then
    git commit -m "feat: render 자동 배포 설정 추가 [$(date '+%Y-%m-%d %H:%M')]"
    git push origin main
    success "GitHub push 완료"
else
    warn "Push 스킵됨 — 나중에 수동으로 push하세요"
fi


# ================================================================
# STEP 4 — Render 로그인 및 서비스 생성
# ================================================================
step "STEP 4: Render 배포"

# Render CLI 로그인
if ! render whoami &>/dev/null 2>&1; then
    info "Render 로그인 중... (브라우저가 열립니다)"
    render login
fi
success "Render 로그인 확인됨"

info "render.yaml 기반으로 서비스 배포 중..."
info "첫 빌드는 torch 때문에 15~25분 걸립니다. 기다려주세요."

# Render Blueprint 배포
REPO_URL="https://github.com/$GITHUB_USER/Project"
info "연결 레포: $REPO_URL"

# 브라우저로 Render Blueprint 페이지 열기 (CLI가 blueprint 미지원 시 대안)
RENDER_BLUEPRINT_URL="https://dashboard.render.com/select-repo?type=blueprint"
info "Render 대시보드에서 레포를 선택하세요."
open "$RENDER_BLUEPRINT_URL"

echo ""
echo -e "${YELLOW}브라우저에서 다음 순서로 진행하세요:${NC}"
echo "  1. 'hyosunglee/Project' 선택"
echo "  2. 'render.yaml detected' 확인 후 Apply 클릭"
echo "  3. 두 서비스 생성 확인:"
echo "     - self-learning-api (Web)"
echo "     - self-learning-loop (Worker)"
echo ""
read -rp "Render 서비스 생성 완료 후 Enter를 누르세요..."


# ================================================================
# STEP 5 — Deploy Hook URL 수집 & GitHub Secrets 자동 등록
# ================================================================
step "STEP 5: GitHub Secrets 자동 등록"

echo ""
echo -e "${YELLOW}Render 대시보드에서 Deploy Hook URL을 복사하세요:${NC}"
echo "  self-learning-api → Settings → Deploy Hook"
echo ""
read -rp "API Deploy Hook URL 붙여넣기: " HOOK_API

echo ""
echo "  self-learning-loop → Settings → Deploy Hook"
echo ""
read -rp "Worker Deploy Hook URL 붙여넣기: " HOOK_WORKER

# GitHub Secrets 자동 등록
cd "$PROJECT_DIR"
gh secret set RENDER_DEPLOY_HOOK_API --body "$HOOK_API"
success "RENDER_DEPLOY_HOOK_API 등록 완료"

gh secret set RENDER_DEPLOY_HOOK_WORKER --body "$HOOK_WORKER"
success "RENDER_DEPLOY_HOOK_WORKER 등록 완료"


# ================================================================
# STEP 6 — 최종 헬스체크
# ================================================================
step "STEP 6: 배포 확인"

info "Render 빌드 완료를 기다리는 중..."
info "약 2분 후 헬스체크를 시도합니다..."
sleep 120

API_URL="https://self-learning-api.onrender.com"

MAX_RETRY=10
for i in $(seq 1 $MAX_RETRY); do
    HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" "$API_URL/healthz" || echo "000")
    if [ "$HTTP_CODE" == "200" ]; then
        success "헬스체크 통과! (시도 $i/$MAX_RETRY)"
        break
    else
        warn "헬스체크 대기 중... ($i/$MAX_RETRY) — 응답코드: $HTTP_CODE"
        sleep 30
    fi
done

if [ "$HTTP_CODE" != "200" ]; then
    warn "헬스체크 미완료 — 빌드가 아직 진행 중일 수 있습니다"
    warn "수동 확인: curl $API_URL/healthz"
fi


# ================================================================
# 완료 요약
# ================================================================
echo ""
echo -e "${GREEN}${BOLD}"
echo "╔════════════════════════════════════════╗"
echo "║            🚀 배포 완료!               ║"
echo "╚════════════════════════════════════════╝"
echo -e "${NC}"
echo -e "  API 주소:     ${BLUE}$API_URL${NC}"
echo -e "  헬스체크:     ${BLUE}$API_URL/healthz${NC}"
echo -e "  GitHub:       ${BLUE}https://github.com/$GITHUB_USER/Project/actions${NC}"
echo ""
echo "  다음 push 시 자동 배포가 트리거됩니다."
echo ""

# 빠른 테스트 명령어 출력
echo -e "${BOLD}테스트 명령어:${NC}"
echo "  curl $API_URL/healthz"
echo "  curl -X POST $API_URL/seed?n=10"
echo "  curl -X POST $API_URL/train"

