@rem git ls-remote https://github.com/ned14/outcome refs/heads/develop
@rem git ls-remote https://github.com/dotnet/runtime refs/heads/master

@rem git ls-remote https://github.com/baldurk/renderdoc origin HEAD
@rem git ls-remote --symref https://github.com/baldurk/renderdoc origin HEAD
@rem ref: refs/heads/v1.x    HEAD
@rem c9c3e0f64619ea26e03d091b4c389353abf0e928        HEAD

git ls-remote %1 %2 %3 > commit.txt