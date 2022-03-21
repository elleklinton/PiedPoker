import setuptools
from setuptools import setup

setup(
    name='pied_poker',
    version='0.2.8',
    description='A Python package to run flexible and fast poker simulations using a monte carlo style simulator.',
    long_description='A Python package to run flexible and fast poker simulations using a monte carlo style simulator.',
    url='https://github.com/elleklinton/PiedPoker',
    author='Ellek Linton',
    author_email='ellek@elleklinton.com',
    license='GNU LGPLv3',
    packages=['pied_poker',
              'pied_poker.card',
              'pied_poker.deck',
              'pied_poker.hand',
              'pied_poker.player',
              'pied_poker.poker_round',
              'pied_poker.probability',
              'pied_poker.probability.events',
              'pied_poker.visualization',
              'pied_poker.visualization.heatmap',
              'pied_poker.visualization.heatmap_samples'
              ],
    install_requires=['joblib', 'tqdm', 'numpy', 'seaborn', 'pandas'],
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'License :: Free for non-commercial use',
        'Topic :: Games/Entertainment :: Simulation',
        'Topic :: Games/Entertainment',
        'Programming Language :: Python :: 3.8',
        'Development Status :: 4 - Beta'
    ],
)
