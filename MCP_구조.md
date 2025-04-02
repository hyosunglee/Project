


/mcp_agent/
├── main.py             # 루프 컨트롤러 진입점
├── goal_manager.py     # 목표 관리
├── planner.py          # 작업 계획 수립 (LLM 호출)
├── executor.py         # MCP 클라이언트 + tool 실행
├── reflector.py        # 결과 분석 및 루프 반복 판단
├── memory/
│   └── history.json    # 이전 작업 로그
└── tools/
    └── mcp_client.py   # MCP 서버 인터페이스