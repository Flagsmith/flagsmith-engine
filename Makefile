.PHONY: sync-engine-test-data

sync-engine-test-data:
	cd tests/engine_tests/engine-test-data && git fetch --tags && git checkout $$(git config -f ../../../.gitmodules submodule.tests/engine_tests/engine-test-data.branch)
