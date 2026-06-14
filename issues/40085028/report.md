# Security: possible memory corruption (double-free) in XPath processing code

| Field | Value |
|-------|-------|
| **Issue ID** | [40085028](https://issues.chromium.org/issues/40085028) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Unknown |
| **Reporter** | ya...@gmail.com |
| **Assignee** | [Deleted User] |
| **Created** | 2010-11-17 |
| **Bounty** | $1,000.00 |

## Description

STEPS TO REPRODUCE:

1. Put the attached files (demo.xml and demo.xsl) in the same directory of the web server.
2. Load demo.xml in the browser via an URL like <http://localhost/evil/demo.xml>.
3. If the renderer doesn't crash immediately, reload the page a few times.

This will result in a sad tab. The crash has been reproduced with the following combinations:

Chrome 7.0.517.44 / Windows XP SP3  

Chromium 9.0.584.0 (66236) / Windows XP SP3  

Chromium 9.0.584.0 (66239) / Ubuntu 10.04 LTS

**VULNERABILITY DETAILS**

(Note:  

Due to network traffic limitations imposed by my university, it's impractical for me to check out the entire Chromium source tree and debug with it. All of my debugging has been done with libxml2 (2.7.8), so the following analysis should only be regarded as a guidance for locating the actual bug in the version of libxml2 as used by Chrome. However, it's quite possible that the description applies to both versions without much difference.)

It seems the issue exists in function xmlXPathCompOpEvalPositionalPredicate() of xpath.c. Upon encountering input expression '//book[evil()][0]', this function is called to evaluate predicate expression 'evil()'. Since evil() is an illegal XPath function, a further call to xmlXPathCompOpEvalToBoolean() would return with an error, and the engine moves into error handling code. Then comes the interesting part:

(Starting from line 11764 of xpath.c)  

if ((ctxt->error != XPATH\_EXPRESSION\_OK) || (res == -1)) {  

xmlXPathObjectPtr tmp;  

/\* pop the result \*/  

tmp = valuePop(ctxt);  

xmlXPathReleaseObject(xpctxt, tmp);  

/\* then pop off contextObj, which will be freed later \*/  

valuePop(ctxt);  

goto evaluation\_error;  

}

Here an XPath object is popped from the value stack and released by xmlXPathReleaseObject(). Then the control moves to evaluation\_error:

(Starting from line 11835 of xpath.c)  

evaluation\_error:  

xmlXPathNodeSetClear(set, hasNsNodes);  

newContextSize = 0;

evaluation\_exit:  

if (contextObj != NULL) {  

if (ctxt->value == contextObj)  

valuePop(ctxt);  

xmlXPathReleaseObject(xpctxt, contextObj);  

}

Here contextObj is not NULL, so xmlXPathReleaseObject() is called again on contextObj, which refers to the same object as the aforementioned block variable tmp in this particular scenario. This will cause the call to xmlFree() by xmlXPathReleaseObject() to operate on an area of already freed memory, leading to memory corruption.

**VERSION**

Chrome 7.0.517.44 / Windows XP SP3  

Chromium 9.0.584.0 (66236) / Windows XP SP3  

Chromium 9.0.584.0 (66239) / Ubuntu 10.04 LTS

**REPRODUCTION CASE**

Please see the attached files (demo.xml and demo.xsl).

## Attachments

- [demo.xml](attachments/demo.xml) (application/xml; charset=us-ascii, 86 B)
- [demo.xsl](attachments/demo.xsl) (application/xml; charset=us-ascii, 314 B)
- [repro.html](attachments/repro.html) (text/plain; charset=us-ascii, 77 B)

## Timeline

### sk...@chromium.org (2010-11-17)

This can be easily automated using a wrapper html that loads the xml and reloads the page (attached). It does indeed cause memory corruption and affects all versions from table to latest dev.

### sc...@gmail.com (2010-11-17)

I've got this.

### ke...@google.com (2010-11-17)

Build kicks off at 7pm, for stable, FYI.

### sc...@gmail.com (2010-11-17)

Reproduces easily for me. Pulling in fix at http://git.gnome.org/browse/libxml2/commit/?id=df83c17e5a2646bd923f75e5e507bc80d73c9722

### bu...@gmail.com (2010-11-18)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=66567

------------------------------------------------------------------------
r66567 | cevans@chromium.org | Wed Nov 17 17:24:47 PST 2010

Changed paths:
 M http://src.chromium.org/viewvc/chrome/trunk/src/third_party/libxml/src/xpath.c?r1=66567&r2=66566&pathrev=66567
 M http://src.chromium.org/viewvc/chrome/trunk/src/third_party/libxml/README.chromium?r1=66567&r2=66566&pathrev=66567

Fix XPath bug from upstream.

BUG=63444
TEST=See bug

Review URL: http://codereview.chromium.org/5196003
------------------------------------------------------------------------

### sc...@gmail.com (2010-11-18)

Merged to M8.

### sc...@gmail.com (2010-11-18)

@yangdingning: thanks for letting us know about this libxml bug!

Q1) With what name, if any, would like us to credit you?

Q2) 

### sc...@gmail.com (2010-11-18)

Oops! Chopped off the second question:

Q2) This bug report may qualify under the Chromium Security Reward program. Can you confirm who else you shared the details of the bug with?

### bu...@gmail.com (2010-11-18)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=66581

------------------------------------------------------------------------
r66581 | cevans@chromium.org | Wed Nov 17 18:23:22 PST 2010

Changed paths:
 M http://src.chromium.org/viewvc/chrome/branches/552/src/third_party/libxml/src/xpath.c?r1=66581&r2=66580&pathrev=66581
 M http://src.chromium.org/viewvc/chrome/branches/552/src/third_party/libxml/README.chromium?r1=66581&r2=66580&pathrev=66581

Merge 66567 - Fix XPath bug from upstream.

BUG=63444
TEST=See bug

Review URL: http://codereview.chromium.org/5196003

TBR=cdn@chromium.org
Review URL: http://codereview.chromium.org/5216001
------------------------------------------------------------------------

### ya...@gmail.com (2010-11-18)

Quick reaction, really!

> Q1) With what name, if any, would like us to credit you?
Please credit Yang Dingning from NCNIPC, Graduate University of Chinese Academy of Sciences. Thanks!

> Q2) This bug report may qualify under the Chromium Security Reward program. Can you confirm who else you shared the details of the bug with?

This bug is also reported to Gnome's bug tracking database for module libxml2, and Apple via their Apple Bug Reporter, since Safari also has dependency on libxml2. No other party has been contacted.

### ya...@gmail.com (2010-11-18)

Just a reminder, Daniel has made a second patch for this issue correcting a tiny problem in the first one. The patch can be found at
http://git.gnome.org/browse/libxml2/commit/?id=fec31bcd452e77c10579467ca87a785b41115de6

### sc...@gmail.com (2010-11-18)

Thank you for your kind words and the follow-up comment. I'll pull in the follow-up fix shortly, although the worst that might happen here seems to be a leak in an error path, so it's not urgent :)

### sc...@gmail.com (2010-11-18)

Congratulations! This bug report qualifies for a $1000 Chromium Security Reward
We are rewarding at the higher $1000 level due to various factors:
- The helpfulness of testing on multiple operating systems and versions.
- Nice simple reduced test case.
- Excellent explanation of the bug at a code level.

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

### bu...@gmail.com (2010-11-20)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=66868

------------------------------------------------------------------------
r66868 | mal@chromium.org | Fri Nov 19 19:11:40 PST 2010

Changed paths:
 M http://src.chromium.org/viewvc/chrome/branches/552d/src/chrome/browser/cocoa/content_settings_dialog_controller_unittest.mm?r1=66868&r2=66867&pathrev=66868
 M http://src.chromium.org/viewvc/chrome/branches/552d/src/chrome/browser/host_content_settings_map_unittest.cc?r1=66868&r2=66867&pathrev=66868
 M http://src.chromium.org/viewvc/chrome/branches/552d/src/chrome/browser/host_content_settings_map.cc?r1=66868&r2=66867&pathrev=66868
 M http://src.chromium.org/viewvc/chrome/branches/552d/src/chrome/browser/cocoa/content_settings_dialog_controller.mm?r1=66868&r2=66867&pathrev=66868
 M http://src.chromium.org/viewvc/chrome/branches/552d/src/chrome/browser/about_flags.cc?r1=66868&r2=66867&pathrev=66868
 M http://src.chromium.org/viewvc/chrome/branches/552d/src/third_party/libxml/src/xpath.c?r1=66868&r2=66867&pathrev=66868
 M http://src.chromium.org/viewvc/chrome/branches/552d/src/chrome/browser/cocoa/content_exceptions_window_controller.h?r1=66868&r2=66867&pathrev=66868
 M http://src.chromium.org/viewvc/chrome/branches/552d/src/chrome/common/chrome_switches.cc?r1=66868&r2=66867&pathrev=66868
 M http://src.chromium.org/viewvc/chrome/branches/552d/src/chrome/renderer/render_view.cc?r1=66868&r2=66867&pathrev=66868
 M http://src.chromium.org/viewvc/chrome/branches/552d/src/chrome/browser/browser_navigator.cc?r1=66868&r2=66867&pathrev=66868
 M http://src.chromium.org/viewvc/chrome/branches/552d/src/chrome/browser/views/options/content_filter_page_view.cc?r1=66868&r2=66867&pathrev=66868
 M http://src.chromium.org/viewvc/chrome/branches/552d/src/chrome/common/chrome_switches.h?r1=66868&r2=66867&pathrev=66868
 M http://src.chromium.org/viewvc/chrome/branches/552d/src/chrome/browser/cocoa/content_setting_bubble_cocoa.mm?r1=66868&r2=66867&pathrev=66868
 M http://src.chromium.org/viewvc/chrome/branches/552d/src/chrome/browser/browser_navigator.h?r1=66868&r2=66867&pathrev=66868
 M http://src.chromium.org/viewvc/chrome/branches/552d/src/chrome/browser/gtk/options/content_filter_page_gtk.cc?r1=66868&r2=66867&pathrev=66868
 M http://src.chromium.org/viewvc/chrome/branches/552d/src/chrome/browser/content_setting_bubble_model_unittest.cc?r1=66868&r2=66867&pathrev=66868
 M http://src.chromium.org/viewvc/chrome/branches/552d/src/chrome/browser/content_setting_bubble_model.cc?r1=66868&r2=66867&pathrev=66868
 M http://src.chromium.org/viewvc/chrome/branches/552d/src/chrome/browser/cocoa/content_settings_dialog_controller.h?r1=66868&r2=66867&pathrev=66868
 M http://src.chromium.org/viewvc/chrome/branches/552d/src/chrome/browser/content_setting_combo_model.cc?r1=66868&r2=66867&pathrev=66868
 M http://src.chromium.org/viewvc/chrome/branches/552d/src/third_party/libxml/README.chromium?r1=66868&r2=66867&pathrev=66868
 M http://src.chromium.org/viewvc/chrome/branches/552d/src/chrome/app/generated_resources.grd?r1=66868&r2=66867&pathrev=66868
 M http://src.chromium.org/viewvc/chrome/branches/552d/src/chrome/browser/cocoa/content_exceptions_window_controller.mm?r1=66868&r2=66867&pathrev=66868
 M http://src.chromium.org/viewvc/chrome/branches/552d/src/webkit/glue/plugins/webplugin_delegate_impl_mac.mm?r1=66868&r2=66867&pathrev=66868
 M http://src.chromium.org/viewvc/chrome/branches/552d/src/chrome/app/nibs/ContentSettings.xib?r1=66868&r2=66867&pathrev=66868
 M http://src.chromium.org/viewvc/chrome/branches/552d/src/chrome/browser/renderer_host/browser_render_process_host.cc?r1=66868&r2=66867&pathrev=66868

Reintegrate 552 r66225-r66645.

------
66466 17.11.2010 19:09:22, by bauerb@chromium.org
Tentative compile fix after merge error.

TBR=kerz
-----
66453 17.11.2010 18:17:09, by bauerb@chromium.org
Merge 65953 -- Move click-to-play to about:flags.

XIB changes: Add an outlet |pluginDefaultSettingMatrix_| to ContentSettingsDialogController, hooked up to the associated matrix, to remove the click-to-play radio button.

While I'm at it, clean up a bit:
* Remove the old --disable-click-to-play flag that reverted to the M6 behavior for blocked plugins
* Make ContentExceptionsWindowController use ContentSettingComboModel for the action popup.
* Make HostContentSettingsMapTest use AutoReset to reset command line switches.

BUG=62091
TEST=unit_tests

Review URL: http://codereview.chromium.org/4643007
-----
66581 18.11.2010 03:23:22, by cevans@chromium.org
Merge 66567 - Fix XPath bug from upstream.

BUG=63444
TEST=See bug

Review URL: http://codereview.chromium.org/5196003

TBR=cdn@chromium.org
Review URL: http://codereview.chromium.org/5216001
-----
66642 18.11.2010 19:14:57, by thakis@chromium.org
Merge 66631 - Mac: Only clear the background of CoreAnimation plugins if we're going to draw into them.

Previously, the logic was:

1.) Clear plugin background
2.) If the plugin didn't update, return early
3.) Paint plugin
4.) "Swap buffers"

But the "Swap buffers" step only unbound and rebound an FBO object If the plugin didn't change, its backing store would contain transparent black, and if the graphics driver decided to flush the FBO for another reason than a "swap buffers" call, the blackness would show up in the browser.

This CL swaps steps 1 and 2, so even if the FBO is flushed for some unrelated reason, we display something valid.

BUG=60341
TEST=Open the file attached to the bug. Resize the window for a few minutes, put the computer to sleep and back on, resize window for a few more minutes. The plugin area (the 191x60px rect in the middle) shouldn't become black. YouTube should still work. CPU usage shouldn't be worse than it was before for the browser, plugin, and renderer processes.

Review URL: http://codereview.chromium.org/5220002

TBR=thakis@chromium.org
Review URL: http://codereview.chromium.org/5167003
-----
66645 18.11.2010 19:30:53, by willchan@chromium.org
Merge 66630 - Fix SPDY crash on race when canceling a stream that just got created.

When I fixed the code not to be re-entrant (since that caused crashes) in r61880, I created a window when the pending create callback was posted to the MessageLoop to be run on the next iteration. In this window before it actually gets invoked, if the pending stream creation got cancelled, then the callback wasn't cancelled, so we would execute a callback on a cancelled stream creation, which can cause crashes.

The fix is to keep track of the pending callbacks. Cancellation of pending stream creations check this pending callback map first.

BUG=63532
TEST=See bug thread for repro steps. New unit test added as well.

Review URL: http://codereview.chromium.org/5174005

TBR=willchan@chromium.org
Review URL: http://codereview.chromium.org/5216002
-----


Review URL: http://codereview.chromium.org/5238002
------------------------------------------------------------------------

### sc...@gmail.com (2010-11-29)

[Empty comment from Monorail migration]

### sc...@gmail.com (2010-12-03)

@yangdingning: e-mail cevans@chromium.org to get set up for collecting your reward! :)

### sc...@gmail.com (2010-12-14)

[Empty comment from Monorail migration]

### sc...@gmail.com (2010-12-20)

Payment is in the electronic system.

### js...@chromium.org (2011-03-21)

[Empty comment from Monorail migration]

### js...@chromium.org (2011-10-05)

Batch update.

### js...@chromium.org (2012-07-13)

CC'ing Debian libxml maintainer.

### bu...@chromium.org (2012-10-13)

This issue has been closed for some time. No one will pay attention to new comments.
If you are seeing this bug or have new data, please click New Issue to start a new bug.

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-11)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-13)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

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

This issue was migrated from crbug.com/chromium/63444?no_tracker_redirect=1

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40085028)*
