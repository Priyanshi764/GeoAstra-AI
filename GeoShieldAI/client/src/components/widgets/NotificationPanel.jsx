const alerts=[

{

time:"14:01",

title:"Credential Leak",

target:"IIITDM Jabalpur",

severity:"HIGH"

},

{

time:"14:04",

title:"Fake Banking APK",

target:"SBI Bhopal",

severity:"CRITICAL"

},

{

time:"14:08",

title:"Fake Aadhaar",

target:"Municipal Corporation",

severity:"HIGH"

}

]

export default function NotificationPanel(){

return(

<div className="bg-[#111827] rounded-xl p-6 border border-gray-700">

<h2 className="text-xl font-bold mb-5">

🚨 Recent Alerts

</h2>

{

alerts.map((item,index)=>(

<div

key={index}

className="border-b border-gray-700 py-3"

>

<p className="text-sm text-gray-400">

{item.time}

</p>

<h3 className="font-semibold">

{item.title}

</h3>

<p className="text-blue-400">

{item.target}

</p>

<p className="text-red-400">

{item.severity}

</p>

</div>

))

}

</div>

)

}