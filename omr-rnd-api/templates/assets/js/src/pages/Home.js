import axios from "axios";
import React from "react";
import { useForm } from "react-hook-form";
import RenderTableOmr from "../components/RenderTableOmr";
import { toast } from "react-toastify";
import SelectExam from "../components/SelectExam";
import SelectSection from "../components/SelectSection";
import SelectSubject from "../components/SelectSubject";
import SelectQuestionCount from "../components/SelectQuestionCount";

export const handleObj = (obj) => {
  return JSON.stringify(obj);
};

export const parseObj = (str) => {
  return JSON.parse(str);
};
export default function Home() {
  const [relaod, setRelaod] = React.useState(false);
  const [examid, setExamid] = React.useState(null);
  const [sectionid, setSectionid] = React.useState(null);
  const [subjectid, setSubjectid] = React.useState(null);
  const [totalstudent, setTotalstudent] = React.useState(null);
  const {
    register,
    handleSubmit,
    watch,
    getValues,
    reset,
    formState: { errors },
  } = useForm();

  React.useEffect(() => {
    if (
      getValues("exam_id") &&
      getValues("section_id") &&
      getValues("subject_id")
    ) {
      const exam = parseObj(getValues("exam_id"));
      const section = parseObj(getValues("section_id"));
      const subject = parseObj(getValues("subject_id"));
      axios
        .get(`/api/student-list/${exam.id}/${section.id}/${subject.id}`)
        .then((response) => {
          setTotalstudent(response.data.data.length);
        })
        .catch((err) => {
          console.log(err);
        });
    }
  }, [watch()]);

  const onSubmit = (data) => {
    setRelaod(true);
    const formData = new FormData();
    formData.append("file", data.file[0]);
    const exam = parseObj(data.exam_id);
    const section = parseObj(data.section_id);
    const subject = parseObj(data.subject_id);
    formData.append("exam_id", exam.id);
    formData.append("section_id", section.id);
    formData.append("subject_id", subject.id);
    formData.append("exam_title", exam.value);
    formData.append("section_title", section.value);
    formData.append("subject_title", subject.value);
    formData.append("question_count", data.question_count);
    let url = "/api/upload-sheet/";
    axios
      .post(url, formData, {
        headers: {
          "content-type": "multipart/form-data",
        },
      })
      .then((res) => {
        reset();
        setRelaod(false);
        toast.success("file uploaded successfully");
      })
      .catch((err) => {
        if (err?.response?.data?.file) {
          toast.error(err.response.data.file[0]);
        } else if (err?.response?.data) {
          toast.error(err.response.data[0]);
        } else {
          toast.error(err.message);
        }
      });
  };

  return (
    <div className="container mx-auto">
      <div class="w-full flex justify-center p-4 bg-white border border-gray-200 rounded-lg shadow sm:p-6 md:p-8 dark:bg-gray-800 dark:border-gray-700">
        <form class="space-y-6 w-full" onSubmit={handleSubmit(onSubmit)}>
          <div className="flex flex-row">
            <div class="flex flex-col items-center bg-white border border-gray-200 rounded-lg shadow md:flex-row w-1/2 hover:bg-gray-100 dark:border-gray-700 dark:bg-gray-800 dark:hover:bg-gray-700">
              <div class="flex items-center justify-center w-full">
                <label
                  for="dropzone-file"
                  class="flex flex-col items-center justify-center w-full h-64 border-2 border-gray-300 border-dashed rounded-lg cursor-pointer bg-gray-50 dark:hover:bg-bray-800 dark:bg-gray-700 hover:bg-gray-100 dark:border-gray-600 dark:hover:border-gray-500 dark:hover:bg-gray-600"
                >
                  <div class="flex flex-col items-center justify-center pt-5 pb-6">
                    <svg
                      aria-hidden="true"
                      class="w-10 h-10 mb-3 text-gray-400"
                      fill="none"
                      stroke="currentColor"
                      viewBox="0 0 24 24"
                      xmlns="http://www.w3.org/2000/svg"
                    >
                      <path
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        stroke-width="2"
                        d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"
                      ></path>
                    </svg>
                    <p class="mb-2 text-sm text-gray-500 dark:text-gray-400">
                      <span class="font-semibold">Click to upload</span> or drag
                      and drop
                    </p>
                    <p class="text-xs text-gray-500 dark:text-gray-400">
                      Compressed files (only zip) are allowed to be uploaded
                    </p>
                  </div>
                  <input
                    id="dropzone-file"
                    type="file"
                    class="hidden"
                    {...register("file")}
                    required
                  />
                </label>
              </div>
            </div>
            <div class="flex flex-col self-center  w-1/2 justify-between p-4 leading-normal">
              <SelectExam register={register} setExamid={setExamid} />
              {examid && (
                <div className="flex items-center justify-start">
                  <SelectSection
                    register={register}
                    exam_id={examid}
                    setSectionid={setSectionid}
                  />
                  <SelectSubject
                    register={register}
                    exam_id={examid}
                    setSubjectid={setSubjectid}
                  />
                  <SelectQuestionCount register={register} />
                </div>
              )}
              {totalstudent && (
                <p className="p-2 text-left text-gray-400 text-sm">
                  Upload zip file contains {totalstudent + 1} OMR with 1
                  'result' named file
                </p>
              )}
            </div>
          </div>
          <button
            type="submit"
            class=" text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800"
          >
            Submit OMR
          </button>
        </form>
      </div>
      <p class="max-w-lg text-left my-4 text-3xl font-semibold leading-normal text-gray-900 dark:text-white">
        All Uploads
      </p>
      <RenderTableOmr reload={relaod} setRelaod={setRelaod} />
    </div>
  );
}
