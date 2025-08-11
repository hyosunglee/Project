{ pkgs }:
{
  deps = [
    pkgs.python311
    pkgs.python311Packages.pip

    # Web / API
    pkgs.python311Packages.flask
    pkgs.python311Packages.requests
    pkgs.python311Packages.beautifulsoup4
    pkgs.python311Packages.pydantic
    pkgs.python311Packages.apscheduler

    # ML stack
    pkgs.python311Packages.numpy
    pkgs.python311Packages.scipy
    pkgs.python311Packages.pandas
    pkgs.python311Packages.scikit-learn
    pkgs.python311Packages.joblib
  ];
}
