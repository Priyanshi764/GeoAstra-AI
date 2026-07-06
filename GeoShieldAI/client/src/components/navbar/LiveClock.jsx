import { useEffect, useState } from "react";

export default function LiveClock() {

  const [time, setTime] = useState("");

  useEffect(() => {

    const interval = setInterval(() => {

      const now = new Date();

      setTime(

        now.toLocaleString("en-IN", {

          dateStyle: "medium",

          timeStyle: "medium",

        })

      );

    }, 1000);

    return () => clearInterval(interval);

  }, []);

  return (

    <span className="text-gray-300">

      {time}

    </span>

  );

}