# Security: Top-level redirect from cross-origin iframe by setting `Content-Security-Policy: sandbox allow-top-navigation`

| Field | Value |
|-------|-------|
| **Issue ID** | [40057349](https://issues.chromium.org/issues/40057349) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>PopupBlocker |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | da...@gmail.com |
| **Assignee** | lb...@chromium.org |
| **Created** | 2021-09-21 |
| **Bounty** | $5,000.00 |

## Description

**VULNERABILITY DETAILS**  

Top-level redirect possible from cross-origin iframe without user-interaction by setting this header `Content-Security-Policy: sandbox allow-top-navigation` in the response.  

This bypasses the patch for <https://crbug.com/1145553>

**VERSION**  

Chrome Version: 94.0.4606.54 (Official Build)  

Tested on the linux build

**REPRODUCTION CASE**  

app.py

```
#!/usr/bin/env python3  
from flask import Flask, Response  
  
app = Flask(__name__)  
  
@app.route("/test")  
def test():  
    resp = Response("""  
    <script>  
        top.location = "https://google.com";  
    </script>  
    """, mimetype="text/html")  
    resp.headers["Content-Security-Policy"] = "sandbox allow-top-navigation allow-scripts"  
    return resp  
  
app.run(host="0.0.0.0", debug=True)  

```

once the flask app is started any page that embeds <http://localhost:5000/test> should be redirected to <https://google.com>

**CREDIT INFORMATION**  

Reporter credit: David Sievers

## Timeline

### [Deleted User] (2021-09-21)

[Empty comment from Monorail migration]

### aj...@google.com (2021-09-21)

Tentatively adding flags and assigning following https://crbug.com/chromium/1145553. I have not repro'd this but could you take a look jkarlin?

[Monorail components: UI>Browser>PopupBlocker]

### [Deleted User] (2021-09-21)

[Empty comment from Monorail migration]

### da...@gmail.com (2021-09-22)

Hi again and sorry for not adding a title. I seem to have forgotten about it out of excitement :D
I created a glitch.me page for this https://foggy-malleable-land.glitch.me/demo
Hope it makes it more convenient to reproduce this

### [Deleted User] (2021-09-22)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-09-22)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-09-22)

[Empty comment from Monorail migration]

### aj...@google.com (2021-09-23)

[Empty comment from Monorail migration]

### aj...@google.com (2021-09-23)

possibly a duplicate of https://crbug.com/chromium/1138794 ?

### jk...@chromium.org (2021-09-23)

+cc Nate: Looking at https://github.com/WICG/interventions/issues/16#issue-150437109 it looks like the intention was to prevent allow-top-navigation in a sandboxed frame from navigating the top frame. But there were changes after that point, so I'm not sure if things are currently WAI or not. 

### da...@gmail.com (2021-09-23)

I'm not sure if the issue is understood correctly. I probably should've explained a bit more:
The issue is basically the same as https://crbug.com/chromium/1145553 in that it is a bypass to the popup-blocker that prevents cross-origin iframes (such as ads) from initiating top-level-navigation without user-interaction. In https://crbug.com/chromium/1145553 this was bypassed by embedding another frame inside the cross-origin frame with the `allow-top-navigation` sandbox attribute set.
The glitch.me app I linked to in https://crbug.com/chromium/1251790#c4 showcases the intended behavior when clicking on `iframe site showing intended behavior`: the top-level-navigation is blocked and an error is shown in the console. Whereas clicking `iframe site showing bypass` shows that when the cross-origin site is server with the `Content-Security-Policy: sandbox allow-top-navigation` header the navigation will go through and thus the pop-up-blocker is bypassed.


### da...@gmail.com (2021-09-23)

This works because the fix to https://crbug.com/chromium/1145553 checks that when a sandboxed frame with allow-top-navigation set tries to initiate top-level-navigation then the parent frame of this frame has to be allowed to do so aswell which is the case here since the parent frame is the top-level frame.

### [Deleted User] (2021-10-07)

jkarlin: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ja...@chromium.org (2021-10-11)

Sorry for the delay.

When we introduced the intervention in https://github.com/WICG/interventions/issues/16#issue-150437109, allow-top-navigation effectively disabled the intervention. I think the initial reason was the code structure of the helper made this the path of least resistance, but it also seemed to make sense as a way to allow a top frame to effectively opt out of this protection.

IIRC, that was before iframes could self-apply sandbox headers by CSP. That breaks the assumption that it's safe to allow a user-gesture-less top navigation in a cross-origin iframe with allow-top-navigation.

I don't know if there's a way to treat parent-imposed sandbox differently than self-imposed CSP sandbox. Failing that, we should look into closing the allow-top-navigation loophole, though that might break some existing content?

### jk...@chromium.org (2021-10-12)

[Comment Deleted]

### jk...@chromium.org (2021-10-12)

This is tough. As the intervention stands right now, a frame can apply allow-top-navigation, but that will be ignored if the embedding frame itself doesn't have the capability of navigating the top-frame.

In the OP's case, the embedding frame is the top frame, and therefore always has the capability to navigate the top frame. And we'd trust the embedding frame to set allow-top-navigation appropriately (even if created by some third-party script executing on the embedder's site). Should we likewise trust that a subframe loaded by the top frame should be trusted? I would argue no, because the embedder would then lose the ability to restrict iframes from navigating the top frame. 

Curious for thoughts from Mike on this.

### mk...@chromium.org (2021-10-13)

Hrm. Yes, framing this intervention as a sandbox flag might have been a mistake. :) It feels more like a capability we ought to be explicitly delegating rather than a relaxation of rules which would otherwise apply.

Since it's probably unlikely that we can turn back time to move this to an `allow` attribute, the simplest thing to do would be to exclude this flag from the set of flags which can be declared in the `sandbox` directive. That should be pretty straightforward.

### [Deleted User] (2021-10-26)

jkarlin: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### da...@gmail.com (2021-11-15)

Is there any update on this?

### [Deleted User] (2021-11-15)

[Empty comment from Monorail migration]

### jk...@chromium.org (2021-11-16)

[Empty comment from Monorail migration]

### [Deleted User] (2022-02-02)

[Empty comment from Monorail migration]

### da...@gmail.com (2022-02-15)

Is there any update on this?

### ja...@chromium.org (2022-03-10)

[Empty comment from Monorail migration]

### [Deleted User] (2022-03-30)

[Empty comment from Monorail migration]

### [Deleted User] (2022-05-25)

[Empty comment from Monorail migration]

### [Deleted User] (2022-08-03)

[Empty comment from Monorail migration]

### da...@gmail.com (2022-08-17)

Hi again, is there any update?

### jk...@chromium.org (2022-08-17)

Ah, sorry, slipped off my radar! Shivani, can you find someone on your team to take this? Using this loophole, ads are able to circumvent the browser's top-frame navigation protections without user gesture.

### sh...@chromium.org (2022-08-17)

Sure.
Liam: PTAL, thanks!


### lb...@chromium.org (2022-08-17)

[Empty comment from Monorail migration]

### lb...@chromium.org (2022-08-17)

[Empty comment from Monorail migration]

### do...@chromium.org (2022-08-18)

I've been asked to comment on the spec situation here. Let me first check if my understanding is correct:

- There are sandbox flags for allow-top-navigation and allow-top-navigation-by-user-activation. So a sandboxed iframe can, by default, not do these things.

- Per spec, the ways an iframe can become sandboxed are via the sandbox="" attribute on the <iframe> element, or via adding CSP sandbox headers.

- So per spec, none of this applies to normal iframes. (Regardless of their origin.) Only sandboxing turns on these restrictions. See also https://html.spec.whatwg.org/#allowed-to-navigate or the upcoming rewrite of it at https://whatpr.org/html/6315/browsing-the-web.html#allowed-to-navigate .

- However, Chromium has an unspecified behavior that disallows some navigations of parent cross-origin iframes, based on user activation or not, even when the iframe is not sandboxed??

- And, this unspecified behavior interacts somehow with sandboxing, if sandboxing *is* present??

- And this interaction is undesirable from our perspective???

If this understanding is correct, then from a spec perspective, you're in totally uncharted territory here, since this is all unspecced behavior. So you should really come up with what behavior you want to design, and then spec it, and write web platform tests, and get interop across browsers.

https://github.com/whatwg/html/issues/8013 is the spec issue we opened for this last time it came up. Any engagement there, and in particular any work from the team responsible for this in properly specifying it, would be appreciated.

### jk...@chromium.org (2022-08-18)

Your understanding is correct. This was launched w/ the common intervention approach at the time. That is, ship it with an intervention monkey patch, tweak the intervention as needed, and eventually spec it once it seems like the approach works. Some discussion of this here: https://groups.google.com/a/chromium.org/g/blink-dev/c/Xi8-y4ySjA4/m/yt8Lilx_AwAJ.

My take here is that this is an intervention that we shipped and do want to continue supporting, so we should work on getting cross-browser support for it and specify it. The team that created the intervention is no longer working on such things. So we'll need to find an owner.

In the meanwhile, this bug needs to be addressed as it's a security issue. It requires a change to CSP sandbox behavior. What's the right approach Mike? Go ahead and make the change along with a monkey patch to the CSP spec and follow the intent-to-deprecate process? 


### lb...@chromium.org (2022-08-22)

[Empty comment from Monorail migration]

### lb...@chromium.org (2022-08-23)

I have a CL up for review: https://chromium-review.googlesource.com/c/chromium/src/+/3842458

This will end up needing some spec work, so I want to make sure everyone here is on board before I start to reach out externally.

The TL;DR is that if a cross-origin iframe is unsandboxed (sandbox="" attribute is not set and the iframe doesn't inherit sandbox flags from its ancestor), but the response headers in the page it's navigating to tries set `allow-top-navigation` in its sandbox flags, it will "downgrade" that flag to `allow-top-navigation-by-user-activation`.

Here are some more cases in detail:

Same-origin iframe: no change to behavior

Cross-origin iframe with sandbox="" attribute set: no change to behavior

Cross-origin iframe with sandbox="" and sandbox flag set in response header: no change to behavior. The sandbox="" will be enough to stop any permissions escalation attempt from the response header.

Cross-origin iframe with NO sandbox="" but sandbox flag set in response header: This is the case where the response header could attempt to escalate privileges. If the response header has the `allow-top-navigation` flag set, convert it to `allow-top-navigation-by-user-activation` before loading normally. This will also output a console warning saying there was an intervention.

What are everyone's thoughts on this?

### do...@chromium.org (2022-08-24)

Maybe you could outline the eventual model starting from scratch, not starting from the current behavior? That would be more like what we end up proposing to standardize.

### lb...@chromium.org (2022-08-24)

[Empty comment from Monorail migration]

### lb...@chromium.org (2022-08-24)

Here's an updated proposal that is based on the current spec behavior instead of the current Chromium behavior:

Determining if top-level navigation is allowed in a frame:

- Disallow top-level navigation if the frame is not the root frame in its frame tree and its nearest ancestor does not allow top-level navigation (determined by a recursive call to this algorithm).

- Allow top-level navigation if the `allow-top-navigation-by-user-activation` sandbox flag is enabled for the frame and the frame has sticky user activation.

- Allow top-level navigation if the `allow-top-navigation` sandbox flag is enabled for the frame and any of the following are true:
- - The frame is same-origin to its parent.
- - The frame has sandbox flags that were inherited from its parent
- - The frame has sandbox flags that were set in its sandbox="" attribute.
- - The frame has sticky user activation.

- Disallow top-level navigation under all other circumstances.


In terms of what will change to the current spec behavior:
- `allow-top-navigation` and `allow-top-navigation-by-user-activation`'s user activation requirements will change from requiring transient user activation to requiring sticky user activation. This will align with how Chromium and Safari currently behave.
- A frame can no longer navigate its top-level browsing context if its sandbox flags are unset, regardless of user activation. (Note: Safari and Chromium currently stop unsandboxed frames from navigating if they don't have sticky user activation)
- A frame can no longer navigate its top-level browsing context if any ancestor frames disallow top-level navigation.
- A frame can no longer navigate its top-level context without user activation if the frame is cross-origin to its parent, does not inherit sandbox flags, and does not have flags set in their sandbox="" attribute.

Let me know what your thoughts are on this.

### do...@chromium.org (2022-08-24)

> and its nearest ancestor

Its nearest ancestor is just its parent. Do we need recursion?



> - A frame can no longer navigate its top-level browsing context if its sandbox flags are unset

This reads as if "no unsandboxed frame (aka sandbox flags are unset) can navigate the top frame". This quite seem right though. Do you mean if its sandbox flags are unset *and it is cross-origin to the main frame* it cannot navigate the top frame? Because same-origin frames, as per the first section of your comment, should remain unaffected by this right? And cross-origin frames that aren't sandboxed can still navigate the top, but only if they have user activation right?




> - A frame can no longer navigate its top-level browsing context if any ancestor frames disallow top-level navigation.

Imagine:
      Top-level (A.com)
          \
       Cross-origin sandbox="allow-same-origin" frame (no `allow-top-navigation`) (B.com)
            \
        Grandchild sandboxed frame (by flag inheritance) (A.com)

The grandchild is same-origin with the top, but its ancestor is not allowed to navigate the top. Today, is the grandchild allowed to navigate the top? With your proposal, are we changing this? Your summary reads as if the grandchild is not allowed to navigate the top (because its ancestor cannot), even though the grandchild is same-origin, so I just want to be clear.




> - A frame can no longer navigate its top-level context without user activation if the frame is cross-origin to its parent, does not inherit sandbox flags, and does not have flags set in their sandbox="" attribute.

With this point, are you just saying that not-sandboxed, cross-origin frames cannot navigate the top frame without user activation?

### do...@chromium.org (2022-08-25)

Thanks for this summary; this is exactly what I was looking for.

+1 to https://crbug.com/chromium/1251790#c40's questions about whether you want to consider the entire ancestor tree, or just the top-vs.-initiator relationship.

Also, when writing up formal spec text, you'll need to be sure to handle the case of the top-level frame itself. As stated I'm not clear whether a top-level frame is allowed to navigate itself, if it uses CSP sandbox headers but doesn't set allow-top-navigation(-by-user-activation). But that's just a detail.

> - `allow-top-navigation` and `allow-top-navigation-by-user-activation`'s user activation requirements will change from requiring transient user activation to requiring sticky user activation. This will align with how Chromium and Safari currently behave.

This is a big change! Are you sure this is how Chrome and Safari behave?? We spent a lot of effort speccing this to require transient activation; sticky activation is a much weaker condition. So if someone clicks inside an iframe, then 10 minutes later, the iframe can top-navigate??

> - Allow top-level navigation if the `allow-top-navigation` sandbox flag is enabled for the frame and any of the following are true:
> - - The frame is same-origin to its parent.
> - - The frame has sandbox flags that were inherited from its parent
> - - The frame has sandbox flags that were set in its sandbox="" attribute.
> - - The frame has sticky user activation.

The way I would phrase this is not to condition on sandbox="" or not; ideally the spec doesn't need to track the provenance of sandboxing flags. Instead, say that CSP: sandbox just is unable to set the allow-top-navigation flag, by having https://w3c.github.io/webappsec-csp/#sandbox-init modify the sandboxing flag set appropriately.

It would also be ideal not to condition on "inherited from its parent", as I believe that's also unprecedented and would also require tracking the provenance of sandboxing flags in a way that would be annoying to spec. (And to implement?) But I don't have a clear suggestion on how to do that.

### lb...@chromium.org (2022-08-26)

Dominic's questions:
> Its nearest ancestor is just its parent. Do we need recursion?
  - This might be getting too deep into implementation details. It's determined in Chromium with a recursive call. I'll take that bit out.

> This reads as if "no unsandboxed frame (aka sandbox flags are unset) can navigate the top frame". This quite seem right though. Do you mean if its sandbox flags are unset *and it is cross-origin to the main frame* it cannot navigate the top frame? Because same-origin frames, as per the first section of your comment, should remain unaffected by this right? And cross-origin frames that aren't sandboxed can still navigate the top, but only if they have user activation right?
  - I think I got confused by the implementation details and what intervention we wanted. Yes, that's correct. I'll update the proposal to include that.

> The grandchild is same-origin with the top, but its ancestor is not allowed to navigate the top. Today, is the grandchild allowed to navigate the top? With your proposal, are we changing this? Your summary reads as if the grandchild is not allowed to navigate the top (because its ancestor cannot), even though the grandchild is same-origin, so I just want to be clear.
  - Right now, the grandchild is not allowed to navigate top because it says that the allow-top-navigation flag is not set. https://grass-mahogany-calculator.glitch.me/demo - There's also this intervention here that doesn't look at origins (https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/frame/local_frame.cc;l=1797-1818;drc=1c9444615ffd1a3606706c3ed607364cb9f6918f), but I'm not sure if it's actually being triggered in my test case.

> With this point, are you just saying that not-sandboxed, cross-origin frames cannot navigate the top frame without user activation?
  - This should specify that the frame is sandboxed. I'll fix it.

Domenic's questions:

> Also, when writing up formal spec text, you'll need to be sure to handle the case of the top-level frame itself. As stated I'm not clear whether a top-level frame is allowed to navigate itself, if it uses CSP sandbox headers but doesn't set allow-top-navigation(-by-user-activation). But that's just a detail.
  - I'll add a case in the proposal just so I don't forget.

> This is a big change! Are you sure this is how Chrome and Safari behave?? We spent a lot of effort speccing this to require transient activation; sticky activation is a much weaker condition. So if someone clicks inside an iframe, then 10 minutes later, the iframe can top-navigate??
  - I think I got confused from my testing. Unsandboxed frames require sticky activation, sandboxed frames require transient activation. I'll fix that.

> It would also be ideal not to condition on "inherited from its parent", as I believe that's also unprecedented and would also require tracking the provenance of sandboxing flags in a way that would be annoying to spec. (And to implement?) But I don't have a clear suggestion on how to do that.
  - If we just naively remove `allow-top-navigation` from a CSP header, then if an iframe with sandbox="allow-top-navigation" embeds a page `allow-top-navigation` in its header, the conversion will prevent any top-level navigation from happening. In our code, we have a function for calculating sandbox flags that knows the difference between a flag set from CSP and a flag from somewhere else. I'm not sure if there's something in the spec that can make that distinction, but I think that's ultimately what we are going to need.

---

Version 2 of the proposal:

Downgrading the `allow-top-navigation` sandbox flag:

- If a frame's CSP header tries to set the `allow-top-navigation` flag, and the frame is otherwise unsandboxed, the flag will be changed to `allow-top-navigation-by-user-activation`.

Determining if top-level navigation is allowed in a frame:

- A top-level frame is always allowed to navigate itself.

- Disallow top-level navigation if the frame is not the root frame in its frame tree and its nearest ancestor does not allow top-level navigation.

- Allow top-level navigation if the `allow-top-navigation-by-user-activation` sandbox flag is enabled for the frame and the frame has transient user activation.

- Allow top-level navigation if the `allow-top-navigation` sandbox flag is enabled for the frame.

- Allow top-level navigation if the frame is unsandboxed and has sticky user activation or is same-origin to the top-level origin.

- Disallow top-level navigation under all other circumstances.


In terms of what will change to the current spec behavior:
- An unsandboxed frame will only be able to navigate its top-level browsing context if it has sticky user activation.
- A frame can no longer navigate its top-level browsing context if any ancestor frames disallow top-level navigation.
- CSP headers in a page being loaded in a frame can no longer set the `allow-top-navigation` sandbox flag. It will be downgraded to `allow-top-navigation-by-user-activation`. This does not change the behavior of `allow-top-navigation` being set anywhere else.

---

Also let me know if I forgot to answer any questions.

### do...@chromium.org (2022-08-26)

> - An unsandboxed frame will only be able to navigate its top-level browsing context if it has sticky user activation.

... this restriction should only apply to cross-origin iframes right? What about:

   A.com
     \
    B.com
       \
      A.com

No sandbox, no user activation. Can A.com-grandchild navigate A.com-parent? I think your proposal says no, due to the following clauses:

"- Disallow top-level navigation if the frame is not the root frame in its frame tree and its nearest ancestor does not allow "top-level navigation.
    - A.com-grandchild's "nearest ancestor" isn't allowed to navigate the top, due to it not having user activation
"- An unsandboxed frame will only be able to navigate its top-level browsing context if it has sticky user activation."
    - As currently written, this reads as if it applies to *all* frames. But I think it should only apply to cross-origin

### lb...@chromium.org (2022-08-30)

> "- Disallow top-level navigation if the frame is not the root frame in its frame tree and its nearest ancestor does not allow "top-level navigation.
>     - A.com-grandchild's "nearest ancestor" isn't allowed to navigate the top, due to it not having user activation

The current Chrome behavior is to disallow a top-level navigation if the immediate ancestor cannot navigate. If you go to https://grass-mahogany-calculator.glitch.me/demo (I've since updated the demo to trigger the correct error) and click the button, you'll get the console error:
`Unsafe attempt to initiate navigation for frame with URL 'https://grass-mahogany-calculator.glitch.me/demo' from frame with URL 'https://grass-mahogany-calculator.glitch.me/redirect'. The frame attempting navigation of the top-level window is sandboxed and is not allowed to navigate since its ancestor frame with origin 'https://brindle-early-road.glitch.me' is unable to navigate the top frame.`

Our 2 options here are to add an exception for a same-origin frame embedded in a cross-origin frame (which will require code changes), or to keep the spec as is. Let me know what you think. I can see the argument for same-origin being able to do whatever it wants with itself, but also that if a frame wants to disallow top-level navigation, no child should be able to override that.

> "- An unsandboxed frame will only be able to navigate its top-level browsing context if it has sticky user activation."
>     - As currently written, this reads as if it applies to *all* frames. But I think it should only apply to cross-origin

Good catch. I'll update that.

---

Version 3 of the proposal:

Downgrading the `allow-top-navigation` sandbox flag:

- If a frame's CSP header tries to set the `allow-top-navigation` flag, and the frame is otherwise unsandboxed, the flag will be changed to `allow-top-navigation-by-user-activation`.

Determining if top-level navigation is allowed in a frame:

- A top-level frame is always allowed to navigate itself.

- Disallow top-level navigation if the frame is not the root frame in its frame tree and its nearest ancestor does not allow top-level navigation.

- Allow top-level navigation if the `allow-top-navigation-by-user-activation` sandbox flag is enabled for the frame and the frame has transient user activation.

- Allow top-level navigation if the `allow-top-navigation` sandbox flag is enabled for the frame.

- Allow top-level navigation if the frame is unsandboxed and has sticky user activation or is same-origin to the top-level origin.

- Disallow top-level navigation under all other circumstances.


In terms of what will change to the current spec behavior:
- An unsandboxed cross-origin frame will only be able to navigate its top-level browsing context if it has sticky user activation.
- A frame can no longer navigate its top-level browsing context if any ancestor frames disallow top-level navigation.
- CSP headers in a page being loaded in a frame can no longer set the `allow-top-navigation` sandbox flag. It will be downgraded to `allow-top-navigation-by-user-activation`. This does not change the behavior of `allow-top-navigation` being set anywhere else.

### do...@chromium.org (2022-08-30)

I think everything LGTM.




> The current Chrome behavior is to disallow a top-level navigation if the immediate ancestor cannot navigate.

I'm definitely surprised we do this, since same-origin children can just get around this via window.top.eval('location.href = ...'), but as long as it is consistent across browsers, then it SGTM since this is not the right place to litigate it. Thanks for investigating.

### do...@chromium.org (2022-09-07)

This proposal looks good to me, although I agree with https://crbug.com/chromium/1251790#c45 that it's weird to check the entire ancestor chain. Please check other browsers to see what they do in such situations; if Chrome is the odd one out, then we should probably avoid that restriction.

Can I ask a big favor, and request that any spec PR here be done against the session-history branch in https://github.com/whatwg/html/pull/6315 ? Some of the sandboxing stuff has been improved, especially the CSP integration, so I hope it will be easier.

### lb...@chromium.org (2022-09-07)

https://github.com/WebKit/WebKit/commit/5716db24987a7ba1883bfb5ce9056b26f5e113a8#diff-65dcc9537c07531c3645f6181cfc912d1eb34c94b1ab52d21bd0c848c6e4ee49

It looks like WebKit handled their equivalent of https://crbug.com/1145553 differently than how we handled it (I think it's https://bugs.webkit.org/show_bug.cgi?id=219408 but I can't confirm because I don't have read access). Their intervention disallows navigation if the frame has never had user activation and its immediate ancestor is cross-origin to the top-level frame being navigated. This has the side effect where, if a cross-origin iframe with sandbox="allow-top-navigation" embeds an iframe with sandbox="allow-top-navigation", that second iframe will not be allowed to navigate top.

I think in this case navigation should be allowed. And I think the only way to do that is to check up the ancestor chain and make sure that all ancestors are allowed to navigate. I chatted with jkarlin@ earlier today, and he wanted to make sure that it was clear that our current intervention requires us recursively checking up the chain to see if there is any ancestor that is not allowed to navigate top. So I'll need to update that in the proposal and spec.

Any browser that's based on Chromium has this behavior.

Firefox does not currently have any of these interventions in place.

In terms of browser engines, we are the odd one out. However, I think this behavior is what other browsers need to do to protect against the top level navigation exploit without being overly locked down.

---

Version 4 of the proposal:

Downgrading the `allow-top-navigation` sandbox flag:

- If a frame's CSP header tries to set the `allow-top-navigation` flag, and the frame is otherwise unsandboxed, the flag will be changed to `allow-top-navigation-by-user-activation`.

Determining if top-level navigation is allowed in a frame:

- A top-level frame is always allowed to navigate itself.

- Disallow top-level navigation if the frame is not the root frame in its frame tree and any of its ancestors do not allow top-level navigation.

- Allow top-level navigation if the `allow-top-navigation-by-user-activation` sandbox flag is enabled for the frame and the frame has transient user activation.

- Allow top-level navigation if the `allow-top-navigation` sandbox flag is enabled for the frame.

- Allow top-level navigation if the frame is unsandboxed and has sticky user activation or is same-origin to the top-level origin.

- Disallow top-level navigation under all other circumstances.


In terms of what will change to the current spec behavior:
- An unsandboxed cross-origin frame will only be able to navigate its top-level browsing context if it has sticky user activation.
- A frame can no longer navigate its top-level browsing context if any ancestor frames disallow top-level navigation.
- CSP headers in a page being loaded in a frame can no longer set the `allow-top-navigation` sandbox flag. It will be downgraded to `allow-top-navigation-by-user-activation`. This does not change the behavior of `allow-top-navigation` being set anywhere else.

### do...@chromium.org (2022-09-08)

I'm not sure our concern came across. We're wondering about the case of:

- Outermost: https://a.com
- Mid: https://b.com, sandboxed (no top-navigation allowed)
- Innermost: https://a.com, no sandbox

We believe that even without user activation, innermost should be able to perform top navigation using `window.top.location.href = "..."`, since nothing in your proposal prevents `window.top.eval('location.href = "..."')`.

Concretely, we're suggesting that

> Disallow top-level navigation if the frame is not the root frame in its frame tree and any of its ancestors do not allow top-level navigation.

be changed to something like

> Disallow top-level navigation if the frame is not the root frame in its frame tree, and there is no same-origin ancestor frame which is allowed top-level navigation.

We were further saying, this change request isn't a hard requirement. We just think it's weird to restrict this sort of case, since it's so easy to work around.

### ar...@google.com (2022-09-08)

[Comment Deleted]

### ar...@google.com (2022-09-08)

What I understood:

[A] Initially, we blocked cross-origin iframe from navigating top without
user-gesture. The goal was to block all those annoying ads! Good!

However it means sandboxed iframe without "allow-same-origin" are considered
cross-origin. They can't navigate without a user gesture anymore. So folks added
an exception [B]: allow partially sandboxed iframe that aren't disallowed to
navigate top to bypass [A]. This is very weird, because sandbox is expected to
add restriction, not to add new capabilities!

Then malicious ads figured out they can create additional child frame
below with sandbox=allow-top-navigation to bypass [A] thanks to [B].

Then, we create [C] to fill the hole created by [B]. The patch is not easy to
understand:
https://chromium-review.googlesource.com/c/chromium/src/+/2688360
To be allowed to navigate top from a sandboxed iframe, we check all ancestors are
allowed to navigate top. That is to say, require one of:
1. be same-origin with the parent, or
2. have a user gesture, or
3. be partially sandboxed without disallowing top navigation.

Then we realized sandbox can not only be applied by the parent using
iframe.sandbox, but it can also be self applied by the child using
CSP.sandbox. It means [C] can be bypassed using (3) via CSP.

Then, the proposed patch:
https://chromium-review.googlesource.com/c/chromium/src/+/3842458
tries to detect when [C] might be bypassed and downgrade the CSP of a
cross-origin document.

This sounds like a bad outcome. It would be best if we could rollback everything
up to [B] and restart from a good foundation.
Do you know how many partially sandboxed document that aren't disallowed by sandbox
to navigate top are navigating top without a user gesture? If the numbers are
low enough, it might still be possible to get back toward a nice model?

If we can't rollback up to [B], it would be best to define a bit telling if a
document can navigate top without user gesture. It would be immutable and
associated with every documents (stored in PolicyContainer). The child's
bit would be stricter or equal to its parent. This way, you don't need to
traverse the whole chain of ancestors or downgrade the CSP of anyone.

### do...@chromium.org (2022-09-08)

RE https://crbug.com/chromium/1251790#c48:


> I'm not sure our concern came across. We're wondering about the case of:
and
> Concretely, we're suggesting that

domenic@'s explanation of the concern is spot on. Its just like permissions policy: any iframe that's same-origin with the top frame can any permission it'd like regardless of how many restricted cross-origin iframes sit in between, because it can always just synchronously run permission-requesting script in the top frame anyways.

However IMO, if all browsers agree that in domenic@'s example the innermost frame *would not* be able to navigate the top frame, I think I'm OK moving forward with that just to simplify this proposal, leaving that as a follow-up task to tackle separately. I'm not sure if all browsers agree on that though.

### lb...@chromium.org (2022-09-08)

> I'm not sure if all browsers agree on that though.

[1]
- Outermost: https://a.com
- Mid: https://b.com, sandboxed (no top-navigation allowed)
- Innermost: https://a.com, no sandbox

- Chrome does not allow top-level navigation because `innermost` inherits sandbox flags from `mid`, which does not have `allow-top-navigation` set.
- Safari and Firefox do not allow top-level navigation for the same reason.
I think what's happening in this case is that the sandbox flag inheritance is taking priority over the same-origin frame being able to do what it wants.

However, I think with the case I mentioned:
> The current Chrome behavior is to disallow a top-level navigation if the immediate ancestor [note: this should've said `if anyone in the ancestor chain`] cannot navigate.
this is the setup we want to trigger the restriction we introduced:
[2]
- Outermost: https://a.com
- Mid: https://b.com, no sandbox
- Innermost: https://a.com, sandboxed (top-navigation allowed)

With this setup, Chrome disallows top-navigation because of the ancestor restriction we introduced.
Safari disallows top-navigation because Innermost's parent is cross-origin and has no user activation.
Firefox allows top-level navigation because they don't have any framebusting systems in place.

So with case [1], since every browser currently agrees that Innermost can't navigate, I think we should keep it that way.
With case [2], having an exception carved out for same-origin top navigations seems reasonable.

Though if we take the approach Arthur suggested and roll back the sandbox flags altogether, none of this will really matter :) (I'll need more time to think about the implications of that)

---

Version 5 of the proposal:

Downgrading the `allow-top-navigation` sandbox flag:

- If a frame's CSP header tries to set the `allow-top-navigation` flag, and the frame is otherwise unsandboxed, the flag will be changed to `allow-top-navigation-by-user-activation`.

Determining if top-level navigation is allowed in a frame:

- A top-level frame is always allowed to navigate itself.

- Disallow top-level navigation if the frame is not the root frame in its frame tree, the frame is cross-origin to the root frame, and any of the frame's ancestors do not allow top-level navigation.

- Allow top-level navigation if the `allow-top-navigation-by-user-activation` sandbox flag is enabled for the frame and the frame has transient user activation.

- Allow top-level navigation if the `allow-top-navigation` sandbox flag is enabled for the frame.

- Allow top-level navigation if the frame is unsandboxed and has sticky user activation or is same-origin to the top-level origin.

- Disallow top-level navigation under all other circumstances.


In terms of what will change to the current spec behavior:
- An unsandboxed cross-origin frame will only be able to navigate its top-level browsing context if it has sticky user activation.
- A frame can no longer navigate its top-level browsing context if any ancestor frames disallow top-level navigation.
- CSP headers in a page being loaded in a frame can no longer set the `allow-top-navigation` sandbox flag. It will be downgraded to `allow-top-navigation-by-user-activation`. This does not change the behavior of `allow-top-navigation` being set anywhere else.


### lb...@chromium.org (2022-09-09)

Just an update: since there are a few people that seem to be in favor of the final spec doing away with the sandbox flags altogether, and since going that route with the spec will be a much longer process, my current plan is to check in the fix first without updating any spec, and then dealing with the spec changes afterwards.

The CL is up here: https://chromium-review.googlesource.com/c/chromium/src/+/3842458 and I plan on refactoring it to use the "can navigate top bit" that Arthur suggested.

### [Deleted User] (2022-10-10)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2022-10-11)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/e6de25ee4229a5154a458c97fb6d0da7d8845b0f

commit e6de25ee4229a5154a458c97fb6d0da7d8845b0f
Author: Liam Brady <lbrady@google.com>
Date: Tue Oct 11 17:02:30 2022

Stop frames from allowing themselves to navigate top without gesture

A previous CL stopped a sandboxed iframe from navigating the top document if its ancestor was not allowed to navigate top[1]. However, there is still a corner case that allows a sandboxed frame to give itself permission to navigate top if the top-level page doesn't have any sandbox flags set.

For this attack, a cross origin iframe is embedded in a page. At
creation time, both the main page and the iframe are unsandboxed, which
means that the iframe requires sticky user activation to be able to
navigate the top frame. Then, this iframe loads a page whose response
header's CSP includes `sandbox allow-top-navigation`. The cross-origin
page just gave itself permission to navigate the top-level frame
without sticky user activation.

This is problematic because it allows a cross-origin iframe to
circumvent our framebust intervention and navigate the top page to a
potentially malicious page. Before this CL, there is no way for the renderer to detect this. It can't distinguish between sandbox flags set on the frame itself by the embedding page and sandbox flags delivered in the response headers. There are 2 checks in LocalFrame::CanNavigate that are looking at the 2 top navigation sandbox flags, but by that point the frame sandbox flags and delivered sandbox flags have been squashed into one place, so there's no way to know if the `allow-top-navigation` flag came from the frame or the response header.

This CL's original approach involved downgrading the allow-top-navigation sandbox flag to allow-top-navigation-by-user-activation specifically when the browser process detected that the document's response headers were attempting to give it that extra ability when the embedder-supplied sandbox flags did not. We ultimately decided against it so that we wouldn't be setting a new precedent of dynamically re-interpreting sandbox flags.

The fix we decided on:
Add a bit to the PolicyContainerPolicies struct to track if a document
can navigate the top-level frame without sticky user activation. If any
of the following conditions hold:
- The document is cross-origin to the root document, and the document's parent document is not allowed to navigate top without
sticky user activation
- The document is cross-origin to the root document, and the frame
hosting the document is either unsandboxed or sandboxed without the
allow-top-navigation flag
The bit will be set to false and the document will require sticky user
activation to navigate top.

This will end up having the same behavior as the downgrading approach,
without needing to have the browser change sandbox flags.

[1] https://chromium-review.googlesource.com/c/chromium/src/+/2688360

Bug: 1251790
Change-Id: I7406d631d6b9c4bdbfc71c433db50b2fca2f0c21
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3842458
Reviewed-by: Arthur Sonzogni <arthursonzogni@chromium.org>
Reviewed-by: Dominic Farolino <dom@chromium.org>
Commit-Queue: Liam Brady <lbrady@google.com>
Reviewed-by: Mike West <mkwst@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1057526}

[add] https://crrev.com/e6de25ee4229a5154a458c97fb6d0da7d8845b0f/third_party/blink/web_tests/external/wpt/html/semantics/embedded-content/the-iframe-element/resources/sandbox-top-navigation-helper.js
[modify] https://crrev.com/e6de25ee4229a5154a458c97fb6d0da7d8845b0f/third_party/blink/renderer/core/loader/frame_loader_test.cc
[add] https://crrev.com/e6de25ee4229a5154a458c97fb6d0da7d8845b0f/third_party/blink/web_tests/external/wpt/html/semantics/embedded-content/the-iframe-element/sandbox-top-navigation-child.tentative.sub.window.js
[modify] https://crrev.com/e6de25ee4229a5154a458c97fb6d0da7d8845b0f/content/browser/renderer_host/navigation_policy_container_builder.h
[modify] https://crrev.com/e6de25ee4229a5154a458c97fb6d0da7d8845b0f/content/renderer/policy_container_util.cc
[delete] https://crrev.com/50626517acd61b4600e40f1976013490ef7f4215/third_party/blink/web_tests/http/tests/security/frameNavigation/sandbox-DENIED-cross-origin-top-navigation-nested-sandbox.html
[delete] https://crrev.com/50626517acd61b4600e40f1976013490ef7f4215/third_party/blink/web_tests/http/tests/security/frameNavigation/sandbox-DENIED-cross-origin-top-navigation-expected.txt
[delete] https://crrev.com/50626517acd61b4600e40f1976013490ef7f4215/third_party/blink/web_tests/http/tests/security/frameNavigation/sandbox-ALLOWED-top-navigation-with-two-flags-expected.txt
[delete] https://crrev.com/50626517acd61b4600e40f1976013490ef7f4215/third_party/blink/web_tests/http/tests/security/frameNavigation/sandbox-DENIED-cross-origin-top-navigation-nested-sandbox-expected.txt
[modify] https://crrev.com/e6de25ee4229a5154a458c97fb6d0da7d8845b0f/third_party/blink/renderer/core/frame/policy_container.cc
[modify] https://crrev.com/e6de25ee4229a5154a458c97fb6d0da7d8845b0f/content/browser/renderer_host/policy_container_host_unittest.cc
[modify] https://crrev.com/e6de25ee4229a5154a458c97fb6d0da7d8845b0f/content/browser/renderer_host/policy_container_host.cc
[delete] https://crrev.com/50626517acd61b4600e40f1976013490ef7f4215/third_party/blink/web_tests/http/tests/security/frameNavigation/resources/cross-iframe-that-performs-top-navigation-in-nested-sandboxed-frame.html
[modify] https://crrev.com/e6de25ee4229a5154a458c97fb6d0da7d8845b0f/third_party/blink/renderer/core/frame/policy_container_test.cc
[modify] https://crrev.com/e6de25ee4229a5154a458c97fb6d0da7d8845b0f/content/browser/renderer_host/policy_container_host.h
[modify] https://crrev.com/e6de25ee4229a5154a458c97fb6d0da7d8845b0f/content/browser/renderer_host/navigation_request.cc
[modify] https://crrev.com/e6de25ee4229a5154a458c97fb6d0da7d8845b0f/content/browser/renderer_host/render_frame_host_impl.cc
[delete] https://crrev.com/50626517acd61b4600e40f1976013490ef7f4215/third_party/blink/web_tests/http/tests/security/frameNavigation/sandbox-DENIED-cross-origin-top-navigation.html
[modify] https://crrev.com/e6de25ee4229a5154a458c97fb6d0da7d8845b0f/third_party/blink/public/mojom/frame/policy_container.mojom
[modify] https://crrev.com/e6de25ee4229a5154a458c97fb6d0da7d8845b0f/content/browser/renderer_host/navigation_policy_container_builder.cc
[add] https://crrev.com/e6de25ee4229a5154a458c97fb6d0da7d8845b0f/third_party/blink/web_tests/external/wpt/html/semantics/embedded-content/the-iframe-element/sandbox-top-navigation-grandchild.tentative.sub.window.js
[modify] https://crrev.com/e6de25ee4229a5154a458c97fb6d0da7d8845b0f/content/browser/renderer_host/navigation_policy_container_builder_unittest.cc
[delete] https://crrev.com/50626517acd61b4600e40f1976013490ef7f4215/third_party/blink/web_tests/flag-specific/disable-site-isolation-trials/http/tests/security/frameNavigation/sandbox-DENIED-cross-origin-top-navigation-expected.txt
[modify] https://crrev.com/e6de25ee4229a5154a458c97fb6d0da7d8845b0f/content/browser/renderer_host/navigation_policy_container_builder_browsertest.cc
[delete] https://crrev.com/50626517acd61b4600e40f1976013490ef7f4215/third_party/blink/web_tests/http/tests/security/frameNavigation/sandbox-ALLOWED-top-navigation-with-user-gesture-expected.txt
[add] https://crrev.com/e6de25ee4229a5154a458c97fb6d0da7d8845b0f/third_party/blink/web_tests/external/wpt/html/semantics/embedded-content/the-iframe-element/sandbox-top-navigation-escalate-privileges.tentative.sub.window.js
[modify] https://crrev.com/e6de25ee4229a5154a458c97fb6d0da7d8845b0f/third_party/blink/public/platform/web_policy_container.h
[delete] https://crrev.com/50626517acd61b4600e40f1976013490ef7f4215/third_party/blink/web_tests/flag-specific/disable-site-isolation-trials/http/tests/security/frameNavigation/sandbox-DENIED-cross-origin-top-navigation-nested-sandbox-expected.txt
[add] https://crrev.com/e6de25ee4229a5154a458c97fb6d0da7d8845b0f/third_party/blink/web_tests/external/wpt/html/semantics/embedded-content/the-iframe-element/sandbox-top-navigation-child-special-cases.tentative.sub.window.js
[delete] https://crrev.com/50626517acd61b4600e40f1976013490ef7f4215/third_party/blink/web_tests/http/tests/security/frameNavigation/sandbox-ALLOWED-top-navigation-with-user-gesture.html
[modify] https://crrev.com/e6de25ee4229a5154a458c97fb6d0da7d8845b0f/content/browser/renderer_host/policy_container_host_browsertest.cc
[modify] https://crrev.com/e6de25ee4229a5154a458c97fb6d0da7d8845b0f/third_party/blink/renderer/core/frame/local_frame.cc
[delete] https://crrev.com/50626517acd61b4600e40f1976013490ef7f4215/third_party/blink/web_tests/http/tests/security/frameNavigation/sandbox-ALLOWED-top-navigation-with-two-flags.html


### lb...@chromium.org (2022-10-11)

I've split off the spec work into a separate crbug: https://crbug.com/1373604

I'm going to leave this open for another day or so to make sure the code doesn't get kicked back, and then I'll close out this ticket.

### da...@gmail.com (2022-10-20)

Friendly Ping: this seems fixed?

### lb...@chromium.org (2022-10-21)

Yes, this is fixed. Forgot to close it out.

### [Deleted User] (2022-10-23)

[Empty comment from Monorail migration]

### [Deleted User] (2022-10-23)

[Empty comment from Monorail migration]

### am...@google.com (2022-11-03)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-11-03)

Congratulations, David! The VRP Panel has decided to award you $5,000 for this report. A member of our finance team will be in touch with you soon to arrange payment. Thank you for your efforts and reporting this issue to us -- nice work! 

### am...@google.com (2022-11-04)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-11-28)

[Empty comment from Monorail migration]

### pg...@google.com (2022-11-29)

[Empty comment from Monorail migration]

### pg...@google.com (2022-11-29)

[Empty comment from Monorail migration]

### [Deleted User] (2023-01-28)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1251790?no_tracker_redirect=1

[Monorail blocking: crbug.com/chromium/1373604]
[Monorail mergedwith: crbug.com/chromium/1268868]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40057349)*
