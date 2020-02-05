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

## 4. Processors (i.e. transformers)

A pipeline contains always:
* a set of transformers
* one and only one predictor (which is the `Lasso` in this example of ML algorithm).

The predictor will not be addressed in this section. In stead, the transformers are being addressed.

All the transformers were defined in the the `regression_model.processing.preprocessors`. In order to follow the recommended way of defining the transformer, it would be better to get:
* the transformation of the features (_in the course, it is being called feature engineering when dealing with log transformations of numerical variables_) (for me the terminology does not sounds correct. In fact, all the explicative variables are considered to be features.)
* the transformation of categorical variables (_as it was done in the course_)

The outcome of definition of the modules, there are 2 modules:
* `regression_model.processing.preprocessors`
* `regression_model.processing.features`

**PS:** `regression_model.processing.features` could be a module that: 
* gets connected to a DB to pull some features.
* does NLP processing to get the bag of words (our features)

## 5. Different ways to set the version of a package

Ref: [https://packaging.python.org/guides/single-sourcing-package-version/](https://packaging.python.org/guides/single-sourcing-package-version/)





