xelatex -output-directory /tmp/ build/$1.tex #> /dev/null 2>&1
cp /tmp/$1.pdf ./build/$1.pdf
#xdg-open ./build/$1.pdf > /dev/null 2>&1
