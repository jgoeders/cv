BUILD_DIR = build
PDF_NAME = cv

TEMPLATE_TEX = template/cv.tex
RENDERED_TEX = build/rendered.tex


$(PDF_NAME).pdf: $(RENDERED_TEX)
	cd $(BUILD_DIR) && pdflatex -jobname=$(PDF_NAME) ../$^ 
	cp $(BUILD_DIR)/$(PDF_NAME).pdf .

$(RENDERED_TEX): $(BUILD_DIR)
	python3 build.py $(TEMPLATE_TEX) > $@

$(BUILD_DIR):
	mkdir $@
	