# IGEA

IGEA is a web-based tool for integrative analysis of gene expression data.


## Development progress

- [X] [DONE] Database
	- [X] schema to store Eperiment, Sample and Microarray metadata
	- [X] schema to store additional info on sample attribute names and values
	- [X] Store additional info on sample attribute standard names and values: link to ontologies (MeSh, EFO), explanation, synonyms
	- [ ] [MOSTLY DONE] store and update in background Experiment status: standardized; mail sent, mail received, has minimal data for integration, is excluded etc.

- [X] [DONE] Automate downloading metadata form ArrayExpress

- [X] [DOING] Admin interface 
	- [X] autocomplete lookup fields and "for each" checkboxes for easier input
	- [ ] reduce loading form loading time
	- [ ] samples metadata standardization form 
	- [ ] samples attribute add or replace form
	- [ ] test data for duplicate entities

- [ ] [DOING] Deployment
	- [X] Deploy to Heroku hosting service; suspended due to exeeded space limit for a free account
	- [X] Deploy to the server at Institute of Molecular Biology and Genetics; accessible at http://194.44.31.241:24173/
	- [ ] deploy to a server at European Grid Infrastructure 

- [X] [DONE] Data plots

- [ ] [DOING] Data access user interface
	- [X] Basic interface with header nav bar
	- [X] Experiments page with basic table of experiments
	- [X] Samples page with basic table of samples
	- [X] Upd tables with filter rows by column value
	- [ ] [DOING] Side bar for Samples table to show/hide certain columns and rows with certain values
	- [X] Intro page
	- [X] Logo
	- [X] Downlowdable BibTex citations on nav bar
	- [ ] Order columns properly 
	- [ ] Download Experiments, Samples tables as TSV files
	- [ ] Upload Experiment, Sample metadata from TSV files provided by user
	- [ ] Slider widgets to Samples side bar as search filters for numeric columns
	- [ ] Exclude rows with empty values option

- [ ] Construct study groups based on metadata 
	- [ ] send study groups' meta- and expression data to Inmex
	
- [ ] Automate downloading and processing sample expression data from ArrayExpress

- [ ] Integrate sample expression data for study groups

- [ ] Search for differentially expressed genes.

- [ ] Embed earlier developed BNFinder tool for gene regulatory networks construction https://github.com/sysbio-vo/bnfinder/

- [ ] Data analysis user interface

- [ ] Embed Telegram bot featured for automated solving bioinformatican's minor problems, which is under development https://github.com/Dantistnfs/telegram-genetic-bot

- [ ] Specialized blog to quickly post new analysis results to IGEA site and to social media 









<!-- 
## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

What things you need to install the software and how to install them

```
Give examples
```

### Installing

A step by step series of examples that tell you have to get a development env running

Say what the step will be

```
Give the example
```

And repeat

```
until finished
```

End with an example of getting some data out of the system or using it for a little demo

## Running the tests

Explain how to run the automated tests for this system

### Break down into end to end tests

Explain what these tests test and why

```
Give an example
```

### And coding style tests

Explain what these tests test and why

```
Give an example
```

## Deployment

Add additional notes about how to deploy this on a live system
 -->
## Built With

* [Python 3.5.2](https://www.python.org/downloads/release/python-352/) - Programming language
* [Django](https://github.com/django/django) - Web develompent framework
* [Postgres](https://rometools.github.io/rome/) - Database

<!-- ## Contributing

Please read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/your/project/tags). 
 
## Authors

* **Billie Thompson** - *Initial work* - [PurpleBooth](https://github.com/PurpleBooth)

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.
-->
## License

This project is licensed under the GNU General Public License - see the [LICENSE](LICENSE) file for details

<!-- 
## Acknowledgments

* Hat tip to anyone who's code was used
* Inspiration
* etc -->

