cd ..
# cleanup old build
rm -r dist
# use virtual environment
src/venv/Scripts/activate.ps1
# get pyinstaller
pip install pyinstaller
# create spec file
pyinstaller --clean -ywF -i src/icon.ico -n DEPTH_CHARGE src/main.py
# build exe
pyinstaller -y DEPTH_CHARGE.spec
# windows setup
mkdir dist/DEPTH_CHARGE
mv dist/DEPTH_CHARGE.exe dist/DEPTH_CHARGE/DEPTH_CHARGE.exe
# copy in assets
cp -r src/assets dist/DEPTH_CHARGE/assets
# copy in license
cp LICENSE.txt dist/DEPTH_CHARGE/
# copy in readme
cp README.txt dist/DEPTH_CHARGE/
# cleanup
deactivate
rm -r build
rm DEPTH_CHARGE.spec
cd scripts
