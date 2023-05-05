import axios from "axios";
import React from "react";
import { handleObj, parseObj } from "../pages/Home";

export default function SelectExam({ register, setExamid }) {
  const [exams, setExams] = React.useState([]);

  const handleSelect = (event) => {
    setExamid(parseObj(event.target.value).id);
  };

  React.useEffect(() => {
    const url = "api/exam-list/";
    axios.get(url).then((response) => {
      let data = response?.data?.data || [];
      setExams(data);
    });
  }, []);
  return (
    <div>
      <label
        for="countries"
        class="block mb-2 text-sm font-medium text-gray-900 dark:text-white"
      >
        Select Exam
      </label>
      <select
        {...register("exam_id", { required: true })}
        onChange={handleSelect}
        id="countries"
        class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
      >
        <option selected disabled value={handleObj({ id: 0 })}>
          select an Exam...
        </option>
        {exams?.map((el) => (
          <option
            key={"exam" + el?.id}
            value={handleObj({ id: el?.id, value: el?.exam_title })}
          >
            {el?.exam_title + "--" + el?.exam_title}
          </option>
        ))}
      </select>
    </div>
  );
}
