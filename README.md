# LBP/USD Scraper

A python script that scrapes the value of the Dollar against the LBP at the shadow market rate, then stores the values in a mongoDB cluster (to be used in my upcoming "Dashboard" project).
I created and hosted a Lambda function and scheduled it to run every hour using CloudWatch.

Docker repo and image can be found [here](https://hub.docker.com/r/zakjanzi/lbp-scraper) .


# Test it

You can test it by invoking the function on [my website](https://zakjanzi.me/). Click the "Send Request" button to run the function and retrieve the current price of the USD-LBP pair.

