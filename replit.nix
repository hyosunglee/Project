{ pkgs }: {
  deps = [
    (pkgs.python311.withPackages (ps: with ps; [
      pip
      flask
      requests
      beautifulsoup4
      pydantic
      apscheduler
      numpy
      scipy
      pandas
      scikit-learn
      joblib
    ]))
  ];
  env = {
    PYTHON_BIN = "${pkgs.python311}/bin/python3.11";
  };
}

