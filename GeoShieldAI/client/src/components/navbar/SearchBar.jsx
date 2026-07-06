import { FaSearch } from "react-icons/fa";

export default function SearchBar() {

  return (

    <div className="flex items-center bg-[#1F2937] rounded-lg px-4 py-2 w-96">

      <FaSearch className="text-gray-400" />

      <input
        type="text"
        placeholder="Search threats, organizations..."
        className="bg-transparent outline-none ml-3 w-full text-white"
      />

    </div>

  );

}
