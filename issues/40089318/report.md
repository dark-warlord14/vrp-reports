# OOB read with Flash

| Field | Value |
|-------|-------|
| **Issue ID** | [40089318](https://issues.chromium.org/issues/40089318) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink, Internals, Internals>Plugins>Flash |
| **Reporter** | ph...@gmail.com |
| **Assignee** | js...@chromium.org |
| **Created** | 2011-03-26 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**

Flash (Actionscript) provide a ways to interact between the browser and the flash applet with the ExternalInterface class.

Test.as  

<<<<<  

private function init(e:Event = null):void {  

//Make the method callMe() available to the browser  

ExternalInterface.addCallback("callMe", this.callMe);  

}  

public function callMe(input:String):String {  

return input;  

}  

<<<<<

A problem was first observe when "" were pass to the function made public.  

It then become vulnerable when passing :  

swf.callMe("\x0000AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")  

The value receive from the method callMe now include what seems to be arbitrary memory data.

Note : I have not debug it to understand the internals. It seems to be reading the values following the string with the initial length.

SEVERITY  

High (Base on <http://www.chromium.org/developers/severity-guidelines>)

**VERSION**  

Chrome Version: 12.0.712.0 dev  

Operating System: Windows XP

**REPRODUCTION CASE**  

See flash.zip  

The poc (test.htm) call the method with various size of string.  

With minimal tests, I was able to see data from another iframe (see the amazon session being expose in the screen).

ADDITIONAL INFORMATION  

IE7+ is not affect by this problem. FF seems to have limited exposure (only few bytes can be overflow max).  

In the flash.zip the Test.as can be recompile quickly with flashdevelop(.org)

... hope I'm eligible to vulnerability reward program.

## Attachments

- [amazon_session.png](attachments/amazon_session.png) (image/png; charset=binary, 113.0 KB)
- [flash.zip](attachments/flash.zip) (application/zip; charset=binary, 9.3 KB)
- [chrome_leak_iframe.png](attachments/chrome_leak_iframe.png) (image/png; charset=binary, 78.6 KB)
- [test_windows7.png](attachments/test_windows7.png) (image/png; charset=binary, 130.8 KB)
- [iframe.png](attachments/iframe.png) (image/png; charset=binary, 57.6 KB)
- [env_path.png](attachments/env_path.png) (image/png; charset=binary, 78.1 KB)

## Timeline

### js...@chromium.org (2011-03-27)

I'm unable to repro this on Windows 7 using stable (10.0.648.204), canary (12.0.716.0), or trunk. I don't see why this would be sensitive to a Windows version, but someone should verify against a Windows XP instance as well.

### ph...@gmail.com (2011-03-27)

@jschuh .. i just test it in windows 7 and get the overflow.

Make sure you access the test page through http:// and not file:// and that the swf (which is invisible) is properly load in the page.

about:version..
Google Chrome	10.0.648.151 (Official Build 78498)
WebKit	534.16 (branches/chromium/648@80788)
V8	3.0.12.30
User Agent	Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.151 Safari/534.16
Command Line	"C:\Users\h3xstream\AppData\Local\Google\Chrome\Application\chrome.exe" --flag-switches-begin --flag-switches-end

### js...@chromium.org (2011-03-30)

I don't have a decent setup to test this while I'm out.

@cdn - Could you try and repro this as described in https://crbug.com/chromium/77493#c2? It looks like the reporter is getting an OOB read off the end of a string (medium severity) but I can't duplicate it.


### sk...@chromium.org (2011-03-30)

Works on Windows 7 x64, Google Chrome	10.0.648.204 (Official Build 79063), WebKit	534.16 (branches/chromium/648@81505), V8	3.0.12.30, Flash - Version: 10.2.154.25

### js...@chromium.org (2011-03-30)

Did you confirm that it's an OOB read? Is it happening in the Flash plugin process or the renderer, and any idea if it's in our code or Flash? (Since the reporter says it affects Firefox as well, my guess would be Flash.)

### sk...@chromium.org (2011-03-30)

I've only confirmed that the repro works in that it's showing arbitrary data at this point. I've not investigated the root cause.

### js...@chromium.org (2011-03-31)

Okay. To triage we still need someone to confirm whether this is an OOB read and if it's in our code or Flash code.

### ph...@gmail.com (2011-04-05)

small detail .. How can a vulnerability that leak resources of other domains can have medium severity?

### js...@chromium.org (2011-04-05)

The issue appears to be an out-of-bounds read, which we handle as a medium-severity issue because this type of vulnerability provides limited information, functions unreliably, and generally must be used in conjunction with another vulnerability. You can see our severity guidelines here for more information:
http://www.chromium.org/developers/severity-guidelines

### ph...@gmail.com (2011-04-05)

ok perfect. i thought same-origin policy bypass was high.

### sc...@gmail.com (2011-04-05)

A 100% reliable SOP bypass which can read full content of arbitrary cross-origin URLs would be rated High.

### js...@chromium.org (2011-04-19)

[Empty comment from Monorail migration]

### js...@chromium.org (2011-04-19)

This looks like either an OOB read or an uninitialized read. It occurs only with our custom Flash, not the normal Flash plugin.

### js...@chromium.org (2011-04-19)

Expanding the CC list. I tested on Windows, Mac, and Linux across versions ranging from stable to trunk. It repros across the board. Making the string bigger hits a crash on an invalid read: http://crash/reportdetail?reportid=8efe250e35c8e7f5


### pi...@chromium.org (2011-04-19)

Pepper is also vulnerable.

### pi...@chromium.org (2011-04-19)

Though in the case of Pepper, there is pepper-specific code that makes it vulnerable.

### bu...@chromium.org (2011-04-19)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=82172

------------------------------------------------------------------------
r82172 | piman@google.com | Tue Apr 19 14:54:26 PDT 2011

Changed paths:
 M http://src.chromium.org/viewvc/chrome/trunk/src/webkit/plugins/ppapi/npapi_glue.cc?r1=82172&r2=82171&pathrev=82172

Fix invalid read in ppapi code

BUG=77493
TEST=attached test

Review URL: http://codereview.chromium.org/6883059
------------------------------------------------------------------------

### ph...@gmail.com (2011-05-12)

quick question.. Is there any chance that I appear in the mentions when the bug get closed? (http://dev.chromium.org/Home/chromium-security/hall-of-fame) Thanks

### js...@chromium.org (2011-05-12)

Yes, you will get credited if we verify that it is a bug in Chrome (and not Flash). I expect to have a chance to look at this issue in depth over the next week or so.

### js...@chromium.org (2011-05-12)

Just to clarify, the "and not Flash" part is because i can't speak for how adobe credits research.

### in...@chromium.org (2011-05-26)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-06-09)

[Empty comment from Monorail migration]

### js...@chromium.org (2011-06-09)

Bug is around line 246 in content/plugin/npobject_util.cc:

    case NPVARIANT_PARAM_STRING:
      result->type = NPVariantType_String;
      result->value.stringValue.UTF8Characters =
          static_cast<NPUTF8 *>(base::strdup(param.string_value.c_str()));
      result->value.stringValue.UTF8Length =
          static_cast<int>(param.string_value.size());
      break;

It's an easy fix and should be a clean merge. We should be able to push it in the first m12 patch.


### sc...@gmail.com (2011-06-09)

[Empty comment from Monorail migration]

### bu...@chromium.org (2011-06-11)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=88758

------------------------------------------------------------------------
r88758 | jschuh@chromium.org | Fri Jun 10 19:54:51 PDT 2011

Changed paths:
 M http://src.chromium.org/viewvc/chrome/trunk/src/content/plugin/npobject_util.cc?r1=88758&r2=88757&pathrev=88758

Prevent OOB read from plugin calls returning strings with embedded NUL characters. Duplicates this Pepper fix: http://src.chromium.org/viewvc/chrome?view=rev&revision=82172

BUG=77493

Review URL: http://codereview.chromium.org/7099006
------------------------------------------------------------------------

### js...@chromium.org (2011-06-11)

Fixed: http://src.chromium.org/viewvc/chrome?view=rev&revision=88758

### in...@chromium.org (2011-06-11)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-06-14)

@philippe.arteau: what name would you like us to credit you with in our release notes?

### bu...@chromium.org (2011-06-14)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=88953

------------------------------------------------------------------------
r88953 | cevans@chromium.org | Mon Jun 13 19:54:45 PDT 2011

Changed paths:
 M http://src.chromium.org/viewvc/chrome/branches/742/src/content/plugin/npobject_util.cc?r1=88953&r2=88952&pathrev=88953

Merge 88758 - Prevent OOB read from plugin calls returning strings with embedded NUL characters. Duplicates this Pepper fix: http://src.chromium.org/viewvc/chrome?view=rev&revision=82172

BUG=77493

Review URL: http://codereview.chromium.org/7099006

TBR=jschuh@chromium.org
Review URL: http://codereview.chromium.org/7153001
------------------------------------------------------------------------

### bu...@chromium.org (2011-06-14)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=88951

------------------------------------------------------------------------
r88951 | cevans@chromium.org | Mon Jun 13 19:52:47 PDT 2011

Changed paths:
 M http://src.chromium.org/viewvc/chrome/branches/782/src/content/plugin/npobject_util.cc?r1=88951&r2=88950&pathrev=88951

Merge 88758 - Prevent OOB read from plugin calls returning strings with embedded NUL characters. Duplicates this Pepper fix: http://src.chromium.org/viewvc/chrome?view=rev&revision=82172

BUG=77493

Review URL: http://codereview.chromium.org/7099006

TBR=jschuh@chromium.org
Review URL: http://codereview.chromium.org/7152001
------------------------------------------------------------------------

### sc...@gmail.com (2011-06-14)

[Empty comment from Monorail migration]

### ph...@gmail.com (2011-06-14)

@scarybeasts "Philippe Arteau" is ok. Thanks!

### sc...@gmail.com (2011-06-16)

@philippe.arteau: congrats! This bug qualifies for a provisional $1000 Chromium Security Reward :D We really like fixing info leak bugs like this, so thanks for finding it!

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

### sc...@gmail.com (2011-06-29)

@philippe.arteau: thanks again, fix live!
http://googlechromereleases.blogspot.com/2011/06/stable-channel-update_28.html
E-mail cevans@chromium.org for instructions to collect payment.

### sc...@gmail.com (2011-08-04)

Payment will be wired soon. It's in the system. Sorry for the delay.

### js...@chromium.org (2011-10-05)

Batch update.

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

This issue was migrated from crbug.com/chromium/77493?no_tracker_redirect=1

[Multiple monorail components: Blink, Internals, Internals>Plugins>Flash]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40089318)*
