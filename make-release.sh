echo "The following files are missing or are not checked in:"
hg st
echo "Enter to continue"
read -e YES
echo "The following files are missing from the MANIFEST file:"
cat MANIFEST | sort > sorted-manifest.txt
hg st --clean| sed "s/^C //" | grep -v "^v3" > sorted-allfiles.txt
diff sorted-allfiles.txt sorted-manifest.txt 

