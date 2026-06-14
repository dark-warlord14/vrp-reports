# Potential XSS attack with [0x8E][0xE3] in EUC-JP page

| Field | Value |
|-------|-------|
| **Issue ID** | [40052600](https://issues.chromium.org/issues/40052600) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink |
| **Reporter** | ma...@gmail.com |
| **Assignee** | js...@chromium.org |
| **Created** | 2012-01-09 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**  

Google Chrome treats [0x8E][0xEC] as [0x5C] in EUC-JP page.  

This means that even though the developer takes correct XSS protection, XSS occurs.

Ex:

<http://example.com/?q=xxx%22%3C%3E> --------

<script>var x="xxx\"&lt;&gt;"</script>

---

<http://example.com/?q=%8E%EC%22;alert(1)//> --------

<script>var x="[0x8E][0xEC]\";alert(1)//"</script>

---

**VERSION**  

Chrome Version: 16.0.912.75 stable  

Operating System: Windows Vista sp2

## Attachments

- [euc_webkit_8EE3.html](attachments/euc_webkit_8EE3.html) (text/plain; charset=unknown-8bit, 63 B)

## Timeline

### ma...@gmail.com (2012-01-09)

Oops, not 8EEC but 8EE3.

### pa...@chromium.org (2012-01-09)

[Empty comment from Monorail migration]

### pa...@chromium.org (2012-01-09)

[Empty comment from Monorail migration]

### js...@chromium.org (2012-01-09)

@jshin, any idea what's going on here?

### ts...@chromium.org (2012-01-26)

The reporter is claiming that there is a transliteration going on here when the page is converted from EUC-JP by the browser hat results in a \ being introduced for byte sequences other than 0x5c.  This makes it hard for EUC-JP website owners to properly filter their untrusted user input.





### ts...@chromium.org (2012-01-26)

[Comment Deleted]

### ts...@chromium.org (2012-01-26)

[Comment Deleted]

### ts...@chromium.org (2012-01-26)

[Comment Deleted]

### ts...@chromium.org (2012-01-26)

Nevermind.  I didn;t see your attached repro.  That does repro on linux. 

### ts...@chromium.org (2012-01-26)

[Comment Deleted]

### ts...@chromium.org (2012-01-26)

This is indeed in icu as expected.  WebCore::TextCodecICU is calling into uncv_toUnicode() in ICU which returns a single \ for the two binary bytes.

### ts...@chromium.org (2012-01-27)

Grepping through ICU for unsafe encodings for "'<>\ (non-ebcdic):

third_party/icu/source/data/mappings/cns-11643-1992.ucm:<U003C> \x81\x22\x36 |0
third_party/icu/source/data/mappings/cns-11643-1992.ucm:<U003E> \x81\x22\x37 |0
third_party/icu/source/data/mappings/cns-11643-1992.ucm:<U005C> \x81\x22\x60 |0
third_party/icu/source/data/mappings/google-euc_jp_mod.ucm:<U005C> \x8E\xE3 |3
third_party/icu/source/data/mappings/ibm-1276_P100-1995.ucm:<U0027> \xA9 |0
third_party/icu/source/data/mappings/ibm-1363_P110-1997.ucm:<U005C> \x7F |2
third_party/icu/source/data/mappings/ibm-33722_P120-1999.ucm:<U005C> \x8E\xE3 |0
third_party/icu/source/data/mappings/ibm-33722_P12A_P12A-2004_U2.ucm:<U005C> \x8E\xE3 |3
third_party/icu/source/data/mappings/ibm-8482_P100-1999.ucm:<U005C> \xB2 |0
third_party/icu/source/data/mappings/ibm-942_P12A-1999.ucm:<U005C> \xFE |3
third_party/icu/source/data/mappings/ibm-943_P130-1999.ucm:<U005C> \x7F |2
third_party/icu/source/data/mappings/ibm-949_P110-1999.ucm:<U005C> \x82 |0
third_party/icu/source/data/mappings/ibm-949_P11A-1999.ucm:<U005C> \x82 |3
third_party/icu/source/data/mappings/ibm-954_P101-2007.ucm:<U005C> \x8E\xE3 |3

Need to find if any of these are used in response to any of the chrome supported charsets.


### ts...@chromium.org (2012-01-27)

None of the others appear to be in ucmlocal.mk.  Good.

### ts...@chromium.org (2012-01-27)

Just for fun, here's a script:

#!/bin/bash
# Finds unsafe transliterations in the encodings chrome usees in ICU.
UCM_SOURCE_CORE='ibm-912_P100-1995.ucm ibm-913_P100-2000.ucm ibm-914_P100-1995.ucm ibm-915_P100-1995.ucm ibm-1089_P100-1995.ucm ibm-9005_X110-2007.ucm ibm-5012_P100-1999.ucm ibm-920_P100-1995.ucm iso-8859_10-1998.ucm ibm-921_P100-1995.ucm iso-8859_14-1998.ucm ibm-923_P100-1998.ucm iso-8859_16-2001.ucm ibm-5346_P100-1998.ucm ibm-5347_P100-1998.ucm ibm-5348_P100-1997.ucm ibm-5349_P100-1998.ucm ibm-5350_P100-1998.ucm ibm-9447_P100-2002.ucm ibm-9448_X100-2005.ucm ibm-9449_P100-2002.ucm ibm-5354_P100-1998.ucm windows-936-2000.ucm gb18030.ucm windows-950-2000.ucm ibm-1375_P100-2007.ucm ibm-943_P15A-2003.ucm google-euc_jp_mod.ucm windows-949-2000.ucm windows-874-2000.ucm ibm-874_P100-1995.ucm macos-0_2-10.2.ucm macos-7_3-10.2.ucm ibm-878_P100-1996.ucm ibm-1168_P100-2002.ucm ibm-864_X110-1999.ucm noop-cns-11643.ucm noop-gb2312_gl.ucm noop-iso-ir-165.ucm'
grep -E '<U00[0-7][0-7A-F]>' $UCM_SOURCE_CORE | grep -E -v '<U00([0-7])([0-7A-F])>\s+[\]x\1\2'

which gives:

ibm-943_P15A-2003.ucm:<U001A> \x7F |0
ibm-943_P15A-2003.ucm:<U001C> \x1A |0
ibm-943_P15A-2003.ucm:<U007F> \x1C |0
google-euc_jp_mod.ucm:<U005C> \x8E\xE3 |3
google-euc_jp_mod.ucm:<U007E> \x8E\xE4 |3
ibm-874_P100-1995.ucm:<U001A> \x7F |0
ibm-874_P100-1995.ucm:<U001C> \x1A |0
ibm-874_P100-1995.ucm:<U007F> \x1C |0
ibm-864_X110-1999.ucm:<U001A> \x7F |0
ibm-864_X110-1999.ucm:<U001C> \x1A |0
ibm-864_X110-1999.ucm:<U007F> \x1C |0




### ts...@chromium.org (2012-01-27)

(Rotating DEL, ^Z, and (rarely used) FS seems fine).  So only euc_jp needs attention.

### ma...@gmail.com (2012-01-28)

Haha, as it happens, I have found this 1A/1C/7F bug, and I was just about to report this issue.
https://twitter.com/#!/kinugawamasato/status/160516005079171073

### js...@chromium.org (2012-01-31)

[Empty comment from Monorail migration]

### bu...@chromium.org (2012-01-31)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=119946

------------------------------------------------------------------------
r119946 | jshin@chromium.org | Tue Jan 31 12:32:56 PST 2012

Changed paths:
 M http://src.chromium.org/viewvc/chrome/trunk/deps/third_party/icu46/mac/icudt46l_dat.S?r1=119946&r2=119945&pathrev=119946
 M http://src.chromium.org/viewvc/chrome/trunk/deps/third_party/icu46/windows/icudt.dll?r1=119946&r2=119945&pathrev=119946
 M http://src.chromium.org/viewvc/chrome/trunk/deps/third_party/icu46/source/data/mappings/google-euc_jp_mod.ucm?r1=119946&r2=119945&pathrev=119946
 M http://src.chromium.org/viewvc/chrome/trunk/deps/third_party/icu46/patches/converters.patch?r1=119946&r2=119945&pathrev=119946
 M http://src.chromium.org/viewvc/chrome/trunk/deps/third_party/icu46/linux/icudt46l_dat.S?r1=119946&r2=119945&pathrev=119946

Revise EUC-JP mapping so that {0x8E 0xE3} and {0x8E 0xE4} are not
mapped to U+005C and U+007E. 

After this is landed, ICU has to be rolled in to get this change.

Patch originally by Tom Sepez. (see the bug). 

BUG=109574
TEST=Go to http://i18nl10n.com/chrome/euc_webkit_8EEE3.html and make sure there's no alert box popping up.
Review URL: https://chromiumcodereview.appspot.com/9233048
------------------------------------------------------------------------

### bu...@chromium.org (2012-02-01)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=120011

------------------------------------------------------------------------
r120011 | jshin@chromium.org | Tue Jan 31 18:14:07 PST 2012

Changed paths:
 M http://src.chromium.org/viewvc/chrome/trunk/src/DEPS?r1=120011&r2=120010&pathrev=120011

Roll in ICU (r=119946).

See http://codereview.chromium.org/9233048 for the actual change. 

BUG=109574
TEST=Go to http://i18nl10n.com/chrome/euc_webkit_8EE3.html and make sure there's no alert box popping up.
TBR=tsepez
Review URL: https://chromiumcodereview.appspot.com/9314007
------------------------------------------------------------------------

### js...@chromium.org (2012-02-01)

The fix is in the ToT. Requesting merge to M-17 branch. 


### js...@chromium.org (2012-02-03)

Let's try merging to M-18 first. 
I guess security team will decide whether or not to merge to M17 after that. 


### js...@chromium.org (2012-02-03)

[Empty comment from Monorail migration]

### ka...@google.com (2012-02-03)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-02-03)

milestone is for our tracking purposes.

### sc...@gmail.com (2012-02-10)

I'll try simply pulling in the latest ICU on M18. Not sure we necessarily need this for M17.

### sc...@gmail.com (2012-02-10)

Looks like M18 already has this.

### sc...@gmail.com (2012-02-11)

@masatokinugawa: thanks! And a $500 security reward for your help :)

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

### sc...@gmail.com (2012-03-25)

[Empty comment from Monorail migration]

### [Deleted User] (2012-05-15)

Marking old security bugs Fixed..

### sc...@gmail.com (2012-05-18)

Payment in system.

### bu...@chromium.org (2012-10-13)

This issue has been closed for some time. No one will pay attention to new comments.
If you are seeing this bug or have new data, please click New Issue to start a new bug.

### bu...@chromium.org (2012-11-14)

The following revision refers to this bug:
    http://goto.ext.google.com/viewvc/chrome-internal?view=rev&revision=21709

------------------------------------------------------------------------
r21709 | jungshik@google.com | 2012-02-03T02:07:50.781965Z

------------------------------------------------------------------------

### la...@google.com (2013-01-18)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-13)

[Empty comment from Monorail migration]

### sc...@gmail.com (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-06)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-06-14)

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

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/109574?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40052600)*
