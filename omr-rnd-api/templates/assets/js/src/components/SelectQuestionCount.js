import axios from "axios";
import React from "react";
import { handleObj, parseObj } from "../pages/Home";

export default function SelectQuestionCount({ register, exam_id }) {
  return (
    <div className="p-2 w-1/2">
      <label
        for="phone"
        class="block mb-2 text-sm font-medium text-gray-900 dark:text-white"
      >
        Number of Question
      </label>
      <input
        type="number"
        id="phone"
        class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
        placeholder="40"
        pattern="[0-9]{3}-[0-9]{2}-[0-9]{3}"
        {...register("question_count", { required: true, min: 1, max: 60 })}
      />
    </div>
  );
}
