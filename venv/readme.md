# Project Guide Line

#### Setup:
    > Setup Python 3.6+
    > Setup PyCharm as IDE
    > Upgrade Pip to latest version
        by pass if PyCharm is a new installation
        pip install --upgrade pip
    > setup distribution tool:   python -m pip install setuptools wheel twine
    > Setup project include restoring project pakage:   pip install -e .
    > Setup tests path: run/edit configuration, click + top left to add python tests option and specify tests folder path
    > Enabling setting for documentation comments
        [Enable Creation of documentation](https://www.jetbrains.com/help/pycharm/enabling-creation-of-documentation-comments.html)         
    > Restore Dev Packages:
        reference package management in the guide line below

    > install mongodb + robomongo
    > import backup database
        ```
        extract /dbbak/cryptoDb.zip to C:\data\db\dump
        run command: mongorestore c:\data\db\dump
        ```
#### Architecture
    Web server
        [Compare NGINX and APACHE](http://www.hostingadvice.com/how-to/nginx-vs-apache)
        NGINX
    Web Framework
        [Compare DJANGO and FLASK](https://www.excella.com/insights/creating-a-restful-api-django-rest-framework-vs-flask)        
        Flask (0.12.2 Released 2017-05-16) is “a microframework for Python based on Werkzeug, Jinja 2 and good intentions.” Includes a built-in development server, unit tesing support, and is fully Unicode-enabled with RESTful request dispatching and WSGI compliance.
    API
        FLASK-REST

#### Code Guide Line:
    > Documentation:
        Code comment need to follow convention for help generation to work
        Add hint check annotation
            Default docstring is "reStructure text"
            Helpful for Unit test and collaboration
            Add stub file .pyi for compatibility with older python version before python 3
        Testable documentation for regression
            python -m pytest --doctest-modules
    > Error handling and rethrow the exception
    > Packages Management:
        https://pip.pypa.io/en/latest/user_guide/#requirements-files
        ```
        requirements.txt is to manage list of package dependencies
        ```
        run:
            pip install -r requirements.txt
            or pip wheel --wheel-dir=/local/wheels -r requirements.txt
        check:
            pip list

    > Unit test (PyTest fw in /tests folder)
        Follow [Unit test good practice](https://docs.pytest.org/en/latest/goodpractices.html#goodpractices) 
        Naming by convention: 
            test_*.py or *_test.py
        Test Coverage
            pytest tool
                python -m pytest --cov-report html --cov [modulename]
            unittest tool
            ```
                run unitest: python -m coverage run -m unittest
                see report: python -m coverage report
                export as html: python -m coverage html
            ```

    > Distribute & Deployment:
    ```
        https://packaging.python.org/tutorials/distributing-packages/#requirements-for-packaging-and-distributing
    ```
        Production
        ```
            https://caremad.io/posts/2013/07/setup-vs-requirement/
        ```
            python setup.py sdist --format zip
            in end machine
            ```
                pip uninstall package.zip
                pip install package.zip
            ```
            Other option is UI Exe packaging tool
                InnoSoft
                    http://www.jrsoftware.org/isdl.php
                PyInstaller
                ```
                    pip install pyinstaller
                    pyinstaller --onefile __main__.py
                ```
