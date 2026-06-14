# UXSS from a local MHTML file

| Field | Value |
|-------|-------|
| **Issue ID** | [40078601](https://issues.chromium.org/issues/40078601) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink, Blink>SavePage |
| **Reporter** | pa...@gmail.com |
| **Assignee** | jc...@chromium.org |
| **Created** | 2013-12-25 |
| **Bounty** | $1,000.00 |

## Description

## Sorry for my bad English, lol

**VULNERABILITY DETAILS**  

Files in .mht and .mhtml formats can execute any javascript code in the context of any domain. It's not enough for the majority of Chromium-based browsers but it is enough for Opera on Mac OS for example which opens mht files itself.

Because it's difficult to make user simply open an mht file, a solution was found in the form of html file that automatically downloads mht file and loads it in iframe, in which the mht file is still executed. Because html files are opened using a default browser this vulnerability exists not only in Opera.

Perfect condition for reproduce is automatical file downloading.  

On loading mht file from any site in iframe it will automatically downloaded in local /Downloads folder, where probably shall be previously downloaded html file.  

After mht file downloading we able to insert it in iframe where it will execute successfully.

We can refer to Chromium warning "this type of file can harm to blah-blah-blah", but user can open html download link from any other app (iMessage, rss-feed, tweetbot, etc) and downaload html file without any warnings, because it's not transfer any refer. Anyway everybody will press "keep" button, when chrome warn.. (:

Thus, user who opened link from external app and isn't changed default browser download settings is almost 100% vulnerable.

For demonstration, i attached mht and html files, which must save in one folder, and then open html file

Live demonstration: <http://package.su/exploit.php>

**VERSION**  

All version of Chromium, which support .mht files

## Attachments

- [test.html](attachments/test.html) (text/html, 32 B)

## Timeline

### pa...@gmail.com (2013-12-25)

[Empty comment from Monorail migration]

### pa...@gmail.com (2013-12-25)

.mht dosent attachements




MIME-Version: 1.0
Content-Type: multipart/related;
	boundary="----"

------
Content-Type: text/html;

<iframe src="http://google.com/test.html"></iframe>
------
Content-Type: text/html
Content-Location: http://google.com/test.html

<script>alert(document.cookie)</script>
--------

### mb...@chromium.org (2013-12-26)

The main issue here is the MHTML UXSS bug. I was able to reproduce this on Chrome OS by simply downloading and opening a similar mht file. There was no warning before downloading the mht file, and the alert box showing document.cookie was displayed after opening it. I'm marking this as medium instead of high severity since it still requires a user to download and open a local file.

### pa...@gmail.com (2013-12-27)

In google chrome for Mac OS nth file downloading without warning, it's problem

### pa...@gmail.com (2013-12-27)

Mht*

### js...@chromium.org (2013-12-27)

@jcivelli - MHT files should not be able specify origins. That breaks the download security mechanisms we have around local files.

### cl...@chromium.org (2014-01-04)

jcivelli@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2014-01-13)

jcivelli@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### jc...@chromium.org (2014-01-13)

I am really busy with 2 other tasks at the moment, also time constrained.
I can look at it after that.
Or if anyone wants to take over this bug.


### cl...@chromium.org (2014-01-22)

jcivelli@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### me...@chromium.org (2014-01-25)

[Empty comment from Monorail migration]

### [Deleted User] (2014-01-28)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-01-30)

jcivelli@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2014-02-07)

jcivelli@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### js...@chromium.org (2014-02-08)

[Empty comment from Monorail migration]

### js...@chromium.org (2014-02-08)

@jcivelli - You wrote the MHTML code, and are essentially the sole owner. If you don't have time to work on it, then find someone who is either familiar or willing to learn it, or land a patch to simply disable MHT support. But we can't have serious security vulnerabilities sitting open for months at a time.


### jc...@chromium.org (2014-02-08)

@jschuh
OK, looking at it now.

I'll also try to find if someone interested in taking over for future bugs, and if I find no one, I'll disable/remove MHTML.

 


### js...@chromium.org (2014-02-09)

@jcivelli - Thanks. Ideally you'll be able to find someone to take ownership of the code since it sounds like you won't be working on it in the future. Sorry if it sounds like we're taking a hard line, but we've been bitten very badly in the past by security vulnerabilities in unowned code.

### jc...@chromium.org (2014-02-10)

I have a patch that only enables MHTML to be loaded for the top frame and disables JavaScript in the page.
Does that sound good?

(I still need to fix the layout tests before I send that patch for review, disabling JS breaks the text-only tests)

### js...@chromium.org (2014-02-10)

That sufficient to me.

### cl...@chromium.org (2014-02-17)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-02-19)

jcivelli@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### jc...@chromium.org (2014-02-19)

Patch ready and LGTMed.
Figuring out why the trybots are failing.
Should land shortly.


### in...@chromium.org (2014-02-19)

[Empty comment from Monorail migration]

### bu...@chromium.org (2014-03-20)

The following revision refers to this bug:
  http://src.chromium.org/viewvc/blink?view=rev&rev=169499

------------------------------------------------------------------
r169499 | jcivelli@chromium.org | 2014-03-18T23:22:33.505652Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/trunk/LayoutTests/mhtml/multi_frames_unmht.mht?r1=169499&r2=169498&pathrev=169499
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/mhtml/resources/frame_4.html?r1=169499&r2=169498&pathrev=169499
   D http://src.chromium.org/viewvc/blink/trunk/LayoutTests/mhtml/invalid-bad-boundary2-expected.txt?r1=169499&r2=169498&pathrev=169499
   D http://src.chromium.org/viewvc/blink/trunk/LayoutTests/mhtml/check_domain.mht?r1=169499&r2=169498&pathrev=169499
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/mhtml/multi_frames_binary-expected.html?r1=169499&r2=169498&pathrev=169499
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/mhtml/relative_url-expected.html?r1=169499&r2=169498&pathrev=169499
   M http://src.chromium.org/viewvc/blink/trunk/LayoutTests/mhtml/page_with_image.html_original?r1=169499&r2=169498&pathrev=169499
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/mhtml/simple_page_ie-expected.html?r1=169499&r2=169498&pathrev=169499
   M http://src.chromium.org/viewvc/blink/trunk/LayoutTests/mhtml/transfer_encoding_7bit.mht?r1=169499&r2=169498&pathrev=169499
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/mhtml/mhtml_in_iframe-expected.txt?r1=169499&r2=169498&pathrev=169499
   M http://src.chromium.org/viewvc/blink/trunk/LayoutTests/mhtml/page_with_image_unmht.mht?r1=169499&r2=169498&pathrev=169499
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/mhtml/page_with_css_and_js_ie-expected.html?r1=169499&r2=169498&pathrev=169499
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/mhtml/relaxed-content-type-parameters-expected.html?r1=169499&r2=169498&pathrev=169499
   D http://src.chromium.org/viewvc/blink/trunk/LayoutTests/mhtml/multi_frames_unmht-expected.txt?r1=169499&r2=169498&pathrev=169499
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/mhtml/invalid-bad-boundary2-expected.html?r1=169499&r2=169498&pathrev=169499
   M http://src.chromium.org/viewvc/blink/trunk/LayoutTests/mhtml/relaxed-content-type-parameters.mhtml_original?r1=169499&r2=169498&pathrev=169499
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/mhtml/transfer_encoding_7bit-expected.html?r1=169499&r2=169498&pathrev=169499
   D http://src.chromium.org/viewvc/blink/trunk/LayoutTests/mhtml/new-image-not-in-archive.mht?r1=169499&r2=169498&pathrev=169499
   M http://src.chromium.org/viewvc/blink/trunk/LayoutTests/mhtml/invalid-bad-boundary.mht?r1=169499&r2=169498&pathrev=169499
   M http://src.chromium.org/viewvc/blink/trunk/LayoutTests/mhtml/shared_buffer_bug.mht?r1=169499&r2=169498&pathrev=169499
   D http://src.chromium.org/viewvc/blink/trunk/LayoutTests/mhtml/base_url.mht?r1=169499&r2=169498&pathrev=169499
   M http://src.chromium.org/viewvc/blink/trunk/LayoutTests/mhtml/page_with_css_and_js.html_original?r1=169499&r2=169498&pathrev=169499
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/mhtml/page_with_javascript.mht?r1=169499&r2=169498&pathrev=169499
   M http://src.chromium.org/viewvc/blink/trunk/LayoutTests/mhtml/simple_page_unmht.mht?r1=169499&r2=169498&pathrev=169499
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/mhtml/resources/frame_1.html?r1=169499&r2=169498&pathrev=169499
   D http://src.chromium.org/viewvc/blink/trunk/LayoutTests/mhtml/relaxed-content-type-parameters-expected.txt?r1=169499&r2=169498&pathrev=169499
   M http://src.chromium.org/viewvc/blink/trunk/LayoutTests/mhtml/content_transfer_encoding_none.mht?r1=169499&r2=169498&pathrev=169499
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/mhtml/invalid-bad-boundary-expected.html?r1=169499&r2=169498&pathrev=169499
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/mhtml/mhtml_in_iframe.html?r1=169499&r2=169498&pathrev=169499
   M http://src.chromium.org/viewvc/blink/trunk/LayoutTests/mhtml/page_with_css_and_js_unmht.mht?r1=169499&r2=169498&pathrev=169499
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/mhtml/page_with_javascript-expected.html?r1=169499&r2=169498&pathrev=169499
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/mhtml/resources/style.css?r1=169499&r2=169498&pathrev=169499
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/mhtml/content_transfer_encoding_none-expected.html?r1=169499&r2=169498&pathrev=169499
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/mhtml/multi_frames_ie-expected.html?r1=169499&r2=169498&pathrev=169499
   D http://src.chromium.org/viewvc/blink/trunk/LayoutTests/mhtml/new-image-not-in-archive-expected.txt?r1=169499&r2=169498&pathrev=169499
   D http://src.chromium.org/viewvc/blink/trunk/LayoutTests/mhtml/multi_frames_binary-expected.txt?r1=169499&r2=169498&pathrev=169499
   M http://src.chromium.org/viewvc/blink/trunk/LayoutTests/mhtml/page_with_image_ie.mht?r1=169499&r2=169498&pathrev=169499
   D http://src.chromium.org/viewvc/blink/trunk/LayoutTests/platform/win/mhtml?r1=169499&r2=169498&pathrev=169499
   D http://src.chromium.org/viewvc/blink/trunk/LayoutTests/mhtml/multi_frames_ie-expected.txt?r1=169499&r2=169498&pathrev=169499
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/mhtml/transfer_encoding_8bit-expected.html?r1=169499&r2=169498&pathrev=169499
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/mhtml/resources/frame_2.html?r1=169499&r2=169498&pathrev=169499
   A http://src.chromium.org/viewvc/blink/trunk/Source/web/tests/data/mhtml?r1=169499&r2=169498&pathrev=169499
   M http://src.chromium.org/viewvc/blink/trunk/LayoutTests/mhtml/simple_page_ie.mht?r1=169499&r2=169498&pathrev=169499
   D http://src.chromium.org/viewvc/blink/trunk/LayoutTests/mhtml/transfer_encoding_7bit-expected.txt?r1=169499&r2=169498&pathrev=169499
   D http://src.chromium.org/viewvc/blink/trunk/LayoutTests/mhtml/transfer_encoding_8bit-expected.txt?r1=169499&r2=169498&pathrev=169499
   M http://src.chromium.org/viewvc/blink/trunk/LayoutTests/mhtml/page_with_css_and_js_ie.mht?r1=169499&r2=169498&pathrev=169499
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/loader/DocumentLoader.cpp?r1=169499&r2=169498&pathrev=169499
   D http://src.chromium.org/viewvc/blink/trunk/LayoutTests/mhtml/page_with_image_ie-expected.txt?r1=169499&r2=169498&pathrev=169499
   M http://src.chromium.org/viewvc/blink/trunk/LayoutTests/mhtml/relaxed-content-type-parameters.mht?r1=169499&r2=169498&pathrev=169499
   M http://src.chromium.org/viewvc/blink/trunk/LayoutTests/mhtml/frame_4.html_original?r1=169499&r2=169498&pathrev=169499
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/mhtml/multi_frames_unmht-expected.html?r1=169499&r2=169498&pathrev=169499
   A http://src.chromium.org/viewvc/blink/trunk/Source/web/tests/data/mhtml/simple_test.mht?r1=169499&r2=169498&pathrev=169499
   D http://src.chromium.org/viewvc/blink/trunk/LayoutTests/mhtml/invalid-bad-boundary-expected.txt?r1=169499&r2=169498&pathrev=169499
   D http://src.chromium.org/viewvc/blink/trunk/LayoutTests/mhtml/simple_page_ie-expected.txt?r1=169499&r2=169498&pathrev=169499
   D http://src.chromium.org/viewvc/blink/trunk/LayoutTests/mhtml/content_transfer_encoding_none-expected.txt?r1=169499&r2=169498&pathrev=169499
   M http://src.chromium.org/viewvc/blink/trunk/Source/web/web.gypi?r1=169499&r2=169498&pathrev=169499
   D http://src.chromium.org/viewvc/blink/trunk/LayoutTests/mhtml/check_domain-expected.txt?r1=169499&r2=169498&pathrev=169499
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/mhtml/page_with_image_unmht-expected.html?r1=169499&r2=169498&pathrev=169499
   D http://src.chromium.org/viewvc/blink/trunk/LayoutTests/mhtml/page_with_css_and_js_ie-expected.txt?r1=169499&r2=169498&pathrev=169499
   M http://src.chromium.org/viewvc/blink/trunk/LayoutTests/mhtml/multi_frames_ie.mht?r1=169499&r2=169498&pathrev=169499
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/mhtml/shared_buffer_bug-expected.html?r1=169499&r2=169498&pathrev=169499
   A http://src.chromium.org/viewvc/blink/trunk/Source/web/tests/MHTMLTest.cpp?r1=169499&r2=169498&pathrev=169499
   D http://src.chromium.org/viewvc/blink/trunk/LayoutTests/mhtml/page_with_image_unmht-expected.txt?r1=169499&r2=169498&pathrev=169499
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/mhtml/simple_page_unmht-expected.html?r1=169499&r2=169498&pathrev=169499
   D http://src.chromium.org/viewvc/blink/trunk/LayoutTests/mhtml/shared_buffer_bug-expected.txt?r1=169499&r2=169498&pathrev=169499
   D http://src.chromium.org/viewvc/blink/trunk/LayoutTests/mhtml/base_url-expected.txt?r1=169499&r2=169498&pathrev=169499
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/mhtml/page_with_css_and_js_unmht-expected.html?r1=169499&r2=169498&pathrev=169499
   D http://src.chromium.org/viewvc/blink/trunk/LayoutTests/mhtml/simple_page_unmht-expected.txt?r1=169499&r2=169498&pathrev=169499
   M http://src.chromium.org/viewvc/blink/trunk/LayoutTests/mhtml/multi_frames.html_original?r1=169499&r2=169498&pathrev=169499
   M http://src.chromium.org/viewvc/blink/trunk/LayoutTests/mhtml/multi_frames_binary.mht?r1=169499&r2=169498&pathrev=169499
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/mhtml/relative_url.mht?r1=169499&r2=169498&pathrev=169499
   D http://src.chromium.org/viewvc/blink/trunk/LayoutTests/mhtml/page_with_css_and_js_unmht-expected.txt?r1=169499&r2=169498&pathrev=169499
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/mhtml/resources/frame_0.html?r1=169499&r2=169498&pathrev=169499
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/mhtml/page_with_image_ie-expected.html?r1=169499&r2=169498&pathrev=169499

Restricts MHTML loading to top frames.
Also disabling JavaScript for MHTML documents.
Because JavaScipt is now disabled, MHTML layout tests had to be changed
not to use JavaScript anymore.

BUG=330663
TEST=Run MHTML layout tests.
R=abarth@chromium.org, jschuh@chromium.org

Review URL: https://codereview.chromium.org/161383002
-----------------------------------------------------------------

### in...@chromium.org (2014-03-20)

[Empty comment from Monorail migration]

### js...@chromium.org (2014-03-20)

Thanks for taking care of this @jcivelli.

### cl...@chromium.org (2014-03-20)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### ti...@chromium.org (2014-03-25)

[Empty comment from Monorail migration]

### ti...@chromium.org (2014-03-25)

[Empty comment from Monorail migration]

### dx...@google.com (2014-03-26)

[Empty comment from Monorail migration]

### ti...@chromium.org (2014-03-28)

jcivelli@ - can you please merge this into 34?

### ti...@chromium.org (2014-03-28)

[Empty comment from Monorail migration]

### in...@chromium.org (2014-04-01)

I am getting conflicts when merging. we will let this roll into m35.

### jc...@chromium.org (2014-04-01)

Sorry, meant to perform that merge and ran into problems as well.
The original CL was really painful to land (as it has MHTML files which are CRLF that must be checked in with svn and don't work with build bots).
Letting it roll M35 will save us some headaches if acceptable.


### ti...@chromium.org (2014-05-18)

packagesu@ - What name/handle would you like to be credited as in our release notes? We'll go with "packagesu" unless you tell us otherwise.

### ti...@chromium.org (2014-05-19)

Congratulations - $1000 for this report! The release notes should go out tomorrow crediting you as "packagesu" unless you tell us otherwise. Someone from Google finance will be in touch in the next week or two regarding payment.

### pa...@gmail.com (2014-05-21)

Thanks guys) 

### cl...@chromium.org (2014-06-26)

Bulk update: removing view restriction from closed bugs.

### ti...@chromium.org (2014-07-22)

[Empty comment from Monorail migration]

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

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### ro...@gmail.com (2020-02-11)

So, do I get this "fix" right?
"I CBA to work on that, so here's patch that completely disables JS".

That's not a resolution. Framed content can be prevented from having access to parent and MHTML content can be prevented from downloading anything (and mostly likely it is prevented already). But JS in form of inline <script> tags or packed as MHTML parts MUST work inside this sandbox. Otherwise "save page as single file" is pretty much useless in most of modern web.

### is...@google.com (2020-02-11)

This issue was migrated from crbug.com/chromium/330663?no_tracker_redirect=1

[Multiple monorail components: Blink, Blink>SavePage]
[Monorail mergedwith: crbug.com/chromium/342128]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40078601)*
