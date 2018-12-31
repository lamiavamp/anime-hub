# Anime Hub
Anime Hub is a project aiming to keep all the Otakus out there up-to-date with the latest Anime shows and movies! we provide what you need to know about the latest anime realeses with the help of the community.

with **Anime Hub** you will be able to:
- view a vraity of anime collections, categorized! (no sign-up needed)
- Sign up with google plus and join the community of Otakus to help us keep our collection of anime as recent as possible. Registered users will be able to:
    * add new Anime to any of the listed categories
    * edit/delete the added Anime

The project is written in Python 2 and created using Flask framework version 1.0.2. Sqlite database is used with sqlalchemy.

### Installation
* Clone the repository using git
`$ git clone https://github.com/lamiavamp/anime-hub.git`
`$ cd anime-hub`
* Download the zip by clicking clone or download > download zip

### Content of the repository
- **database_setup.py:** a script that will create the database and tables
- **seeder.py:** initial database data
- **server.py:** server process -core router-
- **static:** a directory containing all styles and static files such as images
- **templates:** a directory containing all html pages

## Getting Started

### Prerequisites
- The code is running on python 2, make sure it is installed. To install `python 2` in Mac use homebrew: 
`$ brew install python`
or follow [this link](https://realpython.com/installing-python) for other OS 
- install Flask module:
`$ pip install flask`
- install SQLAlchemy module for database setup:
`$ pip install SQLAlchemy`
- install oauth2client module for google sign in:
`$ pip install oauth2client`
- Note that you have to create your credentials (named as `client_secrets.json`) through [Google APIs and Services](https://console.developers.google.com/) to run google sign in functionality

### Usage
1. create the database first by running `database_setup.py`:
`$ python database_setup.py`
2. seed the database with base data by running:
`$ python seeder.py`
3. get the server up and running listening on port 5000:
`$ python server.py`
the server will now be listening on port 5000
4. visit localhost/5000

Enjoy!

### Author Note
Note that there are some functionalties under development and will be released on upcoming versions, such as uploading an image for the Anime when adding it. All contributors are more than welcome to participate, just fork and start coding!

## Author
* **Lamia** - [lamiavamp](https://github.com/lamiavamp)
