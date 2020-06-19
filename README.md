# Sourcerer.io scrapper + API

[![GitHub issues](https://img.shields.io/github/issues/Stormix/sourcerer-io-scrapper.svg?style=flat-square)](https://github.com/Stormix/sourcerer-io-scrapper/issues)
[![GitHub forks](https://img.shields.io/github/forks/Stormix/sourcerer-io-scrapper.svg?style=flat-square)](https://github.com/Stormix/sourcerer-io-scrapper/network)
[![GitHub stars](https://img.shields.io/github/stars/Stormix/sourcerer-io-scrapper.svg?style=flat-square)](https://github.com/Stormix/sourcerer-io-scrapper/stargazers)
 
Because they don't have an API. https://sourcerer.io/Stormix

## Requirements

- Python 3.x 
- Selenium
- BeautifulSoup4
- Flask

## How to use

Install requirements:

```
pip install -r requirements.txt
```

Run the flask app:
```
python main.py
```

## API
### GET Request `/fetch/username`
Just send a `GET` request to: https://sourcerer.stormix.co/fetch/<username>. Give it a second, it spins up a chrome instance to load the site and fetch your profile info. Due to the time it takes, I highly suggest you cache the API response for later use and schedule API calls to update later.
### `200` Response

The response contains:
- updated_at timestamp
- the overview chart info with datapoints containing the specific date range and the commits/language information
- name, username, job, website
- overview technologies
- detailed technologies + libraries
- fun_facts
  
and has the following format:
```
{
  "chart": {
    "dataset": [
      { 
        "data": [
          {
            "commits": 15, 
            "language": "Python", 
            "locs": 570
          }, 
          {
            "commits": 6, 
            "language": "PHP", 
            "locs": 20
          }
        ], 
        "date": [
          "2017-01-01T00:00:00", 
          "2017-04-02T00:00:00"
        ]
      }, 
      ...
      }
    ], 
    "updated_at": "2020-06-18T00:06:00"
  }, 
  "commits": "994", 
  "fun_facts": [
    {
      "fact": [
        "I'm most productive during daytime", 
        "49% of users", 
        "d"
      ], 
      "stat": [
        ""
      ]
    }, 
    ...
  ], 
  "job": "Software Engineer", 
  "loc": "5617325", 
  "location": "Nantes, France", 
  "name": "Anas Mazouni", 
  "overview_technologies": [
    "Python", 
    "PHP", 
    "Slugify", 
    "JavaScript", 
    "Travis CI", 
    "HTML", 
    "Laravel", 
    "CSS", 
    "vue", 
    "express", 
    "async", 
    "vuex"
  ], 
  "site": "stormix.co", 
  "technologies": [
    {
      "commits": 994, 
      "libraries": [
        {
          "loc": 98503, 
          "name": "vue", 
          "type": "ui-framework"
        }, 
        ...
      ], 
      "title": "JavaScript Web"
    },
    ...
  ], 
  "updated_at": "2020-06-18T00:06:00", 
  "username": "Stormix"
}
```
### `500` Response
`Something went wrong ¯\_(ツ)_/¯`

### `404` Response
`
{
  "error": "Not found"
}
`
## Deployment 

### Docker

The repo includes a docker file to build an image of the project, you'll need to expose port `3000` to expose the flask application. 

Its built around the `python:3.8` image, it installs google-chrome and downloads the chrome driver to use with selenium.

### [CapRover](http://caprover.com/)

If you have a [CapRover](http://caprover.com/) server somewhere, you can run the `caprover deploy` command to deploy the project.

Don't forget to set the Container HTTP Port to `3000`.