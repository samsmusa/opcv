import React from "react";
import axios from "axios";

import Table5 from "./Table5";

export default function ExamTable({ reload }) {
  const [student, setStudent] = React.useState([]);
  React.useEffect(() => {
    let url = "http://127.0.0.1:8000/omr/exam/";
    axios.get(url).then((response) => {
      setStudent(response.data);
    });
  }, [reload]);
  return <Table5 data={student} />;
}
