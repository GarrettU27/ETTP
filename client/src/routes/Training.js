import {useLoaderData} from "react-router-dom";

function Training() {
  const image = useLoaderData()

  return(
    <img src={image}  alt={"ECG Plot"}/>
  )
}

export default Training
