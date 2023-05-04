import axios from "axios";
import React from "react";
import { handleObj } from "../pages/Home";

export default function SelectSubject({ register, exam_id }) {
  const [sections, setSections] = React.useState([]);

  React.useEffect(() => {
    const url = `/api/subject-list/${exam_id}/`;
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
        Select subject
      </label>
      <select
        {...register("subject_id", { required: true })}
        id="countries"
        class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
      >
        {sections?.map((el) => (
          <option
            key={"subject_id" + el?.subject_id}
            value={handleObj({ id: el?.subject_id, value: el?.title })}
          >
            {el?.title}
          </option>
        ))}
      </select>
    </div>
  );
}
