from setuptools import find_packages,setup
from typing import List


hyphen_e_dot = '-e .'
def get_requirenments(file_path:str)->List[str]:

    requirements = []

    with open(file_path) as file_obj:
        requirements=file_obj.readlines()
        requirements = [req.replace("\n","") for req in requirements]

        if hyphen_e_dot in requirements:
            requirements.remove(hyphen_e_dot)

    return requirements









setup(name="MlProject",
      version='0.0.1',author="Rohan Routh",
      author_email="rohanrouth@gmail.com",
      packages=find_packages(),install_requires=get_requirenments('requirements.txt'))

