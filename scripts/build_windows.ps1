cd ..
# cleanup old build
rm -r dist
# use virtual environment
src/venv/Scripts/activate.ps1
# get pyinstaller
pip install pyinstaller
# create spec file
pyinstaller --clean -ywF -i src/icon.ico -n depth-charge src/main.py
# build exe
pyinstaller -y depth-charge.spec
# windows setup
mkdir dist/depth-charge
mv dist/depth-charge.exe dist/depth-charge/depth-charge.exe
# copy in assets
cp -r src/assets dist/depth-charge/assets
# copy in license
cp LICENSE.txt dist/depth-charge/
# copy in readme
cp README.txt dist/depth-charge/
# cleanup
deactivate
rm -r build
rm depth-charge.spec
cd scripts
