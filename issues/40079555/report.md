# javascript: url with a leading NULL byte can bypass cross origin protection.

| Field | Value |
|-------|-------|
| **Issue ID** | [40079555](https://issues.chromium.org/issues/40079555) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Internals, Internals>Core |
| **Reporter** | ku...@gmail.com |
| **Assignee** | js...@chromium.org |
| **Created** | 2010-03-04 |
| **Bounty** | $1,000.00 |

## Description

# **(Describe security bug here, with as much details and steps to reproduce as** **possible. Security bugs are visible only to the reporter and to project** **members.)** see sample hehe.html

<iframe name="test" src="http://www.g.cn"></iframe>
<input type=button value="test"
onclick="window.open('\u0000javascript:alert(document.cookie)','test')" >
==================================
or
==================================
<iframe name="test" src="http://www.g.cn"></iframe>
<input type=button value="test"
onclick="window.open('\x00javascript:alert(document.cookie)','test')" >
==================================

## Attachments

- deleted (application/octet-stream, 0 B)

## Timeline

### sk...@chromium.org (2010-03-04)

Confirmed. I expect one of our checks stops when it encounters a NULL byte and reports 
the (empty) URL is ok to load in the context of the page. The code that handles the URL 
ignores the NULL byte and executes the javascript.

Tentatively assigning Internals->Core

### ku...@gmail.com (2010-03-04)

yes!;D

### sk...@chromium.org (2010-03-04)

[Empty comment from Monorail migration]

### ab...@chromium.org (2010-03-04)

I'll look at this tonight.

### ab...@chromium.org (2010-03-04)

[Empty comment from Monorail migration]

### ku...@gmail.com (2010-03-04)

i am so happy than finally i can get the Reward and buy a new computer hahahahahahaha 
thanks google

### lc...@gmail.com (2010-03-04)

skylined, any char such as \x20 or \x09 works. I suspect it's a 
.startsWith("javascript:") security check, again :-( 

### lc...@gmail.com (2010-03-04)

Specifically, isn't this related to http://code.google.com/p/chromium/issues/detail?
id=30660, and to how protocolIs() is implemented in KURL?


### js...@chromium.org (2010-03-04)

Well, it's not exactly StartsWith(), but the same thing for all intents and purposes. 
In BindingDOMWindow::createWindow() there's a call to protocolIsJavaScript(), which 
is a thin wrapper over protocolIs(), which is basically just reimplemented version of 
StartsWith().

However, I'd say the real problem is completely inconsistent whitespace handling. 
After the JavaScript check url_parse::TrimURL() eventually gets called, and clears 
out every surrounding character less than space. Here's the relevant stack:

url_parse::ShouldTrimFromURL(wchar_t ch=0x0000)  Line 46
url_parse::TrimURL<wchar_t>(const wchar_t * spec=0x074eaeb4, int * begin=0x04cfce88, 
int * len=0x04cfcea4)  Line 58
url_canon::`anonymous namespace'::DoIsRelativeURL<wchar_t>(const char * 
base=0x075bda20, const url_parse::Parsed & base_parsed={...}, const wchar_t * 
url=0x074eaeb4, int url_len=0x00000022, bool is_base_hierarchical=true, bool * 
is_relative=0x04cfceff, url_parse::Component * relative_component=0x04cfceec)  Line 
98
url_canon::IsRelativeURL(const char * base=0x075bda20, const url_parse::Parsed & 
base_parsed={...}, const wchar_t * fragment=0x074eaeb4, int fragment_len=0x00000022, 
bool is_base_hierarchical=true, bool * is_relative=0x04cfceff, url_parse::Component * 
relative_component=0x04cfceec)  Line 543
url_util::`anonymous namespace'::DoResolveRelative<wchar_t>(const char * 
base_spec=0x075bda20, int base_spec_len=0x00000017, const url_parse::Parsed & 
base_parsed={...}, const wchar_t * in_relative=0x074eaeb4, int 
in_relative_length=0x00000022, url_canon::CharsetConverter * 
charset_converter=0x04cfdbbc, url_canon::CanonOutputT<char> * output=0x04cfd7a0, 
url_parse::Parsed * output_parsed=0x04cfdc74)  Line 250
url_util::ResolveRelative(const char * base_spec=0x075bda20, int 
base_spec_len=0x00000017, const url_parse::Parsed & base_parsed={...}, const wchar_t 
* relative=0x074eaeb4, int relative_length=0x00000022, url_canon::CharsetConverter * 
charset_converter=0x04cfdbbc, url_canon::CanonOutputT<char> * output=0x04cfd7a0, 
url_parse::Parsed * output_parsed=0x04cfdc74)  Line 403
WebCore::KURLGooglePrivate::init(const WebCore::KURL & 
base="http://localhost:28876/", const wchar_t * rel=0x074eaeb4, int 
relLength=0x00000022, const WebCore::TextEncoding * queryEncoding=0x07568b8c)  Line 
253
WebCore::KURLGooglePrivate::init(const WebCore::KURL & 
base="http://localhost:28876/", const WebCore::String & relative="", const 
WebCore::TextEncoding * queryEncoding=0x07568b8c)  Line 193
WebCore::KURL::KURL(const WebCore::KURL & base="http://localhost:28876/", const 
WebCore::String & relative="", const WebCore::TextEncoding & encoding={...})  Line 
395
WebCore::Document::completeURL(const WebCore::String & url="")  Line 3392
WebCore::FrameLoader::completeURL(const WebCore::String & url="")  Line 1196
WebCore::completeURL(const WebCore::String & relativeURL="")  Line 115
WebCore::BindingDOMWindow<WebCore::V8Binding>::createWindow(WebCore::State<WebCore::V
8Binding> * state=0x04fc0938, WebCore::Frame * callingFrame=0x0765d000, 
WebCore::Frame * enteredFrame=0x0765d000, WebCore::Frame * openerFrame=0x0765d000, 
const WebCore::String & url="", const WebCore::String & frameName="test", const 
WebCore::WindowFeatures & windowFeatures={...}, v8::Handle<v8::Value> 
dialogArgs={...})  Line 112

The immediate fix is to just move the call to completeURL() up two lines in 
BindingDOMWindow::createWindow, which puts it before the protocolIsJavaScript() test. 
However, does it also make sense to modify protocolIs() to ignore leading whitespace 
in the same way that url_parse::TrimURL() does (just in case similar bugs are hiding 
elsewhere)?


### ab...@chromium.org (2010-03-05)

The best thing might be to have protocolIs canonicalize the URL.  Re-assigning to
Justin since he seems to be on top of this bug.  IMHO, we should nuke all these URLs
with String type and just use the KURL type to represent them.

### ku...@gmail.com (2010-03-05)

replace \x00 \x20 \x09 in url header is simple

### js...@chromium.org (2010-03-05)

Adam, yeah I can grab this, but the fix will probably have to wait until Monday because 
I don't currently have a WebKit build environment set up. 

Also, if there's no objections I'm just going to fix the whitespace handling in protocolIs(). That strikes me as the easiest way to get a fix to stable. In the long 
run, however, I agree that we should move off of passing URL strings like we are.


### js...@chromium.org (2010-03-08)

Behavior on Safari and WebKit nightly is odd. The alert doesn't get popped, but we end 
up creating nested frames (which shouldn't happen either). Poking at that a little more 
before I file upstream.

### sc...@gmail.com (2010-03-09)

Great bug!

### js...@chromium.org (2010-03-09)

[Empty comment from Monorail migration]

### sc...@gmail.com (2010-03-09)

@kuzzcc: subject to continued responsible disclosure, we'd like to offer you $1000 (2 
x $500; this counts as two bugs). If you accept, please e-mail cevans@chromium.org to 
start the payment. Thanks again for the report!

### ku...@gmail.com (2010-03-09)

en thank you

### js...@chromium.org (2010-03-10)

Reported upstream here: https://bugs.webkit.org/show_bug.cgi?id=35948

I'll have the patch submitted by tomorrow morning.


### js...@chromium.org (2010-03-10)

[Empty comment from Monorail migration]

### bu...@gmail.com (2010-03-11)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=41244 

------------------------------------------------------------------------
r41244 | mal@chromium.org | 2010-03-10 18:32:39 -0800 (Wed, 10 Mar 2010) | 8 lines
Changed paths:
   A http://src.chromium.org/viewvc/chrome/branches/WebKit/249/LayoutTests/http/tests/security/xss-DENIED-window-open-javascript-url-leading-format-char-expected.txt
   A http://src.chromium.org/viewvc/chrome/branches/WebKit/249/LayoutTests/http/tests/security/xss-DENIED-window-open-javascript-url-leading-format-char.html
   M http://src.chromium.org/viewvc/chrome/branches/WebKit/249/WebCore/platform/KURLGoogle.cpp?r1=41244&r2=41243

Merge WebKit r55822:

Make Chrome consistently handle leading format characters in URLs

TBR= jschuh
BUG= http://crbug.com/37383
TEST= layout tests
Review URL: http://codereview.chromium.org/858001
------------------------------------------------------------------------


### bu...@gmail.com (2010-03-11)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=41247 

------------------------------------------------------------------------
r41247 | dpranke@chromium.org | 2010-03-10 18:40:11 -0800 (Wed, 10 Mar 2010) | 7 lines
Changed paths:
   M http://src.chromium.org/viewvc/chrome/trunk/src/webkit/tools/layout_tests/test_expectations.txt?r1=41247&r2=41246

Adds a LayoutTest exclusion to cover differences between GURL and KURL.

Committing on behalf of jschuh@google.com

BUG=37383
TEST=None
R=dpranke@chromium.org
------------------------------------------------------------------------


### sc...@gmail.com (2010-03-11)

Justin / Adam / Mark landed this on WebKit ToT & 249 branch. Marking FixUnreleased.

### [Deleted User] (2010-03-16)

Verified in build 4.1.249.1036 (Official Build 41514), it has been fixed.

### js...@chromium.org (2010-03-16)

[Empty comment from Monorail migration]

### sc...@gmail.com (2010-03-23)

Releasing due to fix in 4.1.249.1036.

### js...@chromium.org (2011-03-21)

[Empty comment from Monorail migration]

### js...@chromium.org (2011-10-05)

Batch update.

### bu...@chromium.org (2012-10-13)

This issue has been closed for some time. No one will pay attention to new comments.
If you are seeing this bug or have new data, please click New Issue to start a new bug.

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### is...@google.com (2016-10-02)

This issue was migrated from crbug.com/chromium/37383?no_tracker_redirect=1

[Multiple monorail components: Internals, Internals>Core]
[Monorail mergedwith: crbug.com/chromium/38277]
[Monorail components added to Component Tags custom field.]

### pe...@google.com (2024-02-04)

Setting Priority to P1 to match Severity s1. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40079555)*
