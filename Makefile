BUILD_DIR=build
PDF_NAME=jgoeders_cv

BUILD_PY=build.py
DATA_YML=cv_data.yml
TEMPLATE_TEX=template/cv.tex
RENDERED_TEX=build/rendered.tex

IN_ENV=. .venv/bin/activate;

$(PDF_NAME).pdf: .venv/bin/activate $(RENDERED_TEX) 
	cd $(BUILD_DIR) && pdflatex -jobname=$(PDF_NAME) -output-directory=. ../$(word 2, $^)
	cp $(BUILD_DIR)/$(PDF_NAME).pdf .

$(RENDERED_TEX): $(BUILD_DIR) $(TEMPLATE_TEX) $(DATA_YML) $(BUILD_PY)
	$(IN_ENV) python3 $(BUILD_PY) $(TEMPLATE_TEX) $(DATA_YML) > $@

$(BUILD_DIR):
	mkdir $@
	
env: .venv/bin/activate
	sudo apt-get install -y pandoc

.venv/bin/activate: requirements.txt
	python3 -m venv .venv
	$(IN_ENV) pip install --upgrade pip
	$(IN_ENV) pip install -r requirements.txt

clean:
	rm -rf $(BUILD_DIR) cv.pdf