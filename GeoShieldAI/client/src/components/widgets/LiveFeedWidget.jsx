const feed=[

{

time:"14:01",

message:"Selling credentials of IIITDM Jabalpur",

risk:"HIGH"

},

{

time:"14:03",

message:"Need mule accounts in Bhopal",

risk:"HIGH"

},

{

time:"14:05",

message:"Fake Banking APK targeting SBI",

risk:"CRITICAL"

},

{

time:"14:09",

message:"Investment scam targeting Indore",

risk:"MEDIUM"

}

]

export default function LiveFeedWidget(){

return(

<div className="bg-[#111827] rounded-xl p-6 border border-gray-700 h-full">

<h2 className="text-xl font-bold mb-5">

📡 Live Threat Feed

</h2>

<div className="space-y-4">

{

feed.map((item,index)=>(

<div

key={index}

className="border-b border-gray-700 pb-3"

>

<p className="text-gray-400 text-sm">

{item.time}

</p>

<p>

{item.message}

</p>

<p className="text-red-400">

{item.risk}

</p>

</div>

))

}

</div>

</div>

)

}