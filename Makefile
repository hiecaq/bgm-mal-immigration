test:
	@pytest --pep8 -q

install:
	@pip install -e .

unintall:
	@pip uninstall s1acker

create:
	@python setup.py sdist bdist_wheel

clean:
	@rm -rfv ./dist ./build

upload:
	@twine upload -s dist/*
