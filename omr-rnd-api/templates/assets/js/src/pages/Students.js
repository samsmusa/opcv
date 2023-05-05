import React from "react";
import Table4 from "../components/Table4";
import axios from "axios";
import StudentTable from "../components/StudentTable";
import { useForm } from "react-hook-form";
import { toast } from "react-toastify";

export default function Students() {
  const [relaod, setRelaod] = React.useState(false);
  const [classes, setClasses] = React.useState([]);
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
    let url = "http://127.0.0.1:8000/omr/student/";
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
        toast.success("new student created successfully");
      })
      .catch((err) => toast.error(err.message));
  };
  React.useEffect(() => {
    const url = "http://127.0.0.1:8000/omr/class/";
    axios.get(url).then((response) => {
      setClasses(response.data);
    });
  }, []);
  return (
    <div className="container mx-auto grid grid-cols-3 h-screen">
      <div className="col-span-1">
        <div class="w-full max-w-sm p-4 bg-white border border-gray-200 rounded-lg shadow sm:p-6 md:p-8 dark:bg-gray-800 dark:border-gray-700">
          <form class="space-y-6" onSubmit={handleSubmit(onSubmit)}>
            <h5 class="text-xl font-medium text-gray-900 dark:text-white">
              Create New Student
            </h5>
            <div>
              <label
                for="first_name"
                class="block mb-2 text-left text-sm font-medium text-gray-900 dark:text-white"
              >
                First Name
              </label>
              <input
                type="text"
                name="first_name"
                id="first_name"
                class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-600 dark:border-gray-500 dark:placeholder-gray-400 dark:text-white"
                {...register("first_name")}
              />
            </div>

            <div>
              <label
                for="last_name"
                class="block mb-2 text-left text-sm font-medium text-gray-900 dark:text-white"
              >
                Last Name
              </label>
              <input
                type="text"
                name="last_name"
                id="last_name"
                class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-600 dark:border-gray-500 dark:placeholder-gray-400 dark:text-white"
                {...register("last_name")}
              />
            </div>

            <div>
              <label
                for="user_name"
                class="block mb-2 text-left text-sm font-medium text-gray-900 dark:text-white"
              >
                User Name
              </label>
              <input
                type="text"
                name="user_name"
                id="user_name"
                class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-600 dark:border-gray-500 dark:placeholder-gray-400 dark:text-white"
                {...register("user_name", { required: true })}
              />
            </div>

            <div>
              <label
                for="roll"
                class="block mb-2 text-left text-sm font-medium text-gray-900 dark:text-white"
              >
                Roll
              </label>
              <input
                type="number"
                name="roll"
                id="roll"
                class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-600 dark:border-gray-500 dark:placeholder-gray-400 dark:text-white"
                {...register("roll", { required: true, min: 1 })}
              />
            </div>
            <div>
              <label
                for="countries"
                class="block mb-2 text-left text-sm font-medium text-gray-900 dark:text-white"
              >
                Select Class
              </label>
              <select
                {...register("class_name", { required: true })}
                id="countries"
                class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
              >
                {classes?.map((el) => (
                  <option value={el.id}>{el.name}</option>
                ))}
              </select>
            </div>

            <button
              type="submit"
              class="w-full text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800"
            >
              Create Student
            </button>
          </form>
        </div>
      </div>
      <div class="col-span-2">
        <StudentTable reload={relaod} />
      </div>
    </div>
  );
}
