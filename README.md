# Buildapcsales Python Scraper and notifier

This python script will check r/buildapcsales for any new sales in your pre-defined list of keywords and notify you if they are available via text (twilio)

## Getting Started

### Prerequisites

You will need a twilio account and a computer to keep the python script running on. You will also need to setup your developer keys on reddit.

### Running

To run you will need to fill out the config.json and then run the SearchScraper.py script using python.

## Example config.json
```
{
	"search": {
		"type": "GPU",
		"start_price": 0.00,
		"end_price": 500.00,
		"terms": [
			"1070",
			"1080"
		]
	},
	"reddit": {
		"client_key": "xxxxxxxxxxxx",
		"client_secret": "xxxxxxxxxx",
		"username": "xxxxxxxxxx",
		"password": "xxxxxxxxxxxx"
	},
	"twilio": {
		"account_sid": "xxxxxxxxxx",
		"auth_token": "xxxxxxx",
		"receive_phones": [
			"###########"
		]
		"send_phone": "###########"
	},
	"refresh_time": 30
}
```
