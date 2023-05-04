import React from "react";

export default function Table2({ data }) {
  console.log(data);
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
              action
            </th>
          </tr>
        </thead>
        <tbody>
          {data?.map((el) => {
            return (
              <tr
                key={"omr-table-data" + el?.id}
                class="bg-white border-b dark:bg-gray-800 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-600"
              >
                <td class="px-6 py-4">{el?.id}</td>
                <td class="px-6 py-4">{el?.exam_title}</td>
                <td class="px-6 py-4">{el?.section_title}</td>
                <td class="px-6 py-4">{el?.subject_title}</td>
                <td class="px-6 py-4">
                  <button
                    type="button"
                    class="focus:outline-none text-white bg-yellow-400 hover:bg-yellow-500 focus:ring-4 focus:ring-yellow-300 font-medium rounded-lg text-sm px-5 py-2.5 mr-2 mb-2 dark:focus:ring-yellow-900"
                  >
                    Start Scan
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
