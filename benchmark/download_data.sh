# Get cookie file and html code with curl.
# Pipe html to grep and sed and search for file name.
# Get confirm code from cookie file with awk.
# Finally download file with cookie enabled, confirm code and filename.

ggID='0BzQ6rtO2VN95bndCZDdpdXJDV1U'
ggURL='https://drive.google.com/uc?export=download'
filename="$(curl -sc /tmp/gcokie "${ggURL}&id=${ggID}" | grep -o '="uc-name.*</span>' | sed 's/.*">//;s/<.a> .*//')"
getcode="$(awk '/_warning_/ {print $NF}' /tmp/gcokie)"
curl -Lb /tmp/gcokie "${ggURL}&confirm=${getcode}&id=${ggID}" -o "${filename}"
unzip $filename
rm $filename
