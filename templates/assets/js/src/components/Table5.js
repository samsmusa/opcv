import React from "react";

export default function Table5({ data }) {
  return (
    <div class="relative overflow-x-auto shadow-md sm:rounded-lg">
      <table class="w-full text-sm text-left text-gray-500 dark:text-gray-400">
        <thead class="text-xs text-gray-700 uppercase bg-gray-50 dark:bg-gray-700 dark:text-gray-400">
          <tr>
            <th scope="col" class="px-6 py-3">
              id
            </th>
            <th scope="col" class="px-6 py-3">
              Name
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
                <td class="px-6 py-4">{el?.name}</td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
}
