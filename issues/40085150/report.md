# Security: UXSS introduced through bookmark containing user information

| Field | Value |
|-------|-------|
| **Issue ID** | [40085150](https://issues.chromium.org/issues/40085150) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>Bookmarks |
| **Reporter** | g_...@flamescape.com |
| **Assignee** | el...@chromium.org |
| **Created** | 2016-08-18 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**  

Chrome's "Edit Bookmark" dialogue window strips the opening "http://" from the URL field, if it exists. If the URI also contains user (auth) information, then saving the bookmark will change the URI scheme of the bookmark. This bug can be exploited to introduce XSS into the currently open page whenever the bookmark is clicked.

**VERSION**  

Chrome Version: 52.0.2743.116 stable  

Operating System: Windows 10 Pro

**REPRODUCTION CASE**

1. The victim clicks on a specially crafted link whose URL contains malicious javascript disguised as user (auth) information:
   
   <a href='http://javascript:eval(atob("YWxlcnQoIlhTUyIp"))-"@example.com/#"'>Click Me!</a>
2. The browser loads the page at example.com.  
   
   The victim's URL bar only displays the (innocuous looking) text: example.com/#"
3. The user, in an attempt to bookmark the page, performs the following actions:  
   
   a. Click the star icon in the URL bar  
   
   b. Click "Edit..." -or- Click "Choose another folder..." within the Folder drop-down  
   
   c. Click "Save"
4. If the user then clicks on the bookmark, the injected javascript from Step 1 will be executed in the context of whichever domain is currently loaded in the active tab.

Please let me know if you require further information.

## Timeline

### ji...@chromium.org (2016-08-18)

Thanks for reporting, g_google@flamescape.com!

+ianwen@, could you help triage this issue? It looks similar to https://crbug.com/chromium/481015.  Please feel free to suggest other owner. 



[Monorail components: UI>Browser>Bookmarks UI>Browser>Bookmarks>Enhanced]

### ji...@chromium.org (2016-08-18)

[Empty comment from Monorail migration]

### ia...@chromium.org (2016-08-18)

Hmm this is windows 10?

I am not sure who is working on bookmark for desktop now. Since it's a security issue, I would reassign it to felt@ and let her decide?

### ji...@chromium.org (2016-08-18)

it can be reproduced on linux as well. I haven't tested it on mobile, but I guess this issue is not specific to a particular OS.
+felt@, could you suggest a owner? 

### fe...@chromium.org (2016-08-19)

Re #13: Feature teams are responsible for fixing the bugs in their areas of code. The security team is just here to triage and help provide advice if you need it. We wouldn't be able to scale up to fix all security bugs in all features. So in this case, someone on the bookmarks team ought to investigate this. :)

shrike@ - it looks like you have been fixing bookmarks-related bugs, do you know who owns bookmarks now?

### sh...@chromium.org (2016-08-19)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-08-19)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-08-23)

I've only been doing UI work on bookmarks on the Mac. I'm not sure who would be a good person for this fix, but taking a stab at rdevlin.cronin@.


### rd...@chromium.org (2016-08-23)

@5, @8 it looks like sky@ owns bookmarks (components/bookmarks and c/b/bookmarks).  Over to him for triage.

### sh...@chromium.org (2016-09-02)

sky: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-09-17)

sky: Uh oh! This issue still open and hasn't been updated in the last 29 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### el...@chromium.org (2016-09-21)

https://cs.chromium.org/chromium/src/chrome/browser/ui/views/bookmarks/bookmark_editor_view.cc?sq=package:chromium&dr=C&l=380

calls:
    url_tf_->SetText(chrome::FormatBookmarkURLForDisplay(url));

That, in turn, is commented thusly:
base::string16 FormatBookmarkURLForDisplay(const GURL& url) {
  // Because this gets re-parsed by FixupURL(), it's safe to omit the scheme
  // and trailing slash, and unescape most characters.  However, it's
  // important not to drop any username/password, or unescape anything that
  // changes the URL's meaning.
  return url_formatter::FormatUrl(
      url, url_formatter::kFormatUrlOmitAll &
               ~url_formatter::kFormatUrlOmitUsernamePassword,
      net::UnescapeRule::SPACES, nullptr, nullptr, nullptr);
}

Keeping the userinfo (username/password) is not compatible with omitting the scheme, because most schemes work like scheme://user:password@host/path and if you omit the scheme it becomes user:password@host, which, upon reinterpretation, is indistinguishable from scheme:user@host, because non-hierarchical schemes use ":" rather than "://" as the scheme delimiter.

To fix, we could change (url_formatter::kFormatUrlOmitAll & ~url_formatter::kFormatUrlOmitUsernamePassword) to kFormatUrlOmitTrailingSlashOnBareHostname, or we could more selectively do so iff the URL contains a userinfo component. I'm inclined to say that we should just always show the scheme, especially because today it's only omitted for HTTP (not HTTPS) and HTTPS is getting ever more common.

### el...@chromium.org (2016-09-21)

[Empty comment from Monorail migration]

### ji...@chromium.org (2016-09-21)

Thanks for taking on this elawrence@. 

### el...@chromium.org (2016-09-23)

https://codereview.chromium.org/2368593002

### bu...@chromium.org (2016-10-03)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/fa34e547d6ee25ea0692436ba7462ed0a0ef45f4

commit fa34e547d6ee25ea0692436ba7462ed0a0ef45f4
Author: elawrence <elawrence@chromium.org>
Date: Mon Oct 03 18:41:02 2016

Prevent interpretating userinfo as url scheme when editing bookmarks

Chrome's Edit Bookmark dialog formats urls for display such that a
url of http://javascript:scripttext@host.com is later converted to a
javascript url scheme, allowing persistence of a script injection
attack within the user's bookmarks.

This fix prevents such misinterpretations by always showing the
scheme when a userinfo component is present within the url.

BUG=639126

Review-Url: https://codereview.chromium.org/2368593002
Cr-Commit-Position: refs/heads/master@{#422467}

[modify] https://crrev.com/fa34e547d6ee25ea0692436ba7462ed0a0ef45f4/chrome/browser/ui/bookmarks/bookmark_utils.cc
[modify] https://crrev.com/fa34e547d6ee25ea0692436ba7462ed0a0ef45f4/chrome/browser/ui/bookmarks/bookmark_utils.h
[modify] https://crrev.com/fa34e547d6ee25ea0692436ba7462ed0a0ef45f4/chrome/browser/ui/cocoa/bookmarks/bookmark_editor_controller_unittest.mm
[modify] https://crrev.com/fa34e547d6ee25ea0692436ba7462ed0a0ef45f4/chrome/browser/ui/views/bookmarks/bookmark_editor_view_unittest.cc


### el...@chromium.org (2016-10-03)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-04)

[Empty comment from Monorail migration]

### el...@chromium.org (2016-10-05)

Externally reported, so requesting merge to M-54

### di...@chromium.org (2016-10-05)

[Automated comment] Less than 2 weeks to go before stable on M54, manual review required.

### bu...@google.com (2016-10-06)

SGTM, approved for merging into M54

### bu...@chromium.org (2016-10-10)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/2775e31152857adc2bb9775b03212d1356541b4b

commit 2775e31152857adc2bb9775b03212d1356541b4b
Author: Andrew R. Whalley <awhalley@chromium.org>
Date: Mon Oct 10 21:47:53 2016

[merge to m54] Prevent interpretating userinfo as url scheme when editing bookmarks

Chrome's Edit Bookmark dialog formats urls for display such that a
url of http://javascript:scripttext@host.com is later converted to a
javascript url scheme, allowing persistence of a script injection
attack within the user's bookmarks.

This fix prevents such misinterpretations by always showing the
scheme when a userinfo component is present within the url.

BUG=639126

Review-Url: https://codereview.chromium.org/2368593002
Cr-Commit-Position: refs/heads/master@{#422467}
(cherry picked from commit fa34e547d6ee25ea0692436ba7462ed0a0ef45f4)

Review URL: https://codereview.chromium.org/2411473002 .

Cr-Commit-Position: refs/branch-heads/2840@{#708}
Cr-Branched-From: 1ae106dbab4bddd85132d5b75c670794311f4c57-refs/heads/master@{#414607}

[modify] https://crrev.com/2775e31152857adc2bb9775b03212d1356541b4b/chrome/browser/ui/bookmarks/bookmark_utils.cc
[modify] https://crrev.com/2775e31152857adc2bb9775b03212d1356541b4b/chrome/browser/ui/bookmarks/bookmark_utils.h
[modify] https://crrev.com/2775e31152857adc2bb9775b03212d1356541b4b/chrome/browser/ui/cocoa/bookmarks/bookmark_editor_controller_unittest.mm
[modify] https://crrev.com/2775e31152857adc2bb9775b03212d1356541b4b/chrome/browser/ui/views/bookmarks/bookmark_editor_view_unittest.cc


### aw...@chromium.org (2016-10-10)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-10-10)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-10-11)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-10-15)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-10-16)

Nice one, the panel awarded $500 for this bug.  They noted it's not really a UXSS, and needs a fairly uncommon combination of user interaction.  Thanks for the report!  A member of our finance team will be in touch shortly.

### aw...@chromium.org (2016-10-16)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-10-16)

[Empty comment from Monorail migration]

### bu...@chromium.org (2016-10-27)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/2775e31152857adc2bb9775b03212d1356541b4b

commit 2775e31152857adc2bb9775b03212d1356541b4b
Author: Andrew R. Whalley <awhalley@chromium.org>
Date: Mon Oct 10 21:47:53 2016

[merge to m54] Prevent interpretating userinfo as url scheme when editing bookmarks

Chrome's Edit Bookmark dialog formats urls for display such that a
url of http://javascript:scripttext@host.com is later converted to a
javascript url scheme, allowing persistence of a script injection
attack within the user's bookmarks.

This fix prevents such misinterpretations by always showing the
scheme when a userinfo component is present within the url.

BUG=639126

Review-Url: https://codereview.chromium.org/2368593002
Cr-Commit-Position: refs/heads/master@{#422467}
(cherry picked from commit fa34e547d6ee25ea0692436ba7462ed0a0ef45f4)

Review URL: https://codereview.chromium.org/2411473002 .

Cr-Commit-Position: refs/branch-heads/2840@{#708}
Cr-Branched-From: 1ae106dbab4bddd85132d5b75c670794311f4c57-refs/heads/master@{#414607}

[modify] https://crrev.com/2775e31152857adc2bb9775b03212d1356541b4b/chrome/browser/ui/bookmarks/bookmark_utils.cc
[modify] https://crrev.com/2775e31152857adc2bb9775b03212d1356541b4b/chrome/browser/ui/bookmarks/bookmark_utils.h
[modify] https://crrev.com/2775e31152857adc2bb9775b03212d1356541b4b/chrome/browser/ui/cocoa/bookmarks/bookmark_editor_controller_unittest.mm
[modify] https://crrev.com/2775e31152857adc2bb9775b03212d1356541b4b/chrome/browser/ui/views/bookmarks/bookmark_editor_view_unittest.cc


### sh...@chromium.org (2017-01-10)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/639126?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40085150)*
