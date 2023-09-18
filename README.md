# retico-opendialdm
PyOpenDial Dialogue Manager for ReTiCo

You need to clone the version of pyOpenDial maintained by the SLIM Group:

`https://bitbucket.org/bsu-slim/pyopendial`

Then you need to set the PYOD env variable:

```
import os, sys
os.environ['PYOD'] = '/path/to/pyopendial'
sys.path.append(prefix+'retico-opendialdm')
# you might need to add sys.path.append(os.environ['PYOD']) to the dm.py file in retico-opendialdm

from retico_opendialdm.dm import OpenDialModule
domain_dir = 'dialogue.xml'
opendial_variables = ['firstname',
                      'lastname',
                      'work',
                      'email',
                      'note']

dm = OpenDialModule(domain_dir=domain_dir, variables=opendial_variables)

```
Original OpenDial citation and Python implementation citation

```

@INPROCEEDINGS{Lison2016-jk,
  title     = "{OpenDial}: A toolkit for developing spoken dialogue systems
               with probabilistic rules",
  booktitle = "54th Annual Meeting of the Association for Computational
               Linguistics, {ACL} 2016 - System Demonstrations",
  author    = "Lison, Pierre and Kennington, Casey",
  abstract  = "\copyright{} 2016 Association for Computational Linguistics. We
               present a new release of OpenDial, an open-source toolkit for
               building and evaluating spoken dialogue systems. The toolkit
               relies on an information-state architecture where the dialogue
               state is represented as a Bayesian network and acts as a shared
               memory for all system modules. The domain models are specified
               via probabilistic rules encoded in XML. Open-Dial has been
               deployed in several application domains such as human-robot
               interaction, intelligent tutoring systems and multi-modal in-car
               driver assistants.",
  year      =  2016
}

@INPROCEEDINGS{Jang2020-fb,
  title     = "{PyOpenDial}: A python-based domain-independent toolkit for
               developing spoken dialogue systems with probabilistic rules",
  booktitle = "{EMNLP-IJCNLP} 2019 - 2019 Conference on Empirical Methods in
               Natural Language Processing and the 9th International Joint
               Conference on Natural Language Processing, Proceedings of System
               Demonstrations",
  author    = "Jang, Youngsoo and Lee, Jongmin and Park, Jaeyoung and Lee,
               Kyeng Hun and Lison, Pierre and Kim, Kee Eung",
  abstract  = "We present PyOpenDial, a Python-based domain-independent,
               open-source toolkit for spoken dialogue systems. Recent advances
               in core components of dialogue systems, such as speech
               recognition, language understanding, dialogue management, and
               language generation, harness deep learning to achieve
               state-of-the-art performance. The original OpenDial, implemented
               in Java, provides a plugin architecture to integrate external
               modules, but lacks Python bindings, making it difficult to
               interface with popular deep learning frameworks such as
               Tensorflow or PyTorch. To this end, we re-implemented OpenDial
               in Python and extended the toolkit with a number of novel
               functionalities for neural dialogue state tracking and action
               planning. We describe the overall architecture and its
               extensions, and illustrate their use on an example where the
               system response model is implemented with a recurrent neural
               network.",
  pages     = "187--192",
  year      =  2020
}

```

