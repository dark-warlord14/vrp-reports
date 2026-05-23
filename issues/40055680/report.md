# Security: Sanitizer API bypass

| Field | Value |
|-------|-------|
| **Issue ID** | [40055680](https://issues.chromium.org/issues/40055680) |
| **Status** | Fixed |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Blink>SecurityFeature>SanitizerAPI |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | mi...@bentkowski.info |
| **Assignee** | vo...@chromium.org |
| **Created** | 2021-04-26 |
| **Bounty** | $3,000.00 |

## Description

Hey,

I am aware that Sanitizer API is currently behind a flag so I'm not sure if any bypasses qualify for a bounty. Anyway, I still think it's worth to report possible bypasses.

There's a way to bypass the sanitizer when used with sanitizeToString. Here's a short PoC (tested on 92.0.4489.0):

document.body.innerHTML = new Sanitizer().sanitizeToString(`
<math>
<textarea>
<a title="</textarea><img src onerror=alert(1)>">
`)

The payload abuses difference in parsing of foreign content vs "plain" HTML. Originally, <textarea> is parsed in foreign content, hence <a> is a child of <textarea>. However, after sanitization, the <math> tag is no longer present, hence <textarea> is closed just before IMG, allowing to execute JS code.

I've created a short test to check if other tags can also be vulnerable but at the first sight it seems to apply for <textarea> and <style>. Here's the test:

function test() {
    const FOREIGN_CONTENT = ['svg', 'math'];
    const RCDATA = ['title', 'textarea'];
    const RAWTEXT = ['style', 'xmp', 'iframe', 'noembed', 'noframes'];
    const NOSCRIPT = ['noscript'];
    const PLAINTEXT = ['plaintext'];
    
    const ALL_TAGS = RCDATA.concat(RAWTEXT).concat(NOSCRIPT).concat(PLAINTEXT);
    for (const svgOrMath of FOREIGN_CONTENT) {
        for (const tag of ALL_TAGS) {
            const html = `<${svgOrMath}><${tag}><a title="</${tag}><img src onerror=alert(1)>">`;
            const sanitized = new Sanitizer().sanitizeToString(html);
            const template = document.createElement('template');
            template.innerHTML = sanitized;
            const isVulnerable = template.content.querySelector('[onerror]');
            if (isVulnerable) {
                console.error(`Tag ${tag} within ${svgOrMath} is vulnerable!`);
            }
        }
    }
}

## Timeline

### [Deleted User] (2021-04-26)

[Empty comment from Monorail migration]

### mk...@google.com (2021-04-26)

Assigning to vogelheim@ to triage.

[Monorail components: Blink>SecurityFeature>SanitizerAPI]

### mi...@bentkowski.info (2021-04-26)

There's also another bypass (which probably could be reported in a separate issue?) that makes use of <noscript>. This was not caught by the test I wrote, because I was assigning to template.innerHTML - which is parsed with scripting disabled. However, in real world case, when assigning to div.innerHTML, the code is parsed with scripting enabled leading to bypass. Here's the PoC:


    document.body.innerHTML =  new Sanitizer().sanitizeToString(`<noscript><u title="</noscript><img src onerror=alert(1)>">`)

### mi...@bentkowski.info (2021-04-26)

Here's another bypass. This one could theoretically work with sanitize (not only sanitizeToString) but in that case, an element in SVG namespace is created, without a parent <svg> and seems to not be rendered.

The bypass:

    document.body.innerHTML = new Sanitizer().sanitizeToString(`<svg><a href=javascript:alert(1)>CLICK ME`)

This one works because the href attribute is verified for "javascript:" protocol only for HTMLAnchorElement, not for SVGAElement [1].

[1]: https://source.chromium.org/chromium/chromium/src/+/master:third_party/blink/renderer/modules/sanitizer_api/sanitizer.cc;l=345




### aj...@google.com (2021-04-27)

Setting some flags - this might change once I figure out the status of the Sanitizer() api.

### vo...@google.com (2021-04-28)

Thanks for the report. Looking...

### vo...@google.com (2021-04-28)

Thanks for the report! I'll need a bit more time to assess this properly, but a few  quick comments:

- I've tracked this at crbug.com/1203238 - since by then I had only seen the GitHub issues, rather than this one. I think it's the same reporter, though, so this should certainly be their credit. :)

- @ajgo: Status of Sanitizer: Sanitizer API is currently behind a flag. For M91, we're planning on upgrading this to be part of experimental (--enable-experimental-web-platform-features) and have user-accessible UI in chrome://flags. These changes are in the current M91 beta.

- A cursory look suggests there's two issues here, mXSS on the one hand, and SVG / MathML on the other.

  - mXSS - confusion when markup is un-parsed and then re-parsed - is something the Sanitizer cannot (and doesn't claim to) protect against. IMHO, that doesn't count, since we're not violating any of the security properties we're promising.

  - SVG (& other namespaced content): The spec currently doesn't say anything about namespaced content - it's an open issue how we'd like to treat it - and hence we've very naively implemented it by just ignoring all namespaces. I think this counts since, while the spec doesn't make any promises on those particular elements,  our implementation strategy of just ignoring it is just... too simple.


I'll need a bit more time to evaluate this, but it looks like the given examples cover both categories.

### vo...@google.com (2021-04-28)

poc from https://crbug.com/chromium/1202970#c0 (<math> + <textarea>): mXSS.

document.body.innerHTML = new Sanitizer().sanitizeToString(`
<math>
<textarea>
<a title="</textarea><img src onerror=alert(1)>">
`)

The Sanitizer correctly parses + sanitize this (with </textarea> as attribute value), and it's the subsequent unparsing + re-parsing that causes the problem. Note that the variant with .replaceChildren + .sanitize doesn't have this problem:

document.body.replaceChildren(new Sanitizer().sanitize(`
<math>
<textarea>
<a title="</textarea><img src onerror=alert(1)>">
`))

---------------------------------

poc from https://crbug.com/chromium/1202970#c3 (</noscript> in attribute value): mXSS

Same as above. Sanitizer correctly parses + sanitizes this (with the </noscript> being part of the attribute value), and it's the un-parsing + re-parsing that causes the problem:

  document.body.innerHTML =  new Sanitizer().sanitizeToString(`<noscript><u title="</noscript><img src onerror=alert(1)>">`)

The non-mXSS-y usage with .replaceChildren + .sanitizer does not have this problem:

  document.body.replaceChildren(new Sanitizer().sanitize(`<noscript><u title="</noscript><img src onerror=alert(1)>">`))

----------------------

poc from https://crbug.com/chromium/1202970#c4 (javascript:-URL in <svg><a> ): Problem with namespaced element handling.

This one is different than the others and will work with either .sanitize or .sanitizeToString. The analysis in https://crbug.com/chromium/1202970#c4 is correct, that the javascript: handling looks only at HTML <a>, not at SVG <a>. (Per spec, actually.) However, the combination of this, plus our decision to ignore <svg> in the implementation is - IMHO - a valid bug.

    document.body.innerHTML = new Sanitizer().sanitizeToString(`<svg><a href=javascript:alert(1)>CLICK ME`)

This seems properly mitigated by crrev.com/c/2851606. This is tracked on a different bug (crbug.com/1203238).

-----------------

In https://crbug.com/chromium/1202970#c7 I speculated that the reports on which crbug.com/1203238 is based were from the same submitter. On a second view, the names look quite different, so I no longer think this is correct.

### mi...@bentkowski.info (2021-04-28)

My two cents:

I agree that we have two mXSS-es but I don't agree that it's not a bug. I am also a proponent of usage of sanitize instead of sanitizeToString but I'm pretty sure that sanitizeToString would still be quite common. Mainly because many frameworks make it easy to feed arbitrary HTML to an element but not necessarily a document fragment. For instance, in Vue there's a v-html attribute, but we don't have v-doc-fragment. Similarly with dangerouslySetInnerHTML in React.

For this reason, I still believe that such bugs - especially existing in the default configuration - should be fixed.

What I'd propose to do would be very similar to my fairly recent pull request to DOMPurify: https://github.com/cure53/DOMPurify/pull/495. The idea is that we delete elements that have unexpected namespace which could not normally happen on HTML parsing.

Consider the example:

<math>
<textarea>
<a title="</textarea><img src onerror=alert(1)>">

After sanitization, the <math> is deleted but the <textarea> is kept. However, it is not normally possible to create a <textarea> in MathML namespace whose parent is not another element in MathML. Hence, this element should also be deleted. Please refer to the pull request to more info how exactly this method works.

With regard to <noscript>, I believe that parsing on sanitize/sanitizeToString should assume that scripting flag is enabled because when the code will be eventually assigned with replaceChildren/innerHTML, scripting will most likely be enabled.


Lastly, I am not the author of the bypasses in these GitHub issues :)

### vo...@chromium.org (2021-04-29)

Related:
- https://github.com/WICG/sanitizer-api/pull/87 (Fixes the omission of <noscript> in the spec.)
- https://github.com/WICG/sanitizer-api/pull/88 (Proposal to remove <textarea>. I also added <title>, since that appears to have the same parsing rules.)

The first one is covered by the fix for crbug.com/1203238. I intend to implement the 2nd when it's approved for the spec.

Thanks again for the feedback!

### vo...@chromium.org (2021-11-10)

Ah, it's been a while. The fixes named in https://crbug.com/chromium/1202970#c10 have long-since landed. Also, the spec has meanwhile evolved to address mXSS/re-parsing type vulnerabilities by discouraging string-based usage in general, and to -- presently -- simply disallow any non-HTML content. With this, I consider the present issue solved.

We'll have to be careful to not re-introduce this when "proper" handling of MathML + SVG is coming, though. The latest attempts can be found here: https://github.com/WICG/sanitizer-api/pull/137 

### [Deleted User] (2021-11-12)

[Empty comment from Monorail migration]

### [Deleted User] (2021-11-12)

[Empty comment from Monorail migration]

### [Deleted User] (2022-02-16)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@google.com (2022-03-11)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-03-11)

Congratulations! The VRP Panel has decided to award you $3000 for this report. Thank you for this report as well as your exceptional patience as this issue was resolved (yay, spec changes!). 

### am...@google.com (2022-03-11)

[Empty comment from Monorail migration]

### mi...@bentkowski.info (2022-03-15)

Thank you!

### is...@google.com (2022-03-15)

This issue was migrated from crbug.com/chromium/1202970?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40055680)*
