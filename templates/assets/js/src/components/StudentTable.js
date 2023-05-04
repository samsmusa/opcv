import React from "react";
import axios from "axios";
import Table4 from "./Table4";

export default function StudentTable({ reload }) {
  const [student, setStudent] = React.useState([]);
  React.useEffect(() => {
    let url = "http://127.0.0.1:8000/omr/student/";
    axios.get(url).then((response) => {
      setStudent(response.data);
    });
  }, [reload]);
  return <Table4 data={student} />;
}
