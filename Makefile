BUILD_DIR = build
PDF_NAME = cv

BUILD_PY = build.py
DATA_YML = cv_data.yml
TEMPLATE_TEX = template/cv.tex
RENDERED_TEX = build/rendered.tex

IN_ENV = if [ -e .venv/bin/activate ]; then . .venv/bin/activate; fi;

$(PDF_NAME).pdf: $(RENDERED_TEX)
	cd $(BUILD_DIR) && pdflatex -jobname=$(PDF_NAME) -output-directory=. ../$^ 
	cp $(BUILD_DIR)/$(PDF_NAME).pdf .

$(RENDERED_TEX): $(BUILD_DIR) $(TEMPLATE_TEX) $(DATA_YML) $(BUILD_PY) Makefile
	$(IN_ENV) python3 $(BUILD_PY) $(TEMPLATE_TEX) $(DATA_YML) > $@

$(BUILD_DIR):
	mkdir $@
	
env:
	python3.8 -m venv .venv
	$(IN_ENV) pip install --upgrade pip
	$(IN_ENV) pip install pandoc nbconvert pypandoc pyyaml

packages:
	sudo apt-get install -y python3.8-venv pandoc

clean:
	rm -rf $(BUILD_DIR) cv.pdf