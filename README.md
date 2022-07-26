
# Amplifiers of @PolinaPomorenko: a sample of pro-Kremlin Twitter activity

The focus of these sets is on recent retweeters of @PolinaPomorenko, a fairly prominent account in the current pro-Putin Twittersphere.  

## Rationale

Ethically, I believe researchers analysing an information environment with above-average likelihood of state actor interference have a responsibility to report accounts of concern to the relevant platform, and to other researchers. In this model, the task of risk *assessment* rests primarily with the researcher(s), and *investigation and attribution* primarily with the platform - Twitter, in this case. 

This concept is closely in line with Twitter's statement on platform misuse in their [Developer Policy](https://developer.twitter.com/en/developer-terms/policy) where they say: 

> We support research that helps improve conversational health on Twitter

Adding that researchers:

>may use the Twitter API and Twitter Content to measure and analyse topics like spam, abuse, or other platform health-related topics for non-commercial research purposes.


### Notes on data limitations

Some level of data sharing is crucial to enable peer review, repeatability and to allow other researchers to benefit.
However, in accordance with Twitter's [Developer Policy](https://developer.twitter.com/en/developer-terms/policy), I can publish only nonhydrated Twitter User IDs, not raw Twitter JSON data.

Access to the associated account data will therefore require hydration. 

The included Python scripts provide for this. [Here](https://towardsdatascience.com/learn-how-to-easily-hydrate-tweets-a0f393ed340e) is a useful guide on how to hydrate using third-party validated tools. Additionally, I have included in this set a text file of hyperlinks that will take you directly to the Twitter profile of any active account in a normal web browser.

### Datasets

1. pp_amplifiers_category_B_IDs_24-07-22.txt: contains 174 Twitter User IDs of accounts that amplified @PolinaPomorenko in Category B (see below), parsed July 24th 2022
2. pp_amplifiers_category_B_profile_links_27-07-22.txt: contains hyperlinks to the associated Twitter page for each active account in (1) above, parsed July 27th 2022
3. pp_amplifiers_category_C_IDs_24-07-22.txt: contains 426 Twitter User IDs of accounts that amplified @PolinaPomorenko in Category C (see below), parsed July 24th 2022

### Account categories

I will employ the following designations going forward:

- Category A: accounts which have been attributed with high confidence, in published research, to Russian state-linked actors  
- Category B: accounts which have amplified a notable pro-Kremlin account *and also* have at least 1 indicator of possible co-ordination or inauthenticity (see below for list)
- Category C: accounts which have amplified a notable pro-Kremlin account, including those *without* indicators of inauthenticity

As yet, there are no confirmed accounts in Category A. It's worth following [the Information Operations page of Twitter Transparency.](https://transparency.twitter.com/en/reports/information-operations.html) for any updates. Category C is a broad list, which can (for example) be used to gather wider interaction networks via a Gephi stream listener.

### Indicators of possible co-ordination or inauthenticity

Primarily, and in estimated order of reliability:

1. A [Botometer API](https://botometer.osome.iu.edu/) CAP (complete automation probability) score of 0.80 or greater
2. A disproportionate number of tweets relative to friend and follower numbers, quantified as *(fr+fl)/t*
3. Membership of a set of accounts created within a short period of time (i.e, an account registration spike)
4. Presence of six or more digits in the account username (e.g, somename458673)
5. A username composed of multiple alphanumeric bigrams in a hash-like random string arrangement (e.g, f5hg7hdl0hkmxj2)


### Important note regarding indicators

It is important to emphasize that no single indicator is **proof** that a given account is a bot or a troll - much less that it is linked to any state actors. 
Rather, such indicators, particularly in combination, represent an *increased probability* that a given account is inauthentic, automated or part of a co-ordinated campaign, particularly within an information space where such accounts are more common.
Authentic users can and do create accounts with random or numeric usernames; it therefore follows that some individual-run "organic" pro-Kremlin accounts will also appear in these datasets.

### Python scripts

Usage requires basic knowledge of both Python and the Twitter API.

- botometer_usernames.py: using the[Botometer API](https://botometer.osome.iu.edu/), produces a CSV file of the automation probability for each account, given a text file of usernames
- get_account_data.py: takes a text file of user IDs or user names and creates a CSV file of metadata for active accounts, and suspended/deleted status for absent accounts
- report_block.py: automatically blocks (and optionally reports as spam) a text file of account IDs or usernames. For example, `python report_block.py --file bots-galore.txt --report --block`
- username_metrics.py: produces a CSV file quantifying specific aspects of account usernames. Used in indicators 4 and 5 above.
