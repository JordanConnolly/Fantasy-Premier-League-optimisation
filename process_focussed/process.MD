# Improvements via Process focussed approach

## Week on Week Fantasy Premier League Team Update using API

To update your Fantasy Premier League team using the API, you can follow these steps:

1. Obtain your API access token from the Fantasy Premier League website.
2. Make a POST request to the appropriate API endpoint, providing your access token and the necessary parameters for the update.
3. Handle the response from the API to ensure the update was successful.
4. Repeat the process as needed to make additional updates to your team.

## Add credentials

On a MAC or Linux machine, you can add the following lines to your `.bashrc` or `.bash_profile` file to set the environment variables for your FPL email, password, and team ID:

```bash
export FPL_EMAIL='your_email@example.com'
export FPL_PASSWORD='your_password'
export FPL_TEAM_ID='your_team_id'
```

then:

```bash
source ~/.bashrc
# or
source ~/.profile
```
