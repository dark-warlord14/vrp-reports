# Security: Domain spoofing thanks to U+0F8C rendered as 'space' on Mac 

| Field | Value |
|-------|-------|
| **Issue ID** | [40087415](https://issues.chromium.org/issues/40087415) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>Omnibox, UI>GFX, UI>Internationalization |
| **Platforms** | Mac |
| **CVE IDs** | CVE-2017-7763 |
| **Reporter** | mi...@bentkowski.info |
| **Assignee** | rs...@chromium.org |
| **Created** | 2017-04-21 |
| **Bounty** | $2,000.00 |

## Description

The character U+0F8C (TIBETAN SIGN INVERTED MCHU CAN) when used in a domain name in Chrome looks just like a space.

This can be abused to spoof a legitimate domain followed by a chain of the character, e.g. "accounts.google.com<U+0F8C x 52>.bntk.pl".

I have created a domain https://important-domain.google.xn--com-lumaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa.bntk.pl/ which is SSL-enabled and looks just like important-domain.google.com when your Chrome window is now wide enough to cover the whole address. The DNS limits makes it impossible to add arbitrary number of U+0F8C chars in the address bar. As a workaround, the attacker might add just a dot, hoping that the end-user will not notice it, for example: http://important-domain.google.xn--com-lumaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa.xn--cfdaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa.bntk.pl/.

I have attached a screenshot of a SSL-enabled domain using 53 U+0F8C characters.


## Attachments

- [uf8c-demo.png](attachments/uf8c-demo.png) (image/png, 54.3 KB)
- [crbug_714196_win.png](attachments/crbug_714196_win.png) (image/png, 10.4 KB)
- [crbug_714196_linux.png](attachments/crbug_714196_linux.png) (image/png, 16.6 KB)
- [safari_editing.png](attachments/safari_editing.png) (image/png, 28.2 KB)
- [safari_committed.png](attachments/safari_committed.png) (image/png, 25.6 KB)
- [mac_views.png](attachments/mac_views.png) (image/png, 139.2 KB)

## Timeline

### me...@chromium.org (2017-04-21)

Thanks for the report. This seems Mac specific, as I'm seeing proper rendering of U+0F8C on Linux and Windows. I'm tentatively assigning severity-medium, but the fact that the attack relies on the omnibox being narrow could make this low severity as well.

jshin: Can you please take a look?

[Monorail components: UI>Browser>Omnibox UI>Internationalization UI>Security>UrlFormatting]

### js...@chromium.org (2017-04-21)

Hmmm... Indeed, it's Mac-specific.  I wonder why Mac omnibox does not use Mac's last resort font if it can't find any font covering U+0F8C. It's an "gfx" bug on Mac to render U+0F8C as a space. 

BTW, U+0F8C is allowed as an 'Identifier' (https://goo.gl/x0uHF4 : unicode.org unicode set utility is buggy in saying that it's not allowed. The canonical source is http://unicode.org/Public/security/9.0.0/IdentifierStatus.txt which has this line:

0F8C..0F8F    ; Allowed    # 6.0   [4] TIBETAN SIGN INVERTED MCHU CAN..TIBETAN SUBJOINED SIGN INVERTED MCHU CAN




[Monorail components: UI>GFX]

### js...@chromium.org (2017-04-21)

Not knowing who works on the text rendering part of GFX in the UI these days, adding a few people who might know. 

### ta...@chromium.org (2017-04-22)

I think this rendering is largely up to AppKit. There might be a workaround we can do in OmniboxViewMac::ApplyTextAttributes() https://cs.chromium.org/chromium/src/chrome/browser/ui/cocoa/omnibox/omnibox_view_mac.mm?q=OmniboxViewMac::ApplyTextAttributes+package:%5Echromium$&l=584

the status bubble also renders spaces, and so do other NSTextFields.

Safari renders spaces when editing, but drops back to rendering 'aaaa' when the URL is committed.

MacViews uses a (kinda ugly) "missing glyph" character.

### sh...@chromium.org (2017-04-22)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-04-22)

[Empty comment from Monorail migration]

### me...@google.com (2017-04-25)

rsesek, mgiuca: Any thoughts? Can you suggest an owner for this bug?

### pa...@chromium.org (2017-04-25)

tapted, is Views going to be the default on Mac any time soon? Maybe that will fix the fallback-font aspect of this bug?

The remaining part seems to be about what happens when the window isn't wide enough, in which case we should be following https://www.chromium.org/Home/chromium-security/enamel#TOC-Eliding-Origin-Names-And-Hostnames. It seems like we're not?

How does iOS behave given this domain name?

### rs...@chromium.org (2017-04-25)

Views won't be replacing this part of the browser any time soon, no.

Maybe sdy@ could help look at this? Also +shrike as TL for Mac.

### sh...@chromium.org (2017-04-26)

Hello lgrey@ - can you take a look at this important security bug?


### lg...@chromium.org (2017-04-26)

Looks like iOS correctly displays a "missing glyph" box. I think the root cause is a font bug in macOS (as in: the glyph is "there" but has no data.) 

Safari doesn't decode the Punycode in this case, but I'm not sure how they know not to. https://github.com/google/nomulus/blob/master/java/google/registry/idn/Tibetan-IDN.txt suggests this character may not be allowed in a domain, so maybe they maintain a whitelist like this?

palmer@ would eliding from the left be a sufficient fix for this? 

We could also try substituting this code point's glyph to the "missing" glyph manually as well, but I think U+0F8{D,E,F}/U+0F8{9,A} would have the same issue, sticking just to Tibetan script, so I would imagine there's more out there.

### rs...@chromium.org (2017-04-26)

Safari is falling back to Punycode for display of the committed URL, so why doesn't Chrome do that in this case? If I copy the URL displayed in the Omnibox on Mac, I get the Punycode-encoded domain, so why aren't we using that for display as well?

Re: #11: No, I don't think eliding from the left to be sufficient, because we always want to display the origin. With left-elide, a really long URL would have only the tail of the path be visible.

### el...@chromium.org (2017-04-26)

Re #11/#12: Isn't https://crbug.com/chromium/714196#c2 noting that the IDN rules allow this display of this character? Our IDNSpoofChecker::SetAllowedUnicodeSet function does tactically block a few more characters, but U+0F8C doesn't seem to meet the same criteria insofar as there's nothing "wrong" with the character, but just the font.

Safari appears to use a script whitelisting approach; even using other Tibetan characters and setting the OS language to Tibetan doesn't seem to allow rendering in Unicode.

Chrome always copies urls in punycoded form (presumably for interop with other applications).

### rs...@chromium.org (2017-04-26)

lgrey@ found that in RFC 5892 that the point is "reserved"/UNASSIGNED, but that pre-dates this character's introduction into Unicode by a few months.

The problem is indeed with the font: the glyph exists in the font but it renders blank. We may just have to blacklist these points on Mac, since the glyph isn't technically missing. Then we have to hope other characters don't have this same issue...

### sh...@chromium.org (2017-04-27)

From https://en.wikipedia.org/wiki/Tibetan_(Unicode_block), which lgrey@ pointed me at yesterday, it seems like there are probably several other characters rendering blank.

### rs...@chromium.org (2017-04-27)

Just another datapoint, it doesn't appear that Tibetan is on the list of supported languages for the default system font (via CTFontCopySupportedLanguages). Tested this in Python:

>>> import CoreText as CT
>>> import AppKit
>>> font = AppKit.NSFont.systemFontOfSize_(0)
>>> font
".AppleSystemUIFont 13.00 pt. P [] (0x7fe71b113de0) fobj=0x7fe71b113c30, spc=3.59"
>>> langs = CT.CTFontCopySupportedLanguages(font)
>>> langs.containsObject_("bo")
False
>>> langs.containsObject_("tib")
False
>>> langs.containsObject_("bod")
False

I don't know if we we should use that as a test for anything, though. Because while a font that does support Tibetan does exist on macOS:

>>> font_tib = CT.CTFontCreateWithName("Kailasa", 0, None)
>>> font_tib
"Kailasa 12.00 pt. P [] (0x7fe717e0aec0) fobj=0x7fe717e0aec0, spc=4.73"
>>> CT.CTFontCopySupportedLanguages(font_tib)
(
    bo,
    dz
)

... it also renders U+0F8C as a blank.

### lg...@chromium.org (2017-04-27)

When I paste U+0F8C into TextEdit it changes the font to "Songti SC". In character palette, it looks like all the Songti include it (but render as blank).

### rs...@chromium.org (2017-04-27)

Nor does it display in the system UI font used explicitly for Tibetan, as derived by:

>>> CT.CTFontCreateUIFontForLanguage(CT.kCTFontUIFontLabel, 0, "bo")
".SFNSText 10.00 pt. P [] (0x7fe71b129240) fobj=0x7fe71b129240, spc=2.94"

I haven't been able to find a font that can display this glyph on Mac, so I think blacklisting this series of glyphs on Mac is probably the right way to go.

jshin: WDYT?

### js...@chromium.org (2017-04-29)

Well, the character in question is rendered like 'space' even in HTML because one of Chinese fonts on Mac makes a false claim that it supports the character but has just an  blank glyph for that. 

This should be reported to Apple. It's a bug in that Chinese font. 

### js...@chromium.org (2017-04-29)

See https://www.compart.com/en/unicode/U+0F8C  and inspect where that character is supposed to be with DOM inspector. 'Kaiti SC' claims that it supports the character, but it does not. There are other Chinese fonts (Mac OS bundled fonts) that made the same false claim. 



### js...@chromium.org (2017-04-29)

> because one of Chinese fonts on Mac makes a false claim that it supports the character but has just an  blank glyph for that. 


There are more than one broken Chinese fonts making that false claim. Perhaps, need to examine other fonts as well to see if how many characters are falsely claimed to be supported by those fonts. 

### lg...@chromium.org (2017-05-01)

Filed rdar://31914563 with Apple.

Can we still do something on our end to mitigate this?

### es...@chromium.org (2017-05-03)

Friendly ping. Since it's security fix-it week, is there anything we can do in Chrome to address this? (Blacklisting as rsesek suggested in https://crbug.com/chromium/714196#c18?)

If there's nothing that can be done in Chrome, perhaps we should change this to Status=ExternalDependency.

### mi...@bentkowski.info (2017-05-03)

Just for the record: I've reported the same issue to Mozilla and, apart from reporting the bug to Apple as well, they decided to blacklist the offending characters.

This seems a sane approach for me since we don't really know how long it's going to take Apple to fix it while the blacklisting could be done right away.


### rs...@chromium.org (2017-05-03)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-05-03)

Hello rsesek@,

lgrey@ believes there are other characters that are rendered blank - can you check with him (if you haven't already) so that they are all blacklisted?


### rs...@chromium.org (2017-05-03)

Re: #24: Thanks for the additional information. We've also reported it to Apple (in #22) and will blacklist the codepoint in Chrome.

Re: #26: Yes, I have been working with lgrey@ on this. I was worried about the "known unknowns" problem, so I wrote a small program to iterate over all the Unicode characters between (0x0000,0xFFFF) in the default system font, drawing each to find any that rendered blank. From that set, I dropped anything whose Unicode character name contains the following substrings:

empty_chars \
    .pipe(drop_if_contains('<control>')) \
    .pipe(drop_if_contains('SPACE')) \
    .pipe(drop_if_contains('INVISIBLE')) \
    .pipe(drop_if_contains('ISOLATE')) \
    .pipe(drop_if_contains('LEFT-TO-RIGHT')) \
    .pipe(drop_if_contains('RIGHT-TO-LEFT')) \
    .sort_index() \
    .Name

The remaining characters that draw as blank in the system font are:

Value
00AD                                 SOFT HYPHEN
034F                   COMBINING GRAPHEME JOINER
0605                    ARABIC NUMBER MARK ABOVE
061C                          ARABIC LETTER MARK
0620                  ARABIC LETTER KASHMIRI YEH
065F                     ARABIC WAVY HAMZA BELOW
0F8C              TIBETAN SIGN INVERTED MCHU CAN
0F8D          TIBETAN SUBJOINED SIGN LCE TSA CAN
0F8E             TIBETAN SUBJOINED SIGN MCHU CAN
0F8F    TIBETAN SUBJOINED SIGN INVERTED MCHU CAN
0FD9            TIBETAN MARK LEADING MCHAN RTAGS
0FDA           TIBETAN MARK TRAILING MCHAN RTAGS
180E                   MONGOLIAN VOWEL SEPARATOR
18AA        MONGOLIAN LETTER MANCHU ALI GALI LHA
2000                                     EN QUAD
2001                                     EM QUAD
200C                       ZERO WIDTH NON-JOINER
2028                              LINE SEPARATOR
2029                         PARAGRAPH SEPARATOR
202C                  POP DIRECTIONAL FORMATTING
2060                                 WORD JOINER
2061                        FUNCTION APPLICATION
206A                  INHIBIT SYMMETRIC SWAPPING
206B                 ACTIVATE SYMMETRIC SWAPPING
206C                 INHIBIT ARABIC FORM SHAPING
206D                ACTIVATE ARABIC FORM SHAPING
206E                       NATIONAL DIGIT SHAPES
206F                        NOMINAL DIGIT SHAPES
2800                       BRAILLE PATTERN BLANK
3164                               HANGUL FILLER
A4A2                              YI RADICAL ZUP
A4A3                              YI RADICAL CYT
A4B4                             YI RADICAL NZUP
A4C1                              YI RADICAL ZUR
A4C5                             YI RADICAL NBIE

### rs...@chromium.org (2017-05-08)

From the above list of characters, the only ones that need to be explicitly blacklisted I think are the 0F8C - 0FDA range. The remainder are already handled appropriately by our IDN system.

### dr...@chromium.org (2017-05-09)

Re #27, nice work, Robert.

### bu...@chromium.org (2017-05-09)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/bccbe7c22a38f68da0c4d0bb9258060f2554e318

commit bccbe7c22a38f68da0c4d0bb9258060f2554e318
Author: rsesek <rsesek@chromium.org>
Date: Tue May 09 19:31:02 2017

Remove a small range of Tibetan characters from the allowed IDN set on Mac.

These characters do not display in the default macOS system font, despite the
font reporting that the glyphs are present.

BUG=714196

Review-Url: https://codereview.chromium.org/2865213002
Cr-Commit-Position: refs/heads/master@{#470407}

[modify] https://crrev.com/bccbe7c22a38f68da0c4d0bb9258060f2554e318/components/url_formatter/url_formatter.cc
[modify] https://crrev.com/bccbe7c22a38f68da0c4d0bb9258060f2554e318/components/url_formatter/url_formatter_unittest.cc


### rs...@chromium.org (2017-05-10)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-05-10)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-05-15)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-05-22)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-05-22)

Congratulations michal@! The VRP panel decided to award $2,000 for this report.  A member of our finance team will be in touch shortly to arrange payment.

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an established charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@chromium.org (2017-05-22)

[Empty comment from Monorail migration]

### mi...@bentkowski.info (2017-06-14)

When are you planning to release the patch in a release?

I'm asking since new Firefox has been released with exactly the same issue ( https://www.mozilla.org/en-US/security/advisories/mfsa2017-15/#CVE-2017-7763 ), which means it is now pretty easy to construct an "exploit" for Chrome basing on the patch for Firefox.


### rs...@chromium.org (2017-06-14)

This is slated for release in M60.

### js...@chromium.org (2017-06-14)

Hmm... we could have merged this to M59 branch. It's not too late. 

https://crbug.com/chromium/725660 is similar (one Arabic character  needs to be blocked on Mac). 

rsesek@: what do you think of merging to M59 branch? 

### rs...@chromium.org (2017-06-14)

It would be safe to merge, so let's ask.

### ab...@chromium.org (2017-06-14)

Since merge is safe, been in Dev for over a month, approving merge for M59. 

### bu...@chromium.org (2017-06-14)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/bf14cbf2c61544fed2d02a78a77cad0f04164e41

commit bf14cbf2c61544fed2d02a78a77cad0f04164e41
Author: Robert Sesek <rsesek@chromium.org>
Date: Wed Jun 14 19:37:32 2017

Remove a small range of Tibetan characters from the allowed IDN set on Mac.

These characters do not display in the default macOS system font, despite the
font reporting that the glyphs are present.

BUG=714196
TBR=rsesek@chromium.org

(cherry picked from commit bccbe7c22a38f68da0c4d0bb9258060f2554e318)

Review-Url: https://codereview.chromium.org/2865213002
Cr-Original-Commit-Position: refs/heads/master@{#470407}
Change-Id: I96f412f602bf035d079caa0251ce3bc0de00181d
Reviewed-on: https://chromium-review.googlesource.com/535659
Reviewed-by: Robert Sesek <rsesek@chromium.org>
Cr-Commit-Position: refs/branch-heads/3071@{#788}
Cr-Branched-From: a106f0abbf69dad349d4aaf4bcc4f5d376dd2377-refs/heads/master@{#464641}
[modify] https://crrev.com/bf14cbf2c61544fed2d02a78a77cad0f04164e41/components/url_formatter/url_formatter.cc
[modify] https://crrev.com/bf14cbf2c61544fed2d02a78a77cad0f04164e41/components/url_formatter/url_formatter_unittest.cc


### js...@chromium.org (2017-06-14)

Thanks !



### aw...@chromium.org (2017-06-15)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-06-15)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-06-15)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-08-16)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rs...@chromium.org (2017-11-15)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### me...@chromium.org (2018-11-08)

[Empty comment from Monorail migration]

### is...@google.com (2018-11-08)

This issue was migrated from crbug.com/chromium/714196?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: UI>Browser>Omnibox, UI>GFX, UI>Internationalization, UI>Security>UrlFormatting]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40087415)*
