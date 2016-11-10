.PHONY = docs-serve docs-build

# =========== MkDocs ================= #
docs-serve:
	@mkdocs serve

docs-build:
	@mkdocs build
