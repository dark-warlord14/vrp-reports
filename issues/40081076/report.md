# ASSERTION FAILED: !value || (value->isPrimitiveValue())

| Field | Value |
|-------|-------|
| **Issue ID** | [40081076](https://issues.chromium.org/issues/40081076) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Unknown |
| **Reporter** | sa...@gmail.com |
| **Assignee** | rb...@chromium.org |
| **Created** | 2014-12-29 |
| **Bounty** | $1,500.00 |

## Description

**VULNERABILITY DETAILS**

crash when setting font-kerning style attribute in web animations to "unset" through element.animate() method

==8845==ERROR: AddressSanitizer: SEGV on unknown address 0x0000fbadbeef (pc 0x000113cad35f bp 0x7fff5523a4b0 sp 0x7fff5523a4a0 T0)

**VERSION**  

Chrome Version: 41.0.2260.0 (ASAN Developer Build)  

Operating System: Mac OSx 10.9.5

**REPRODUCTION CASE**  

open file POC2.html

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: tab  

Crash State: see ASANlog.txt

## Attachments

- [POC2.html](attachments/POC2.html) (text/html, 236 B)
- [ASANlog.txt](attachments/ASANlog.txt) (text/plain, 11.0 KB)

## Timeline

### cl...@chromium.org (2014-12-29)

ClusterFuzz is analyzing your testcase. Chromium developers can follow the progress at https://cluster-fuzz.appspot.com/testcase?key=6497589456273408

### cl...@chromium.org (2014-12-29)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-12-29)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6497589456273408

Uploader: rsesek@chromium.org
Job Type: Linux_asan_chrome_mp

Crash Type: ASSERT
Crash Address: 
Crash State:
  ASSERTION FAILED: !value || (value->isPrimitiveValue())
  blink::StyleBuilderFunctions::applyValueCSSPropertyFontKerning
  void blink::StyleResolver::applyAnimatedProperties<
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=307131:307349

Minimized Testcase (0.16 Kb):
Download: https://cluster-fuzz.appspot.com/download/AMIfv95yCf48E8dPlvovkW__jTwuHNY4Yd9U8NcroyL8iLmuQWtaI9n4exQZjxLz7tTUC3DzB3Lp3iXgW0-mOWFpSN8jT8eM0tsT1qE_ifd_AgZ1FHDMcc9a_BfKaBaontp4yu8SAY7Pb5tJGlugUst8GDHunVyQtw
</body>
<script>
HTML6=document.createElement("RUBY")
document.body.appendChild(HTML6)
HTML6.animate([{fontKerning:'unset',},{fontKerning:'unset',}],1)
</script>





### in...@chromium.org (2014-12-30)

looks like regression from

commit	dcd27fc400b90b03129e0c0014835e8f8038c8f4	
author	rob.buis@samsung.com <rob.buis@samsung.com>	Mon Dec 08 14:48:50 2014
committer	rob.buis@samsung.com <rob.buis@samsung.com>	Mon Dec 08 14:48:50 2014
Remove code in PropertyValueForSerializer

After r186604 we support a proper CSSValue for unset, so the
code to lookup whether we should serialize to initial or
inherit is not needed anymore, we just write out whatever
value the all property has.

The fast/css/all-shorthand-css-text.html now actually
passes the failing subtest, so rebaseline
all-shorthand-css-text-expected.txt.

BUG=399497

Review URL: https://codereview.chromium.org/782003002

git-svn-id: svn://svn.chromium.org/blink/trunk@186700 bbb929c8-8fbe-4397-9dbb-9b2b20218538
LayoutTests/fast/css/all-shorthand-css-text-expected.txt[diff]
LayoutTests/fast/css/all-shorthand-css-text.html[diff]
Source/core/css/StylePropertySerializer.cpp[diff]


### in...@chromium.org (2014-12-30)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-12-30)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-12-30)

This medium+ severity security issue is a regression on trunk.

Please fix this asap. If you are unable to look into this soon, please revert your change.

- Your friendly ClusterFuzz

### rw...@gmail.com (2015-01-06)

[Empty comment from Monorail migration]

### rw...@gmail.com (2015-01-07)

[Empty comment from Monorail migration]

### bu...@chromium.org (2015-01-08)

The following revision refers to this bug:
  http://src.chromium.org/viewvc/blink?view=rev&rev=188009

------------------------------------------------------------------
r188009 | rob.buis@samsung.com | 2015-01-08T00:25:08.077031Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/css/resolver/StyleBuilderCustom.cpp?r1=188009&r2=188008&pathrev=188009
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/css/resolver/StyleResolver.cpp?r1=188009&r2=188008&pathrev=188009
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/animations/interpolation/font-size-interpolation-unset-expected.txt?r1=188009&r2=188008&pathrev=188009
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/animations/interpolation/background-color-interpolation-unset.html?r1=188009&r2=188008&pathrev=188009
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/animations/interpolation/font-size-interpolation-unset.html?r1=188009&r2=188008&pathrev=188009
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/animations/interpolation/background-color-interpolation-unset-expected.txt?r1=188009&r2=188008&pathrev=188009

Fix assert when interpolating using unset

In Debug mode interpolating using unset hit an ASSERT because
StyleBuilder::applyProperty did not take it into account and assumed the
CSSValue was a primitive value if not initial or inherit. So add the code
to handle unset and determine if we should fallback to inherit or initial
for the given property.

Add a test for interpolating unset with an inherited property (font-size)
and one which falls back to initial (background-color).

BUG=445332

Review URL: https://codereview.chromium.org/840463002
-----------------------------------------------------------------

### in...@chromium.org (2015-01-08)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-01-08)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

Your fix is very close to the branch point. After the branch happens, please make sure to check if your fix is in.

- Your friendly ClusterFuzz

### cl...@chromium.org (2015-01-08)

ClusterFuzz has detected this issue as fixed in range 310445:310458.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6497589456273408

Uploader: rsesek@chromium.org
Job Type: Linux_asan_chrome_mp

Crash Type: ASSERT
Crash Address: 
Crash State:
  ASSERTION FAILED: !value || (value->isPrimitiveValue())
  blink::StyleBuilderFunctions::applyValueCSSPropertyFontKerning
  void blink::StyleResolver::applyAnimatedProperties<
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=307131:307349
Fixed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=310445:310458

Minimized Testcase (0.16 Kb):
Download: https://cluster-fuzz.appspot.com/download/AMIfv95yCf48E8dPlvovkW__jTwuHNY4Yd9U8NcroyL8iLmuQWtaI9n4exQZjxLz7tTUC3DzB3Lp3iXgW0-mOWFpSN8jT8eM0tsT1qE_ifd_AgZ1FHDMcc9a_BfKaBaontp4yu8SAY7Pb5tJGlugUst8GDHunVyQtw
</body>
<script>
HTML6=document.createElement("RUBY")
document.body.appendChild(HTML6)
HTML6.animate([{fontKerning:'unset',},{fontKerning:'unset',}],1)
</script>

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.


### in...@chromium.org (2015-01-25)

[Empty comment from Monorail migration]

### in...@chromium.org (2015-01-25)

[Empty comment from Monorail migration]

### sa...@gmail.com (2015-04-08)

Hey guys i am new to this i was just wondering about the process the bug needs to go through after the last comment and labels Merge-Triage Merge-NA. if someone can point me to the right direction it would be awesome

Thanks,

Saif

### rs...@chromium.org (2015-04-08)

Tim: This bug has had reward-topanel since January.

### ti...@google.com (2015-04-08)

Thanks Robert - there are quite a few bugs that need an update so I'll do a sweep today.

### ti...@google.com (2015-04-09)

Congratulations - $1500 for this report (and my apologies for the delay).

Someone from our finance team should be in contact within two weeks on how to collect payment. If that doesn't happen, please contact me directly.

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an established charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************



### sa...@gmail.com (2015-04-09)

Thank you guys this  was my first security bug. Appreciate your help

Saif

### cl...@chromium.org (2015-04-16)

Bulk update: removing view restriction from closed bugs.

### sa...@gmail.com (2015-04-23)

Hello Sir, you have told me that someone will contact me within two weeks and if it didnt happen i should contact you directly. i cant seem to find your direct email. so i just wanted to let you know that nobody contacted me so far

### ti...@google.com (2015-04-23)

Thanks for letting me know. I'll get in contact with you directly.

### ti...@google.com (2015-05-06)

[Empty comment from Monorail migration]

### ti...@google.com (2015-06-25)

Processing via our e-payment system can take up to two weeks, but the reward should be on its way to you. Thanks again for your help!

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### is...@google.com (2016-10-02)

This issue was migrated from crbug.com/chromium/445332?no_tracker_redirect=1

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40081076)*
