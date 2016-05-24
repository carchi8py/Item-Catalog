Item Catalog
=============

## Description 
This app show a collection of items used in different sports. A 3rd party authentication system (Google) is implemented to let users add, update, and delete the own sport items. Also, this app implements an API endpoint, where the user can get the information in json format. This app uses Flask Python famework for it backend, and uses Bootstrap for javascript and CSS

## Requirements
- [Vagrant](https://www.vagrantup.com/)
- [VirtualBox](https://www.virtualbox.org/)
- [Python ~2.7](https://www.python.org/)

## Usage

Launch the Vagrant VM from inside the *vagrant* folder with:

`vagrant up`

`vagrant ssh`

Then move inside the catalog folder:

`cd /vagrant/itemCatalog`

Create a new database running the following command

`python database_setup.py`

Fill the database with objects running this command

`python lotsofitems.py`

Start the web server with the following command

`python finalProject.py`

Now the website has started up you can view it at 

`http://localhost:8000/`

It is important you use *localhost* instead of *0.0.0.0* inside the URL address. That will prevent OAuth from failing.