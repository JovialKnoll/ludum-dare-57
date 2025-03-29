cd ..
# cleanup old build
rm -r dist
# use virtual environment
src/venv/Scripts/activate.ps1
# get pyinstaller
pip install pyinstaller
# create spec file
pyinstaller --clean -ywF -i src/icon.ico -n REPLACE src/main.py
# build exe
pyinstaller -y REPLACE.spec
# windows setup
mkdir dist/REPLACE
mv dist/REPLACE.exe dist/REPLACE/REPLACE.exe
# copy in assets
cp -r src/assets dist/REPLACE/assets
# copy in license
cp LICENSE.txt dist/REPLACE/
# copy in readme
cp README.txt dist/REPLACE/
# cleanup
deactivate
rm -r build
rm REPLACE.spec
cd scripts
