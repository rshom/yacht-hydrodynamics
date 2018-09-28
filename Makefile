## Put this Makefile in your project directory---i.e., the directory
## containing the paper you are writing. Assuming you are using the
## rest of the toolchain here, you can use it to create .html, .tex,
## and .pdf output files (complete with bibliography, if present) from
## your markdown file. 
## -	Change the paths at the top of the file as needed.
## -	Using `make` without arguments will generate html, tex, and pdf 
## 	output files from all of the files with the designated markdown
##	extension. The default is `.md` but you can change this. 
## -	You can specify an output format with `make tex`, `make pdf` or 
## - 	`make html`. 
## -	Doing `make clean` will remove all the .tex, .html, and .pdf files 
## 	in your working directory. Make sure you do not have files in these
##	formats that you want to keep!

## Extension (e.g. md, markdown, mdown).
## for all markdown files in the directory
MEXT = pmd

## Variable for all markdown files in the working directory
SRC = $(wildcard *.$(MEXT))

## Location of Pandoc support files.
PREFIX = /home/russ/.pandoc

## Location of your working bibliography file
#BIB = /home/russ/Dropbox/2intel/bibs/pandoc.bib
BIB = ./ref.bib

## CSL stylesheet (located in the csl folder of the PREFIX directory).
CSL = apsa


## Dependencies: .pdf depends on .pmd, .html depends on .pmd, etc
PDFS=$(SRC:.pmd=.pdf)
HTML=$(SRC:.pmd=.html)
TEX=$(SRC:.pmd=.tex)
DOCX=$(SRC:.pmd=.docx)

## Rules -- make all, make pdf, make html: first call the `clean` rule (see below),
## then the filetype rule.
all:	$(PDFS) $(HTML) $(TEX) $(DOCX)

pdf:	clean $(PDFS)
html:	clean $(HTML)
tex:	clean $(TEX)
docx:	clean $(DOCX)

## The actual commands.
## How to produce a .html file corresponding to each .pmd in the directory. Run when
## `make html` is the command.
%.html:	%.pmd
	pweave -f pandoc $<
	pandoc --filter pandoc-crossref --filter pandoc-citeproc --bibliography=$(BIB) -s -o $@ $*.md
	rm -f $*.md

## Same goes for the other file types
%.tex:	%.pmd
	pweave -f pandoc $<
	pandoc --filter pandoc-crossref --filter pandoc-citeproc --bibliography=$(BIB) -o $@ $*.md
	rm -f $*.md

%.pdf:	%.pmd
	pweave -f pandoc $<
	pandoc --filter pandoc-crossref --filter pandoc-citeproc --bibliography=$(BIB) -s -o $@ $*.md
	rm -f $*.md

%.docx:	%.pmd
	pweave -f pandoc $<	
	pandoc --filter pandoc-crossref --filter pandoc-citeproc --bibliography=$(BIB) -o $@ $*.md
	rm -f $*.md


clean:
	rm -f *.html *.pdf *.tex *.aux *.log *.docx
	rm -f figures/*

.PHONY: clean

# Below is the original code which I stole
# It includes stuff for templates which I am not yet using

# ## The actual commands.
# ## How to produce a .html file corresponding to each .pmd in the directory. Run when
# ## `make html` is the command.
# %.html:	%.pmd
# 	pandoc -r markdown+simple_tables+table_captions+yaml_metadata_block -w html -S --template=$(PREFIX)/templates/html.template --css=$(PREFIX)/marked/kultiad-serif.css --filter pandoc-crossref --filter pandoc-citeproc --csl=$(PREFIX)/csl/$(CSL).csl --bibliography=$(BIB) -o $@ $<


# ## Same goes for the other file types
# %.tex:	%.pmd
# 	pandoc -r markdown+simple_tables+table_captions+yaml_metadata_block --listings -w latex -s -S --latex-engine=pdflatex --template=$(PREFIX)/templates/latex.template --filter pandoc-crossref --filter pandoc-citeproc --csl=$(PREFIX)/csl/ajps.csl --filter pandoc-citeproc-preamble --bibliography=$(BIB) -o $@ $<


# %.pdf:	%.pmd
# 	pandoc -r markdown+simple_tables+table_captions+yaml_metadata_block --listings -s -S --latex-engine=pdflatex --template=$(PREFIX)/templates/latex.template --filter pandoc-crossref --filter pandoc-citeproc --csl=$(PREFIX)/csl/$(CSL).csl --filter pandoc-citeproc-preamble --bibliography=$(BIB) -o $@ $<

# %.docx:	%.pmd
# 	pandoc -r markdown+simple_tables+table_captions+yaml_metadata_block -s -S --filter pandoc-crossref --csl=$(PREFIX)/csl/$(CSL).csl --bibliography=$(BIB) -o $@ $<


# clean:
# 	rm -f *.html *.pdf *.tex *.aux *.log *.docx

# .PHONY: clean
