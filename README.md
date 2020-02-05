# Deploying Machine Learning Models
For the documentation, visit the course on Udemy.

## 1. Virtual environment
It is recommended to use the module `venv` of python to create a virtual environment. In fact, `virtualenv` is deprecated as it can be seen in [https://github.com/pyenv/pyenv-virtualenv/issues/144?fbclid=IwAR24uh0r9J6oGsVygsYchOBBJAuLdQme2NUhLg3Rb0AYVBJdGD_LjpTi6Bg](https://github.com/pyenv/pyenv-virtualenv/issues/144?fbclid=IwAR24uh0r9J6oGsVygsYchOBBJAuLdQme2NUhLg3Rb0AYVBJdGD_LjpTi6Bg).

The creation of a virtual environment is as follows:

```sh
python -m venv env
```

## 2. Setting paths for packages

After setting the virtual environment `env`, setting the paths of the packages to be created in a given project will be through creating a pth file in `env\Lib\site-packages\regression_model.pth` that contains the following lines:

```shell
..\..\..\packages\regression_model
```

## 3. Testing 

In order to test the packages, the package `pytest` is required. Consequently, it can be installed through adding this requirement in the `requirements.txt` file as follows:

```txt
jupyter==1.0.0
matplotlib==3.1.1
pandas==0.25.3
scikit-learn==0.22.1

# for testing
pytest==5.3.5
```
The testing command line is:

```sh
pytest packages/regression_model/tests -W ignore::DeprecationWarning
# ====================================================================== test session starts ======================================================================= 
# platform win32 -- Python 3.7.6, pytest-5.3.5, py-1.8.1, pluggy-0.13.1
# rootdir: C:\Users\999138\Documents\ME
# collected 1 item                                                                                                                                                   

# packages\regression_model\tests\test_predict.py .                                                                                                           [100%] 

# ======================================================================== warnings summary ======================================================================== 
# env\lib\site-packages\sklearn\externals\joblib\__init__.py:15
#   c:\users\999138\documents\me\udemy-deploying-machine-learning-models\env\lib\site-packages\sklearn\externals\joblib\__init__.py:15: FutureWarning: sklearn.externals.joblib is deprecated in 0.21 and will be removed in 0.23. Please import this functionality directly from joblib, which can be installed with: pip install joblib. If this warning is raised when loading pickled models, you may need to re-serialize those models with scikit-learn 0.21+.
#     warnings.warn(msg, category=FutureWarning)

# -- Docs: https://docs.pytest.org/en/latest/warnings.html
# ================================================================== 1 passed, 1 warning in 1.12s ================================================================== 
```

As it can be seen, there is one ignore::FutureWarning that it would be better if we address it. It is this import `import sklearn.externals.joblib` 

**Solving the ignore::FutureWarning**

- Installation of the `joblib` through this command `pip install joblib` (already installed after double checking)
- Modify the file `data_management.py` as follows:

```py
# from sklearn.externals import joblib ## comment this line
import joblib
```



