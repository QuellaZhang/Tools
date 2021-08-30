@rem git ls-remote https://github.com/ned14/outcome refs/heads/develop
@rem git ls-remote https://github.com/dotnet/runtime refs/heads/master
git ls-remote %1 %2 > commit.txt