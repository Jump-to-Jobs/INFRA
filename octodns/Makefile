.PHONY: install plan-test apply-test clean

install:
	python -m pip install -r requirements.txt

plan-test:
	@if [ -z "$$METANAME_ACCOUNT_REF" ] && [ -z "$$METANAME_ACCOUNT_REF_REF" ]; then \
		echo "Set the Metaname secrets (see env/metaname-test.env.example) before running plan-test."; \
		exit 1; \
	fi
	octodns-validate --config-file configs/metaname.test.yaml
	octodns-sync --config-file configs/metaname.test.yaml

apply-test:
	@if [ -z "$$METANAME_ACCOUNT_REF" ] && [ -z "$$METANAME_ACCOUNT_REF_REF" ]; then \
		echo "Set the Metaname secrets (see env/metaname-test.env.example) before running apply-test."; \
		exit 1; \
	fi
	octodns-sync --config-file configs/metaname.test.yaml --doit

clean:
	rm -rf .venv/ .pytest_cache/ .mypy_cache/ .ruff_cache/
