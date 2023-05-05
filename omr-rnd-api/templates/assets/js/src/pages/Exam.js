import React from "react";
import axios from "axios";
import { useForm } from "react-hook-form";
import { toast } from "react-toastify";
import ExamTable from "../components/ExamTable";

export default function Exam() {
  const [relaod, setRelaod] = React.useState(false);
  const [classes, setClasses] = React.useState([]);
  const [students, setStudents] = React.useState([]);
  const {
    register,
    handleSubmit,
    watch,
    reset,
    formState: { errors },
  } = useForm();

  const onSubmit = (data) => {
    setRelaod(true);
    let url = "http://127.0.0.1:8000/omr/exam/";
    axios
      .post(url, data, {
        headers: {
          "content-type": "application/json",
        },
      })
      .then((res) => {
        console.log(res.data);
        reset();
        setRelaod(false);
        toast.success("new Exam created successfully");
      })
      .catch((err) => toast.error(err.message));
  };
  React.useEffect(() => {
    let url = "/api/exam-list/";
    axios.get(url).then((response) => {
      setClasses(response.data.data);
    });
    url = "http://127.0.0.1:8000/omr/student/";
    axios.get(url).then((response) => {
      setStudents(response.data);
    });
  }, []);
  return (
    <div className="container mx-auto grid grid-cols-3 h-screen">
      <div className="col-span-1">
        <div class="w-full max-w-sm p-4 bg-white border border-gray-200 rounded-lg shadow sm:p-6 md:p-8 dark:bg-gray-800 dark:border-gray-700">
          <form class="space-y-6" onSubmit={handleSubmit(onSubmit)}>
            <h5 class="text-xl font-medium text-gray-900 dark:text-white">
              Create New Exam
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

            <div>
              <label
                for="countries"
                class="block mb-2 text-left text-sm font-medium text-gray-900 dark:text-white"
              >
                Select Class
              </label>
              <select
                {...register("classes", { required: true })}
                id="countries"
                class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
              >
                {classes?.map((el) => (
                  <option value={el?.id}>{el?.name}</option>
                ))}
              </select>
            </div>

            <div>
              <label
                for="countries"
                class="block mb-2 text-left text-sm font-medium text-gray-900 dark:text-white"
              >
                Select Students
              </label>
              <select
                multiple
                {...register("students", { required: true })}
                id="countries"
                class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
              >
                {students?.map((el) => (
                  <option value={el?.id}>{el?.first_name}</option>
                ))}
              </select>
            </div>

            <button
              type="submit"
              class="w-full text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800"
            >
              Create Exam
            </button>
          </form>
        </div>
      </div>
      <div class="col-span-2">
        <ExamTable reload={relaod} />
      </div>
    </div>
  );
}
