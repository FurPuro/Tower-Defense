rmdir "dist\main\" /s /q
pyinstaller main.spec
move "dist\main\_internal\assets" "dist\main\"