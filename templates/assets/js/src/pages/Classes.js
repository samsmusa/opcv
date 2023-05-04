import React from "react";
import axios from "axios";
import { useForm } from "react-hook-form";
import { toast } from "react-toastify";
import ClassTable from "../components/ClassTable";

export default function Classes() {
  const [relaod, setRelaod] = React.useState(false);
  const {
    register,
    handleSubmit,
    watch,
    reset,
    formState: { errors },
  } = useForm();

  const onSubmit = (data) => {
    console.log(data);
    setRelaod(true);
    let url = "http://127.0.0.1:8000/omr/class/";
    axios
      .post(url, data, {
        headers: {
          "content-type": "multipart/form-data",
        },
      })
      .then((res) => {
        console.log(res.data);
        reset();
        setRelaod(false);
        toast.success("new class created successfully");
      })
      .catch((err) => toast.error(err.message));
  };
  return (
    <div className="container mx-auto grid grid-cols-3 h-screen">
      <div className="col-span-1">
        <div class="w-full max-w-sm p-4 bg-white border border-gray-200 rounded-lg shadow sm:p-6 md:p-8 dark:bg-gray-800 dark:border-gray-700">
          <form class="space-y-6" onSubmit={handleSubmit(onSubmit)}>
            <h5 class="text-xl font-medium text-gray-900 dark:text-white">
              Create New Class
            </h5>
            <div>
              <label
                for="first_name"
                class="block mb-2 text-left text-sm font-medium text-gray-900 dark:text-white"
              >
                Name
              </label>
              <input
                type="text"
                name="first_name"
                id="first_name"
                class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-600 dark:border-gray-500 dark:placeholder-gray-400 dark:text-white"
                {...register("name")}
              />
            </div>

            <button
              type="submit"
              class="w-full text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800"
            >
              Create Class
            </button>
          </form>
        </div>
      </div>
      <div class="col-span-2">
        <ClassTable reload={relaod} />
      </div>
    </div>
  );
}
