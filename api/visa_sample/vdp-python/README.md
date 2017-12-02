# Python Sample Code for Visa API calls

## Installation

We use nose to run our unit tests

Install nose using 

    $ pip install nose
  
To install the package and the required dependencies run the following command

	$ python setup.py install

## Usage
  	 
Update the `configuration.ini` file under the `visa` folder. For more information on `configuration.ini` refer :
	 
* [Manual](https://github.com/visa/SampleCode/wiki/Manual)

Run Visa sample calls by moving to the visa package and then execute:
    
    $ nosetests

Mac users might be required to give:
    
    $ nosetests --exe

You would need to generate a Call Id for calling Visa Checkout. The documentation for generating Call Id can be found at :

* [Visa Checkout Guide](https://github.com/visa/SampleCode/wiki/Visa-Checkout)

Auto-population of test data is available only for Visa Transaction Alerts for now. We are working on this and will try to further improve your experience by generating it for other products as well.

The sample code provided reads the credentials from configuration file as plain text. As a best practice we recommend you to store the credentials in an encrypted form and decrypt while using them.