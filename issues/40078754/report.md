# Security: unicode character can create phishing-friendly address bar

| Field | Value |
|-------|-------|
| **Issue ID** | [40078754](https://issues.chromium.org/issues/40078754) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | UI>Browser>Omnibox |
| **Reporter** | ge...@gmail.com |
| **Assignee** | sk...@chromium.org |
| **Created** | 2014-01-24 |
| **Bounty** | $1,500.00 |

## Description

**VULNERABILITY DETAILS**  

Inserting the Unicode Right-to-Left override character in links allows attackers to construct omnibox displays that result in user confusion that could greatly aid in phishing.

**VERSION**  

Chrome Version: 32.0.1700.76 stable  

Operating System: Windows 8.1

Chrome Version: 31.0.1650.63 stable  

Operating System: Ubuntu Desktop Linux 13.10

**REPRODUCTION CASE**  

HTML file to reproduce attached, note that the issue isn't specific to href anchors, using document.location from JavaScript will result in a similar end result without the user involvement of clicking a link. Screenshot of the end-result attached as well showing omnibox display and devtools to illustrate what is really being hit.

Note that after the link is followed (or the document.location is set), the user is interacting with a page controlled by the attacker (that could trivially be styled to look like the target site though isn't in this demo) but on the address bar he or she appears to be on a different site. Chrome correctly renders font weights to differentiate the hostname from the path, but this detail is unlikely to be noticed by an average user in the face of an otherwise correct looking url.

## Attachments

- [phish.html](attachments/phish.html) (text/html, 106 B)
- [chromephish.jpg](attachments/chromephish.jpg) (image/jpeg, 83.9 KB)
- [phishipvshost.jpg](attachments/phishipvshost.jpg) (image/jpeg, 58.3 KB)
- [main.go](attachments/main.go) (application/octet-stream, 1.5 KB)

## Timeline

### ge...@gmail.com (2014-01-24)

A couple of additional notes:

The incorrect hostname/path order only seems to occur if the hostname of the site serving the malicious link is addressed by ip address.  If I address the host by a DNS resolved hostname, the hostname properly renders first.  See additional attachment for illustration.  Of course, if I am the phisher I could always just forward you to the IP address of the middle-man site hosting the malicious link.

Also, because the omnibox will render any symbols present in the system font, a lock can be added enhancing the https believability if the system font provides such a symbol.  On Windows, the vast majority of users will have Segoe Symbol UI which includes the lock symbol:

<script>
loc = "\u202e=rerrefer?moc.ografsllew.www//:sptth"

if (navigator.appVersion.indexOf("Win")!=-1) {
	loc += "\uD83D\uDD12";
}

document.location = loc;
</script>


### js...@chromium.org (2014-01-24)

@pkasting, do you mind taking a look at this one, or punting it to someone who should?

### ge...@gmail.com (2014-01-24)

Attached code to a small http server written in Go that displays behavior reported to make it easier to reproduce.  To actually use it, the targetIpAddr const on line 14 should be changed to an ip address that would route the chrome user to the server being run.

For example if you're running it on a system with hostname test.chrome.com with ip address of 192.168.1.200 change targetIpAddr to 192.168.1.200, and then hit the server via:

http://test.chrome.com/trick

Server will detect if the incoming host header from chrome looks like an ip address, if it doesn't, it'll redirect them to the ip address version so the omnibox reordering trick will work. 

### me...@chromium.org (2014-01-24)

[Empty comment from Monorail migration]

### pk...@chromium.org (2014-01-24)

@2: I'm going to be out all next week, so I won't be getting to this soon.  You might want to re-assign if you think this deserves quick attention.

### pa...@chromium.org (2014-01-24)

This looks like a solid High-severity spoof, no?

george.mcbay: I'm going to put this up to our vulnerability reward program panel for consideration under our reward program. http://www.chromium.org/Home/chromium-security/vulnerability-rewards-program

Thank you for reporting this!

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

pkasting: Know anyone who might be a good assignee? Is it as simple as stripping out the RTL override character? Are there other characters we should strip out, while we're at it?

### ge...@gmail.com (2014-01-24)

Thanks, and you're welcome for the report.

I suppose the severity rating is a judgement call based on how convincing one believes the spoof to be.  I'm a biased source, of course, but I think it is pretty convincing in the context of being seen by an average user (who probably has no pre-existing reason to suspect foul play), but it isn't a perfect display spoof because of the font weighting and lack of color on the protocol and lock symbol when spoofing https.  

I did play around with some other additive effects like sticking unicode spaces (in the \u200x range) at the end of the spoofed path to smash the actual server host ip off the address bar completely to make the spoofed address even more convincing, and this sorta works, but when inserting too many spaces at the end Chrome places the viewport of the omnibox over to the right which can clip the beginning of the spoofed address, so it becomes difficult to strike a balance of how many spaces to insert (even when knowing the browser client area width) because of variance in dpi/OS magnification of fonts.

FWIW, when presented with the same input Firefox escapes the RTL character, it shows up as %E2%80%AE in the address bar and the rest of the url is "backwards" (which is actually forward relative to how it appears in the original code).  IE keeps the RTL and displays the real path in reverse just like Chrome does, but properly keeps the path to the right of the hostname in all tested cases.  Chrome acts like IE when the hostname is an actual hostname, the damaging part is that when the hostname is an ip address it ends up to the right of the path, making it look like the actual path is the hostname, and vice-versa.

### ms...@chromium.org (2014-01-24)

[Empty comment from Monorail migration]

### me...@chromium.org (2014-01-25)

[Empty comment from Monorail migration]

### sk...@chromium.org (2014-01-25)

I have two proposals
- Render the URL piecewise - hostname and then the path. But I am not sure if this will break any select-copy-paste functionality or may have some non-obvious side-effect.

- Follow Firefox's behavior - Directionality characters {LR,RL}{O,E,M} are useful, but not always entirely necessary. I think it is simpler and less likely to break anything else. For that matter, we should probably escape all invisible unicode characters - spaces (http://www.cs.tut.fi/~jkorpela/chars/spaces.html), ZWNJ etc.

Let me know if I should work on it.

### pk...@chromium.org (2014-01-25)

If piecewise rendering means what I think it means (e.g. using multiple separate RenderTexts) then that's not a good way to go.

I bet the difference between IP address and hostname in this case (i.e. why this works only when the host is an IP) is that the hostname contains strong-LTR characters (Latin) while the IP address doesn't.

It seems like the answer here is to escape invisible characters.  LRM and RLM, in particular, were already noted on https://crbug.com/chromium/296291 (where the possibility of using them for phishing was mentioned, but dismissed, because we weren't thinking enough about RLM), as well as https://crbug.com/chromium/53579, which is the longstanding "omnibox should escape invisible characters" bug that the former is now duped to.

So presumably this should be duped as well, and we should actually fix that old bug.  I believe it's assigned to Jungshik because he's the Unicode expert who knows what "invisible characters" actually means.

### sk...@chromium.org (2014-01-25)

If you think about it, the issue arises because we omit the "http://" from the URL, which allows the possibility of URL starting with weak-directionality chars (numbers!)

I found this Mozilla bug - https://bugzilla.mozilla.org/show_bug.cgi?id=511521, which seems to impact albeit a different scenario. More importantly this seems to be fixed by the code here - http://mxr.mozilla.org/mozilla-central/source/uriloader/exthandler/nsExternalHelperAppService.cpp#1243

But I think we should be escaping the prohibited characters as specified in RFC 3454 - Preparation of Internationalized Strings ("stringprep")  - http://www.ietf.org/rfc/rfc3454.txt.

This list seems to be referenced by various other RFCs - http://mxr.mozilla.org/mozilla-central/search?string=202d&find=rfc.*txt&findi=&filter=%5E%5B%5E%5C0%5D*%24&hitlimit=&tree=mozilla-central

### pk...@chromium.org (2014-01-25)

To a layman like me, using RFC 3454 sounds fine.  That's because I know nothing about it.  I defer to folks who know more.

Again, I'm kinda hoping to move discussion to the older bug on this, unless we think the particular bug here needs a separate or additional fix from the other one.

### sk...@chromium.org (2014-01-27)

The resolution of this should also consider rendering of URLs in Omnibox dropdown.

### dh...@chromium.org (2014-01-28)

[Empty comment from Monorail migration]

### sk...@chromium.org (2014-02-01)

cc:jshin@

So I started with 
http://www.chromium.org/developers/design-documents/idn-in-google-chrome
which refers:
http://src.chromium.org/viewvc/chrome/trunk/src/net/base/net_util.cc (IsIDNComponentSafe)

Further digging revealed : http://www.unicode.org/reports/tr46/
which links to the new set of RFCs for IDNA.

And finally ICU has an implementation of the same:
https://code.google.com/p/chromium/codesearch#chromium/src/third_party/icu/source/common/unicode/uidna.h

I think if there is any error in parsing (See https://code.google.com/p/chromium/codesearch#chromium/src/third_party/icu/source/test/intltest/uts46test.cpp), especially UIDNA_ERROR_DISALLOWED, the IsIDNComponentSafe above should return false.

I am not sure if I should broaden the scope of this fix to this extent. So unassigning myself. I can look at it again, if there is someone knowledgeable to discuss more details.

### fe...@chromium.org (2014-02-05)

[Empty comment from Monorail migration]

### fe...@chromium.org (2014-02-05)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-02-08)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-02-09)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-02-12)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-02-14)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-02-16)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-02-17)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-02-17)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-02-24)

[Empty comment from Monorail migration]

### ge...@gmail.com (2014-02-25)

Is this still being worked on or did rolling it up into an old bug stall it?  

### js...@chromium.org (2014-02-25)

@skanuj - Please do not unassign yourself from a security bug unless you're transferring it to a new owner. This bug has been open almost 30 days already, and needs to be fixed ASAP or it will exceed the 60-day maximum for high severity bugs.


### sk...@chromium.org (2014-02-25)

- I was not aware of any such policy about security bugs. Good to know. But this shouldn't have been difficult to monitor.
- I already explained that I am not in a position to fix this bug. There is no point in assigning it to me again. So please reassign.


### sk...@chromium.org (2014-02-25)

Assigning to David Black.

As per jschuh@, the 1993 team owns the omnibox. But I sure do not have the expertise to solve this bug correctly.


### js...@chromium.org (2014-02-25)

[Empty comment from Monorail migration]

### sk...@chromium.org (2014-02-27)

Finally I have some authoritative answer - http://tools.ietf.org/html/rfc3987#section-4.1

1. The BiDi control characters are not allowed in IRI.
2. Additionally there is a concept of rendering BiDi IRIs as if they are embedded in LRE-PDF. 

1 implies change in net/base/escape.cc to disallow unescaping bidi control chars in the method UnescapeURLWithOffsetsImpl (https://code.google.com/p/chromium/codesearch#chromium/src/net/base/escape.cc&q=escape.cc&sq=package:chromium&l=135)

2 is tricky, because it means modifying the text in omnibox, which in turn requires reverting in case user tries to select all to copy.

### sk...@chromium.org (2014-02-27)

Some related finds:
http://www.w3.org/International/iri-edit/BidiExamples
http://www.w3.org/International/articles/idn-and-iri/

### bu...@chromium.org (2014-02-28)

------------------------------------------------------------------------
r254091 | skanuj@chromium.org | 2014-02-28T10:42:33.953803Z

Changed paths:
   M http://src.chromium.org/viewvc/chrome/trunk/src/net/base/escape_unittest.cc?r1=254091&r2=254090&pathrev=254091
   M http://src.chromium.org/viewvc/chrome/trunk/src/net/base/escape.cc?r1=254091&r2=254090&pathrev=254091
   M http://src.chromium.org/viewvc/chrome/trunk/src/net/base/net_util_unittest.cc?r1=254091&r2=254090&pathrev=254091

Don't unescape BiDi control characters in URL components

As per http://tools.ietf.org/html/rfc3987#section-4.1, the BiDi control
characters are not allowed in IRI.

Add constants for the new BiDi control characters from http://www.unicode.org/reports/tr9/ in rtl.h.

BUG=337746
TBR=rsleevi

Review URL: https://codereview.chromium.org/181483008
------------------------------------------------------------------------

### in...@chromium.org (2014-02-28)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-02-28)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### ti...@chromium.org (2014-03-04)

[Empty comment from Monorail migration]

### la...@google.com (2014-03-05)

[Empty comment from Monorail migration]

### in...@chromium.org (2014-03-05)

We should just let this go in m34. Skanuj@, please merge to m34 branch and flip Merge-Approved to Merge-Merged and add Release-0-M34.

### sk...@chromium.org (2014-03-06)

I don't know about the merge process. Anywhere I can learn about it?

### in...@chromium.org (2014-03-06)

http://www.chromium.org/developers/how-tos/drover

### sk...@chromium.org (2014-03-10)

I am not a committer - That tool seems to be meant for committers.

### bu...@chromium.org (2014-03-10)

------------------------------------------------------------------------
r255997 | mpearson@chromium.org | 2014-03-10T18:43:01.904982Z

Changed paths:
   M http://src.chromium.org/viewvc/chrome/branches/1847/src/net/base/escape_unittest.cc?r1=255997&r2=255996&pathrev=255997
   M http://src.chromium.org/viewvc/chrome/branches/1847/src/net/base/escape.cc?r1=255997&r2=255996&pathrev=255997
   M http://src.chromium.org/viewvc/chrome/branches/1847/src/net/base/net_util_unittest.cc?r1=255997&r2=255996&pathrev=255997

Merge 254091 "Don't unescape BiDi control characters in URL comp..."

on behalf of skanuj@

> Don't unescape BiDi control characters in URL components
> 
> As per http://tools.ietf.org/html/rfc3987#section-4.1, the BiDi control
> characters are not allowed in IRI.
> 
> Add constants for the new BiDi control characters from http://www.unicode.org/reports/tr9/ in rtl.h.
> 
> BUG=337746
> TBR=rsleevi
> 
> Review URL: https://codereview.chromium.org/181483008

TBR=skanuj@chromium.org

Review URL: https://codereview.chromium.org/192973004
------------------------------------------------------------------------

### mp...@chromium.org (2014-03-10)

Add tag per https://crbug.com/chromium/337746#c39.

### ge...@gmail.com (2014-03-14)

Fix looks good in 34.xx, can no longer reproduce on beta channel builds.

### dx...@google.com (2014-03-15)

[Empty comment from Monorail migration]

### ti...@chromium.org (2014-04-05)

[Comment Deleted]

### in...@chromium.org (2014-04-05)

George.mcbay@, how will you like to be credited in the release notes.

### ge...@gmail.com (2014-04-05)

You can just use my name (George McBay), thanks.



### ti...@chromium.org (2014-04-05)

[Comment Deleted]

### ti...@chromium.org (2014-04-05)

[Empty comment from Monorail migration]

### ge...@gmail.com (2014-04-10)

Thanks for the release note credit!

As a first-time security issue submitter to chromium, how does the reward system work... do I have to sign something?



### pa...@chromium.org (2014-04-10)

Adding timwillis to handle the logistics of payout.

### ti...@chromium.org (2014-04-14)

I'll start the payment process today for the $1500. As a first-timer, this means that someone on the Google Finance team should reach out to you this week (or early next week) asking you for account details so that we can pay you.



### ti...@chromium.org (2014-04-14)

[Empty comment from Monorail migration]

### ti...@chromium.org (2014-04-15)

I've started the payment process. Please contact me directly if you haven't heard from the Google Finance team by this time next week.

### ti...@chromium.org (2014-04-28)

Processing via our e-payment system can take a few weeks, but reward should be on its way to you. Please do NOT publicly disclose details until a fix has been released to all our users. Thanks again for your help!

### cl...@chromium.org (2014-06-06)

Bulk update: removing view restriction from closed bugs.

### cl...@chromium.org (2016-02-02)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### la...@chromium.org (2016-12-09)

Security>UX component is deprecated in favor of the Team-Security-UX label

[Monorail components: -Security>UX]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/337746?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/265346, crbug.com/chromium/351536]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40078754)*
