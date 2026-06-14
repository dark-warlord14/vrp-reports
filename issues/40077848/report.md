# Security: URL spoof with http status 204

| Field | Value |
|-------|-------|
| **Issue ID** | [40077848](https://issues.chromium.org/issues/40077848) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Unknown |
| **Reporter** | ch...@gmail.com |
| **Assignee** | cr...@chromium.org |
| **Created** | 2013-07-28 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**  

It is possible to display url of a page which returns http status 204 on address bar, while displaying contents of another origin.

\* But it is not possible to spoof https indicators.

**VERSION**  

Chrome Version: [29.0.1547.32] + [beta]  

[30.0.1580.0 (214109)] + [trunk]  

Operating System: [Ubuntu 12.04]

**REPRODUCTION CASE**

Prerequisite  

Need a web server which supports php like apache. Otherwise it is necessary to change 204.php.

1. Download and copy repro1.html and 204.php to the root folder of local web server.
2. Open chrome with this --host-resolver-rules flag.  
   
   chrome --host-resolver-rules="MAP chamalabc.com 127.0.0.1
3. Open repro1.html with this url <http://127.0.0.1/repro1.html>.
4. Click "visit chamalabc.com" link.
5. Chrome will open a new tab.  
   
   URL of new tab is <http://chamalabc.com/204.php>.  
   
   But content from 127.0.0.1 is displayed.

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: Not a crash

## Attachments

- [repro1.html](attachments/repro1.html) (text/html; charset=us-ascii, 323 B)
- [204.php](attachments/204.php) (text/x-php; charset=us-ascii, 44 B)
- [repro2.html](attachments/repro2.html) (text/html; charset=us-ascii, 353 B)

## Timeline

### ae...@chromium.org (2013-07-29)

Reproduces on 30.0.1575.0 linux.

I tested, that it works across two different hosts.

So an evil page can display the URL of any victim page that responds 204. That's useful for phishing I guess. Not sure how common it is for GET requests to respond 204 though, isn't it normally used with POST requests? I think this is a low severity security issue, but I'd like to get a second opinion.

tsepez, maybe you could also take a look?


### ts...@chromium.org (2013-07-29)

I'm not sure I understand the comment about "It is not possible to spoof https indicators." If a site happened to return a 204 over HTTPS, what happens?

### ts...@chromium.org (2013-07-29)

Anyways, I'd call this medium and bounce it over to creis for additional comments.

### ch...@gmail.com (2013-07-30)

[Comment Deleted]

### ch...@gmail.com (2013-07-30)

aedla, I actually found this issue, because of a url in google translate which returns http status 204. I updated and attached a test case with that url.

tsepez, If a site returns a 204 request over https, chrome will display that https url on address bar. But chrome will not make https section of url green. Chrome will also not display padlock icon. Clicking on paper icon on address bar will show "Identitiy not verified". 
So this bug cannot be used to spoof https addresses.See the attached test case with https url which belongs to google translate.


* Executing this test case will "Turn off instant translation" of google translate.
  So run this test case on a Test computer.

Steps
-----
1. Download and copy repro2.html to local web server.
2. Open chrome and open repro2.html.
3. Click on link "Visit google translate"
4. Chrome will open a new tab.
   URL is set to google translate url which "Turns off instant translation".
   Content is from 127.0.0.1.

### cr...@chromium.org (2013-07-30)

Yep, there's a real bug here.  Given that it has to do with the visible URL and repros in M29/M30 but not M28, my money is that it's fallout from the fix for https://crbug.com/chromium/9682.  I'll investigate tomorrow.

### ae...@chromium.org (2013-07-30)

Indeed, repro2 reproduces with google translate. Thanks for the additional information.

### cr...@chromium.org (2013-07-31)

I've tracked this down, and I may need Adam's help to come up with a fix.  At a high level, the spoof is working because we're not detecting it with didAccessInitialDocument (which was the defense we put in place in https://crbug.com/chromium/9682).  The 204 response is only important because it leaves the pending entry around.  It would work just as well with a slow URL that doesn't commit.

We would normally detect an attack like the following:
  var w = window.open('https://translate.google.com/translate/uc?ua=eotf&uav=0');
  w.document.body.innerHTML='Attacker controlled';

That's because V8's MayAccessPrecheck returns UNKNOWN in Isolate::MayNamedAccess, which causes V8Window::namedSecurityCheckCustom to call target->loader()->didAccessInitialDocument().

This attack is slightly different in that it puts a javascript URL into the window.open call.  Here's a simplified repro case:
window.open("javascript:document.body.innerHTML += 'Attacker controlled';document.location='https://translate.google.com/translate/uc?ua=eotf&uav=0';");

In this case, V8's MayAccessPrecheck is returning YES instead of UNKNOWN, so we never get to namedSecurityCheckCustom or didAccessInitialDocument.  Perhaps this is because it's a javascript: URL?

Adam, do you know of a way we could detect this case?

### cr...@chromium.org (2013-08-02)

I've confirmed that we still call context->UseDefaultSecurityToken() in the javascript: URL case, but MayAccessPrecheck is never returning UNKNOWN, so we never get to didAccessInitialDocument.

Not 100% sure, but it might be due to the receiver_context == native_context check.  I'm a bit over my head in that code, though.

### ab...@chromium.org (2013-08-07)

Yes, the access check is skipped because the script is executing in the same context.  It's always the case that a context can access itself.

We should call didAccessInitialDocument when we evaluate script in the document.  The call should probably go in ScriptController::executeScriptInMainWorld.

### wf...@chromium.org (2013-08-08)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-08-08)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/blink?view=rev&rev=155790

------------------------------------------------------------------------
r155790 | creis@chromium.org | 2013-08-08T21:28:26.061033Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/trunk/Source/bindings/v8/ScriptController.cpp?r1=155790&r2=155789&pathrev=155790
   M http://src.chromium.org/viewvc/blink/trunk/Source/web/tests/WebFrameTest.cpp?r1=155790&r2=155789&pathrev=155790

Call didAccessInitialDocument when javascript: URLs are used.

BUG=265221
TEST=See bug for repro.

Review URL: https://chromiumcodereview.appspot.com/22572004
------------------------------------------------------------------------

### cr...@chromium.org (2013-08-09)

Thanks Adam.  This should be fixed in https://src.chromium.org/viewvc/blink?view=rev&revision=155790.  Blink is still at 155780 in today's canary, so hopefully it will be in the next canary.

### sc...@gmail.com (2013-08-09)

[Empty comment from Monorail migration]

### cr...@chromium.org (2013-08-09)

scarybeasts: Note that this bug does affect M29.  Should it be labeled that way, or did you pick M30 intentionally?

### ch...@gmail.com (2013-08-12)

creis, there is one more small issue.
After the fix address bar shows the url as about:blank which is correct.
But when I click on the paper icon on address bar it says "translate.google.com".
But content displayed on page is still from 127.0.0.1.

### cr...@chromium.org (2013-08-12)

Thanks, that's a good catch.  I'll put together a patch for the website settings dialog, which appears to be using GetActiveURL instead of GetVisibleURL.  (CC'ing Nasko, since he's been looking into cases like that.)

### bu...@chromium.org (2013-08-14)

------------------------------------------------------------------------
r217485 | creis@chromium.org | 2013-08-14T05:12:31.164532Z

Changed paths:
   M http://src.chromium.org/viewvc/chrome/trunk/src/chrome/browser/ui/views/location_bar/page_info_helper.cc?r1=217485&r2=217484&pathrev=217485
   M http://src.chromium.org/viewvc/chrome/trunk/src/chrome/browser/ui/gtk/location_bar_view_gtk.cc?r1=217485&r2=217484&pathrev=217485
   M http://src.chromium.org/viewvc/chrome/trunk/src/chrome/browser/content_settings/tab_specific_content_settings.cc?r1=217485&r2=217484&pathrev=217485
   M http://src.chromium.org/viewvc/chrome/trunk/src/chrome/browser/ui/android/website_settings_popup_android.cc?r1=217485&r2=217484&pathrev=217485
   M http://src.chromium.org/viewvc/chrome/trunk/src/chrome/browser/tab_contents/render_view_context_menu.cc?r1=217485&r2=217484&pathrev=217485
   M http://src.chromium.org/viewvc/chrome/trunk/src/chrome/browser/ui/cocoa/location_bar/location_icon_decoration.mm?r1=217485&r2=217484&pathrev=217485

Use visible entry for website settings dialog.

BUG=265221
TEST=Click page icon after clicking a link to a page with a 204 response.

Review URL: https://chromiumcodereview.appspot.com/22831005
------------------------------------------------------------------------

### cr...@chromium.org (2013-08-14)

The website settings dialog issue is fixed as well in r217845, which should be in tomorrow's canary.  We can revisit whether these need to be merged after we verify it in the canary.

### cr...@chromium.org (2013-08-22)

This has been baking on canary for a little while and looks like it works.  

(I found that there are some cases where the page icon dialog does not display (https://crbug.com/chromium/277845), but that's a separate issue dating back to 2009, independent of these CLs.)

Both the Blink change and Chrome change affect M29 and M30.  The Blink change made it into M30, but the Chrome change landed just after the M30 branch.  Karen, is it ok to merge r217485 to M30?

### ka...@google.com (2013-08-23)

so i see pri3 but also medium impact. i assume we wanna ignore the p3?

### cr...@chromium.org (2013-08-26)

Yeah, that label should have been updated after https://crbug.com/chromium/265221#c5.  There was a real exploitable bug here.

### ka...@google.com (2013-08-26)

okie

### bu...@chromium.org (2013-08-26)

------------------------------------------------------------------------
r219604 | creis@chromium.org | 2013-08-26T20:48:42.649276Z

Changed paths:
   M http://src.chromium.org/viewvc/chrome/branches/1599/src/chrome/browser/content_settings/tab_specific_content_settings.cc?r1=219604&r2=219603&pathrev=219604
   M http://src.chromium.org/viewvc/chrome/branches/1599/src/chrome/browser/ui/android/website_settings_popup_android.cc?r1=219604&r2=219603&pathrev=219604
   M http://src.chromium.org/viewvc/chrome/branches/1599/src/chrome/browser/tab_contents/render_view_context_menu.cc?r1=219604&r2=219603&pathrev=219604
   M http://src.chromium.org/viewvc/chrome/branches/1599/src/chrome/browser/ui/cocoa/location_bar/location_icon_decoration.mm?r1=219604&r2=219603&pathrev=219604
   M http://src.chromium.org/viewvc/chrome/branches/1599/src/chrome/browser/ui/views/location_bar/page_info_helper.cc?r1=219604&r2=219603&pathrev=219604
   M http://src.chromium.org/viewvc/chrome/branches/1599/src/chrome/browser/ui/gtk/location_bar_view_gtk.cc?r1=219604&r2=219603&pathrev=219604

Merge 217485 "Use visible entry for website settings dialog."

> Use visible entry for website settings dialog.
> 
> BUG=265221
> TEST=Click page icon after clicking a link to a page with a 204 response.
> 
> Review URL: https://chromiumcodereview.appspot.com/22831005

TBR=creis@chromium.org

Review URL: https://codereview.chromium.org/23463002
------------------------------------------------------------------------

### ch...@gmail.com (2013-08-30)

creis, scarybeasts, 
I did not report about the google translate url (which turns off instant translation) to security@google, because I think they are not checking for csrf intentionaly.
Anyway can you please check with security@google about that url, before making this issue public?

### ka...@google.com (2013-09-03)

this looks merged. can i change to merge-merged?

### cr...@chromium.org (2013-09-03)

Yes, sorry about that.

### in...@chromium.org (2013-09-25)

Did you saw our new criteria for possibly issuing higher rewards? See http://www.chromium.org/Home/chromium-security/vulnerability-rewards-program/reward-nomination-process
E.g. If you are able to provide a repro that faulted at an address of 0x41414141, it will qualify for the new higher rewards. Or, if you can show that you have control between free and crash points, etc.

### sc...@gmail.com (2013-09-26)

Heh. https://www.google.com/gen_204

### mb...@chromium.org (2013-09-26)

[Empty comment from Monorail migration]

### sc...@gmail.com (2013-09-28)

$500 reward!

### ch...@gmail.com (2013-09-28)

Thank you very much for the reward!

### pa...@chromium.org (2013-10-18)

[Empty comment from Monorail migration]

### js...@chromium.org (2013-11-18)

Bulk release of old security bug reports.


### js...@chromium.org (2013-11-18)

Bulk release of old security bug reports.


### ti...@chromium.org (2014-02-28)

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

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/265221?no_tracker_redirect=1

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40077848)*
