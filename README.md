# PANKIS.CLICK Backend

## Routes

all routes return a JSON object with the following fields:
- `success` (boolean): A boolean indicating if the request was successful.
- `message` (string): A string with a message about the request.

### GET /account/create
Creates a new account. Requires the following GET parameters:
- `username` (string): The username of the account.
- `password` (string): The password of the account.
- `email` (string): The email of the account.

### GET /account/login
Logs in an account. Requires the following GET parameters:
- `email` (string): The email of the account.
- `password` (string): The password of the account.

returns a JSON object with the following fields:
- `token` (string): The token of the account.

### GET /account/update-stats
Updates the stats of an account. Requires the following GET parameters:
- `token` (string): The token of the account.
- `pancakes` (int): The amount of pancakes the account has.
- `total_pancakes` (int): The total amount of pancakes the account has earned.

### GET /leaderboard
Returns the leaderboard.

returns a JSON list with the following fields:
- `username` (string): The username of the account.
- `pancakes` (int): The amount of pancakes the account has.
- `total_pancakes` (int): The total amount of pancakes the account has earned.
