import {useLoaderData} from "react-router-dom";

function Training() {
  const image = useLoaderData()

  return(
    <img width={"100%"} src={image}  alt={"ECG Plot"}/>
  )
}

export default Training
