import axios from "axios";
import React from "react";
import { useForm } from "react-hook-form";
import { toast } from "react-toastify";
import Table3 from "../components/Table3";

export default function OmrResults() {
  const [students, setStudents] = React.useState([]);
  const [classes, setClasses] = React.useState([]);
  const [exams, setExams] = React.useState([]);
  const [relaod, setRelaod] = React.useState(false);
  const [result, setResult] = React.useState([]);

  React.useEffect(() => {
    let url = "http://127.0.0.1:8000/omr/student/";
    axios.get(url).then((response) => {
      setStudents(response.data);
      console.log(response.data);
    });
    url = "http://127.0.0.1:8000/omr/exam/";
    axios.get(url).then((response) => {
      setExams(response.data);
    });
    url = "http://127.0.0.1:8000/omr/class/";
    axios.get(url).then((response) => {
      setClasses(response.data);
    });
    url = "http://127.0.0.1:8000/omr/resultlist/";
    axios.get(url).then((response) => {
      setResult(response.data);
    });
  }, []);
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
    let url = `http://127.0.0.1:8000/omr/resultlist/?exam=${data.exam}&student=${data.student}`;
    axios
      .get(url)
      .then((res) => {
        setResult(res.data);
        setRelaod(false);
      })
      .catch((err) => toast.error(err.message));
  };
  return (
    <div className="container mx-auto">
      <div class="w-full flex justify-center p-4 bg-white border border-gray-200 rounded-lg shadow sm:p-6 md:p-8 dark:bg-gray-800 dark:border-gray-700">
        <form class="space-y-6 w-full" onSubmit={handleSubmit(onSubmit)}>
          <div className="flex flex-row">
            <div class="flex flex-col self-center  w-1/2 justify-between p-4 leading-normal">
              <label
                for="countries"
                class="block mb-2 text-sm font-medium text-gray-900 dark:text-white"
              >
                Select Exam
              </label>
              <select
                {...register("exam")}
                id="countries"
                class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
              >
                {exams?.map((el) => (
                  <option value={el?.id}>{el?.name}</option>
                ))}
              </select>
            </div>
            <div class="flex flex-col self-center  w-1/2 justify-between p-4 leading-normal">
              <label
                for="Student"
                class="block mb-2 text-sm font-medium text-gray-900 dark:text-white"
              >
                Select Student
              </label>
              <select
                {...register("student")}
                id="Student"
                class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
              >
                {students?.map((el) => (
                  <option key={el?.id} value={el?.id}>
                    {el?.first_name}
                  </option>
                ))}
              </select>
            </div>
            <div class="flex flex-col self-center  w-1/2 justify-between p-4 leading-normal">
              <label
                for="classes"
                class="block mb-2 text-sm font-medium text-gray-900 dark:text-white"
              >
                Select Class
              </label>
              <select
                {...register("classes")}
                id="classes"
                class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
              >
                {classes?.map((el) => (
                  <option key={el?.id} value={el?.id}>
                    {el?.name}
                  </option>
                ))}
              </select>
            </div>
          </div>
          <button
            type="submit"
            class=" text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800"
          >
            Get Result
          </button>
        </form>
      </div>

      <p class="max-w-lg text-left my-4 text-3xl font-semibold leading-normal text-gray-900 dark:text-white">
        Result
      </p>
      {result && <Table3 data={result} />}
    </div>
  );
}
