# Data extraction with XSS Auditor

| Field | Value |
|-------|-------|
| **Issue ID** | [40076978](https://issues.chromium.org/issues/40076978) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink |
| **Platforms** | Mac |
| **Reporter** | ho...@gmail.com |
| **Assignee** | ts...@chromium.org |
| **Created** | 2013-02-13 |
| **Bounty** | $500.00 |

## Description

UserAgent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.57 Safari/537.17

Steps to reproduce the problem:
with mode=block; we can detect if sent payload was found in the response body by checking location.href=='about:blank' (because it inherits parent's origin). It gives us a powerful tool for private data extraction.
1) we can see if user has
<script>admin=1
by sending #<script>admin=1
2)we can check some state for example sending
#onclick=switch_on()
or 
#onclick=switch_off()
3) same applies for http-equiv meta and javacript: links.
4) we can bruteforce some data easily and this is the most dangerous aspect. 

please check out my gist: https://gist.github.com/homakov/5f9427642f9c144a5b5b

in the PoC is used sinatra app with some private data on localhost:4567/token and i extracted it from 127.0.0.1:4567/extract. Works like a charm. In my showcase private data is pin code (6 digits)
Private data can be:
<script>var user_id=123;
<script>var csrf_token='abc123dfg';
<script>var PRELOADED={email:'homakov@gmail.com',

Yes, bruteforcing csrf token doesn't look mad - we can save state(last checked bunch) in the cookie and continue later - couple of hours and job is done. depends on its length, of course. But anyway dangerous and feasible.

Some tricks and tips to improve it
1) moving bruteforce payload generation on server side 
2) only 25 windows are allowed
3) we can use GET but most servers have limit on its size and can respond with 414. We can use POST but not all endpoints accept POST. And, we can use fragment - it's perfect because it is not sent on server side and can be very long.
4) search is case insensitive - useful to brute csrf token

code in PoC looks very ugly, sorry about that. Flow is simple:
we take bunch (25*25*25*25) of values, split them between 25 windows, put payloads in fragments, waiting for first about:blank(auditor detection) then taking detected payload, splitting between 25 again until we realize the original value. Algo can be scaled and optimized, this is just demo.

http://cl.ly/image/1m2F1J0T2L3k
http://cl.ly/image/3h0L3j1U0t3b

What is the expected behavior?
i'm not supposed to know when xss auditor blocked my payload

What went wrong?
----

Did this work before? N/A 

Chrome version: 24.0.1312.57  Channel: stable
OS Version: OS X 10.8.2

no info in public now :) responsible disclosure

## Attachments

- [TXN_รหัสอ้างอิง. 202012031BC2WFdfJLkGvq9qQ.jpg](attachments/TXN_รหัสอ้างอิง. 202012031BC2WFdfJLkGvq9qQ.jpg) (image/jpeg, 150.8 KB)

## Timeline

### ts...@chromium.org (2013-02-13)

This may force us to go with the unique origin remedy we avoided last time.

### ts...@chromium.org (2013-02-13)

BTW, I think your search is even easier than you imagine using prefixes.  Given

token='bba'

I try:

token='a
token='b, match, try token='b', fail
token='ba
token='bb, match, try token='bb', fail
token='bba, match try token='bba', win.


### ts...@chromium.org (2013-02-14)

Exploitation in the wild may be difficult; you need to have the information to siphon occur directly after the <script> tag and before any punctuation which would terminate the fragment for comparison.  

### ts...@chromium.org (2013-02-14)

Looking at it again, I don't think the prefix matching works, since we're matching the page against the URL, not the other way around.  So you do have to brute force the token, in which case it's no easier than guessing the token directly and using it.  Let me know if I'm missing something.

### ho...@gmail.com (2013-02-14)

Yes i know about this limitation. Information should be between <script> and , but this happens quite often. All examples were found in real projects. 

in the current page code.google.com: 
<script type="text/javascript">
 window.___gcfg = {lang: 'en'};

we can extract lang.

are you sure about prefixes?

### ho...@gmail.com (2013-02-14)

i don't get your point with prefixes.
Payload can be in hash/query string or post payload. it matches between <script> and first comma. 
wdyt about timing attack by the way? i despise them but how auditor's performance impacts on onload event

### ho...@gmail.com (2013-02-14)

regards bruteforcing - this is way easier. 1) you have detection if your guess was right. usually you don't know if your csrf token is ok. 2) case insensitive 3) fragment is not sent on server side and can be super long. if bruteforce generator located on server side attack can be pretty possible

### ts...@chromium.org (2013-02-14)

Ironically, this page has its own token like:

<script type="text/javascript">
 
 
 
 
 var codesite_token = "pZ...

Without the prefix trick, which turns a base^n step brute force into a base*n step brute force, I'm less interested. Otherwise, you can just iterate requests to the sever trying XSRF tokens.  The local-only attack is faster, but just a constant factor so it doesn't change the computational complexity from O(b^n) to something lower.  The severity-medium was based upon dramatically reducing the strength of a CSRF token.

If you can brute force your own token on this page, let me know.  I'd be really really interested then.

### ho...@gmail.com (2013-02-14)

It was your assumption that it will work with prefixes :)

I only told that it works fine with boolean(switch_on/off) values, predefined(admin=1) and not random user_id=123123.

>but just a constant factor so it doesn't change the computational complexity from O(b^n) to something lower
10 million times faster? Or maybe more - didn't play with fragment further. 

Case insensitive, if length is 8(tokens can be pretty short) 26^8 = 208827064576.
we can try up to 10 000 000 tokens in bunch every time(need to optimize JS and generation). 
20k requests, 25 windows every 3 seconds =  40 minutes to find bunch containing token. then search in this bunch - 30-60 seconds and token is found.

i would be more interested too, if auditor would detect partial tokens too, but no :)

### ts...@chromium.org (2013-02-14)

Ah.  If the length of the fragment isn't limited to something reasonable, then maybe that's a bug in itself.

### ts...@chromium.org (2013-02-14)

(e.g. I had presumed that you only get a handfull of tokens in the URL before you hit the maximum URL length limit).  But maybe that's not the case.

### ho...@gmail.com (2013-02-14)

fragment clearly has no limit. i just get "Aw snap" because my memory is low.
location.hash.length
1747201

check my poc - it showcases POST too, which is limited only by post_body_size on the server, usually 2-10 MB. This is enough.

### ho...@gmail.com (2013-02-16)

i think you need about:blocked page with explanation why page was blocked.
just wonder if bounty is possible for this one, but this is low-severity? I just want to publish a blog post.

### sc...@gmail.com (2013-02-16)

@homakov: we'll have a chat about possible reward after the weekend. It's true that we don't usually reward for low severity issues. I think the main reason that this is low severity is that the web site has to be vulnerable to XSS in the first place! That's a significant pre-requisite.

### ho...@gmail.com (2013-02-16)

> is that the web site has to be vulnerable to XSS in the first place
O_o really? Please read again, vulnerability is not about website, it's about Extraction information using XSS Auditor. Auditor is vulnerable and I can extract info from any website with mode=block.

### ho...@gmail.com (2013-02-16)

I think tsepez can explain it better - he understood the issue well :)

### ts...@chromium.org (2013-02-19)

@scarybeasts - no, this site doesn't need to have an XSS.  The preconditions are as follows.

1. The site must supply an 'x-xss-protection mode=block' header.
2. The site must place sensitive information in an inline <script> block.
3. The sensitive information must occur within the first 100 characters of the block.
4. The sensitive information must occur before the first comment or comma.
5. The sensitive information must be enumerable in javascript in a reasonable amount of time.
6. The site must not block you after making repeated requests for the same page rapidly in a loop (i.e. no DOS protection).

In that case, you can extract that information.

For example, this bug tracker page meets all of the above except 5 - because our CSRF token is strong.  But I could see how I might be able to extract something like a bank balance if all the stars align.

I think this meets the bar for sev medium; if it could be done reliably it would be high.

### ho...@gmail.com (2013-02-19)

@tsepez is right. 

>1. The site must supply an 'x-xss-protection mode=block' header.
this can also be the case for non blocking pages. But precondition is more complex, 
<form action="/secret_path"></form><script>forms[0].submit()</script> 
and payload is trying to guess secret_path, if guessed it submits to about:blank and we can detect it. 
Not very feasible in real world though. I just mean that we should use "about:blocked" or similar instead of parent-origin-inheriting about:blank.

>2. The site must place sensitive information in an inline <script> block.

being more specific, any script that is detectable by auditor can be extracted: on* events, "javascript:..." links and http-equiv metas. But <script> is more common to contain private data.

>6. The site must not block you after making repeated requests for the same page rapidly in a loop (i.e. no DOS protection).

yes, but it will not look like DoS for simple values/numbers - for example <script> var balance = 390625; is extractable using just 25+25+25+25=100 requests.
But for not strong csrf tokens it is harder, and requires logging of "checked" tokens because can take about an hour.

### ts...@chromium.org (2013-02-19)

[Empty comment from Monorail migration]

### jl...@chromium.org (2013-02-20)

[Empty comment from Monorail migration]

### ts...@chromium.org (2013-02-21)

Upstreamed as https://bugs.webkit.org/show_bug.cgi?id=110406

### jl...@chromium.org (2013-02-21)

[Empty comment from Monorail migration]

### ts...@chromium.org (2013-02-21)

Fixed in http://trac.webkit.org/changeset/143644.

@homakov - please hold off on public discussion until this change has made its way into a released version of chrome.  Thanks.

### ho...@gmail.com (2013-02-21)

Sure, just let me know when I can post about it.

### ho...@gmail.com (2013-02-26)

To keep my ratio vulns / month i would like to publish it in early march, is it possible? :)

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### ho...@gmail.com (2013-03-14)

just wonder, no bounty right, and can i publish details?
thx

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-05)

[Empty comment from Monorail migration]

### js...@chromium.org (2013-04-11)

Bulk edit for SecurityNotify.

### sc...@gmail.com (2013-05-03)

@homakov: thanks for all your interesting research into the XSS Auditor. This particular bug earns a $500 Chromium Security Reward :D
[I think the fix didn't go out with Chrome 26, but should with the upcoming Chrome 27, we'll credit you in that release]

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties.
*********************************

### ho...@gmail.com (2013-05-03)

interesting, you know how to get in touch: homakov@gmail.com

P.s. consider fixing this too http://homakov.blogspot.ru/2013/03/pwning-your-privacy-in-all-browsers.html ;)

### sc...@gmail.com (2013-05-17)

[Empty comment from Monorail migration]

### ho...@gmail.com (2013-05-26)

version 27 is out! How can I get the bounty?

### pa...@chromium.org (2013-05-28)

[Empty comment from Monorail migration]

### ho...@gmail.com (2013-06-21)

bуmp

### pa...@chromium.org (2013-06-24)

[Empty comment from Monorail migration]

### ho...@gmail.com (2013-08-19)

>Labels: -reward-inprocess 


what does "inprocess" particularly mean? :) Is it wire transfer?

### js...@chromium.org (2013-11-18)

Bulk release of old security bug reports.


### sh...@chromium.org (2016-06-14)

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

### ch...@gmail.com (2020-12-03)

[Empty comment from Monorail migration]

### is...@google.com (2020-12-03)

This issue was migrated from crbug.com/chromium/176137?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40076978)*
