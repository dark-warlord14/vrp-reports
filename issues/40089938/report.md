# Bypass extensions permission

| Field | Value |
|-------|-------|
| **Issue ID** | [40089938](https://issues.chromium.org/issues/40089938) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Platform>Extensions |
| **Reporter** | ku...@gmail.com |
| **Assignee** | [Deleted User] |
| **Created** | 2011-04-15 |
| **Bounty** | $500.00 |

## Description

Test chrome 12.0.733.0 dev windows xp sp3

1,install testcase.crx

see result

## Attachments

- deleted (application/octet-stream, 0 B)
- [testcase.crx](attachments/testcase.crx) (application/octet-stream; charset=binary, 775 B)

## Timeline

### ku...@gmail.com (2011-04-15)

[Empty comment from Monorail migration]

### ku...@gmail.com (2011-04-15)

chrome.windows.create

### ku...@gmail.com (2011-04-15)

[Comment Deleted]

### in...@chromium.org (2011-04-15)

Kuzzcc, I see a vuln in the first one, but not in the 2nd testcase. 

1. Testcase.crx
Yeah, tabs permission should not allow to get content from arbitary origins.

<script>
inject_str = 'javascript:x = new XMLHttpRequest(); x.open(\'get\', \'http://jquery.com\', false); x.send(); alert(x.responseText)'
chrome.tabs.create({url: inject_str})
</script>


2. Bookmark.crx
The extension install is creating a bookmark with a javascript url. bookmark when clicked executes the javascript url in the context of the domain. Normal bookmarks work in the same way. and i dont see a reason why should prevent that. I remember filing a bug in this regard and now they should the url in the tooltip. I dont see anything else they can do here.

<script>
chrome.bookmarks.create({parentId: '1', title: 'clickme', url: 'javascript:alert(document.domain)'})
</script>

### aa...@chromium.org (2011-04-15)

ffff. I thought I checked to make sure create() didn't have the same problem as update(), but apparently did not understand. I will check the window.create/update methods again.

### aa...@chromium.org (2011-04-15)

Ok, I remember why I thought this was OK now. The javascript string executes in the main world with no special privileges from the extension system. It should be just the same as a web page doing: window.open("javascript:...").

Since there is no previous URL, the content is about:blank, which is not interesting -- so there is nothing to protect, so no need to do anything special in extension system.

However, somehow that JavaScript ends up getting cross-origin request privileges. How?

I've traced it to:

http://www.google.com/codesearch/p#OAMlx_jo-ck/src/third_party/WebKit/Source/WebCore/loader/DocumentThreadableLoader.cpp&l=225

We zig when we should zag here. I think perhaps we end up with the incorrect SecurityOrigin instance in the document, causing this check to go the wrong way. I'm not sure why yet.

Note that in both cases, from javascript's point of view, the URL is 'about:blank'. But there are other flags in SecurityOrigin that might not be getting set correctly.

### ab...@chromium.org (2011-04-15)

Generally, about:blank inherits its securityOrigin from it's opener.  Who is the opener in this case?

### aa...@chromium.org (2011-04-15)

There is no opener. An extension (in a totally different process) is calling chrome.tabs.create(), which ends up telling the browser process to open a tab and navigate it to "javascript:...".

I've verified the same thing happens if I navigate a new tab to about:blank, then type this code into devtools.

Can we make about:blank default to the null origin?

### ab...@chromium.org (2011-04-15)

> Can we make about:blank default to the null origin?

Yes.  about:blank should default to the "empty" origin if there's no opener.

### ab...@chromium.org (2011-04-15)

Yeah, that's all kinds of wrong.  Investigating.

### ku...@gmail.com (2011-04-15)

[Comment Deleted]

### ab...@chromium.org (2011-04-15)

Testing a patch now.

### ku...@gmail.com (2011-04-15)

[Comment Deleted]

### aa...@chromium.org (2011-04-15)

Hm. I guess we could somehow tag bookmarks as having come from an extension, then check that extension's permission before running?

### ab...@chromium.org (2011-04-15)

Maybe extensions shouldn't be able to create bookmarks with JavaScript URLs?  They can just script the pages directly or add browser / page actions.

### in...@chromium.org (2011-04-17)

Fixed in http://trac.webkit.org/changeset/84099.

Filed seperate low severity bug for bookamrks with javascript url issue.

### ab...@chromium.org (2011-04-17)

Thanks inferno!

### sc...@gmail.com (2011-05-02)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-05-02)

This is already in M12 (which branched at WebKit r84325)

### sc...@gmail.com (2011-06-02)

@kuzzcc: thanks for this bug! Although we don't reward too many Medium severity bugs, we'd like to offer you a $500 Chromium Security Reward for this one. Thanks for continuing to help with extensions permission security.

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

Oops forgot to pay this one with your $1337 reward, will pay it out separately now, sorry about that.

### sc...@gmail.com (2011-07-03)

Invoice finalized; payment is in e-payment system; it can take a couple of weeks.

### js...@chromium.org (2011-10-05)

Batch update.

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

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### is...@google.com (2016-10-02)

This issue was migrated from crbug.com/chromium/79566?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40089938)*
