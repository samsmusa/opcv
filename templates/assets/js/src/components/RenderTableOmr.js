import axios from "axios";
import React from "react";
import Table from "./Table";

export default function RenderTableOmr({ reload, setRelaod }) {
  const [omr, setOmr] = React.useState([]);

  React.useEffect(() => {
    const url = "/api/upload-sheet/";
    axios.get(url).then((response) => {
      setOmr(response.data);
    });
  }, [reload]);
  return <Table data={omr} setRelaod={setRelaod} />;
}
