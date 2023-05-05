import axios from "axios";
import React from "react";
import { handleObj, parseObj } from "../pages/Home";

export default function SelectSection({ register, exam_id, setSectionid }) {
  const [sections, setSections] = React.useState([]);
  const handleSelect = (event) => {
    setSectionid(parseObj(event.target.value).id);
  };

  React.useEffect(() => {
    const url = `/api/section-list/${exam_id}/`;
    axios.get(url).then((response) => {
      let data = response?.data?.data || [];
      setSections(data);
    });
  }, [exam_id]);
  return (
    <div className="p-2 w-1/2">
      <label
        for="countries"
        class="block mb-2 text-sm font-medium text-gray-900 dark:text-white"
      >
        Select Section
      </label>
      <select
        {...register("section_id", { required: true })}
        onChange={handleSelect}
        id="countries"
        class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
      >
        <option selected disabled value={handleObj({ id: 0 })}>
          select an section...
        </option>
        {sections?.map((el) => (
          <option
            key={"section" + el?.id}
            value={handleObj({ id: el?.id, value: el?.title })}
          >
            {el?.title}
          </option>
        ))}
      </select>
    </div>
  );
}
