# Security: HTTPS Address Bar Spoofing Using View-source And Redirection

| Field | Value |
|-------|-------|
| **Issue ID** | [40095888](https://issues.chromium.org/issues/40095888) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals |
| **CVE IDs** | CVE-2011-3907 |
| **Reporter** | mi...@acrossecurity.com |
| **Assignee** | cr...@chromium.org |
| **Created** | 2011-10-04 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**

There is an inconsistency in the way Google Chrome renders some web page  

redirections in a way that allows an attacker to perform address bar  

spoofing, resulting in an HTTPS URL being displayed with the content  

from some other web site. Let's take, for example, a simple javascript  

redirection page located at <http://source/sample.html> that looks as  

follows:

```
<script>  
location="http://target";  
</script>  

```

When observing the above sample in execution all parts of UI behave  

consistently, meaning that as the address bar changes from URL of the  

source page to the target URL, the page content changes accordingly and  

promptly (at once). However by altering the script like this:

```
location="view-source:http://source/redir.php?url=http://target";  

```

one can see the address bar starts changing before the source page  

content gets replaced by a new canvas. So for a split second the address  

bar displays "<http://target>" while the DOM is still from  

"<http://source/sample.html>". The given example is composed of 2 tricks:

1)Apparently the view-source: prefix causes the asynchronous behavior  

between address bar and the DOM.

2)The redir.php is a HTTP 302 redirection script used to cause a  

redirect from "view-source:<http://source/redir.php>" to "<http://target>",  

thus removing the "view-source:" prefix from the URL (the goal is to  

spoof the address bar to a legitimate domain as will be shown later).

Also, after redirection, the browser no longer tries to display the  

source code but renders the HTML of "<http://target>".

All demos (available from address below) employ the above 2 tricks with  

<http://target> replaced by a Gmail login page address. However, to stop  

the redirection at the exact moment when the inconsistency between the  

address bar and the page contents is being exhibited, a further trick is  

used.

In ABS1.php, <https://proxy.google.com:80/> is used as target of the  

redir.php script to block the redirection for about 30 seconds (After  

that an error page is displayed as Chrome decides that it cannot  

establish an SSL/TLS connection with the server on port 80). At the same  

time as the redirection "view-  

source:<http://www.acrossecurity.com/redir.php?url=https://proxy.google.c>  

om:80/" is triggered, a form with a text field is displayed simulating a  

fake login page. If text is entered and the submit button is pressed the  

data gets sent to <http://www.acrossecurity.com>. Tests have shown that  

instead of <https://proxy.google.com:80> an unresponsive server script can  

be used or an invalid target URL such as view-source:<http://source>.

In ABS2.php, we avoid the suspicious :80 port by using any open redirect  

present on https://\*.google.com as the desired spoof URL. The demo is  

analogous to the previous except that an additional redirect is used  

after the <http://www.acrossecurity.com/redir.php> script and the  

<https://proxy.google.com:80> is replaced by a download-throttling page  

<http://www.acrossecurity.com/slow.php> that delays the loading for an  

arbitrary amount of time. This time the URL that the redirection gets  

stuck on is  

[https://www.google.com/url?q=http://www.acros.si/slow.php[...]](https://www.google.com/url?q=http://www.acros.si/slow.php%5B...%5D).

In ABS3.php we manage to spoof the exact URL string of the Gmail login  

page. To do that a modal dialog is used to stop the redirection instead  

of the "wrong port trick" as in <https://proxy.google.com:80> or the  

download-throttling slow.php mentioned above. A precondition however is  

that the victim has come to <http://www.acrossecurity.com> from the  

spoofed-to-be host (in our case <https://accounts.google.com>) or another  

host in its 2nd level domain (either via search results or a redirection  

script) before address bar spoofing redirection begins and a modal  

dialog can stop it (step 1). In step 2 a similar redirection is launched  

as in the previous demo, but with the following differences:

-a blocked (pinned) modal dialog is used to stop the redirection at the  

right moment. Like in the previous demo a fake login form is displayed,  

but any requests resulting from its submit button being pressed are  

queued for the life time of the modal dialog. Therefore a "self  

destruction" javascript is in place inside the modal dialog that  

triggers after the submit button has been pressed, thus releasing the  

said queue and allowing the credentials to be sent to attacker's server.

-a more convincing URL <https://accounts.google.com> is used as target of  

the redir.php script, avoiding the :80 port trick and the slow.php trick  

from previous demos.

All three demos are available here as on-the-fly links:

```
http://www.acrossecurity.com/demo/ABS_chrome_v14via_url_53d1r  

```

For further clarification of each individual demo, open their individual  

pages in Chrome and follow the on-screen step by step instructions:

Demo 1:  

<http://www.acrossecurity.com/demo/ABS_chrome_v14via_url_53d1r/ABS1.php>

Demo 2:  

<http://www.acrossecurity.com/demo/ABS_chrome_v14via_url_53d1r/ABS2.php>

Demo 3:  

<http://www.acrossecurity.com/demo/ABS_chrome_v14via_url_53d1r/ABS3.php>

Of course, in a real world attack the described demos would be presented  

to the victim as "click me" URLs enveloped as redirect URLs from  

[www.google.com](http://www.google.com) without further interaction needed.

In summary, we found ways to get Chrome to display an HTTPS URL from one  

host while displaying the content from another host. Note that the icon  

left to the URL is a grey planet as is typical for HTTP addresses - and  

not a green lock as is typical for valid HTTPS addresses. However, while  

many users may notice the "https" and consider it as a guarantee of  

trust, they are less likely to notice the \*absence\* of a lock -  

especially since the visual identification of HTTPS URLs is different in  

different web browsers. In addition, while users could notice a crossed-  

over lock icon (shown on HTTPS web sites that seem suspect), a grey  

planet icon does not indicate any danger.

**VERSION**  

Chrome Version: v14.0.835.187+stable,16.0.891.0+dev-m  

Operating System: Windows XP, Version 5.1.2600 Service Pack 3 Build 2600  

Windows 7 Professional SP1

## Timeline

### js...@chromium.org (2011-10-04)

@creis - It sounds like a redirect from view-source triggers the case of the omnibox getting updated before the load commits. Can you cover this one, or should someone else?

### cr...@chromium.org (2011-10-04)

Yes, I can take a look at this one.

### cr...@chromium.org (2011-10-07)

I've been looking at this one and I have a draft of a fix, but I'm still trying to understand all of the corner cases.

The root problem here is that NavigationController::GetVisisbleEntry is showing the pending_entry_ for certain renderer-initiated navigations.  As these spoofs demonstrate, we should not show the pending URL for renderer-initiated navigations.  In most cases, we have no pending_entry_ for renderer-initiated navigations, so this bug doesn't happen on most link clicks.

The problem only occurs when the renderer punts a navigation to the browser to force a process swap.  That happens with view-source links (as shown here), but also in transitions between extensions/apps and normal pages.  I think you could see the same results going from a non-app page to a URL of an installed hosted app.

I have a fix that checks if the pending_entry_ has a transition_type() of PageTransition::LINK, in which case we should not show it in GetVisibleEntry.

I originally thought I should make an exception for cases where the link is opened in a new tab.  In that case, there's no committed entry and it felt strange to show "about:blank" until the slow page committed.  It turns out that's unsafe-- the attacker can control the contents of the "about:blank" tab until the slow page commits (e.g., using w = window.open(); w.document.body.innerHTML += "foo").

Even though it feels counter-intuitive, I think we need to keep showing "about:blank" while the new tab is loading.

I'm continuing to investigate corner cases with interrupted navigations and omnibox prerendering to see if anything goes wrong there.  Should have a CL for review soon.

### cr...@chromium.org (2011-10-07)

CC'ing Dominic for the omnibox prerendering issue.  My fix ends up hiding the URL when that's enabled because the prerendering logic always uses LINK (rather than PageTransition::TYPED in the omnibox case).  That's now filed separately in https://crbug.com/chromium/99542.

### [Deleted User] (2011-10-10)

Omnibox prerendering issue fixed in r104756.

### cr...@chromium.org (2011-10-10)

Thanks for the quick change, Dominic!

### js...@chromium.org (2011-10-10)

Flagging for merge to 874: http://src.chromium.org/viewvc/chrome?view=rev&revision=104756

### cr...@chromium.org (2011-10-10)

Sorry, it's not fixed yet.  Dominic's CL was just something blocking the fix I'm working on.

### js...@chromium.org (2011-10-10)

Ah, sorry, jumped the gun. I should give you at least another five minutes to finish off the patch. ;)

### bu...@chromium.org (2011-10-10)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=104756

------------------------------------------------------------------------
r104756 | dominich@chromium.org | Mon Oct 10 12:16:37 PDT 2011

Changed paths:
 M http://src.chromium.org/viewvc/chrome/trunk/src/chrome/browser/prerender/prerender_contents.cc?r1=104756&r2=104755&pathrev=104756

Use TYPED PageTransition for Omnibox prerendering.


BUG=99542,99016
TEST=UnitTest: Prerender*, BrowserTest: Prerender*


Review URL: http://codereview.chromium.org/8216009
------------------------------------------------------------------------

### cr...@chromium.org (2011-10-11)

A CL to fix this is in review:
http://codereview.chromium.org/8224023/

### bu...@chromium.org (2011-10-13)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=105355

------------------------------------------------------------------------
r105355 | creis@chromium.org | Thu Oct 13 12:48:34 PDT 2011

Changed paths:
 M http://src.chromium.org/viewvc/chrome/trunk/src/chrome/browser/ui/blocked_content/blocked_content_container.cc?r1=105355&r2=105354&pathrev=105355
 M http://src.chromium.org/viewvc/chrome/trunk/src/chrome/browser/external_tab_container_win.cc?r1=105355&r2=105354&pathrev=105355
 M http://src.chromium.org/viewvc/chrome/trunk/src/content/browser/tab_contents/tab_contents_delegate.cc?r1=105355&r2=105354&pathrev=105355
 M http://src.chromium.org/viewvc/chrome/trunk/src/chrome/browser/ui/webui/active_downloads_ui.cc?r1=105355&r2=105354&pathrev=105355
 M http://src.chromium.org/viewvc/chrome/trunk/src/chrome/browser/ui/gtk/sad_tab_gtk.cc?r1=105355&r2=105354&pathrev=105355
 M http://src.chromium.org/viewvc/chrome/trunk/src/chrome/browser/chromeos/login/registration_screen.cc?r1=105355&r2=105354&pathrev=105355
 M http://src.chromium.org/viewvc/chrome/trunk/src/chrome/browser/ui/webui/html_dialog_tab_contents_delegate.cc?r1=105355&r2=105354&pathrev=105355
 M http://src.chromium.org/viewvc/chrome/trunk/src/chrome/browser/ui/gtk/extensions/extension_install_dialog_gtk.cc?r1=105355&r2=105354&pathrev=105355
 M http://src.chromium.org/viewvc/chrome/trunk/src/chrome/browser/bookmarks/bookmark_utils.cc?r1=105355&r2=105354&pathrev=105355
 M http://src.chromium.org/viewvc/chrome/trunk/src/chrome/browser/ui/views/bookmarks/bookmark_context_menu_test.cc?r1=105355&r2=105354&pathrev=105355
 M http://src.chromium.org/viewvc/chrome/trunk/src/chrome/browser/extensions/webstore_inline_installer.cc?r1=105355&r2=105354&pathrev=105355
 M http://src.chromium.org/viewvc/chrome/trunk/src/content/browser/tab_contents/page_navigator.cc?r1=105355&r2=105354&pathrev=105355
 M http://src.chromium.org/viewvc/chrome/trunk/src/content/browser/tab_contents/tab_contents.cc?r1=105355&r2=105354&pathrev=105355
 M http://src.chromium.org/viewvc/chrome/trunk/src/chrome/browser/sync/test/integration/performance/sessions_sync_perf_test.cc?r1=105355&r2=105354&pathrev=105355
 M http://src.chromium.org/viewvc/chrome/trunk/src/chrome/browser/bookmarks/bookmark_context_menu_controller_unittest.cc?r1=105355&r2=105354&pathrev=105355
 M http://src.chromium.org/viewvc/chrome/trunk/src/chrome/browser/ui/gtk/about_chrome_dialog.cc?r1=105355&r2=105354&pathrev=105355
 M http://src.chromium.org/viewvc/chrome/trunk/src/content/browser/tab_contents/render_view_host_manager_unittest.cc?r1=105355&r2=105354&pathrev=105355
 M http://src.chromium.org/viewvc/chrome/trunk/src/content/browser/tab_contents/navigation_entry_unittest.cc?r1=105355&r2=105354&pathrev=105355
 M http://src.chromium.org/viewvc/chrome/trunk/src/content/browser/tab_contents/navigation_entry.h?r1=105355&r2=105354&pathrev=105355
 M http://src.chromium.org/viewvc/chrome/trunk/src/chrome/browser/ui/gtk/page_info_bubble_gtk.cc?r1=105355&r2=105354&pathrev=105355
 M http://src.chromium.org/viewvc/chrome/trunk/src/chrome/browser/ui/gtk/global_bookmark_menu.cc?r1=105355&r2=105354&pathrev=105355
 M http://src.chromium.org/viewvc/chrome/trunk/src/chrome/browser/ui/views/tabs/dragged_tab_controller.cc?r1=105355&r2=105354&pathrev=105355
 M http://src.chromium.org/viewvc/chrome/trunk/src/content/browser/tab_contents/navigation_controller.cc?r1=105355&r2=105354&pathrev=105355
 M http://src.chromium.org/viewvc/chrome/trunk/src/chrome/browser/ui/gtk/view_id_util_browsertest.cc?r1=105355&r2=105354&pathrev=105355
 M http://src.chromium.org/viewvc/chrome/trunk/src/chrome/browser/ui/browser_navigator.cc?r1=105355&r2=105354&pathrev=105355
 M http://src.chromium.org/viewvc/chrome/trunk/src/chrome/browser/rlz/rlz_unittest.cc?r1=105355&r2=105354&pathrev=105355
 M http://src.chromium.org/viewvc/chrome/trunk/src/chrome/browser/ui/gtk/bookmarks/bookmark_menu_controller_gtk.cc?r1=105355&r2=105354&pathrev=105355
 M http://src.chromium.org/viewvc/chrome/trunk/src/chrome/browser/ui/browser_navigator.h?r1=105355&r2=105354&pathrev=105355
 M http://src.chromium.org/viewvc/chrome/trunk/src/content/browser/tab_contents/navigation_controller_unittest.cc?r1=105355&r2=105354&pathrev=105355
 M http://src.chromium.org/viewvc/chrome/trunk/src/chrome/browser/oom_priority_manager_browsertest.cc?r1=105355&r2=105354&pathrev=105355
 M http://src.chromium.org/viewvc/chrome/trunk/src/content/browser/tab_contents/navigation_controller.h?r1=105355&r2=105354&pathrev=105355
 M http://src.chromium.org/viewvc/chrome/trunk/src/chrome/browser/sessions/session_types.cc?r1=105355&r2=105354&pathrev=105355
 M http://src.chromium.org/viewvc/chrome/trunk/src/chrome/browser/debugger/devtools_window.cc?r1=105355&r2=105354&pathrev=105355
 M http://src.chromium.org/viewvc/chrome/trunk/src/chrome/browser/ui/gtk/global_history_menu.cc?r1=105355&r2=105354&pathrev=105355
 M http://src.chromium.org/viewvc/chrome/trunk/src/content/browser/tab_contents/navigation_entry.cc?r1=105355&r2=105354&pathrev=105355
 M http://src.chromium.org/viewvc/chrome/trunk/src/chrome/browser/ui/views/bookmarks/bookmark_bar_view_test.cc?r1=105355&r2=105354&pathrev=105355
 M http://src.chromium.org/viewvc/chrome/trunk/src/chrome/browser/ui/gtk/tabs/dragged_tab_controller_gtk.cc?r1=105355&r2=105354&pathrev=105355
 M http://src.chromium.org/viewvc/chrome/trunk/src/content/browser/site_instance_unittest.cc?r1=105355&r2=105354&pathrev=105355
 M http://src.chromium.org/viewvc/chrome/trunk/src/chrome/browser/ui/gtk/location_bar_view_gtk.cc?r1=105355&r2=105354&pathrev=105355
 M http://src.chromium.org/viewvc/chrome/trunk/src/chrome/browser/ui/browser.cc?r1=105355&r2=105354&pathrev=105355
 M http://src.chromium.org/viewvc/chrome/trunk/src/content/browser/tab_contents/page_navigator.h?r1=105355&r2=105354&pathrev=105355

Don't show URL for pending new navigations initiated by the renderer.

BUG=99016
TEST=Click a link to a slow view-source: URL.

Review URL: http://codereview.chromium.org/8224023
------------------------------------------------------------------------

### in...@chromium.org (2011-10-13)

This one, we might want to let it roll in m16.

### cr...@chromium.org (2011-10-13)

Yeah, I was going to mention something about that.  With the number of files it touches (even though most are just adding an extra parameter), it wouldn't be easy to merge to M15.  We just didn't have enough info to fix the bug without the new parameter.

### bu...@chromium.org (2011-10-14)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=105577

------------------------------------------------------------------------
r105577 | creis@chromium.org | Fri Oct 14 14:11:02 PDT 2011

Changed paths:
 M http://src.chromium.org/viewvc/chrome/trunk/src/chrome/browser/ui/browser_navigator.cc?r1=105577&r2=105576&pathrev=105577
 M http://src.chromium.org/viewvc/chrome/trunk/src/tools/valgrind/memcheck/suppressions.txt?r1=105577&r2=105576&pathrev=105577

Fix memory error in previous CL.

BUG=100315
BUG=99016
TEST=Memory bots go green

Review URL: http://codereview.chromium.org/8302001
------------------------------------------------------------------------

### [Deleted User] (2011-10-17)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-12-10)

@mitja.kolsek: thanks for this report. It does look like a valid URL spoofing bug, and the report quality was high. For this combination, we offer a $1000 Chromium Security Reward. Thanks again!

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

### mi...@acrossecurity.com (2011-12-12)

@scarybeasts: Thanks. When do you expect this issue to be fixed? 

### mi...@acrossecurity.com (2011-12-13)

Hey guys, could you please correct the acknowledgments for this issue (CVE-2011-3907) at http://googlechromereleases.blogspot.com/2011/12/stable-channel-update.html so that instead of my name, it would state "Luka Treiber of ACROS Security"?

I only reported this to you, Luka did the heavy lifting.

Thanks a lot!

### js...@chromium.org (2011-12-14)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-02-15)

Payment is in e-system. Give it a week or two for the wire to execute.

### cr...@chromium.org (2012-02-22)

[Empty comment from Monorail migration]

### [Deleted User] (2012-05-15)

Marking old security bugs Fixed..

### bu...@chromium.org (2012-10-13)

This issue has been closed for some time. No one will pay attention to new comments.
If you are seeing this bug or have new data, please click New Issue to start a new bug.

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-13)

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

### is...@google.com (2016-10-02)

This issue was migrated from crbug.com/chromium/99016?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/75559]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40095888)*
