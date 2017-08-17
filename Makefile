PUBLIC_FOLDER = ./public


runserver:
	@cd $(PUBLIC_FOLDER) && python -m SimpleHTTPServer

.PHONY=clean
clean:
	@rm -f .klasses.json
	@rm -rf $(PUBLIC_FOLDER)/*
	@mkdir -p $(PUBLIC_FOLDER)/static
	@echo "Cleaning done."

.PHONY=collect_static
collect_static:
	@echo "Collecting static..."
	@cp -r static $(PUBLIC_FOLDER)/

.PHONY=index_generator_for_version
generate_index_for_version:
	@./bin/generate_index.py

.PHONY=build_for_version
build_for_version:
	@./bin/compile_static.py

build_local:
	@make clean
	@make collect_static
	@make generate_index_for_version
	@make build_for_version

build:
	@make clean
	@make collect_static
	@tox
