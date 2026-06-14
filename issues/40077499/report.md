# Cross-origin named subframe access leaks cross-origin subframes of the same name

| Field | Value |
|-------|-------|
| **Issue ID** | [40077499](https://issues.chromium.org/issues/40077499) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Unknown |
| **Reporter** | bo...@gmail.com |
| **Assignee** | ab...@chromium.org |
| **Created** | 2013-04-30 |
| **Bounty** | $1,500.00 |

## Description

**VULNERABILITY DETAILS**  

This is really a spec issue, I think, but given that there's no way to file security-sensitive HTML5 bugs, I'm just filing bugs on all the affected vendors. We can fix the spec once everyone is in good shape here.

The basic problem is as follows. Since Window is not [OverrideBuiltins], named subframes are not supposed to be able to shadow builtin properties. So if a page has an iframe with name="localStorage", resolving |localStorage| in global scope should still give the storage object rather than the subframe window. This seems to be the behavior in the UAs I've tested.

However, we run into trouble when we throw cross-origin access to named subframes into the mix. The spec currently doesn't allow this, but all UAs do, so I'd previously filed [1] to make the spec match reality on this issue.

Most UAs seem to implement cross-origin security checks by a whitelist of properties followed by an IsFrameIndexOrName-esque check for indexed and named subframes. So the same-origin policy enforcement ends up granting access to any name that matches a subframe name, but the subsequent lookup ends up selecting the builtin property over the subframe, creating a cross-origin leak.

Due to some other implementational wonkiness, this was a non-issue in Gecko until Firefox 22 (currently Aurora, still 8 weeks from release). While fixing that wonkiness, I discovered this issue, and fixed it on Nightly and Aurora in [2]. I then did some cross-browser testing, and discovered that this was a problem in Chrome (and a worse one, because security wrappers mostly save us here in Gecko). In my testcase, Chrome leaks localStorage and navigator. Safari and IE don't leak anything AFAICT.

The solution I implemented in [2] was to deny cross-origin access (at policy enforcement time) to named subframes that would *end up* resolving to a non-cross-origin-accessible property of the window. This seems like the safest behavior to me, but I'm happy to discuss alternatives with everyone if that turns out to be difficult for other vendors to implement.

[1] <https://www.w3.org/Bugs/Public/show_bug.cgi?id=21674>  

[2] <https://bugzilla.mozilla.org/show_bug.cgi?id=860494>

**VERSION**  

stable

**REPRODUCTION CASE**  

Testcases attached. Put a and b on cross-origin hosts and update the URL in a.

## Attachments

- [a.html](attachments/a.html) (text/html; charset=us-ascii, 1.1 KB)
- [b.html](attachments/b.html) (text/html; charset=us-ascii, 455 B)

## Timeline

### ts...@chromium.org (2013-05-01)

I had initially thought that this would be low severity, because good.com would have to generate iframes with these particular names, which seemed unlikely.  But if good.com allows framing evil.org (think Ad networks), then evil.org can do something like:
  <script>window.name='navigator';alert(window.parent.navigator.vendor);</script>
and force the conflict onto the parent and reap the results.

Setting severity medium, but this may be high.


### ts...@chromium.org (2013-05-01)

[Empty comment from Monorail migration]

### bo...@gmail.com (2013-05-01)

Yeah, per https://crbug.com/chromium/237022#c1 this effectively means that any non-sandboxed iframe can pull this trick on its parent assuming that window.name is properly reflected into the browsing context tree.

I've rated the associated mozilla bug as sec-high.

### ts...@chromium.org (2013-05-01)

Looks like in V8DOMWindow::namedSecurityCheckCustom(), we're returning true for "localStorage" via:
       if (type == v8::ACCESS_GET && childFrame && !host->HasRealNamedProperty(key->ToString()) && name != nameOfProtoProperty)
            return true;

as it appears host->HasRealNamedProperty() => false.


### ts...@chromium.org (2013-05-01)

[Empty comment from Monorail migration]

### ts...@chromium.org (2013-05-01)

Adam, please take a look when you get a chance.

### ts...@chromium.org (2013-05-01)

[Empty comment from Monorail migration]

### in...@chromium.org (2013-05-02)

Please do read Mark's email titled "Calling a Code 28 for Security Bugs" on chrome-team mailing list.

### bo...@gmail.com (2013-05-02)

> Please do read Mark's email titled "Calling a Code 28 for Security Bugs"
> on chrome-team mailing list.

Was that directed at me? I can't find this list anywhere. Is it public?

### ts...@chromium.org (2013-05-02)

Bobby - No, it was part of a mass-update directed at Chromium developers.

### sc...@gmail.com (2013-05-03)

[Empty comment from Monorail migration]

### in...@chromium.org (2013-05-07)

Adam, can you please help us with this one for security code 28. 

### bo...@gmail.com (2013-05-07)

This seems pretty clearly sec-high to me. Can someone provide the rational for moderate?

### ts...@chromium.org (2013-05-07)

I had originally rated this as medium under the "limited amount of information"; you don't get full unfettered access to the DOM, as far as I can tell.  You don't get document.cookie, for example, just a handful of objects like Navigator.  But since one of these objects is localStorage, that probably crosses the "confidential information of other sites" threshold.

### sc...@gmail.com (2013-05-10)

@abarth: do you have cycles to knock this one over?

### ab...@chromium.org (2013-05-10)

Sure.  It will probably need to wait until Monday, if that's ok.

### in...@chromium.org (2013-05-10)

Yes, Monday works. Thanks Adam.

### pa...@chromium.org (2013-05-11)

[Empty comment from Monorail migration]

### sc...@gmail.com (2013-05-17)

@abarth, curious if you made any progress?

### ab...@chromium.org (2013-05-17)

Sorry, I forgot about this one.  Looking now.

### ab...@chromium.org (2013-05-17)

Nasty...  Bobby, your approach sounds good.  Let me try that.

### ab...@chromium.org (2013-05-17)

Verified.

### ab...@chromium.org (2013-05-17)

Short test case:

<iframe sandbox="allow-scripts"
        src="data:text/html,<script>window.name='navigator';alert(top.navigator);</script>"></iframe>

### ab...@chromium.org (2013-05-17)

https://codereview.chromium.org/15346002

### in...@chromium.org (2013-05-18)

https://src.chromium.org/viewvc/blink?view=rev&revision=150616

### bu...@chromium.org (2013-05-18)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/blink?view=rev&rev=150616

------------------------------------------------------------------------
r150616 | abarth@chromium.org | 2013-05-18T00:40:09.730308Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/trunk/Source/bindings/v8/custom/V8DOMWindowCustom.cpp?r1=150616&r2=150615&pathrev=150616
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/http/tests/security/xss-DENIED-window-name-alert.html?r1=150616&r2=150615&pathrev=150616
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/http/tests/security/xss-DENIED-window-name-navigator.html?r1=150616&r2=150615&pathrev=150616
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/http/tests/security/xss-DENIED-window-name-alert-expected.txt?r1=150616&r2=150615&pathrev=150616
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/http/tests/security/xss-DENIED-window-name-navigator-expected.txt?r1=150616&r2=150615&pathrev=150616

Named access checks on DOMWindow miss navigator

The design of the named access check is very fragile. Instead of doing the
access check at the same time as the access, we need to check access in a
separate operation using different parameters. Worse, we need to implement a
part of the access check as a blacklist of dangerous properties.

This CL expands the blacklist slightly by adding in the real named properties
from the DOMWindow instance to the current list (which included the real named
properties of the shadow object).

In the longer term, we should investigate whether we can change the V8 API to
let us do the access check in the same callback as the property access itself.

BUG=237022

Review URL: https://chromiumcodereview.appspot.com/15346002
------------------------------------------------------------------------

### sc...@gmail.com (2013-05-28)

M27 is r151274


### sc...@gmail.com (2013-05-28)

M28 is r151275

### sc...@gmail.com (2013-06-03)

@bobbyholley: thanks for a really interesting report! It qualifies for a $1500 Chromium Security Reward.

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties.
*********************************

### pa...@chromium.org (2013-06-24)

Payment is on the way...

### js...@chromium.org (2013-08-13)

Adding hixie in. Once the spec is updated and we don't think other browsers are affected we should open this.

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

### sh...@chromium.org (2018-07-29)

[Empty comment from Monorail migration]

### is...@google.com (2018-07-29)

This issue was migrated from crbug.com/chromium/237022?no_tracker_redirect=1

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40077499)*
