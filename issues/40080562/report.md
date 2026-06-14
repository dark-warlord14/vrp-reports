# Security: SOP Bypass of Data Exfiltration with CSS

| Field | Value |
|-------|-------|
| **Issue ID** | [40080562](https://issues.chromium.org/issues/40080562) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>CSS |
| **Reporter** | fi...@gmail.com |
| **Assignee** | mk...@chromium.org |
| **Created** | 2014-10-01 |
| **Bounty** | $1,337.00 |

## Description

**VULNERABILITY DETAILS**

Brief Description: Webkit/Blink allows a page to load any external resource as  

CSS and will interpret it even if its MIME type is not correct. This allows an  

attacker to exfiltrate data from cross-origin page via CSS string property  

injection with a couple of techniques.

=

The behavior had been discussed before ([https://crbug.com/chromium/9877](https://code.google.com/p/chromium/issues/detail?id=9877)) and was patched later.  

The fix that has been employed is to engage a \*stricter parsing mode\* when  

loading cross-origin resource with incorrect MIME type. In addition, it is  

noticeable that setting the header \*\*X-Content-Type-Options: nosniff\*\* will not  

help browsers refrain from this behavior. The whole process can be summarized as  

follow:

- We can import any type of cross-origin resource as CSS, and browsers will  
  
  parse it
- When doing so, a \*stricter parsing mode\* for CSS is engaged to stop  
  
  potential attacks

Webkit/Blink has adopted the so-called [Minimal Enforcement](http://www.iefans.net/wp-content/uploads/2010/09/css.pdf)(corresponds to  

\*stricter parsing mode\*) as defense. The idea of it is that the parser will stop  

parsing on the first syntactic error. This is effective for most of the cases.

However, there are still possibilities for this attack in extreme cases. The  

[attack limitations](http://scarybeastsecurity.blogspot.hk/2009/12/generic-cross-browser-cross-domain.html) are described below:

1. Insufficient Injection points - the attack requires two injection points,  
   
   \*pre-string\* and \*post-string\*
2. Quotes - data cannot contain both single and double quotes
3. Line Breaks - data cannot contain line breaks

Besides, the imported resource (or at least the content before pre-string) must  

be syntactically correct in CSS due to the patch. Consequently, it is unfeasible  

to perform such an attack in real world scenarios.

=

Unfortunately, during my investigation, I discovered a couple of techniques that  

can make the attack possible in many websites.

If we can control the charset of the target as UTF-16, we can bypass most of the  

limitations. As UTF-16 maps two bytes into one character, it wipes out all the  

ASCII characters in a document (ASCII in UTF-16 requires NUL-byte). As a result,  

quotes and line breaks are eliminated (corresponds to \*point 2 and 3\*  

respectively). Moreover, [CSS allow Unicode characters in range U+00A0 to  

U+10FFFF as identifiers](http://www.w3.org/TR/CSS2/syndata.html#value-def-identifier), which we can abuse to force the content of a  

document into valid CSS syntax. We can even abuse the fact that [blocks can be  

closed with EOF-token](http://www.w3.org/TR/css3-syntax/#consume-a-simple-block0), so that only one injection point is required to  

exfiltrate data (corresponds to \*point 1\*). In fact, if a page does not have  

charset configured in header, it is highly vulnerable to the attack, as [we are  

allowed to decide its charset](http://www.w3.org/TR/css3-syntax/#input-byte-stream). The lack of charset in header is very common  

that it even exists in a [Google's service](https://orkut.google.com/). To sum up, there are two  

requirements to perform this attack:

- The target does not have charset configured in header
- The injection point allows NUL-byte

This is common enough to be exploited in the wild. What is even worse, is that  

if the injection point appears in the first byte of the response body, we can  

insert a \*BOM\* to force the charset into UTF-16 as [it takes the highest  

precedence](http://www.w3.org/TR/css3-syntax/#input-byte-stream) when determining charset.

=

The fix is fairly simple: browsers should refuse to load cross-origin resource  

as CSS if its MIME type is incorrect. Indeed, other browsers like [Internet  

Explorer and Firefox have adopted this approach](https://www.owlfolio.org/htmletc/css-data-theft/).

=

**VERSION**

Chrome Version: 37.0.2062.124 Stable

Operating System: 6.1 (Windows 7, Windows Server 2008 R2)

**REPRODUCTION CASE**

Victim: <http://body.innerht.ml/csstheft/victim_search.php>

PoC: <http://innerht.ml/csstheft/poc_search.html>

In this proof of concept, the attack will be demonstrated to steal a token of a  

form. There is an injection point in the page that is safe from normal XSS  

attacks. Also note that they are cross-origin.

Steps:

1. Open the victim page and check the token in the source code
2. Open the PoC
3. The extracted data will be shown in the page and the console. The result  
   
   should contain the token

Please let me know if you have any question. I will try my best to explain  

everything.

## Timeline

### fi...@gmail.com (2014-10-01)

Sorry for the long paragraph, but I think it is necessary as it is a historical and controversial topic that needs strong evidence.

### fe...@chromium.org (2014-10-01)

+abarth, scarybeasts, lcamtuf from earlier discussion in https://crbug.com/chromium/9877

### fe...@chromium.org (2014-10-01)

[Empty comment from Monorail migration]

### lc...@google.com (2014-10-01)

Well, if others are unconditionally breaking cross-origin CSS with bad C-T these days, no real harm in matching their behavior. 

Although we'd normally advise anyone to always specify charset on any responses that contain anything interesting or user-controlled (and not doing so generally opens you to some other attacks), your utf-16 PoC seems reasonably convincing.

### cl...@chromium.org (2014-10-01)

[Empty comment from Monorail migration]

### fe...@chromium.org (2014-10-02)

[Empty comment from Monorail migration]

### jw...@chromium.org (2014-10-02)

I'm with lcamtuf. Off the cuff, it sounds like we can probably block bad content types given that others are already doing it, although we should probably collect some stats on how often we're seeing this in Blink today.

I'd love to hear abarth's opinion on this, though, before we go too far down this path.

### fe...@chromium.org (2014-10-04)

abarth@, any thoughts?

### ke...@chromium.org (2014-10-07)

We have to lock down this behavior (and more) for site isolation, at least for cross-origin CSS. The ability to load non-CSS resources by claiming it was really CSS would defeat the whole point of that.

One of Charlie's interns last year (Don Jang) had a project looking at how disruptive this would be on the web if we were strict about content-type, and it seemed to come out looking not too bad (something like 0.2% of resource loads were 'potentially disruptive', IIRC). I don't know if he had numbers specifically for cross-origin CSS loads.

### cr...@chromium.org (2014-10-09)

I haven't read this report in detail yet, but we definitely plan to block certain responses based on content type and sniffing, as part of the site isolation effort.

The project Ken alluded to is documented here:
http://www.chromium.org/developers/design-documents/blocking-cross-site-documents
It's partly implemented (but not enforced) in site_isolation_policy.h.

The overall site isolation work is documented here:
http://www.chromium.org/developers/design-documents/site-isolation

### fi...@gmail.com (2014-10-09)

creis@: Not sure if the policy could cover the attack - it seems it will block a cross-site document only if its content type is incorrect and it is confirmed to be  HTML, XML, or JSON by a custom content sniffer. However, the attack actually turns the target into a valid CSS document controlling the charset, thus no sniffing, unless the sniffer ignores charset.

### cl...@chromium.org (2014-10-10)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-10-18)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-10-22)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-10-26)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-10-29)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-10-30)

[Empty comment from Monorail migration]

### fi...@gmail.com (2014-10-31)

Any plan to fix it? It's been a month

### wf...@chromium.org (2014-10-31)

mike - this bug needs an owner, can you help find one?

### cl...@chromium.org (2014-11-08)

mkwst@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2014-11-08)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-11-15)

mkwst@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### mk...@chromium.org (2014-11-17)

I agree with folks above; we should simply stop loading `text/html` as CSS, and suck up the compatibility impact. Given that Firefox already goes this route, I'd expect lowish risk.

I'll put a CL together.

### cl...@chromium.org (2014-11-24)

mkwst@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2014-12-02)

You have far exceeded the 60-day deadline for fixing this high severity security vulnerability.

We commit ourselves to this deadline and appreciate your utmost priority on this issue.

If you are unable to look into this soon, please find someone else to own this.

- Your friendly ClusterFuzz

### fi...@gmail.com (2014-12-13)

Any update? In fact I have found real world scenario where this attack is present. And the exceeded deadline doesn't sound good.

### in...@chromium.org (2015-01-07)

No more M39 patches, moving to M40.

### in...@chromium.org (2015-01-07)

[Empty comment from Monorail migration]

### bu...@chromium.org (2015-02-06)

The following revision refers to this bug:
  http://src.chromium.org/viewvc/blink?view=rev&rev=189669

------------------------------------------------------------------
r189669 | mkwst@chromium.org | 2015-02-06T19:33:32.873233Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/fetch/CSSStyleSheetResource.cpp?r1=189669&r2=189668&pathrev=189669
   M http://src.chromium.org/viewvc/blink/trunk/LayoutTests/http/tests/security/cross-origin-css.html?r1=189669&r2=189668&pathrev=189669
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/fetch/CSSStyleSheetResource.h?r1=189669&r2=189668&pathrev=189669
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/inspector/InspectorPageAgent.cpp?r1=189669&r2=189668&pathrev=189669
   M http://src.chromium.org/viewvc/blink/trunk/LayoutTests/http/tests/inspector/resource-tree/resource-tree-invalid-mime-type-css-content-expected.txt?r1=189669&r2=189668&pathrev=189669
   M http://src.chromium.org/viewvc/blink/trunk/LayoutTests/http/tests/misc/css-accept-any-type-expected.txt?r1=189669&r2=189668&pathrev=189669
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/dom/ProcessingInstruction.cpp?r1=189669&r2=189668&pathrev=189669
   M http://src.chromium.org/viewvc/blink/trunk/LayoutTests/http/tests/misc/css-accept-any-type.html?r1=189669&r2=189668&pathrev=189669
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/css/StyleSheetContents.cpp?r1=189669&r2=189668&pathrev=189669
   D http://src.chromium.org/viewvc/blink/trunk/LayoutTests/http/tests/security/cross-origin-css-expected.txt?r1=189669&r2=189668&pathrev=189669

CSS: Drop the quirks-mode exception for CSS MIME types.

This matches Firefox's behavior (though it returns 'transparent' instead of
'rgba(0, 0, 0, 0)', which is a bit annoying).

BUG=419383

Review URL: https://codereview.chromium.org/733993002
-----------------------------------------------------------------

### bu...@chromium.org (2015-02-06)

The following revision refers to this bug:
  http://src.chromium.org/viewvc/blink?view=rev&rev=189711

------------------------------------------------------------------
r189711 | dpranke@chromium.org | 2015-02-06T23:32:39.509256Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/fetch/CSSStyleSheetResource.h?r1=189711&r2=189710&pathrev=189711
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/inspector/InspectorPageAgent.cpp?r1=189711&r2=189710&pathrev=189711
   M http://src.chromium.org/viewvc/blink/trunk/LayoutTests/http/tests/inspector/resource-tree/resource-tree-invalid-mime-type-css-content-expected.txt?r1=189711&r2=189710&pathrev=189711
   M http://src.chromium.org/viewvc/blink/trunk/LayoutTests/http/tests/misc/css-accept-any-type-expected.txt?r1=189711&r2=189710&pathrev=189711
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/dom/ProcessingInstruction.cpp?r1=189711&r2=189710&pathrev=189711
   M http://src.chromium.org/viewvc/blink/trunk/LayoutTests/http/tests/misc/css-accept-any-type.html?r1=189711&r2=189710&pathrev=189711
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/css/StyleSheetContents.cpp?r1=189711&r2=189710&pathrev=189711
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/http/tests/security/cross-origin-css-expected.txt?r1=189711&r2=189710&pathrev=189711
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/fetch/CSSStyleSheetResource.cpp?r1=189711&r2=189710&pathrev=189711
   M http://src.chromium.org/viewvc/blink/trunk/LayoutTests/http/tests/security/cross-origin-css.html?r1=189711&r2=189710&pathrev=189711

Revert "CSS: Drop the quirks-mode exception for CSS MIME types."

This is a speculative revert to see if it unblocks the Blnk roll;
we're seeing various failures in PPAPI input event tests and
sheriff-o-matic's build triangulation is pointing at this rev.

TBR=mkwst@chromium.org
BUG=419383

Review URL: https://codereview.chromium.org/904143002
-----------------------------------------------------------------

### ts...@chromium.org (2015-02-06)

[Empty comment from Monorail migration]

### dp...@chromium.org (2015-02-07)

Unfortunately, it looks like the patch did cause the test failures; the failing bots have since greened up and the roll has unblocked. Sorry!

### mk...@chromium.org (2015-02-07)

Can you point me at the failing tests? "PPAPI input event tests" isn't very specific. :)

### dp...@chromium.org (2015-02-07)

Sure, I had linked to them in a comment (#10) on your original CL, but repeating here:

https://build.chromium.org/p/chromium.webkit/builders/Mac10.6%20Tests/builds/28273
https://build.chromium.org/p/chromium.webkit/builders/Win7%20Tests/builds/8377

Those two failures bracketed that revision, but they failed across all of the bots in this time frame, e.g.:

https://build.chromium.org/p/chromium.webkit/builders/Linux%20Tests/builds/42371



### mk...@chromium.org (2015-02-07)

Got it. Sorry, I was looking at the revert. I should have checked the original. I have no idea why a change to MIME types for CSS would break PPAPI, but I'll fix it Monday.

Thanks!

### fi...@gmail.com (2015-02-07)

Just a quick question: since the patch is Blink specific but not Webkit, is it okay if I report it to them as well?

### ti...@google.com (2015-02-11)

filedescriptor: You can certainly go ahead and report it to Webkit. 

I've added a Hotlist-Webkit tag to the bug which *should* get their attention, but I can't be sure that it will.

### dd...@apple.com (2015-02-12)

filedescriptor: Do you want to create a bug on bugs.webkit.org with your own account, or would you like me to do it?  (Either way, you need to set up an account on bugs.webkit.org so I can CC you on the bug if you want to track its progress.)  Is copying and pasting https://crbug.com/chromium/419383#c0 okay if I create the bug?


### fi...@gmail.com (2015-02-12)

ddkilzer@: I think it'd be great if you could help doing it (my account is the same  as the one I'm using). Copy and pasting should not be a problem to create the bug.

### dd...@apple.com (2015-02-12)

Filed as:  <https://bugs.webkit.org/show_bug.cgi?id=141501>


### js...@chromium.org (2015-02-13)

Adjusting severity. High-severity would be an unmitigated UXSS, which is clearly not the case here, since there are several preconditions that need to be in alignment. Out of an abundance of caution I'll set it at medium.

### fi...@gmail.com (2015-02-13)

juschuh@: I'm kind of confused. For example: https://code.google.com/p/chromium/issues/detail?id=399951. This one requires user to manually enable a flag yet it has huge constrains and preconditions, and it still triaged as high severity.

### js...@chromium.org (2015-02-13)

The effect of the flag in https://crbug.com/chromium/399951 is reflected in it being impact-none (by default not exposed on any channel) whereas this bug is impact-stable (by default exposed on stable). The severity rating is an assessment of the severity and exploitability for affected releases after accounting for mitigating factors.

### ti...@google.com (2015-02-17)

mkwst: is this on your list to fix today? (In #35 you mentioned that you were Monday, but I'm assuming that you were doing the right thing and honoring US Presidents yesterday).

Bumping to at least M-41, but unlikely it will go out with the first stable.

### ti...@google.com (2015-02-25)

mkwst: any progress here? see #35 and #44 for context. Thanks.

### ti...@google.com (2015-03-16)

@mkwst: Can you please provide an update? (re: #44).

### fi...@gmail.com (2015-03-17)

I've emailed Mike several times but in vein.

### cl...@chromium.org (2015-04-03)

[Empty comment from Monorail migration]

### mb...@chromium.org (2015-04-27)

mkwst: Another ping. Have you had a chance to try to reland this?

### fi...@gmail.com (2015-04-30)

So I've pinged him on Twitter and emailed him multiple times but still can't reach him and it's already >180 days. Hmm...

### ti...@google.com (2015-05-07)

Pinged mkwst using uber secret communication channel.

### ti...@google.com (2015-05-08)

Chatted with mkwst about this briefly yesterday. He's going to update shortly. I'd update on his behalf but I'm likely to accidentally misrepresent his view.

### mk...@chromium.org (2015-05-11)

In a nutshell: I landed a fix in Blink, which was reverted because it broke a number of tests in Chromium. Those tests turn out to break because the piece of testing infrastructure they use doesn't send mime types along with requests. That looks like it's going to be a lot of work to change, and I haven't taken the time to do so.

So, we've got ~3 choices:

1. Disable the tests and fix them in The Future(tm) after landing the change.
2. Fix the server code and then land the change.
3. Something else.

I'll try to look at this again this week, but if anyone else has free time and wants to dig in, I'd appreciate the help.

### bu...@chromium.org (2015-05-12)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/b28d5ba5a59654d9d32e2420c4173483c1a21ac4

commit b28d5ba5a59654d9d32e2420c4173483c1a21ac4
Author: mkwst <mkwst@chromium.org>
Date: Tue May 12 05:47:51 2015

Send proper MIME type along with PPAPI test CSS files.

https://codereview.chromium.org/1126133003 changes the behavior of
Blink CSS file support; we need to send the proper MIME type, even in
quirks mode. This CL fixes the tests which broke when that patch
initially landed way back when.

BUG=419383
TBR=bbudge@chromium.org

Review URL: https://codereview.chromium.org/1136493003

Cr-Commit-Position: refs/heads/master@{#329358}

[modify] http://crrev.com/b28d5ba5a59654d9d32e2420c4173483c1a21ac4/ppapi/BUILD.gn
[modify] http://crrev.com/b28d5ba5a59654d9d32e2420c4173483c1a21ac4/ppapi/ppapi_tests.gypi
[add] http://crrev.com/b28d5ba5a59654d9d32e2420c4173483c1a21ac4/ppapi/tests/test_page.css.mock-http-headers


### bu...@chromium.org (2015-05-12)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/f479194866c3d9e08ef245ed0fdd5b9771ce6195

commit f479194866c3d9e08ef245ed0fdd5b9771ce6195
Author: mkwst <mkwst@chromium.org>
Date: Tue May 12 11:33:29 2015

Add PPAPI test mock headers to *.isolate files.

This should have been part of https://codereview.chromium.org/1136493003.

BUG=419383

Review URL: https://codereview.chromium.org/1139913002

Cr-Commit-Position: refs/heads/master@{#329390}

[modify] http://crrev.com/f479194866c3d9e08ef245ed0fdd5b9771ce6195/chrome/browser_tests.isolate
[modify] http://crrev.com/f479194866c3d9e08ef245ed0fdd5b9771ce6195/chrome/interactive_ui_tests.isolate


### bu...@chromium.org (2015-05-12)

The following revision refers to this bug:
  http://src.chromium.org/viewvc/blink?view=rev&rev=195266

------------------------------------------------------------------
r195266 | mkwst@chromium.org | 2015-05-12T18:29:34.171158Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/fetch/CSSStyleSheetResource.cpp?r1=195266&r2=195265&pathrev=195266
   M http://src.chromium.org/viewvc/blink/trunk/LayoutTests/http/tests/security/cross-origin-css.html?r1=195266&r2=195265&pathrev=195266
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/fetch/CSSStyleSheetResource.h?r1=195266&r2=195265&pathrev=195266
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/inspector/InspectorPageAgent.cpp?r1=195266&r2=195265&pathrev=195266
   M http://src.chromium.org/viewvc/blink/trunk/LayoutTests/http/tests/inspector/resource-tree/resource-tree-invalid-mime-type-css-content-expected.txt?r1=195266&r2=195265&pathrev=195266
   M http://src.chromium.org/viewvc/blink/trunk/LayoutTests/http/tests/misc/css-accept-any-type-expected.txt?r1=195266&r2=195265&pathrev=195266
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/dom/ProcessingInstruction.cpp?r1=195266&r2=195265&pathrev=195266
   M http://src.chromium.org/viewvc/blink/trunk/LayoutTests/http/tests/misc/css-accept-any-type.html?r1=195266&r2=195265&pathrev=195266
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/css/StyleSheetContents.cpp?r1=195266&r2=195265&pathrev=195266
   D http://src.chromium.org/viewvc/blink/trunk/LayoutTests/http/tests/security/cross-origin-css-expected.txt?r1=195266&r2=195265&pathrev=195266

CSS: Drop the quirks-mode exception for CSS MIME types.

This matches Firefox's behavior (though it returns 'transparent' instead of
'rgba(0, 0, 0, 0)', which is a bit annoying).

---------------------------------------------------------------------------
This is a reland of https://codereview.chromium.org/733993002, which was
reverted after breaking tests. https://codereview.chromium.org/1136493003
fixes those tests by sending a correct MIME type for CSS files. The patch
is otherwise identical % rebasing.
---------------------------------------------------------------------------

BUG=419383

Review URL: https://codereview.chromium.org/1126133003
-----------------------------------------------------------------

### mb...@chromium.org (2015-05-14)

Assuming this is fixed by the commits in comments 54-56.

### cl...@chromium.org (2015-05-15)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

Your fix is very close to the branch point. After the branch happens, please make sure to check if your fix is in.

- Your friendly ClusterFuzz

### ti...@google.com (2015-06-12)

Congrats - $1337 for this report.

We'll start payment via our new process (should take 1-2 weeks) from when you see the "reward-inprocess" label on this bug.

### ti...@google.com (2015-06-15)

Fix is in M44 already based on revision numbers - let's roll it with M44.

### ti...@google.com (2015-06-25)

[Empty comment from Monorail migration]

### ti...@google.com (2015-07-24)

Processing via our e-payment system can take up to two weeks, but the reward should be on its way to you. Thanks again for your help!

(Note: sorry for the delay here - it turns out in the new payment system, these payments were waiting for a second approval from me).

### mb...@chromium.org (2015-07-24)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-08-21)

Bulk update: removing view restriction from closed bugs.

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/419383?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40080562)*
