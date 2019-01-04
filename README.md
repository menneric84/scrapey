# scrapey

This is a super simple python script that uses beautifulsoup4, twilio, and requests library to scrape a website and send a text and email to myself if a new product arrives.

Libraries can be installed via pip

Data that is scraped is then formatted and put into a csv file (for now). The previous data is checked to make sure that notifications are sent to me only when new items arrive. 

Script doesn't follow proper python formatting standards and contains it's fair share of hardcoded values.
  - Shoudlnt' be used as an example on good coding practices
  
If running a Unix system you can create a shell script that calls your python script. Then call that shell script in a crontab entry using the following command `crontab -e`

Example of a job that runs every 10 minutes */10 * * * * scrapey.sh

Note: This is being considered a finish work for the time being, but will most likely be updated in the future for conding standards and a better how to doc
