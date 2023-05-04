import axios from "axios";
import React from "react";
import { useForm } from "react-hook-form";
import Table2 from "../components/Table2";
import { toast } from "react-toastify";

export default function OmrScan() {
  const [omr, setOmr] = React.useState([]);
  const [classes, setClasses] = React.useState([]);
  const [relaod, setRelaod] = React.useState(false);
  const [result, setResult] = React.useState([]);

  React.useEffect(() => {
    const url = "/api/upload-sheet/";
    axios.get(url).then((response) => {
      setOmr(response.data);
    });
  }, [relaod]);
  // const {
  //   register,
  //   handleSubmit,
  //   watch,
  //   reset,
  //   formState: { errors },
  // } = useForm();

  // const onSubmit = (data) => {
  //   console.log(data);
  //   setRelaod(true);
  //   let url = "http://127.0.0.1:8000/omr/result/";
  //   axios
  //     .post(url, data, {
  //       headers: {
  //         "content-type": "application/json",
  //       },
  //     })
  //     .then((res) => {
  //       console.log(res.data);
  //       setResult(res.data);
  //       reset();
  //       setRelaod(false);
  //       toast.success("Omr result set successfully");
  //     })
  //     .catch((err) => toast.error(err.message));
  // };
  return (
    <div className="container mx-auto">
      {/* <div class="w-full flex justify-center p-4 bg-white border border-gray-200 rounded-lg shadow sm:p-6 md:p-8 dark:bg-gray-800 dark:border-gray-700"> */}
      {result && <Table2 data={omr} />}
      {/* </div> */}
    </div>
  );
}
