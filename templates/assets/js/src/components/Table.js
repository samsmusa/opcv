import axios from "axios";
import React from "react";
import { toast } from "react-toastify";

export default function Table({ data, setRelaod }) {
  const handleDelete = (id) => {
    setRelaod(true);
    axios
      .delete(`/api/upload-sheet/${id}`)
      .then((res) => {
        setRelaod(false);
        toast.success("file deleted successfully");
      })
      .catch((err) => {
        toast.error(err.message);
        setRelaod(false);
      });
  };
  return (
    <div class="relative overflow-x-auto shadow-md sm:rounded-lg">
      <table class="w-full text-sm text-left text-gray-500 dark:text-gray-400">
        <thead class="text-xs text-gray-700 uppercase bg-gray-50 dark:bg-gray-700 dark:text-gray-400">
          <tr>
            <th scope="col" class="px-6 py-3">
              id
            </th>
            <th scope="col" class="px-6 py-3">
              exam
            </th>
            <th scope="col" class="px-6 py-3">
              section
            </th>
            <th scope="col" class="px-6 py-3">
              subject
            </th>
            <th scope="col" class="px-6 py-3">
              File
            </th>
            <th scope="col" class="px-6 py-3">
              action
            </th>
          </tr>
        </thead>
        <tbody>
          {data?.map((el) => {
            return (
              <tr
                key={el?.id}
                class="bg-white border-b dark:bg-gray-800 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-600"
              >
                <th
                  scope="row"
                  class="px-6 py-4 font-medium text-gray-900 whitespace-nowrap dark:text-white"
                >
                  {el?.id}
                </th>
                <td class="px-6 py-4">{el?.exam_title}</td>
                <td class="px-6 py-4">{el?.section_title}</td>
                <td class="px-6 py-4">{el?.subject_title}</td>
                <td class="px-6 py-4">
                  <a href={el?.file} download>
                    <button
                      type="button"
                      class="focus:outline-none text-white bg-green-700 hover:bg-green-800 focus:ring-4 focus:ring-green-300 font-medium rounded-lg text-sm px-5 py-2.5 mr-2 mb-2 dark:bg-green-600 dark:hover:bg-green-700 dark:focus:ring-green-800"
                    >
                      download
                    </button>
                  </a>
                </td>
                <td class="px-6 py-4">
                  <button
                    onClick={() => handleDelete(el?.id)}
                    type="button"
                    class="focus:outline-none text-white bg-green-700 hover:bg-green-800 focus:ring-4 focus:ring-green-300 font-medium rounded-lg text-sm px-5 py-2.5 mr-2 mb-2 dark:bg-green-600 dark:hover:bg-green-700 dark:focus:ring-green-800"
                  >
                    Delete
                  </button>
                </td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
}
