.PHONY: test install uninstall create clean upload

test:
	@pytest --pep8 -q

install:
	@pip install -e .

unintall:
	@pip uninstall bgm_mal_immigration

create:
	@python setup.py sdist bdist_wheel

clean:
	@rm -rfv ./dist ./build

upload:
	@twine upload -s dist/*
