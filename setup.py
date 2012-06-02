from distutils.core import setup


setup(
    name="django-spaceview",
    version=__import__("spaceview").__version__,
    author="Gustavo Diaz Jaimes",
    author_email="gustavodiazjaimes@gmail.com",
    description="Father app dependency in reusable aplications, object and context access using namespaces and class base views",
    long_description=open("README.rst").read(),
    url="https://github.com/gustavodiazjaimes/spaceview",
    packages="spaceview",
    install_requires = [
        "django-appconf==0.5",
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Framework :: Django",
    ],
)