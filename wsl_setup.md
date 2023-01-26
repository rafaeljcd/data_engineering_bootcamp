### Since the virtual env in the pycharm doesn't automatically activate, there is a need for alternative to automatically activate it

[Source](https://intellij-support.jetbrains.com/hc/en-us/community/posts/360004168199-Unable-to-start-virtual-environment-virtualenv-in-wsl-in-integrated-terminal)

```shell
nano ~/.bashrc
```

Add this at the very end

```shell
if [ -n "$ACTIVATE_VENV" ]; then . "$ACTIVATE_VENV"; fi
```

Afterwards, we must add an environmental variable `ACTIVATE_VENV` with the path
to the `venv`

Go to the File > Settings > Tools > Terminal > Click the button next to Environmental variables

And then edit it with the `venv path`

![](https://i.imgur.com/WxbvDis.png)

And now restart the terminal

![](https://i.imgur.com/PKG7Btu.png)