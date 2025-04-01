
```
ai_agent/
│
├── main.py                     # 전체 실행 컨트롤러 (FastAPI or CLI)
├── config.py                   # 설정 파일 (모델, DB, 크롤링 옵션 등)
│
├── agents/
│   ├── task_manager.py         # 전체 플로우 관리
│   ├── web_query.py            # 자연어 → 검색 쿼리 생성
│   ├── crawler.py              # Playwright 기반 크롤러
│   ├── data_cleaner.py         # HTML → 정제 Text
│   ├── llm_processor.py        # Local LLM 호출 및 요약
│   ├── structurer.py           # JSON / YAML 형태 구조화
│   └── action_executor.py      # 응답 생성, 액션 실행
│
├── models/
│   ├── local_llm.py            # Ollama / LLaMA / Mistral 모델 연결
│   └── embedding.py            # 텍스트 임베딩 처리
│
├── db/
│   ├── vector_store.py         # Chroma / FAISS 저장 로직
│   ├── metadata_store.py       # MongoDB or SQLite 메타 저장
│   └── schema.py               # DB 구조 정의
│
├── utils/
│   ├── logger.py               # 로깅 관리
│   ├── html_parser.py          # BeautifulSoup / BoilerPy3
│   ├── text_utils.py           # 텍스트 정제 공통 유틸
│   └── scheduler.py            # 정기 크롤링 스케줄러
│
└── tests/
    └── test_pipeline.py        # 핵심 파이프라인 테스트
```