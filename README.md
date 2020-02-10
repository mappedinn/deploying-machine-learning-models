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


## 6. Packaging

Serveral steps are required to build a package:

1. Separating the requirements.txt files: one file per package + one file for development

**requirements.txt of the package regression_model** (located in `packages/regression_model`)
```py
# production requirements
numpy==1.18.0
pandas==0.25.3
scikit-learn==0.22.1

# for packaging
setuptools==41.2.0
wheel==0.34.2

# for testing
pytest==5.3.5
```

**requirements.txt of the development** (located in `./regression_model`)
```py
# development requirements
jupyter==1.0.0
matplotlib==3.1.1

# production requirements
numpy==1.18.0
pandas==0.25.3
scikit-learn==0.22.1

# for packaging
setuptools==41.2.0
wheel==0.34.2

# for testing
pytest==5.3.5
```

2. Creation of the `packages/regression_model/setup.py` file

```py
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import io
import os
from pathlib import Path

from setuptools import find_packages, setup


# Package meta-data.
NAME = 'regression_model'
DESCRIPTION = 'Train and deploy regression model.'
URL = 'https://github.com/mappedinn/deploying-machine-learning-models'
EMAIL = 'jallouli.med.amine@gmail.com'
AUTHOR = 'Mohamed Amine Jallouli'
REQUIRES_PYTHON = '>=3.7.0'


# What packages are required for this module to be executed?
def list_reqs(fname='requirements.txt'):
    with open(fname) as fd:
        return fd.read().splitlines()


# The rest you shouldn't have to touch too much :)
# ------------------------------------------------
# Except, perhaps the License and Trove Classifiers!
# If you do change the License, remember to change the
# Trove Classifier for that!

here = os.path.abspath(os.path.dirname(__file__))

# Import the README and use it as the long-description.
# Note: this will only work if 'README.md' is present in your MANIFEST.in file!
try:
    with io.open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
        long_description = '\n' + f.read()
except FileNotFoundError:
    long_description = DESCRIPTION


# Load the package's __version__.py module as a dictionary.
ROOT_DIR = Path(__file__).resolve().parent
PACKAGE_DIR = ROOT_DIR / NAME
about = {}
with open(PACKAGE_DIR / 'VERSION') as f:
    _version = f.read().strip()
    about['__version__'] = _version


# Where the magic happens:
setup(
    name=NAME,
    version=about['__version__'],
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type='text/markdown',
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    packages=find_packages(exclude=('tests',)),
    package_data={'regression_model': ['VERSION']},
    install_requires=list_reqs(),
    extras_require={},
    include_package_data=True,
    license='MIT',
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy'
    ],
)
```

3. Creation of `packages/regression_model/MANIFEST.in`

```MANIFEST
include *.txt
include *.md
include *.cfg
include *.pkl
recursive-include ./regression_model/*

include regression_model/datasets/train.csv
include regression_model/datasets/test.csv
include regression_model/trained_models/*.pkl
include regression_model/VERSION

include ./requirements.txt
exclude *.log

recursive-exclude * __pycache__
recursive-exclude * *.py[co]
```

4. Building the package

```sh
python packages/regression_model/setup.py sdist bdist_wheel
```

5. Installation of the package `regression_model`

Surprisingly, the `dist` and `build` folders are not going to be used. The `packages/regression_model` is going to be used.

The command line of installation:

```sh
pip install -e packages/regression_model
(env) C:\Users\999138\Documents\ME\udemy-deploying-machine-learning-models>pip install -e packages/regression_model
# Obtaining file:///C:/Users/999138/Documents/ME/udemy-deploying-machine-learning-models/packages/regression_model
# Requirement already satisfied: numpy==1.18.0 in c:\users\999138\documents\me\udemy-deploying-machine-learning-models\env\lib\site-packages (from regression-model==0.1.0) (1.18.0)
# Requirement already satisfied: pandas==0.25.3 in c:\users\999138\documents\me\udemy-deploying-machine-learning-models\env\lib\site-packages (from regression-model==0.1.0) (0.25.3)
# Requirement already satisfied: scikit-learn==0.22.1 in c:\users\999138\documents\me\udemy-deploying-machine-learning-models\env\lib\site-packages (from regression-model==0.1.0) (0.22.1)
# Requirement already satisfied: setuptools==41.2.0 in c:\users\999138\documents\me\udemy-deploying-machine-learning-models\env\lib\site-packages (from regression-model==0.1.0) (41.2.0)
# Requirement already satisfied: wheel==0.34.2 in c:\users\999138\documents\me\udemy-deploying-machine-learning-models\env\lib\site-packages (from regression-model==0.1.0) (0.34.2)     
# Requirement already satisfied: pytest==5.3.5 in c:\users\999138\documents\me\udemy-deploying-machine-learning-models\env\lib\site-packages (from regression-model==0.1.0) (5.3.5)
# Requirement already satisfied: pytz>=2017.2 in c:\users\999138\documents\me\udemy-deploying-machine-learning-models\env\lib\site-packages (from pandas==0.25.3->regression-model==0.1.0) (2019.3)
# Requirement already satisfied: python-dateutil>=2.6.1 in c:\users\999138\documents\me\udemy-deploying-machine-learning-models\env\lib\site-packages (from pandas==0.25.3->regression-model==0.1.0) (2.8.1)
# Requirement already satisfied: scipy>=0.17.0 in c:\users\999138\documents\me\udemy-deploying-machine-learning-models\env\lib\site-packages (from scikit-learn==0.22.1->regression-model==0.1.0) (1.4.1)
# Requirement already satisfied: joblib>=0.11 in c:\users\999138\documents\me\udemy-deploying-machine-learning-models\env\lib\site-packages (from scikit-learn==0.22.1->regression-model==0.1.0) (0.14.1)
# Requirement already satisfied: py>=1.5.0 in c:\users\999138\documents\me\udemy-deploying-machine-learning-models\env\lib\site-packages (from pytest==5.3.5->regression-model==0.1.0) (1.8.1)
# Requirement already satisfied: pluggy<1.0,>=0.12 in c:\users\999138\documents\me\udemy-deploying-machine-learning-models\env\lib\site-packages (from pytest==5.3.5->regression-model==0.1.0) (0.13.1)
# Requirement already satisfied: colorama; sys_platform == "win32" in c:\users\999138\documents\me\udemy-deploying-machine-learning-models\env\lib\site-packages (from pytest==5.3.5->regression-model==0.1.0) (0.4.3)
# Requirement already satisfied: packaging in c:\users\999138\documents\me\udemy-deploying-machine-learning-models\env\lib\site-packages (from pytest==5.3.5->regression-model==0.1.0) (20.1)
# Requirement already satisfied: atomicwrites>=1.0; sys_platform == "win32" in c:\users\999138\documents\me\udemy-deploying-machine-learning-models\env\lib\site-packages (from pytest==5.3.5->regression-model==0.1.0) (1.3.0)
# Requirement already satisfied: importlib-metadata>=0.12; python_version < "3.8" in c:\users\999138\documents\me\udemy-deploying-machine-learning-models\env\lib\site-packages (from pytest==5.3.5->regression-model==0.1.0) (1.5.0)
# Requirement already satisfied: wcwidth in c:\users\999138\documents\me\udemy-deploying-machine-learning-models\env\lib\site-packages (from pytest==5.3.5->regression-model==0.1.0) (0.1.8)
# Requirement already satisfied: more-itertools>=4.0.0 in c:\users\999138\documents\me\udemy-deploying-machine-learning-models\env\lib\site-packages (from pytest==5.3.5->regression-model==0.1.0) (8.2.0)
# Requirement already satisfied: attrs>=17.4.0 in c:\users\999138\documents\me\udemy-deploying-machine-learning-models\env\lib\site-packages (from pytest==5.3.5->regression-model==0.1.0) (19.3.0)
# Requirement already satisfied: six>=1.5 in c:\users\999138\documents\me\udemy-deploying-machine-learning-models\env\lib\site-packages (from python-dateutil>=2.6.1->pandas==0.25.3->regression-model==0.1.0) (1.14.0)
# Requirement already satisfied: pyparsing>=2.0.2 in c:\users\999138\documents\me\udemy-deploying-machine-learning-models\env\lib\site-packages (from packaging->pytest==5.3.5->regression-model==0.1.0) (2.4.6)     
# Requirement already satisfied: zipp>=0.5 in c:\users\999138\documents\me\udemy-deploying-machine-learning-models\env\lib\site-packages (from importlib-metadata>=0.12; python_version < "3.8"->pytest==5.3.5->regression-model==0.1.0) (2.1.0)
# Installing collected packages: regression-model
#   Attempting uninstall: regression-model
#     Found existing installation: regression-model 0.1.0
#     Not uninstalling regression-model at c:\users\999138\documents\me\udemy-deploying-machine-learning-models\packages\regression_model, outside environment c:\users\999138\documents\me\udemy-deploying-machine-learning-models\env
#     Can't uninstall 'regression-model'. No files were found to uninstall.
#   Running setup.py develop for regression-model
# Successfully installed regression-model
```
**NB:** There is one important comment that I would like to add. It is regarding the package name. What I tried to install is `regression_model`. Nevertheless, the log of the command line is showing that the package `regression-model` is being installed.

At the end of the installation, the command `pip` showed it installed the package `regression-model`. This package will not be able to be imported. Instead, the package `regression_model` can be imported.

Please be noticed that the package `regression_model` is not located in the `env/Lib/site-packages` like `numpy` for example. It os located in the `packages/regression_model`. This is confirmed with the command `pip`:

```sh
(env) C:\Users\999138\Documents\ME\udemy-deploying-machine-learning-models>pip list
# Package            Version Location
# ------------------ ------- ----------------------------------------------------------------------------------------------
# astroid            2.3.3
# atomicwrites       1.3.0
# attrs              19.3.0
# colorama           0.4.3
# importlib-metadata 1.5.0   
# isort              4.3.21
# joblib             0.14.1
# lazy-object-proxy  1.4.3
# mccabe             0.6.1
# more-itertools     8.2.0
# numpy              1.18.0
# packaging          20.1    
# pandas             0.25.3
# pip                20.0.2
# pluggy             0.13.1
# py                 1.8.1
# pylint             2.4.4
# pyparsing          2.4.6
# pytest             5.3.5
# python-dateutil    2.8.1
# pytz               2019.3
# regression-model   0.1.0   c:\users\999138\documents\me\udemy-deploying-machine-learning-models\packages\regression_model
# scikit-learn       0.22.1
# scipy              1.4.1
# setuptools         41.2.0
# six                1.14.0
# typed-ast          1.4.1
# wcwidth            0.1.8
# wheel              0.34.2
# wrapt              1.11.2
# zipp               2.1.0
```

## 6. Creation of a RESTful API for serving the ML algorithm

**Steps:**
* Installation of `flask` though setting up the requirements.txt file as follows:
```py
# api
flask==1.1.1

# local regression_model package
# update with your local path
-e "packages/regression_model" 
```
* Creation of a web application controller as follows:

```py
# packages/ml_api/api/controller.py
from flask import Blueprint, request

prediction_app = Blueprint('prediction_app', __name__)

@prediction_app.route('/', methods=['GET'])
def home():
    if request.method == 'GET':
        return 'Landing page of the ML API'

@prediction_app.route('/health', methods=['GET'])
def health():
    if request.method == 'GET':
        return 'ok'

```
* Creation of a Flask application as follows:
```py
from flask import Flask


def create_app() -> Flask:
    """Create a flask app instance."""

    flask_app = Flask('ml_api')

    # import blueprints
    from api.controller import prediction_app
    flask_app.register_blueprint(prediction_app)

    return flask_app
```
* The main application

```py
#  packages/ml_api/run.py
from api.app import create_app

application = create_app()

if __name__ == '__main__':
    application.run()
```

* Serving the flask application

```sh
python packages/ml_api/run.py
```

## 7. Prediction end point of the REST API

```py
# packages/ml_api/api/controller.py
# ...
@prediction_app.route('/v1/predict/regression', methods=['POST'])
def predict():
    if request.method == 'POST':
        json_data = request.get_json()
        _logger.info(f'Inputs: {json_data}')

        result = make_prediction(input_data=json_data)
        _logger.info(f'Outputs: {result}')

        predictions = result.get('predictions')[0]
        version = result.get('version')

        return jsonify({'predictions': predictions,
                        'version': version})
```

## 8. Testing the prediction end point of the REST API

```py
# packages/ml_api/tests/test_controller.py
# ...
def test_prediction_endpoint_returns_prediction(flask_test_client):
    # Given
    # Load the test data from the regression_model package
    # This is important as it makes it harder for the test
    # data versions to get confused by not spreading it
    # across packages.
    test_data = load_dataset(file_name=model_config.TESTING_DATA_FILE)
    post_json = test_data[0:1].to_json(orient='records')

    # When
    response = flask_test_client.post('/v1/predict/regression',
                                      json=post_json)

    # Then
    assert response.status_code == 200
    response_json = json.loads(response.data)
    prediction = response_json['predictions']
    response_version = response_json['version']
    assert math.ceil(prediction) == 112476
    assert response_version == _version
```

```sh
(env) C:\Users\999138\Documents\ME\udemy-deploying-machine-learning-models>pytest packages\ml_api\tests
# ========================================================================================== test session starts ==========================================================================================
# platform win32 -- Python 3.7.6, pytest-5.3.5, py-1.8.1, pluggy-0.13.1
# rootdir: C:\Users\999138\Documents\ME
# collected 2 items

# packages\ml_api\tests\test_controller.py ..                                                [100%]

# =========================================================================================== warnings summary ============================================================================================
# udemy-deploying-machine-learning-models/packages/ml_api/tests/test_controller.py::test_health_endpoint_returns_200
#   C:\ProgramData\Anaconda3\lib\importlib\_bootstrap.py:219: RuntimeWarning: numpy.ufunc size changed, may indicate binary incompatibility. Expected 192 from C header, got 216 from PyObject
#     return f(*args, **kwds)

# -- Docs: https://docs.pytest.org/en/latest/warnings.html
# ===================================================================================== 2 passed, 1 warning in 1.20s ======================================================================================
```

It seems to be that an older version of `numpy` should be considered.

## 9. API schema validation
Schema validation of the features being provided to the ML algorithm API is necessary. In fact, it would allow returning an error in case of invalid schema.
* **Library:** There are several libraries that do schema validation. These alternatives and complements to marshmallow are:
    - Pydantic: [https://pydantic-docs.helpmanual.io/](https://pydantic-docs.helpmanual.io/)
    - Cerberus: [http://docs.python-cerberus.org/en/stable/](http://docs.python-cerberus.org/en/stable/)
    - Colander: [https://github.com/Pylons/colander](https://github.com/Pylons/colander)

    The installation of `marshmallow` is installed through: `pip install marshmallow`

* **Creation of class for schema validation:** 

```py
class HouseDataRequestSchema(Schema):
    Alley = fields.Str(allow_none=True)
    BedroomAbvGr = fields.Integer()
    BldgType = fields.Str()
    BsmtCond = fields.Str()
    BsmtExposure = fields.Str(allow_none=True)
    BsmtFinSF1 = fields.Float()
    BsmtFinSF2 = fields.Float()
    BsmtFinType1 = fields.Str()
    BsmtFinType2 = fields.Str()
    BsmtFullBath = fields.Float()
    BsmtHalfBath = fields.Float()
    BsmtQual = fields.Str(allow_none=True)
    BsmtUnfSF = fields.Float()
    CentralAir = fields.Str()
    Condition1 = fields.Str()
    Condition2 = fields.Str()
    Electrical = fields.Str()
    EnclosedPorch = fields.Integer()
    ExterCond = fields.Str()
    ExterQual = fields.Str()
    Exterior1st = fields.Str()
    Exterior2nd = fields.Str()
    Fence = fields.Str(allow_none=True)
    FireplaceQu = fields.Str(allow_none=True)
    Fireplaces = fields.Integer()
    Foundation = fields.Str()
    FullBath = fields.Integer()
    Functional = fields.Str()
    GarageArea = fields.Float()
    GarageCars = fields.Float()
    GarageCond = fields.Str()
    GarageFinish = fields.Str(allow_none=True)
    GarageQual = fields.Str()
    GarageType = fields.Str(allow_none=True)
    GarageYrBlt = fields.Float()
    GrLivArea = fields.Integer()
    HalfBath = fields.Integer()
    Heating = fields.Str()
    HeatingQC = fields.Str()
    HouseStyle = fields.Str()
    Id = fields.Integer()
    KitchenAbvGr = fields.Integer()
    KitchenQual = fields.Str()
    LandContour = fields.Str()
    LandSlope = fields.Str()
    LotArea = fields.Integer()
    LotConfig = fields.Str()
    LotFrontage = fields.Float(allow_none=True)
    LotShape = fields.Str()
    LowQualFinSF = fields.Integer()
    MSSubClass = fields.Integer()
    MSZoning = fields.Str()
    MasVnrArea = fields.Float()
    MasVnrType = fields.Str(allow_none=True)
    MiscFeature = fields.Str(allow_none=True)
    MiscVal = fields.Integer()
    MoSold = fields.Integer()
    Neighborhood = fields.Str()
    OpenPorchSF = fields.Integer()
    OverallCond = fields.Integer()
    OverallQual = fields.Integer()
    PavedDrive = fields.Str()
    PoolArea = fields.Integer()
    PoolQC = fields.Str(allow_none=True)
    RoofMatl = fields.Str()
    RoofStyle = fields.Str()
    SaleCondition = fields.Str()
    SaleType = fields.Str()
    ScreenPorch = fields.Integer()
    Street = fields.Str()
    TotRmsAbvGrd = fields.Integer()
    TotalBsmtSF = fields.Float()
    Utilities = fields.Str()
    WoodDeckSF = fields.Integer()
    YearBuilt = fields.Integer()
    YearRemodAdd = fields.Integer()
    YrSold = fields.Integer()
    FirstFlrSF = fields.Integer()
    SecondFlrSF = fields.Integer()
    ThreeSsnPortch = fields.Integer()
```

* **Validation of the input**

```py
def validate_inputs(input_data):
    """Check prediction inputs against schema."""

    # set many=True to allow passing in a list
    schema = HouseDataRequestSchema(strict=True, many=True)

    # convert syntax error field names (beginning with numbers)
    for dict in input_data:
        for key, value in SYNTAX_ERROR_FIELD_MAP.items():
            dict[value] = dict[key]
            del dict[key]

    errors = None
    try:
        schema.load(input_data)
    except ValidationError as exc:
        errors = exc.messages

    # convert syntax error field names back
    # this is a hack - never name your data
    # fields with numbers as the first letter.
    for dict in input_data:
        for key, value in SYNTAX_ERROR_FIELD_MAP.items():
            dict[key] = dict[value]
            del dict[value]

    if errors:
        validated_input = _filter_error_rows(
            errors=errors,
            validated_input=input_data)
    else:
        validated_input = input_data

    return validated_input, errors

def _filter_error_rows(errors: dict,
                       validated_input: t.List[dict]
                       ) -> t.List[dict]:
    """Remove input data rows with errors."""

    indexes = errors.keys()
    # delete them in reverse order so that you
    # don't throw off the subsequent indexes.
    for index in sorted(indexes, reverse=True):
        del validated_input[index]

    return validated_input
```

* **Redefinition of the prediction endpoint**

```py
@prediction_app.route('/v1/predict/regression', methods=['POST'])
def predict():
    if request.method == 'POST':
        # Step 1: Extract POST data from request body as JSON
        json_data = request.get_json()
        _logger.debug(f'Inputs: {json_data}')

        # Step 2: Validate the input using marshmallow schema
        input_data, errors = validate_inputs(input_data=json_data)

        # Step 3: Model prediction
        result = make_prediction(input_data=input_data)
        _logger.debug(f'Outputs: {result}')

        # Step 4: Convert numpy ndarray to list
        predictions = result.get('predictions').tolist()
        version = result.get('version')

        # Step 5: Return the response as JSON
        return jsonify({'predictions': predictions,
                        'version': version,
                        'errors': errors})
```