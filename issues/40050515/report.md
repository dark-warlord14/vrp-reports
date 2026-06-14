# Security: Phishing with Unicode Domains

| Field | Value |
|-------|-------|
| **Issue ID** | [40050515](https://issues.chromium.org/issues/40050515) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Internationalization |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, iOS, ChromeOS |
| **Reporter** | tz...@gmail.com |
| **Assignee** | me...@chromium.org |
| **Created** | 2019-10-24 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**

Following the research of Xudong Zheng (spoofing аррӏе.com with cyrillic letters : <https://www.xn--80ak6aa92e.com/>)  

I've researched other spoofabable domains that can bypass Google Chrome's IDN policy (<https://www.chromium.org/developers/design-documents/idn-in-google-chrome>)  

And was able to bypass the restrictions in the policy to display a simingly popular domains (in the 10K list that are included in <https://chromium.googlesource.com/chromium/src/+/master/tools/perf/page_sets/alexa1-10000-urls.json>)  

This was done using characters from various scripts like Latin scripts, Cyrillic scripts and mixed Latin with various Asian scripts.  

I'm specifing here only the relevant characters for bypassing all of Chrome's IDN restrictions for the 10K domains, but if you're interesed,  

I'd be happy to share more characters that I've found to bypass anything BUT the 10k restriction which can be used to spoof sites that are not in that list. (I'll give one example)  

The reason that chrome displays most of these characters like that is because these characters skeleton is the character itself, as opposed to "ǧ" which is decomposed (with NFD) to "g" (0067) and a caron (030c). They mostly don't have confusables or have confusables only with specific scripts that are not Latin/Cyrillic.

**VERSION**  

Chrome Version: 78.0.3904.70 stable (Official Build) (64-bit)  

Operating System: Windows 10, version 1903, build 18362.175

**REPRODUCTION CASE**  

I've registered a few domains as a POC:  

Latin scripts:  

<https://www.xn--gogle-ita.com/> (gðogle.com)  

<https://www.xn--youtue-mza.com/> (youtuþe.com)  

<https://www.xn--rottentomats-yic.com/> (rottentomatœs.com)

but there are literally thoughtands of domains (just in the 10k list) that can be spoofed just with þ/ß/ẞ/Þ or that contains an "o" character that can be confused with "ð"  

[www.faceþook.com](http://www.face%C3%BEook.com)  

[www.facebðok.com/](http://www.faceb%C3%B0ok.com/)  

[www.ßooking.com](http://www.%C3%9Fooking.com)  

[www.ẞooking.com](http://www.%E1%BA%9Eooking.com)

here are some of the domains that can be confused with a þ/Þ/ß/ẞ:  

<http://www.facebook.com/>  

<http://www.youtube.com/>  

<http://www.tumblr.com/>  

<http://www.adobe.com/>

Here are some examples of domains that will be easier to register with a "ß", "ẞ" as the carachers seems like a capital B  

<http://baidu.com/>  

<http://www.blogger.com/>  

<http://www.booking.com/>  

<http://www.bbc.co.uk/>  

<http://www.blogspot.com/>  

<http://www.bing.com/>  

<http://www.bankofamerica.com/>  

<http://www.badoo.com/>  

<http://www.babylon.com/>

Here are all of the domain in the 10k list that can be registered with the "œ" character in order to spoof them:  

<http://rottentomatoes.com/>  

<http://www.netshoes.com.br/>  

<http://www.die-boersenformel.com/>  

<http://www.phoenix.edu/>  

<http://www.metroer.com/>  

<http://www.dasoertliche.de/>  

<http://www.bravoerotica.com/>  

<http://www.joemonster.org/>  

<http://www.boerse.bz/>  

<http://www.ricardoeletro.com.br/>  

<http://www.canoe.ca/>  

<http://www.voegol.com.br/>  

<http://www.oeeee.com/>  

<http://www.moe.gov.eg/>  

<http://www.youtube.com/user/SkyDoesMinecraft/>  

<http://www.voetbalzone.nl/>  

<http://www.oem.com.mx/>  

<http://www.bancoestado.cl/>  

<http://uplus.metroer.com/~content/>  

<http://www.poemhunter.com/>",  

<http://www.shoebuy.com/>  

<http://www.whattoexpect.com/>  

<http://www.autoevolution.com/>  

<http://www.comoeumesintoquando.tumblr.com/>  

<http://www.heroeswm.ru/>  

<http://www.noelshack.com/>  

<http://www.roem.ru/>  

<http://www.publiekeomroep.nl/>

For the Latin various scripts, here are the relevant charaters that chrome displays as is:  

þ //oofe <https://www.compart.com/en/unicode/U+00FE>  

Þ //oode <https://www.compart.com/en/unicode/U+00DE> although it's currently being registered with "p" but looks a bit like "b" in different scenarious  

ß //oodf <https://www.compart.com/en/unicode/U+00DF> actually an S and because of it isn't being detected as 'B'  

ẞ //1e9e <https://www.compart.com/en/unicode/U+1E9E> actually an S and because of it isn't being detected as 'B'  

æ //00e6 <https://www.compart.com/en/unicode/U+00E6> looks like ae  

Æ //00c6 <https://www.compart.com/en/unicode/U+00C6> looks like ae  

ð //00f0 <https://www.compart.com/en/unicode/U+00F0> looks like o  

œ //0153 <https://www.compart.com/en/unicode/U+0153> is registered as a "ce" but actually looks like "oe"  

Ə //018f <https://www.compart.com/en/unicode/U+018F> looks a bit like e or capital G switched.

The following characters will be displayed as is if the domain is NOT in the 10k list - by that i mean that if ANY of them are used with ANY characters in Latin, Chinese (Han, Bopomofo), Japanese (Kanji, Katakana, Hiragana), or Korean (Hangul, Hanja) chrome will display it as it is. (This is a partial list)  

Ŋ //014a <https://www.compart.com/en/unicode/U+014A>  

ŋ //014b <https://www.compart.com/en/unicode/U+014B>  

Œ //0152 <https://www.compart.com/en/unicode/U+0152> This is the Capital of œ (0153) which looks more like CE but just to make thinks more complete, i've added it here.  

ẹ //1EB9 <https://www.compart.com/en/unicode/U+1EB9>  

ĺ //013a <https://www.compart.com/en/unicode/U+013A>

Cyrilic scripts:  

<http://xn--80abl2d.com/> (ебау.com)

б //0431 <https://www.compart.com/en/unicode/U+0431> can be confused with "b"  

ӎ //04CE <https://www.compart.com/en/unicode/U+04CE> can be confused with "M"  

М //041C <https://www.compart.com/en/unicode/U+041C> can be confused with "M"  

ф //0444 <https://www.compart.com/en/unicode/U+0444> can be confused with "o"  

ы //044B <https://www.compart.com/en/unicode/U+044B> can be confused with "BI"

Ъ //042A <https://www.compart.com/en/unicode/U+042A> this character can be combined with other "b" like "в" or "Ь" in order for chrome to show them as it is (аӏіЬаЪа.com, ЬЪс.co.uk will be shown as it is, but ЪЪс.co.uk and аӏіЬаЬа.com, ввс.co.uk, вЬс.co.uk will be shown as punycode.

This is a partial list of characters that can be used to spoof domains that are not in the 10k list - by that i mean that if ANY of them are used with ANY characters in Cyrillic, chrome will display it as it is.  

в //0432 <https://www.compart.com/en/unicode/U+0432>  

Ь //042c <https://www.compart.com/en/unicode/U+042C>  

ҟ //049F <https://www.compart.com/en/unicode/U+049F>  

ґ //0491 <https://www.compart.com/en/unicode/U+0491>  

Ԍ //050C <https://www.compart.com/en/unicode/U+050C>  

ԍ //050D <https://www.compart.com/en/unicode/U+050D>  

т //0442 <https://www.compart.com/en/unicode/U+0442>  

п //043F <https://www.compart.com/en/unicode/U+043F>  

ӽ //04FD <https://www.compart.com/en/unicode/U+04FD>  

Ӽ //04FC <https://www.compart.com/en/unicode/U+04FC>  

ҫ //04AB <https://www.compart.com/en/unicode/U+04FC>

I've found a few other domains that are being displayed in chrome without showing the punycode:  

ԍооԍІе.com (the і seems like an l in Chrome)  

ԍффԍӏе.com  

ԍМаіІ.com (the і seems like an l in Chrome)  

ԍӎаіІ.com  

ԁґорбох.com  

ԁгорбох.com  

ԁгфрЬох.com  

іӎԁб.com  

іӎԁъ.com  

іМԁб.com  

іМԁъ.com  

аԁобе.com  

аӏібаба.com  

аӏіЬаЪа.com  

ЬЪс.co.uk  

аѕфѕ.com

Here's an example for a domain that is not in the 10K list:  

һҫӏ.com

By using the ẹ and ĺ characters, I was able to bypass also the restrictions that charome has in place even for the 10K domain list, for india, China, Japan and Taiwan TLDs.  

Obviously there are more characters, I'll be happy to provide more info.  

In these domains (cn,com.tw) it's harder to explout this as the domain owner needs to be registered as a business in the relevant countries (also apply to co.jp)

ẹ //1EB9 <https://www.compart.com/en/unicode/U+1EB9>  

ĺ //013a <https://www.compart.com/en/unicode/U+013A>

[http://www.bĺogspot.jp](http://www.b%C4%BAogspot.jp)  

[http://www.googlẹ.in](http://www.googl%E1%BA%B9.in)  

[http://www.googlẹ.com.tw](http://www.googl%E1%BA%B9.com.tw)  

[http://www.googlẹ.cn](http://www.googl%E1%BA%B9.cn)

In Hiragana, there is the letter Si, whic can resemble "L" and can be used to spoof blogspot.jp for example.  

し //3057 <https://www.compart.com/en/unicode/U+3057>  

[http://bしogspot.jp](http://b%E3%81%97ogspot.jp)

**CREDIT INFORMATION**  

Reporter credit: Tzachy Horesh

## Timeline

### jd...@chromium.org (2019-10-24)

Thanks for the report!

Rather than the Alexa list you found, we use the following domain list for spoof checks: https://cs.chromium.org/chromium/src/components/url_formatter/spoof_checks/top_domains/domains.list

Most of these characters have already been mitigated (e.g. ы,ԍ,Ԍ,т). Any that rely on capitalizing are typically considered out of scope, since they get normalized to lowercase. Further, some of these characters I don't find very convincing (e.g. ф).

There are still some bugs in here though (e.g. the faceþook example should have been fixed in crbug/798892, but reproduces for me).

reporter: can you help us by providing a single list of characters along with one example domain per character that spoofs a domain from domains.list and isn't shown in punycode?

meacer: assigning to you by default, but I'm happy to take it if you'd prefer.

[Monorail components: UI>Internationalization UI>Security>UrlFormatting]

### me...@chromium.org (2019-10-24)

Quick comments:

- crbug/798892 mapped þ to p. That fixes some cases such as wikiþedia.org but obviously doesn't help faceþook. This is a known issue (https://crbug.com/chromium/904327). At the time I considered restricting the character to Iceland's ccTLD (.is) which is documented in https://crbug.com/chromium/1017707#c2 of that bug.

- I agree with ф not being convincing. A better spoof can be made by replacing o with 0.

- Some of the spoofs are convincing, so I think we need some action there (e.g. ЬЪс.co.uk).

- https://crbug.com/chromium/770709 covers Latin characters with dots such as ẹ, but we really should do better here. 

I'll dig into the examples here and split them into separate bugs when needed.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-10-25)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/cc0bbcbe7c986094da8e58c37a21fdd179b686b0

commit cc0bbcbe7c986094da8e58c37a21fdd179b686b0
Author: meacer <meacer@chromium.org>
Date: Fri Oct 25 01:09:31 2019

Restrict Latin Small Letter Thorn (U+00FE) to Icelandic domains

This character (þ) can be confused with both b and p when used in a domain
name. IDN spoof checker doesn't have a good way of flagging a character as
confusable with multiple characters, so it can't catch spoofs containing
this character. As a practical fix, this CL restricts this character to
domains under Iceland's ccTLD (.is). With this change, a domain name containing
"þ" with a non-.is TLD will be displayed in punycode in the UI.

This change affects less than 10 real world domains with limited popularity.

Bug: 798892, 843352, 904327, 1017707
Change-Id: Ib07190dcde406bf62ce4413688a4fb4859a51030
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1879992
Commit-Queue: Mustafa Emre Acer <meacer@chromium.org>
Reviewed-by: Christopher Thompson <cthomp@chromium.org>
Cr-Commit-Position: refs/heads/master@{#709309}

[modify] https://crrev.com/cc0bbcbe7c986094da8e58c37a21fdd179b686b0/components/url_formatter/spoof_checks/idn_spoof_checker.cc
[modify] https://crrev.com/cc0bbcbe7c986094da8e58c37a21fdd179b686b0/components/url_formatter/spoof_checks/idn_spoof_checker.h
[modify] https://crrev.com/cc0bbcbe7c986094da8e58c37a21fdd179b686b0/components/url_formatter/url_formatter.cc


### sh...@chromium.org (2019-10-25)

[Empty comment from Monorail migration]

### tz...@gmail.com (2019-10-25)

Hi, I've marked each character to a domain in the domain.list file. I also note a mistake of mine for the letters  ӎ , М. 
Also, I was wondering what is the expected behaviour of chrome for a domain not in that list? as hcl.com can be spoofed for һҫӏ.com even though it won't happen if hcl.com was in the domain.list file.

Latin Scripts:faceþook.com (facebook.com) , þookmyshow.com (bookmyshow.com)
þ	//oofe https://www.compart.com/en/unicode/U+00FEdropÞox.com (dropbox.com)
Þ	//oode https://www.compart.com/en/unicode/U+00DE although it's currently being registered with "p" but looks a bit like "b" in different scenariousßooking.com   (booking.com)
ß 	//oodf https://www.compart.com/en/unicode/U+00DF actually an S and because of it isn't being detected as 'B'ẞooking.com   (booking.com)
ẞ 	//1e9e https://www.compart.com/en/unicode/U+1E9E actually an S and because of it isn't being detected as 'B'æmps.es (aemps.es) , (oncinema.com (aeoncinema.com) æ 	//00e6 https://www.compart.com/en/unicode/U+00E6 looks like aeÆoncinema.com (aeoncinema.com)
Æ 	//00c6 https://www.compart.com/en/unicode/U+00C6 looks like aegðogle.com  (google.com)
ð	//00f0 https://www.compart.com/en/unicode/U+00F0 looks like o rottentomatœs.com  (rottentomatoes.com)
œ 	//0153 https://www.compart.com/en/unicode/U+0153 is registered as a "ce" but actually looks like "oe"http://businessinsidƏr.com , http://Əksisozluk.com  (eksisozluk.com)Ə	//018f https://www.compart.com/en/unicode/U+018F looks a bit like e or capital G switched.  

Cyrillic Script:ебау.com (ebay.com)
б 	//0431 https://www.compart.com/en/unicode/U+0431 can be confused with "b"ф	//0444 https://www.compart.com/en/unicode/U+0444 can be confused with "o"Ыпԍ.com
ы	//044B https://www.compart.com/en/unicode/U+044B can be confused with "BI"
іӎԁЪ.com , іМԁЪ.com
Ъ	//042A https://www.compart.com/en/unicode/U+042A this character can be combined with other "b" like "в" or "Ь" in order for chrome to show them as it is (аӏіЬаЪа.com, ЬЪс.co.uk will be shown as it is, but ЪЪс.co.uk and аӏіЬаЬа.com, ввс.co.uk, вЬс.co.uk will be shown as punycode.  


Hiragana Script: 
beしcy.jp    (belcy.jp)
し	//3057 https://www.compart.com/en/unicode/U+3057 
The ӎ , М  example was an error on my part as chrome does show punycode for the domains in the "domains.list" file.ӎ	//04CE https://www.compart.com/en/unicode/U+04CE can be confused with "M"
М	//041C https://www.compart.com/en/unicode/U+041C can be confused with "M"

### me...@chromium.org (2019-10-25)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-10-25)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/1e9a4a24b50d0eda7ff0b2c9502756474f3ed4a9

commit 1e9a4a24b50d0eda7ff0b2c9502756474f3ed4a9
Author: meacer <meacer@chromium.org>
Date: Fri Oct 25 19:29:59 2019

Restrict Latin Small Letter Eth (U+00F0) to Icelandic domains

crrev.com/c/1879992 restricted Latin Small Letter Thorn to Icelandic
domains. This CL does the same for Eth (ð) as it can be confused with
the characters "o" and "d" in some fonts.

This change affects less than 10 real world domains with limited popularity.

Bug: 1017707, 929711
Change-Id: I037054530feb1d34e9243ef5da35cf431f3b80b5
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1881344
Reviewed-by: Christopher Thompson <cthomp@chromium.org>
Commit-Queue: Mustafa Emre Acer <meacer@chromium.org>
Cr-Commit-Position: refs/heads/master@{#709580}

[modify] https://crrev.com/1e9a4a24b50d0eda7ff0b2c9502756474f3ed4a9/components/url_formatter/spoof_checks/idn_spoof_checker.cc
[modify] https://crrev.com/1e9a4a24b50d0eda7ff0b2c9502756474f3ed4a9/components/url_formatter/spoof_checks/idn_spoof_checker.h
[modify] https://crrev.com/1e9a4a24b50d0eda7ff0b2c9502756474f3ed4a9/components/url_formatter/spoof_checks/idn_spoof_checker_unittest.cc


### tz...@gmail.com (2019-10-27)

[Comment Deleted]

### tz...@gmail.com (2019-10-27)

Hi,
I'm adding a few more issues for the Greek script:
I've marked each character to a domain in the domain.list file.

Greek Scripts:
http://βββ.org (bbb.org)
β   //03B2 https://www.compart.com/en/unicode/U+03B2
http://αμ.com
μ //03BC https://www.compart.com/en/unicode/U+03BC
http://υη.org (un.org)
η //03B7 https://www.compart.com/en/unicode/U+03B7
http://αττ.com (att.com), http://οττο.de (otto.de)
τ //03C4 https://www.compart.com/en/unicode/U+03C4
http://ιεεε.org (ieee.com), http://ωωε.com (wwe.com)
ε	//03B5 https://www.compart.com/en/unicode/U+03B5

Also, I noticed you fixed 3 Greek letters that make it confusables to their look a like in ASCII (Chrome 77 didn't catch those and 78 is catching them, is that correct?
υ
κ
ο


Lastly, I wanted to ask what is your stand about links that seem to be legitimate but obviously aren't, like:
http://ΕΒΑΥ.COM
http://ΗΡ.COM 
As users will likely click on this link and get to a page that may seem like the original, in the hope (of the attacker) that this will cause them not to notice the URL.

Regards,

Tzachy

### me...@chromium.org (2019-10-31)

More detailed response.

> https://www.xn--gogle-ita.com/ (gðogle.com)
> https://www.xn--youtue-mza.com/ (youtuþe.com)
> https://www.xn--rottentomats-yic.com/ (rottentomatœs.com)

These were previously reported in 929711 (ð, U+00F0), 798892 (þ, U+00FE), 843352
(œ, U+0153). I landed fixes for ð and þ. œ is still TBD.


> www.ßooking.com

Chrome decodes ß as ss today. This may change in the future, but this is not a valid spoof as of M78.

æ: This is essentially the same issue as https://crbug.com/chromium/843352.

ŋ, ẹ: Their skeletons are correctly mapped to n and e. This means spoofing a top site shouldn't be possible because skeletons will match (e.g. biŋg.com and googlẹ.com will remain punycode). This general is covered by https://crbug.com/chromium/770709 but needs improvement.

> This is a partial list of characters that can be used to spoof domains that are not in the 10k list - by that i mean that if ANY of them are used with ANY characters in Cyrillic, chrome will display it as it is.
)
These characters have their skeletons mapped to Latin characters in IDNSpoofChecker: https://cs.chromium.org/chromium/src/components/url_formatter/spoof_checks/idn_spoof_checker.cc?rcl=a98ce1cee74f10dd86265d013678e76a0a039109&l=192

Spoofing a popular domain using them shouldn't be possible since the skeletons are going to be identical.


> I'm adding a few more issues for the Greek script: ...

The examples in your report are whole script confusables. We have https://crbug.com/chromium/722167 open for WSC in Greek and other scripts.

> Lastly, I wanted to ask what is your stand about links that seem to be legitimate but obviously aren't, like:

I think you are asking about how these URLs are displayed in the status bar at the bottom of the content area. We do not treat status bar as a security indicator so we don't consider these as spoofs: https://chromium.googlesource.com/chromium/src/+/master/docs/security/faq.md#Where-are-the-security-indicators-located-in-the-browser-window


# Summary

The remaining spoof that's not covered by an existing bug is "ə". googlə.com and əməzon.com look reasonably good spoofs so we should fix this issue.


### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-11-08)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/dd29dd4c87b17d04bfc4c98ea96affe9a3f6e7a1

commit dd29dd4c87b17d04bfc4c98ea96affe9a3f6e7a1
Author: meacer <meacer@chromium.org>
Date: Fri Nov 08 15:23:47 2019

Disallow Latin Small Letter Schwa (U+0259) for domains outside .az TLD

The letter "ə" (U+0259) can be confused with both "e" and "a" when used
in domain names. IDN spoof checker currently doesn't have a way of
treating a single character as confusable with multiple characters, so
the only option is to map this letter to either "e" or "a" but not both.
This is obviously not desirable since the Schwa can be used to spoof the
non-mapped character.

As a result, there is no straightforward solution other than limiting the
character to .az domains (The letter is used commonly in Azerbaijani
language).

This fix affects ~250 registered domains containing the letter "ə".
However, only ~40 of these domains serve some sort of content, the rest
are either parked or don't serve content. Furthermore, only 1 of these
domains appear in usage logs and the domain is not widely used, so this
is probably a safe change.

Bug: 1017707
Change-Id: Ied699b3b7bd067945d90dd360d2ecf3243912145
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1904761
Commit-Queue: Joe DeBlasio <jdeblasio@chromium.org>
Reviewed-by: Joe DeBlasio <jdeblasio@chromium.org>
Cr-Commit-Position: refs/heads/master@{#713832}

[modify] https://crrev.com/dd29dd4c87b17d04bfc4c98ea96affe9a3f6e7a1/components/url_formatter/spoof_checks/idn_spoof_checker.cc
[modify] https://crrev.com/dd29dd4c87b17d04bfc4c98ea96affe9a3f6e7a1/components/url_formatter/spoof_checks/idn_spoof_checker_unittest.cc


### me...@chromium.org (2019-11-08)

Closing.

tzachyr: Please let me know if I missed anything from your original report, thanks.

### sh...@chromium.org (2019-11-09)

[Empty comment from Monorail migration]

### na...@google.com (2019-11-18)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-11-18)

Requesting merge to beta M79 because latest trunk commit (713832) appears to be after beta branch point (706915).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-11-18)

This bug requires manual review: Less than 18 days to go before AppStore submit on M79
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://goto.google.com/chrome-release-branch-merge-guidelines
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on master/ToT?
4. Why are these changes required in this milestone after branch?
5. Is this a new feature?
6. If it is a new feature, is it behind a flag using finch?

Please contact the milestone owner if you have questions.
Owners: benmason@(Android), kariahda@(iOS), cindyb@(ChromeOS), govind@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### go...@chromium.org (2019-11-18)

How is the change looking in canary so far?

+adetaylor@ (Security TPM) for M79 merge review. If merge is approved and merged latest by tomorrow, Tuesday noon, then we can pick it up for this week beta release on Wednesday. 

### ad...@chromium.org (2019-11-18)

Yep, if this is deemed to be low risk it would be great to merge to beta. The commit comment is MARVELLOUS and makes me think risks have been very carefully considered.

### go...@chromium.org (2019-11-18)

meacer@, is the change looking  good in canary and safe to merge to M79 now?

### me...@chromium.org (2019-11-18)

Yup, looks good to merge.

### go...@chromium.org (2019-11-18)

Approving merge to M79 branch 3945 based on comments #18 and #20.

### go...@chromium.org (2019-11-19)

Please merge your change to M79 branch 3945 by 12:30 PM PT, today so we can pick it up for tomorrow's beta release. Thank you.

### me...@chromium.org (2019-11-19)

This turned out to be a nontrivial merge, it depends on https://chromium.googlesource.com/chromium/src/+/b52ac904853312627c64028956731c0d8804dea8

Do we still want to merge? (I lean towards no given the complexity)

### go...@chromium.org (2019-11-19)

Rejecting merge to M79 based on #23. 

### ad...@chromium.org (2019-11-19)

Agreed, we should only merge if it's easy and low-risk. I'm sure govind@ would agree, so removing the merge label. Thanks!

### na...@google.com (2019-11-21)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2019-11-21)

Congrats! The Panel decided to reward $500  for this report!

### na...@google.com (2019-11-21)

[Empty comment from Monorail migration]

### ad...@google.com (2020-02-02)

[Empty comment from Monorail migration]

### ad...@chromium.org (2020-02-03)

[Empty comment from Monorail migration]

### ad...@chromium.org (2020-02-10)

[Empty comment from Monorail migration]

### [Deleted User] (2020-02-15)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2020-02-15)

This issue was migrated from crbug.com/chromium/1017707?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: UI>Internationalization, UI>Security>UrlFormatting]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40050515)*
