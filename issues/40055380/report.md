# Security: Site isolation break because of double fetch of shared buffer

| Field | Value |
|-------|-------|
| **Issue ID** | [40055380](https://issues.chromium.org/issues/40055380) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript>Runtime, Internals>Network>Cache, Internals>Sandbox>SiteIsolation |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | hi...@gmail.com |
| **Assignee** | bb...@chromium.org |
| **Created** | 2021-03-30 |
| **Bounty** | $15,000.00 |

## Description

in the function GeneratedCodeCache::WriteEntry, the buffer |data| is passed from renderer process, the function calculate the hash |checksum_key|
firstly and then write the buffer to code cache backing store. if renderer modify the content of the buffer between calculation and write. the
checksum_key will mismatch with the content. so checksum_key can be mapped to any content.

so an compromised renderer process can create an entry, whoes checksum_key will be used by a victim site, and the content of the code cache can be controlled by the compromised renderer process.
when the victim site load the code cache, any malicous code can be injected into the victim site, breaking the site isolation.

void GeneratedCodeCache::WriteEntry(const GURL& url,
                                    const GURL& origin_lock,
                                    const base::Time& response_time,
                                    mojo_base::BigBuffer data) {
  if (backend_state_ == kFailed) {
    // Silently fail the request.
    CollectStatistics(CacheEntryStatus::kError);
    return;
  }

  // Reject buffers that are large enough to cause overflow problems.
  if (data.size() >= std::numeric_limits<int32_t>::max())
    return;

  scoped_refptr<net::IOBufferWithSize> small_buffer;
  scoped_refptr<BigIOBuffer> large_buffer;
  uint32_t data_size = static_cast<uint32_t>(data.size());
  // We have three different cache entry layouts, depending on data size.
  if (data_size <= kSmallDataLimit) {
    // 1. Small
    // [stream0] response time, size, data
    // [stream1] <empty>
    small_buffer = base::MakeRefCounted<net::IOBufferWithSize>(
        kHeaderSizeInBytes + data.size());
    // Copy |data| into the small buffer.
    memcpy(small_buffer->data() + kHeaderSizeInBytes, data.data(), data.size());
    // Write 0 bytes and truncate stream 1 to clear any stale data.
    large_buffer = base::MakeRefCounted<BigIOBuffer>(mojo_base::BigBuffer());
  } else if (data_size <= GetLargeDataLimit()) {
    // 2. Large
    // [stream0] response time, size
    // [stream1] data
    small_buffer =
        base::MakeRefCounted<net::IOBufferWithSize>(kHeaderSizeInBytes);
    large_buffer = base::MakeRefCounted<BigIOBuffer>(std::move(data));
  } else {
    // 3. Very Large
    // [stream0] response time, size, checksum
    // [stream1] <empty>
    // [stream0 (checksum key entry)] <empty>
    // [stream1 (checksum key entry)] data
    uint8_t result[crypto::kSHA256Length];
    crypto::SHA256HashString(
        base::StringPiece(reinterpret_cast<char*>(data.data()), data.size()),
        result, base::size(result));                                             ######calculate hash here
    std::string checksum_key = base::HexEncode(result, base::size(result));
    small_buffer = base::MakeRefCounted<net::IOBufferWithSize>(
        kHeaderSizeInBytes + kSHAKeySizeInBytes);
    // Copy |checksum_key| into the small buffer.
    DCHECK_EQ(kSHAKeySizeInBytes, checksum_key.length());
    memcpy(small_buffer->data() + kHeaderSizeInBytes, checksum_key.data(),
           kSHAKeySizeInBytes);
    // Write 0 bytes and truncate stream 1 to clear any stale data.
    large_buffer = base::MakeRefCounted<BigIOBuffer>(mojo_base::BigBuffer());

    // Issue another write operation for the code, with the checksum as the key
    // and nothing in the header.
    auto small_buffer2 = base::MakeRefCounted<net::IOBufferWithSize>(0);
    auto large_buffer2 = base::MakeRefCounted<BigIOBuffer>(std::move(data));
    auto op2 = std::make_unique<PendingOperation>(Operation::kWriteWithSHAKey,
                                                  checksum_key, small_buffer2,
                                                  large_buffer2);
    EnqueueOperation(std::move(op2));                                           ##########write will occure in this function
  }
  WriteCommonDataHeader(small_buffer, response_time, data_size);

  // Create the write operation.
  std::string key = GetCacheKey(url, origin_lock);
  auto op = std::make_unique<PendingOperation>(Operation::kWrite, key,
                                               small_buffer, large_buffer);
  EnqueueOperation(std::move(op));
}

reproduce steps:
1. apply the following patch to you branch, rebuild it as a release build
```
diff --git a/content/browser/code_cache/generated_code_cache.cc b/content/browser/code_cache/generated_code_cache.cc
index 69d1f926f3e8..86a87dc66cda 100644
--- a/content/browser/code_cache/generated_code_cache.cc
+++ b/content/browser/code_cache/generated_code_cache.cc
@@ -391,6 +391,7 @@ void GeneratedCodeCache::WriteEntry(const GURL& url,
     std::string checksum_key = base::HexEncode(result, base::size(result));
     small_buffer = base::MakeRefCounted<net::IOBufferWithSize>(
         kHeaderSizeInBytes + kSHAKeySizeInBytes);
+    sleep(2);
     // Copy |checksum_key| into the small buffer.
     DCHECK_EQ(kSHAKeySizeInBytes, checksum_key.length());
     memcpy(small_buffer->data() + kHeaderSizeInBytes, checksum_key.data(),
@@ -406,6 +407,10 @@ void GeneratedCodeCache::WriteEntry(const GURL& url,
                                                   checksum_key, small_buffer2,
                                                   large_buffer2);
```
2. unzip the attached poc.tar to the build directory such as out/Release
3. start a webserver in out/Release, assure we can access the attacker.html by the address http://127.0.0.2:8000/attacker.html
4. launch browser by the command "./chrome-wrapper --user-data-dir=tmp --enable-blink-features=MojoJS http://127.0.0.2:8000/attacker.html"
5. the poc will will run about in 10 second, it'll alert "aaaaaaaaaaaaa" two times, and after "bbbbbbbbbbbb" one time because the code cache is modified.


## Attachments

- [poc.tar](attachments/poc.tar) (application/octet-stream, 6.3 MB)
- [demo.gif](attachments/demo.gif) (image/gif, 185.5 KB)
- [site isolation.png](attachments/site isolation.png) (image/png, 42.2 KB)
- [attacker.html](attachments/attacker.html) (text/plain, 2.1 KB)
- [victim.html](attachments/victim.html) (text/plain, 185 B)
- [cached.js](attachments/cached.js) (text/plain, 73.8 KB)
- [cachearray.js](attachments/cachearray.js) (text/plain, 456.7 KB)

## Timeline

### [Deleted User] (2021-03-30)

[Empty comment from Monorail migration]

### dr...@chromium.org (2021-03-31)

[Empty comment from Monorail migration]

### dr...@chromium.org (2021-03-31)

Since the GeneratedCodeCache also keys based on the origin requesting the resource, it seems like this is limited to one page within an origin attacking another. Assigning low severity since this seems to require both a compromised renderer and a very tight race condition.

Unfortunately there's no owners on the code cache itself, so triaging to top-level content/ OWNERs.

### hi...@gmail.com (2021-04-01)

@drubery I think you misunderstood the attack scenario, an original can attack another origin, in my poc, attacker is in 127.0.0.2, victim is in 127.0.0.1. and only the attacker require a compromised renderer, actually the race is not tight because there may be  other operations the write operations, it's easy to achieve this, I add a sleep patch just for you to quickly understand and reproduce, please re-review it, thanks 

### hi...@gmail.com (2021-04-01)

Add a demo,  the demo shows the attacker is in  the origin 127.0.0.2,  the victim's origin is 127.0.0.1(refer to the alert dialog and the src of the iframe), the victim page is just a normal page, it doesn't call any mojo related function(doesn't require a compromised renderer).

### hi...@gmail.com (2021-04-01)

From the attached picture, you can see 127.0.0.2 and 127.0.0.1 are in different process, site isolation is enabled.

### [Deleted User] (2021-04-01)

Setting Pri-2 to match security severity Low. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### cr...@chromium.org (2021-04-02)

Thanks for the report!

To be clear, the GeneratedCodeCache is meant to only allow a process to write entries that are readable from its own origin_lock (which can be enforced at the site boundary).  Your description seems to talk about a time-of-check-to-time-of-use (i.e., double fetch) bug with the checksum, but I don't see how that would allow a different origin to read the compromised results.  Can you say more about how your PoC causes 127.0.0.1 to read from 127.0.0.2's code cache?  That would help us understand the severity, which might need to be raised.

(It's also worth confirming whether it's specific to 127.0.0.* as a special case or if it applies to non-local cases as well.)

I haven't looked into the PoC yet, but I'm CC'ing mythria@, who worked on the Site Isolation support for GeneratedCodeCache in https://crbug.com/chromium/812168.

[Monorail components: Blink>JavaScript>Runtime Internals>Network>Cache Internals>Sandbox>SiteIsolation]

### cr...@chromium.org (2021-04-02)

To help others quickly triage the report, here's what looks like the relevant parts of the PoC.  The rest of the attached file appears to be generated MojoJS files; not sure if there's anything relevant to look at in there.

### hi...@gmail.com (2021-04-02)

[Comment Deleted]

### hi...@gmail.com (2021-04-02)

If the code cache is small, it stores the cache in the form as following
key = "_key$url \n$site"
value = the content of code cache
If the code cache is very large(larger than |GetLargeDataLimit()|), it stores the cache in two levels, in the form as following
first_level_key = "_key$url \n$site"
first_level_value = the hash string of the code cache
second_level_key = the hash string of the code cache
second_level_value = the content of code cache

GeneratedCodeCache only ensure isolating small cache from each other, if the cache code is large and the content of code cache is the same, it'll use the same entry

### cr...@chromium.org (2021-04-02)

Oh!  If the origin keying of the code cache is not respected for large cache entries, that would be a security issue.  mythria@, can you take a closer look and confirm if that's a bypass?  I'll tentatively raise this to High severity in case that's correct.  Thanks for the extra info!

### [Deleted User] (2021-04-02)

Setting milestone and target because of Security_Impact=Stable and high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### my...@chromium.org (2021-04-06)

Right, we de-duplicate very large entries by using SHA-256 hash of contents. So indeed two origins could share the same data as long as the content is the same. It is also possible to change the contents in such a way that the SHA-256 hash still remains the same. I thought this was highly unlikely and hence safe to use SHA-256 hash to de-duplicate the entries. 

+bbudge@ who actually implemented this. 

### my...@chromium.org (2021-04-06)

From the PoC this seems to be the code to change the contents and fix up the hash to look the same:

for (var i = 0; i < 200; i++)
      //modify long string
       u8[u8.length - 14 * 16 - 2 - i] = 98;
 //fix hash
 u8[28] = 0x15;
 u8[29] = 0xff;
 u8[30] = 0x2a;
 u8[31] = 0xb3;

The original string had a long string of a's. This modifies few of them to b's and fixes up the hash. 

### my...@chromium.org (2021-04-06)

palmer@ / creis@ / bbudge@,  We use SHA-256 hashes to de-duplicate code cache entries. I suppose it is possible of the attacker to change the contents in such a way that the hash still remains the same. Do you think SHA-256 hash isn't sufficient here? Are there any other stronger hashes we could compute here?  

For the context:
Here's the cl that introduced de-duplication: https://chromium-review.googlesource.com/c/chromium/src/+/1846102
Here's the design doc: https://docs.google.com/document/d/1SCH15oCFJW55jsTJZ0T7XAQIZVryI_IJOIENyL_q4n4/edit

### my...@chromium.org (2021-04-06)

I think this feature isn't enabled by default yet. It is being finched on all channels though. If this is a serious enough security concern it should be possible to pause this experiment too. Since this has larger impact for WASM than javascript code caches I will let Bill take the decision there.

### hi...@gmail.com (2021-04-06)

I think the root cause is the TOCTOU issue, it's reasonable that two identical code cache share the same entry.

### my...@chromium.org (2021-04-06)

I am sorry, I misunderstood the problem then. So it isn't the hash key being the same for different contents then? It is that we are able to change the contents of the code after the hash is computed?

I am still unclear how that is happening. We use mojo::Bigbuffer to send data from renderer to the browser. In my understanding renderer wouldn't be able to update the data. I will take a closer look at the PoC to understand what's happening there. 

### bb...@chromium.org (2021-04-06)

If the compromised renderer is modifying the shared memory of the Mojo::BigBuffer there are two problems:

1) While the browser process is computing the checksum and writing the cached entry. This seems extremely difficult to get the timing right. We could fix this by copying the data in the browser process before computing the checksum, with very little impact on performance.

2) While the browser process is fetching from the cache. This would allow the compromised renderer to get compiled code for some other resource/origin. This seems harmless, since the renderer is already compromised.

Re #17 the Finch experiment is only adjusting the double-key threshold, so we can't directly turn it off. If Finch can push a very large threshold though, we could effectively make it never de-duplicate entries.

I will check out the PoC now.

### my...@chromium.org (2021-04-06)

I looked at the PoC more closely. We create a big buffer with shared memory and use mojo JS interface to send that data over. Since we still have access to buffer, this data could be modified, after the computation of the key thus installing the modified content which the victim will then retrieve. For proof of concept, the patch changes the generated code cache implementation to sleep right after the computation of key, and we modify the content in a timeout handler. I believe this could happen even without the sleep as long as render process has access to the mojo::BigBuffer. I am not that familiar with mojo::BigBuffer. I am a bit unsure if this is indeed an issue even when we don't use mojo js bindings. 

So the real issue here I think is if renderer is able to modify the contents of mojo::BigBuffer after requesting a write we could potentially corrupt the cached code.  We still need a way to reliably change the contents after the computation of key on the browser side but before the contents are written but is possible. Without de-duplication this wouldn't be a security concern since they wouldn't be reused across origins. With de-duplication we could potentially reuse across origins and hence becomes a security issue.

Please disregard my comments about SHA-256 hash in https://crbug.com/chromium/1194046#c16. My understanding wasn't correct then. If we indeed can change contents, any hash could cause the same problems.

higongguang@, Please let me know if my understanding is correct this time.
 
The thing I am still unclear though is  if it is really possible for renderer to update the contents of mojo::BigBuffer after it has requested a code cache write. As far as I understand, we do transfer the ownership of shared memory to the big buffer. I am not fully sure if we can update it from renderer process. 

kinuko/bbudge, Do you know if this is possible? If yes, then should we copy the data for renderer-browser boundary? 

### bb...@chromium.org (2021-04-06)

Looking at the attacker.html, it looks like the JS is directly storing something in the generated code cache. That seems bad and I didn't realize we expose this. The code is near the top of the file:

        this.ptr = new blink.mojom.CodeCacheHostPtr;
        Mojo.bindInterface(blink.mojom.CodeCacheHost.name, mojo.makeRequest(ptr).handle, "process");
        var shareBuffer = Mojo.createSharedBuffer(cached_array.length);
        var view = shareBuffer.handle.mapBuffer(0, cached_array.length);
        console.log(view);
        var u8 = new Uint8Array(view.buffer);
        for (var i = 0; i < u8.length; i++)
            u8[i] = cached_array[i];
        bigBuffer = new mojoBase.mojom.BigBuffer({ sharedMemory: new mojoBase.mojom.BigBufferSharedMemoryRegion({ bufferHandle: shareBuffer.handle, size: cached_array.length }) });

        ptr.didGenerateCacheableMetadata(blink.mojom.CodeCacheType.kJavascript, new url.mojom.Url({ url: "http://127.0.0.1:8000/cached.js" }), new mojoBase.mojom.Time, bigBuffer);


### my...@chromium.org (2021-04-06)

I was under the impression that that is a feature which is disabled by default and is used for tests etc., I am not sure if it is intended for production use. I am not 100% sure there though.

### bb...@chromium.org (2021-04-06)

On further thought it's a PoC, to demonstrate the possibility without actually having a compromised renderer. So the vulnerability is still there.

### bb...@chromium.org (2021-04-06)

Adding rockot@ for Mojo::BigBuffer expertise.

### na...@chromium.org (2021-04-06)

Enabling MojoJS to demonstrate a security bug is fine by me. It indeed makes the work of simulating an exploited renderer a lot easier. Our assumption is that a compromised renderer can execute arbitrary code and can even enable MojoJS itself.

If we are reading the buffer contents after we have computed the key, then it is indeed a time-of-check-time-of-use bug (TOCTOU) and we should fix this.

### bb...@chromium.org (2021-04-06)

Proposed fix is up:

https://chromium-review.googlesource.com/c/chromium/src/+/2807255

### bb...@chromium.org (2021-04-06)

I think the fix is to copy the data before hashing and writing. I don't see anything in the Mojo code that prevents the renderer from writing to the shared memory after it's sent to the browser.

### ro...@google.com (2021-04-06)

Right, unfortunately I don't think we can ensure the browser has exclusive ownership of the region once it's passed, because OS support for that sort of thing just doesn't exist on some platforms.

### na...@chromium.org (2021-04-06)

Regarding https://crbug.com/chromium/1194046#c20 part (2) - I think this is not entirely correct. In the case of very large buffer, we have different cache layout. As per line 382:

    // 3. Very Large
    // [stream0] response time, size, checksum
    // [stream1] <empty>
    // [stream0 (checksum key entry)] <empty>
    // [stream1 (checksum key entry)] data

What we do in this case is to have *two* cache entries. One that takes the origin key we compute based on the process lock and stashes the checksum in the data. Then we write a second entry that uses the checksum as the lookup key and the actual script data.
On lookups, we compute the origin key based on the same two inputs - the script URL and the process lock. Then we do another lookup based on the SHA hash that we get back. So here is a list of steps to exploit this as site isolation bypass as far as I understand it:

* victim.com loads script foo.com/script.js. It writes two entries (v, f) -> sha, (sha) -> original content.
* attacker.com loads script foo.com/script.js. It writes two entries again - (a, f) -> sha, (sha) -> *altered content using this bug*
* victim.com gets reloaded or anoter page loads script foo.com/script.js. It does a lookup using (v, f) and gets back sha back. It then does a second lookup of (sha) and it gets back the altered content that the attacker cached.

The problem is that we effectively have content addressable cache for this case, which bypasses the origin protections we have in place. We can fix this in two ways - the proposed way of making a copy before computing the hash or we don't deduplicate across origins, which is what the current scheme is trying to do.

### ki...@chromium.org (2021-04-06)

Interesting, thanks a lot for the analysis made on this issue so far. Indeed the code is effectively doing content addressable cache, which itself should be okay as far as the content and hash matches and other general timing/history leak issue is not a concern. But when it is combined with TOCTOU yes this is pretty bad :(. I probably wasn't very aware of the big security aspect of BigBuffer, this could be more clearly documented.

### hi...@gmail.com (2021-04-07)

mythria@, Re to https://crbug.com/chromium/1194046#c21, the understanding is correct and I think copy the buffer before calculating the SHA can fix this issue too. 

### my...@chromium.org (2021-04-07)

[Empty comment from Monorail migration]

### cr...@chromium.org (2021-04-07)

Thanks everyone for the analysis here!  Copying the buffer seems like a good first step.  I think dcheng@ might be looking into whether similar TOCTOU issues might exist with other Mojo shared memory uses, where the value sent from the renderer is validated but then modified before use.

I'm also curious about the steps in nasko@'s https://crbug.com/chromium/1194046#c30, where the victim writes a good entry to the content addressable cache, and then the attacker overwrites it with a bad entry at the same checksum key.  If that happens, is there a reason we allow entries in the content addressable cache to be overwritten?  Seems like a value shouldn't change for a given key, so maybe we could prevent changes?  (That said, I'm unclear if it's necessary for the victim to write the good entry first for the attack to work-- nasko@ mentioned it might be, but at first glance the PoC seems to have the attacker write the entry first.)

### cr...@chromium.org (2021-04-07)

mythria@: Also, can you clarify which feature is being experimented with?  My understanding was that the Site Isolation aspects of the code cache fully launched back in M72 in https://crbug.com/chromium/812168-- that's not still experimental, right?  (Maybe it's just the de-duplication / content-addressable cache part?)  Thanks!

### my...@chromium.org (2021-04-07)

re c#35, Yes Site Isolation are fully launched in M72 and is fully enabled. I was only talking about de-duplication of the large entries in my earlier comment. As Bill clarified later, de-duplication feature is also enabled by default and the finch experiment is only changing the thresholds at which we trigger the de-duplication.

re c#34, I believe we don't overwrite the data if there was already an entry associated with it [1]. Though we only skip writing it if lengths match. Actually lengths should match if there is a valid entry there. We do have DCHECKs later to check the entry was empty if the lengths don't match. In a release build possibly this DCHECKs don't trigger and we end up overwriting the entry. Though just preventing overwriting entries isn't sufficient to stop the attack.

In the scenario nasko@ mentioned, we can just skip step 1 and still get the attacker to force malicious code on victim sites. So, I think it isn't important that victim has to store first.  Copying the data before we compute the key should prevent these attacks. 

[1] https://source.chromium.org/chromium/chromium/src/+/master:content/browser/code_cache/generated_code_cache.cc;l=577;drc=c72fbb03a13a55a11761912c96e5876de2cf15fb;bpv=1;bpt=1

### gi...@appspot.gserviceaccount.com (2021-04-07)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/cea0cb8eee9900308d9b43661e9faca449086940

commit cea0cb8eee9900308d9b43661e9faca449086940
Author: Bill Budge <bbudge@chromium.org>
Date: Wed Apr 07 16:55:55 2021

[GeneratedCodeCache] Copy large data before hashing and writing

- Makes a copy before hashing and writing large code entries.

Bug: chromium:1194046
Change-Id: Id5a6e6d3a04c83cfed2f18db53587d654d642fc0
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2807255
Reviewed-by: Nasko Oskov <nasko@chromium.org>
Reviewed-by: Mythri Alle <mythria@chromium.org>
Commit-Queue: Bill Budge <bbudge@chromium.org>
Cr-Commit-Position: refs/heads/master@{#870064}

[modify] https://crrev.com/cea0cb8eee9900308d9b43661e9faca449086940/content/browser/code_cache/generated_code_cache.cc


### bb...@chromium.org (2021-04-07)

[Empty comment from Monorail migration]

### [Deleted User] (2021-04-07)

[Empty comment from Monorail migration]

### [Deleted User] (2021-04-07)

Requesting merge to stable M89 because latest trunk commit (870064) appears to be after stable branch point (843830).

Requesting merge to beta M90 because latest trunk commit (870064) appears to be after beta branch point (857950).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-04-07)

This bug requires manual review: We are only 5 days from stable.
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://chromium.googlesource.com/chromium/src.git/+/master/docs/process/merge_request.md#when-to-request-a-merge
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on ToT?
4. Does this change need to be merged into other active release branches (M-1, M+1)?
5. Why are these changes required in this milestone after branch?
6. Is this a new feature?
7. If it is a new feature, is it behind a flag using finch?

Chrome OS Only:
8. Was the change reviewed and approved by the Eng Prod Representative? See Eng Prod ownership by component: http://go/cros-engprodcomponents

Please contact the milestone owner if you have questions.
Owners: govind@(Android), bindusuvarna@(iOS), cindyb@(ChromeOS), srinivassista@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### cr...@chromium.org (2021-04-08)

https://crbug.com/chromium/1194046#c36: Thanks!  Also, to leave a breadcrumb for dcheng@'s work mentioned in https://crbug.com/chromium/1194046#c34, https://crbug.com/chromium/1135729 is about broader copy-on-write semantics for Mojo shared memory.

### [Deleted User] (2021-04-08)

[Empty comment from Monorail migration]

### ad...@google.com (2021-04-15)

Approving merge to M90, branch 4430, assuming no stabilty (or performance?) concerns have appeared in Canary.

### bb...@chromium.org (2021-04-15)

Canary looks OK since the CL landed. There was a spike in browser crashes a few days later but it has recovered.

https://uma.googleplex.com/timeline_v2?sid=97f130b11ef3c4fa1c2204291e29868e

### [Deleted User] (2021-04-15)

[Empty comment from Monorail migration]

### ad...@google.com (2021-04-16)

Great, please go ahead and merge if you're happy.

### bb...@chromium.org (2021-04-16)

CL still needs an owner +1 or TPM override to land.

### na...@chromium.org (2021-04-16)

Do you have a link to the CL?

### bb...@chromium.org (2021-04-16)

Whoops, CL: https://chromium-review.googlesource.com/c/chromium/src/+/2827763

### na...@chromium.org (2021-04-16)

Stamped.

### bb...@chromium.org (2021-04-16)

Thanks!

### gi...@appspot.gserviceaccount.com (2021-04-16)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/66b9ad64f4a4158e847403f974569dc9ef7c50b3

commit 66b9ad64f4a4158e847403f974569dc9ef7c50b3
Author: Bill Budge <bbudge@chromium.org>
Date: Fri Apr 16 23:22:33 2021

[merge][90][GeneratedCodeCache] Copy large data before hashing and writing

- Makes a copy before hashing and writing large code entries.

(cherry picked from commit cea0cb8eee9900308d9b43661e9faca449086940)

Bug: chromium:1194046
Change-Id: Id5a6e6d3a04c83cfed2f18db53587d654d642fc0
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2807255
Reviewed-by: Nasko Oskov <nasko@chromium.org>
Reviewed-by: Mythri Alle <mythria@chromium.org>
Commit-Queue: Bill Budge <bbudge@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#870064}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2827763
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Commit-Queue: Nasko Oskov <nasko@chromium.org>
Reviewed-by: Bill Budge <bbudge@chromium.org>
Auto-Submit: Bill Budge <bbudge@chromium.org>
Cr-Commit-Position: refs/branch-heads/4430@{#1303}
Cr-Branched-From: e5ce7dc4f7518237b3d9bb93cccca35d25216cbe-refs/heads/master@{#857950}

[modify] https://crrev.com/66b9ad64f4a4158e847403f974569dc9ef7c50b3/content/browser/code_cache/generated_code_cache.cc


### ad...@google.com (2021-04-19)

[Empty comment from Monorail migration]

### ad...@google.com (2021-04-19)

[Empty comment from Monorail migration]

### ac...@chromium.org (2021-04-20)

[Empty comment from Monorail migration]

### gi...@google.com (2021-04-20)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-04-20)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/1028ffc9bd836eadc3fb89c3fb96fec7bd059557

commit 1028ffc9bd836eadc3fb89c3fb96fec7bd059557
Author: Bill Budge <bbudge@chromium.org>
Date: Tue Apr 20 15:22:33 2021

M86-LTS: [GeneratedCodeCache] Copy large data before hashing and writing

- Makes a copy before hashing and writing large code entries.

(cherry picked from commit cea0cb8eee9900308d9b43661e9faca449086940)

Bug: chromium:1194046
Change-Id: Id5a6e6d3a04c83cfed2f18db53587d654d642fc0
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2807255
Reviewed-by: Nasko Oskov <nasko@chromium.org>
Reviewed-by: Mythri Alle <mythria@chromium.org>
Commit-Queue: Bill Budge <bbudge@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#870064}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2838077
Reviewed-by: Bill Budge <bbudge@chromium.org>
Commit-Queue: Achuith Bhandarkar <achuith@chromium.org>
Owners-Override: Achuith Bhandarkar <achuith@chromium.org>
Cr-Commit-Position: refs/branch-heads/4240@{#1612}
Cr-Branched-From: f297677702651916bbf65e59c0d4bbd4ce57d1ee-refs/heads/master@{#800218}

[modify] https://crrev.com/1028ffc9bd836eadc3fb89c3fb96fec7bd059557/content/browser/code_cache/generated_code_cache.cc


### ad...@google.com (2021-04-20)

[Empty comment from Monorail migration]

### as...@google.com (2021-04-21)

[Empty comment from Monorail migration]

### am...@google.com (2021-04-22)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2021-04-23)

Congratulations, higongguang@! The VRP Panel has decided to award you $15,000 for this report. Nice work!

### hi...@gmail.com (2021-04-23)

Thanks for the bounty, @amyressler

### am...@google.com (2021-04-26)

[Empty comment from Monorail migration]

### am...@google.com (2021-04-26)

[Empty comment from Monorail migration]

### [Deleted User] (2021-07-28)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1194046?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>JavaScript>Runtime, Internals>Network>Cache, Internals>Sandbox>SiteIsolation]
[Monorail mergedwith: crbug.com/chromium/1194048]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40055380)*
