mapbox费用:
	https://www.mapbox.com/pricing/#navigation

tableue:
	https://zhuanlan.zhihu.com/p/29304685
	https://zhuanlan.zhihu.com/p/28666551
	https://zhuanlan.zhihu.com/p/32733049

https://www.ted.com/talks/amy_cuddy_your_body_language_shapes_who_you_are?language=zh-cn#t-88637X

the agency responsible for licensing and 
	* regulating New York City's medallion (yellow) taxis, 
	* street hail livery (green) taxis,
		 They may only pick up above W 110 St/E 96th St in Manhattan and in the boroughs
	* for-hire vehicles (FHVs), commuter vans, and paratransit vehicles
		- high-volume for-hire vehicle bases  
		- (bases for companies dispatching 10,000+ trip per day, meaning Uber, Lyft, Via, and Juno),
		- community livery bases, luxury limousine bases, and black car bases. 

		- In 2015, only the 
			dispatching base number, 
			pickup datetime, and the 
			location of the pickup (see section on matching zone IDs below)
		- In summer of 2017, the TLC mandated that the companies provide the 
			drop-off date/time and the 
			drop-off location.
		- In the 2018 FHV records, there is a field called SR_Flag, share chain
			shared trips	null
			unshared trips	1

PULocationid & DOLocationID
	numbers ranging from 1-263

For shared trips, the value is 1. For non-shared rides, this field is null.
* NOTICE
	TLC cannot guarantee their accuracy.