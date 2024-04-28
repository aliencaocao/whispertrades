# Whispertrades API Python Wrapper

## About
[Whispertrades](https://whispertrades.com/) is an advanced automated options trading and backtesting platform. This is an **unofficial** Python wrapper for its [API](https://docs.whispertrades.com/i1-R-overview). It builds on `Pydantic` for strong typing support to ease development, and `requests` library for HTTP requests.

## Installation
### Using pip
```bash
pip install whispertrades
```
### From source (for latest features and development)
```bash
pip install git+https://github.com/aliencaocao/whispertrades
```

## Quick Start
Create an account at [Whispertrades](https://whispertrades.com/) and follow the documentation [here](https://docs.whispertrades.com/i1-R-overview) to apply for an API key.

To ensure security of your API key, it is recommended to store it in an environment variable. You can do this by using `WHISPERTRADES_API_KEY=your_api_key` in your terminal. Else, you can also pass it in when initializing the client.

```python3
from whispertrades import *

client = WTClient(token='YOUR_API_KEY_OR_DO_NOT_PASS_THIS_IF_YOU_HAVE_SET_ENV_VAR')
print(client.bots)
print(client.orders)
print(client.positions)
print(client.reports)
print(client.variables)

bot1 = client.bots['YOUR BOT NUMBER']
print(bot1.orders)  # orders made from this bot
print(bot1.positions)  # positions of this bot
print(bot1.reports)  # reports generated from this bot

# Enable bot
bot1.enable()

# Disable bot
bot1.disable()

# Close all positions of this bot
bot1.close_all_positions()

# Close a particular position by number
client.positions['YOUR POSITION NUMBER'].close()
# OR (making sure the provided position number belongs to the bot)
bot1.positions['YOUR POSITION NUMBER'].close()
```

This project has rate limiting built-in using `requests-ratelimiter` and set to 30 requests per minute, the maximum as stated by [Whispertrades documentation](https://docs.whispertrades.com/i1-R-overview#HnA7L).

## Documentation
https://whispertrades.readthedocs.io/

## Disclaimer
This project is strictly provided as-is with absolutely no guarantee. Neither this project nor Whispertrades is an approved financial advisor or broker. The author is not responsible for any financial loss or damages caused by the use of this project or Whispertrades.

## License
Whispertrades Python API Wrapper © 2024 by Billy Cao is licensed under CC BY 4.0

You are free to:
- Share — copy and redistribute the material in any medium or format for any purpose, even commercially.
- Adapt — remix, transform, and build upon the material for any purpose, even commercially.

Under the following terms:
- Attribution — You must give appropriate credit , provide a link to the license, and indicate if changes were made. You may do so in any reasonable manner, but not in any way that suggests the licensor endorses you or your use.
- No additional restrictions — You may not apply legal terms or technological measures that legally restrict others from doing anything the license permits.