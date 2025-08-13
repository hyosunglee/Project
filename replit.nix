{ pkgs, ... }:
{
  # 중요: 최신(25_05) 말고 안정 채널로 고정
  channel = "stable-24_11";

  deps = [
    pkgs.python311Full

    # build basics (파이썬 빌드 체인 일관성)
    pkgs.python311Packages.pip
    pkgs.python311Packages.setuptools
    pkgs.python311Packages.wheel

    # Web / API
    pkgs.python311Packages.flask
    pkgs.python311Packages.requests
    pkgs.python311Packages.beautifulsoup4
    pkgs.python311Packages.pydantic
    pkgs.python311Packages.apscheduler

    # ML stack (전부 Nix에서)
    pkgs.python311Packages.numpy
    pkgs.python311Packages.scipy
    pkgs.python311Packages.pandas
    pkgs.python311Packages.scikit-learn
    pkgs.python311Packages.joblib
  ];
}