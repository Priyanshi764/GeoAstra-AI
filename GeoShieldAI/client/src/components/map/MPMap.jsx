import { MapContainer, TileLayer, CircleMarker, Popup } from "react-leaflet";

const locations = [

{
name:"Bhopal",
lat:23.2599,
lng:77.4126,
risk:"Critical",
alerts:12,
color:"red"
},

{
name:"Jabalpur",
lat:23.1815,
lng:79.9864,
risk:"High",
alerts:8,
color:"orange"
},

{
name:"Indore",
lat:22.7196,
lng:75.8577,
risk:"Medium",
alerts:5,
color:"yellow"
},

{
name:"Gwalior",
lat:26.2183,
lng:78.1828,
risk:"Low",
alerts:2,
color:"green"
}

];

export default function MPMap(){

return(

<div className="bg-[#111827] rounded-xl p-4 border border-gray-700">

<h2 className="text-xl font-bold mb-4">

🗺 Madhya Pradesh Threat Map

</h2>

<MapContainer

center={[23.6,78.9]}

zoom={7}

style={{height:"500px",width:"100%"}}

>

<TileLayer

url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"

/>

{

locations.map((city,index)=>(

<CircleMarker

key={index}

center={[city.lat,city.lng]}

radius={18}

pathOptions={{

color:city.color,

fillColor:city.color,

fillOpacity:0.7

}}

>

<Popup>

<h2>{city.name}</h2>

<p>

Risk :

{city.risk}

</p>

<p>

Alerts :

{city.alerts}

</p>

</Popup>

</CircleMarker>

))

}

</MapContainer>

</div>

)

}