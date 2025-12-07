[app]
title = Nikita AI
package.name = nikita_ai
package.domain = org.test
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.2

# ВАЖНО: Добавили openai и requests
requirements = python3,kivy==2.2.1,kivymd==1.1.1,pillow,openai,requests,urllib3,chardet,idna

orientation = portrait
fullscreen = 0
android.permissions = INTERNET
android.archs = arm64-v8a, armeabi-v7a
android.allow_backup = True

[buildozer]
log_level = 2
warn_on_root = 1
