# Security: Postpwnium: Full exploit chain for ChromeOS

| Field | Value |
|-------|-------|
| **Issue ID** | [40077347](https://issues.chromium.org/issues/40077347) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P4 |
| **Component** | Unknown |
| **Reporter** | es...@gmail.com |
| **Assignee** | mo...@google.com |
| **Created** | 2013-04-05 |
| **Bounty** | $31,336.00 |

## Description

# **VULNERABILITY DETAILS** \_\_\_\_ \_\_ \_ / \_\_ \_\_\_\_ ***/ /*** \_ \_\_\_\_\_\_ (*)* \_\_\_\_\_\_ \_\_\_ / /*/ / \_\_ / ***/ **/ \_\_ \ | /| / / \_\_ / / / / / \_\_ `** \ / ****/ /*/ (** ) /*/ /*/ / |/ |/ / / / / / /*/ / / / / / / /*/ \_***/****/\_*/ .***/|**/|\_\_/*/ /*/*/\_*,*/*/ /*/ /*/ /\_/

The following document gives an overview of the bugs that I was  

cobbling together for the Pwnium 3 competition to achieve remote code  

execution on the device.

While inspecting the browser plugins installed by default on my  

Chromebook, I noticed that the "Google Talk" plugin is running in an  

'unsandboxed' mode. Inspecting the entry more closely, one sees that  

not one MIME type, but two are registered, 'application/googletalk'  

and 'application/vnd.o3d.auto'. Since the Google Talk extension is  

closed source and O3D is an open source project, I decided to set my  

sights on O3D. Moreover, since O3D seems to be a dead-end technology,  

that looked like a safe bet to find bugs in.

By inspecting the Chromium source code and using gdb I reassured  

myself that the O3D plugin really was running in unsandboxed mode:

[function ComputeBuiltInPlugins(std::vector[content::PepperPluginInfo](javascript:void(0);)\* plugins)]  

-- snip -- [chrome/common/chrome\_content\_client.cc in Chromium r185835]  

static bool skip\_o3d\_file\_check = false;  

if (PathService::Get(chrome::FILE\_O3D\_PLUGIN, &path)) {  

if (skip\_o3d\_file\_check || file\_util::PathExists(path)) {  

content::PepperPluginInfo o3d;  

o3d.path = path;  

o3d.name = kO3DPluginName;  

o3d.is\_out\_of\_process = true;  

o3d.is\_sandboxed = false;  

o3d.permissions = kO3DPluginPermissions;  

webkit::WebPluginMimeType o3d\_mime\_type(kO3DPluginMimeType,  

kO3DPluginExtension,  

kO3DPluginDescription);  

o3d.mime\_types.push\_back(o3d\_mime\_type);  

plugins->push\_back(o3d);

```
  skip_o3d_file_check = true;  
}  

```

}  

-- snap --

# ================================================================================ Objective: Pop the Chromebook through the O3D plugin.

Let's see what steps are necessary to get from here to there\*.

\* where here is a URL I give you to visit on your Chromebook and there  

is a connect-back shell being spawned on your shiny toy.

(A) Getting a O3D plugin object instantiated. This was initially  

perceived as "an easy feat", but as all easy tasks, it turned out  

to be much harder than expected. "Why?", I hear you ask. The  

plugin is configured with a list of whitelisted domains:

```
-- snip -- [from build/branding.gypi]  
      'plugin_domain_whitelist': ('".corp.google.com", '  
                                  '".prod.google.com", '  
                                  '".googleplex.com", '  
                                  '"hostedtalkgadget.google.com", '  
                                  '"mail.google.com", '  
                                  '"plus.google.com", '  
                                  '"plus.sandbox.google.com", '  
                                  '"talk.google.com", '  
                                  '"talkgadget.google.com"')  
-- snap --  

Initially, my Chromebook was running ChromeOS 23.x, which didn't  
actually implement this whitelisting feature for reasons unknown.  

However, on ChromeOS 25.x, unless the HTML document embedding the  
o3d plugin is served over a HTTPS connection from one of these  
domains, the plugin will be blocked. This can be overcome with an  
XSS on one of the above Google properties, by being able to spoof  
window.location.href or by making use of Chromium Issue #64229  
(which has been marked as WontFix since January 2011):  
https://code.google.com/p/chromium/issues/detail?id=64229  

This can be seen in the function IsDomainAuthorized():  

-- snip -- [from plugin/cross/whitelist.cc]  
bool IsDomainAuthorized(NPP instance) {  
#ifdef O3D_PLUGIN_DOMAIN_WHITELIST  
  std::string url(GetURL(instance));  
  if (url.empty()) {  
    // This can happen in Chrome due to a bug with cross-origin security checks,  
    // including on legitimate pages. Until it's fixed we'll just allow any  
    // domain when this happens.  
    // http://code.google.com/p/chromium/issues/detail?id=64229  
    LOG(WARNING) <<  
        "Allowing use despite inability to determine the hosting page";  
    return true;  
  }  
-- snap --  

Since that bug has been rotting in the bugtracker for over two  
years and also was marked as \*WontFix\*, it was assumed to have  
gained the status of a "feature".  

Since I wasn't able to get the situation reproduced initially, I  
went trawling through the WebKit repository and thought that the  
problem was fixed by this or a related commit:  

--- snip --- [from http://trac.webkit.org/changeset/124693]  

2012-08-04  Adam Barth  <abarth@webkit.org>  

    [V8] Re-wire "target" half of the same-origin security check through Document rather than DOMWindow  
    https://bugs.webkit.org/show_bug.cgi?id=93079  

    Reviewed by Eric Seidel.  

    Before this patch, we were traversing from Nodes to Frames to  
    DOMWindows to SecurityOrigins when determing the "target" of an  
    operation for the same-origin policy security check. Rather than  
    detouring through DOMWindow, these security checks should operate in  
    terms of ScriptExecutionContexts (aka Documents) because that's the  
    canonical place we store SecurityOrigin objects.  

    A future patch will re-wire the "active" part of the security check to  
    use ScriptExecutionContexts as well and we'll be able to remove the  
    extra copy of SecurityOrigin that we keep in DOMWindow.  

--- snap ---  

More specifically, this change:  

--- snip ---  
static v8::Handle<v8::Context> activeContext()  
{  
    v8::Handle<v8::Context> context = v8::Context::GetCalling();  
    if (!context.IsEmpty())  
        return context;  
    // Unfortunately, when processing script from a plug-in, we might not  
    // have a calling context. In those cases, we fall back to the  
    // entered context.  
    return v8::Context::GetEntered();  
}  

[activeContext() now uses GetEntered() instead of GetCurrent() which  
 \*might\* mitigate the problem described in the above  
 discussion. BUT I WAS WRONG! IT DOES NOT MITIGATE THE  
 PROBLEM. SEE BELOW.]  

I then wasted endless hours trying to find an XSS in one of the above  
Google sites. Apparently I suck at these things; I heard that this  
is supposed to be rather easy...  

 
Revisiting the situation later -- using much hair-pulling and gdb  
-- I was able to discern a scenario that triggered the href  
property becoming 0 due to a failed cross-origin check.  
The following discussion was very helpful for that:  
https://groups.google.com/a/chromium.org/forum/?fromgroups=#!msg/chromium-dev/Nh40uy3tWG8/qkUblKmqt3sJ  
The trigger is racy, but with a forced reload on the outer frame it  
works reliably.  

By embedding an iframe such as the following  
-- snip -- [iframe_href0.html, included]  
<html>  
<body onload="document.defaultView.getComputedStyle(e).getPropertyValue('width');">  
<div id="e"></div>  
</body>  
</html>  
-- snap --  

Quick explanation: we can force a CSS style computation to happen  
in an inner iframe with the o3d plugin embedded on the outer  
frame. This in turn will trigger a layout of the page, which  
happens in the V8 context of the inner iframe. During this layout  
(actually, in the post layout stage) a plugin instantiation will  
be attempted for the o3d object on the outer frame. This in turn  
will lead to NPN_GetProperty calling V8 bindings (V8Location) for  
the window.location.href property. Since this is in the V8 context  
of the inner iframe, the access will fail due to a cross-origin  
violation. Don't ask me how to fix these bugs properly...  I have  
included a testcase testcase_plugin_href0.html for this.  

```

(B) Having an exploitable memory corruption in the O3D plugin. To any  

arrogant memory corruption practioner, the O3D code base looks  

sufficiently large to find at least a couple of decent use-after  

free or type confusion vulnerabilities in. And I only need one. The  

reference-counting patterns used throughout the code base together  

with the weak\_ptrs were extremely annoying (due to me hitting a  

number of false positives), but finally I found a simple way to  

UAF: Setting the owner property on a DrawElement object and  

subsequently destroying that owner object will cause a dangling  

pointer. To wit, the DrawElement class contains a bare Element  

pointer:

```
-- snip -- [from /core/cross/draw_element.h]  
Element\* owner_;  // our current owner.  
-- snap --  

Let's have a look at the available Javascript bindings of DrawElement:  

-- snip -- [from plugin/idl/draw_element.idl]  
[getter, setter, userglue_setter] Element? owner_;  

[verbatim=cpp_glue] %{  
  void userglue_setter_owner_(  
      o3d::DrawElement\* _this,  
      o3d::Element\* owner) {  
    _this->SetOwner(owner);  
  }  
-- snap --  

and more specifically at the setter function:  

-- snip -- [from /core/cross/draw_element.cc]  
void DrawElement::SetOwner(Element\* new_owner) {  
  // Hold a ref to ourselves so we make sure we don't get deleted while  
  // as we remove ourself from our current owner.  
  DrawElement::Ref temp(this);  

  if (owner_ != NULL) {  
    bool removed = owner_->RemoveDrawElement(this);  
    DCHECK(removed);  
  }  

  owner_ = new_owner;  

  if (new_owner) {  
    new_owner->AddDrawElement(this);  
  }  
}  
-- snap --  

The o3d::Element class follows the following inheritance:  
Element -> ParamObject -> NamedObject -> ObjectBase -> RefCounted  
  
More importantly, there is a virtual class inheriting from Element  
that we can instantiate through Javascript bindings, namely the  
Primitive class. This means the standard dangling pointer vtable  
overwrite, using the JS binding to pull the UAF trigger, is possible.  
\*pop goes the glock\*  

Please note that this find may look somewhat easier than it was -   
there are tons of other cases (see above) in which the object manager  
abstraction used is very successful at preventing UAF by making the   
objects unavailable through Javascript bindings.  

```

(C) A memory leak to defeat ASLR. While many a memory leak can be  

procured out of a UAF usually, I was not so lucky with the one  

that I had. But that just meant I need to find a dedicated  

one.... Contrary to more security-conscious operating systems such  

as OpenBSD [sorry, can't help the trolling here :)], free()d  

memory is not zero-filled on Linux. This means that being able to  

allocate memory that can be read through Javascript bindings and  

which is left uninitialized after the allocation can give us the  

juicy bits we want, especially if we can choose the allocation  

size as well! I found this behaviour in o3d::Buffer, in the  

processing of RawData objects into fields with input that  

intentionally is too short. In this case, the fields are not  

overwritten and can be used to peek into previously freed memory -  

just be careful to not get any floating point conversions into  

your way - this is what happened to me initially and made pointers  

only approximately correct ;) Look at the function  

Buffer::Set(o3d::RawData \*, size\_t, size\_t) in file  

core/cross/buffer.c as well as Buffer::AllocateElements(unsigned)  

and VertexBufferGLES2::ConcreteAllocate(size\_t) to see what I'm  

talking about [GLES2 and not GL is used on the Chromebook, also  

I've arbitrarily chosen VertexBuffer over IndexBuffer here].

```
This now allowed me to leak useful objects like the  
base::PendingTask object of Chrome which gives us the offset of  
the chrome binary to reliably predict addresses in memory. This  
also gives a great way to allocate memory and set its content for  
a use-after free, as long as the chunk is a multiple of 4 bytes  
in size.  

```

**VERSION**  

Chrome Version: 25.0.1364.173 stable  

Operating System: ChromeOS 25.0.1364.173, platform 3428.210.0, lumpy

**REPRODUCTION CASE**  

Full exploit is contained in pwnium.html and pwnium.js. Please adjust  

the destination of the connectback host in cbShellCmd in pwnium.js  

before running.

To run the exploit, please adjust the cbShellCmd in pwnium.js and  

the iframe reference to the iframe\_href0.html file in pwnium.html.

Make sure that the origin of the iframe\_href0.html is different from  

the origin you run pwnium.html from.

Use tmux with the following options to accept the connectback:  

tmux new-session -s pwniumcb -d 'openssl s\_server -nocert -cipher aNULL -accept 5000'; split-window -d 'openssl s\_server -nocert -cipher aNULL -accept 5001'; attach

The connectback may take a while, especially if the IP address of the  

connecting ChromeOS device cannot be reverse-resolved  

Please also note that this exploit does not contain any support for continuation  

of execution as this was not required by the Pwnium3 rules. Be careful to  

kill the plugin process before shutting down connections.

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

**Type of crash: [tab, browser, etc.]**  

**Crash State: [see link above: stack trace, registers, exception record]**  

**Client ID (if relevant): [see link above]**

## Attachments

- [pwnium.js](attachments/pwnium.js) (text/x-c++; charset=us-ascii, 10.3 KB)
- [pwnium.html](attachments/pwnium.html) (text/html; charset=us-ascii, 1.4 KB)
- [testcase_plugin_href0.html](attachments/testcase_plugin_href0.html) (text/html; charset=us-ascii, 416 B)
- [iframe_href0.html](attachments/iframe_href0.html) (text/html; charset=us-ascii, 126 B)

## Timeline

### js...@chromium.org (2013-04-05)

[Empty comment from Monorail migration]

### pi...@chromium.org (2013-04-05)

About the window.location.href confusion:
- we added a Pepper API for Flash to get the hosting document URL without going through JavaScript (PPB_UrlUtil_Dev.GetDocumentURL), we should use that in any talk/o3d/o1d/... plugin that we want to URL-whitelist.
- relevant bug with more data if we want to fix the underlying problem: https://code.google.com/p/chromium/issues/detail?id=74569

### ae...@chromium.org (2013-04-05)

I don't have a chromebook, but with slight modifications, the pwn() part works on my desktop. It hits system() with the specified command. I had to change the offset of system() and modify groom_dangling_pointer because of a different trampoline.

### jo...@chromium.org (2013-04-05)

[Empty comment from Monorail migration]

### jo...@chromium.org (2013-04-05)

Jüri: ToT Chrome in c#3?

### ae...@chromium.org (2013-04-05)

jorgelo: yes, ToT Chrome and I built the o3d plugin from chrome/trunk/o3d

### sc...@gmail.com (2013-04-05)

Nice. I actually went medieval on the O3D plug-in just before Pwnium and fixed about 9 integer / buffer overflows. You have defeated me with a UAF :P

### jo...@chromium.org (2013-04-05)

Working unmodified on R25, although we're about to update people to R26 ;-)

### js...@chromium.org (2013-04-05)

[Empty comment from Monorail migration]

### js...@chromium.org (2013-04-05)

[Empty comment from Monorail migration]

### js...@chromium.org (2013-04-05)

@haraken - Do you have a sense of what's going on here in the v8 bindings?

### jo...@chromium.org (2013-04-05)

Domain authorization issue tracked at https://crbug.com/chromium/227158.

### jo...@chromium.org (2013-04-05)

UAF in Talk tracked at https://crbug.com/chromium/227181.

### jo...@chromium.org (2013-04-05)

Infoleak tracked at https://crbug.com/chromium/227197.

### jl...@chromium.org (2013-04-09)

[Empty comment from Monorail migration]

### pa...@chromium.org (2013-04-09)

[Empty comment from Monorail migration]

### sc...@gmail.com (2013-04-10)

[Empty comment from Monorail migration]

### jo...@chromium.org (2013-04-10)

[Empty comment from Monorail migration]

### js...@chromium.org (2013-04-10)

Broken out into separate bugs for triage and tracking. This will be the placeholder bug for the reward.

### js...@chromium.org (2013-04-10)

[Empty comment from Monorail migration]

### js...@chromium.org (2013-04-11)

[Empty comment from Monorail migration]

### js...@chromium.org (2013-04-11)

Bulk edit for SecurityNotify.

### [Deleted User] (2013-04-11)

[Empty comment from Monorail migration]

### pa...@chromium.org (2013-04-12)

[Empty comment from Monorail migration]

### [Deleted User] (2013-04-15)

Tagging with reward! $31,336 :D

### pa...@chromium.org (2013-04-26)

[Empty comment from Monorail migration]

### pa...@chromium.org (2013-06-24)

[Empty comment from Monorail migration]

### js...@chromium.org (2013-11-18)

Bulk release of old security bug reports.


### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### is...@google.com (2016-10-02)

This issue was migrated from crbug.com/chromium/226937?no_tracker_redirect=1

[Monorail blocked-on: crbug.com/chromium/227158, crbug.com/chromium/227181, crbug.com/chromium/227197]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40077347)*
