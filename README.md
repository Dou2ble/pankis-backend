# PANKIS.CLICK Backend

## Routes

all routes return a JSON object with the following fields:
- `success`: A boolean indicating if the request was successful.
- `message`: A string with a message about the request.

### GET /account/create
Creates a new account. Requires the following GET parameters:
- `username`: The username of the account.
- `password`: The password of the account.
- `email`: The email of the account.

### GET /account/login
Logs in an account. Requires the following GET parameters:
- `email`: The email of the account.
- `password`: The password of the account.

returns a JSON object with the following fields:
- `token`: The token of the account.

### GET /account/update-stats
Updates the stats of an account. Requires the following GET parameters:
- `token`: The token of the account.
- `pancakes`: The amount of pancakes the account has.
- `total_pancakes`: The total amount of pancakes the account has earned.

### GET /leaderboard
Returns the leaderboard.