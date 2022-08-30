
.. image:: https://badge.fury.io/py/sequana-laa.svg
     :target: https://pypi.python.org/pypi/sequana_laa

.. image:: http://joss.theoj.org/papers/10.21105/joss.00352/status.svg
    :target: http://joss.theoj.org/papers/10.21105/joss.00352
    :alt: JOSS (journal of open source software) DOI

.. image:: https://github.com/sequana/laa/actions/workflows/main.yml/badge.svg
   :target: https://github.com/sequana/laa/actions/workflows/main.yml)



This is is the **laa** pipeline from the `Sequana <https://sequana.readthedocs.org>`_ project

:Overview: Perform amplicon analysis on Pacbio data sets including variant and phylogeny
:Input: A set of CCS files from pacbio in FastQ formats
:Output: variant calling, phylogney, consensus genomes, etc
:Status: production but may change
:Citation: Cokelaer et al, (2017), ‘Sequana’: a Set of Snakemake NGS pipelines, Journal of Open Source Software, 2(16), 352, JOSS DOI doi:10.21105/joss.00352

This pipeline was used in :

- L'Honneur et al (polyomavirus, 2022) https://pubmed.ncbi.nlm.nih.gov/34979561/ 
- Kali et al (rabies,2021), https://pubmed.ncbi.nlm.nih.gov/33444703/
- Claireaux et al. (gene involved in HIV, 2022) accepted, not yet on pubmed

Installation
~~~~~~~~~~~~

You must install Sequana first::

    pip install sequana

Then, just install this package::

    pip install sequana_laa


Usage
~~~~~

::

    sequana_laa --help
    sequana_laa --input-directory DATAPATH 

This creates a directory with the pipeline and configuration file. You will then need 
to execute the pipeline::

    cd laa
    sh laa.sh  # for a local run

This launch a snakemake pipeline. If you are familiar with snakemake, you can 
retrieve the pipeline itself and its configuration files and then execute the pipeline yourself with specific parameters::

    snakemake -s laa.rules -c config.yaml --cores 4 --stats stats.txt --wrapper-prefix git+file:///home/cokelaer/Work/github/forked/sequana-wrappers

Or use `sequanix <https://sequana.readthedocs.io/en/main/sequanix.html>`_ interface.

Requirements
~~~~~~~~~~~~

This pipelines requires the following executable(s):

- vt
- freebayes
- igvtools
- sequana
- snpeff (optional)
- samtools
- bamtools
- minimap2

.. image:: https://raw.githubusercontent.com/sequana/laa/main/sequana_pipelines/laa/dag.png


Details
~~~~~~~~~

This pipeline runs amplicon analysis on long reads data from pacbio sequencers. 


Rules and configuration details
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Here is the `latest documented configuration file <https://raw.githubusercontent.com/sequana/laa/main/sequana_pipelines/laa/config.yaml>`_
to be used with the pipeline. Each rule used in the pipeline may have a section in the configuration file. 

Changelog
~~~~~~~~~

========= ====================================================================
Version   Description
========= ====================================================================
0.9.0     add singularity containers
0.8.0     **First release.**
========= ====================================================================


