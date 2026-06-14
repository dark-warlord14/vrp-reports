# Dragging a file into a web renderer exposes the file: scheme

| Field | Value |
|-------|-------|
| **Issue ID** | [40058083](https://issues.chromium.org/issues/40058083) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals |
| **Reporter** | ma...@m-austin.com |
| **Assignee** | ts...@chromium.org |
| **Created** | 2012-05-10 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**  

A html <a> tag is created using a file:/// url. The HTML5 "download" attribute allowing the attacker to set the name and force the file download. This allows the attacker to effectively copy any file the user has access to into the downloads directory and rename it. In the POC listed below the victim would then be tricked into dragging the local system file from the chrome download bar back into an HTML5 Drop zone uploading it to the server.

The current example takes advantage of issue: <http://code.google.com/p/chromium/issues/detail?id=127522>. However the is not necessary for the attack.

**VERSION**  

Chrome Version: Chrome build 14.0.835.15+  

Operating System: OSX, XP, Win7 were tested.

**REPRODUCTION CASE**  

POC with DND Local File Disclosure: <http://m-austin.com/hax/chrome/demo2.html> (unpublished at time of report)

<a href="file:///C:/boot.ini" download="test.txt">Win XP,</a>  

<a href="file:///C:/Windows/System32/drivers/etc/hosts" download="test.txt">Win 7,</a>  

<a href="file:////etc/hosts" download="test.txt">OSX</a>

## Attachments

- [drag.png](attachments/drag.png) (image/png; charset=binary, 7.0 KB)
- [demo2.html](attachments/demo2.html) (text/html; charset=us-ascii, 5.1 KB)

## Timeline

### ma...@m-austin.com (2012-05-10)

For some reason on OSX this POC also eats up a ton of CPU (115%) after it runs, and continues until the browser is closed. 

### js...@chromium.org (2012-05-10)

I can't repro this, but more specifically there's an explicit check that prevents accessing the file: and other sensitive schemes from a web scheme (such as http: or https:).

### ma...@m-austin.com (2012-05-10)

I can constantly reproduce form the URL listed: http://m-austin.com/hax/chrome/demo2.html  Running the file locally did have different behavior. 

### ma...@m-austin.com (2012-05-10)

If this issue marked as "Status: Invalid" I'll assume its safe to make public / blog?

### js...@chromium.org (2012-05-11)

Sorry, your description was a bit confusing. The initial drag from the download bar is necessary to grant the renderer access to the file: URL in the first place. Unfortunately, you didn't mention that as the critical step in your explanation, so I didn't test it. For future reference, we prefer a minimal repro that clearly demonstrates the exact behavior necessary, and notes any dependencies.

@creis, @rdsmith - I'm not sure who should look at this. We definitely should not be blessing file: URLs from the render, or maybe it's that the change event is executing in the wrong context?

### js...@chromium.org (2012-05-11)

@creis, @rdmith - Actually adding you guys in this time, with the question from the previous comment.

### ma...@m-austin.com (2012-05-11)

Sorry about that,  I think a better description in the POC file, but yes when the file is not run as a local HTML file the first file drag is required.  It appears though that once the tab opens the file, from then on that tab can open the file: urls even after a refresh. 

### ma...@m-austin.com (2012-05-11)

On a related note the file:///  scheme also "downloads" a directory listing.  The attacker could push file:////Users/ on OSX (or documents and settings on win) and an HTML version of the directory listing will download. The attacker could parse out the user names, then attack the keychain or documents folders (e-mails, logs, ...). 

### ts...@chromium.org (2012-05-11)

RenderViewHostImpl::DragTargetDragEnter() has always granted both
  ChildProcessSecurityPolicy::GrantReadFile() and
  ChildProcessSecurityPolicy::GrantRequestURL() on the dragged (downloaded) file.

ChildProcessSecurityPolicy::GrantRequestURL() then blesses the entire file:// scheme.
ChildProcessSecurityPolicy::CanRequestURL() then returns true for any file:// URL.

There are two issues here:
1. RVHI should only GrantReadFile() here.  
2. Granting access to a file URL should imply GrantReadFile to register the file; CanRequestURL should be more particular about the file:// scheme (perhaps according to the setting of "can access files from files") doing a check for CanReadFile when the scheme is file.

Unclear what breaks when these both change.  

 

### ts...@chromium.org (2012-05-11)

[Empty comment from Monorail migration]

### cr...@chromium.org (2012-05-11)

Yes, sounds like Adam would be familiar with these checks.  I agree that it sounds like we should not be blessing the entire file:// scheme after a single file drag.

### ts...@chromium.org (2012-05-11)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-05-12)

[Empty comment from Monorail migration]

### js...@chromium.org (2012-05-13)

[Empty comment from Monorail migration]

### bu...@chromium.org (2012-05-15)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=137184

------------------------------------------------------------------------
r137184 | tsepez@chromium.org | Tue May 15 11:29:00 PDT 2012

Changed paths:
 M http://src.chromium.org/viewvc/chrome/trunk/src/content/browser/renderer_host/render_view_host_impl.cc?r1=137184&r2=137183&pathrev=137184
 M http://src.chromium.org/viewvc/chrome/trunk/src/content/browser/renderer_host/render_view_host_unittest.cc?r1=137184&r2=137183&pathrev=137184

DragEnter grants both read and navigate permissions to files.

Calling ChildProcessSecurityPolicy::GrantReadFile() ought to be sufficient for the renderer to process files dragged into it. Giving the GrantRequestURL() permission is excessive.

BUG=127525
Review URL: https://chromiumcodereview.appspot.com/10397002
------------------------------------------------------------------------

### ts...@chromium.org (2012-05-15)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-05-18)

What are your thoughts on an M20 merge, Tom?

### sc...@gmail.com (2012-05-18)

[Empty comment from Monorail migration]

### ts...@chromium.org (2012-05-18)

I'd like to let it bake a bit.  May have hidden side-effects breaking someone's file uploader widget or extension somewhere.

### ma...@m-austin.com (2012-05-31)

For re-testing this bug i noticed that a recent fix prevents "data: " urls from being downloaded. (as of production version 19.0.1084.52).  The POC url listed has been updated to download a "real" file file.txt and the demo works again as expected on the current production versions of chrome. 

### ts...@chromium.org (2012-05-31)

Although "fixed", this is not yet released and will not hit until chrome 21 (possibly pushed up to chrome 20 per https://crbug.com/chromium/127525#c17).

### ma...@m-austin.com (2012-05-31)

Yes I understand. I just wanted to update because some other fix prevented the original POC from working. I wanted to note this incase there were any issues retesting.

### ts...@chromium.org (2012-05-31)

Ah, many thanks.  I tested this using file URLs, not the POC.

### ts...@chromium.org (2012-06-01)

Reverting due to http://code.google.com/p/chromium/issues/detail?id=130710

There is ambiguous behaviour as to what it means to drag a file onto the tab; either use the file for the value of a file input element, or navigate to the file.  At the time of the drag the browser doesn't distinguish between the two, which is why both permissions were granted in the RVH so that when the renderer made up its mind, either would succeed.  The downside of that simple approach is this issue.

Probably the fix needs to be in CPSP so that granting navigation to a singe file doesn't enable the entire file:// scheme.  Some special case code for file:// may be required there.



### ts...@chromium.org (2012-06-01)

[Empty comment from Monorail migration]

### bu...@chromium.org (2012-06-01)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=140074

------------------------------------------------------------------------
r140074 | tsepez@chromium.org | Fri Jun 01 12:07:46 PDT 2012

Changed paths:
 M http://src.chromium.org/viewvc/chrome/trunk/src/content/browser/renderer_host/render_view_host_impl.cc?r1=140074&r2=140073&pathrev=140074
 M http://src.chromium.org/viewvc/chrome/trunk/src/content/browser/renderer_host/render_view_host_unittest.cc?r1=140074&r2=140073&pathrev=140074

Revert 137184 - DragEnter grants both read and navigate permissions to files.

Calling ChildProcessSecurityPolicy::GrantReadFile() ought to be sufficient for the renderer to process files dragged into it. Giving the GrantRequestURL() permission is excessive.

TBR=abarth@chromium.org
BUG=127525
Review URL: https://chromiumcodereview.appspot.com/10397002

TBR=tsepez@chromium.org
Review URL: https://chromiumcodereview.appspot.com/10476003
------------------------------------------------------------------------

### ts...@chromium.org (2012-06-07)

[Empty comment from Monorail migration]

### bu...@chromium.org (2012-06-08)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=141124

------------------------------------------------------------------------
r141124 | tsepez@chromium.org | Thu Jun 07 17:10:40 PDT 2012

Changed paths:
 M http://src.chromium.org/viewvc/chrome/trunk/src/content/browser/child_process_security_policy_unittest.cc?r1=141124&r2=141123&pathrev=141124
 M http://src.chromium.org/viewvc/chrome/trunk/src/content/browser/renderer_host/render_view_host_impl.cc?r1=141124&r2=141123&pathrev=141124
 M http://src.chromium.org/viewvc/chrome/trunk/src/content/browser/child_process_security_policy_impl.cc?r1=141124&r2=141123&pathrev=141124
 M http://src.chromium.org/viewvc/chrome/trunk/src/content/renderer/render_view_impl.cc?r1=141124&r2=141123&pathrev=141124
 M http://src.chromium.org/viewvc/chrome/trunk/src/content/browser/child_process_security_policy_impl.h?r1=141124&r2=141123&pathrev=141124
 M http://src.chromium.org/viewvc/chrome/trunk/src/content/browser/renderer_host/render_view_host_unittest.cc?r1=141124&r2=141123&pathrev=141124

DragEnter grants RequestURL to entire file:// scheme.

DragEnter can't know if the end action of a dragged file will be to assign
it to the value of a file input element, or to navigate to the file itself,
so it grants the permissions required for both. The RequestURL permission,
however, currently implies access to all of file:// even though we intend to
request only one file.  This change adds a method to ChildProcessSecurityPolicy
for more granular permissions for file:// URLs which is applied to the existing
renderer.  A second change causes file:// navigations to be browser-navigations,
so that the existing renderer will fork a new "file-privileged" renderer.  The
old renderer, having permissions for this one URL, will pass the checks
required to lauch the new renderer for the URL, but will not have permission
to fork renderers for other file:// URLs.

This is a second attempt at resolving the issue, see also:
http://codereview.chromium.org/10397002/

BUG=127525

Review URL: https://chromiumcodereview.appspot.com/10517009
------------------------------------------------------------------------

### ts...@chromium.org (2012-06-08)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-07-31)

[Empty comment from Monorail migration]

### bu...@chromium.org (2012-10-13)

This issue has been closed for some time. No one will pay attention to new comments.
If you are seeing this bug or have new data, please click New Issue to start a new bug.

### js...@chromium.org (2012-12-20)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-13)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-14)

[Empty comment from Monorail migration]

### sc...@gmail.com (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-06-14)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-07-27)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-11-18)

[Empty comment from Monorail migration]

### aw...@google.com (2016-11-18)

The panel decided to award $500 for this bug. The bug itself has little security value, but the fix is a good hardening measure. Thanks!

### aw...@google.com (2016-11-18)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/127525?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40058083)*
