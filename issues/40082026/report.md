# Security: URL Spoof with link in pdf and slow url

| Field | Value |
|-------|-------|
| **Issue ID** | [40082026](https://issues.chromium.org/issues/40082026) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Internals>Plugins>PDF, UI>Browser>Navigation |
| **Reporter** | ch...@gmail.com |
| **Assignee** | rd...@chromium.org |
| **Created** | 2015-05-07 |
| **Bounty** | $2,000.00 |

## Description

**VULNERABILITY DETAILS**  

Chrome changes URL in address bar only after a web page is loaded, when a user clicks on a link.  

But chrome changes the URL in address bar first and then loads the web page, when user clicks on a web link of a PDF file.  

This behavior can be used to spoof a slow to load URL , for a small period of time (Until slow URL is loaded).

**VERSION**  

Chrome Version: [42.0.2311.135 m] + [stable]  

[44.0.2395.0] + [trunk]  

Operating System: [Windows 8.1, Ubuntu 14.04]

**REPRODUCTION CASE**

Required software: Web server with support for PHP.  

Web server should serve content from 127.0.0.1 and 127.0.0.2.  

Enable chrome PDF plugin if it is disabled.

1. Download test.html, link.pdf and delay.php.
2. Host downloaded files on local web server's root folder.
3. Visit <http://127.0.0.1/test.html>.
4. Click on "Visit 127.0.0.2" web link inside PDF file.  
   
   Do this before 10 seconds. Because after 10 seconds contents of web page will change.
5. URL of address bar will change to <http://127.0.0.2/delay.php>.  
   
   <http://127.0.0.2/delay.php> will take 60 seconds to complete it's load.
6. After 10 seconds from step 3, contents of current web page will be changed to a html form.  
   
   URL will remain <http://127.0.0.2/delay.php>.
   
   \* Content (html form) from <http://127.0.0.1> will remain under <http://127.0.0.2/delay.php>, only till <http://127.0.0.2/delay.php> completes loading.

## Attachments

- [delay.php](attachments/delay.php) (text/plain, 37 B)
- [test.html](attachments/test.html) (text/html, 236 B)
- [link.pdf](attachments/link.pdf) (application/pdf, 1.5 KB)

## Timeline

### ri...@chromium.org (2015-05-07)

Thanks for the detailed report! Adding some security UX folks.

Here's a summary of what this looks like:

A user clicks a link on a page, and the URL changes to the target before the target is fully loaded. The page contents can then be replaced in the window of time when the target is loading. The URL bar does not display a lock icon (but it does show https:// if the target is over https) until after the load completes, regardless of whether the origin page or the target page are on HTTPS.

Added a some enamel/PDF folks in case they might know where to send this. I'm marking this as low severity for the moment since it requires user interaction and a sufficiently slow target page, but feel free to to change if folks think otherwise.

### pa...@chromium.org (2015-05-22)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-08-21)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-10-02)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-11-13)

[Empty comment from Monorail migration]

### cl...@chromium.org (2016-01-15)

[Empty comment from Monorail migration]

### cl...@chromium.org (2016-03-03)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-04-14)

[Empty comment from Monorail migration]

### me...@chromium.org (2016-04-26)

Adding navigation label because the original report mentions "slow loading page".

[Monorail components: UI>Browser>Navigation]

### sh...@chromium.org (2016-05-26)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-07-21)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-09-01)

[Empty comment from Monorail migration]

### ra...@chromium.org (2016-09-06)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-13)

[Empty comment from Monorail migration]

### ra...@chromium.org (2016-11-30)

[Empty comment from Monorail migration]

[Monorail components: -Security>UX]

### lg...@chromium.org (2016-11-30)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-12-02)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-01-26)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-03-10)

[Empty comment from Monorail migration]

### me...@chromium.org (2017-04-20)

Has anyone from the navigation team had a chance to look at this bug?

### sh...@chromium.org (2017-04-20)

[Empty comment from Monorail migration]

### cr...@chromium.org (2017-04-28)

I've just verified that this is the same as https://crbug.com/chromium/660498, which was fixed by r431726 and merged to M55.

Since this report seems to have fallen between the cracks and came in before https://crbug.com/chromium/660498, maybe the award panel could take a look at this one as well?  (Not sure if you want to mark it as a duplicate or not.)

### sh...@chromium.org (2017-04-29)

[Empty comment from Monorail migration]

### aw...@google.com (2017-05-05)

The VRP panel decided to use its discretion to award $2,000 for this bug, since although no fix was made, it was reported earlier than https://crbug.com/chromium/660498 which we did fix and reward for. Thanks for the report, chamal.desilva@!

### aw...@chromium.org (2017-05-05)

[Empty comment from Monorail migration]

### ch...@gmail.com (2017-05-06)

Andrew,Creis, Reward Panel,
Thanks a lot for giving a reward for this bug.
I would like to donate this reward to Sri Lanka Red Cross.
http://www.redcross.lk/
I would be thankful if you could directly donate this reward to Sri Lanka Red Cross.

### sh...@chromium.org (2017-08-05)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2017-08-05)

This issue was migrated from crbug.com/chromium/485550?no_tracker_redirect=1

[Multiple monorail components: Internals>Plugins>PDF, UI>Browser>Navigation]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40082026)*
