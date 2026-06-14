# Security: RTL+ space, formatting, invisible characters can lead to URL Spoofing

| Field | Value |
|-------|-------|
| **Issue ID** | [40090883](https://issues.chromium.org/issues/40090883) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Network, UI>Browser>Omnibox |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, iOS, ChromeOS |
| **Reporter** | xi...@gmail.com |
| **Assignee** | ct...@chromium.org |
| **Created** | 2018-03-22 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**  

Chrome address bar using RTL-IDNs-TLD

**VERSION**  

Chrome65 on ALL (Windows/macOS/iOS/Android)

**REPRODUCTION CASE**

1.Access <http://xisigr.com/test/spoof/chrome/RLT-IDN-TLD.html>.  

2.Click on the "gmail.com" button.  

3.Address bar says [www.gmail.com](http://www.gmail.com) - this is not [www.gmail.com](http://www.gmail.com).

## Attachments

- [RLT-IDN-TLD.html](attachments/RLT-IDN-TLD.html) (text/plain, 339 B)
- [chrome-ios.png](attachments/chrome-ios.png) (image/png, 81.5 KB)
- [chrome-incognito-ios.png](attachments/chrome-incognito-ios.png) (image/png, 80.7 KB)
- [IMG_3236.png](attachments/IMG_3236.png) (image/png, 183.9 KB)
- [chrome-ios-1.png](attachments/chrome-ios-1.png) (image/png, 198.0 KB)
- [chrome-ios-2.png](attachments/chrome-ios-2.png) (image/png, 176.5 KB)

## Timeline

### el...@chromium.org (2018-03-22)

This looks reasonably plausible; on Mac, I see a "..." after the fake GMail string and the base domain always remains visible at the right end of the omnibox, but it's easily overlooked. Similar in nature to https://crbug.com/chromium/656417.

[Monorail components: UI>Browser>Omnibox UI>Security>UrlFormatting]

### ct...@chromium.org (2018-03-22)

Confirming the same behavior noted in #1 on Linux -- the right part of the domain is still visible, although the highlighting behavior and empty space is very confusing.

On iOS, the right part of the domain is entirely elided, as shown in the original report's screenshots.

Marking this Medium severity (since it isn't a perfect spoof, although it is significantly worse on iOS than other platforms), and Impact-Stable (as it repros on M65 on iOS for me).

Here's the full URL (in punycode):

http://www.gmail.com.xn--ggbla3j.xn--ngbc5azd/?%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%DB%B0



### mg...@chromium.org (2018-03-23)

Yup.

I had a bit of a look.

A break-down of the URL:

http://www.gmail.com.<ARABIC-TEXT>.<ARABIC-TEXT>/?<256xU+00A0 NO-BREAK SPACE><U+06F0 EXTENDED ARABIC-INDIC DIGIT ZERO>

A Python3 expression that produces this URL in unquoted/rendered form:
'http://www.gmail.com.\u0627\u0645\u0627\u0621.\u0634\u0628\u0643\u0629/?' + 256 * '\xa0' + '\u06f0'

Bidi tool analysis of the string:
https://unicode.org/cldr/utility/bidi.jsp?a=http%3A%2F%2Fwww.gmail.com.%D8%A7%D9%85%D8%A7%D8%A1.%D8%B4%D8%A8%D9%83%D8%A9%2F%3F%C2%A0%C2%A0%C2%A0%C2%A0%C2%A0%DB%B0&p=LTR

The fact that the last character is Arabic is a red herring; it works if the last character is any STRONG RTL character or WEAK LTR character (e.g., any number, even ASCII numbers). The rendering treats all the characters up until the end of "gmail.com." as LTR, then switches into RTL to render the Arabic domain labels from the right, and then because the final character is weak LTR, it is nested inside the RTL run and thus the entire rest of the string is rendered as RTL, hence pushing the Arabic domain labels far to the right, with the NBSPs in the middle.

This is a well-known long-standing issue (https://crbug.com/chromium/351639) with a fix implemented (chrome://flags/#left-to-right-urls completely resolves the issue) but requires standards work to roll it out, and I don't have time to work on it. Though the more of these reports I see, the more I am tempted to just ask to push it out as an intervention.

What gives this particular example more weight is that the "middle" characters are NBSPs. I am shocked that NBSP is allowed in a URL. I think it should be blacklisted and thus would appear as "%C2%A0" instead of " ". Note that Firefox blacklists this character which is why the bug doesn't apply there. +jshin to look into blacklisting this character, which I think would close this particular bug.

TL;DR: We should blacklist U+00A0 as a high priority. And the "proper" fix for this is to enable chrome://flags/#left-to-right-urls (https://crbug.com/chromium/351639).

### sh...@chromium.org (2018-03-24)

[Empty comment from Monorail migration]

### xi...@gmail.com (2018-03-26)

mgiuca:
The RTL address bar spoof has never stopped, just like you said https://crbug.com/chromium/351639. Always only show the origin in the Chrome Address Bar that maybe pretty much resolve this and other future spoof bugs, once and for all. (like what Safari does)

### mg...@chromium.org (2018-03-26)

#5 showing only the origin reduces utility, though. That's for our UX designers to decide.

Either way, it doesn't fully resolve these issues. You can still do RTL spoofs with just the origin (like having the labels shown out-of-order).

### js...@chromium.org (2018-03-26)

Black-listing U+00A0 in the path and the query (as opposed to the host name portion) should be handled in GURL. 

>   the more of these reports I see, the more I am tempted to just ask to push it out as an intervention.

mkwst@ : can you look into U+00A0 handling in GURL ?  





[Monorail components: Internals>Network]

### js...@chromium.org (2018-03-26)

>   the more of these reports I see, the more I am tempted to just ask to push it out as an intervention.

I quoted the above for https://crbug.com/chromium/351639, but forgot add a comment on that.  I'm also very tempted to. 

### mg...@chromium.org (2018-03-27)

Why should U+00A0 be allowed in host portion? I would've thought this character should be blacklisted in net/base/escape.cc like some of those other characters.

### mm...@chromium.org (2018-03-27)

Assigning to Mike as per c#7.

### mg...@chromium.org (2018-03-28)

jshin@ can you explain why this should be handled in GURL?

As far as I know, GURL simply escapes everything (to store it canonically as ASCII). It's the net/ side of things that renders out the URL for Omnibox and decides which characters to unescape, and thus where U+00A0 should be blacklisted. (In other words, how is this different from blacklisting any other character for spoofing?)

(I just chatted to Mike and he shares my confusion about this being handled in GURL.)

### xi...@gmail.com (2018-03-28)

Long time ago I have reported a spoof bug using NBSPs(U+00A0) in https://crbug.com/chromium/665358, but chrome haven't fixed. The POC in https://crbug.com/chromium/665358 can now be reproduced.(http://xisigr.com/test/spoof/chrome/rtl_1.html).

### xi...@gmail.com (2018-03-28)

I think forcing the U+00A0 to be displayed as %C2%A0 is much easier to implement as a short-term fix.

### js...@chromium.org (2018-04-03)

> Why should U+00A0 be allowed in host portion?

U+00A0 is not allowed in the host portion [1], but this bug is not about the hostname portion, is it? 

[1]. e.g. (goo<U+00A0>gle.com ) 
http://xn--google-rga.com/

### js...@chromium.org (2018-04-03)

Sorry for conflating net/ with gurl/. 

UnescapeURLWithAdjustmentsImpl in net has to be changed to keep a lot more characters escaped than it currently does (only BiDi-related format control characters are kept escaped). Others include 
format control characters, invisible characters, whitespace-like characters, etc: I have to think a bit more about what characters to include.  However, I'm afraid I don't have time to work on this atm. 


https://cs.chromium.org/chromium/src/net/base/escape.cc?rcl=3ceb5e5e7d3369c157c5e8a401cff8a4acbf602c&l=200


Adding a couple of folks who touched the file.  


### mm...@chromium.org (2018-04-03)

What about the other space characters?  https://www.fileformat.info/info/unicode/category/Zs/list.htm has a list.  There are also weird things like 0-width breaking/non-breaking spaces, which impact display of some languages, I believe?  I'm happy to make code changes, but am far from an expert in this space (pun intended), so would need guidance on just what characters we should be excluding.

### mm...@chromium.org (2018-04-03)

Aside from the space issue, why aren't we displaying the full host name or the slash after it?  splitting up a URL that contains RTL and LTL components to be displayed as non-contiguous blocks of text also seems like a problem to me.

### mg...@chromium.org (2018-04-04)

#7 (jshin):
> Black-listing U+00A0 in the path and the query (as opposed to the host name portion) should be handled in GURL.

#9 (mgiuca):
> Why should U+00A0 be allowed in host portion?

#14 (jshin):
> U+00A0 is not allowed in the host portion [1], but this bug is not about the hostname portion, is it?

Right, your #7 indicated that you wanted to blacklist in path and query BUT NOT host. I was saying, just blacklist it everywhere including host and everywhere else. So doesn't /net make sense?

I'm not sure of the exact mechanism used for blacklisting characters; I guess most of your previous work has been on the domain label blacklisting (keeping domain labels in punycode) rather than the mechanism in net to exclude characters from the whole URL. I think UnescapeURLWithAdjustmentsImpl is the right place but it needs better abstraction (currently splitting it up into three and four-byte characters is a bit UTF-8-implementation-driven). Is this something mmenke@ could work on?

#16 (mmenke):
> What about the other space characters?
Yeah, I think all of them should be excluded. Instead of looking at the Zs category, just use u_isspace (in ICU) [1] to check, maybe? (But then you lose the optimization of looking at the UTF-8 bytes directly; I'd say this function has gotten out of hand and you should just decode each index into a Unicode code point, then can do sane things like looking up code points in a table, and using u_isspace, instead of comparing UTF-8 byte sequences.)

[1] http://icu-project.org/apiref/icu4c/uchar_8h.html#a9e5a0b4c0d3f1ce71e185afc12cb1645

#17 (mmenke):
> why aren't we displaying the full host name or the slash after it?  splitting up a URL that contains RTL and LTL components to be displayed as non-contiguous blocks of text also seems like a problem to me.

See #3. This is https://crbug.com/chromium/351639, which has a fix but there's a compat problem with rolling it out (the current behaviour is explicitly required by spec).

### mg...@chromium.org (2018-04-04)

[Empty comment from Monorail migration]

### mm...@chromium.org (2018-04-04)

I'll take on refactoring the method and using u_isspace - I agree the method has gotten out of hand, and I don't think we decode a URL for display *that* often.  Is there an icu or base method to convert a UTF8 character to UTF32?  CBU8_NEXT, I guess?

I think the simplest thing to do is to unescape the entire string (Respecting ASCII rules about what not to escape), and then use CBU8_NEXT to walk back through it, unicode-character-by-character (Including invalid characters), re-escaping ones that are not safe.

There are other options, but nothing that seems simpler, even if re-escaping is a bit ugly.

### js...@chromium.org (2018-04-04)

> Right, your #7 indicated that you wanted to blacklist in path and query BUT NOT host.

Matt, sorry I was not clear. I did not mean that U+00A0 and other related characters should not be blocked in the host name portion. They are already blocked (they ARE not allowed by IDN RFC to begin with). See https://www.chromium.org/developers/design-documents/idn-in-google-chrome . I start with a relatively small subset of the Unicode and add more constraints. That small subset excludes a lot of characters (invisible, control, whitespace, math alphabet, punctuation marks, etc). 

As to how to fix the function in question, I agree that what's described in https://crbug.com/chromium/824715#c18/20 is a sane way (the current approach is hard to generalize). 

Thanks, mmenke@. 

As for what characters to keep escaped, there are a few sets to join together:

https://unicode.org/cldr/utility/list-unicodeset.jsp?a=[:WSpace:]
https://unicode.org/cldr/utility/list-unicodeset.jsp?a=[:Default_Ignorable_Code_Point=Yes:]
https://unicode.org/cldr/utility/list-unicodeset.jsp?a=%5B%3ACf%3A%5D&abb=on&g=gc&i=

See also 
http://unicode.org/reports/tr31/tr31-8.html#Layout_and_Format_Control_Characters

I suggest that we start with an aggressive set (to err on the safe side). We can loosen up as specific 'linguistic' needs are reported.

You can use uchar.h API of ICU ( http://icu-project.org/apiref/icu4c/uchar_8h.html ) to test for various Unicode character properties. 

### js...@chromium.org (2018-04-04)

[Empty comment from Monorail migration]

### mg...@chromium.org (2018-04-04)

#20: 
> Is there an icu or base method to convert a UTF8 character to UTF32?  CBU8_NEXT, I guess?

Yes, that's it, but use this wrapper in base:

https://cs.chromium.org/chromium/src/base/strings/utf_string_conversion_utils.h?q=ReadUnicodeCharacter&l=35

(I don't know why it decrements char_index so you have to increment it again, but there you go.)

> I think the simplest thing to do is to unescape the entire string (Respecting ASCII rules about what not to escape), and then use CBU8_NEXT to walk back through it, unicode-character-by-character (Including invalid characters), re-escaping ones that are not safe.

Hmm. I understand why (otherwise you can't use ReadUnicodeCharacter to read the UTF-8 sequences that are encoded), but I'm hesitant to recommend this. It makes the final code quite messy, since you'll have to deal with ASCII characters separately to non-ASCII. Basically, you'll have to selectively *decode* ASCII characters while always decoding non-ASCII (i.e., what we do now). And then in a separate pass, selectively *encode* non-ASCII characters while ignoring ASCII. That seems quite messy.

I would rather you do it all in one pass, even if it makes UTF-8 decoding trickier:

for each character:
  if it is '%':
    decode it into a byte
    while this is an unfinished UTF-8 byte sequence:
      look for following '%' and decode those
    decode the UTF-8 byte sequence into a code point
    if the code point is allowed to be unescaped, replace the % sequence with the decoded bytes

It means you can't use CBU8_NEXT or ReadUnicodeCharacter, but you can probably find a lower-level thing in ICU to decode one byte at a time. I think you can make this a lot cleaner than the thing where you decode then re-encode. I'm happy to help dig through ICU to find the right thing to call.

### js...@chromium.org (2018-04-04)

BTW, https://url.spec.whatwg.org/#url-rendering  does not have much to say except that 'invisible' characters are not to be unescaped. 


### mm...@chromium.org (2018-04-04)

I'm unaware of any method that takes in one unicode character as input at a time.  (icu may have one, somewhere, but doing a random walk through ICU functions and trying to determine what they do is something that has significant potential to drive me to madness).

I suppose I could use CBU8_IS_SINGLE / CBU8_IS_LEAD / otherwise to assemble one icu character "string" at a time, and be sure to handle the case where we have a valid UTF8 character followed by invalid non-single / non-lead bytes.

Actually, I'm not sure I can even use icu here.  We build Cronet without icu, to save on binary size, using platform Java functions instead, and I'm not sure we can exclude the files that depend on unescaping from the Cronet build, so anything that depends on icu's database being loaded may not work here, unfortunately.

### mm...@chromium.org (2018-04-04)

It looks like this code indeed cannot depend on icu, due to cronet.  I'll clean up the parser and just expand the list of characters - we may want to look at using icu in a followup, to help protect against regressions.  There are few consumers of this method in net/, but there are some.

Are non-breaking spaces OK to keep escaped?  My understanding is that in some languages, they can affect character display, so not unescaping them could lead to display issues those languages.

Expect to have a CL out today or tomorrow.

### mm...@chromium.org (2018-04-04)

Also, if we're going to be aggressive, first pass, about blocking characters, I don't think we want to merge to M66 - stable isn't really a good place to deal with the fallout this will inevitably result in.  Alternatively, we could just block pure whitespace characters (excluding 0-width spaces), and merge that to M66, and deal with broadening the net on trunk.

### mm...@chromium.org (2018-04-05)

[Empty comment from Monorail migration]

### xi...@gmail.com (2018-04-08)

#6 (mgiuca)
>Either way, it doesn't fully resolve these issues. You can still do RTL spoofs with just the origin (like having the labels shown out-of-order).

You are right.
I give a case. Please access http://www.gmail.com.xn--mgb.999.xn--ggbla3j.xn--ngbc5azd in chrome. 
It will display http://www.gmail.com.ا.999.اماء.شبكة/ in address bar. It is a spoof.

### mg...@chromium.org (2018-04-09)

#29 Yes, and this is well-known (https://crbug.com/chromium/351639), with a fix landed (chrome://flags/#left-to-right-urls) but blocked on web standards discussions. That's orthogonal to rendering of invisible characters, which is the novel issue identified here.

### sa...@chromium.org (2018-04-09)

[Empty comment from Monorail migration]

### mm...@chromium.org (2018-04-11)

I don't think we can do anything reasonable in escape.cc until we fix https://crbug.com/chromium/831321, since adding logic not to unescape code affects the UTF-16 variant of the unescaping function in weird and magic ways.

### xi...@gmail.com (2018-04-12)

I think this issue security severity should be set to high level, which can make a perfect spoof in address bar.

I give another demo: http://xisigr.com/test/spoof/chrome/RLT-IDN-TLD-1.html

### mg...@chromium.org (2018-04-12)

The current fix CL is a fairly long chain behind a large refactor. Not likely to land in M67 and not mergeable either.

If we do want to have this fixed in M67 (or 66?) then my suggestion was to hack in the new blacklisted characters into the existing three-utf-8-byte structure, and then apply the refactor later. (But mmenke said on [1]: "don't think writing this CL twice is a useful time investment".)

I'm not fussed if this fix is delayed until M68 (since the bug likely been around "forever"). If security team thinks it's urgent, I think the above approach (hack fix, then refactor and fix again) is the only feasible way to merge this. I vote we wait.

[1] https://chromium-review.googlesource.com/c/chromium/src/+/998014#message-7d5e1b4866288aa9d3ca915cabbd1501acd7ec1d

### js...@chromium.org (2018-04-12)

> We build Cronet without icu, to save on binary size, using platform Java functions instead, 

Platform Java can be used to get most of character properties. 

An alternative would be to carve out a small subset of ICU for Cronet (it can be pretty small:  a few hundreds kB). 

### xi...@gmail.com (2018-04-13)

You can spoof all 'io/no' TLD in address bar at least.
Demo 3: http://xisigr.com/test/spoof/chrome/RLT-IDN-TLD-2.html

### mm...@chromium.org (2018-04-13)

I think the refactoring/omnibox fix would be relatively safe to merge to M67, since it just branched.  But I agree that merging them to M66 is not a good idea.  I'll defer to more security-minded folks on whether it's worth merging ~200 lines of refactor (Plus the omnibox search fix) in order to land the actual fix for this bug.

### ct...@chromium.org (2018-04-13)

We should definitely try to merge into M67.

I'm borderline on whether this is medium or high severity -- on at least iOS the spoofing is fairly complete, which would be closer to High severity. Given that, I'd say should see if we can merge into M66, but if you think it is particularly risky or the mitigating factors are sufficient, then we can maybe just do it in M67. The current fix CL does look moderately complicated (from my quick skim of it), so I'll defer to you on the risk assessment.

### mg...@chromium.org (2018-04-16)

Because of the way the fix was structured (a fairly major refactor), merging (even into M67) will be complicated.

You'll need to merge:

1. https://crrev.com/550720 (+116, -220) (precursor to refactor)
2. https://crrev.com/c/998014 (+209, -185) (refactor, not yet landed)
3. A not-yet-written CL to actually add those characters to the blacklist.

I still believe if we want to merge this fix, it should be written in a way that does not depend on the refactor (by adding those space characters to the existing UTF-8-based blacklist), even though it's more work.

### mm...@chromium.org (2018-04-16)

Given that branch point was just a couple days ago, I don't think it's that unreasonable to merge the extra CLs - I'd certainly oppose merging that much two weeks down the line.

### mg...@chromium.org (2018-04-16)

OK. I'm reviewing https://crrev.com/c/998014 now.

### bu...@chromium.org (2018-04-16)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/6e8dbd1dd7d1fd3232f3f0c40eb3c133ea58966c

commit 6e8dbd1dd7d1fd3232f3f0c40eb3c133ea58966c
Author: Matt Menke <mmenke@chromium.org>
Date: Mon Apr 16 17:55:36 2018

Restructure UnescapeURLWithAdjustmentsImpl().

In particular, unescape entire unicode characters at once, and then
compare against unescape blacklists, rather than the other way around,
to simplify code and avoid the tree structure of the old code. This
will also allow the method to use icu's code point classification
logic, at some point in the future.

Also separate out comparing against the character blacklist and UTF-8
character decoding into separate methods, and add a few more test cases
to unittest.

The method itself should behave exactly the same as before.

Bug: 824715
Change-Id: I5311f25bfda4132b122ec4a079740adf093099a3
Reviewed-on: https://chromium-review.googlesource.com/998014
Commit-Queue: Matt Menke <mmenke@chromium.org>
Reviewed-by: Matt Giuca <mgiuca@chromium.org>
Reviewed-by: Helen Li <xunjieli@chromium.org>
Cr-Commit-Position: refs/heads/master@{#551029}
[modify] https://crrev.com/6e8dbd1dd7d1fd3232f3f0c40eb3c133ea58966c/net/base/escape.cc
[modify] https://crrev.com/6e8dbd1dd7d1fd3232f3f0c40eb3c133ea58966c/net/base/escape.h
[modify] https://crrev.com/6e8dbd1dd7d1fd3232f3f0c40eb3c133ea58966c/net/base/escape_unittest.cc


### bu...@chromium.org (2018-04-17)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/fb02f0ec4a52fa0a19009a54d7c9e65b25ca92f5

commit fb02f0ec4a52fa0a19009a54d7c9e65b25ca92f5
Author: Matt Menke <mmenke@chromium.org>
Date: Tue Apr 17 06:05:02 2018

UnescapeURLComponent:  Don't unescape UTF-8 space characters.

Bug: 824715
Change-Id: I71d7f38a2dbe9de6515b8e9d284ab622c2311276
Reviewed-on: https://chromium-review.googlesource.com/1014367
Commit-Queue: Matt Giuca <mgiuca@chromium.org>
Reviewed-by: Matt Giuca <mgiuca@chromium.org>
Cr-Commit-Position: refs/heads/master@{#551260}
[modify] https://crrev.com/fb02f0ec4a52fa0a19009a54d7c9e65b25ca92f5/net/base/escape.cc
[modify] https://crrev.com/fb02f0ec4a52fa0a19009a54d7c9e65b25ca92f5/net/base/escape_unittest.cc


### bu...@chromium.org (2018-04-17)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/6e8dbd1dd7d1fd3232f3f0c40eb3c133ea58966c

commit 6e8dbd1dd7d1fd3232f3f0c40eb3c133ea58966c
Author: Matt Menke <mmenke@chromium.org>
Date: Mon Apr 16 17:55:36 2018

Restructure UnescapeURLWithAdjustmentsImpl().

In particular, unescape entire unicode characters at once, and then
compare against unescape blacklists, rather than the other way around,
to simplify code and avoid the tree structure of the old code. This
will also allow the method to use icu's code point classification
logic, at some point in the future.

Also separate out comparing against the character blacklist and UTF-8
character decoding into separate methods, and add a few more test cases
to unittest.

The method itself should behave exactly the same as before.

Bug: 824715
Change-Id: I5311f25bfda4132b122ec4a079740adf093099a3
Reviewed-on: https://chromium-review.googlesource.com/998014
Commit-Queue: Matt Menke <mmenke@chromium.org>
Reviewed-by: Matt Giuca <mgiuca@chromium.org>
Reviewed-by: Helen Li <xunjieli@chromium.org>
Cr-Commit-Position: refs/heads/master@{#551029}
[modify] https://crrev.com/6e8dbd1dd7d1fd3232f3f0c40eb3c133ea58966c/net/base/escape.cc
[modify] https://crrev.com/6e8dbd1dd7d1fd3232f3f0c40eb3c133ea58966c/net/base/escape.h
[modify] https://crrev.com/6e8dbd1dd7d1fd3232f3f0c40eb3c133ea58966c/net/base/escape_unittest.cc


### mm...@chromium.org (2018-04-17)

I'm assuming that the above messages do *not* mean this was merged, but instead we have a bot going berserk, mad with power.

### sh...@chromium.org (2018-04-18)

Please mark security bugs as fixed as soon as the fix lands, and before requesting merges. This update is based on the merge- labels applied to this issue. Please reopen if this update was incorrect.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mm...@chromium.org (2018-04-18)

Requesting to merge the CL chain to M67.

https://chromium-review.googlesource.com/1004855
https://chromium-review.googlesource.com/998014
https://chromium-review.googlesource.com/1014367

https://crbug.com/chromium/824715#c46 looks to be mis-interpreting the mass-spammed "merge-merged-testbranch" label, though the issue is in fact fixed.

### sh...@chromium.org (2018-04-19)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-04-19)

Your change meets the bar and is auto-approved for M67. Please go ahead and merge the CL to branch 3396 manually. Please contact milestone owner if you have questions.
Owners: cmasso@(Android), cmasso@(iOS), kbleicher@(ChromeOS), govind@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### bu...@chromium.org (2018-04-19)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/22f489551e5371eb2fb50a69578defc940b78d07

commit 22f489551e5371eb2fb50a69578defc940b78d07
Author: Matt Menke <mmenke@chromium.org>
Date: Thu Apr 19 16:59:01 2018

Remove UnescapeURLComponent() overload that takes a base::string16.

The method has some safe-for-display safety checks that assume the input
is UTF-8 / output is UTF-8.  This change makes it at least a little
harder to avoid those checks, and makes output no longer vary based on
whether passing in a std::string or a string16 (By removing the latter
option entirely).

TBR=mmenke@chromium.org

(cherry picked from commit 4858757b3c659da84c0eb8d4cccc728331eba281)

Bug: 824715, 831321
Change-Id: Ib39a2cccd71861213341e92932525e8ecafc60cd
Reviewed-on: https://chromium-review.googlesource.com/1004855
Reviewed-by: Matt Giuca <mgiuca@chromium.org>
Reviewed-by: Justin Donnelly <jdonnelly@chromium.org>
Commit-Queue: Matt Menke <mmenke@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#550720}
Reviewed-on: https://chromium-review.googlesource.com/1019841
Reviewed-by: Matt Menke <mmenke@chromium.org>
Cr-Commit-Position: refs/branch-heads/3396@{#130}
Cr-Branched-From: 9ef2aa869bc7bc0c089e255d698cca6e47d6b038-refs/heads/master@{#550428}
[modify] https://crrev.com/22f489551e5371eb2fb50a69578defc940b78d07/components/omnibox/browser/url_index_private_data.cc
[modify] https://crrev.com/22f489551e5371eb2fb50a69578defc940b78d07/net/base/escape.cc
[modify] https://crrev.com/22f489551e5371eb2fb50a69578defc940b78d07/net/base/escape.h
[modify] https://crrev.com/22f489551e5371eb2fb50a69578defc940b78d07/net/base/escape_unittest.cc
[modify] https://crrev.com/22f489551e5371eb2fb50a69578defc940b78d07/net/base/unescape_url_component_fuzzer.cc


### bu...@chromium.org (2018-04-19)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/96c462f079dc876cd6678efe1e67c91cdd68b64b

commit 96c462f079dc876cd6678efe1e67c91cdd68b64b
Author: Matt Menke <mmenke@chromium.org>
Date: Thu Apr 19 18:47:56 2018

Restructure UnescapeURLWithAdjustmentsImpl().

In particular, unescape entire unicode characters at once, and then
compare against unescape blacklists, rather than the other way around,
to simplify code and avoid the tree structure of the old code. This
will also allow the method to use icu's code point classification
logic, at some point in the future.

Also separate out comparing against the character blacklist and UTF-8
character decoding into separate methods, and add a few more test cases
to unittest.

The method itself should behave exactly the same as before.

TBR=mmenke@chromium.org

(cherry picked from commit 6e8dbd1dd7d1fd3232f3f0c40eb3c133ea58966c)

Bug: 824715
Change-Id: I5311f25bfda4132b122ec4a079740adf093099a3
Reviewed-on: https://chromium-review.googlesource.com/998014
Commit-Queue: Matt Menke <mmenke@chromium.org>
Reviewed-by: Matt Giuca <mgiuca@chromium.org>
Reviewed-by: Helen Li <xunjieli@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#551029}
Reviewed-on: https://chromium-review.googlesource.com/1020080
Reviewed-by: Matt Menke <mmenke@chromium.org>
Cr-Commit-Position: refs/branch-heads/3396@{#136}
Cr-Branched-From: 9ef2aa869bc7bc0c089e255d698cca6e47d6b038-refs/heads/master@{#550428}
[modify] https://crrev.com/96c462f079dc876cd6678efe1e67c91cdd68b64b/net/base/escape.cc
[modify] https://crrev.com/96c462f079dc876cd6678efe1e67c91cdd68b64b/net/base/escape.h
[modify] https://crrev.com/96c462f079dc876cd6678efe1e67c91cdd68b64b/net/base/escape_unittest.cc


### mm...@chromium.org (2018-04-19)

I'm not comfortable marking this as fixed yet, given that we're leaving formatting characters and the like unescaped, so marking it as assigned (It was just marked as fixed by two bots running amok)

### bu...@chromium.org (2018-04-20)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/5b06c8a7de19d69518513604c1122ffb8a1be101

commit 5b06c8a7de19d69518513604c1122ffb8a1be101
Author: Matt Menke <mmenke@chromium.org>
Date: Fri Apr 20 22:03:32 2018

UnescapeURLComponent:  Don't unescape UTF-8 space characters.

TBR=mmenke@chromium.org

(cherry picked from commit fb02f0ec4a52fa0a19009a54d7c9e65b25ca92f5)

Bug: 824715
Change-Id: I71d7f38a2dbe9de6515b8e9d284ab622c2311276
Reviewed-on: https://chromium-review.googlesource.com/1014367
Commit-Queue: Matt Giuca <mgiuca@chromium.org>
Reviewed-by: Matt Giuca <mgiuca@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#551260}
Reviewed-on: https://chromium-review.googlesource.com/1022870
Reviewed-by: Matt Menke <mmenke@chromium.org>
Cr-Commit-Position: refs/branch-heads/3396@{#176}
Cr-Branched-From: 9ef2aa869bc7bc0c089e255d698cca6e47d6b038-refs/heads/master@{#550428}
[modify] https://crrev.com/5b06c8a7de19d69518513604c1122ffb8a1be101/net/base/escape.cc
[modify] https://crrev.com/5b06c8a7de19d69518513604c1122ffb8a1be101/net/base/escape_unittest.cc


### sh...@chromium.org (2018-05-04)

mmenke: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mm...@chromium.org (2018-05-04)

I'm going to leave on nags, mostly to make sure this stays on my radar, but I'm deprioritizing dealing with the formatting characters - working my way there, just a matter of time.

### sh...@chromium.org (2018-05-19)

mmenke: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2018-05-30)

[Empty comment from Monorail migration]

### xi...@gmail.com (2018-07-02)

Any update here?
Is 'http://xisigr.com/test/spoof/chrome/RLT-IDN-TLD.html' fixed in M-67?

### mm...@chromium.org (2018-07-10)

Sorry for the slow response.  We no longer unescape whitespace characters in URLs, so that particular URL is fixed.  I didn't add any control codes or other characters suggested in https://crbug.com/chromium/824715#c21, so am leaving the bug open (We've run into issues where the unescaping code is expected to do different things by different people, and don't want to broaden the changes until we have that resolved - something I, at least, am not actively working on)

### mg...@chromium.org (2018-07-11)

#59 I am actively working (slowly) on fixing the unescaping code. See https://crbug.com/chromium/849998 (which I'll add as a blocker then).

### sh...@chromium.org (2018-07-25)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-09-05)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-10-17)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-12-05)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-01-30)

[Empty comment from Monorail migration]

### xi...@gmail.com (2019-02-21)

Any update here?

### mm...@chromium.org (2019-02-21)

Not that I'm aware of, at least since mgiuca's last updates on https://crbug.com/chromium/849998.  Unfortunately, this issue is largely blocked on auditing and fixing all consumers of the unescaping code, which crosses a lot of areas of the code that I'm unfamiliar with, and figuring out what to do for each consumer and fixing it often isn't straightforward.

If someone else has the cycles, I'm certainly happy to cede ownership of the bug.

### sh...@chromium.org (2019-03-13)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-04-24)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-06-06)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-07-31)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-09-11)

[Empty comment from Monorail migration]

### ct...@chromium.org (2019-09-13)

Nabbing this bug as we are working to drive down Medium+ severity security UI bugs this quarter.

My understanding is as follows:

The change crrev.com/c/1014367 “Don’t unescape UTF-8 space characters” added Unicode spaces to the banned list for unescaping. However, the full set of characters we want to keep unescaped are:

https://unicode.org/cldr/utility/list-unicodeset.jsp?a=[:WSpace:]
https://unicode.org/cldr/utility/list-unicodeset.jsp?a=[:Default_Ignorable_Code_Point=Yes:]
https://unicode.org/cldr/utility/list-unicodeset.jsp?a=%5B%3ACf%3A%5D&abb=on&g=gc&i=

(Per https://crbug.com/chromium/824715#c21. See also the Unicode Layout and Format Control Characters doc.)

However, we are hesitant to add this to the banned list because we already have bugs with non-display code using URL rendering code (https://crbug.com/chromium/849998 tracks this). Many of these have been fixed, but a few remain (at least https://crbug.com/chromium/849938 and https://crbug.com/chromium/868214 for drag-and-drop and bookmarks).

If those consumers are all fixed, then adding the remaining character sets to the banned list should be relatively straightforward.

Those two remaining bugs, however, I don't believe need to be fixed for us to add the remaining charsets to the banned list. https://crbug.com/chromium/849938 no longer repros for me on Linux (and we don't think it ever repro'd outside Linux), and https://crbug.com/chromium/868214 is more or less fixed already.

I'll do one last scan for additional consumers that are incorrectly using these functions, and if there doesn't appear to be anything with obvious breakage I'll go ahead an add the additional charsets to the banned list.

If we do add the new banned characters, then the only remaining issue is the BiDi label ordering problem, which is tracked in https://crbug.com/chromium/351639 (so https://crbug.com/chromium/824715 could be closed).

### mm...@chromium.org (2019-09-13)

That sounds reasonable to me - I remove all the cases where I thought changing to the other method was clearly the right thing to do, only leaving ambiguous callers around, where they may actually want the extra behavior.  Thanks for taking this!

### ct...@chromium.org (2019-09-13)

I have a WIP CL up at https://chromium-review.googlesource.com/c/chromium/src/+/1803833

It should cover everything that was not already on the banned list from the Default Ignorable and Formatting sets.

However, my new tests for the Tags block (U+E0000--E007F) and Ideographic-specific variation selectors (U+E0100--E01EF) are all failing and I'm not sure why. Any ideas mmenke@? I'll keep digging to see if I can figure out why they are still getting unescaped by the code.

### mm...@chromium.org (2019-09-13)

[cthomp]:  Disclaimer:  I'm not all that familiar with this space.  That having been said, I think your test is wrong?

https://www.fileformat.info/info/unicode/char/e0001/index.htm claims that U+e0001 is 0xF3 0xA0 0x80 0x80, not %F0%9C%80%80 (Which looks to be U+1c000).

### ct...@chromium.org (2019-09-13)

Oh huh... Yep it appears the lookup tool I was using to get the %-escaped versions was failing on these ones. Thanks!

### ct...@chromium.org (2019-09-24)

The CL at crrev.com/c/1803833 landed yesterday but bugdroid never updated this bug... Marking this as fixed.

### na...@google.com (2019-09-27)

[Empty comment from Monorail migration]

### na...@google.com (2019-10-04)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2019-10-04)

Congrats! The Panel decided to reward $3,000 for this report :) 

### na...@google.com (2019-10-07)

[Empty comment from Monorail migration]

### ad...@google.com (2019-12-05)

[Empty comment from Monorail migration]

### ad...@chromium.org (2019-12-06)

[Empty comment from Monorail migration]

### ad...@chromium.org (2019-12-10)

[Empty comment from Monorail migration]

### sh...@chromium.org (2020-01-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-05)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-05)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-06)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-08)

This issue was migrated from crbug.com/chromium/824715?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Internals>Network, UI>Browser>Omnibox, UI>Security>UrlFormatting]
[Monorail blocked-on: crbug.com/chromium/831321, crbug.com/chromium/849998]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40090883)*
