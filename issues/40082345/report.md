# Security: improperly escaped "saved from url" info allows modification of saved pages

| Field | Value |
|-------|-------|
| **Issue ID** | [40082345](https://issues.chromium.org/issues/40082345) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Blink>Editing |
| **CVE IDs** | CVE-2015-6784 |
| **Reporter** | in...@gmail.com |
| **Assignee** | yo...@chromium.org |
| **Created** | 2015-06-22 |
| **Bounty** | $500.00 |

## Description

**This template is ONLY for reporting security bugs. Please use a different**  

**template for other types of bug reports.**

**Please see the following link for instructions on filing security bugs:**  

**<http://www.chromium.org/Home/chromium-security/reporting-security-bugs>**

**VULNERABILITY DETAILS**  

Whenever we save a webpage to our local storage, the following bit of information is added to the source:

<!-- saved from url=(0055){URL}-->

The {URL} parameter is not escaped. An attacker could append "-->" to break the HTML comment, and then insert malicious information or scripts.

**VERSION**  

Chrome Version: Version 43.0.2357.124 m  

Operating System: Windows 8

**REPRODUCTION CASE**

1. Go to [https://www.google.com#-->](https://www.google.com#--%3E)<script>alert("whoops")</script><--
2. Save the page
3. Open the page

## Attachments

- [poc_screenshot.png](attachments/poc_screenshot.png) (image/png, 72.3 KB)
- [poc.zip](attachments/poc.zip) (application/zip, 26.3 KB)

## Timeline

### es...@chromium.org (2015-06-22)

Can you please outline an attack scenario? It seems to me that if the user is downloading a page and then opening it, the page can already include whatever malicious content it wants, and doesn't need to insert it via the HTML comment with the URL.

### es...@chromium.org (2015-06-22)

[Empty comment from Monorail migration]

### in...@gmail.com (2015-06-22)

Obviously the page itself can include malicious content, but we're talking about a universal issue that occurs when saving legit sites such as Google.com as well. Using this, an attacker can inject the malicious content into sites the user trusts.

Simple attack scenario:
1. A trusted online HTML page includes a list of bank account numbers
2. Attacker sends this (legit, trusted) page to the victim, but appends a script that'd change an account number to his account number
3. Victim checks the page, verifies it's legit saves the page for offline use
4. Once the victim opens the saved trusted page locally, the account number has changed

It's a matter of trust. An attacker shouldn't be able to mess with extern webpages such as Google when they're saved locally.

### es...@chromium.org (2015-06-22)

Ah, I see, thanks for the explanation.

eae@, do you think you could please take a look at this?

### in...@gmail.com (2015-06-23)

[Comment Deleted]

### in...@gmail.com (2015-06-23)

[Comment Deleted]

### in...@gmail.com (2015-06-23)

[Comment Deleted]

### in...@gmail.com (2015-06-23)

Some additional info: 
It seems this'll only works when inserting the payload after the hashtag. Parameters in the url will be properly encoded.
Here's another PoC on Google.com that'll change the actual data

http://www.google.com/about/company/facts/management/#--><script>window.onload=function(){document.getElementsByTagName("h1")[1].innerHTML="Helloworld!1!!!!1!";document.getElementById("larry").innerHTML="IntiDC";document.getElementsByTagName("img")[1].src="https://c4.staticflickr.com/4/3828/13622229425_92c7489401_n.jpg"}</script><!--

Just save and open to see it happen

### in...@gmail.com (2015-06-23)

Just realized this can be used to leak data. An attacker'd simply need to insert a script that'd send the body of a webpage to the attacker's server.

### in...@gmail.com (2015-06-24)

I dug into this a bit and believe I have found the cause.

In WebPageSerializer.cpp:

WebString WebPageSerializer::generateMarkOfTheWebDeclaration(const WebURL& url)
{
    return String::format("\n<!-- saved from url=(%04d)%s -->\n",
                          static_cast<int>(url.spec().length()),
                          url.spec().data());
}

This prints the URL expecting it's URL encoded. Part after the hashtag won't be URL encoded, so we'd need to escape or encode this part.

### in...@gmail.com (2015-06-25)

Found another possible payload using the "downloads" feature. Doesn't look as exploitable as the first one, but still worth looking into

Example link:
http://www.example.com/#"><script>alert(0)</script>

Save the page, go to "Downloads", save the downloads page, open the downloads page. Javascript will execute (and we'll be able to steal the downloads)

### in...@gmail.com (2015-06-25)

Another interesting one: we can use the browsing history to inject the malicious scripts (and to steal the browsing history).

An attacker can make the victim navigate to

http://example.com/#" onmouseover="alert(0)" style="position:absolute;width:100%;height:2000px;z-index:99;top:0;left:0

The victim doesn't need to save the page - as long as this URL is logged in the browsing history. Victim now saves the browsing history page and opens it. The script will run. Only thing the victim'd have to do is to save and open the browsing history.

### es...@chromium.org (2015-06-25)

eae@, are you able to look into these or help find another owner? I assigned you originally because it looked like you had been the last person to touch the code that generates the "saved from url" string.

### in...@gmail.com (2015-07-05)

So it has been two weeks. Any update?

I think this is an interesting and exploitable vulnerability so I'd really like to get someone to triage/prioritize this. eae@ seems to be out of office for a while, so could someone reassign this one?

### es...@chromium.org (2015-07-06)

dcheng@: do you think you might able to help find an owner for this?

### in...@chromium.org (2015-07-06)

gustav.tiger@sonymobile.com, i think your https://crbug.com/chromium/328354 should fix this ? Or since you are already looking into the rewrite, can you please take a look at this one as well.

### gu...@sonymobile.com (2015-07-06)

inferno@: It should indeed fix this problem. I'm hoping to re-land the final commit in a day or two. I'll update here as things progress.

### in...@chromium.org (2015-07-06)

Thanks!

### gu...@sonymobile.com (2015-07-09)

https://src.chromium.org/viewvc/blink?revision=198151&view=revision has been merged for almost a day now so this bug should not be an issue anymore. I'll close #328354 once I've re-enabled the tests that where disabled during the merge.

### cl...@chromium.org (2015-07-10)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-07-30)

gustav.tiger@: Uh oh! This issue is still open and hasn't been updated in the last 21 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### in...@gmail.com (2015-08-06)

So what's next? Other bug is closed with the 'verified' status.

### gu...@sonymobile.com (2015-08-11)

I tried to verify this today but apparently this still exists. It looks like MarkupFormatter::appendComment doesn't escape the content (which I also see that it states in a comment in the function). 

So the issue is still reproducible. I just assumed that it would indeed fix the problem. Sorry for not verifying this at the time. Can someone else take a look at htis?

### in...@gmail.com (2015-08-13)

This behaviour affects the following functions

MarkupFormatter::appendComment
MarkupFormatter::appendProcessingInstruction
MarkupFormatter::appendCDATASection

Seems like XMLSerializer is expected to throw an exception when it includes "-->", which, in the "saved from url" case, seems a bit silly. I'd just escape the content then.

Not too sure who should be assigned to this issue. Can somebody help out please?

### in...@gmail.com (2015-08-19)

gustav.tiger@ - do you happen to know anyone that can possibly take care of this (and put them in CC)? I'm not skilled enough to tackle this one myself, otherwise I'd do it. Thanks!

### cl...@chromium.org (2015-08-21)

[Empty comment from Monorail migration]

### gu...@sonymobile.com (2015-08-31)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-08-31)

hajimehoshi@: Uh oh! This issue is still open and hasn't been updated in the last 56 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### ha...@chromium.org (2015-09-07)

yosin: Could you take a look?

### in...@gmail.com (2015-09-08)

This just got more severe. Wrote a PoC that can extract:

- Local file/folder structure
- Facebook messages
- Mails

User interaction is a mitigating factor. Even though the exploit files are downloaded automatically, the victim still needs to open "app.htm" and follow the instructions (save and open).

Unlisted video: https://www.youtube.com/watch?v=w660gE_1HFY

PoC and screenshot attached

### yo...@chromium.org (2015-09-28)

[Empty comment from Monorail migration]

### yo...@chromium.org (2015-09-30)

[Empty comment from Monorail migration]

### yo...@chromium.org (2015-09-30)

In review: https://codereview.chromium.org/1371323003/

### bu...@chromium.org (2015-10-01)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/a81593e7f162428585832ac8f6e71f75592b53e7

commit a81593e7f162428585832ac8f6e71f75592b53e7
Author: yosin <yosin@chromium.org>
Date: Thu Oct 01 05:57:30 2015

Escape "--" in the page URL at page serialization

This patch makes page serializer to escape the page URL embed into a HTML
comment of result HTML[1] to avoid inserting text as HTML from URL by
introducing a static member function |PageSerialzier::markOfTheWebDeclaration()|
for sharing it between |PageSerialzier| and |WebPageSerialzier| classes.

[1] We use following format for serialized HTML:
saved from url=(${lengthOfURL})${URL}

BUG=503217
TEST=webkit_unit_tests --gtest_filter=PageSerializerTest.markOfTheWebDeclaration
TEST=webkit_unit_tests --gtest_filter=WebPageSerializerTest.fromUrlWithMinusMinu

Review URL: https://codereview.chromium.org/1371323003

Cr-Commit-Position: refs/heads/master@{#351736}

[modify] http://crrev.com/a81593e7f162428585832ac8f6e71f75592b53e7/third_party/WebKit/Source/core/page/PageSerializer.cpp
[modify] http://crrev.com/a81593e7f162428585832ac8f6e71f75592b53e7/third_party/WebKit/Source/core/page/PageSerializer.h
[modify] http://crrev.com/a81593e7f162428585832ac8f6e71f75592b53e7/third_party/WebKit/Source/web/WebPageSerializer.cpp
[modify] http://crrev.com/a81593e7f162428585832ac8f6e71f75592b53e7/third_party/WebKit/Source/web/tests/PageSerializerTest.cpp
[modify] http://crrev.com/a81593e7f162428585832ac8f6e71f75592b53e7/third_party/WebKit/Source/web/tests/WebPageSerializerTest.cpp
[add] http://crrev.com/a81593e7f162428585832ac8f6e71f75592b53e7/third_party/WebKit/Source/web/tests/data/pageserialization/text_only_page.html


### yo...@chromium.org (2015-10-01)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-10-01)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

Your fix is very close to the branch point. After the branch happens, please make sure to check if your fix is in.

- Your friendly ClusterFuzz

### in...@gmail.com (2015-10-11)

yosin@: thanks for the fix, tested and confirmed, however, some chrome:// functionalities still allow HTML/JS to be injected upon saving a page (see #11 and #12).

User interaction is considerably higher in these cases, but as it can lead to (download)history theft, I'd fix it.

### in...@gmail.com (2015-10-11)

I dug into this and believe this is a different rendering issue (not chrome:// related) causing links like http://www.google.com#"><script>alert(0)</script> to execute JS when saved.

Created ticket #542054 as I believe they're seperate issues.

### ti...@google.com (2015-10-12)

Fix is already in M-47 based on revision number. Leaving Merge-Triage on this bug to consider a post-stable M-46 merge after some more baketime in M47.

### ti...@google.com (2015-10-12)

[Empty comment from Monorail migration]

### ti...@google.com (2015-11-23)

[Empty comment from Monorail migration]

### ti...@google.com (2015-12-01)

Updating severity.

### in...@gmail.com (2015-12-01)

[Comment Deleted]

### in...@gmail.com (2015-12-01)

[Comment Deleted]

### in...@gmail.com (2015-12-01)

I'm not entirely sure about the severity change. Yes, this bug does require some user interaction but it also allows the  leakage and modification of anything on a saved page, see poc given in #30, including facebook messages, emails, (and thus also CSRF tokens) and even local folders and files. If I'm correct this last thing isn't even possible with a regular UXSS. Note that these files are also auto downloaded so open and save is really the  only thing a victom should do. Using the iframe trick, also demonstrated in the PoC, the payload or even the webpage we steal the content from will never be visible.

### ti...@google.com (2015-12-01)

Hey Inti, this was updated based on the preconditions for a successful exploitation and at the recommendation of the reward panel. The panel noted that successful exploitation would require significant user interaction, page injection control and "save as". 

That said, it's definitely worth fixing and the panel awarded you $500 for taking the time effort to report this issue to us. I see that you're already registered on our end for payment so I'll add that reward into our next payment run.

We'll also list you in our release notes as "Inti De Ceukelaire". Please let me know if you would prefer to use another name for credit and I can update the release notes. I'll also follow up with a CVE ID in a few hours time for your reference.


### in...@gmail.com (2015-12-01)

Ah I see. Thanks for the explanation and reward! I can blog about this once the fix is released on stable, right? "Inti De Ceukelaire" is fine. Thanks!

### ti...@google.com (2015-12-01)

No worries - thanks for your help! Usually we ask for our security researchers to wait a few weeks after stable release (scheduled for tomorrow) to give users time to update. That said, if you have something lined up and would like to publish earlier, let me know and I can make this bug public so that you can link to it.

### ti...@google.com (2015-12-01)

CVE-2015-6784

### ti...@google.com (2015-12-14)

[Empty comment from Monorail migration]

### ti...@google.com (2016-01-05)

[Empty comment from Monorail migration]

### cl...@chromium.org (2016-01-07)

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

### sh...@chromium.org (2018-07-28)

[Empty comment from Monorail migration]

### is...@google.com (2018-07-28)

This issue was migrated from crbug.com/chromium/503217?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail blocked-on: crbug.com/chromium/328354]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40082345)*
