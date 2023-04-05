# -*- python -*-
#
# Copyright 2022 Stéphane Caron

load("@bazel_tools//tools/build_defs/repo:git.bzl", "git_repository")

def upkie_description_repository():
    """
    Clone repository from GitHub and make its targets available for binding.
    """
    git_repository(
        name = "upkie_description",
        remote = "https://github.com/tasts-robots/upkie_description",
        commit = "cbba6ddad34f640a09e436d76147494aee687a5e",
        shallow_since = "1652897584 +0200"
    )
