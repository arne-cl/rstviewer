# a '-' before a shell command causes make to ignore its exit code (errors)

clean:
	find . -name '*.pyc' -delete
	find . -name ".ipynb_checkpoints" -type d -exec rm -rf {} \;
	find . -name "__pycache__" -type d -exec rm -rf {} \;
	rm -rf .eggs .cache
	rm -rf git_stats
	rm -rf build dist src/rstviewer.egg-info
	rm -rf docs/_build
	rm -rf htmlcov
