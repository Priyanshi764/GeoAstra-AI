export default function ThreatTrendWidget(){

return(

<div className="bg-[#111827] rounded-xl p-6 border border-gray-700">

<h2 className="text-xl font-bold mb-6">

📈 Threat Trend

</h2>

<div className="space-y-5">

<div>

<p>

High

</p>

<div className="w-full h-4 bg-gray-700 rounded">

<div className="w-[90%] h-4 bg-red-500 rounded"></div>

</div>

</div>

<div>

<p>

Medium

</p>

<div className="w-full h-4 bg-gray-700 rounded">

<div className="w-[60%] h-4 bg-yellow-500 rounded"></div>

</div>

</div>

<div>

<p>

Low

</p>

<div className="w-full h-4 bg-gray-700 rounded">

<div className="w-[35%] h-4 bg-green-500 rounded"></div>

</div>

</div>

</div>

</div>

)

}