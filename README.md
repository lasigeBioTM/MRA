Most of the Ontologies nowadays are in the English language, which is a problem if you want to process some non-English text using Text Mining techniques that use these Ontologies. One solution would be to translate the ontology. Other is to translate the text and this is the approach that is explored in this demo application.

Here we consider the problem of annotating non-English medical reports with [RadLex](http://www.radlex.org/) terms.

The flow of the application goes like this. The doctor or researcher uploads a .txt file containing a medical report to the application, and the text of this report is sent to [Unbabel](https://unbabel.com/)'s translation services, which combines human translation with machine translation. In this prototype only machine translation is being used, for demonstration purposes. In a real-life scenario, human translation could also be used for more reliable results. So, the text is sent to translation and after a while (~2 min, to simulate a real human and machine translation) the translation is ready.

Then, the translated text is sent to [BioPortal](http://bioportal.bioontology.org/) annotation services. After this is done it is possible to explore the annotations in a user friendly interface.

The interface of the annotations was partly inspired by a similar project called [LexMap](http://lexmap.xrlabs.com/).

**Developers:**

*   [Luís Campos](https://llcampos.wordpress.com/)

**Supervisors:**

*   [Francisco Couto (FCUL)](http://webpages.fc.ul.pt/~fjcouto/)
*   [Vasco Pedro (Unbabel)](https://unbabel.com/)
